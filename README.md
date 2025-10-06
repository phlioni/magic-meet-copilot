# ✨ Magic Meet Copilot ✨

**Magic Meet Copilot** é uma ferramenta revolucionária projetada para transformar o fluxo de criação de propostas comerciais, reduzindo o ciclo de vendas de dias para minutos e encantando clientes desde o primeiro contato.

Utilizando transcrição em tempo real do microfone do operador, análise por IA e automação robótica de processos (RPA), esta aplicação gera um protótipo de software funcional e personalizado *durante* a reunião com o cliente, criando um inesquecível "efeito UAU".

---

### 🚀 Principais Funcionalidades

* **Transcrição Direta do Microfone:** Captura o áudio diretamente do microfone padrão do usuário, sem necessidade de softwares de terceiros.
* **Análise por IA:** Utiliza GPT-4 para analisar a transcrição, filtrar conversas triviais e extrair os requisitos essenciais do projeto.
* **Geração de Proposta Otimizada:** Cria uma pré-análise de negócios e um prompt de alta performance otimizado para ferramentas de prototipagem.
* **Criação de Protótipo Automatizada:** Usa Playwright para abrir o LovableAI, realizar login, inserir o prompt, anexar arquivos e gerar um protótipo funcional em tempo real.
* **Log de Progresso Visual:** O usuário acompanha em tempo real cada passo que a automação está executando.

### 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.11
* **Interface Gráfica:** CustomTkinter
* **Orquestração de IA:** OpenAI API (GPT-4 Turbo)
* **Transcrição de Áudio:** Google Cloud Speech-to-Text API
* **Captura de Áudio:** Sounddevice
* **Automação Web (RPA):** Playwright

---

### 🏁 Começando (Para Desenvolvedores)

#### Pré-requisitos de Software
* Python 3.11 (recomendado)
* Git
* Um microfone funcional configurado como padrão no sistema operacional.

#### Instalação
1.  Clone o repositório.
2.  Crie e ative um ambiente virtual (`py -3.11 -m venv .venv` e `.\.venv\Scripts\activate`).
3.  Atualize as ferramentas do pip: `python -m pip install --upgrade pip setuptools wheel`.
4.  Instale as dependências: `pip install -r requirements.txt`.
5.  Instale os navegadores do Playwright: `playwright install`.

#### Configuração
O projeto requer dois arquivos de configuração na raiz:
1.  **`.env`**: Para as chaves de API e credenciais (OpenAI, Lovable, etc.).
2.  **`google_credentials.json`**: Chave da conta de serviço do Google Cloud para a API Speech-to-Text.

---

### 🎈 Como Usar a Aplicação

1.  **Verifique o Microfone:** Certifique-se de que seu microfone desejado está definido como o dispositivo de entrada padrão nas configurações de som do seu sistema operacional.
2.  **Execute a Aplicação:** `.\.venv\Scripts\python.exe main.py` ou use o script `run.bat`.
3.  **Durante a Reunião:**
    * Preencha as informações do cliente.
    * Clique em **▶️ Iniciar Transcrição**. A aplicação começará a ouvir sua voz.
    * **Lembre-se da "Técnica do Espelho":** Repita e resuma os pontos importantes do cliente para que eles sejam capturados na transcrição.
    * Ao final, clique em **⏹️ Parar Transcrição**.
    * Clique em **✨ Criar Protótipo!** e acompanhe o progresso na caixa de log.