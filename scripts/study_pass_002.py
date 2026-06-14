"""Study pass 002: add structured reading notes and writing seeds.

This pass records actual study of selected corpus sections:
- Howlett, Introduction + Life and Works
- Copenhaver, Magic and the Dignity of Man, Introduction
- Copenhaver, Pico on Trial, Introduction
- Walden, Savonarola/Pico article
- Farmer, Roman Debate opening
- Wirszubski/Kristeller, Introduction + Hebrew/Kabbalah opening
- Akopyan, astrology/Disputationes structure
"""

from __future__ import annotations

import importlib.util
import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "pico.db"


DOCS = {
    "howlett": "Critical_Political_Theory_and_Radical_Practice_Sophia_Howlett_-_Re-evaluating_Pico__Aristotelian_pdf_3c6c4fa3",
    "copenhaver_magic": "Brian_P_Copenhaver_Magic_and_the_Dignity_of_Man__Pico_della_Mirandola_and_His_Oration_in_Modern__pdf_f7f272e1",
    "copenhaver_trial": "Brian_P_Copenhaver_Pico_della_Mirandola_on_Trial__Heresy_Freedom_and_Philosophy_libgen_li_pdf_753eb1fa",
    "walden": "An_Anatomy_of_Influence_Savonarola_and_P_pdf_2910b592",
    "farmer": "Medieval_Renaissance_Texts_Studies_167_Stephen_A_Farmer_Giovanni_Pico_Della_Mirandola_Syncretism_pdf_c99b971b",
    "wirszubski": "Chaim_Wirszubski_Paul_Oskar_Kristeller_Pico_della_Mirandola_s_Encounter_with_Jewish_Mysticism_Ha_pdf_cd8c112f",
    "akopyan": "Brill_s_Studies_in_Intellectual_History_325_Ovanes_Akopyan_Debating_the_Stars_in_the_Italian_Ren_pdf_c6917f0c",
}


