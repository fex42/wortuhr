class LetterGenerator:
    """A generator for the letters that respect the order of GridLocations"""


    def __init__(self,
        cnt_x = 11, # number of letters in a row
        cnt_y = 10 # number of letter rows
    ):
        self.cnt_x = cnt_x
        self.cnt_y = cnt_y
        letters_fr = [
            "ILNESTODEUX",
            "QUATRETROIS",
            "NEUFUNESEPT",
            "HUITSIXCINQ",
            "MIDIXMINUIT",
            "ONZERHEURES",
            "MOINSOLEDIX",
            "ETRQUARTPMD",
            "VINGT-CINQU",
            "ETSDEMIEPAM"
        ]

        letters_de_alt = [
            "ESKISTLFÜNF",
            "ZEHNZWANZIG",
            "DREIVIERTEL",
            "NACHAPPYVOR",
            "HALBIRTHDAY",
            "DRZWÖLFÜNFX",
            "ZEHNEUNDREI",
            "ZWEINSIEBEN",
            "ELFVIERACHT",
            "SECHSIUHRYE"
        ]

        letters_de = [
            "ESKISTRFÜNF",
            "ZEHNZWANZIG",
            "DREIVIERTEL",
            "TGNACHVORUM",
            "HALBGZWÖLFJ",
            "ZWEINSIEBEN",
            "KDREIRHFÜNF",
            "ELFNEUNVIER",
            "NACHTZEHNBX",
            "USECHSFUHRY"
        ]

        letters_en = [
            "ITLISASAMPM",
            "ACQUARTERDC",
            "TWENTYFIVEX",
            "HALFSTENFTO",
            "PASTERUNINE",
            "ONESIXTHREE",
            "FOURFIVETWO",
            "EIGHTELEVEN",
            "SEVENTWELVE",
            "TENSEOCLOCK"
        ]

        self.letters = letters_de_alt

        self._x = self.cnt_x
        self._y = 1

    def next_char(self):
        c = self.letters[self._y-1][self._x-1]
#        print(f"next_char(x = {self._x}, y={self._y}) -> {c}")
        self._y += 1
        if self._y > self.cnt_y:
            self._y = 1
            self._x -= 1
        if self._x <= 0:
            self._x = self.cnt_x
        return c

if __name__ == '__main__':
    gen = LetterGenerator()
    for x in range(11):
        for y in range(10):
            print(gen.next_char() + " ", end="")
        print()