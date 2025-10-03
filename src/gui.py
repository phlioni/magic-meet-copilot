# src/gui.py

import customtkinter as ctk
from customtkinter import filedialog # Importa o diálogo de arquivos
import threading
import os
from src.core.orchestrator import iniciar_processo_criacao
from src.services.transcription_service import TranscriptionService, set_google_credentials

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
set_google_credentials()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Magic Meet Copilot")
        self.geometry("1000x800")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Frame de Entrada ---
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(input_frame, text="Nome Cliente:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.client_name_entry = ctk.CTkEntry(input_frame, placeholder_text="Nome do cliente...")
        self.client_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(input_frame, text="Cores (Hex):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.client_colors_entry = ctk.CTkEntry(input_frame, placeholder_text="#FFFFFF, #000000")
        self.client_colors_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # --- NOVA SEÇÃO DE UPLOAD DE LOGO ---
        ctk.CTkLabel(input_frame, text="Logo Cliente:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.logo_path_entry = ctk.CTkEntry(input_frame, placeholder_text="Nenhum arquivo selecionado...")
        self.logo_path_entry.grid(row=2, column=1, padx=(10, 5), pady=5, sticky="ew")
        self.logo_button = ctk.CTkButton(input_frame, text="Selecionar...", width=100, command=self.select_logo_file)
        self.logo_button.grid(row=2, column=2, padx=(0, 10), pady=5, sticky="e")
        input_frame.grid_columnconfigure(2, weight=0) # Impede que o botão estique
        # ------------------------------------
        
        # ... (O resto do código da GUI continua o mesmo) ...
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
        self.status_label = ctk.CTkLabel(self, text="Aguardando comando...", anchor="w")
        self.status_label.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
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

    # --- NOVA FUNÇÃO PARA SELECIONAR O LOGO ---
    def select_logo_file(self):
        # Abre a janela de seleção de arquivo
        filepath = filedialog.askopenfilename(
            title="Selecione o arquivo de logo",
            filetypes=(("Imagens", "*.png *.jpg *.jpeg *.svg"), ("Todos os arquivos", "*.*"))
        )
        if filepath:
            self.logo_path_entry.delete(0, "end")
            self.logo_path_entry.insert(0, filepath)
    
    # ... (O resto dos métodos continua igual)
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
        self.status_label.configure(text="Transcrição em andamento... 🎤")

    def stop_transcription(self):
        self.transcription_service.stop_streaming()
        self.transcription_start_button.configure(state="normal")
        self.transcription_stop_button.configure(state="disabled")
        self.status_label.configure(text="Transcrição parada. Pronto para criar protótipo.")

    def iniciar_thread_criacao(self):
        self.create_button.configure(state="disabled", text="Gerando...")
        self.status_label.configure(text="Iniciando processo... ⏳")
        thread = threading.Thread(target=self.run_creation_process)
        thread.start()

    def run_creation_process(self):
        transcription_text = self.summary_textbox.get("1.0", "end-1c")
        client_info = {
            "nome": self.client_name_entry.get(),
            "cores": self.client_colors_entry.get(),
            # Adiciona o caminho do logo ao dicionário
            "logo_path": self.logo_path_entry.get() 
        }
        if not transcription_text.strip():
            self.after(0, self.update_gui_results, "Erro: A transcrição não pode estar vazia.", "", "")
            return
        self.status_label.configure(text="Comunicando com a IA... 🧠")
        pre_analise, prompt_lovable, link_prototipo = iniciar_processo_criacao(transcription_text, client_info)
        self.after(0, self.update_gui_results, pre_analise, prompt_lovable, link_prototipo)

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
        if "Erro" in link_prototipo:
             self.status_label.configure(text="Processo concluído com falhas na automação. ⚠️")
        else:
            self.status_label.configure(text="Processo completo! Protótipo gerado. ✅")
        self.create_button.configure(state="normal", text="✨ Criar Protótipo!")