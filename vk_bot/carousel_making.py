import json


def make_carousel_element_data(title, description, link, photo_id):
    return {
        "title": title[:76] + '...',  # Vkontakte doesn't allow sending more characters
        "description": description,
        "action": {
            "type": "open_link",
            "link": link
        },
        "photo_id": photo_id,
        "buttons": [{
            "action": {
                "type": "open_link",
                "label": "Перейти к новости",
                "link": link,
            }
        }]
    }


def make_carousel(elements):
    return json.dumps({
        "type": "carousel",
        "elements": elements
    })


def get_carousel_from_news(news):
    elements = []
    for current_news in news:
        elements.append(
            make_carousel_element_data(current_news.title, str(current_news.date), current_news.link,
                                       current_news.photo_id))
    return make_carousel(elements)

