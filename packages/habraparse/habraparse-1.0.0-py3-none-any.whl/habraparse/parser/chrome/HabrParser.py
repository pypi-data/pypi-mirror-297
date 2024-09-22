
from logging import debug, info

from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By

from habraparse.habr import HabraTopic

class HabrParser:

    def parse(self, page: str) -> HabraTopic:
        """ Производит парсинг страницы и заполнение модели """

        topic = HabraTopic()

        # Step 1. Start Chrome driver
        options = ChromeOptions()
        options.binary_location = "/usr/bin/chromium-browser"
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = Chrome(options=options)

        # Step 2. Retrive Habr article
        driver.get(page)
        sleep(5)

        # Step 3. Parse post title
        post_titles = driver.find_elements(By.XPATH, "//h1[contains(@class,'tm-title')]/span")
        post_title_len = len(post_titles)
        if post_title_len > 0:
            post_title = post_titles[0]
            post_title = post_title.get_attribute('innerHTML')
            post_title = post_title.strip("\r\n")
            info("Article page title {post_title!r}".format(post_title=post_title))
            topic.post['title'] = post_title

        # Step 4. Parse article author
        topic.post['author'] = '' # TODO - parse author address ...
        topic.post['author_url'] = '' # TODO - parse author address ...

        # Step 5. Stylesheet
        post_stylesheets = driver.find_elements(By.XPATH, "//link[@rel='stylesheet']")
        stylesheets = []
        for post_stylesheet in post_stylesheets:
            href = post_stylesheet.get_attribute('href')
            stylesheets.append(href)
        topic.post['stylesheets'] = stylesheets

        # Step 5. Styles
        post_styles = driver.find_elements(By.XPATH, "//style")
        styles = []
        for post_style in post_styles:
            style = post_style.get_attribute('innerHTML')
            styles.append(style)
        topic.post['styles'] = "\n".join(styles)

        # Step 6. Parse article body
        post_article_body = driver.find_elements(By.XPATH, "//div[contains(@class, 'article-formatted-body')]")
        #post_article_body = driver.find_elements(By.XPATH, "//div[contains(@class, 'tm-article-body')]")

        post_article_body_len = len(post_article_body)
        if post_article_body_len > 0:
            post_article_body = post_article_body[0]
            post_article_body = post_article_body.get_attribute('innerHTML')
            topic.post['text'] = post_article_body
        #
        driver.close()
        #
        return topic
