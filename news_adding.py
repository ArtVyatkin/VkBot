from datetime import datetime
import pandas as pd

from vk_bot.image_handler import ImageHandler


def set_news_data(vk_bot, crawler, start_date, university_name, keywords=None):
    if keywords is None:
        keywords = []
    image_handler = ImageHandler(vk_bot)
    current_crawler = crawler(start_date, keywords)
    news = current_crawler.get_news()
    aggregated_news = pd.DataFrame(columns=["university", "title", "link", "date", "photo_link", "theme"])
    aggregated_news = aggregated_news.append(news)
    for i in range(0, aggregated_news.shape[0]):
        photo_id = image_handler.load_image_for_carousel(aggregated_news.get("photo_link")[i])
        date = datetime.strptime(aggregated_news.get("date")[i], "%d %b %Y").date()
        title = aggregated_news.get("title")[i].strip()
        link = aggregated_news.get("link")[i]
        theme = aggregated_news.get("theme")[i]
        vk_bot.db.add_news(date=date, university=university_name, title=title, link=link, photo_id=photo_id,
                           theme=theme)
