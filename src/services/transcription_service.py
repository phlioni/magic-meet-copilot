# src/services/transcription_service.py

import os
from google.cloud import speech
import sounddevice as sd
import queue
import threading
from dotenv import load_dotenv

def set_google_credentials():
    load_dotenv()
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path and os.path.exists(credentials_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        print("✅ Credenciais do Google configuradas com sucesso.")
    else:
        print("❌ AVISO: GOOGLE_APPLICATION_CREDENTIALS não encontrado ou caminho inválido no .env")

class TranscriptionService:
    def __init__(self, on_transcription_update):
        self.client = None
        self.on_transcription_update = on_transcription_update
        self._buff = queue.Queue()
        self.is_running = False
        self.thread = None
        self.stream = None
        # --- NOVA LÓGICA DE GERENCIAMENTO DE TEXTO ---
        self.final_transcripts = []

    def _audio_generator(self):
        while self.is_running:
            chunk = self._buff.get()
            if chunk is None:
                return
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    def _listen_print_loop(self, responses):
        try:
            print("... Aguardando respostas do Google ...")
            for response in responses:
                if not self.is_running:
                    break

                if not response.results:
                    continue

                result = response.results[0]
                if not result.alternatives:
                    continue
                
                transcript = result.alternatives[0].transcript

                # --- LÓGICA DE ATUALIZAÇÃO EM TEMPO REAL ---
                if result.is_final:
                    # Se o resultado é final, o adicionamos à nossa lista permanente
                    self.final_transcripts.append(transcript)
                    # Monta o texto completo e envia para a GUI
                    full_text = " ".join(self.final_transcripts) + " "
                    self.on_transcription_update(full_text)
                else:
                    # Se é intermediário, montamos o texto final + o palpite atual
                    temp_text = " ".join(self.final_transcripts) + " " + transcript
                    self.on_transcription_update(temp_text)
                # --- FIM DA NOVA LÓGICA ---

        except Exception as e:
            print(f"❌ Erro ao processar resposta do Google: {e}")
            self.stop_streaming()

    def start_streaming(self):
        if self.is_running:
            return
            
        # Limpa o histórico da transcrição anterior
        self.final_transcripts = []
        self.is_running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def stop_streaming(self):
        print("🔴 Parando a transcrição...")
        self.is_running = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self._buff.put(None)
        print("🔴 Transcrição parada.")

    def _run(self):
        try:
            self.client = speech.SpeechClient()
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="pt-BR",
            )
            streaming_config = speech.StreamingRecognitionConfig(
                config=config, interim_results=True # Habilita resultados intermediários
            )

            def audio_callback(indata, frames, time, status):
                self._buff.put(bytes(indata))

            self.stream = sd.RawInputStream(
                samplerate=16000, blocksize=4096, channels=1, dtype='int16',
                callback=audio_callback
            )
            
            with self.stream:
                print("✅ Stream de áudio aberto. Iniciando comunicação com o Google...")
                audio_stream_generator = self._audio_generator()
                requests = (req for req in audio_stream_generator)
                responses = self.client.streaming_recognize(streaming_config, requests)
                print("✅ Comunicação com Google estabelecida. Ouvindo...")
                self._listen_print_loop(responses)

        except Exception as e:
            print(f"❌ Erro fatal na thread de transcrição: {e}")
        finally:
            print("-> Thread de transcrição finalizada.")
            self.is_running = False