NOTES = {
    "artifacts/source_packets/howlett_intro_life.md": """# Source Packet: Howlett, Introduction and Life/Works

- Artifact ID: `sp_howlett_intro_life`
- Document ID: `Critical_Political_Theory_and_Radical_Practice_Sophia_Howlett_-_Re-evaluating_Pico__Aristotelian_pdf_3c6c4fa3`
- Page range studied: extracted pages 11-40
- Evidence status: SOURCE_ANCHORED_DRAFT

## Local Summary

Howlett opens by treating Pico as a contested site rather than a stable Renaissance emblem. The familiar Pico is overdetermined: philosopher-prince, miraculous memory, saintly penitent, proto-modern individual, Ficino's Platonic satellite, and last universal knower. Howlett argues that the glittering myth is partly Pico's own self-fashioning and partly a later contest to claim him.

The major re-evaluation is fourfold. First, Pico's fragmentary works can still be read as substantially coherent. Second, his universe rests on three pillars: Aristotelianism, Platonism, and Jewish Kabbalism. Third, concord succeeds only where shared structures exist and fails/reveals rupture where traditions genuinely diverge. Fourth, unlike Ficino's reforming renovatio, Pico is exceptionalist: the journey is solitary, ascetic, mystical, and directed toward henosis/cleaving rather than return to communal reform.

The life chapter emphasizes that Pico's noble status is not decorative biography. It made the Roman debate materially possible, gave him access to courts and scholars, and let him hire translators and teachers. Howlett also sharpens the itinerary: Ferrara, Padua, Pavia, Florence, Paris, Arezzo, Perugia/La Fratta, Rome, France/Vincennes, and Florence again.

## Extracted Claims

| Claim | Type | Theme | Evidence |
|---|---|---|---|
| Pico's fame is disproportionate to his surviving output and is sustained by mythic characterizations. | historiographical | reception | pp. 11-12 |
| Howlett's Pico rests on Aristotelianism, Platonism, and Jewish Kabbalism as three pillars. | interpretive | ontology | p. 13 |
| The Oration's modern reading as dignity/proto-modernity misses that dignity is not the main topic of the speech. | historiographical | Oration | p. 14 |
| Pico's noble status made his intellectual career materially possible and shaped reception of his audacity. | historical | biography | p. 20 |
| Pavia is important for logic and mathematics; Paris for via moderna scholasticism. | geographical | education | pp. 22-24 |
| The Arezzo abduction and Perugia/La Fratta retreat belong directly to the 1486 debate preparation. | historical | biography | pp. 26-27 |
| Vincennes should be treated as a royal-protective detention site, not only a prison. | geographical | trial | p. 30 |

## Candidate Promotions

- Update biography page with the “contested site” opening.
- Add concept dossier: `Pico exceptionalism`.
- Add historiography node: `Against the Oration-only Pico`.
- Add map nodes: La Fratta, Perugia, Pavia, Vincennes.
""",
    "artifacts/source_packets/copenhaver_magic_intro.md": """# Source Packet: Copenhaver, Magic and the Dignity of Man, Introduction

- Artifact ID: `sp_copenhaver_magic_intro`
- Document ID: `Brian_P_Copenhaver_Magic_and_the_Dignity_of_Man__Pico_della_Mirandola_and_His_Oration_in_Modern__pdf_f7f272e1`
- Page range studied: extracted pages 20-25
- Evidence status: SOURCE_ANCHORED_DRAFT

## Local Summary

Copenhaver frames the book as a correction to the usual stories about Pico and the Oration. The central claim is intentionally disruptive: Pico never wrote an Oration about human dignity. Instead, the undelivered speech promoted ascetic mysticism and Kabbalah, and later readers made the opening pages into a humanist emblem. Copenhaver treats misreadings of Pico as misreadings of Renaissance humanism itself.

The book is not a life-and-works biography or a simple influence history. It is a cultural and philosophical history of Pico's unstable celebrity over five centuries, organized by topic and geography. The study also asks why the opening of the speech has been detached from the rest of the text, especially the sections on magic and Kabbalah.

## Extracted Claims

| Claim | Type | Theme | Evidence |
|---|---|---|---|
| The ordinary story of Pico and his Oration is wrong in matters larger than detail. | historiographical | reception | p. 21 |
| The speech was drafted but never delivered. | historical | Oration | p. 21 |
| The Oration promoted ascetic mysticism, not modern dignity as usually understood. | interpretive | Oration | p. 21 |
| The book studies Pico's unstable celebrity over five centuries rather than offering a standard intellectual biography. | bibliographic | scholarship | pp. 22-23 |
| The key interpretive problem is connecting the famous opening pages with the rest of the speech. | interpretive | Oration | p. 23 |

## Candidate Promotions

- Historiography node: `Modern dignity myth`.
- Oration dossier section: `Not a speech about dignity`.
- Website card for Copenhaver 2019.
""",
    "artifacts/source_packets/copenhaver_trial_intro.md": """# Source Packet: Copenhaver, Pico on Trial, Introduction

- Artifact ID: `sp_copenhaver_trial_intro`
- Document ID: `Brian_P_Copenhaver_Pico_della_Mirandola_on_Trial__Heresy_Freedom_and_Philosophy_libgen_li_pdf_753eb1fa`
- Page range studied: extracted pages 14-19
- Evidence status: SOURCE_ANCHORED_DRAFT

## Local Summary

Copenhaver's second Pico book shifts the portal's center of gravity from the Oration to the Apology and heresy case. It argues that Pico's work before and after the Oration was not progressive or humanist. The Apology reveals a public, academic, combative Pico arguing over Christian doctrine in scholastic terms. The trial material concerns incarnation, Christ's descent to Hell, the Eucharistic body, and the freedom or constraint of belief.

The important methodological claim is that Pico must be brought back into philosophical conversation through scholastic semantics, logic, and theology. Copenhaver reads Pico as a philosopher in the same sense as Aquinas, Scotus, and Ockham, and uses analytic tools to make the arguments visible.

## Extracted Claims

| Claim | Type | Theme | Evidence |
|---|---|---|---|
| Pico's Apology reveals more about him than the famous undelivered speech. | interpretive | Apology | p. 14 |
| The Oration is esoteric while the Apology is public, academic, and belligerent. | interpretive | genre | p. 14 |
| The Conclusions and Apology are products of the late Middle Ages rather than modern humanism. | historiographical | scholasticism | p. 17 |
| Pico should be read as a philosopher in continuity with Aquinas, Scotus, and Ockham. | interpretive | philosophy | p. 17 |
| The heresy case turns on technical terms where theological mistakes could be fatal. | interpretive | heresy | pp. 15-16 |

## Candidate Promotions

- Work dossier: `Apologia`.
- Historiography node: `Pico no humanist`.
- Concept dossier: `Scholastic Pico`.
""",
    "artifacts/source_packets/farmer_roman_debate.md": """# Source Packet: Farmer, Syncretism in the West, Chapter 1 Opening

- Artifact ID: `sp_farmer_roman_debate`
- Document ID: `Medieval_Renaissance_Texts_Studies_167_Stephen_A_Farmer_Giovanni_Pico_Della_Mirandola_Syncretism_pdf_c99b971b`
- Page range studied: extracted pages 19-25
- Evidence status: SOURCE_ANCHORED_DRAFT

## Local Summary

Farmer places the 900 Theses at the center of Pico's Roman project and insists that the Oration was only the preface. Pico's debate was enormous, theatrical, and designed as a puzzle whose hidden concatenation had to be deciphered. The project was printed in Rome on 7 December 1486, posted publicly, sent to universities, and planned for debate in the apostolic senate before cardinals and possibly the pope. The Epiphany timing mattered because it symbolized the submission of the pagan nations to Christ.

Farmer's opening is indispensable for the portal because it restores the oral, public, disputational, and puzzle-like nature of the 900 Conclusions.

## Extracted Claims

| Claim | Type | Theme | Evidence |
|---|---|---|---|
| The Oration is a preface to the 900 Theses, not the main event. | textual | Oration | p. 20 |
| Pico designed the theses as an elaborate puzzle with hidden connections. | interpretive | 900 Conclusions | pp. 19-20 |
| The theses were printed in Rome on 7 December 1486. | historical | publication | p. 21 |
| Pico sent or ordered copies to be sent to Italian universities and offered to pay travel expenses for opponents. | historical | disputation | p. 21 |
| The planned debate's Epiphany date symbolized the submission of pagan nations to Christ. | interpretive | concord | p. 22 |

## Candidate Promotions

- Work dossier: `900 Conclusions`.
- Timeline event: 7 December 1486 printing.
- Concept dossier: `occulta concatenatio`.
""",
    "artifacts/source_packets/wirszubski_kabbalah_opening.md": """# Source Packet: Wirszubski/Kristeller, Encounter with Jewish Mysticism Opening

- Artifact ID: `sp_wirszubski_kabbalah_opening`
- Document ID: `Chaim_Wirszubski_Paul_Oskar_Kristeller_Pico_della_Mirandola_s_Encounter_with_Jewish_Mysticism_Ha_pdf_cd8c112f`
- Page range studied: extracted pages 9-18
- Evidence status: SOURCE_ANCHORED_DRAFT

## Local Summary

Kristeller's introduction frames Wirszubski as the scholar who clarifies the content, sources, and individual shape of Pico's Kabbalism. The study confirms Pico as the main founder of Christian Kabbalism in the Renaissance and shows how Pico gave Kabbalah a Christian interpretation that later shaped Reuchlin, Egidio da Viterbo, and others.

The opening chapter overturns a common assumption: Pico became interested in Kabbalah before he knew Hebrew. He began studying Hebrew and Chaldean for the sake of Kabbalah, making him the first notable Christian Hebraist known to have done so. By autumn 1486, Pico could write some Hebrew prose but almost certainly depended on Latin translations by Flavius Mithridates for substantial Kabbalistic reading.

## Extracted Claims

| Claim | Type | Theme | Evidence |
|---|---|---|---|
| Wirszubski clarifies the content and sources of Pico's Kabbalism. | historiographical | Kabbalah | pp. 9-11 |
| Pico, not his Hebrew sources or Christian predecessors, laid ground for Christian interpretation of Kabbalah. | interpretive | Christian Kabbalah | p. 11 |
| Pico became interested in Kabbalah before he knew Hebrew. | historical | Hebrew | p. 15 |
| Pico studied Hebrew and Chaldean for the sake of Kabbalah. | historical | Kabbalah | p. 15 |
| The summer/autumn of 1486 is crucial for Mithridates' translations and Pico's Kabbalistic theses. | historical | translations | pp. 16-18 |

## Candidate Promotions

- Scholar profile: Chaim Wirszubski.
- Scholar profile: Paul Oskar Kristeller.
- Concept dossier: `Christian Kabbalah`.
- Map/timeline: Perugia/La Fratta summer-autumn 1486 as Kabbalah translation setting.
""",
    "artifacts/source_packets/akopyan_astrology_structure.md": """# Source Packet: Akopyan, Debating the Stars Structure

- Artifact ID: `sp_akopyan_astrology_structure`
- Document ID: `Brill_s_Studies_in_Intellectual_History_325_Ovanes_Akopyan_Debating_the_Stars_in_the_Italian_Ren_pdf_c6917f0c`
- Page range studied: table of contents and opening references
- Evidence status: SOURCE_ANCHORED_DRAFT

## Local Summary

Akopyan provides the portal's main scaffold for Pico and astrology. The book is structured in three parts: before the Disputationes, the Disputationes itself, and the pro/contra afterlife. Its chapters move from scientia naturalis, Kabbalah, and celestial spheres (1486-1493), through Pico's sources and critique of prisca theologia and astrological tradition, to later appropriations by Savonarola, Gianfrancesco Pico, Maximus the Greek, Bellanti, Pontano, and Francesco Zorzi.

For the portal, this means astrology cannot be treated only as a late rejection. It has a developmental arc from Pico's earlier natural philosophy and Kabbalistic-celestial interests into a late anti-divinatory polemic.

## Extracted Claims

| Claim | Type | Theme | Evidence |
|---|---|---|---|
| Akopyan divides the topic into before the Disputationes, the Disputationes, and its afterlife. | bibliographic | astrology | contents |
| Pico's astrology must be read developmentally from 1486 to 1493. | interpretive | astrology | chapter 1 title |
| The Disputationes involves sources, prisca theologia, astrological tradition, and natural philosophy. | bibliographic | Disputationes | contents |
| Savonarola's Contro gli astrologi is an ideological appropriation of Pico's Disputationes. | bibliographic | reception | chapter 7 title |

## Candidate Promotions

- Work dossier: `Disputationes`.
- Concept dossier: `Pico and astrology`.
- Timeline: 1486-1493 astrology arc.
""",
}


