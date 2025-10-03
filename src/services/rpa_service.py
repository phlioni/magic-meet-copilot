import os
from playwright.sync_api import sync_playwright, TimeoutError
from dotenv import load_dotenv

load_dotenv()

def _handle_login(page):
    try:
        login_button_selector = "#login-link"
        page.wait_for_selector(login_button_selector, timeout=7000)
        page.click(login_button_selector)
        continue_with_email_selector = "#email-login-button"
        page.wait_for_selector(continue_with_email_selector)
        page.click(continue_with_email_selector)
        email = os.getenv("LOVABLE_EMAIL")
        page.fill("#email", email)
        page.get_by_role("button", name="Continuar", exact=True).click()
        password = os.getenv("LOVABLE_PASSWORD")
        page.fill("#password", password)
        page.get_by_role("button", name="Login").click()
        page.wait_for_selector("#chatinput", timeout=30000)
    except TimeoutError:
        print("✅ Sessão de login provavelmente já ativa.")
    except Exception as e:
        print(f"❌ Ocorreu um erro durante o login: {e}")
        raise e

def criar_prototipo_lovable(prompt: str, logo_path: str = None, progress_callback=None) -> str:
    def report_progress(message):
        print(message)
        if progress_callback:
            progress_callback(message)

    link_prototipo = "Erro ao gerar protótipo."
    
    lovable_url = os.getenv("LOVABLE_URL")
    if not lovable_url:
        return "Erro: LOVABLE_URL não definida."

    with sync_playwright() as p:
        report_progress("-> [⚙️] Iniciando navegador...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            report_progress(f"-> [⚙️] Navegando para {lovable_url}...")
            page.goto(lovable_url, timeout=60000)

            report_progress("-> [⚙️] Verificando e realizando login...")
            _handle_login(page)
            report_progress("-> [✅] Login concluído.")

            report_progress("-> [⚙️] Inserindo prompt na plataforma...")
            page.fill("#chatinput", prompt)

            if logo_path and os.path.exists(logo_path):
                report_progress("-> [⚙️] Anexando arquivo de logo...")
                try:
                    with page.expect_file_chooser() as fc_info:
                        page.get_by_role("button", name="Anexar").click()
                    
                    file_chooser = fc_info.value
                    file_chooser.set_files(logo_path)
                    
                    try:
                        add_files_button = page.get_by_role("button", name="Adicionar Arquivos")
                        add_files_button.wait_for(state="visible", timeout=3000)
                        add_files_button.click()
                    except TimeoutError:
                        pass
                    report_progress("-> [✅] Logo anexado.")
                except Exception as e:
                    report_progress(f"-> [⚠️] Não foi possível anexar o logo: {e}")
            
            report_progress("-> [⚙️] Enviando para geração do protótipo...")
            page.click('#chatinput-send-message-button')
            
            report_progress("-> [⏳] Aguardando geração do Lovable... (Este passo pode levar vários minutos)")
            preview_link_selector = 'a[href*="preview--"]'
            page.wait_for_selector(preview_link_selector, timeout=0)
            
            report_progress("-> [⚙️] Extraindo link do protótipo...")
            link_prototipo = page.get_attribute(preview_link_selector, 'href')
            report_progress("-> [✅] Protótipo gerado com sucesso!")

        except Exception as e:
            error_message = f"-> [❌] Erro na automação: {e}"
            report_progress(error_message)
            link_prototipo = error_message
        finally:
            browser.close()
            
    return link_prototipo