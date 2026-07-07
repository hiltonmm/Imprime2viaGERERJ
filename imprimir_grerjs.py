import os
import glob
import re
import time
import logging
import sys
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pdfplumber

# ==========================================
# CONFIGURAÇÕES DE TEMPO (Ajuste para acelerar)
# ==========================================
TEMPO_CARREGAR_PDF = 2       # Tempo para o PDF abrir na nova aba
TEMPO_ESPERA_IMPRESSORA = 5  # Tempo aguardando a impressora de rede receber o comando
# ==========================================

# Configuração do arquivo de Log
logging.basicConfig(
    filename='erro_grerj.log', 
    level=logging.ERROR,
    format='%(asctime)s - GRERJ: %(message)s'
)

def extrair_grerjs_do_pdf():
    """Busca o único PDF na pasta e extrai os números de GRERJ."""
    arquivos_pdf = glob.glob("*.pdf")
    
    if not arquivos_pdf:
        print("Erro: Nenhum arquivo PDF encontrado na pasta.")
        return []
    if len(arquivos_pdf) > 1:
        print("Aviso: Mais de um PDF encontrado. Usando o primeiro da lista.")

    caminho_pdf = arquivos_pdf[0]
    print(f"Lendo o arquivo: {caminho_pdf}")
    
    numeros_grerj = []
    
    # Extrai os textos e busca por padrões de 13 dígitos
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            # Encontra sequências exatas de 13 números (padrão da GRERJ)
            encontrados = re.findall(r'\b\d{13}\b', texto)
            numeros_grerj.extend(encontrados)
            
    # Remove duplicatas caso a mesma GRERJ apareça mais de uma vez
    return list(dict.fromkeys(numeros_grerj))

def iniciar_navegador():
    """Configura o Selenium com impressão automática ativada."""
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument('--start-maximized') # Garante que a janela abra em tela cheia para evitar sobreposição de elementos
    opcoes.add_argument('--kiosk-printing')  # Ativa a impressão silenciosa
    
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico, options=opcoes)
    return navegador

def processar_grerjs(navegador, lista_grerjs):
    """Acessa o site e processa cada GRERJ da lista."""
    url_tjrj = "https://www3.tjrj.jus.br/grerjweb/#/grerj-reimpressao/reimpressao"
    espera = WebDriverWait(navegador, 10)
    total = len(lista_grerjs)

    for indice, grerj in enumerate(lista_grerjs, start=1):
        print(f"[{indice}/{total}] Processando GRERJ: {grerj}...")
        try:
            navegador.get(url_tjrj)
            
            # --- PASSO 1: Preencher o número da GRERJ ---
            campo_input = espera.until(EC.presence_of_element_located((By.XPATH, "(//input)[5]")))
            campo_input.clear()
            campo_input.send_keys(grerj)
            
            # --- PASSO 2: Clicar em Reimpressão ---
            btn_reimprimir = espera.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Reimpressão da GRERJ')]")))
            navegador.execute_script("arguments[0].click();", btn_reimprimir)
            
            # --- PASSO 3: Lidar com o Modal de Sucesso ---
            espera.until(EC.text_to_be_present_in_element((By.XPATH, "//body"), "Abrindo tela de reimpressão"))
            
            time.sleep(1) # Pausa rápida para a animação do modal
            
            xpath_botoes = "//button[contains(translate(., 'OKok', 'okok'), 'ok')] | //input[contains(translate(@value, 'OKok', 'okok'), 'ok')]"
            btn_ok = espera.until(
                lambda nav: next(
                    (b for b in nav.find_elements(By.XPATH, xpath_botoes) if b.is_displayed() and b.is_enabled()), 
                    None
                )
            )
            navegador.execute_script("arguments[0].click();", btn_ok)

            # --- PASSO 4: Trocar de aba e Imprimir ---
            espera.until(lambda d: len(d.window_handles) > 1)
            navegador.switch_to.window(navegador.window_handles[1])
            
            time.sleep(TEMPO_CARREGAR_PDF) # Usa a variável do topo
            
            navegador.execute_script("window.print();")
            
            time.sleep(TEMPO_ESPERA_IMPRESSORA) # Usa a variável do topo
            
            navegador.close()
            navegador.switch_to.window(navegador.window_handles[0])
            print(f"-> GRERJ {grerj} enviada com sucesso!\n")

        except Exception as e:
            print(f"\n{'='*60}")
            print(f"ERRO CRÍTICO AO PROCESSAR A GRERJ: {grerj}")
            print(f"{'='*60}")
            print("DETALHES DO ERRO PARA DEPURAÇÃO (TRACEBACK):")
            traceback.print_exc()
            print(f"{'='*60}\n")
            
            logging.error(f"{grerj} - Falha no processamento!\n{traceback.format_exc()}")
            
            try:
                if len(navegador.window_handles) > 1:
                    navegador.close()
            except:
                pass 
                
            print("Encerrando o programa imediatamente devido ao erro acima.")
            sys.exit(1)

if __name__ == "__main__":
    grerjs = extrair_grerjs_do_pdf()
    
    if grerjs:
        print(f"Total de GRERJs encontradas: {len(grerjs)}")
        meu_navegador = iniciar_navegador()
        try:
            processar_grerjs(meu_navegador, grerjs)
            print("Todas as GRERJs foram processadas com sucesso!")
        finally:
            meu_navegador.quit()