class Territory:
    name: str
    player: int = 0
    armies: int
    neighbors: list
    loc: tuple[int, int]

    def __init__(self, name, armies = 0, location = (0,0)):
        self.name = name
        self.armies = armies
        self.neighbors = []
        self.loc = location

SELECTED = []

TERRITORIES: dict[str, Territory] = {
    # NORTH AMERICA
    "Alaska" : Territory(name="Alaska",location=(42,32)),
    "Northwest Territory" : Territory(name="Northwest Territory",location=(122,42)),
    "Greenland" : Territory(name="Greenland",location=(320,72)),
    "Alberta" : Territory(name="Alberta",location=(100,100)),
    "Ontario" : Territory(name="Ontario",location=(172,110)),
    "Quebec" : Territory(name="Quebec",location=(242,118)),
    "Western United States" : Territory(name="Western United States",location=(86,160)),
    "Eastern United States" : Territory(name="Eastern United States",location=(146,172)),
    "Central America" : Territory(name="Central America",location=(110,220)),
    # SOUTH AMERICA
    "Venezuela" : Territory(name="Venezuela",location=(140,290)),
    "Peru" : Territory(name="Peru",location=(120,340)),
    "Brazil" : Territory(name="Brazil",location=(200,320)),
    "Argentina" : Territory(name="Argentina",location=(160,410)),
    # AFRICA
    "North Africa" : Territory(name="North Africa",location=(310,330)),
    "Egypt" : Territory(name="Egypt",location=(365,320)),
    "East Africa" : Territory(name="East Africa",location=(400,350)),
    "Congo" : Territory(name="Congo",location=(370,390)),
    "South Africa" : Territory(name="South Africa",location=(360,430)),
    "Madagascar" : Territory(name="Madagascar",location=(420,440)),
    # EUROPE
    "Iceland" : Territory(name="Iceland",location=(315,140)),
    "Scandinavia" : Territory(name="Scandinavia",location=(390,95)),
    "Ukraine" : Territory(name="Ukraine",location=(420,180)),
    "Great Britain" : Territory(name="Great Britain",location=(300,210)),
    "Northern Europe" : Territory(name="Northern Europe",location=(370,210)),
    "Southern Europe" : Territory(name="Southern Europe",location=(400,240)),
    "Western Europe" : Territory(name="Western Europe",location=(340,260)),
    # AUSTRALIA
    "Indonesia" : Territory(name="Indonesia",location=(560,345)),
    "New Guinea" : Territory(name="New Guinea",location=(610,350)),
    "Western Australia" : Territory(name="Western Australia",location=(560,400)),
    "Eastern Australia" : Territory(name="Eastern Australia",location=(600,410)),
    # ASIA
    "Siam" : Territory(name="Siam",location=(560,280)),
    "India" : Territory(name="India",location=(515,280)),
    "China" : Territory(name="China",location=(525,230)),
    "Mongolia" : Territory(name="Mongolia",location=(540,180)),
    "Japan" : Territory(name="Japan",location=(605,180)),
    "Irkutsk" : Territory(name="Irkutsk",location=(540,105)),
    "Yakutsk" : Territory(name="Yakutsk",location=(565,60)),
    "Kamchatka" : Territory(name="Kamchatka",location=(580,90)),
    "Siberia" : Territory(name="Siberia",location=(500,120)),
    "Afghanistan" : Territory(name="Afghanistan",location=(465,215)),
    "Ural" : Territory(name="Ural",location=(475,120)),
    "Middle East" : Territory(name="Middle East",location=(460,270)),
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
