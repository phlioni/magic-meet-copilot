# src/services/openai_service.py

import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

def gerar_analise_e_prompt(api_key: str, transcricao_completa: str, info_cliente: dict) -> dict:
    """
    Recebe a transcrição COMPLETA da reunião, filtra, analisa e gera saídas otimizadas.
    """
    openai.api_key = api_key
    
    # --- PROMPT MESTRE OTIMIZADO V3 (ECONOMIA DE TOKENS) ---
    prompt_mestre = f"""
    Analise a transcrição para o cliente '{info_cliente.get('nome', 'N/A')}'.
    Filtre conversas não essenciais. Extraia o objetivo, público-alvo e funcionalidades.

    Gere um objeto JSON com duas chaves: "pre_analise" e "prompt_lovable".

    1.  **"pre_analise" (string, em português):**
        * Um resumo conciso contendo as seções: "Objetivo Principal:", "Público-Alvo:" e "Funcionalidades Essenciais:".

    2.  **"prompt_lovable" (string, em inglês):**
        * Um prompt de UI detalhado. Use este template como guia:
        * **Overview:** [Descreva a aplicação em 1 frase. Ex: A modern dashboard for sales managers to track team performance.]
        * **Style:** [Descreva o estilo. Ex: Clean, modern, professional, using primary colors {info_cliente.get('cores', 'N/A')}. The UI must be user-friendly and intuitive.]
        * **Main Components:** [Descreva os componentes principais da UI de forma detalhada. Ex: A left navigation sidebar with links. The main area must have 4 key metric cards at the top (Total Revenue, New Customers, etc). Below the cards, a data table with columns for Customer, Product, Value, and Status, including a search bar above it.]
        * **UI Language:** All UI text must be in Portuguese.

    **Transcrição para Análise:**
    ---
    {transcricao_completa}
    ---

    Retorne APENAS o objeto JSON.
    """
    
    try:
        response = openai.chat.completions.create(
            # Usar um modelo mais rápido e barato como o gpt-3.5-turbo também é uma ótima forma de otimizar
            # Mas para a qualidade que queremos, manteremos o gpt-4-turbo por enquanto.
            model="gpt-4-turbo", 
            messages=[
                {"role": "system", "content": "Você é uma IA especialista em processar transcrições e gerar saídas JSON estruturadas para prototipagem de UI. Seja direto e siga o formato solicitado."},
                {"role": "user", "content": prompt_mestre}
            ],
            response_format={"type": "json_object"},
            temperature=0.3, # Diminuímos um pouco mais a temperatura para ser ainda mais direto
        )
        resultado_json = json.loads(response.choices[0].message.content)
        return resultado_json

    except Exception as e:
        print(f"Erro ao chamar a API da OpenAI: {e}")
        return {
            "pre_analise": "Ocorreu um erro ao gerar a análise.",
            "prompt_lovable": "Error generating prompt."
        }