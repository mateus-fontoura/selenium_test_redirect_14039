import asyncio
from pyppeteer import launch
import time
import requests

async def track_redirects(response):
    if response.status >= 300 and response.status < 400:
        print(f"Redirecionado de {response.request.url} para {response.headers['location']}")

async def main():
    # Use a biblioteca 'requests' para obter os cabeçalhos
    response = requests.get('https://www.metropoles.com/?amp', headers={'Pragma': 'azion-debug-cache'})
    expires_in_seconds = int(response.headers.get('X-Cache-Expires-In', 0))

    print(f"X-Cache-Expires-In: {expires_in_seconds}")

    browser = await launch(headless=False)
    page = await browser.newPage()
    
    # Defina o rastreamento de redirecionamento
    page.on('response', track_redirects)
    await page.goto('https://www.metropoles.com/vida-e-estilo/horoscopo/horoscopo-2023-confira-a-previsao-de-hoje-02-08-para-seu-signo?amp')

    # Aguarde o tempo calculado (retirado do header da Azion usando o request acima)
    if expires_in_seconds > 0:
        print(f"Aguardando {expires_in_seconds} segundos para o cache expirar...")
        await asyncio.sleep(expires_in_seconds)

    # Código para clicar no botão através do XPath
    selector = '/html/body/header/div/a'  # Substitua pelo XPath do seu browser - esse foi pego do meu usando o Iphone Pro 12 ( pode variar)
    await page.waitForXPath(selector)
    link = await page.xpath(selector)
    if link:
        await link[0].click()
        print("Clicou no link")
    else:
        print("Link não encontrado")

    # Aguarde um pouco antes de fechar
    await asyncio.sleep(60)

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
