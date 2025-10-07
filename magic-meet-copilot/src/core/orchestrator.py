import os
from dotenv import load_dotenv
from src.services import openai_service, rpa_service

load_dotenv()

def iniciar_processo_criacao(transcricao_completa: str, info_cliente: dict, progress_callback=None) -> tuple[str, str, str]:
    
    def report_progress(message):
        if progress_callback:
            progress_callback(message)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "ERRO: Chave da API da OpenAI não encontrada.", "", ""

    report_progress("-> [⚙️] Analisando transcrição com a IA...")
    resultado_ia = openai_service.gerar_analise_e_prompt(
        api_key=api_key,
        transcricao_completa=transcricao_completa,
        info_cliente=info_cliente
    )
    report_progress("-> [✅] Análise da IA concluída.")
    
    pre_analise = resultado_ia.get("pre_analise", "Falha ao extrair a pré-análise.")
    prompt_lovable_data = resultado_ia.get("prompt_lovable", "Error extracting prompt.")
    
    prompt_lovable = ""
    if isinstance(prompt_lovable_data, dict):
        prompt_lovable = " ".join(str(v) for v in prompt_lovable_data.values())
    else:
        prompt_lovable = str(prompt_lovable_data)

    link_prototipo = ""
    if "Falha" not in prompt_lovable and "Error" not in prompt_lovable:
        logo_path = info_cliente.get("logo_path", None)
        link_prototipo = rpa_service.criar_prototipo_lovable(prompt_lovable, logo_path, progress_callback)
    else:
        link_prototipo = "Não foi possível gerar o protótipo pois o prompt falhou."

    return pre_analise, prompt_lovable, link_prototipo