WEBSITE_NOTES = {
    "artifacts/website_notes/biographies/pico_biography_pass002.md": """# Giovanni Pico Biography Draft Pass 002

Status: DRAFT  
Promotes to: Pico biography page

## Thesis

Pico's life should be narrated as a sequence of intellectual geographies rather than as a simple rise-and-fall of a prodigy. Mirandola gives him noble status and ecclesiastical expectation. Ferrara, Padua, Pavia, Paris, and Bologna give him the university and scholastic apparatus that later humanist readings often obscure. Florence gives him Ficino, Poliziano, Lorenzo, Hebrew/Kabbalah, and finally Savonarola. Rome turns his concordist ambition into a juridical-theological crisis. France/Vincennes transforms the crisis into imprisonment and diplomatic rescue. San Marco fixes the late-life image of penitence, Savonarolan proximity, and posthumous memory.

## Education and Mobility

Howlett's account makes family and mobility central. Pico's elite position allowed him to pursue education wherever curiosity drew him, hire translators and teachers, and attempt public enterprises that ordinary scholars could not risk. His educational route includes Ferrara, Padua, Pavia, Florence, and Paris. Pavia matters for logic and mathematics; Paris matters for the via moderna; Padua matters for Aristotelian philosophy. This makes the mature Pico more scholastic and Aristotelian than a Ficino-centered story suggests.

## The Year 1486

1486 is the hinge year. Pico is in Florence and Arezzo, becomes disgraced by the Margherita episode, moves between Perugia and La Fratta, works with an entourage including Elijah del Medigo and Flavius Mithridates, develops the debate project, and prepares the Conclusions for Rome. Wirszubski makes this period crucial for Kabbalah: Pico's Hebrew was recent and limited, while Mithridates' Latin translations made massive Kabbalistic reading possible.

## Crisis and Return

Farmer restores the Roman debate as a giant public puzzle, not merely a backdrop to the Oration. The 900 Theses were printed, posted, and circulated, with Pico planning a debate before cardinals. The project collapsed under papal scrutiny. Howlett's life chapter and other corpus notes place Pico's later detention at the royal palace/castle of Vincennes, where French protection may have kept him away from the papal nuncios rather than simply abandoning him to prison.

## Late Florence

The late Florentine Pico should be written without caricature. Walden argues against a crude opposition between Savonarola the medieval preacher and Pico the secular Neoplatonic prodigy. Their affinity is theological, exegetical, ascetic, and rhetorical. Pico's anti-astrology work, late religious seriousness, and burial at San Marco belong in the same late-life field.
""",
    "artifacts/website_notes/historiography/against_oration_only_pico.md": """# Historiography Node: Against the Oration-Only Pico

Status: DRAFT

## Problem

Modern readers often begin and end Pico with the so-called Oration on the Dignity of Man. The corpus strongly resists that habit.

## Positions

| Scholar | Position |
|---|---|
| Copenhaver | Pico never wrote an Oration about human dignity; the famous speech was undelivered and promoted ascetic mysticism, Kabbalah, and concord rather than modern dignity. |
| Farmer | The Oration was only the preface to the 900 Conclusions, whose hidden structure and intended oral debate must be deciphered. |
| Howlett | The Oration-centered proto-modern Pico is a modernist desire; Pico's works should be read through Aristotelianism, Platonism, and Kabbalism. |
| Walden | The Oration has been secularized while Pico's later theological works have been neglected. |

## Stakes

This node should govern the public website's introduction. The portal should not reproduce the textbook Pico as a free-floating emblem of human dignity. The Oration is important, but it must be situated in the debate project, the 900 Conclusions, magic/Kabbalah, scholastic theology, and reception history.
""",
    "artifacts/website_notes/concepts/christian_kabbalah_seed.md": """# Concept Dossier Seed: Christian Kabbalah in Pico

Status: DRAFT

## Working Definition

In Pico, Kabbalah is not merely an exotic ornament added to Platonism. According to the Wirszubski/Kristeller line, Pico's encounter with Kabbalah is a watershed in Christian Hebraism and Christian Kabbalah. Pico studied Hebrew and Chaldean for the sake of Kabbalah, but his actual access in 1486 depended heavily on Latin translations produced by Flavius Mithridates.

## Core Claims to Track

- Pico's Kabbalistic interest preceded serious Hebrew competence.
- Mithridates' translations are a crucial infrastructure of Pico's Kabbalah.
- Pico Christianizes Kabbalistic material and links it with Orphic, Chaldean, Proclean, Cusan, Lullian, and ancient-theology materials.
- Kabbalah alters the meaning of Pico's concordism and cannot be treated as a side topic.

## Website Sections

1. Hebrew before and after Kabbalah.
2. Mithridates and translation.
3. The 900 Conclusions.
4. Heptaplus and the three worlds.
5. Magic, mysticism, and Christian confirmation.
6. Later Christian Kabbalah: Reuchlin, Egidio, and after.
""",
    "artifacts/website_notes/concepts/pico_astrology_seed.md": """# Concept Dossier Seed: Pico and Astrology

Status: DRAFT

## Working Definition

Pico's astrology must be treated as a developmental problem. Akopyan's structure makes clear that the Disputationes does not appear from nowhere. The field includes earlier scientia naturalis, Kabbalah, celestial spheres, Pico's sources, his changing attitude toward prisca theologia, his critique of the astrological tradition, and the reception of the Disputationes by Savonarola, Gianfrancesco Pico, Bellanti, Pontano, Zorzi, and others.

## Website Sections

1. Before the Disputationes, 1486-1493.
2. Natural philosophy and celestial causation.
3. Kabbalah and the heavens.
4. Against divinatory astrology.
5. Savonarola and ideological appropriation.
6. Anti-Pico responses and later debate.

## Map/Timeline Use

Late Florence and San Marco matter here because Walden and Akopyan both link the anti-astrology work to Savonarolan proximity, even though the precise relation between influence, collaboration, and appropriation must remain open.
""",
}


