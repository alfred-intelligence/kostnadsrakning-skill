"""Mall för generering av svensk rättegångskostnadsräkning som PDF.

Komplett mall med sex analytiska perspektiv (A–F). Använd som utgångspunkt
— fyll i datat i sektionen 'Data' och kör scriptet.

Kritiska fixar inbyggda:
- NBSP istället för thin space (för att undvika svart fyrkant i Helvetica)
- Paragraph i beskrivningsceller (för korrekt textwrap)
- Kvart-avrundning av all tid
- Tomma månader visas i perspektiv E
"""

import math
import statistics

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.lib.enums import TA_LEFT


# ============================================================================
# Hjälpfunktioner
# ============================================================================

def kr(n):
    """NBSP istället för thin space — renderas korrekt i Helvetica."""
    return f"{n:,.0f}".replace(",", "\u00a0") + " kr"


def round_quarter(timmar):
    """Avrunda uppåt till närmaste påbörjade kvart."""
    return math.ceil(timmar * 4) / 4


def fmt_timmar(t):
    """Formatera timmar utan onödiga nollor."""
    if t == int(t):
        return str(int(t))
    return f"{t:.2f}".rstrip("0").rstrip(".")


def get_manad(datum):
    """Extrahera YYYY-MM från datum."""
    return datum[:7]


def alla_manader_i_intervallet(start_yyyymm, slut_yyyymm):
    """Returnerar alla månader (YYYY-MM) från start till slut, inklusive."""
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


# ============================================================================
# Tabell-byggare
# ============================================================================

