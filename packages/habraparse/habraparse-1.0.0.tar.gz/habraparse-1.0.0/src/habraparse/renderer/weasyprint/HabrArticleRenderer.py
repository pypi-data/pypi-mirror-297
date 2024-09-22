
from logging import basicConfig, DEBUG, INFO, debug, info
from argparse import ArgumentParser
from pathlib import Path

from weasyprint import HTML, CSS

from .habr.topic import HabraTopic
from .parser import HabrParser, HabrParserModern

def prepare_html(topic):
    t = topic
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
    html = html_format.format(title=t.title(), author=t.author(), author_url=t.author_url(), text=t.text(), style=t.styles(), styles=styles )
    html = str(html).replace('"//habrastorage.org', '"https://habrastorage.org')
    return html

def main():
    # Step 1. Parse parameters
    parser = ArgumentParser(prog='habraparse')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Включить отладочный вывод')
    subparsers = parser.add_subparsers()
    parser_save_post = subparsers.add_parser('save_post', help='Используется для сохранения публикации')
    parser_save_post.add_argument('topic_id', help='Ссылка на публикацию')
    parser_save_post.add_argument('--output', help='Имя выходного файла')
    parser_save_post.add_argument('--raw', help='Имя подготовленного для печати в PDF выходного файла')
    args = parser.parse_args()
    # Step 2. Enable verbose output
    if args.verbose:
       basicConfig(filename='habraparse.log', level=DEBUG)
    else:
       basicConfig(filename='habraparse.log')
    # Step 3. Debug output
    debug(args)
    # Step 4. Check nad create output directory
    if args.output:
        name = args.output
    else:
        name = args.topic_id
    fname = Path(name)
    fname.parent.mkdir(parents=True, exist_ok=True)
    fname = fname.with_suffix('.pdf')
    debug("Output name {fname}".format(fname=fname))
    # Step 5. Retrive article
    #parser = HabrParser()
    parser = HabrParserModern()
    ht = parser.parse(topic_id=args.topic_id)
    # Step 6. Render article
    html = prepare_html(ht)
    if args.raw:
        raw_out_path = Path(args.raw)
        raw_out_path.parent.mkdir(parents=True, exist_ok=True)
        raw_out_path.write_text(html)
    css = CSS(string='@page { size: A4; margin: 0.5cm; !important;} img { width: 100%; height: auto; !important; } code { width: 100%; height: auto; white-space: pre-wrap; !important; } table { width: 100%; height: auto; !important; }')
    page_css = CSS(string=ht.styles())
    HTML(string=html).write_pdf(fname, stylesheets=[css, page_css],
        jpeg_quality=95,
    )
