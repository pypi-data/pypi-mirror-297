
from base64 import b64decode, b64encode
from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By

class HabrArticle:
    pass

class HabrArticleRenderer:

    def __init__(self, wait=20.0):
        self.wait = wait

    @staticmethod
    def prepare_html(article: HabrArticle) -> str:
        t = article
        html_format = '''
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <meta charset="UTF-8">
    <title>{title}</title>
    <meta name="author" content="{author}">
    <meta name="generator" content="habraparse">

    {styles}
    <style>{style}</style>
    </head>
    <body>
      <div id="app">
        <div class="tm-article-body">
            <div id="post-content-body">
                <div>
                    <h1 class="tm-title"><span>{title}</span></h1>
                    <div class="author">
                      <a title="Автор текста" href="{author_url}" >{author}</a>
                    </div>
                    <div class="article-formatted-body article-formatted-body article-formatted-body_version-1">
                      <div>
                          {text}
                      </div>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </body>
    </html>
    '''

        stylesheets = []
        if 'stylesheets' in t.post:
            for href in t.post['stylesheets']:
                stylesheets.append('<link rel="stylesheet" href="{href}">'.format(href=href))
        styles = "\n".join(stylesheets)

        style = ""
        style += t.styles()
        style += "@page { size: A4; margin: 0.5cm; !important; }\n"
        style += "img { width: 100%; height: auto; !important; }\n"
        style += "code { width: 100%; height: auto; white-space: pre-wrap; !important; }\n"
        style += "table { width: 100%; height: auto; !important; }\n"

        html = html_format.format(title=t.title(), author=t.author(), author_url=t.author_url(), text=t.text(), style=style, styles=styles )
        html = str(html).replace('"//habrastorage.org', '"https://habrastorage.org')

        return html



    def render(self, article: HabrArticle) -> bytes:
        """ Render PDF page """
        #
        options = ChromeOptions()
        options.binary_location = "/usr/bin/chromium-browser"
#        options.add_argument("--kiosk-printing") # TODO - wtf?
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = Chrome(options=options)
        driver.execute_cdp_cmd("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-color-scheme", "value": "light"}]})
        #
        html_content = HabrArticleRenderer.prepare_html(article)
        with open("debug.html", "w") as stream:
            stream.write(html_content)
        raw = bytes(html_content, 'utf-8')
        b64 = b64encode(raw)
        content = b64.decode('utf-8')
        driver.get(f"data:text/html;base64,{content}")
        #
        sleep(self.wait)
        #
        driver.execute_script("return window.print()")
        pdf = driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": False})
        pdf_data = b64decode(pdf["data"])
        return pdf_data
