# ✨ Magic Meet Copilot ✨

**Magic Meet Copilot** é uma ferramenta revolucionária projetada para transformar o fluxo de criação de propostas comerciais, reduzindo o ciclo de vendas de dias para minutos e encantando clientes desde o primeiro contato.

Utilizando transcrição em tempo real, análise por IA e automação robótica de processos (RPA), esta aplicação gera um protótipo de software funcional e personalizado *durante* a reunião com o cliente, criando um inesquecível "efeito UAU".

---

### 🚀 Principais Funcionalidades

* **Transcrição em Tempo Real:** Conecta-se a uma fonte de áudio (como o OBS) para transcrever a conversa da reunião ao vivo.
* **Análise por IA:** Utiliza um modelo de linguagem avançado (GPT-4) para analisar a transcrição completa, filtrar conversas triviais e extrair os requisitos essenciais do projeto.
* **Geração de Proposta Otimizada:** A IA cria uma pré-análise de negócios e um prompt de alta performance otimizado para ferramentas de prototipagem.
* **Criação de Protótipo Automatizada:** Um robô (RPA com Playwright) abre a ferramenta de prototipagem (LovableAI), insere o prompt e os arquivos do cliente, e gera um protótipo funcional em tempo real.
* **Interface Simples:** Uma interface desktop intuitiva para controlar a transcrição e iniciar o processo de geração.

### 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Interface Gráfica:** CustomTkinter
* **Orquestração de IA:** OpenAI API (GPT-4 Turbo)
* **Transcrição de Áudio:** Google Cloud Speech-to-Text API
* **Automação Web (RPA):** Playwright
* **Captura de Áudio:** SoundDevice & VB-CABLE (ponte de áudio virtual)

---

### 🏁 Começando

Siga estas instruções para configurar o ambiente de desenvolvimento.

#### Pré-requisitos

* Python 3.9+
* Git
* [OBS Studio](https://obsproject.com/)
* [VB-CABLE Virtual Audio Device](https://vb-audio.com/Cable/)

#### Instalação

1.  **Clone o repositório:**
    ```sh
    git clone [https://github.com/seu-usuario/magic-meet-copilot.git](https://github.com/seu-usuario/magic-meet-copilot.git)
    cd magic-meet-copilot
    ```

2.  **Crie e ative um ambiente virtual:**
    ```sh
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # macOS / Linux
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Instale os navegadores do Playwright:**
    ```sh
    playwright install
    ```

#### Configuração

O projeto requer dois arquivos de configuração na raiz:

1.  **`.env`**: Crie este arquivo para armazenar suas chaves de API e URLs. Preencha com suas informações.
    ```env
    OPENAI_API_KEY="sk-..."
    LOVABLE_EMAIL="seu-email@exemplo.com"
    LOVABLE_PASSWORD="sua-senha-aqui"
    LOVABLE_URL="[https://app.lovable.ai/](https://app.lovable.ai/)"
    GOOGLE_APPLICATION_CREDENTIALS="google_credentials.json"
    ```

2.  **`google_credentials.json`**: Este é o arquivo de chave da sua conta de serviço do Google Cloud. Faça o download no painel do GCP e coloque-o na pasta raiz do projeto. Lembre-se de adicionar este arquivo ao seu `.gitignore`.

---

### 🎈 Como Usar

1.  **Configure a Ponte de Áudio:**
    * No OBS, configure o áudio da sua reunião para ser monitorado e enviado para o `CABLE Input`.
    * Nas configurações de som do Windows, defina o dispositivo de **Entrada** padrão como `CABLE Output`.

2.  **Execute a Aplicação:**
    * Com o ambiente virtual ativo, rode o comando:
        ```sh
        python main.py
        ```

3.  **Durante a Reunião:**
    * Preencha as informações do cliente (Nome, Cores, Logo).
    * Clique em **▶️ Iniciar Transcrição**. A conversa começará a aparecer na tela.
    * Ao final da discussão de requisitos, clique em **⏹️ Parar Transcrição**.
    * Clique em **✨ Criar Protótipo!** e aguarde a mágica acontecer. O link do protótipo e a análise aparecerão nos campos de resultado.