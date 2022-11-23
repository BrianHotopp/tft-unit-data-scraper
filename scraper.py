import requests
from pathlib import Path
import time
from bs4 import BeautifulSoup
import json
class ChampData():
    """
    A champion in the champion list
    """

    def __init__(self, name, cost, traits, health, armor, magic_resist, mana, attack_damage, attack_speed, attack_range, rarity=None):
        # error check inputs
        # name must be string and between 1 and 15 characters
        if type(name) != str:
            raise TypeError("name must be a string")
        if len(name) < 1 or len(name) > 30:
            raise ValueError("name must be between 1 and 30 characters")
        # cost must be an int between 0 and 10
        if type(cost) != int:
            raise TypeError("cost must be an int")
        if cost < 0 or cost > 10:
            raise ValueError("cost must be between 0 and 10") 
        # rarity must be an int between 1 and 5 if it is given (optional)
        if rarity != None:
            if type(rarity) != int:
                raise TypeError("rarity must be an int")
            if rarity < 1 or rarity > 5:
                raise ValueError("rarity must be between 1 and 5")
        # traits must be a list of strings
        if type(traits) != list:
            raise TypeError("traits must be a list of strings")
        for trait in traits:
            if type(trait) != str:
                raise TypeError("traits must be a list of strings")
        # health must be a dict with keys 1, 2, 3 and integer values between 0 and 20000
        if type(health) != dict:
            raise TypeError("health must be a dict")
        for key in health:
            if type(key) != int:
                raise TypeError("health must be a dict with int keys")
            if key < 1 or key > 3:
                raise ValueError("health must be a dict with int keys between 1 and 3")
            if type(health[key]) != int:
                raise TypeError("health must be a dict with int keys and int values")
            if health[key] < 0 or health[key] > 20000:
                raise ValueError("health must be a dict with int keys and int values between 0 and 20000")
        if type(armor) != int:
            raise TypeError("armor must be an int")
        # magic_resist must be an int   
        if type(magic_resist) != int:
            raise TypeError("magic_resist must be an int")
        # mana must be a dict with keys 1, 2 and int values between 0 and 1000
        if type(mana) != dict:
            raise TypeError("mana must be a dict")
        if 1 not in mana or 2 not in mana:
            raise ValueError("mana must have keys 1 and 2")
        if type(mana[1]) != int or type(mana[2]) != int:
            raise TypeError("mana must have int values")
        if mana[1] < 0 or mana[1] > 1000 or mana[2] < 0 or mana[2] > 1000:
            raise ValueError("mana values must be between 0 and 1000")
        # attack_damage must be a dict with integer keys and float values between 0 and 1000
        if type(attack_damage) != dict:
            raise TypeError("attack_damage must be a dict")
        for key in attack_damage:
            if type(key) != int:
                raise TypeError("attack_damage must be a dict with int keys")
            if key < 1 or key > 3:
                raise ValueError("attack_damage must be a dict with int keys between 1 and 3")
            if type(attack_damage[key]) != float:
                raise TypeError("attack_damage must be a dict with int keys and float values")
            if attack_damage[key] < 0 or attack_damage[key] > 1000:
                raise ValueError("attack_damage values must be between 0 and 1000")
        # attack_speed must be a float between 0 and 10
        if type(attack_speed) != float:
            raise TypeError("attack_speed must be a float")
        if attack_speed < 0 or attack_speed > 10:
            raise ValueError("attack_speed must be between 0 and 1")
        # attack_range must be an int between 1 and 10 
        if type(attack_range) != int:
            raise TypeError("attack_range must be an int")
        if attack_range < 1 or attack_range > 10:
            raise ValueError("attack_range must be between 1 and 10")

        # set instance variables
        self.name = name
        self.cost = cost
        self.rarity = rarity
        self.traits = traits
        self.health = health
        self.attack_damage = attack_damage
        self.attack_speed = attack_speed
        self.attack_range = attack_range
    def __str__(self) -> str:
        """
        Return a string representation of the row
        """
        return f"Name: {self.name}"
class TraitData():
    """
    A row in the trait list
    """
    def __init__(self, name, breaks):
        # error check inputs
        # name must be string and between 1 and 15 characters
        if type(name) != str:
            raise TypeError("name must be a string")
        if len(name) < 1 or len(name) > 30:
            raise ValueError("name must be between 1 and 30 characters")
        # breaks must be a list of integers
        if type(breaks) != list:
            raise TypeError("breaks must be a list of integers")
        for break_ in breaks:
            if type(break_) != int:
                raise TypeError("breaks must be a list of integers")
            if break_ < 0 or break_ > 10:
                raise ValueError("breaks must be a list of integers between 0 and 10")
        # set instance variables
        self.name = name
        self.breaks = breaks
        