def build_period_table(rows, total_label, cell_style):
    """Tabell för perspektiv A (period)."""
    header = ["Datum", "Aktbil.", "Beskrivning", "Del", "Timmar", "À-pris", "Belopp"]
    display_data = [header]

    for r in rows:
        display_data.append([
            r["datum"],
            r["aktbil"],
            Paragraph(r["beskrivning"], cell_style),
            r["del"],
            fmt_timmar(r["timmar"]),
            kr(r["à_pris"]),
            kr(r["belopp"]),
        ])

    total = sum(r["belopp"] for r in rows)
    display_data.append(["", "", total_label, "", "", "", kr(total)])

    col_widths = [22 * mm, 18 * mm, 70 * mm, 12 * mm, 16 * mm, 20 * mm, 22 * mm]
    table = Table(display_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ALIGN", (4, 0), (-1, 0), "RIGHT"),
        ("ALIGN", (3, 0), (3, 0), "CENTER"),
        ("FONTNAME", (0, 1), (-1, -2), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -2), 9),
        ("ALIGN", (4, 1), (-1, -2), "RIGHT"),
        ("ALIGN", (3, 1), (3, -2), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, -1), (-1, -1), 9),
        ("ALIGN", (2, -1), (-1, -1), "RIGHT"),
        ("LINEABOVE", (0, -1), (-1, -1), 0.5, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table, total


def build_utlagg_table(rows):
    """Tabell för utlägg."""
    header = ["Datum", "Beskrivning", "Belopp"]
    display_data = [header]
    for r in rows:
        display_data.append([r["datum"], r["beskrivning"], kr(r["belopp"])])

    total = sum(r["belopp"] for r in rows)
    display_data.append(["", "Summa utlägg", kr(total)])

    col_widths = [30 * mm, 100 * mm, 30 * mm]
    table = Table(display_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ALIGN", (2, 0), (2, 0), "RIGHT"),
        ("FONTNAME", (0, 1), (-1, -2), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -2), 9),
        ("ALIGN", (2, 1), (2, -2), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, -1), (-1, -1), 9),
        ("ALIGN", (1, -1), (-1, -1), "RIGHT"),
        ("LINEABOVE", (0, -1), (-1, -1), 0.5, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table, total


def build_sammantr_table(sammantr_kod, sammantr_namn, poster, utlagg, cell_style):
    """Tabell för specifikt sammanträde med både arbete och utlägg (perspektiv B)."""
    arbete = [p for p in poster if p["sammantr"] == sammantr_kod]
    utl = [u for u in utlagg if u["sammantr"] == sammantr_kod]

    header = ["Datum", "Beskrivning", "Typ", "Timmar", "À-pris/belopp", "Belopp"]
    display_data = [header]

    for r in arbete:
        display_data.append([
            r["datum"],
            Paragraph(r["beskrivning"], cell_style),
            "Arbete" if r["typ"] == "arbete" else "Tidsspillan",
            fmt_timmar(r["timmar"]),
            kr(r["à_pris"]),
            kr(r["belopp"]),
        ])

    for u in utl:
        display_data.append([
            u["datum"],
            Paragraph(u["beskrivning"], cell_style),
            u["typ"].capitalize(),
            "",
            "",
            kr(u["belopp"]),
        ])

    total = sum(r["belopp"] for r in arbete) + sum(u["belopp"] for u in utl)
    display_data.append(["", f"Delsumma {sammantr_namn}", "", "", "", kr(total)])

    col_widths = [22 * mm, 70 * mm, 22 * mm, 16 * mm, 24 * mm, 24 * mm]
    table = Table(display_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ALIGN", (3, 0), (-1, 0), "RIGHT"),
        ("FONTNAME", (0, 1), (-1, -2), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -2), 9),
        ("ALIGN", (3, 1), (-1, -2), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, -1), (-1, -1), 9),
        ("ALIGN", (1, -1), (-1, -1), "RIGHT"),
        ("LINEABOVE", (0, -1), (-1, -1), 0.5, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table, total


def build_summary_table(rows):
    """Generisk sammanställningstabell: kategori -> belopp (perspektiv C, D, E)."""
    header = ["Kategori", "Belopp", "Andel"]
    display_data = [header]
    total = sum(r[1] for r in rows)
    for r in rows:
        andel = f"{(r[1] / total * 100):.1f} %" if total > 0 else "0 %"
        display_data.append([r[0], kr(r[1]), andel])
    display_data.append(["Totalt", kr(total), "100 %"])

    col_widths = [100 * mm, 35 * mm, 25 * mm]
    table = Table(display_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ALIGN", (1, 0), (-1, 0), "RIGHT"),
        ("FONTNAME", (0, 1), (-1, -2), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -2), 9),
        ("ALIGN", (1, 1), (-1, -2), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, -1), (-1, -1), 9),
        ("ALIGN", (1, -1), (-1, -1), "RIGHT"),
        ("LINEABOVE", (0, -1), (-1, -1), 0.5, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table, total


def build_nyckeltal_table(rader):
    """Specialtabell för nyckeltal (perspektiv F)."""
    header = ["Nyckeltal", "Värde"]
    display_data = [header] + [list(r) for r in rader]

    col_widths = [100 * mm, 60 * mm]
    table = Table(display_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (1, 1), (1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


# ============================================================================
# Data — fyll i för det specifika målet
# ============================================================================

# Standard-à-priser (justera vid behov)
PRIS_ARBETE = 1000
PRIS_TIDSSPILLAN = 800

# Filnamn för output
OUTPUT_PATH = "/mnt/user-data/outputs/Kostnadsrakning.pdf"

# Mål-info
TITEL = "Kostnadsräkning"
UNDERTITEL = "Mål [målnummer] vid [domstol] — [parter]"
ORT_DATUM = "[Ort], den [datum]"
NAMN = "[Namn]"

# Periodrubriker
PERIOD1_RUBRIK = "Period 1 — [beskrivning av fas och datumintervall]"
PERIOD2_RUBRIK = "Period 2 — [beskrivning av fas och datumintervall]"
PERIOD3_RUBRIK = "Period 3 — [beskrivning av fas och datumintervall]"

# Centralt dataregister — varje post har full metadata
# Fält per post: datum, aktbil, beskrivning, del, timmar, à_pris, period,
#                sammantr (None/MUF1/MUF2/HF), typ (arbete/tidsspillan)
poster = [
    # Exempel:
    # {
    #     "datum": "2025-03-28", "aktbil": "20",
    #     "beskrivning": "Yttrande på svaromål",
    #     "del": "R", "timmar": 5, "à_pris": PRIS_ARBETE,
    #     "period": 1, "sammantr": None, "typ": "arbete",
    # },
]

# Avrunda alla timmar till närmaste kvart, beräkna belopp
for p in poster:
    p["timmar"] = round_quarter(p["timmar"])
    p["belopp"] = round(p["timmar"] * p["à_pris"])

# Utlägg — fält per post: datum, beskrivning, belopp, sammantr, typ
# typ: "utlägg", "körersättning", "parkering"
utlagg = [
    # Exempel:
    # {"datum": "2025-02-05", "beskrivning": "Stämningsavgift", "belopp": 900,
    #  "sammantr": None, "typ": "utlägg"},
]


# ============================================================================
# Bygg PDF
# ============================================================================

styles = getSampleStyleSheet()
style_title = ParagraphStyle("title", parent=styles["Title"], fontSize=14, leading=18, alignment=TA_LEFT, spaceAfter=6)
style_subtitle = ParagraphStyle("subtitle", parent=styles["Normal"], fontSize=10, leading=14, spaceAfter=12, textColor=colors.HexColor("#555555"))
style_h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontSize=13, leading=16, spaceBefore=18, spaceAfter=8)
style_h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=11, leading=14, spaceBefore=12, spaceAfter=6)
style_normal = ParagraphStyle("normal", parent=styles["Normal"], fontSize=9, leading=12, spaceAfter=4)
style_total = ParagraphStyle("total", parent=styles["Normal"], fontSize=11, leading=14, spaceBefore=12, spaceAfter=6, fontName="Helvetica-Bold")
style_cell = ParagraphStyle("cell", parent=styles["Normal"], fontSize=9, leading=11, spaceBefore=0, spaceAfter=0)
style_grand = ParagraphStyle("grand", parent=styles["Normal"], fontSize=12, leading=16, spaceBefore=12, fontName="Helvetica-Bold")

doc = SimpleDocTemplate(
    OUTPUT_PATH,
    pagesize=A4,
    leftMargin=20 * mm,
    rightMargin=20 * mm,
    topMargin=20 * mm,
    bottomMargin=20 * mm,
)

story = []

# Header
story.append(Paragraph(TITEL, style_title))
story.append(Paragraph(UNDERTITEL, style_subtitle))
story.append(Paragraph(
    "Kostnaderna redovisas i sex perspektiv: (A) per processfas, (B) per sammanträde, "
    "(C) per måldel, (D) per kostnadstyp, (E) per månad och (F) nyckeltal. Perspektiv A "
    "är huvudredovisningen och innehåller samtliga poster. Perspektiv B–F är "
    "sammanställningar av samma underlag ur olika synvinklar. All tid har avrundats "
    "uppåt till närmaste påbörjade kvart.",
    style_normal,
))
story.append(Paragraph(
    "<b>Förkortning i kolumnen 'Del':</b> R = räntefrågan, S = skadeståndsfrågan, "
    "B = båda/processuellt. À-pris för eget arbete: 1 000 kr/timme. "
    "À-pris för tidsspillan: 800 kr/timme.",
    style_normal,
))

# ===== PERSPEKTIV A — Per processfas =====
story.append(Paragraph("Perspektiv A — Per processfas", style_h1))

sub1 = sub2 = sub3 = 0

p1 = [p for p in poster if p["period"] == 1]
if p1:
    story.append(Paragraph(PERIOD1_RUBRIK, style_h2))
    t1, sub1 = build_period_table(p1, "Delsumma period 1", style_cell)
    story.append(t1)

p2 = [p for p in poster if p["period"] == 2]
if p2:
    story.append(Paragraph(PERIOD2_RUBRIK, style_h2))
    t2, sub2 = build_period_table(p2, "Delsumma period 2", style_cell)
    story.append(t2)

p3 = [p for p in poster if p["period"] == 3]
if p3:
    story.append(PageBreak())
    story.append(Paragraph(PERIOD3_RUBRIK, style_h2))
    t3, sub3 = build_period_table(p3, "Delsumma period 3", style_cell)
    story.append(t3)

arbete_tidsspillan_total = sub1 + sub2 + sub3
story.append(Paragraph(f"Summa arbete och tidsspillan: {kr(arbete_tidsspillan_total)}", style_total))

# Utlägg
sub_u = 0
if utlagg:
    story.append(Paragraph("Utlägg", style_h2))
    tu, sub_u = build_utlagg_table(utlagg)
    story.append(tu)

grand_total = arbete_tidsspillan_total + sub_u
story.append(Spacer(1, 12))
story.append(Paragraph(f"<b>TOTALSUMMA: {kr(grand_total)}</b>", style_grand))

# ===== PERSPEKTIV B — Per sammanträde =====
sammantraden = sorted({p["sammantr"] for p in poster if p["sammantr"]})
if sammantraden:
    story.append(PageBreak())
    story.append(Paragraph("Perspektiv B — Per sammanträde", style_h1))
    story.append(Paragraph(
        "Denna sammanställning visar alla kostnader hänförliga till varje sammanträde i målet, "
        "inklusive förberedelse, restid, sammanträdestid och utlägg. Notera att samma poster "
        "även redovisas i perspektiv A — detta är samma underlag presenterat ur ett annat "
        "perspektiv.",
        style_normal,
    ))

    for kod in sammantraden:
        # Anpassa namnet efter behov
        namn_map = {
            "MUF1": "Sammanträde 1 — Första muntliga förberedelsen",
            "MUF2": "Sammanträde 2 — Andra muntliga förberedelsen",
            "HF": "Sammanträde 3 — Huvudförhandling",
        }
        story.append(Paragraph(namn_map.get(kod, f"Sammanträde {kod}"), style_h2))
        tab, _ = build_sammantr_table(kod, namn_map.get(kod, kod).split(" — ")[0].lower(), poster, utlagg, style_cell)
        story.append(tab)

# ===== PERSPEKTIV C — Per måldel =====
story.append(PageBreak())
story.append(Paragraph("Perspektiv C — Per måldel", style_h1))
story.append(Paragraph(
    "Denna sammanställning visar kostnadernas fördelning mellan målets olika delar. "
    "Perspektivet är särskilt relevant för bedömning enligt 18 kap. 4 § rättegångsbalken.",
    style_normal,
))

del_summary = {}
for p in poster:
    del_summary[p["del"]] = del_summary.get(p["del"], 0) + p["belopp"]
utlagg_total = sum(u["belopp"] for u in utlagg)

# Anpassa rader efter målets kategorier
del_rows = [
    ("Räntefrågan (R)", del_summary.get("R", 0)),
    ("Skadeståndsfrågan (S)", del_summary.get("S", 0)),
    ("Båda/processuellt (B) inkl. utlägg", del_summary.get("B", 0) + utlagg_total),
]
tc, _ = build_summary_table(del_rows)
story.append(tc)

story.append(Spacer(1, 8))
story.append(Paragraph(
    "Anmärkning: Posterna i kategorin 'Båda/processuellt' (B) avser arbete som inte kan "
    "isoleras till en enskild måldel, såsom hantering av processuella frågor, deltagande "
    "i muntliga förberedelser, restid samt huvudförhandlingen där argumentationen rörde "
    "båda frågorna samtidigt.",
    style_normal,
))

# ===== PERSPEKTIV D — Per kostnadstyp =====
story.append(Paragraph("Perspektiv D — Per kostnadstyp", style_h1))
story.append(Paragraph(
    "Denna sammanställning visar totalsummans uppdelning på de olika kostnadstyper som ingår.",
    style_normal,
))

typ_arbete = sum(p["belopp"] for p in poster if p["typ"] == "arbete")
typ_tidsspillan = sum(p["belopp"] for p in poster if p["typ"] == "tidsspillan")
typ_korersattning = sum(u["belopp"] for u in utlagg if u["typ"] == "körersättning")
typ_parkering = sum(u["belopp"] for u in utlagg if u["typ"] == "parkering")
typ_ovriga_utlagg = sum(u["belopp"] for u in utlagg if u["typ"] == "utlägg")

typ_rows = [
    ("Eget arbete (1 000 kr/h)", typ_arbete),
    ("Tidsspillan (800 kr/h)", typ_tidsspillan),
    ("Körersättning", typ_korersattning),
    ("Parkering", typ_parkering),
    ("Övriga utlägg", typ_ovriga_utlagg),
]
td, _ = build_summary_table(typ_rows)
story.append(td)

# ===== PERSPEKTIV E — Per månad (med tomma månader) =====
if poster:
    story.append(Paragraph("Perspektiv E — Per månad", style_h1))
    story.append(Paragraph(
        "Denna sammanställning visar kostnadernas kronologiska fördelning per kalendermånad. "
        "Tomma månader visas för att illustrera att kostnaderna inte uppstått i en koncentrerad "
        "burst utan följer processens egen utveckling.",
        style_normal,
    ))

    manad_summary = {}
    for p in poster:
        m = get_manad(p["datum"])
        manad_summary[m] = manad_summary.get(m, 0) + p["belopp"]
    for u in utlagg:
        m = get_manad(u["datum"])
        manad_summary[m] = manad_summary.get(m, 0) + u["belopp"]

    manad_namn = {
        "01": "januari", "02": "februari", "03": "mars", "04": "april",
        "05": "maj", "06": "juni", "07": "juli", "08": "augusti",
        "09": "september", "10": "oktober", "11": "november", "12": "december",
    }

    sorterade_aktiva = sorted(manad_summary.keys())
    alla_manader = alla_manader_i_intervallet(sorterade_aktiva[0], sorterade_aktiva[-1])

    manad_rows = []
    for m in alla_manader:
        ar, mn = m.split("-")
        namn = f"{manad_namn[mn].capitalize()} {ar}"
        belopp = manad_summary.get(m, 0)
        manad_rows.append((namn, belopp))

    te, _ = build_summary_table(manad_rows)
    story.append(te)

# ===== PERSPEKTIV F — Nyckeltal =====
if poster:
    story.append(Paragraph("Perspektiv F — Nyckeltal", style_h1))
    story.append(Paragraph(
        "Denna sammanställning visar deskriptiv statistik över de timbaserade arbets- och "
        "tidsspillansposterna. Utlägg ingår inte i statistiken eftersom de inte är timbaserade.",
        style_normal,
    ))

    arbete_poster = [p for p in poster if p["typ"] == "arbete"]
    tidsspillan_poster = [p for p in poster if p["typ"] == "tidsspillan"]
    alla_timposter = arbete_poster + tidsspillan_poster
    arbete_timmar = [p["timmar"] for p in arbete_poster]
    tidsspillan_timmar = [p["timmar"] for p in tidsspillan_poster]
    alla_timmar = [p["timmar"] for p in alla_timposter]

    antal_aktiva_manader = len({get_manad(p["datum"]) for p in poster})
    antal_totala_manader = len(alla_manader)

    datum_lista = sorted({p["datum"] for p in poster})
    forsta_datum = datum_lista[0]
    sista_datum = datum_lista[-1]

    nyckeltal_rader = [
        ("Totalt antal nedlagda timmar", f"{sum(alla_timmar):.2f}".rstrip("0").rstrip(".") + " h"),
        ("Varav eget arbete", f"{sum(arbete_timmar):.2f}".rstrip("0").rstrip(".") + " h"),
        ("Varav tidsspillan", f"{sum(tidsspillan_timmar):.2f}".rstrip("0").rstrip(".") + " h"),
        ("Antal separata insatser", str(len(alla_timposter))),
        ("Medeltid per insats", f"{statistics.mean(alla_timmar):.2f} h"),
        ("Median per insats", f"{statistics.median(alla_timmar):.2f} h"),
        ("Längsta enskilda insats", f"{max(alla_timmar):.2f}".rstrip("0").rstrip(".") + " h"),
        ("Kortaste enskilda insats", f"{min(alla_timmar):.2f}".rstrip("0").rstrip(".") + " h"),
        ("Totalt antal månader (första–sista aktiva)", f"{antal_totala_manader} st"),
        ("Antal aktiva månader (med kostnad)", f"{antal_aktiva_manader} st"),
        ("Antal månader utan aktivitet", f"{antal_totala_manader - antal_aktiva_manader} st"),
        ("Genomsnittlig kostnad per aktiv månad", kr(round(sum(p["belopp"] for p in poster) / antal_aktiva_manader))),
        ("Processens längd (första–sista datum)", f"{forsta_datum} – {sista_datum}"),
    ]

    tf = build_nyckeltal_table(nyckeltal_rader)
    story.append(tf)

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Anmärkning: Medeltid och median per insats indikerar att arbetet huvudsakligen utförts "
        "i kortare arbetspass och inte i koncentrerade arbetstoppar. Det stora antalet separata "
        "insatser återspeglar målets processuella komplexitet.",
        style_normal,
    ))

# Footer
story.append(Spacer(1, 24))
story.append(Paragraph(ORT_DATUM, style_normal))
story.append(Spacer(1, 18))
story.append(Paragraph(NAMN, style_normal))

doc.build(story)
print(f"PDF genererad: {OUTPUT_PATH}")
