"""Study pass 003: primary-text and textual-transmission notes.

This pass begins sustained reading of Pico's own works and the textual
apparatus around the 900 Conclusions:
- Oration opening and ascent sequence
- On Being and the One, proem and opening chapters
- Heptaplus first and second proems
- Farmer on the 900 Conclusions as text, edition, hidden-connection system
- Farmer on Disputationes/tampering problems
"""

from __future__ import annotations

import importlib.util
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "pico.db"


DOCS = {
    "anthology": "Heptaplus_Pico_della_Mirandola_On_the_Dignity_of_Man_Being_and_One_pdf_29945776",
    "farmer": "Medieval_Renaissance_Texts_Studies_167_Stephen_A_Farmer_Giovanni_Pico_Della_Mirandola_Syncretism_pdf_c99b971b",
}


SOURCE_PACKETS = {
    "artifacts/source_packets/oration_opening_ascent.md": """# Source Packet: Oration Opening and Ascent Sequence

- Artifact ID: `sp_oration_opening_ascent`
- Document ID: `Heptaplus_Pico_della_Mirandola_On_the_Dignity_of_Man_Being_and_One_pdf_29945776`
- Page range studied: extracted pages 38-54
- Evidence status: SOURCE_ANCHORED_DRAFT

## Local Summary

The opening of the Oration begins with the familiar claim that man is a great wonder, but the argument immediately moves beyond generic human excellence. Pico rejects ordinary explanations of human greatness: man is not most wonderful merely because he mediates between creatures, interprets nature, joins eternity and time, or stands a little lower than the angels. The decisive point is indeterminacy. God gives Adam no fixed seat, form, or peculiar gift; instead, man is placed at the world's center with the power to shape himself downward into plant or brute, upward into heavenly rationality, angelic intellect, and ultimately unity with God.

This opening must therefore be read as a moral and mystical program, not as a secular declaration of autonomy. The passage builds a ladder of transformation: seeds of life, moral choice, angelic models, purgation, dialectic, natural philosophy, theology, and finally union beyond ordinary selfhood. The seraph, cherub, and throne provide a threefold model: charity, intelligence, and judgment. The Jacob's ladder passage turns that model into method: moral philosophy washes the lower powers, dialectic trains orderly ascent and descent, natural philosophy reads the ladder of nature, and theology brings the soul to peace in the Father.

The philosophical disciplines are not ornamental. They are the mechanism of ascent. Moral philosophy disciplines appetite and anger; dialectic calms unstable reason; natural philosophy handles the conflict and multiplicity of nature; theology alone brings the peace that nature cannot give. Pico reinforces this order by appealing across Christian, Mosaic, Greek, Pythagorean, Chaldean, and Kabbalistic materials, making the Oration a concordist initiation speech for the proposed disputation.

## Extracted Claims

| Claim | Type | Theme | Evidence |
|---|---|---|---|
| Pico's initial account of dignity is grounded in human indeterminacy rather than fixed excellence. | textual | Oration | extracted pp. 38-40 |
| The opening ascent moves from lower life through reason and intellect toward union with God. | textual | Oration | extracted pp. 40-42 |
| Seraph, cherub, and throne organize charity, intelligence, and judgment as angelic models for human ascent. | textual | angelology | extracted pp. 42-44 |
| Pico assigns moral philosophy, dialectic, natural philosophy, and theology distinct roles in purification and ascent. | textual | philosophy | extracted pp. 44-49 |
| The Oration uses Mosaic, Christian, Greek, Pythagorean, Chaldean, and Kabbalistic witnesses to support a concordist discipline of philosophy. | textual | concord | extracted pp. 47-52 |

## Candidate Promotions

- Oration work dossier: opening sequence, discipline ladder, angelic models.
- Concept dossier: philosophical ascent.
- Website introduction: dignity is indeterminate vocation ordered to purification and union.
""",
    "artifacts/source_packets/on_being_one_opening.md": """# Source Packet: On Being and the One, Proem and Opening Chapters

- Artifact ID: `sp_on_being_one_opening`
- Document ID: `Heptaplus_Pico_della_Mirandola_On_the_Dignity_of_Man_Being_and_One_pdf_29945776`
- Page range studied: extracted pages 72-88
- Evidence status: SOURCE_ANCHORED_DRAFT

## Local Summary

On Being and the One is framed as a response to a discussion among Lorenzo de' Medici, Angelo Poliziano, and Domenico Benivieni. Pico states the problem as a concordist one: those who think Aristotle disagrees with Plato disagree with Pico, who makes a concordant philosophy of both. The immediate issue is whether the one is superior to being, as Platonists claim, or convertible with being, as Aristotle appears to teach.

The first chapters refuse an easy Platonist victory. Pico argues that the Parmenides is a dialectical exercise rather than a doctrinal assertion, and that the Sophist better supports equality between one and being. He then distinguishes senses of "being." In the ordinary and Aristotelian sense, being includes whatever is outside nothing and is convertible with the one. In a stricter participatory sense, God can be said to be above being, because God is existence itself rather than a being that participates in existence.

The central strategy is not to choose Plato over Aristotle but to show how both languages can be true when their senses are carefully distinguished. Pico then develops a four-step negative-theological ascent. One first removes corporeal and lower imperfections from divine names, then removes particular generic limitation, then recognizes the deficiency of names, and finally enters the "light of ignorance," where God is known as above every name and concept. This makes On Being and the One crucial for the portal's ontology: concord requires semantic discipline, metaphysical hierarchy, and apophatic humility.

## Extracted Claims

| Claim | Type | Theme | Evidence |
|---|---|---|---|
| The work is explicitly framed as a defense of concord between Plato and Aristotle. | textual | concord | extracted pp. 72-73 |
| Pico reads the Parmenides as dialectical exercise rather than clear doctrine about the one above being. | textual | Platonism | extracted pp. 74-76 |
| Pico distinguishes two senses of being: what is outside nothing and what participates in existence. | textual | metaphysics | extracted pp. 76-80 |
| God can be called above being because God is existence itself, not a being by participation. | textual | theology | extracted pp. 79-80 |
| The four-step ascent to divine darkness joins scholastic semantics to Dionysian negative theology. | textual | apophasis | extracted pp. 81-88 |

## Candidate Promotions

- Work dossier: On Being and the One.
- Concept dossier: concord as semantic discipline.
- Ontology term: apophatic ascent / divine darkness.
""",
    "artifacts/source_packets/heptaplus_proems.md": """# Source Packet: Heptaplus Proems

- Artifact ID: `sp_heptaplus_proems`
- Document ID: `Heptaplus_Pico_della_Mirandola_On_the_Dignity_of_Man_Being_and_One_pdf_29945776`
- Page range studied: extracted pages 101-114
- Evidence status: SOURCE_ANCHORED_DRAFT

## Local Summary

The publisher's dedication presents the Heptaplus as a correct edition of Pico's Sevenfold Narration of the Six Days of Genesis, dedicated to Lorenzo de' Medici and meant to make Pico's natural and divine mysteries common to scholars. Pico's own proem explains the work as a response to Lorenzo's interest in Moses and as an aid to Pico's broader work on the Psalms. Genesis is treated as the site where the secrets of all nature are contained.

The first proem defends the philosophical depth of Moses against readers who see only rough surface simplicity. Pico argues that ancient sages often concealed religious truth through figures, silence, allegory, veils, mathematical images, and parables. Moses, Christ, Matthew, John, Paul, and Dionysius are aligned within a broad theory of esoteric communication: divine wisdom is not always written plainly because not all audiences can bear it. The creation narrative is therefore a privileged field for hidden philosophy.

Pico states three interpretive difficulties. First, Moses must not seem inadequate or unsophisticated. Second, interpretation must remain coherent rather than arbitrary, holding a continuous line within each sense. Third, Moses must not be made to assert anything alien to nature or to truths accepted by better philosophers. The second proem then lays out the famous world-structure: ultramundane/angelic, celestial, sublunary, and man as a fourth lesser world. The worlds mutually contain one another, and this mutual containment grounds allegorical interpretation. The scripture of Moses becomes an exact image of the world.

## Extracted Claims

| Claim | Type | Theme | Evidence |
|---|---|---|---|
| Pico treats Genesis as containing secrets of all nature. | textual | Heptaplus | extracted pp. 102-103 |
| The Heptaplus defends hidden philosophical meaning beneath the plain surface of Mosaic writing. | textual | hermeneutics | extracted pp. 103-106 |
| Pico's method requires coherent interpretation across seven senses rather than arbitrary allegory. | methodological | hermeneutics | extracted pp. 108-110 |
| Pico names three worlds: angelic/intelligible, celestial, and sublunary. | textual | cosmology | extracted pp. 110-112 |
| Man is a fourth world containing the rest, a lesser world with elemental body, heavenly spirit, vegetative soul, sense, reason, angelic mind, and likeness of God. | textual | anthropology | extracted pp. 114 |
| Mutual containment of worlds grounds allegorical interpretation. | interpretive | allegory | extracted pp. 112-114 |

## Candidate Promotions

- Heptaplus work dossier: proem, sevenfold method, four worlds.
- Concept dossier: mutual containment.
- Concept dossier: allegory and natural correspondences.
""",
    "artifacts/source_packets/farmer_preface_textual_system.md": """# Source Packet: Farmer Preface and 900 Conclusions Textual System

- Artifact ID: `sp_farmer_preface_textual_system`
- Document ID: `Medieval_Renaissance_Texts_Studies_167_Stephen_A_Farmer_Giovanni_Pico_Della_Mirandola_Syncretism_pdf_c99b971b`
- Page range studied: extracted pages 5-12
- Evidence status: SOURCE_ANCHORED_DRAFT

## Local Summary

Farmer's table of contents and preface define the 900 Conclusions as both an edition problem and a theory problem. The book has two parts: an introductory monograph on Pico's Roman debate, syncretism, the deciphering of the theses, and Pico/Anti-Pico; then a text, translation, and commentary. The preface frames Pico as the obvious Renaissance case for studying syncretic processes, because the 900 theses compress more than two thousand years of Western traditions and expose the growth and decline of premodern religious and philosophical systems.

The 900 Conclusions are treated as a handbook of late fifteenth-century thought. They address Greek, Arabic, Hebrew, and Latin scholastic conflicts, Renaissance Neoplatonism, humanism, natural magic, numerology, astrology, Kabbalah, and related esoteric traditions. Farmer stresses that the work had no fixed title in the princeps because it was meant to be debated, not simply read. It also became, according to Farmer, the first printed book banned universally by the church.

Farmer makes the hidden-connection problem central. Pico's Apology says an occulta concatenatio links scattered theses, but corruption in accessible versions made serious study nearly impossible. Farmer's edition aims to provide the first reliable version since the rare princeps and the first translation based on trustworthy Latin sources. For PicoDB, this means every claim about the 900 Conclusions must track edition, numbering, translation, and hidden cross-links.

## Extracted Claims

| Claim | Type | Theme | Evidence |
|---|---|---|---|
| Farmer divides the project into an introductory monograph and a text/translation/commentary of the 900 Conclusions. | bibliographic | 900 Conclusions | extracted pp. 5-6 |
| The 900 Conclusions are presented as a unique window onto Renaissance thought and premodern intellectual systems. | historiographical | syncretism | extracted pp. 9-10 |
| Pico's theses cover Greek, Arabic, Hebrew, and Latin scholasticism, Neoplatonism, magic, numerology, astrology, and Kabbalah. | bibliographic | corpus scope | extracted p. 10 |
| The editio princeps carried no title because the theses were meant for debate rather than ordinary reading. | textual | publication | extracted p. 10 |
| Farmer treats the occulta concatenatio as a hidden structure that requires reconstruction across scattered theses. | methodological | hidden connections | extracted p. 10 |
| Textual corruption in later versions made meaningful study of the theses difficult before Farmer's edition. | textual | textual transmission | extracted pp. 10-11 |

## Candidate Promotions

- Work dossier: 900 Conclusions textual status.
- Ontology: hidden connection, thesis cluster, edition witness.
- Website note: the 900 Conclusions as database object rather than linear treatise.
""",
    "artifacts/source_packets/farmer_deciphering_900.md": """# Source Packet: Farmer, Deciphering the 900 Theses

- Artifact ID: `sp_farmer_deciphering_900`
- Document ID: `Medieval_Renaissance_Texts_Studies_167_Stephen_A_Farmer_Giovanni_Pico_Della_Mirandola_Syncretism_pdf_c99b971b`
- Page range studied: extracted pages 115-121
- Evidence status: SOURCE_ANCHORED_DRAFT

## Local Summary

Farmer's chapter on deciphering begins from Pico's own Apology: a disputation proposition is brief, concise, and unexplained because difficulties are meant to be resolved in the battle of debate. The 900 Conclusions are therefore not self-explanatory aphorisms. They are intentionally compressed nodes in a disputational system, loaded with ambiguities that Pico expected to resolve orally.

Farmer's first example is Pico's treatment of the substance/accident distinction. Pico uses linguistic reversals and hierarchical correspondences to reconcile apparently conflicting theses. What counts as substance or accident depends on level, relation, and cosmic hierarchy. This method supports Pico's wider Neoplatonic and emanationist system, but it also creates theological danger. His account of accidents threatens ordinary accounts of separable accidents and therefore raises Eucharistic problems, leading to some of the theses attacked by the papal commission.

The chapter then ties substance/accident questions to epistemology and mysticism. The dispute over intelligible images is not merely technical psychology; it reflects metaphysical and theological assumptions about intellect, participation, hierarchy, and ascent. Pico can make room for both Aristotelian sensual abstraction and Platonic innate/elevated knowledge by assigning them different levels in a hierarchical theory of cognition.

## Extracted Claims

| Claim | Type | Theme | Evidence |
|---|---|---|---|
| Pico's theses are intentionally brief debate propositions whose difficulties were meant to be resolved in oral dispute. | methodological | disputation | extracted p. 115 |
| Farmer reads the theses by collating topically related propositions rather than isolating them. | methodological | reading system | extracted p. 115 |
| Pico hierarchizes the substance/accident distinction through cosmic proportion and correspondence. | interpretive | metaphysics | extracted pp. 116-117 |
| Pico's position on accidents created danger around Eucharistic theology and separable accidents. | historical | heresy | extracted pp. 117-118 |
| Pico reconciles Aristotelian and Platonic knowledge by assigning ordinary abstraction and elevated knowledge to different levels. | interpretive | epistemology | extracted pp. 119-121 |

## Candidate Promotions

- Reading system: thesis cluster collation protocol.
- Concept dossier: substance/accident hierarchy.
- Trial page: Eucharist, accidents, and papal danger.
""",
    "artifacts/source_packets/farmer_disputationes_tampering.md": """# Source Packet: Farmer on Disputationes and Posthumous Tampering

- Artifact ID: `sp_farmer_disputationes_tampering`
- Document ID: `Medieval_Renaissance_Texts_Studies_167_Stephen_A_Farmer_Giovanni_Pico_Della_Mirandola_Syncretism_pdf_c99b971b`
- Page range studied: extracted pages 189-194
- Evidence status: SOURCE_ANCHORED_DRAFT

## Local Summary

Farmer's chapter on Pico and Anti-Pico makes textual transmission into a major interpretive problem. He argues that no text of Pico printed or reprinted by Gianfrancesco Pico can be assumed free from adulteration. Even the printed Oration shows minor but noteworthy tampering when compared with early draft materials and parallel Apology passages, especially around magic, Cabala, demons, Mithridates, and Pico's associates.

The Disputationes is the critical case. Farmer asks whether Pico's apparent palinode against prisci theologi, natural magic, esoteric numerology, and Cabala is real or the result of posthumous doctoring. He does not claim final certainty for every line, but shifts the burden of proof: given Gianfrancesco's record and evidence of Pico's continuing esoteric interests, anyone denying serious tampering must make the case.

The Savonarolan context matters. Pico's papers were held at San Marco; Gianfrancesco sought Savonarola's advice; Savonarola used the Disputationes in a political-prophetic conflict over astrology and natural prophecy in Florence. Farmer argues that through Gianfrancesco's editorial manipulation, the apolitical elder Pico was posthumously made to join Savonarola's camp. This gives PicoDB an important rule: late works, especially the Disputationes, require textual-transmission status before doctrinal conclusions are promoted.

## Extracted Claims

| Claim | Type | Theme | Evidence |
|---|---|---|---|
| Farmer argues that Pico texts printed or reprinted by Gianfrancesco cannot be assumed free of adulteration. | historiographical | textual transmission | extracted p. 189 |
| Farmer sees minor but noteworthy tampering even in Gianfrancesco's printed Oration. | textual | Oration | extracted p. 189 |
| The Disputationes may not straightforwardly represent Pico's own palinode against magic, Cabala, and prisci theologi. | interpretive | Disputationes | extracted pp. 189-190 |
| Farmer shifts the burden of proof toward those denying serious tampering in the Disputationes. | historiographical | Disputationes | extracted p. 190 |
| Savonarola and Gianfrancesco had political and religious reasons to use Pico's anti-astrology work in Florentine propaganda. | historical | Savonarola | extracted pp. 190-194 |
| PicoDB should mark late printed Pico texts with textual-transmission risk before using them as evidence for doctrine. | methodological | ontology | extracted pp. 189-194 |

## Candidate Promotions

- Historiography node: textual tampering and the Anti-Pico problem.
- Work dossier: Disputationes evidence risk.
- Ontology flag: transmission_status.
""",
}


