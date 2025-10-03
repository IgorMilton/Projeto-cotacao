✅ Requisitos

Python 3.8+

Google Chrome instalado

ChromeDriver compatível com a versão do seu Chrome

📦 Instalação de dependências

Recomenda-se usar um ambiente virtual:

python -m venv venv
venv\Scripts\activate  # No Windows


Depois, instale as dependências necessárias:

pip install selenium


✅ Selenium é a única biblioteca externa usada neste projeto.

🧩 ChromeDriver

Verifique sua versão do Google Chrome:

Acesse chrome://settings/help no navegador.

Baixe o ChromeDriver correspondente à sua versão em:

https://sites.google.com/chromium.org/driver/

Extraia o arquivo chromedriver.exe e coloque em:

Selenium-Investidor10-main\chromedriver\chromedriver.exe


⚠️ O caminho exato deve ser:

C:\Users\aluno\Desktop\Selenium-Investidor10-main\Selenium-Investidor10-main\chromedriver\chromedriver.exe


Caso deseje mudar o local, edite a variável CHROMEDRIVER_PATH no topo do script investidor10_itsa3_1dia.py.

🏁 Como executar

Navegue até a pasta do projeto no terminal/prompt de comando:

cd C:\Users\aluno\Desktop\Selenium-Investidor10-main\Selenium-Investidor10-main


Execute o script:

python investidor10_itsa3_1dia.py


O script irá:

Abrir o navegador.

Acessar a página da ação ITUB4 no site Investidor10.

Clicar na aba "1 dia".

Tirar um screenshot da seção de cotação.

Salvar a imagem em:

C:\Users\aluno\Downloads\unieuro_downloads\cotacao_itub4_1dia.png


📸 O nome do arquivo muda de acordo com o ticker definido.

⚙️ Configurações personalizáveis

No início do script, você pode alterar:

TICKER = "ITUB4"  # Altere para outro código, ex: "PETR4", "ITSA3", etc.
HEADLESS = False  # Coloque como True se quiser rodar sem abrir janela do navegador

🧹 Limpeza automática

O script cria um perfil temporário do Chrome para evitar interferência com seu navegador.

Esse perfil é deletado automaticamente ao final da execução.

❗ Possíveis Erros
Erro: FileNotFoundError: ChromeDriver não encontrado em...

Esse erro significa que o ChromeDriver não está no caminho especificado. Baixe e coloque no local correto ou atualize o valor de CHROMEDRIVER_PATH.

📁 Estrutura do Projeto
Selenium-Investidor10-main/
├── chromedriver/
│   └── chromedriver.exe
├── investidor10_itsa3_1dia.py
├── atividade.py (outro script opcional)
└── README.md
