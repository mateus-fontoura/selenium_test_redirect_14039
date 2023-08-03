from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import concurrent.futures
import requests

# Caminho completo para o chromedriver.exe ( ########## Necessário atualizar o path do seu C.Driver, ou mudar o código
# pra conseguir usar o PATH(modo certo)
chromedriver_path = "C:\\Users\\Mateus\\Documents\\GitHub\\azion\\Tickets\\chromedriver.exe"

# Função do teste a ser executada
def run_test():
    # Configurar as opções do Chrome para emular um iPhone
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone X"})

    # Criar o WebDriver do Chrome com as opções configuradas
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)

    try:
        # Acessar a página específica
        driver.get("https://www.metropoles.com/vida-e-estilo/horoscopo/horoscopo-2023-confira-a-previsao-de-hoje-02-08-para-seu-signo?amp")

        # Aguardar o carregamento completo da página (pode ajustar o tempo conforme necessário)
        time.sleep(5)

        # Clicar no botão especificado pelo XPath
        button_element = driver.find_element(By.XPATH, "/html/body/header/div/a/amp-img/img")
        button_element.click()

        # Aguardar o carregamento completo da página após o clique (pode ajustar o tempo conforme necessário)
        time.sleep(5)

        # Fazer uma solicitação HTTP para a página após o carregamento
        response = requests.get(driver.current_url)
        page_status = response.status_code

        print("Status da página após o carregamento completo:", page_status)

    except Exception as e:
        print("Ocorreu um erro durante o teste:", e)

    finally:
        driver.quit()

# Repetir o teste 10 vezes
for i in range(10):
    # Executar 10 testes simultaneamente usando ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_test) for _ in range(10)]

    # Aguardar um intervalo entre as repetições do teste (pode ajustar conforme necessário)
    time.sleep(5)
