@echo off
:: Coloca um título na janela do terminal que pode aparecer rapidamente.
title Magic Meet Copilot

:: Cria o ambiente virtual (.venv) somente se a pasta ainda não existir.
IF NOT EXIST .venv (
    echo Criando ambiente virtual pela primeira vez...
    python -m venv .venv
)

:: Instala ou verifica as dependências de forma silenciosa.
:: O '>nul' esconde a saída do terminal para uma experiência mais limpa.
echo Verificando dependencias...
.\.venv\Scripts\pip.exe install -r requirements.txt > nul
.\.venv\Scripts\playwright.exe install > nul

:: Inicia a aplicação principal usando o Python de dentro do ambiente virtual.
echo Iniciando Magic Meet Copilot...
.\.venv\Scripts\python.exe main.py