CARDS = [
    ("hist-oration-only", "historiography", "Against the Oration-Only Pico", "Copenhaver, Farmer, Howlett, Walden", "The portal's governing historiographical correction: Pico cannot be reduced to a proto-modern Oration on dignity. The Oration must be read as preface, reception object, mystical text, and part of the 900 Conclusions crisis.", "DRAFT", "sp_copenhaver_magic_intro"),
    ("concept-kabbalah", "concept", "Christian Kabbalah in Pico", "Mithridates, Hebrew, 900 Conclusions", "Pico's Kabbalah depends on translation, Hebrew aspiration, Christian interpretation, and the ambitious integration of Jewish mystical materials into concordist philosophy.", "DRAFT", "sp_wirszubski_kabbalah_opening"),
    ("concept-astrology", "concept", "Pico and Astrology", "From scientia naturalis to Disputationes", "Pico's anti-astrology polemic must be studied as a development from earlier natural philosophy and celestial/Kabbalistic interests into late Florentine anti-divinatory critique.", "DRAFT", "sp_akopyan_astrology_structure"),
    ("bio-farmer", "scholar", "Stephen A. Farmer", "900 Theses and syncretic systems", "Farmer restores the 900 Conclusions as a massive puzzle and oral-disputational project whose hidden connections structure Pico's Roman ambition.", "DRAFT", "sp_farmer_roman_debate"),
    ("bio-wirszubski", "scholar", "Chaim Wirszubski", "Pico and Jewish mysticism", "Wirszubski clarifies the sources, manuscripts, translations, and Christianizing shape of Pico's Kabbalah, making him essential for any serious portal treatment of Pico's Hebrew and Kabbalistic materials.", "DRAFT", "sp_wirszubski_kabbalah_opening"),
    ("bio-akopyan", "scholar", "Ovanes Akopyan", "Pico and astrology", "Akopyan supplies the main structure for reading Pico's Disputationes, its prehistory, sources, natural philosophy, and pro/contra afterlife.", "DRAFT", "sp_akopyan_astrology_structure"),
]


