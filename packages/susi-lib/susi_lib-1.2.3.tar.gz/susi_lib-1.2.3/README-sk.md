# susi-lib

Python knižnica pre organizátorov [SuŠi](https://susi.trojsten.sk).

## Prehľad

Sú tu triedy pre reprezentáciu reťazcov v morzeovke, braille, semafore a ako poradia v abecede a trieda, ktorá vie premieňať medzi týmito kódovaniami.

Tiež je tu kolekcia funkcií, ktoré sa často môžu hodiť pri hľadaní hesiel a netreba ich programovať nanovo.

Triedy na vyhľadávanie slov v zadanom zozname slov/súbore.

Aplikácia pre terminál na vyhľadávanie slov v súbore.

## Inštalácia

Treba mať nainštalovaný python. Treba si otvoriť príkazový riadok a spustiť nasledujúci príkaz.

### Linux

```bash
python -m pip install susi-lib
```

Niektoré linuxy (napr. Arch) vedia mať problém s globálnym inštalovaním python balíčkov. Treba vtedy skúsiť user inštaláciu. Ak ani to nepomôže, tak treba použiť virtual environment (napríklad builtin venv) - verím, že ak máš linux, tak vieš čo to je a nebudem to tu vysvetľovať.

### Windows

```bash
py -m pip install susi-lib
```

TODO: otestovať inštaláciu na windowse a popísať riešenie problémov

## Použivanie

Na použitie v kóde treba balíček importovať. To sa robí kľúčovým slovom `import` a po ňom napísať názov balíčka `import susi_lib`. Ďalej v kóde sa dajú jednotlivé triedy/funkcie použiť ako `susi_lib.<podbalíček>.<vec>`, kde vec je väčšinou nejaká funkcia/trieda a podbalíček je "cesta" k danej veci. Štruktúra balíčka je nižšie. Alebo sa dá daná vec importnúť aj nasledovne `from susi_lib.<podbalíček> import <vec>`, vo zvyšku kódu potom viete danú vec používať aj iba napísaním vec bez "cesty".

```no
susi_lib
├─ functions (podbalíček)
│   └─ obsahuje nejaké funkcie
├─ types (podbalíček)
│   └─ obsahuje triedy na reprezentáciu slov v kódovaniach
├─ Finder (vec) - trieda na hľadanie slov pomocou aplikácie zadanej funkcie na každé slovo,
│      táto funkcia urči, či dané slovo chceme alebo nie
├─ RegEx (vec) - trieda na hľadanie pomocou regulárnych výrazov
├─ create_regex (vec) - funkcia, ktorá vytvorí regulárny výraz z postupnosti zadaných písmen
├─ Selection (vec) - pomocný enum pre funkciu create_regex
└─ Dictionary (vec) - trieda, ktorá automaticky stiahne požadovaný slovník a vráti cestu k nemu
```

Podrobnejšia dokumentácia jednotlivých vecí vznikne v blízkej budúcnosti, zatiaľ existujú iba komentáre pre jednotlivé veci, ktoré vie každý rozumnejší code editor zobraziť v náhľade.

### Príklady použitia

Ukážkové programy sa nachádzajú v priečinku examples:

- `finder_example.py`

## Aplikácia `susi-word-finder`

TODO: prepísať dokumentáciu zo starej verzie a pridať popis pre nové features

## Feedback

Budem rád za hocijaký feedback na ktorúkoľvek časť knižnice alebo aj dokumentáciu. Preferované formy komunikácie sú správa na Slacku alebo vytvorenie issue priamo na GitHube.

Ak chceš pridať nejakú feature, ktorú vieš naprogramovať, tak si sprav pull request s danou feature (v budúcnosti možno pribudne návod na nástroje, ktoré tu používam).
