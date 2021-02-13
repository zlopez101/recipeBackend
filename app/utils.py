import requests
from bs4 import BeautifulSoup
import re
import unicodedata


def makeIngredient(ingredient: str) -> str:
    """make ingredient ready for ingestion by program

    :param ingredient: a raw ingredient string from the recipe link
    :type ingredient: str
    :return: cleaned ingredient string
    :rtype: str
    """
    return removeLeadingSpaces(
        vulgarFractions(cleanIngredient(replaceNewLine(ingredient)))
    )


def cleanIngredient(ingredient: str) -> str:
    """Remove all other characters from the ingredient string

    :param ingredient: a raw ingredient string from the recipe link
    :type ingredient: str
    :return: cleaned ingredient string
    :rtype: str
    """
    return "".join(
        [char if char.isalnum() or char in "/.-()" else " " for char in ingredient]
    )


def removeLeadingSpaces(ingredient: str) -> str:
    """Remove the leading space if any

    :param ingredient: a raw ingredient string from the recipe link
    :type ingredient: str
    :return: cleaned ingredient string
    :rtype: str
    """
    if not (ingredient.startswith(" ")):
        return ingredient
    else:
        return removeLeadingSpaces(ingredient[1:])


def replaceNewLine(ingredient: str) -> str:
    """replace the '\n' character with a space

    :param ingredient: [description]
    :type ingredient: str
    :return: [description]
    :rtype: str
    """
    return ingredient.replace(r"\n", " ")


def vulgarFractions(ingredient: str) -> str:
    """Removes the "Vulgar Fractions from the ingredient string"
    see:
        https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=[:Decomposition_Type=Fraction:]
        https://stackoverflow.com/questions/49440525/detect-single-string-fraction-ex-%C2%BD-and-change-it-to-longer-string


    :param ingredient: [description]
    :type ingredient: str
    :return: [description]
    :rtype: float
    """
    res = []
    for char in ingredient:
        try:
            name = unicodedata.name(char)
        except ValueError:
            continue
        if name.startswith("VULGAR FRACTION"):
            normalized = unicodedata.normalize("NFKC", char)
            res.append(normalized)
        else:
            res.append(char)
    return "".join(res)


def getRecipe(url: str, userId: str) -> dict:
    """for the provided url, get all the information associated with the page

    :param url: url supplied by the user in the twilio webhook
    :type url: str
    :param userId: userId supplied
    :type userId: str
    :return: dict with name, url, source, ingredients
    :rtype: dict
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")

    def getIngredients(soup: BeautifulSoup) -> list:
        """get ingredients

        :param soup: Soup of url
        :type soup: BeautifulSoup
        :return: list of ingredients
        :rtype: list
        """
        return [
            makeIngredient(item.text)
            for item in soup("li", class_=re.compile(r"[a-z-]*ingredient"))
        ]

    def getTitleAndSource(soup: BeautifulSoup) -> (str, str):
        title = soup.select("title")[0].text
        return [removeLeadingSpaces(text) for text in title.split("-")]

    title, source = getTitleAndSource(soup)
    ingredients = getIngredients(soup)
    return dict(
        name=title, source=source, ingredients=ingredients, url=url, userId=userId
    )
