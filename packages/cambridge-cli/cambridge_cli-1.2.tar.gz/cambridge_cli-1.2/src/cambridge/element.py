from bs4 import Tag
from urllib.parse import urljoin
from .const import DOMAIN
from .define import Define
from rich.console import Console

console = Console()

class Elememt():

    def __init__(self):
        self.pos = None
        self.us_voice = None
        self.uk_voice = None
        self.us_pron = None
        self.uk_pron = None
        self.defines = []

    def cover(self, tag: Tag) -> dict:

        header=tag.select_one("div.pos-header.dpos-h")
        sense_list = tag.select("div.pr.dsense")
        
        self.cover_none(header)
        self.cover_voice(header)

        for sense in sense_list:
            define = Define()
            define.cover(sense)
            self.defines.append(define)
        return self.__dict__

    def print(self) -> None:
        console.print(f"UK {self.uk_pron} US {self.us_pron} \[{self.pos}]")
        console.line()

        for de in self.defines:
            de.print()

    def to_dict(self) -> dict:
        return {
            "pos": self.pos,
            "us_voice": self.us_voice,
            "uk_voice": self.uk_voice,
            "us_pron": self.us_pron,
            "uk_pron": self.uk_pron,
            "defines": [define.to_dict() for define in self.defines],
        }
    
    def cover_none(self, dict:Tag) -> None:
        self.pos = dict.select_one('span.pos.dpos').text   

    def cover_voice(self, dict:Tag) -> None:

        uk_source = dict.select_one("span.uk.dpron-i source[type='audio/mpeg']")
        us_source = dict.select_one("span.us.dpron-i source[type='audio/mpeg']")

        self.us_pron = dict.select_one("span.us.dpron-i span.pron.dpron").text
        self.uk_pron = dict.select_one("span.uk.dpron-i span.pron.dpron").text

        self.us_voice = urljoin(DOMAIN,us_source['src'])
        self.uk_voice = urljoin(DOMAIN,uk_source['src'])