CLAIMS = [
    ("claim_howlett_002", "sp_howlett_intro_life", DOCS["howlett"], "Howlett presents Pico as a contested site whose fame is sustained by competing myths: philosopher-prince, saintly penitent, proto-modern individual, Ficino satellite, and universal knower.", "historiographical", "reception", "Pico biography", "pp. 11-12", "high", "DRAFT", ""),
    ("claim_howlett_003", "sp_howlett_intro_life", DOCS["howlett"], "Howlett's fourfold re-evaluation reads Pico as coherent, structured by Aristotelianism-Platonism-Kabbalism, only partially successful in concord, and exceptionalist rather than Ficinian-renovative.", "interpretive", "historiography", "Howlett position", "pp. 13-17", "high", "DRAFT", ""),
    ("claim_howlett_004", "sp_howlett_intro_life", DOCS["howlett"], "Pico's noble status enabled the Roman debate project, access to courts, and the hiring of translators and scholars.", "historical", "biography", "Pico social status", "p. 20", "high", "DRAFT", ""),
    ("claim_howlett_005", "sp_howlett_intro_life", DOCS["howlett"], "Pico studied at Ferrara, Padua, Pavia, Florence, and Paris, making his formation strongly scholastic and Aristotelian as well as Platonic.", "historical", "education", "Pico education", "pp. 22-24", "high", "DRAFT", ""),
    ("claim_howlett_006", "sp_howlett_intro_life", DOCS["howlett"], "In 1486 Pico moved between Perugia and La Fratta while preparing the debate project with an entourage including Elijah del Medigo and Flavius Mithridates.", "historical", "biography", "1486 preparation", "pp. 26-27", "high", "DRAFT", ""),
    ("claim_copenhaver_magic_003", "sp_copenhaver_magic_intro", DOCS["copenhaver_magic"], "Copenhaver argues that being wrong about Pico means misunderstanding Renaissance humanism itself.", "historiographical", "humanism", "Copenhaver 2019", "p. 21", "high", "DRAFT", ""),
    ("claim_copenhaver_trial_003", "sp_copenhaver_trial_intro", DOCS["copenhaver_trial"], "Copenhaver's 2022 book relocates Pico's Conclusions and Apology in late medieval scholastic thought rather than progressive humanism.", "historiographical", "scholasticism", "Copenhaver 2022", "p. 17", "high", "DRAFT", ""),
    ("claim_farmer_001", "sp_farmer_roman_debate", DOCS["farmer"], "Farmer argues that the 900 Theses were designed as an elaborate puzzle whose hidden concatenation Pico expected to reveal in debate.", "interpretive", "900 Conclusions", "Farmer Roman debate", "pp. 19-20", "high", "DRAFT", ""),
    ("claim_farmer_002", "sp_farmer_roman_debate", DOCS["farmer"], "The 900 Theses were printed in Rome on 7 December 1486 and circulated publicly and to universities.", "historical", "publication", "900 Conclusions", "p. 21", "high", "DRAFT", ""),
    ("claim_wirszubski_001", "sp_wirszubski_kabbalah_opening", DOCS["wirszubski"], "Pico became interested in Kabbalah before he knew Hebrew and studied Hebrew/Chaldean for the sake of Kabbalah.", "historical", "Kabbalah", "Pico Hebrew", "p. 15", "high", "DRAFT", ""),
    ("claim_wirszubski_002", "sp_wirszubski_kabbalah_opening", DOCS["wirszubski"], "Pico likely depended heavily on Mithridates' Latin translations for Kabbalistic reading in 1486.", "historical", "translation", "Mithridates", "pp. 16-18", "high", "DRAFT", ""),
    ("claim_akopyan_001", "sp_akopyan_astrology_structure", DOCS["akopyan"], "Akopyan's structure treats Pico and astrology as a developmental arc from 1486-1493 into the Disputationes and its later pro/contra reception.", "historiographical", "astrology", "Akopyan position", "contents", "high", "DRAFT", ""),
]


