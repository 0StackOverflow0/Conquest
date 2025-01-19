class Territory:
    name: str
    player: int = 0
    armies: int
    neighbors: list

    def __init__(self, name, armies = 0):
        self.name = name
        self.armies = armies
        self.neighbors = []

TERRITORIES: dict[str, Territory] = {
    # NORTH AMERICA
    "Alaska" : Territory(name="Alaska"),
    "Northwest Territory" : Territory(name="Northwest Territory"),
    "Greenland" : Territory(name="Greenland"),
    "Alberta" : Territory(name="Alberta"),
    "Ontario" : Territory(name="Ontario"),
    "Quebec" : Territory(name="Quebec"),
    "Western United States" : Territory(name="Western United States"),
    "Eastern United States" : Territory(name="Eastern United States"),
    "Central America" : Territory(name="Central America"),
    # SOUTH AMERICA
    "Venezuela" : Territory(name="Venezuela"),
    "Peru" : Territory(name="Peru"),
    "Brazil" : Territory(name="Brazil"),
    "Argentina" : Territory(name="Argentina"),
    # AFRICA
    "North Africa" : Territory(name="North Africa"),
    "Egypt" : Territory(name="Egypt"),
    "East Africa" : Territory(name="East Africa"),
    "Congo" : Territory(name="Congo"),
    "South Africa" : Territory(name="South Africa"),
    "Madagascar" : Territory(name="Madagascar"),
    # EUROPE
    "Iceland" : Territory(name="Iceland"),
    "Scandinavia" : Territory(name="Scandinavia"),
    "Ukraine" : Territory(name="Ukraine"),
    "Great Britain" : Territory(name="Great Britain"),
    "Northern Europe" : Territory(name="Northern Europe"),
    "Southern Europe" : Territory(name="Southern Europe"),
    "Western Europe" : Territory(name="Western Europe"),
    # AUSTRALIA
    "Indonesia" : Territory(name="Indonesia"),
    "New Guinea" : Territory(name="New Guinea"),
    "Western Australia" : Territory(name="Western Australia"),
    "Eastern Australia" : Territory(name="Eastern Australia"),
    # ASIA
    "Siam" : Territory(name="Siam"),
    "India" : Territory(name="India"),
    "China" : Territory(name="China"),
    "Mongolia" : Territory(name="Mongolia"),
    "Japan" : Territory(name="Japan"),
    "Irkutsk" : Territory(name="Irkutsk"),
    "Yakutsk" : Territory(name="Yakutsk"),
    "Kamchatka" : Territory(name="Kamchatka"),
    "Siberia" : Territory(name="Siberia"),
    "Afghanistan" : Territory(name="Afghanistan"),
    "Ural" : Territory(name="Ural"),
    "Middle East" : Territory(name="Middle East"),
}

TERRITORIES["Alaska"].neighbors = [
    TERRITORIES["Northwest Territory"],
    TERRITORIES["Alberta"],
    TERRITORIES["Kamchatka"]
]
TERRITORIES["Northwest Territory"].neighbors = [
    TERRITORIES["Greenland"],
    TERRITORIES["Alaska"],
    TERRITORIES["Ontario"],
    TERRITORIES["Alberta"]
]
TERRITORIES["Alberta"].neighbors = [
    TERRITORIES["Western United States"],
    TERRITORIES["Northwest Territory"],
    TERRITORIES["Ontario"],
    TERRITORIES["Alaska"]
]
TERRITORIES["Western United States"].neighbors = [
    TERRITORIES["Central America"],
    TERRITORIES["Ontario"],
    TERRITORIES["Eastern United States"],
    TERRITORIES["Alberta"]
]
TERRITORIES["Central America"].neighbors = [
    TERRITORIES["Western United States"],
    TERRITORIES["Eastern United States"],
    TERRITORIES["Venezuela"]
]
TERRITORIES["Eastern United States"].neighbors = [
    TERRITORIES["Quebec"],
    TERRITORIES["Ontario"],
    TERRITORIES["Western United States"],
    TERRITORIES["Central America"]
]
TERRITORIES["Quebec"].neighbors = [
    TERRITORIES["Greenland"],
    TERRITORIES["Eastern United States"],
    TERRITORIES["Ontario"]
]
TERRITORIES["Ontario"].neighbors = [
    TERRITORIES["Alberta"],
    TERRITORIES["Western United States"],
    TERRITORIES["Eastern United States"],
    TERRITORIES["Quebec"],
    TERRITORIES["Northwest Territory"],
    TERRITORIES["Greenland"]
]
TERRITORIES["Greenland"].neighbors = [
    TERRITORIES["Northwest Territory"],
    TERRITORIES["Quebec"],
    TERRITORIES["Ontario"],
    TERRITORIES["Iceland"]
]

