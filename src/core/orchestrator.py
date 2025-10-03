# src/core/orchestrator.py

import os
from dotenv import load_dotenv
from src.services import openai_service, rpa_service
# Removi a importação de set_google_credentials daqui para evitar redundância, 
# já que o gui.py já chama. Mas pode manter se preferir.

# Carrega as variáveis de ambiente
load_dotenv()
# set_google_credentials() # Opcional, já chamado em gui.py

def iniciar_processo_criacao(transcricao_completa: str, info_cliente: dict) -> tuple[str, str, str]:
    """
    Orquestra a chamada à IA, a criação do protótipo via RPA (com logo) e retorna os resultados.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "ERRO: Chave da API da OpenAI não encontrada.", "", ""

    print("🤖 Chamando a IA para gerar análise e prompt otimizado...")
    resultado_ia = openai_service.gerar_analise_e_prompt(
        api_key=api_key,
        transcricao_completa=transcricao_completa,
        info_cliente=info_cliente
    )
    
    # --- PONTO DE CORREÇÃO E DEPURAÇÃO ---
    print(f"DEBUG: Resposta completa da IA: {resultado_ia}") # Para vermos o que a IA retornou

    pre_analise = resultado_ia.get("pre_analise", "Falha ao extrair a pré-análise.")
    
    # Pega o dado do prompt
    prompt_lovable_data = resultado_ia.get("prompt_lovable", "Error extracting prompt.")
    
    # Garante que o prompt seja sempre uma string
    prompt_lovable = ""
    if isinstance(prompt_lovable_data, dict):
        # Se for um dicionário, concatena todos os seus valores em um único texto
        prompt_lovable = " ".join(str(v) for v in prompt_lovable_data.values())
    else:
        # Se for qualquer outra coisa (texto, número, etc.), converte para string
        prompt_lovable = str(prompt_lovable_data)
    # --- FIM DA CORREÇÃO ---

    print("✅ Análise e prompt gerados e formatados!")
    
    link_prototipo = ""
    if "Falha" not in prompt_lovable and "Error" not in prompt_lovable:
        logo_path = info_cliente.get("logo_path", None)
        link_prototipo = rpa_service.criar_prototipo_lovable(prompt_lovable, logo_path)
    else:
        link_prototipo = "Não foi possível gerar o protótipo pois o prompt falhou."

    return pre_analise, prompt_lovable, link_prototipo