def extract_traits(class_or_origin):
    c = []
    details = class_or_origin.findAll("div", class_="details")
    for div in details:
        name = div.find("div", class_="details__pic").find("img").get("src")
        name = Path(name).stem
        breaks = []
        l = div.find("ul", class_="bbcode_list")
        if l != None:
            lis = l.findAll("li")
            if not lis[0].text[0].isdigit():
                breaks = [1]
            else:
                for li in lis:
                    breaks.append(int(li.text[0]))
        else:
            breaks = [1]
        c.append(TraitData(name, breaks))
    return c

def parse_page(raw_scrape_text):
    """
    Parse the raw scrape text
    raw_scrape_text: the raw scrape text
    returns: list of champs as ChampData objects, list of traits as TraitData objects
    """
    champs_list = []
    soup = BeautifulSoup(raw_scrape_text, "html.parser")
    # get divs with class "champions-wrap__details"
    champion_divs = soup.find_all("div", class_="champions-wrap__details")
    # extract name and cost
    for champion_div in champion_divs:
        champ_info = champion_div.find("div", class_="champions-wrap__details__champion__info")
        # name is the text in the span with class "name"
        champion_name = champ_info.find("span", class_="name").text
        # cost is the text in the span with class "cost"
        champion_cost = champ_info.find("span", class_="cost")
        if champion_cost == None:
            champion_cost = 0
        else:
            champion_cost = int(champion_cost.text[:-1])
        # the image srcs contain the traits of the champion
        traits_imgs = champ_info.findAll("img")
        traits = []
        for trait_img in traits_imgs:
            p = Path(trait_img.get("src"))
            # the filename without the extension is the trait name
            trait_name = p.stem
            traits.append(trait_name)
        # get the champion ability name and description
        abil_div = champion_div.find("div", class_="champions-wrap__details__ability")
        ability_name = Path(abil_div.find("img").get("src")).stem
        ability_desc = abil_div.find("span", class_="description").text
        # get the champion stats
        stats = champion_div.findAll("div", class_="champions-wrap__details__stat")
        # health is the first stat
        health = dict([(y[0]+1, y[1]) for y in enumerate([int(x) for x in stats[0].text.split()])])
        # armor is the second stat
        armor = stats[1].text
        armor = int(armor)
        # magic res is the third stat
        magic_res = stats[2].text
        magic_res = int(magic_res)
        # mana is the fourth stat
        mana = stats[3].text
        mana = dict([(y[0]+1, y[1]) for y in enumerate([int(x.strip()) for x in mana.split("/")])])
        # attack_damage is the fifth stat
        attack_damage = stats[4].text
        attack_damage = dict([(y[0]+1, y[1]) for y in enumerate([float(x.strip()) for x in attack_damage.split()])])
        # attack_speed is the sixth stat
        attack_speed = stats[5].text
        attack_speed = float(attack_speed)
        # attack_range is the seventh stat
        attack_range = stats[6].text
        attack_range = int(attack_range)
        # create a ChampData object
        champs_list.append(ChampData(champion_name, champion_cost, traits, health, armor, magic_res, mana, attack_damage, attack_speed, attack_range))
    # hydrate the rarity on the champions
    rarities = {}
    blocks = soup.find("div", class_="cheatsheet").findAll("div", class_="champion")
    for block in blocks:
        rarity = block.find("img").get("class")[0].split("-")[1]
        name = block.find("span").text
        rarities[name] = int(rarity)
    for champ in champs_list:
        if champ.name in rarities:
            champ.rarity = rarities[champ.name]
    # done with champs, now extract the trait data
    traits = []
    over = soup.find("div", class_="synergies-wrap")
    origins = over.find("div", class_ = "origins")
    classes = over.find("div", class_ = "classes")
    traits.extend(extract_traits(origins))
    traits.extend(extract_traits(classes))
    return champs_list, traits

def scrape_page(url, raw_save_folder, cleaned_save_folder):
    """
    Scrape the page and save the data to the artifacts folder
    url (string): the page to scrape
    raw_save_folder (string): the folder to save the raw data to
    cleaned_save_folder (string): the folder to save the cleaned data to
    returns: path to the raw data file, path to the champs file, path to the traits file
    """
    raw_scrape = requests.get(url)
    raw_scrape.raise_for_status()
    scraped_text = raw_scrape.text
    timestamp = str(int(time.time()))
    # save the raw data to a file with a timestamp
    raw_save_path = raw_save_folder / f"{url.split('/')[-1]}-{timestamp}.html"
    with open(raw_save_path, "w") as fh:
        fh.write(raw_scrape.text)
    # parse the raw data
    champs_list, traits = parse_page(scraped_text)
    # save the data as json to files with names based on the timestamp
    champs_save_path = f"{cleaned_save_folder}/champs_{timestamp}.json"
    traits_save_path = f"{cleaned_save_folder}/traits_{timestamp}.json"
    with open(champs_save_path, "w") as fh:
        json.dump(champs_list, fh, indent=4, default=lambda x: x.__dict__)
    with open(traits_save_path, "w") as fh:
        json.dump(traits, fh, indent=4, default=lambda x: x.__dict__)
    return raw_save_path, champs_save_path, traits_save_path




