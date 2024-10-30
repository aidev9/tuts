import os
from pyppeteer import launch
import asyncio

# A python script to convert HTML pages to PDF
# Input: a list of 10 URLs
# Output: 10 PDF files saved in the data directory

# List of 10 OWASP Secure Coding Guide URLs
urls = [
    'https://owasp.org/www-project-developer-guide/release',
    'https://owasp.org/www-project-developer-guide/release/foundations',
    'https://owasp.org/www-project-developer-guide/release/foundations/security_fundamentals',
    'https://owasp.org/www-project-developer-guide/release/foundations/secure_development',
    'https://owasp.org/www-project-developer-guide/release/foundations/security_principles',
    'https://owasp.org/www-project-developer-guide/release/foundations/crypto_principles',
    'https://owasp.org/www-project-developer-guide/release/foundations/owasp_top_ten',
    'https://owasp.org/www-project-developer-guide/release/requirements',
    'https://owasp.org/www-project-developer-guide/release/requirements/requirements_in_practice',
    'https://owasp.org/www-project-developer-guide/release/requirements/risk_profile'
]

# Directory to save PDFs
output_dir = './data'
os.makedirs(output_dir, exist_ok=True)

# Convert each URL to a PDF
async def html_to_pdf(url, output_path):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle2'})
    await page.pdf({'path': output_path, 'format': 'A4'})
    await browser.close()


# Convert each URL to a PDF
for i, url in enumerate(urls):
    output_path = os.path.join(output_dir, f'page_{i+1}.pdf')
    print(f'Converting {url} to {output_path}')
    asyncio.get_event_loop().run_until_complete(html_to_pdf(url, output_path))

print('All URLs converted to PDFs')