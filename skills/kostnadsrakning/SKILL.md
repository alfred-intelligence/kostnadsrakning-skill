---
name: kostnadsrakning
description: Genererar svenska rättegångskostnadsräkningar som PDF med periodvis uppdelning, måldelskategorisering och sex analytiska perspektiv (processfas, sammanträde, måldel, kostnadstyp, månad, nyckeltal). Använd detta skill när användaren ber om en kostnadsräkning, kostnadsspecifikation, rättegångskostnader, "kostnadsbilaga", eller behöver redovisa eget arbete och tidsspillan i en svensk domstolsprocess (tingsrätt, hovrätt, HD). Trigga också när användaren vill rekonstruera, sammanställa eller exportera en kostnadsräkning från dagboksblad eller andra källor. Trigga även om användaren nämner DVFS-norm, à-pris, eller hänvisar till 18 kap. rättegångsbalken i kostnadssammanhang.
---

# Svenska rättegångskostnadsräkningar

Genererar professionella kostnadsräkningar för svenska domstolsprocesser som PDF. Skillen hanterar uppdelning per processfas, separation mellan eget arbete och tidsspillan, utläggsredovisning, samt sex analytiska perspektiv på samma underlag.

## När detta skill triggas

Användaren ber om en kostnadsräkning eller kostnadsspecifikation för en svensk domstolsprocess. Vanliga formuleringar:

- "Skapa en kostnadsräkning för målet"
- "Jag behöver redovisa mina rättegångskostnader"
- "Sammanställ vad jag lagt ned i tid"
- "Gör en kostnadsbilaga till överklagandet"
- "Återskapa min kostnadsräkning från dagboksbladet"

## Användarens initiala fråga

Skillen utgår från följande standardförfrågan om användaren inte preciserar annorlunda:

> "Skapa en kostnadsräkning som PDF. Strukturen ska följa processfaser (period 1, period 2, period 3 osv). Eget arbete och tidsspillan redovisas ihop som arbete-och-tidsspillan-poster, med olika à-priser. Utlägg (inklusive körersättning och parkering) redovisas helt separat. Specifikationen ska innehålla kolumner för datum, aktbilaga, beskrivning, vilken del av målet, timmar, à-pris och belopp. Designen ska vara stram och saklig — inga färger som sticker ut. All tid avrundas uppåt till närmaste påbörjade kvart. Utöver huvudredovisningen genereras analytiska sammanställningar per sammanträde, måldel, kostnadstyp, månad och nyckeltal."

## Standardparametrar

Om användaren inte anger något annat:

- **À-pris eget arbete:** 1 000 kr/timme
- **À-pris tidsspillan:** 800 kr/timme
- **Körersättning:** 2,50 kr/km
- **Parkering:** 25 kr per sammanträde
- **Tidsavrundning:** uppåt till närmaste påbörjade kvart (15 min)
- **Delkolumn-förkortningar:** R = räntefrågan, S = skadeståndsfrågan, B = båda/processuellt. Anpassa förkortningarna efter målets natur.

Fråga alltid användaren om à-priserna ska justeras innan PDF genereras. Olika mål och olika klagandetyper har olika tariffer.

## De sex perspektiven

Den färdiga PDF:en innehåller sex sammanställningar av samma underlag:

### Perspektiv A — Per processfas (huvudredovisning)

Den primära redovisningen, uppdelad i tidsmässiga faser av processen. Innehåller samtliga poster med fullständiga detaljer (datum, aktbilaga, beskrivning, måldel, timmar, à-pris, belopp). Avslutas med utläggssektion och totalsumma.

**Periodgränser:** Sammanträden tillhör typiskt slutet av föregående period (dvs. MUF 1-dagen hör till period 1, MUF 2-dagen till period 2). Klargör med användaren om annan indelning önskas.

### Perspektiv B — Per sammanträde

Visar alla kostnader hänförliga till varje sammanträde i målet — förberedelse, restid, sammanträdestid och utlägg. Detta är medvetet "dubbel redovisning" av samma underlag som perspektiv A, men ur sammanträdesperspektiv.

### Perspektiv C — Per måldel

Visar fördelningen mellan målets olika sakfrågor (t.ex. räntefrågan, skadeståndsfrågan, processuellt). Detta är processuellt det viktigaste perspektivet vid 18 kap. 4 § rättegångsbalken-bedömning eftersom det möjliggör proportionerlig bedömning av arbetsinsatsens fördelning.

Utlägg räknas tillsammans med "Båda/processuellt" eftersom de inte är hänförliga till någon enskild måldel.

### Perspektiv D — Per kostnadstyp

Visar totalsummans uppdelning på de olika kostnadstyper som ingår: eget arbete, tidsspillan, körersättning, parkering, övriga utlägg. Ger en transparent bild av vad totalsumman består av.