LOCATIONS = [
    ("la_frata", "La Fratta", "Italy", 43.167, 12.133, "retreat_site", "Pico's country retreat near Perugia where he worked in autumn 1486 while preparing the Roman debate and studying languages/Kabbalah; coordinate approximate and needs review.", "needs_review"),
    ("milan", "Milan", "Italy", 45.4642, 9.1900, "power_network", "Sforza/Visconti power network involved in Pico's diplomatic rescue after the French detention.", "likely"),
]


TIMELINE = [
    ("tl_064", "1482", None, "Autumn 1482", "Studies at Pavia", "Howlett places Pico at Pavia University from autumn 1482 into 1483; Pavia is important for logic, mathematics, and scholastic philosophy.", "pavia", "education", "likely", "Howlett, Life and Works, extracted p. 24.", 4),
    ("tl_065", "1485", None, "Summer 1485", "Goes to Paris", "Wirszubski notes that Pico went to Paris in summer 1485 and returned to Italy in March 1486.", "paris", "education", "likely", "Wirszubski, ch. 1, extracted p. 17.", 4),
    ("tl_066", "1486-03", None, "March 1486", "Returns from Paris to Italy", "Pico returns to Italy from Paris, entering the decisive year of Arezzo, Perugia/La Fratta, Hebrew/Kabbalah study, and the 900 Conclusions.", "florence", "travel", "likely", "Wirszubski, ch. 1, extracted p. 17.", 4),
    ("tl_067", "1486-05", None, "May 1486", "Arezzo abduction scandal", "Howlett records Pico's attempt to abduct Margherita de' Medici at Arezzo, after which he was caught, she was rescued, and Pico was disgraced.", "arezzo", "trouble", "likely", "Howlett, Life and Works, extracted p. 27.", 5),
    ("tl_068", "1486-07", None, "July 1486", "Elijah del Medigo joins Pico", "Howlett notes that Pico's old teacher Elijah del Medigo came to him while he was preparing the debate project.", "perugia", "network", "likely", "Howlett, Life and Works, extracted p. 27.", 3),
    ("tl_069", "1486-08", None, "Summer 1486", "Mithridates translations flow in", "Wirszubski identifies summer 1486 as the period when Flavius Mithridates' Kabbalistic translations for Pico flowed in great profusion.", "la_frata", "translation", "likely", "Wirszubski, ch. 1, extracted pp. 17-18.", 5),
    ("tl_070", "1486-10-15", None, "15 October 1486", "Pico at Perugia", "Wirszubski uses a dated letter to Andrea Corneo to place Pico at Perugia on 15 October 1486.", "perugia", "travel", "verified", "Wirszubski, ch. 1, extracted p. 16.", 4),
    ("tl_071", "1486-12-07", None, "7 December 1486", "900 Theses printed in Rome", "Farmer states that the text of the 900 Theses was printed by Eucharius Silber in Rome on 7 December 1486.", "rome", "publication", "verified", "Farmer, Roman Debate, extracted p. 21.", 5),
    ("tl_072", "1488", None, "1488", "Vincennes as royal-protective detention", "Howlett reports that Pico was imprisoned at the royal palace of Vincennes, away from papal nuncios; this suggests detention under French royal protection as well as confinement.", "vincennes", "trouble", "likely", "Howlett, Life and Works, extracted p. 30.", 5),
]


