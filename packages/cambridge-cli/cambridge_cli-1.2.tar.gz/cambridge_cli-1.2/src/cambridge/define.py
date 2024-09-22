from bs4 import Tag
from rich.console import Console

console = Console()

class Define:

    def __init__(self):
        self.leval = None
        self.define = None
        self.guide = None
        self.examples = []
    
    def cover_defines(self, tag: Tag):
        self.define = tag.select_one('div.def.ddef_d.db').text

    def cover_examples(self, tag: Tag):

        list = tag.select('span.eg.deg')
        for i in list:
            self.examples.append(i.text)


    def cover_leval(self, tag:Tag) -> None:
        
        leval = tag.select_one("span.epp-xref.dxref")

        if leval:
            self.leval = leval.text
    
    def print(self) -> None:

        console.print(f"### {self.leval}", style="bright_blue")
        console.print(f"{self.define}",style="green")

        console.line()
        for e in self.examples:
            console.print(f"- {e}",style="cyan")
        console.line()

    def to_dict(self) -> dict:
        return {
            "leval": self.leval,
            "define": self.define,
            "guide": self.guide,
            "examples": self.examples,
        }

    def cover_guide(self, tag:Tag) -> None:
        guide = tag.select_one("span.guideword.dsense_gw > span")
        if guide:
            self.guide = guide.text

    def cover(self, tag: Tag) -> dict:

        self.cover_leval(tag)
        self.cover_guide(tag)
        self.cover_defines(tag)
        self.cover_examples(tag)

        return self.__dict__