### Perspektiv E — Per månad

Visar kostnadernas kronologiska fördelning per kalendermånad. **Visa även tomma månader med 0 kr och 0,0 % andel** — detta är processuellt viktigt eftersom det visar att arbetet följt processens egen utveckling och inte är en kontinuerlig fakturering. Fyll alltså i alla månader mellan första och sista aktiva månad, inklusive de utan aktivitet.

### Perspektiv F — Nyckeltal

Deskriptiv statistik över de timbaserade arbets- och tidsspillansposterna:

- Totalt antal nedlagda timmar (varav eget arbete / varav tidsspillan)
- Antal separata insatser
- Medeltid per insats
- Median per insats
- Längsta och kortaste enskilda insats
- Totalt antal månader (första–sista aktiva)
- Antal aktiva månader (med kostnad)
- Antal månader utan aktivitet
- Genomsnittlig kostnad per aktiv månad
- Processens längd (första–sista datum)

Det här perspektivet hjälper hovrätten/granskaren att se att timföringen inte är en efterhandskonstruktion — medianen och spridningen ska se realistisk ut för verkligt arbete.

## Strukturkrav

PDF:en ska struktureras enligt följande mall:

```
Rubrik
Underrubrik med målnummer och parter

Inledningstext som beskriver de sex perspektiven
Förklaring av Del-kolumn och à-priser

Perspektiv A — Per processfas
  Period 1 — [beskrivning av fas och datumintervall]
    Tabell: Datum | Aktbil. | Beskrivning | Del | Timmar | À-pris | Belopp
    Delsumma period 1
  Period 2 — ...
  Period 3 — ...
  Summa arbete och tidsspillan
  Utlägg
    Tabell: Datum | Beskrivning | Belopp
    Summa utlägg
  TOTALSUMMA

Perspektiv B — Per sammanträde
  Sammanträde 1 — [datum] ...
  Sammanträde 2 ...
  Sammanträde 3 (huvudförhandling) ...

Perspektiv C — Per måldel
  Tabell + andelar
  Anmärkning om B-kategorin

Perspektiv D — Per kostnadstyp
  Tabell + andelar

Perspektiv E — Per månad
  Tabell med ALLA månader inklusive 0-månader

Perspektiv F — Nyckeltal
  Tabell med deskriptiv statistik
  Anmärkning om medeltid/median som indikator på arbetets karaktär

Datum och ort, klagandens signatur
```

## Kritiska tekniska fallgropar — undvik!

Dessa fel uppstår regelmässigt vid PDF-generering med reportlab och måste aktivt undvikas:

### 1. Thin space (U+202F) renderas som svart fyrkant

Helveticas grundläggande glyfuppsättning innehåller **inte** thin space (`\u202f`). Om du använder den för tusentalsavgränsning kommer talet "1 600 kr" att renderas som "1█600 kr" — svart fyrkant där mellanrummet skulle vara.

**Fel:**
```python
def kr(n):
    return f"{n:,.0f}".replace(",", "\u202f") + " kr"  # Svart fyrkant!
```

**Rätt:**
```python
def kr(n):
    return f"{n:,.0f}".replace(",", "\u00a0") + " kr"  # Non-breaking space (NBSP)
```

Alternativt: använd vanligt mellanslag, eller punkt som tusentalsavgränsare. NBSP (`\u00a0`) ingår i Helveticas grundläggande glyfuppsättning och fungerar säkert.

### 2. Långa beskrivningstexter måste wrappas

Vanlig sträng i en `Table`-cell wrappar **inte** automatiskt — den flyter ut i nästa kolumn istället för att radbrytas. Detta leder till att Del-kolumnens "B" eller "R/S" tränger in mitt i beskrivningstexten ("18:6 RB**B**yrkande" istället för "18:6 RB-yrkande").

**Fel:**
```python
display_data.append([datum, aktbil, beskrivning, del, timmar, ...])
```

**Rätt:**
```python
from reportlab.platypus import Paragraph
cell_style = ParagraphStyle("cell", fontSize=9, leading=11)
display_data.append([
    datum,
    aktbil,
    Paragraph(beskrivning, cell_style),  # Wrappas automatiskt
    del_,
    timmar,
    ...
])
```

Beskrivningskolumnen ska *alltid* använda `Paragraph`-objekt. Korta kolumner som datum, aktbilaga, del, timmar kan vara vanliga strängar.

### 3. Kvart-avrundning

All tid ska avrundas uppåt till närmaste påbörjade kvart (15 min) innan beloppen beräknas:

```python
import math
def round_quarter(timmar):
    return math.ceil(timmar * 4) / 4

# Tillämpa på varje post innan beloppsberäkning:
for p in poster:
    p["timmar"] = round_quarter(p["timmar"])
    p["belopp"] = round(p["timmar"] * p["à_pris"])
```

