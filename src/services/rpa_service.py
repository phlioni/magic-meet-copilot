# src/services/rpa_service.py

import os
from playwright.sync_api import sync_playwright, TimeoutError
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

def _handle_login(page):
    """
    Função auxiliar para cuidar do fluxo de login, interagindo com o modal.
    """
    try:
        login_button_selector = "#login-link"
        page.wait_for_selector(login_button_selector, timeout=7000)
        
        print("🔍 Botão de Login encontrado. Clicando...")
        page.click(login_button_selector)

        continue_with_email_selector = "#email-login-button"
        print("-> Aguardando modal de login...")
        page.wait_for_selector(continue_with_email_selector)
        print("-> Clicando em 'Continue with email' dentro do modal...")
        page.click(continue_with_email_selector)

        email = os.getenv("LOVABLE_EMAIL")
        email_input_selector = "#email"
        page.wait_for_selector(email_input_selector)
        page.fill(email_input_selector, email)
        
        page.get_by_role("button", name="Continuar", exact=True).click()

        password = os.getenv("LOVABLE_PASSWORD")
        password_input_selector = "#password"
        page.wait_for_selector(password_input_selector)
        page.fill(password_input_selector, password)
        
        page.get_by_role("button", name="Login").click()
        
        print("✅ Login realizado com sucesso!")
        page.wait_for_selector("#chatinput", timeout=30000)
        
    except TimeoutError:
        print("✅ Sessão de login provavelmente já ativa (nenhum botão de login encontrado).")
    except Exception as e:
        print(f"❌ Ocorreu um erro durante o login: {e}")
        raise e

def criar_prototipo_lovable(prompt: str, logo_path: str = None) -> str:
    """
    Usa o Playwright para fazer login, inserir o prompt, anexar um logo
    e extrair o link do protótipo.
    """
    link_prototipo = "Erro ao gerar protótipo."
    
    lovable_url = os.getenv("LOVABLE_URL")
    if not lovable_url:
        return "Erro: A variável LOVABLE_URL não foi definida no arquivo .env"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            print(f"🤖 Iniciando automação em {lovable_url}...")
            page.goto(lovable_url, timeout=60000)

            _handle_login(page)

            print("1. Inserindo o prompt na caixa de texto...")
            page.fill("#chatinput", prompt)
            print("✅ Prompt inserido com sucesso.")

            if logo_path and os.path.exists(logo_path):
                print("2. Iniciando processo de anexo de arquivo...")
                try:
                    # --- LÓGICA DE UPLOAD CORRIGIDA ---
                    
                    # Passo 1: Clica no botão "Anexar" principal para abrir o modal
                    page.get_by_role("button", name="Anexar").click()
                    print("-> Modal de anexo aberto.")

                    # Passo 2: A janela de escolher arquivo SÓ VAI ABRIR depois do próximo clique.
                    # Então, preparamos o "ouvinte" para ela agora.
                    with page.expect_file_chooser() as fc_info:
                        # Passo 3: Dentro do modal, clica em "Adicionar Arquivos".
                        # Esta ação irá disparar a abertura da janela de seleção de arquivos.
                        print("-> Clicando em 'Adicionar Arquivos' dentro do modal...")
                        page.get_by_role("button", name="Adicionar Arquivos").click()
                    
                    # Passo 4: Agora que a janela foi aberta e o "ouvinte" a capturou,
                    # podemos selecionar o arquivo.
                    file_chooser = fc_info.value
                    file_chooser.set_files(logo_path)
                    
                    print(f"✅ Arquivo de logo '{logo_path}' selecionado com sucesso.")
                    # --- FIM DA LÓGICA CORRIGIDA ---

                except Exception as e:
                    print(f"⚠️ Não foi possível anexar o logo: {e}")
            
            print("3. Clicando no botão de enviar...")
            page.click('#chatinput-send-message-button')
            print("⏳ Aguardando a geração do protótipo... Isso pode levar vários minutos.")

            print("4. Aguardando o link de preview do protótipo...")
            preview_link_selector = 'a[href*="preview--"]'
            page.wait_for_selector(preview_link_selector, timeout=0)
            
            link_prototipo = page.get_attribute(preview_link_selector, 'href')

            print(f"✅ Protótipo gerado com sucesso! Link: {link_prototipo}")

        except Exception as e:
            print(f"❌ Ocorreu um erro inesperado durante a automação: {e}")
            link_prototipo = f"Erro: {e}"
        finally:
            browser.close()
            
    return link_prototipo