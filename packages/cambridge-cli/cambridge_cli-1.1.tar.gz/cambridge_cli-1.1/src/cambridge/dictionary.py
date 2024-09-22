from .utils import response_txt
from .element import Elememt
from bs4 import BeautifulSoup,Tag
from rich.console import Console
import os
import json
from .const import DOMAIN

console = Console()

class Dictionary():

    def __init__(self, word):
        self.word=word
        self.url=f"{DOMAIN}/dictionary/english/{word}"
        self.elements=[]
        self.process()

    def __str__(self):
        return json.dumps(self.__dict__,indent=4,ensure_ascii=False)

    def process(self):

        tag = self.load()
        self.cover_list(tag)
    
    def cover_list(self, diet: Tag) -> None:
        # block
        for item in diet.select("div.pr.entry-body__el"):
            ele = Elememt()
            ele.cover(item)
            self.elements.append(ele)

    def print(self) -> None:

        # word
        console.print(f"## {self.word}",style="bold red")
        console.print(f"## {self.url}",style="red")
        console.print()
        
        for ele in self.elements:
            ele.print()

    def to_dict(self) -> dict:
        return {
            "word": self.word,
            "url": self.url,
            "elements": [element.to_dict() for element in self.elements]
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(),ensure_ascii=False)

    def load(self) -> Tag:
        
        cache_file=f"{self.word}.html"

        if os.path.exists(cache_file):
            with open(cache_file,) as f:
                html=f.read()
        else:
            html = response_txt(self.url)
            with open(f"{self.word}.html", "w") as f:
                f.write(html)

        obj={"data-id":"cald4"}
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find(**obj)


