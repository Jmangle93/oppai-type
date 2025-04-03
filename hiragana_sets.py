from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class HiraganaSet:
    name: str
    characters: List[Tuple[str, str]]

vowels = HiraganaSet("vowels", [('a', 'あ'), ('i', 'い'), ('u', 'う'), ('e', 'え'), ('o', 'お')])
k = HiraganaSet("k", [('ka', 'か'), ('ki', 'き'), ('ku', 'く'), ('ke', 'け'), ('ko', 'こ')])
g = HiraganaSet("g", [('ga', 'が'), ('gi', 'ぎ'), ('gu', 'ぐ'), ('ge', 'げ'), ('go', 'ご')])
s = HiraganaSet("s", [('sa', 'さ'), ('shi', 'し'), ('su', 'す'), ('se', 'せ'), ('so', 'そ')])
z = HiraganaSet("z", [('za', 'ざ'), ('ji', 'じ'), ('zu', 'ず'), ('ze', 'ぜ'), ('zo', 'ぞ')])
t = HiraganaSet("t", [('ta', 'た'), ('chi', 'ち'), ('tsu', 'つ'), ('te', 'て'), ('to', 'と')])
d = HiraganaSet("d", [('da', 'だ'), ('ji', 'ぢ'), ('dzu', 'づ'), ('de', 'で'), ('do', 'ど')])
n = HiraganaSet("n", [('na', 'な'), ('ni', 'に'), ('nu', 'ぬ'), ('ne', 'ね'), ('no', 'の'), ('n', 'ん')])
h = HiraganaSet("h", [('ha', 'は'), ('hi', 'ひ'), ('fu', 'ふ'), ('he', 'へ'), ('ho', 'ほ')])
b = HiraganaSet("b", [('ba', 'ば'), ('bi', 'び'), ('bu', 'ぶ'), ('be', 'べ'), ('bo', 'ぼ')])
p = HiraganaSet("p", [('pa', 'ぱ'), ('pi', 'ぴ'), ('pu', 'ぷ'), ('pe', 'ぺ'), ('po', 'ぽ')])
m = HiraganaSet("m", [('ma', 'ま'), ('mi', 'み'), ('mu', 'む'), ('me', 'め'), ('mo', 'も')])
y = HiraganaSet("y", [('ya', 'や'), ('yu', 'ゆ'), ('yo', 'よ')])
r = HiraganaSet("r", [('ra', 'ら'), ('ri', 'り'), ('ru', 'る'), ('re', 'れ'), ('ro', 'ろ')])
w = HiraganaSet("w", [('wa', 'わ'), ('wo', 'を')])
default = HiraganaSet("default", vowels.characters + k.characters + s.characters + t.characters)