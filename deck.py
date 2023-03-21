import json
from random import choices
from PIL import Image
from os import path


class Card:
    def __init__(self, name: str, desc: list[str, str, str]):
        """
        A Tarot card.

        :param name: The name of the card (corresponding to image file name)
        :param desc: The three-word description of the card.
        """
        self.name = name
        self.readable_name = self.name.replace('_', ' ').title()
        self.desc = desc
        self.image = Image.open(path.join(path.dirname(__file__), "deck", f"{self.name}.png"))


class Deck:
    def __init__(self):
        """ A deck containing all available Tarot cards. """
        with open("deck.json", 'r') as file:
            cards = json.load(file)
        self.cards = [Card(k, v) for k, v in cards.items()]

    def draw3(self) -> list[Card]:
        """
        Draw three Tarot cards from the deck.

        :return: Three Tarot cards.
        """
        return choices(self.cards, k=3)


def display_three_cards(cards: list[Card, Card, Card], image_border: int = 20):
    """
    Creates an image containing three Tarot cards.

    :param cards: A list of three Tarot cards.
    :param image_border: The distance between the cards in the resulting image.
    :return: The image with three Tarot cards.
    """
    card_images = [card.image for card in cards]

    # Calculate max width/height per card
    card_width = max(map(lambda x: x.width, card_images))
    card_height = max(map(lambda x: x.height, card_images))

    # Calculate size of final image
    total_width = (3 * card_width + 4 * image_border)
    total_height = (card_height + 2 * image_border)

    # Paste cards into larger image
    image = Image.new('RGBA', (total_width, total_height), (255, 0, 0, 0))
    image.paste(card_images[0], (image_border, image_border))
    image.paste(card_images[1], (2 * image_border + card_width, image_border))
    image.paste(card_images[2], (3 * image_border + 2 * card_width, image_border))

    return image
