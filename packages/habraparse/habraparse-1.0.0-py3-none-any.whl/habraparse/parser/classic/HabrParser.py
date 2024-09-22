
from logging import debug, info

from requests import Session
from lxml import etree, html

from habraparse.habr import HabraTopic


class HabrParser:

    def parse(self, topic_id) -> HabraTopic:
        """ Производит парсинг и заполнение модели """
        topic = HabraTopic(topic_id=topic_id)
        topic.post = dict()
        # Step 1. Receive a Habr article
        s = Session()
        resp = s.get(topic.url)
        debug("Habr response code {status_code}".format(status_code=resp.status_code))
        if resp.status_code != 200:
            raise IOError('Not loaded! {url} gives status_code={status_code}'.format(url=self.url, status_code=resp.status_code))
        # Step 2. Parse HTML article
        doc = html.document_fromstring(resp.text)
        # Step 3. Parse post title
        post_titles = doc.xpath("//h1[contains(@class,'tm-title')]/span/text()")
        debug("Article page headers {post_titles!r}".format(post_titles=post_titles))
        post_title_len = len(post_titles)
        if post_title_len > 0:
            post_title = post_titles[0]
            post_title = post_title.strip("\r\n")
            info("Article page title {post_title!r}".format(post_title=post_title))
            topic.post['title'] = post_title
        # Step 4. Parse article author
        topic.post['author'] = '' # TODO - parse author address ...
        topic.post['author_url'] = '' # TODO - parse author address ...
        # Step 5. Parse CSS styles
        post_styles = doc.xpath("//style/text()")
        post_style_len = len(post_styles)
        debug("Article CSS style count {post_style_len}".format(post_style_len=post_style_len))
        debug("Article CSS styles {post_styles!r}".format(post_styles=post_styles))
        style = '\n'.join(post_styles)
        debug("Article style {style}".format(style=style))
        topic.post['styles'] = style
        # Step 6. Parse article body
        post_article_body = doc.xpath("//div[contains(@class, 'tm-article-body')]")
        post_article_body_len = len(post_article_body)
        if post_article_body_len > 0:
            post_article_body = post_article_body[0]
            post_article_body = etree.tostring(post_article_body, pretty_print=True, method='html', encoding='UTF-8', xml_declaration=False)
            post_article_body = post_article_body.decode('utf-8')
            topic.post['text'] = post_article_body
        #
        return topic
