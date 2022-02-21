# Semestrální projekt do předmětu BI-PYT 21/22

## Ovládání
Hráč se pohybuje pomocí `WSAD` a střílí pomocí `šipek`.
Po vyčištění místnosti stačí stisknout klávesu E pro pokračování do další místnosti.
Hráč může použít teleport pomocí stisku `pohybové klávesy + mezerníku`.
Stiskem Q hráč změní způsob vykreslování.

## Gameplay
Hráč se ocitá v náhodně generovaných místnostech s několika druhy nepřátel. Cílem je vyčistit co nejvíce místností.

Hráč může střílet (`šipky`) a teleportovat se `WSAD + mezerník`. Hlavně se vyhýbejte ohnivým polím, protože můžou hodně zabolet!

Nepřátelé se:
- pohybují po zemi pomocí A* algoritmu a vyhýbají se ohnivým plochám
- létají

Nepřátelé mají několik režimů střelby, takže pozor na ně!

## Instalace
Stačí stáhnout adresář a je zde připraveno conda prostředí s názvem `semestral-work`, stačí tedy spustit

```shellscript
conda env create --name semestral-work --file=environment.yml
conda activate semestral-work
```

Následně stačí spustit soubor `__main__.py` v kořeni adresáře `sw`.

Testy testují dle mého potřebnou funkcionalitu, ostatní testy jsou založené na otestovaných věceh. Spustíte je příkazem `pytest`.
