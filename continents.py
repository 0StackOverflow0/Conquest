from territories import *

class Continent:
    name: str
    score: int
    territories: list[Territory]

    def __init__(self, name, score):
        self.name = name
        self.score = score
        self.territories = []

CONTINENTS: dict[str, Continent] = {
    "Asia"          : Continent(name="Asia",            score=7),
    "Africa"        : Continent(name="Africa",          score=3),
    "North America" : Continent(name="North America",   score=5),
    "South America" : Continent(name="South America",   score=3),
    "Australia"     : Continent(name="Australia",       score=2),
    "Europe"        : Continent(name="Europe",          score=6)
}

CONTINENTS["Africa"].territories = []
CONTINENTS["Asia"].territories = [
    TERRITORIES["Siam"],
    TERRITORIES["India"],
    TERRITORIES["China"],
    TERRITORIES["Mongolia"],
    TERRITORIES["Japan"],
    TERRITORIES["Irkutsk"],
    TERRITORIES["Yakutsk"],
    TERRITORIES["Kamchatka"],
    TERRITORIES["Siberia"],
    TERRITORIES["Afghanistan"],
    TERRITORIES["Ural"],
    TERRITORIES["Middle East"],
]
CONTINENTS["North America"].territories = [
    TERRITORIES["Alaska"],
    TERRITORIES["Alberta"],
    TERRITORIES["Northwest Territory"],
    TERRITORIES["Western United States"],
    TERRITORIES["Eastern United States"],
    TERRITORIES["Central America"],
    TERRITORIES["Quebec"],
    TERRITORIES["Ontario"],
    TERRITORIES["Greenland"],
]
CONTINENTS["South America"].territories = [
    TERRITORIES["Venezuela"],
    TERRITORIES["Peru"],
    TERRITORIES["Brazil"],
    TERRITORIES["Argentina"],
]
CONTINENTS["Australia"].territories = [
    TERRITORIES["Indonesia"],
    TERRITORIES["New Guinea"],
    TERRITORIES["Western Australia"],
    TERRITORIES["Eastern Australia"],
]
CONTINENTS["Europe"].territories = [
    TERRITORIES["Iceland"],
    TERRITORIES["Scandinavia"],
    TERRITORIES["Great Britain"],
    TERRITORIES["Northern Europe"],
    TERRITORIES["Southern Europe"],
    TERRITORIES["Western Europe"],
    TERRITORIES["Ukraine"],
]