TERRITORIES["Venezuela"].neighbors = [
    TERRITORIES["Central America"],
    TERRITORIES["Brazil"],
    TERRITORIES["Peru"]
]
TERRITORIES["Peru"].neighbors = [
    TERRITORIES["Venezuela"],
    TERRITORIES["Brazil"],
    TERRITORIES["Argentina"]
]
TERRITORIES["Brazil"].neighbors = [
    TERRITORIES["Venezuela"],
    TERRITORIES["Peru"],
    TERRITORIES["Argentina"],
    TERRITORIES["North Africa"]
]
TERRITORIES["Argentina"].neighbors = [
    TERRITORIES["Peru"],
    TERRITORIES["Brazil"]
]

TERRITORIES["North Africa"].neighbors = [
    TERRITORIES["Brazil"],
    TERRITORIES["Western Europe"],
    TERRITORIES["Egypt"],
    TERRITORIES["East Africa"],
    TERRITORIES["Congo"]
]
TERRITORIES["Egypt"].neighbors = [
    TERRITORIES["Southern Europe"],
    TERRITORIES["North Africa"],
    TERRITORIES["East Africa"],
    TERRITORIES["Middle East"],
]
TERRITORIES["East Africa"].neighbors = [
    TERRITORIES["North Africa"],
    TERRITORIES["Congo"],
    TERRITORIES["South Africa"],
    TERRITORIES["Madagascar"],
    TERRITORIES["Middle East"],
    TERRITORIES["Egypt"],
]
TERRITORIES["Congo"].neighbors = [
    TERRITORIES["North Africa"],
    TERRITORIES["South Africa"],
    TERRITORIES["East Africa"],
]
TERRITORIES["South Africa"].neighbors = [
    TERRITORIES["Congo"],
    TERRITORIES["Madagascar"],
    TERRITORIES["East Africa"],
]
TERRITORIES["Madagascar"].neighbors = [
    TERRITORIES["South Africa"],
    TERRITORIES["East Africa"],
]

TERRITORIES["Indonesia"].neighbors = [
    TERRITORIES["Siam"],
    TERRITORIES["New Guinea"],
    TERRITORIES["Western Australia"],
]
TERRITORIES["New Guinea"].neighbors = [
    TERRITORIES["Indonesia"],
    TERRITORIES["Western Australia"],
    TERRITORIES["Eastern Australia"],
]
TERRITORIES["Western Australia"].neighbors = [
    TERRITORIES["Indonesia"],
    TERRITORIES["New Guinea"],
    TERRITORIES["Eastern Australia"],
]
TERRITORIES["Eastern Australia"].neighbors = [
    TERRITORIES["Western Australia"],
    TERRITORIES["New Guinea"],
]

