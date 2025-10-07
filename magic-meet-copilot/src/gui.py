import customtkinter as ctk
from customtkinter import filedialog
import threading
import os
from src.core.orchestrator import iniciar_processo_criacao
from src.services.transcription_service import TranscriptionService, set_google_credentials

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# A chamada foi movida para o main.py para garantir a ordem de execução, 
# mas mantê-la aqui não causa problemas.
# set_google_credentials() 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Magic Meet Copilot")
        self.geometry("1000x900")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(input_frame, text="Nome Cliente:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.client_name_entry = ctk.CTkEntry(input_frame, placeholder_text="Nome do cliente...")
        self.client_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(input_frame, text="Cores (Hex):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.client_colors_entry = ctk.CTkEntry(input_frame, placeholder_text="#FFFFFF, #000000")
        self.client_colors_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(input_frame, text="Logo Cliente:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.logo_path_entry = ctk.CTkEntry(input_frame, placeholder_text="Nenhum arquivo selecionado...")
        self.logo_path_entry.grid(row=2, column=1, padx=(10, 5), pady=5, sticky="ew")
        self.logo_button = ctk.CTkButton(input_frame, text="Selecionar...", width=100, command=self.select_logo_file)
        self.logo_button.grid(row=2, column=2, padx=(0, 10), pady=5, sticky="e")
        input_frame.grid_columnconfigure(2, weight=0)

        controls_frame = ctk.CTkFrame(self)
        controls_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        controls_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.transcription_start_button = ctk.CTkButton(controls_frame, text="▶️ Iniciar Transcrição", command=self.start_transcription)
        self.transcription_start_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.transcription_stop_button = ctk.CTkButton(controls_frame, text="⏹️ Parar Transcrição", command=self.stop_transcription, state="disabled")
        self.transcription_stop_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.create_button = ctk.CTkButton(controls_frame, text="✨ Criar Protótipo!", command=self.iniciar_thread_criacao)
        self.create_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        summary_frame = ctk.CTkFrame(self)
        summary_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="nsew")
        summary_frame.grid_rowconfigure(1, weight=1)
        summary_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(summary_frame, text="Transcrição da Reunião", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.summary_textbox = ctk.CTkTextbox(summary_frame, wrap="word", font=("Arial", 14))
        self.summary_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        progress_frame = ctk.CTkFrame(self)
        progress_frame.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        progress_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(progress_frame, text="Progresso da Geração", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.progress_log_textbox = ctk.CTkTextbox(progress_frame, height=100, state="disabled", wrap="word")
        self.progress_log_textbox.grid(row=1, column=0, padx=10, pady=(0,10), sticky="ew")

        output_frame = ctk.CTkFrame(self)
        output_frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(2, weight=1) 
        ctk.CTkLabel(output_frame, text="Resultados Gerados", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.link_textbox = ctk.CTkTextbox(output_frame, wrap="word", height=20, state="disabled")
        self.link_textbox.grid(row=1, column=0, padx=10, pady=(0,5), sticky="nsew")
        self.pre_analysis_textbox = ctk.CTkTextbox(output_frame, wrap="word", height=150, state="disabled")
        self.pre_analysis_textbox.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        self.lovable_prompt_textbox = ctk.CTkTextbox(output_frame, wrap="word", height=80, state="disabled")
        self.lovable_prompt_textbox.grid(row=3, column=0, padx=10, pady=(5,10), sticky="nsew")

        self.transcription_service = TranscriptionService(on_transcription_update=self.update_transcription_textbox)

    def log_progress(self, message):
        self.after(0, self._append_to_log, message)

    def _append_to_log(self, message):
        self.progress_log_textbox.configure(state="normal")
        self.progress_log_textbox.insert("end", message + "\n")
        self.progress_log_textbox.see("end")
        self.progress_log_textbox.configure(state="disabled")

    def run_creation_process(self):
        self.progress_log_textbox.configure(state="normal")
        self.progress_log_textbox.delete("1.0", "end")
        self.progress_log_textbox.configure(state="disabled")

        transcription_text = self.summary_textbox.get("1.0", "end-1c")
        client_info = {
            "nome": self.client_name_entry.get(),
            "cores": self.client_colors_entry.get(),
            "logo_path": self.logo_path_entry.get() 
        }
        if not transcription_text.strip():
            self.after(0, self.update_gui_results, "Erro: A transcrição não pode estar vazia.", "", "")
            return
        
        pre_analise, prompt_lovable, link_prototipo = iniciar_processo_criacao(
            transcription_text, 
            client_info, 
            progress_callback=self.log_progress
        )
        self.after(0, self.update_gui_results, pre_analise, prompt_lovable, link_prototipo)

    def select_logo_file(self):
        filepath = filedialog.askopenfilename(title="Selecione o arquivo de logo", filetypes=(("Imagens", "*.png *.jpg *.jpeg *.svg"), ("Todos os arquivos", "*.*")))
        if filepath:
            self.logo_path_entry.delete(0, "end")
            self.logo_path_entry.insert(0, filepath)
            
    def update_transcription_textbox(self, full_text):
        self.after(0, self._update_gui_text, full_text)

    def _update_gui_text(self, full_text):
        self.summary_textbox.delete("1.0", "end")
        self.summary_textbox.insert("1.0", full_text)
        self.summary_textbox.see("end")

    def start_transcription(self):
        self.transcription_service.start_streaming()
        self.transcription_start_button.configure(state="disabled")
        self.transcription_stop_button.configure(state="normal")

    def stop_transcription(self):
        self.transcription_service.stop_streaming()
        self.transcription_start_button.configure(state="normal")
        self.transcription_stop_button.configure(state="disabled")

    def iniciar_thread_criacao(self):
        self.create_button.configure(state="disabled", text="Gerando...")
        thread = threading.Thread(target=self.run_creation_process)
        thread.start()

    def update_gui_results(self, pre_analise, prompt_lovable, link_prototipo):
        self.link_textbox.configure(state="normal")
        self.link_textbox.delete("1.0", "end")
        self.link_textbox.insert("1.0", f"🔗 Link do Protótipo: {link_prototipo}")
        self.link_textbox.configure(state="disabled")

        self.pre_analysis_textbox.configure(state="normal")
        self.pre_analysis_textbox.delete("1.0", "end")
        self.pre_analysis_textbox.insert("1.0", f"--- PRÉ-ANÁLISE ---\n\n{pre_analise}")
        self.pre_analysis_textbox.configure(state="disabled")

        self.lovable_prompt_textbox.configure(state="normal")
        self.lovable_prompt_textbox.delete("1.0", "end")
        self.lovable_prompt_textbox.insert("1.0", f"--- PROMPT UTILIZADO ---\n\n{prompt_lovable}")
        self.lovable_prompt_textbox.configure(state="disabled")

        self.create_button.configure(state="normal", text="✨ Criar Protótipo!")