WEBSITE_NOTES = {
    "artifacts/website_notes/works/oration_primary_pass003.md": """# Oration Work Dossier Pass 003

## Status

SOURCE_ANCHORED_DRAFT based on extracted pages 38-54 of the anthology translation.

## Section Summary

The opening section begins with wonder at man but turns immediately to the problem of why man is more wonderful than angels. Pico's answer is not that man has a fixed superiority; it is that man has no fixed seat, form, or proprietary gift. The human being is a mobile, self-shaping creature who can descend into plant or brute life, rise into rational and angelic life, and finally become one spirit with God.

The next movement converts this anthropology into a discipline of ascent. Seraph, cherub, and throne become models of charity, intelligence, and judgment. Jacob's ladder then becomes the structure of philosophical practice: moral philosophy washes appetite and anger; dialectic trains reason to move in order; natural philosophy follows the ladder of nature through multiplicity; theology brings final peace and union.

This section should not be presented as secular self-fashioning without qualification. Pico's freedom is dangerous, ascetic, and teleological. Human plasticity is ordered toward purification, philosophy, theology, angelic imitation, and union with God.

## Website Use

The Oration page should open with the problem of indeterminacy and ascent rather than the modern slogan of dignity. The title can still use "Dignity," but the body must immediately explain that dignity means an unstable vocation: the human creature can become lower, higher, angelic, or united with God depending on the cultivated seed and the philosophical-theological path.
""",
    "artifacts/website_notes/works/being_one_primary_pass003.md": """# On Being and the One Work Dossier Pass 003

## Status

SOURCE_ANCHORED_DRAFT based on extracted pages 72-88 of the anthology translation.

## Section Summary

On Being and the One is a compact concordist work. Pico writes to Poliziano after Lorenzo de' Medici raised the question of whether the one is above being. The work defends the possibility of reconciling Aristotle and Plato by distinguishing senses of "being" and by refusing to treat Platonic language as always doctrinally literal.

The opening chapters argue that the Parmenides is a dialectical exercise and that the Sophist supports the convertibility of one and being. Pico then distinguishes being as "whatever is outside nothing" from being as a participated mode. In the first sense, being and one are convertible. In the second, God is above being because God is existence itself, not a being that participates in existence.

The work culminates in a four-step apophatic ascent: remove corporeal errors, remove particular generic limitations, recognize the inadequacy of names, and enter the light of ignorance. This makes the text central for PicoDB's pages on concord, scholastic semantics, and negative theology.
""",
    "artifacts/website_notes/works/heptaplus_primary_pass003.md": """# Heptaplus Work Dossier Pass 003

## Status

SOURCE_ANCHORED_DRAFT based on extracted pages 101-114 of the anthology translation.

## Section Summary

The Heptaplus begins as a Genesis project dedicated to Lorenzo de' Medici and tied to Pico's broader biblical scholarship. Pico presents Moses as a writer whose surface simplicity hides philosophical and natural secrets. Ancient wisdom, Christian scripture, Jewish commentary, Pythagorean silence, Platonic allegory, and Dionysian esotericism all support the idea that divine truth is often veiled.

Pico identifies three interpretive demands: defend Moses from the charge of inadequacy, maintain coherent interpretation across each sense, and avoid attributing to Moses claims contrary to nature or sound philosophy. The sevenfold interpretation is not supposed to be arbitrary allegory; it is a disciplined attempt to read Genesis as an exact image of the world.

The second proem gives the portal a major conceptual structure: three worlds plus man as a fourth lesser world. The angelic/intelligible, celestial, and sublunary worlds mutually contain one another, and man contains them in miniature. Allegory is possible because natures correspond across worlds.
""",
    "artifacts/website_notes/works/conclusions_900_pass003.md": """# 900 Conclusions Work Dossier Pass 003

## Status

SOURCE_ANCHORED_DRAFT based on Farmer's preface and chapter 3 opening.

## Section Summary

The 900 Conclusions must be represented as a database object, not merely a book. Farmer's account makes them a set of brief debate propositions whose meanings depend on hidden connections, topical clusters, oral disputation, edition history, and cross-traditional authorities. They cover scholastic conflicts across Greek, Arabic, Hebrew, and Latin traditions as well as Neoplatonism, magic, numerology, astrology, and Kabbalah.

The reading protocol is therefore cluster-first. A thesis should not be interpreted alone when Farmer gives reason to collate related theses. Pico's substance/accident material shows the method: apparently conflicting propositions become intelligible when arranged hierarchically across worlds and levels of being.

The website should let readers browse the 900 Conclusions by thesis number, theme, authority, tradition, danger level, hidden-connection cluster, and relation to the papal case.
""",
    "artifacts/website_notes/historiography/textual_tampering_antipico.md": """# Historiography Node: Textual Tampering and the Anti-Pico Problem

## Status

SOURCE_ANCHORED_DRAFT based on Farmer, chapter 4.

## Argument

Farmer turns Pico's posthumous textual transmission into a historiographical problem. The late Pico cannot be read simply from printed texts edited by Gianfrancesco Pico. Farmer argues that Gianfrancesco, Savonarola, and their circle had religious and political motives for reshaping Pico's papers, especially around astrology, magic, Cabala, and prophecy.

This matters most for the Disputationes. If the anti-astrology text was doctored, shortened, or selectively framed, then Pico's apparent late rejection of prisci theologi, natural magic, esoteric numerology, and Cabala cannot be treated as straightforward evidence without transmission analysis.

## Portal Rule

Every work dossier should include a `transmission_status` field before doctrinal claims are promoted. Late printed works and works controlled by Gianfrancesco/San Marco should carry explicit risk notes.
""",
}


