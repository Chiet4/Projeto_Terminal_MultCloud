import os
import asyncio
from pyppeteer import launch

# Lista de URLs da documentação AWS CLI
urls = [
    'https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/accept-address-transfer.html',
    'https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/describe-instance-types.html',
    'https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/create-security-group.html',
    'https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/create-key-pair.html',
    'https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/import-key-pair.html'
]

# Criar a pasta "./data" se não existir
output_folder = "data"
os.makedirs(output_folder, exist_ok=True)

async def convert_to_pdf(url, browser):
    """Acessa a URL e salva o conteúdo em um arquivo PDF dentro de ./data"""
    page = await browser.newPage()
    await page.goto(url, {"waitUntil": "networkidle2"})  # Aguarda carregamento completo

    # Nome do arquivo PDF baseado na URL
    filename = url.split("/")[-1].replace(".html", ".pdf")
    output_path = os.path.join(output_folder, filename)

    # Gerar o PDF sem cabeçalhos e rodapés
    await page.pdf({
        'path': output_path,
        'format': 'A4',
        'printBackground': True,
        'displayHeaderFooter': False
    })

    print(f"📄 PDF salvo: {output_path}")
    await page.close()

async def main():
    """Executa a conversão de todas as URLs para PDF"""
    browser = await launch(headless=True, args=['--no-sandbox'])
    
    try:
        tasks = [convert_to_pdf(url, browser) for url in urls]
        await asyncio.gather(*tasks)
    finally:
        await browser.close()  # Fecha corretamente o navegador

# Resolver o problema do loop de eventos fechando corretamente
asyncio.run(main())
