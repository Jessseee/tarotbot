import json
from random import choice, choices
from PIL import Image
from os import path


class Card:
    def __init__(self, name: str, desc: list[str, str, str]):
        self.name = name
        self.desc = desc
        self.image = Image.open(path.join(path.dirname(__file__), "..", "deck", f"{self.name}.png"))


class Deck:
    def __init__(self):
        with open("deck.json", 'r') as file:
            cards = json.load(file)
        self.cards = [Card(k, v) for k, v in cards]

    def draw3(self) -> list[Card]:
        return choices(self.cards, k=3)


def cards_image(cards: list[Card, Card, Card]):
    card_images = [card.image for card in cards]
    card_width = max(map(lambda x: x.width, card_images))
    card_height = max(map(lambda x: x.height, card_images))
    image_border = 20
    total_width = (3 * card_width + 4 * image_border)
    total_height = (card_height + 2 * image_border)
    image = Image.new('RGBA', (total_width, total_height), (255, 0, 0, 0))
    image.paste(card_images[0], (image_border, image_border))
    image.paste(card_images[1], (2 * image_border + card_width, image_border))
    image.paste(card_images[2], (3 * image_border + 2 * card_width, image_border))
    return image