ARTIFACT_ROWS = [
    ("sp_oration_opening_ascent", "source_packet", "Oration Opening and Ascent Sequence", "artifacts/source_packets/oration_opening_ascent.md", DOCS["anthology"], "Oration on the Dignity of Man", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("sp_on_being_one_opening", "source_packet", "On Being and the One Opening", "artifacts/source_packets/on_being_one_opening.md", DOCS["anthology"], "On Being and the One", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("sp_heptaplus_proems", "source_packet", "Heptaplus Proems", "artifacts/source_packets/heptaplus_proems.md", DOCS["anthology"], "Heptaplus", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("sp_farmer_preface_textual_system", "source_packet", "Farmer Preface and 900 Conclusions Textual System", "artifacts/source_packets/farmer_preface_textual_system.md", DOCS["farmer"], "900 Conclusions", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("sp_farmer_deciphering_900", "source_packet", "Farmer Deciphering the 900 Theses", "artifacts/source_packets/farmer_deciphering_900.md", DOCS["farmer"], "900 Conclusions", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("sp_farmer_disputationes_tampering", "source_packet", "Farmer on Disputationes and Posthumous Tampering", "artifacts/source_packets/farmer_disputationes_tampering.md", DOCS["farmer"], "Disputationes", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("work-oration-pass003", "pico_work_dossier", "Oration Work Dossier Pass 003", "artifacts/website_notes/works/oration_primary_pass003.md", DOCS["anthology"], "Oration on the Dignity of Man", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("work-being-one-pass003", "pico_work_dossier", "On Being and the One Work Dossier Pass 003", "artifacts/website_notes/works/being_one_primary_pass003.md", DOCS["anthology"], "On Being and the One", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("work-heptaplus-pass003", "pico_work_dossier", "Heptaplus Work Dossier Pass 003", "artifacts/website_notes/works/heptaplus_primary_pass003.md", DOCS["anthology"], "Heptaplus", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("work-900-pass003", "pico_work_dossier", "900 Conclusions Work Dossier Pass 003", "artifacts/website_notes/works/conclusions_900_pass003.md", DOCS["farmer"], "900 Conclusions", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("hist-textual-tampering", "historiography_node", "Textual Tampering and the Anti-Pico Problem", "artifacts/website_notes/historiography/textual_tampering_antipico.md", DOCS["farmer"], "Disputationes", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
]


CLAIMS = [
    ("claim_oration_001", "sp_oration_opening_ascent", DOCS["anthology"], "Pico grounds the Oration's opening anthropology in human indeterminacy rather than fixed human superiority.", "textual", "Oration", "Oration opening", "extracted pp. 38-40", "high", "DRAFT", ""),
    ("claim_oration_002", "sp_oration_opening_ascent", DOCS["anthology"], "The Oration opening describes a ladder of transformation from lower life through reason and intellect toward unity with God.", "textual", "ascent", "Oration opening", "extracted pp. 40-42", "high", "DRAFT", ""),
    ("claim_oration_003", "sp_oration_opening_ascent", DOCS["anthology"], "Pico assigns moral philosophy, dialectic, natural philosophy, and theology distinct roles in purgation, ordering, contemplation, and final peace.", "textual", "philosophy", "Oration discipline ladder", "extracted pp. 44-49", "high", "DRAFT", ""),
    ("claim_being_001", "sp_on_being_one_opening", DOCS["anthology"], "On Being and the One is framed as a concordist defense of agreement between Plato and Aristotle.", "textual", "concord", "On Being and the One", "extracted pp. 72-73", "high", "DRAFT", ""),
    ("claim_being_002", "sp_on_being_one_opening", DOCS["anthology"], "Pico distinguishes being as what is outside nothing from being as participated existence in order to reconcile Aristotelian and Platonist language.", "textual", "metaphysics", "being and one", "extracted pp. 76-80", "high", "DRAFT", ""),
    ("claim_being_003", "sp_on_being_one_opening", DOCS["anthology"], "Pico's four-step ascent to divine darkness joins semantic analysis with Dionysian negative theology.", "interpretive", "apophasis", "divine darkness", "extracted pp. 81-88", "high", "DRAFT", ""),
    ("claim_heptaplus_001", "sp_heptaplus_proems", DOCS["anthology"], "Pico treats the Mosaic creation narrative as containing the secrets of all nature.", "textual", "Heptaplus", "Genesis", "extracted pp. 102-103", "high", "DRAFT", ""),
    ("claim_heptaplus_002", "sp_heptaplus_proems", DOCS["anthology"], "The Heptaplus requires coherent sevenfold interpretation rather than arbitrary allegorical switching.", "methodological", "hermeneutics", "Heptaplus method", "extracted pp. 108-110", "high", "DRAFT", ""),
    ("claim_heptaplus_003", "sp_heptaplus_proems", DOCS["anthology"], "Pico's second proem defines three worlds and man as a fourth lesser world containing the rest.", "textual", "cosmology", "four worlds", "extracted pp. 110-114", "high", "DRAFT", ""),
    ("claim_heptaplus_004", "sp_heptaplus_proems", DOCS["anthology"], "Mutual containment among worlds grounds Pico's theory of allegorical interpretation.", "interpretive", "allegory", "mutual containment", "extracted pp. 112-114", "high", "DRAFT", ""),
    ("claim_farmer_text_001", "sp_farmer_preface_textual_system", DOCS["farmer"], "Farmer treats the 900 Conclusions as a unique window onto Renaissance thought and premodern intellectual systems.", "historiographical", "900 Conclusions", "Farmer preface", "extracted pp. 9-10", "high", "DRAFT", ""),
    ("claim_farmer_text_002", "sp_farmer_preface_textual_system", DOCS["farmer"], "Farmer makes the occulta concatenatio a methodological problem requiring reconstruction across scattered theses.", "methodological", "hidden connections", "900 Conclusions", "extracted p. 10", "high", "DRAFT", ""),
    ("claim_farmer_decipher_001", "sp_farmer_deciphering_900", DOCS["farmer"], "Farmer reads the 900 Conclusions by collating topically related theses rather than isolating individual propositions.", "methodological", "reading system", "900 Conclusions", "extracted p. 115", "high", "DRAFT", ""),
    ("claim_farmer_decipher_002", "sp_farmer_deciphering_900", DOCS["farmer"], "Pico's hierarchical treatment of substance and accident creates theological danger around Eucharistic doctrine.", "interpretive", "heresy", "substance/accident", "extracted pp. 117-118", "high", "DRAFT", ""),
    ("claim_farmer_tamper_001", "sp_farmer_disputationes_tampering", DOCS["farmer"], "Farmer argues that no Pico text printed or reprinted by Gianfrancesco can be assumed free of adulteration.", "historiographical", "textual transmission", "Gianfrancesco Pico", "extracted p. 189", "high", "DRAFT", ""),
    ("claim_farmer_tamper_002", "sp_farmer_disputationes_tampering", DOCS["farmer"], "Farmer treats the Disputationes as a transmission-risk text whose apparent anti-magic palinode may be posthumously shaped.", "interpretive", "Disputationes", "textual tampering", "extracted pp. 189-190", "high", "DRAFT", ""),
    ("claim_farmer_tamper_003", "sp_farmer_disputationes_tampering", DOCS["farmer"], "Farmer connects Savonarolan political prophecy conflicts to the posthumous use and possible doctoring of Pico's anti-astrology work.", "historical", "Savonarola", "Disputationes reception", "extracted pp. 190-194", "high", "DRAFT", ""),
]


CARDS = [
    ("work-oration-primary", "work", "Oration: Indeterminacy and Ascent", "Opening sequence", "The Oration's famous opening is a disciplined program of self-shaping, angelic imitation, philosophical purgation, and ascent to union with God.", "DRAFT", "sp_oration_opening_ascent"),
    ("work-being-one-primary", "work", "On Being and the One", "Concord and apophasis", "Pico reconciles Plato and Aristotle by distinguishing senses of being and by moving from semantics to Dionysian divine darkness.", "DRAFT", "sp_on_being_one_opening"),
    ("work-heptaplus-primary", "work", "Heptaplus: Genesis and the Four Worlds", "Sevenfold Mosaic interpretation", "The Heptaplus reads Genesis as hidden natural and divine philosophy, organized by coherent sevenfold interpretation and a four-world cosmology.", "DRAFT", "sp_heptaplus_proems"),
    ("work-900-system", "work", "900 Conclusions as a Knowledge System", "Thesis clusters and hidden connections", "The 900 Conclusions should be treated as a debate database of compressed propositions, cross-links, traditions, and edition problems.", "DRAFT", "sp_farmer_preface_textual_system"),
    ("hist-antipico", "historiography", "The Anti-Pico Problem", "Textual tampering and late doctrine", "Farmer's textual-transmission argument warns that late printed Pico, especially the Disputationes, cannot be used doctrinally without checking Gianfrancesco/San Marco risk.", "DRAFT", "sp_farmer_disputationes_tampering"),
]


PAGES = [
    ("page-oration-primary-pass003", "work", "Oration: Indeterminacy and Ascent", "artifacts/website_notes/works/oration_primary_pass003.md", "DRAFT", "sp_oration_opening_ascent"),
    ("page-being-one-pass003", "work", "On Being and the One: Concord and Divine Darkness", "artifacts/website_notes/works/being_one_primary_pass003.md", "DRAFT", "sp_on_being_one_opening"),
    ("page-heptaplus-pass003", "work", "Heptaplus: Genesis and the Four Worlds", "artifacts/website_notes/works/heptaplus_primary_pass003.md", "DRAFT", "sp_heptaplus_proems"),
    ("page-900-pass003", "work", "900 Conclusions: Database Object and Debate Machine", "artifacts/website_notes/works/conclusions_900_pass003.md", "DRAFT", "sp_farmer_preface_textual_system"),
    ("page-antipico-pass003", "historiography", "Textual Tampering and the Anti-Pico Problem", "artifacts/website_notes/historiography/textual_tampering_antipico.md", "DRAFT", "sp_farmer_disputationes_tampering"),
]


TIMELINE_EVENTS = [
    ("tl_073", "1489", None, "1489", "Heptaplus dedicated to Lorenzo de' Medici", "The Heptaplus is presented as Pico's Sevenfold Narration of the Six Days of Genesis and dedicated to Lorenzo, joining Genesis, natural secrets, and Medici intellectual patronage.", "florence", "writing", "likely", "Anthology, Heptaplus publisher dedication and proem, extracted pp. 101-103.", 4),
    ("tl_074", "1491", None, "1491", "On Being and the One responds to Lorenzo/Poliziano discussion", "Pico frames On Being and the One as a compact answer to a discussion about whether the one is above being and whether Plato and Aristotle can be reconciled.", "florence", "writing", "likely", "Anthology, On Being and the One proem, extracted pp. 72-73.", 4),
    ("tl_075", "1495", None, "1495", "Pico's papers held at San Marco after his death", "Farmer reports that Pico's papers and books were apparently held at San Marco while Gianfrancesco Pico and Giovanni Mainardi transcribed them.", "san_marco_florence", "textual_transmission", "needs_review", "Farmer, Pico and Anti-Pico, extracted pp. 192-194.", 3),
    ("tl_076", "1496", None, "1496", "Disputationes enters Savonarolan anti-astrology conflict", "Farmer reads the posthumous publication and use of the Disputationes within Florentine political conflict over prophecy, astrology, and Savonarola's authority.", "florence", "reception", "likely", "Farmer, Pico and Anti-Pico, extracted pp. 190-194.", 4),
    ("tl_077", "1998", None, "1998", "Farmer makes textual-transmission risk central", "Farmer's Syncretism in the West argues that the 900 Conclusions require reliable edition, hidden-connection reconstruction, and caution about posthumously edited Pico texts.", None, "scholarship", "verified", "Farmer preface and chapter 4 readings.", 3),
]


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")


def load_seed_module():
    spec = importlib.util.spec_from_file_location("seed_research_artifacts", ROOT / "scripts" / "seed_research_artifacts.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load seed_research_artifacts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    for path, text in SOURCE_PACKETS.items():
        write(path, text)
    for path, text in WEBSITE_NOTES.items():
        write(path, text)

    conn = sqlite3.connect(DB)
    conn.executemany(
        """
        INSERT OR REPLACE INTO reading_artifacts
        (id, artifact_type, title, path, document_id, target_entity, status, evidence_status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT created_at FROM reading_artifacts WHERE id = ?), ?), ?)
        """,
        [row + (row[0], now, now) for row in ARTIFACT_ROWS],
    )
    conn.executemany(
        """
        INSERT OR REPLACE INTO claims
        (id, artifact_id, document_id, claim_text, claim_type, theme, target_entity, evidence_page, confidence, review_status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        CLAIMS,
    )
    conn.executemany(
        "INSERT OR REPLACE INTO website_cards(id, entity_type, title, subtitle, summary, status, source_artifact_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        CARDS,
    )
    conn.executemany(
        "INSERT OR REPLACE INTO website_pages(id, entity_type, title, markdown_path, status, source_artifact_id) VALUES (?, ?, ?, ?, ?, ?)",
        PAGES,
    )
    conn.executemany(
        """
        INSERT OR REPLACE INTO timeline_events
        (id, start_date, end_date, date_label, title, summary, location_id, category, evidence_status, source_note, importance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        TIMELINE_EVENTS,
    )
    conn.commit()

    seed = load_seed_module()
    seed.export_data(conn)
    seed.build_site(conn)
    conn.close()
    print("Study pass 003 complete.")


if __name__ == "__main__":
    main()