TERRITORIES["Iceland"].neighbors = [
    TERRITORIES["Greenland"],
    TERRITORIES["Great Britain"],
    TERRITORIES["Scandinavia"],
]
TERRITORIES["Scandinavia"].neighbors = [
    TERRITORIES["Iceland"],
    TERRITORIES["Great Britain"],
    TERRITORIES["Northern Europe"],
    TERRITORIES["Ukraine"],
]
TERRITORIES["Ukraine"].neighbors = [
    TERRITORIES["Scandinavia"],
    TERRITORIES["Northern Europe"],
    TERRITORIES["Southern Europe"],
    TERRITORIES["Middle East"],
    TERRITORIES["Afghanistan"],
    TERRITORIES["Ural"],
]
TERRITORIES["Great Britain"].neighbors = [
    TERRITORIES["Iceland"],
    TERRITORIES["Scandinavia"],
    TERRITORIES["Northern Europe"],
]
TERRITORIES["Northern Europe"].neighbors = [
    TERRITORIES["Great Britain"],
    TERRITORIES["Scandinavia"],
    TERRITORIES["Western Europe"],
    TERRITORIES["Southern Europe"],
    TERRITORIES["Ukraine"],
]
TERRITORIES["Southern Europe"].neighbors = [
    TERRITORIES["Western Europe"],
    TERRITORIES["Northern Europe"],
    TERRITORIES["Egypt"],
    TERRITORIES["Ukraine"],
    TERRITORIES["Middle East"],
]
TERRITORIES["Western Europe"].neighbors = [
    TERRITORIES["Northern Europe"],
    TERRITORIES["North Africa"],
    TERRITORIES["Southern Europe"],
]

TERRITORIES["Siam"].neighbors = [
    TERRITORIES["India"],
    TERRITORIES["Indonesia"],
    TERRITORIES["China"],
]
TERRITORIES["India"].neighbors = [
    TERRITORIES["Siam"],
    TERRITORIES["China"],
    TERRITORIES["Middle East"],
    TERRITORIES["Afghanistan"],
]
TERRITORIES["China"].neighbors = [
    TERRITORIES["Siam"],
    TERRITORIES["India"],
    TERRITORIES["Afghanistan"],
    TERRITORIES["Ural"],
    TERRITORIES["Siberia"],
    TERRITORIES["Mongolia"],
]
TERRITORIES["Mongolia"].neighbors = [
    TERRITORIES["Japan"],
    TERRITORIES["China"],
    TERRITORIES["Irkutsk"],
    TERRITORIES["Siberia"],
    TERRITORIES["Kamchatka"],
]
TERRITORIES["Japan"].neighbors = [
    TERRITORIES["Mongolia"],
    TERRITORIES["Kamchatka"],
]
TERRITORIES["Irkutsk"].neighbors = [
    TERRITORIES["Mongolia"],
    TERRITORIES["Kamchatka"],
    TERRITORIES["Yakutsk"],
    TERRITORIES["Siberia"],
]
TERRITORIES["Yakutsk"].neighbors = [
    TERRITORIES["Kamchatka"],
    TERRITORIES["Siberia"],
    TERRITORIES["Irkutsk"],
]
TERRITORIES["Kamchatka"].neighbors = [
    TERRITORIES["Alaska"],
    TERRITORIES["Japan"],
    TERRITORIES["Mongolia"],
    TERRITORIES["Irkutsk"],
    TERRITORIES["Yakutsk"],
]
TERRITORIES["Siberia"].neighbors = [
    TERRITORIES["Ural"],
    TERRITORIES["China"],
    TERRITORIES["Irkutsk"],
    TERRITORIES["Mongolia"],
    TERRITORIES["Yakutsk"],
]
TERRITORIES["Afghanistan"].neighbors = [
    TERRITORIES["Ukraine"],
    TERRITORIES["Middle East"],
    TERRITORIES["India"],
    TERRITORIES["China"],
    TERRITORIES["Ural"],
]
TERRITORIES["Ural"].neighbors = [
    TERRITORIES["Ukraine"],
    TERRITORIES["Afghanistan"],
    TERRITORIES["China"],
    TERRITORIES["Siberia"],
]
TERRITORIES["Middle East"].neighbors = [
    TERRITORIES["Southern Europe"],
    TERRITORIES["Egypt"],
    TERRITORIES["India"],
    TERRITORIES["Afghanistan"],
    TERRITORIES["Ukraine"],
    TERRITORIES["East Africa"],
]

def validTerritory(territory: str) -> bool:
    return territory in TERRITORIES.keys()