### 4. Tomma månader i perspektiv E

Visa **alla** månader mellan första och sista aktiva, inklusive de med 0 kr. Detta är processuellt avgörande — det visar att arbete inte skett varje månad, vilket motbevisar misstankar om kontinuerlig (fiktiv) fakturering. Använd en hjälpfunktion som genererar alla månader i intervallet:

```python
def alla_manader_i_intervallet(start_yyyymm, slut_yyyymm):
    start_ar, start_mn = map(int, start_yyyymm.split("-"))
    slut_ar, slut_mn = map(int, slut_yyyymm.split("-"))
    resultat = []
    ar, mn = start_ar, start_mn
    while (ar, mn) <= (slut_ar, slut_mn):
        resultat.append(f"{ar:04d}-{mn:02d}")
        mn += 1
        if mn > 12:
            mn = 1
            ar += 1
    return resultat
```

### 5. Kolumnbredder

Använd millimeter (`mm`) som enhet. För A4 stående med 20mm marginaler finns 170mm att fördela över kolumnerna. För en arbetsrad med 7 kolumner är ett rimligt utgångsläge:

```python
col_widths = [
    22 * mm,  # Datum (yyyy-mm-dd)
    18 * mm,  # Aktbilaga
    70 * mm,  # Beskrivning (alltid Paragraph)
    12 * mm,  # Del (R/S/B)
    16 * mm,  # Timmar
    20 * mm,  # À-pris
    22 * mm,  # Belopp
]
```

## Mall-script

Använd `references/template.py` som utgångspunkt. Det innehåller en komplett implementation med:

- Korrekt `kr()`-funktion med NBSP
- `round_quarter()` för tidsavrundning
- `build_period_table()` som använder `Paragraph` i beskrivningscellen
- `build_utlagg_table()` för utläggsredovisning
- `build_summary_table()` för perspektiv C, D, E
- `build_sammantr_table()` för perspektiv B
- Specialtabell för nyckeltal i perspektiv F
- Funktion för att fylla i tomma månader
- Strama stilar utan stickande färger (ljusgrå header, svart text)
- Exempelstruktur för hela rapporten

Kopiera mallen, fyll i datat, kör scriptet.

## Output

Spara PDF:en till `/mnt/user-data/outputs/` med beskrivande namn som t.ex. `Kostnadsrakning_T_786-25.pdf` eller `Kostnadsrakning_hovratten.pdf`. Använd `present_files` för att dela med användaren.

## Vanliga frågor att ställa innan generering

1. **Vilket mål?** (målnummer, instans, parter)
2. **Vilka processfaser?** (typiskt pre-MUF 1, mellan MUF 1 och MUF 2, post-MUF 2, eventuellt huvudförhandling som separat fas)
3. **À-priser?** (1 000 kr arbete / 800 kr tidsspillan är default men varierar)
4. **Körsträckor och restider** för varje sammanträde
5. **Övriga utlägg** (stämningsavgift, betalningsföreläggande, post m.m.)
6. **Måldelskategorier** — vilka koder ska användas? (R/S/B är default för räntefrågan/skadeståndsfrågan/båda)

## Notering om underliggande timföring

Användaren har ofta sin timföring i blandade källor — Notion-loggar, dagboksblad, e-postkorrespondens. Hjälp användaren rekonstruera systematiskt:

1. Gå igenom dagboksbladet kronologiskt
2. Matcha varje insats mot motsvarande aktbilaga om möjligt
3. Var generös men inte överdriven — håll totalsumman rimlig i relation till målet
4. Notera att AI-stöd kan motivera lägre tidsåtgång på vissa moment
5. Om en pott är angiven (t.ex. "Notion-loggen visar 19 h för perioden"), fördela inom potten — överskrid inte den dokumenterade totalen

## Strategiska överväganden om måldelsfördelning

Måldelskategoriseringen (R/S/B) är processuellt viktigast i perspektiv C. Vid kostnadsbedömning enligt 18 kap. 4 § rättegångsbalken kan en hög andel kostnader hänförliga till den vunna frågan motverka jämkning till klagandens nackdel.

Hjälp användaren att noggrant överväga varje post:

- Hör posten *primärt* till en specifik sakfråga? → R eller S
- Är posten processuell eller hanterar båda frågor? → B
- Var försiktig med att kategorisera bevisning som hör till en fråga men *också* används för en annan — primärsyftet styr

Diskutera särskilt sammanträden och förberedelser där tidpunkten avgör: om ett sammanträde hölls innan en viss sakfråga framställts, är det normalt hänförligt till de frågor som var aktuella vid tidpunkten.
