import asyncio
import requests
from pyppeteer import launch
from tqdm import tqdm


# Script em python para simular o comportamento do ticket https://tickets.azion.com/a/tickets/14039
# Instalar dependencias -  "pip install pyppeteer tqdm requests"
async def track_redirects(response):
    if response.status >= 300 and response.status < 400:
        print(f"Redirecionado de {response.url} para {response.headers['location']}")

async def main():
    # Use a biblioteca 'requests' para obter os cabeçalhos
    response = requests.get('https://www.metropoles.com/?amp', headers={'Pragma': 'azion-debug-cache'})
    expires_in_seconds = int(response.headers.get('X-Cache-Expires-In', 0))

    print(f"X-Cache-Expires-In: {expires_in_seconds}")

    # Defina o User-Agent para simular ser um iPhone 12 Pro
    user_agent = (
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) '
        'AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
    )

    # Lançar o navegador com o User-Agent configurado
    browser = await launch(headless=False, args=['--user-agent=' + user_agent])
    page = await browser.newPage()

    # Defina o rastreamento de redirecionamento
    page.on('response', track_redirects)

    # Agora vá para a URL desejada
    await page.goto('https://www.metropoles.com/vida-e-estilo/horoscopo/horoscopo-2023-confira-a-previsao-de-hoje-02-08-para-seu-signo?amp')

    # Aguarde o tempo calculado (em segundos) com barra de carregamento
    if expires_in_seconds > 0:
        with tqdm(total=expires_in_seconds, desc="Aguardando cache expirar") as pbar:
            for _ in range(expires_in_seconds):
                await asyncio.sleep(1)
                pbar.update(1)

    # Código para clicar no botão através do XPath
    selector = '/html/body/header/div/a'  # Substitua pelo XPath do seu browser(so abrir a home e inspect > botao em cima > copy xpath)
    await page.waitForXPath(selector)
    link = await page.xpath(selector)
    if link:
        await link[0].click()
        print("Clicou no link")
    else:
        print("Link não encontrado")

    #printar novamente so pra ver se ta em 300 or so
    response2 = requests.get('https://www.metropoles.com/?amp', headers={'Pragma': 'azion-debug-cache'})
    expires_in_seconds_2 = int(response2.headers.get('X-Cache-Expires-In', 0))
    print(f"X-Cache-Expires-In: {expires_in_seconds_2}")
    
    # Aguarde antes de fechar
    await asyncio.sleep(60)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
