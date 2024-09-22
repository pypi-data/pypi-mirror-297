# habraparse

Библиотека работы с статями с Habr сделана на основе `habraparse`

## Пример использования

```
from habraparse.parser.classic import HabrParser
from habraparse.renderer.classic import HabrArticleRenderer

topics = ["750270", "750608", "750794", "752132", "751002", "751060"]
for topic in topics:
    parser = HabrParser(topic_id=topic)
    a = parser.parse()
    renderer = HabrArticleRenderer()
    renderer.render(f"article_{topic}.pdf", a)
```
