# Imprime2viaGERERJ

Este projeto automatiza a extração de números de GRERJ de um arquivo PDF e realiza a reimpressão automática através do site do TJRJ utilizando Selenium.

## 📋 Pré-requisitos

Para executar este projeto, você precisará ter instalado em sua máquina:

* **Python 3.x** (Recomendado versão 3.10 ou superior).
* **Google Chrome** instalado.

## 🚀 Como instalar

1. Clone o repositório ou baixe os arquivos para uma pasta em seu computador.
2. Abra o terminal na pasta do projeto e crie um ambiente virtual:
```bash
python -m venv .venv

```


3. Ative o ambiente virtual:
* **Windows:** `.venv\Scripts\activate`


4. Instale as dependências necessárias:


```bash
pip install -r requirements.txt

```



## ⚙️ Como usar

1. Coloque o arquivo PDF contendo os números das GRERJs na pasta raiz do projeto.
2. O script buscará automaticamente o primeiro arquivo PDF encontrado na pasta.


3. Execute o arquivo `executar.bat` (ou execute via terminal: `python imprimir_grerjs.py`).


4. O navegador Chrome abrirá automaticamente, processará cada número de GRERJ encontrado e enviará o comando de impressão.



## 🛠️ Configurações

No topo do arquivo `imprimir_grerjs.py`, você pode ajustar os tempos de espera caso sua conexão ou impressora sejam mais lentas:

* `TEMPO_CARREGAR_PDF`: Tempo em segundos para esperar o PDF carregar na nova aba.
* `TEMPO_ESPERA_IMPRESSORA`: Tempo em segundos que o sistema aguarda a impressora receber o comando de impressão.

## ⚠️ Observações importantes

* 
**Impressão Silenciosa:** O script utiliza o argumento `--kiosk-printing` para tentar realizar a impressão sem abrir a caixa de diálogo do sistema. Certifique-se de que sua impressora padrão esteja configurada corretamente.


* 
**Logs de Erro:** Caso ocorra alguma falha, o erro será registrado no arquivo `erro_grerj.log` na pasta do projeto.


* 
**Requisitos:** O projeto utiliza `selenium` para navegação, `webdriver-manager` para gerenciar o driver do Chrome e `pdfplumber` para a extração dos dados do PDF.