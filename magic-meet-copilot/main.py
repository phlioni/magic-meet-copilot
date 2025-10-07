import sys
import os
from dotenv import load_dotenv

# --- BLOCO DE CONFIGURAÇÃO DE CAMINHOS ---
# Este bloco detecta se o app está rodando como um script ou como um executável "congelado".

if getattr(sys, 'frozen', False):
    # Se estiver rodando como um executável (congelado pelo PyInstaller)
    # O 'base_path' é a pasta onde o .exe está localizado
    base_path = os.path.dirname(sys.executable)
    # O PyInstaller coloca os arquivos adicionados (com --add-data) em uma pasta temporária `_MEIPASS`
    # O caminho para a credencial do Google precisa apontar para lá.
    google_creds_path = os.path.join(sys._MEIPASS, 'google_credentials.json')
else:
    # Se estiver rodando como um script .py normal
    # O 'base_path' é a pasta onde o script está
    base_path = os.path.dirname(os.path.abspath(__file__))
    google_creds_path = os.path.join(base_path, 'google_credentials.json')

# 1. Carrega o arquivo .env do local correto (ao lado do .exe ou do script)
dotenv_path = os.path.join(base_path, '.env')
if os.path.exists(dotenv_path):
    print(f"✅ Carregando configurações de: {dotenv_path}")
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f"❌ AVISO: Arquivo .env não encontrado em {dotenv_path}")

# 2. Define a variável de ambiente para as credenciais do Google com o caminho absoluto correto
if os.path.exists(google_creds_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_creds_path
    print(f"✅ Credenciais do Google apontadas para: {google_creds_path}")
else:
    print(f"❌ AVISO: Arquivo de credenciais do Google não encontrado em {google_creds_path}")
# --- FIM DO BLOCO DE CONFIGURAÇÃO ---


# AGORA, com o ambiente devidamente configurado, importamos e rodamos o resto do app.
# É importante importar DEPOIS de configurar as variáveis de ambiente.
from src.gui import App

if __name__ == "__main__":
    app = App()
    app.mainloop()