def write(path: str, text: str) -> Path:
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(text, encoding="utf-8", newline="\n")
    return full


def register_artifact(conn, artifact_id, artifact_type, title, path, doc_id, target):
    now = datetime.now().isoformat(timespec="seconds")
    conn.execute(
        """
        INSERT OR REPLACE INTO reading_artifacts
        (id,artifact_type,title,path,document_id,target_entity,status,evidence_status,created_at,updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        (artifact_id, artifact_type, title, str(path), doc_id, target, "DRAFT", "SOURCE_ANCHORED_DRAFT", now, now),
    )


def main():
    conn = sqlite3.connect(DB)
    for rel, text in NOTES.items():
        full = write(rel, text)
        aid = "sp_" + full.stem.replace("_seed", "")
        # Explicit IDs where filenames already include prefix.
        aid = full.stem if full.stem.startswith("sp_") else aid
        register_artifact(conn, aid, "source_packet", full.stem.replace("_", " ").title(), full, None, full.stem)
    for rel, text in WEBSITE_NOTES.items():
        full = write(rel, text)
        if "historiography" in rel:
            typ = "historiography_node"
        elif "concepts" in rel:
            typ = "concept_dossier"
        else:
            typ = "website_page"
        aid = "note_" + full.stem
        register_artifact(conn, aid, typ, full.stem.replace("_", " ").title(), full, None, full.stem)
        conn.execute(
            "INSERT OR REPLACE INTO website_pages(id,entity_type,title,markdown_path,status,source_artifact_id) VALUES (?,?,?,?,?,?)",
            ("page_" + full.stem, typ, full.stem.replace("_", " ").title(), str(full), "DRAFT", aid),
        )
    conn.executemany(
        "INSERT OR REPLACE INTO website_cards(id,entity_type,title,subtitle,summary,status,source_artifact_id) VALUES (?,?,?,?,?,?,?)",
        CARDS,
    )
    conn.executemany(
        """
        INSERT OR REPLACE INTO claims
        (id,artifact_id,document_id,claim_text,claim_type,theme,target_entity,evidence_page,confidence,review_status,notes)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """,
        CLAIMS,
    )
    conn.executemany(
        "INSERT OR REPLACE INTO locations(id,name,modern_country,latitude,longitude,location_type,pico_role,evidence_status) VALUES (?,?,?,?,?,?,?,?)",
        LOCATIONS,
    )
    conn.executemany(
        """
        INSERT OR REPLACE INTO timeline_events
        (id,start_date,end_date,date_label,title,summary,location_id,category,evidence_status,source_note,importance)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """,
        TIMELINE,
    )
    conn.commit()
    # Reuse export and static-site builder from the artifact seeder.
    spec = importlib.util.spec_from_file_location("seed_research_artifacts", ROOT / "scripts" / "seed_research_artifacts.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.export_data(conn)
    mod.build_site(conn)
    conn.close()
    print("Study pass 002 complete.")


if __name__ == "__main__":
    main()
