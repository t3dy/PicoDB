"""Study pass 011: Pico's angels and angelology."""

from __future__ import annotations

import importlib.util
import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "pico.db"
DATA = ROOT / "data"
DOCS = ROOT / "docs"

DOCS_BY_KEY = {
    "oration": "della_Mirandola_Pico__Borghesi_Francesco__Papio_Michael__Riva_Pico_della_Mirandola__Oration_on_t_pdf_2a7ee6ab",
    "heptaplus_english": "Heptaplus_Pico_della_Mirandola_On_the_Dignity_of_Man_Being_and_One_pdf_29945776",
    "heptaplus_black": "Studies_in_Medieval_and_Reformation_Traditions_66_Crofton_Black_-_Picos_Heptaplus_and_Biblical_H_pdf_98e6bcc6",
    "farmer": "Medieval_Renaissance_Texts_Studies_167_Stephen_A_Farmer_Giovanni_Pico_Della_Mirandola_Syncretism_pdf_c99b971b",
    "wirszubski": "Chaim_Wirszubski_Paul_Oskar_Kristeller_Pico_della_Mirandola_s_Encounter_with_Jewish_Mysticism_li_pdf_cd8c112f",
    "allen": "Studies_in_the_Platonism_of_Marsilio_Ficino_and_Giovanni_PicoMichael_J._B._AllenRoutledge1080299_epub_65585d05",
    "copenhaver": "Brian_P_Copenhaver_Magic_and_the_Dignity_of_Man__Pico_della_Mirandola_and_His_Oration_in_Modern__pdf_f7f272e1",
    "edelheit": "Amos_Edelheit_Maynooth_University_-_A_Philosopher_at_the_Crossroads_Giovanni_Pico_Della_Mirandol_pdf_dd0f01e6",
    "salas": "The_Thomist__A_Speculative_Quarterly_Review_2014_jul_1_vol_78_iss_3_Salas_Victor_M_Giovanni_Pico_pdf_7f997dd5",
}

FILES = {
    "docs/ANGELOLOGY_READING_PROTOCOL.md": """# Angelology Reading Protocol

Status: DRAFT  
Created in study pass 011.

## Purpose

Pico's angels must be read across anthropology, metaphysics, biblical hermeneutics, Kabbalah, and intellect theory. Do not treat "angel" as one flat tag. In Pico, angelic language can mean a created spiritual substance, an intelligible world, a Dionysian hierarchy, a Kabbalistic name/order, a model for human transformation, an Arabic/Aristotelian intellect problem, or a Ficinian/Neoplatonic hypostasis translated into Christian language.

## Required Fields

- pico_work: Oration, 900 Conclusions, Heptaplus, On Being and Unity, Commento, Apology, letters, reception text.
- angelology_register: imitation, hierarchy, separate_substance, angelic_mind, intelligible_world, kabbalistic_order, biblical_messenger, demon_daemon, active_intellect, grace_and_beatitude, Christological_access.
- source_family: Dionysian, Thomistic, Proclean, Plotinian, Ficinian, Arabic, Aristotelian, Kabbalistic, biblical, patristic, scholastic, Chaldean/Orphic.
- authority_named: Pseudo-Dionysius, Aquinas, Proclus, Plotinus, Ficino, Avicenna, Averroes, Al-Farabi, Ibn Bajja, Maimonides, Gersonides, Recanati, Abulafia, Michael, Metatron, Enoch, Lucifer, Seraphim, Cherubim, Thrones.
- metaphysical_level: God, first_created_mind, angelic/intellectual_world, celestial_world, sublunary_world, human_microcosm, soul, body.
- function_in_argument: ascent, mediation, correspondence, causation, knowledge, felicitas, exegesis, Kabbalistic proof, concord, correction_of_Ficino, theological_boundary.
- transformation_status: imitation, participation, elevation, union, grace_drawn, natural_limit, fall, deformation.
- textual_risk: primary passage, translation note, thesis reconstruction, Kabbalistic source mediation, posthumous edition, scholar inference.
- scholar_governor: Black, Wirszubski, Farmer, Allen, Copenhaver, Edelheit, Salas, Howlett, Busi.

## Style Rules

1. Distinguish angelic ontology from angelic imitation. The Oration asks humans to become angelic; the Heptaplus and Conclusions also discuss angelic/intellectual realities.
2. Separate "angelic mind," "intellect," "intellectual nature," "first created mind," and "separate substance" before deciding whether they are equivalent in a given passage.
3. When Kabbalah is involved, record Hebrew/Latin mediation and source witness. Do not treat Michael, Metatron, or angelic hierarchies as generic Christian angelology.
4. When Dionysius is involved, identify whether Pico uses hierarchy, anagogy, darkness, names, or angelic orders.
5. When Aquinas is involved, ask whether the passage concerns separate substances, beatitude, grace, created intellect, or the limits of natural knowledge.
6. When Proclus or Plotinus is involved, tag whether angelic language translates henads, intellect, intelligible world, or ascent beyond intellect.
7. When Ficino is involved, ask whether Pico is borrowing Ficinian Platonist architecture, correcting it, or replacing Soul/world-soul mediation with angelic/intellectual anthropology.
8. When Arabic metaphysics is involved, tag Active/Agent Intellect, conjunction, felicitas, prophecy, and whether Pico Christianizes or contests the philosophical model.
""",
    "artifacts/concepts/pico_angelology_taxonomy_pass011.md": """# Concept Dossier: Pico Angelology Taxonomy

- Artifact ID: `concept_pico_angelology_taxonomy`
- Type: concept dossier
- Status: SOURCE_ANCHORED_DRAFT
- Evidence status: likely

## Working Taxonomy

1. Angelic imitation: the Oration's call to become thrones, cherubim, and seraphim through discipline, knowledge, and love.
2. Angelic hierarchy: Dionysian and Kabbalistic ordering of angelic ranks, especially the ninefold problem.
3. Angelic/intellectual world: the highest created world in Heptaplus, called angelic by theologians and intelligible by philosophers.
4. Angelic mind / first created mind: flexible metaphysical language in the 900 Conclusions and related scholarship for intellect, angel, intellectual nature, or first created mind.
5. Kabbalistic angels: Metatron, Michael, mundane angels, six-winged angels, and Hebrew angelic names mediated by Mithridates, Recanati, Abulafia, Axelrad, and other sources.
6. Arabic intellect angelology: Active/Agent Intellect, separate intellects, conjunction, prophecy, and felicitas as a bridge between Arabic metaphysics and angelic anthropology.
7. Ficinian/Neoplatonic angels: Ficino's angelic intelligences, demons/daimons, and hypostatic structures as a source and foil for Pico.
8. Thomistic separate substances: Aquinas as a control for created intellect, angelic knowledge, grace, and limits of natural beatitude.
9. Christological access: Heptaplus on men and angels as made for true felicity, with grace drawing creatures beyond natural intellectual perfection.
10. Demonic boundary: demons/daimons must be separated from angels, especially when Ficinian and magical materials are in view.

## Use Rule

No future artifact should tag a passage simply as "angelology." It must choose a register, a source family, a metaphysical level, and a function in the argument.
""",
    "artifacts/source_packets/pico_angelology_source_map_pass011.md": """# Source Packet: Pico Angelology Source Map

- Artifact ID: `source_pico_angelology_map_pass011`
- Type: source packet
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Primary Loci

| Work | Angelological Material | Research Function |
|---|---|---|
| Oration | Man is not simply less than angels; the human vocation is plastic ascent into angelic and finally divine life. Seraphim, cherubim, and thrones become models for love, intelligence, and judgment. Enoch/Metatron supplies a Kabbalistic instance of transformation. | Anthropology as angelic imitation and ascent. |
| 900 Conclusions | Angelic/intellectual nature appears under many names: intellect, angelic mind, first created mind, Metatron, Pallas, intelligible sphere, Dionysian orders, Kabbalistic hierarchies, and sefirotic correlations. | Disputational metaphysics and source-correlation. |
| Heptaplus | The highest created world is angelic/intellectual; the tabernacle and Genesis order map the worlds; man participates in angelic mind; true felicity exceeds natural angelic self-knowledge and requires grace. | Biblical cosmology, anagogy, and grace. |
| On Being and Unity | Angelology is not always explicit, but the treatise's being/One problem is crucial for created intellect, Dionysian darkness, Thomistic transcendental language, and the correction of Ficino's Proclean Plato. | Metaphysical control language. |
| Commento | Ficinian, Platonic, and poetic-theological material raises problems of soul, intellect, desire, demons, and celestial mediation that must be kept near angelology without collapsing into it. | Boundary with Ficino and daemonology. |

## Scholarship Searched

| Scholar | Contribution |
|---|---|
| Black | Heptaplus as structured biblical hermeneutics: angelic/invisible world, anagogy, intellect, felicitas, Aquinas, Dionysius, Arabic and Jewish source ecologies. |
| Wirszubski | Kabbalistic source precision for angelic hierarchies, Michael, Metatron, mundane angels, and the three-world doctrine. |
| Farmer | Syncretic and correlative hierarchy in the 900 Conclusions; flexible naming of the first created mind as intellect, angel, angelic nature, Metatron, Pallas, and related symbols. |
| Allen | Ficino-Pico Platonism, Oration anthropology, Idea of Man, Proclean/Plotinian structures, and Pico's correction of Ficino. |
| Copenhaver | Oration structure: Adam's children must become angels; angelic ascent, Kabbalah, magic, and Dionysian darkness. |
| Edelheit and Salas | Scholastic and Thomistic controls for metaphysics, separate substances, being, unity, and theological boundaries. |

## Immediate Claims

- Pico's angelology is a hinge concept, not a subtopic. It joins anthropology, hierarchy, intellect, exegesis, Kabbalah, and grace.
- The Oration uses angels primarily as models and thresholds for human transformation.
- The 900 Conclusions use angelic language as part of a compressed metaphysical and Kabbalistic correlation machine.
- The Heptaplus converts angelology into biblical cosmology: the angelic world is both a world in itself and a register contained in man.
- Pico's strongest Christian move is not to make humans naturally equal to angels, but to say that both men and angels need grace for true felicity beyond natural intellectual perfection.
""",
    "artifacts/section_summaries/angelology/pico_angelology_passage_matrix_pass011.md": """# Passage Matrix: Pico's Angels and Angelology

- Artifact ID: `summary_pico_angelology_passage_matrix`
- Type: section summary
- Status: SOURCE_ANCHORED_DRAFT
- Evidence status: likely

## Oration

The Oration begins by asking why man is admirable if angels and heavenly choirs seem more admirable. Pico rejects a static answer based on centrality or microcosmic dignity. Man's excellence lies in indeterminacy and self-transformation. The positive transformation is angelic: human beings may rise into rational and angelic life and then beyond angelic order toward union with God. The angelic orders become a curriculum. Thrones signify judgment and stability; cherubim signify intelligence; seraphim signify burning love. Jacob's ladder then translates angelology into disciplines: moral philosophy purifies, dialectic orders reason, natural philosophy ascends through nature, theology brings peace, and higher magic/Kabbalah belongs to the later ascent. Enoch becoming Metatron supplies a Kabbalistic proof that human nature can be transformed into angelic/divine service.

## 900 Conclusions

The Conclusions make angelology more technical and more unstable. Farmer's reading requires collation across thesis clusters: first created mind, intellect, angelic mind, angelic nature, Metatron, Pallas, and intelligible sphere may belong to the same metaphysical problem-field without being identical in every context. Wirszubski identifies specific Kabbalistic angelology: Michael as celestial priest, nine angelic hierarchies named through Hebrew materials, mundane angels who appear to humans, and six-winged angels. The key rule is source control. A thesis about angelic hierarchy may be Dionysian in number, Kabbalistic in names, Proclean in hierarchical metaphysics, and Pico's own in the act of correlation.

## Heptaplus

The Heptaplus makes the angelic world part of Genesis hermeneutics. The highest world is called angelic by theologians and intelligible by philosophers. The three-world scheme is angelic/intellectual, celestial, and sublunary; man is the fourth or lesser world containing all three. Pico's tabernacle imagery maps common lower world, celestial holy place, and angelic holy of holies. The angelic world is the fountain of knowledge; in the human body it corresponds to the head and brain. The work also makes a decisive theological move in the seventh exposition: natural felicity gives each nature its own perfection, so angels know God in themselves as their substance manifests him. True felicity is higher. Men and angels are made for it, but neither achieves it by natural power; grace draws them toward God.

## On Being and Unity

On Being and Unity matters indirectly but strongly. Pico's angelology depends on how created being participates in divine unity. Aquinas supplies the language of being, unity, created participation, and the limits of created intellect. Dionysius supplies darkness, hierarchy, and supereminent divine transcendence. Allen's Ficino frame shows that Pico is policing Proclean metaphysics rather than abandoning Platonism. Angelology therefore belongs to the same problem as the convertibility of being and one: can the highest created intellect be affirmed without making the One beyond being into a non-Christian principle?

## Commento and Ficinian Boundary

The Commento and Ficinian Platonism add the boundary with demons, soul, desire, and celestial mediation. Ficino's world includes angelic intelligences, demons/daimons, World Soul, spiritus, and mathematical/celestial mediation. Pico shares this Neoplatonic atmosphere but redirects it. His angelology is less a demonological science and more an anthropology of ascent, a metaphysics of intellect, and a biblical/Kabbalistic correlation system.
""",
    "artifacts/historiography/pico_angelology_scholar_matrix.md": """# Historiography Node: Pico Angelology Scholar Matrix

- Artifact ID: `hist_pico_angelology_scholar_matrix`
- Type: historiography node
- Status: SOURCE_ANCHORED
- Evidence status: likely

| Scholar | Governing Value | PicoDB Rule |
|---|---|---|
| Crofton Black | Heptaplus structure, angelic/invisible world, anagogy, intellect, felicitas, Aquinas, Dionysius, Arabic and Jewish sources. | Heptaplus angelology must be read as biblical hermeneutics and ascent, not decorative cosmology. |
| Chaim Wirszubski | Philological source control for Kabbalistic angelology. | For Michael, Metatron, angelic hierarchies, mundane angels, and Hebrew names, record the translation witness and source chain. |
| Stephen Farmer | Correlative hierarchy and thesis collation in the 900 Conclusions. | Do not isolate one angel thesis; collate angel, intellect, first created mind, Metatron, Pallas, henads, and sefirot clusters. |
| Michael J. B. Allen | Ficino-Pico Platonism, Idea of Man, Proclean and Plotinian source architecture. | Ask whether angelic language is Pico borrowing Ficino, correcting Ficino, or translating Neoplatonic hypostasis into Christian anthropology. |
| Brian Copenhaver | Oration structure, angelic transformation, Kabbalah, magic, Dionysian darkness, modern-memory correction. | Read the Oration as a disciplined ascent speech, not a secular dignity manifesto. |
| Amos Edelheit | Scholastic theological formation and anti-reductive method. | Angelology must be checked against scholastic theology, not read as pure Platonism or pure Kabbalah. |
| Victor Salas | Thomistic solution to On Being and Unity. | Use Aquinas for being, unity, created participation, separate substances, and limits of created intellect. |

## Synthesis

The scholarship does not give a single "Pico on angels" doctrine. It gives a method: keep registers distinct, collate across works, and let angelology expose Pico's whole intellectual machine. Angels are models of human transformation, names for created intellects, ranks in Dionysian and Kabbalistic hierarchy, mediators in biblical cosmology, and test cases for whether Platonist metaphysics can be Christianized.
""",
    "artifacts/essays/pico_angels_angelology_synthesis_draft.md": """# Essay Draft: Pico's Angels and Angelology

- Artifact ID: `essay_pico_angels_angelology`
- Status: DRAFT
- Evidence status: SOURCE_ANCHORED_DRAFT

## Thesis

Pico's angelology is not a small doctrine about heavenly beings. It is one of the best ways to see how his whole system works. Angels appear where anthropology becomes metaphysics, where biblical exegesis becomes ascent, where Kabbalah enters Christian theology, where Dionysian hierarchy meets Proclean and Plotinian intellect, where Aquinas controls the limits of created knowledge, where Ficino's Platonism becomes both resource and foil, and where Arabic theories of separate intellects and felicitas press against Christian grace. To collect Pico's writings on angels is therefore to collect the hinges of his thought.

The first hinge is the Oration. Pico begins with a deliberately unstable question: why should man be admired if angels and the heavenly choirs seem more admirable? The obvious older answers are not enough. Man is a microcosm, an interpreter of nature, a middle being between time and eternity, and only slightly lower than angels. But Pico says those are not the principal grounds of admiration. The principal ground is that man has no fixed place, form, or gift. He can descend into plant and beast; he can rise into rational and angelic life; and he can be drawn still higher toward union with God. The comparison with angels is not ornamental. It is the pressure that forces Pico to define human dignity as vocation rather than possession.

This means that the Oration's angelology is first a discipline of imitation. Seraphim, cherubim, and thrones become models for the philosophical life. The seraph burns with love; the cherub shines with intelligence; the throne sits in stable judgment. Pico turns the hierarchy into an ascetic curriculum. Moral philosophy cleanses the soul's lower powers. Dialectic orders reason. Natural philosophy follows the ladder of nature upward through multiplicity. Theology gives peace. The higher disciplines of magic and Kabbalah, in the later movement of the speech, intensify this ascent toward divine union. Angelic orders are not merely described; they are enacted as stages of human conversion.

The Oration also adds a Kabbalistic transformation scene: Enoch becomes Metatron. This matters because Pico's examples of mutability are otherwise dangerous or ambiguous. Humans can deform themselves into brutes or plants; Proteus-like change can mean instability rather than glory. Enoch/Metatron supplies the positive version: human nature can be lifted into angelic service. Copenhaver's correction of the modern Oration myth is crucial here. This is not secular self-fashioning. It is a risky, hierarchical, mystical anthropology. Freedom matters because it can become angelic and then pass beyond angelic imitation into divine darkness.

The second hinge is the 900 Conclusions, where angelology becomes technical and difficult. Farmer's method is indispensable: individual theses must be collated across clusters. Pico uses many names for the upper created level: intellect, angel, angelic mind, angelic nature, first created mind, paternal mind, intelligible sphere, Metatron, Pallas, and sometimes symbols drawn from prisci, Pythagorean materials, Proclean henads, and Kabbalistic sefirot. These are not casual synonyms. They are attempts to map a highest created intellectual order across several traditions at once.

That mapping creates both power and danger. Dionysian angelic orders can be correlated with Proclean henads. Kabbalistic sefirot can be brought into relation with Neoplatonic hierarchy. Metatron can be correlated with illuminating intellect. The first created mind can look Platonic, Christian, Kabbalistic, or Arabic depending on the thesis cluster. Farmer's lesson is that Pico's angelology is correlative: it looks for structural agreements across traditions, then uses those agreements to build a disputational machine. The danger is over-harmonization. A database note must therefore ask: is Pico claiming identity, analogy, correspondence, hierarchy, or merely debate-worthy proximity?

Wirszubski gives the strongest controls for the Kabbalistic side. He shows that Pico's angelic material is not generic exoticism. The thesis on Michael as celestial priest draws on specific Jewish sources: Michael is the high priest above and sacrifices the souls of the just. The thesis on nine angelic hierarchies names Cherubim, Seraphim, Hasmalim, Haiot, Aralim, Tarsisim, Ophanim, Tephsarim, and Isim, and Wirszubski traces its unusual number and forms through Abraham Axelrad's Corona Nominis Boni and related materials. The significance is double. Pico aligns the number nine with Dionysius, but the names and source-path are Kabbalistic. The conclusion is Pico's own Christian correlation, not a simple borrowing from one source.

Other Kabbalistic angel theses sharpen the point. "Mundane angels" who appear to humans are linked by Wirszubski to Recanati and ultimately to Zoharic exegesis of Genesis. A thesis on a six-winged angel depends on another specific Jewish source chain. Michael and Gabriel can be read as right and left, water and fire, harmonized by divine peace. These angelic materials are exegetical, cosmological, and ritual at once. They help Pico read Scripture, correlate upper and lower worlds, and place Christian mysteries inside Hebrew secret theology. The ontology must therefore treat "Kabbalistic angelology" as a source-controlled register with names, witnesses, operations, and Christianizing moves.

The third hinge is the Heptaplus. Here angels are no longer mainly the rhetorical pressure of the Oration or the thesis clusters of the Conclusions. They become part of a biblical cosmology. Pico's second proem gives the classic structure: the ancients imagined three worlds. The highest is called angelic by theologians and intelligible by philosophers. Beneath it is the celestial world. Beneath that is the sublunary world. Man is a fourth, lesser world because he contains all three in himself. He has bodily elements, vegetative life, animal sense, celestial reason, participation in angelic mind, and the image of God.

This is where Black's Heptaplus is indispensable. The angelic world is not a decorative layer; it is part of the work's theory of interpretation. Genesis can speak across worlds because the worlds correspond. The tabernacle becomes a visible map: the common lower part corresponds to the world of animals and men; the golden middle corresponds to the planets; the holy of holies with cherubim corresponds to the supercelestial dwelling of angels. When Christ's death tears the temple veil, the closed access to the angelic holy of holies is reopened. Angelology becomes Christological access.

The Heptaplus also makes angelology epistemological. The highest part of the world, angelic or intellectual, is the fountain of knowledge. In the great-man analogy, the world corresponds to the human body: head and brain signify knowledge, heart signifies life and motion, generative parts signify lower generation. Man contains the angelic order as mind. This explains why the Oration's angelic imitation is not merely moral exhortation. The human being can imitate angels because the human microcosm already participates in angelic mind.

But Pico does not let natural angelic perfection become final beatitude. This is the fourth hinge and the most Christian one. In the Heptaplus, angels are the highest creatures because of their noble substance and their nearness to their end. Philosophers call them minds and intellects and say they know God. Pico accepts this as natural felicity, but only within limits. Angels naturally know God insofar as God is manifested in their own substance. That is not yet knowing God in God. True felicity carries creatures back to the contemplation of God's face and perfect union with the beginning from which they sprang. Men and angels are made for that felicity, but neither achieves it by natural power. Grace draws them.

This point lets Aquinas enter the essay with real force. Pico's angels are not just Neoplatonic intellects. They are created substances whose knowledge and perfection have limits. Aquinas gives Pico tools for distinguishing natural from supernatural beatitude, created intellect from divine essence, participation from identity, and grace from natural ascent. Salas and Edelheit help keep this scholastic control in view. Pico's angelology may use Proclus, Dionysius, Kabbalah, and Arabic metaphysics, but it is not allowed to erase the Christian boundary between created intellect and God.

Dionysius works differently. Dionysius gives Pico hierarchy, anagogy, darkness, and the prestige of Christian Neoplatonism. In the Oration, the movement through angelic orders leads into the Father's darkness. In the Heptaplus, symbols and worlds lead the reader upward. In the Conclusions, Dionysian ninefold hierarchy can be correlated with Kabbalistic angel names and Proclean structures. Dionysius therefore authorizes a Christian use of hierarchy while also keeping ascent apophatic: the goal is beyond the images and names through which the mind rises.

Proclus and Plotinus supply the deeper metaphysical architecture. Plotinus gives a model of One, Intellect, Soul, and return; Proclus elaborates hierarchy, henads, and a more crowded metaphysical mediation. Pico's angelic/intellectual world can be read as the Christianized translation of this post-Plotinian problem. The first created mind, the intelligible sphere, and the angelic mind all mark the same pressure: how can the highest created intellectual level mediate multiplicity without compromising divine simplicity? Farmer and Allen both make clear that Pico is working in a Neoplatonic field, but not passively. He recodes it through scholastic, Christian, Kabbalistic, and disputational forms.

Ficino is therefore both source and foil. Ficino's Platonic Theology places soul between body and angelic intelligences, and his broader Platonism includes World Soul, spiritus, demons, celestial mediation, and the hierarchy of minds. Pico learns much from this world. Yet Allen's work warns against treating him as a Ficinian satellite. Pico's Oration makes the human vocation more sharply transformative and exceptional. On Being and Unity corrects Ficino's Proclean reading of Plato by forcing the One/being problem through Aristotelian and Thomistic language. The angelic question belongs inside that dispute: is the upper intelligible order a Ficinian-Platonic mediation system, or a created order disciplined by Christian metaphysics?

Arabic metaphysics adds another necessary register. Copenhaver and Black point toward the Arabic and Jewish philosophical field around Agent Intellect, conjunction, prophecy, and felicitas. Avicenna, Averroes, Al-Farabi, Ibn Bajja, Maimonides, Gersonides, and the Hebrew transmission around Elia del Medigo all matter because they turn intellect into a theory of human perfection. If supreme happiness is conjunction with a separate intellect, then angelology and noetics overlap. Pico's texts repeatedly stand near this problem. But the Heptaplus converts it: natural conjunction or intellectual perfection is not enough for true felicity. Grace draws men and angels beyond self-contained intellectual perfection toward God in God.

This is why Pico's angelology cannot be filed under one tradition. It is Dionysian when it orders ascent through hierarchies and darkness. It is Thomistic when it distinguishes created intellect, natural beatitude, and grace. It is Proclean when it correlates hierarchies, henads, and levels of mediation. It is Plotinian when it thinks through intellect, return, and union. It is Ficinian when it borrows the language and architecture of Renaissance Platonism. It is anti-Ficinian or post-Ficinian when it corrects that architecture through Aristotle, Aquinas, and Christian doctrine. It is Arabic when separate intellect and felicitas govern the question of perfection. It is Kabbalistic when Metatron, Michael, angelic names, mundane angels, and Hebrew source chains become evidence for Christian mysteries.

The central conclusion is simple but demanding: angels are Pico's test case for concord. If concord means flattening differences, angelology fails. Dionysian orders, Kabbalistic names, Proclean henads, Ficinian intelligences, Arabic intellects, and Thomistic separate substances are not the same thing. But if concord means disciplined comparison across levels, then angelology is one of Pico's most successful laboratories. Angels let him ask how created intellect participates in God, how humans may become higher than their given condition, how Scripture hides metaphysics, how traditions can be correlated without losing their texture, and why grace remains necessary even at the summit of created being.

For PicoDB, the next reading pass should build a row for every angelological locus. Each row should record the exact work, passage, source family, angelic register, metaphysical level, function in argument, scholar governor, and open problem. The essay should then grow from this matrix into separate pages on Oration angelic ascent, Heptaplus angelic world, Kabbalistic angelology in the 900 Conclusions, and Arabic intellect/angelology.
""",
}

ARTIFACT_ROWS = [
    ("concept_pico_angelology_taxonomy", "concept_dossier", "Pico Angelology Taxonomy", "artifacts/concepts/pico_angelology_taxonomy_pass011.md", DOCS_BY_KEY["oration"], "Pico angelology", "SOURCE_ANCHORED_DRAFT", "likely"),
    ("source_pico_angelology_map_pass011", "source_packet", "Pico Angelology Source Map", "artifacts/source_packets/pico_angelology_source_map_pass011.md", DOCS_BY_KEY["oration"], "Pico angelology", "SOURCE_ANCHORED", "likely"),
    ("summary_pico_angelology_passage_matrix", "section_summary", "Pico Angelology Passage Matrix", "artifacts/section_summaries/angelology/pico_angelology_passage_matrix_pass011.md", DOCS_BY_KEY["heptaplus_english"], "Pico angelology", "SOURCE_ANCHORED_DRAFT", "likely"),
    ("hist_pico_angelology_scholar_matrix", "historiography_node", "Pico Angelology Scholar Matrix", "artifacts/historiography/pico_angelology_scholar_matrix.md", DOCS_BY_KEY["heptaplus_black"], "Pico angelology scholarship", "SOURCE_ANCHORED", "likely"),
    ("essay_pico_angels_angelology", "website_page", "Pico's Angels and Angelology", "artifacts/essays/pico_angels_angelology_synthesis_draft.md", DOCS_BY_KEY["oration"], "Pico angelology", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
]

CLAIMS = [
    ("claim_angelology_011_001", "essay_pico_angels_angelology", DOCS_BY_KEY["oration"], "The Oration uses angels to define human dignity as a vocation of ascent rather than a fixed possession.", "interpretive", "angelology", "Oration", "Oration opening and angelic ascent", "high", "DRAFT", "Pass 011."),
    ("claim_angelology_011_002", "summary_pico_angelology_passage_matrix", DOCS_BY_KEY["oration"], "Seraphim, cherubim, and thrones function as a philosophical curriculum of love, intelligence, and judgment.", "interpretive", "angelic imitation", "Oration", "Oration angelic orders", "high", "DRAFT", "Pass 011."),
    ("claim_angelology_011_003", "essay_pico_angels_angelology", DOCS_BY_KEY["wirszubski"], "Wirszubski shows that Pico's Kabbalistic angelology requires source-level control for Michael, Metatron, nine angelic hierarchies, mundane angels, and Hebrew names.", "philological", "Kabbalah", "900 Conclusions", "Wirszubski angelology chapters", "high", "DRAFT", "Pass 011."),
    ("claim_angelology_011_004", "essay_pico_angels_angelology", DOCS_BY_KEY["farmer"], "Farmer's thesis collation shows that angel, intellect, angelic mind, first created mind, Metatron, Pallas, henads, and sefirot belong to a correlative metaphysical problem-field in Pico.", "interpretive", "900 Conclusions", "Pico angelology", "Farmer hierarchy and subject index", "high", "DRAFT", "Pass 011."),
    ("claim_angelology_011_005", "essay_pico_angels_angelology", DOCS_BY_KEY["heptaplus_english"], "The Heptaplus identifies the highest created world as angelic or intellectual and makes it the fountain of knowledge in the world/man correspondence.", "interpretive", "Heptaplus", "angelic world", "Heptaplus second proem and fifth exposition", "high", "DRAFT", "Pass 011."),
    ("claim_angelology_011_006", "essay_pico_angels_angelology", DOCS_BY_KEY["heptaplus_english"], "The Heptaplus distinguishes natural felicity from true felicity: men and angels are made for union with God, but both require grace beyond natural intellectual perfection.", "theological", "felicitas", "men and angels", "Heptaplus seventh exposition", "high", "DRAFT", "Pass 011."),
    ("claim_angelology_011_007", "hist_pico_angelology_scholar_matrix", DOCS_BY_KEY["allen"], "Allen's Ficino-Pico frame requires reading angelic and intellectual language as shared Platonist architecture that Pico selectively corrects rather than merely inherits.", "historiographical", "Ficino", "Pico angelology", "Allen synthesis", "medium", "DRAFT", "Pass 011."),
    ("claim_angelology_011_008", "concept_pico_angelology_taxonomy", DOCS_BY_KEY["heptaplus_black"], "Future angelology artifacts must separate imitation, hierarchy, separate substance, angelic mind, intelligible world, Kabbalistic order, daemonology, Arabic intellect, and grace.", "methodological", "ontology", "Pico angelology", "Pass 011 taxonomy", "high", "DRAFT", "Pass 011."),
]

CARDS = [
    ("essay-pico-angels-angelology", "essay", "Pico's Angels and Angelology", "Angelic ascent, intellect, hierarchy, and grace", "A new synthesis essay collects Pico's angelological materials across the Oration, 900 Conclusions, Heptaplus, Ficino, Dionysius, Aquinas, Proclus, Plotinus, Kabbalah, and Arabic intellect theory.", "DRAFT", "essay_pico_angels_angelology"),
    ("concept-pico-angelology-taxonomy", "concept", "Angelology Taxonomy", "Do not tag angelology alone", "PicoDB now separates angelic imitation, hierarchy, angelic mind, intelligible world, Kabbalistic angels, Arabic intellect, Thomistic separate substances, and grace.", "DRAFT", "concept_pico_angelology_taxonomy"),
    ("source-pico-angelology-map", "source_packet", "Angelology Source Map", "Primary loci and scholarship", "A new source map identifies angelological loci in the Oration, 900 Conclusions, Heptaplus, On Being and Unity, Commento, and the major scholarship.", "DRAFT", "source_pico_angelology_map_pass011"),
    ("hist-pico-angelology-scholars", "historiography", "Angelology Scholar Matrix", "Black, Wirszubski, Farmer, Allen, Copenhaver", "A new matrix assigns guide roles for Pico's angelology: Heptaplus structure, Kabbalistic source control, thesis collation, Ficino-Pico Platonism, and Oration myth correction.", "DRAFT", "hist_pico_angelology_scholar_matrix"),
]


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")


def append_once(path: Path, marker: str, text: str) -> None:
    original = path.read_text(encoding="utf-8")
    if marker not in original:
        path.write_text(original.rstrip() + "\n\n" + text.strip() + "\n", encoding="utf-8", newline="\n")


def load_seed_module():
    spec = importlib.util.spec_from_file_location("seed_research_artifacts", ROOT / "scripts" / "seed_research_artifacts.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load seed_research_artifacts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def update_ontology() -> None:
    path = DATA / "reading_artifact_ontology.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version"] = "0.10.0"
    payload["angelology_reading_fields"] = [
        "pico_work",
        "angelology_register",
        "source_family",
        "authority_named",
        "metaphysical_level",
        "function_in_argument",
        "transformation_status",
        "textual_risk",
        "scholar_governor",
        "confidence",
    ]
    payload["angelology_taxonomy"] = [
        "angelic_imitation",
        "angelic_hierarchy",
        "angelic_intellectual_world",
        "angelic_mind_first_created_mind",
        "kabbalistic_angels",
        "arabic_intellect_angelology",
        "ficinian_neoplatonic_angels",
        "thomistic_separate_substances",
        "christological_access",
        "demonic_boundary",
    ]
    payload["angelology_scholar_synthesis"] = {
        "Black": "heptaplus_structure_angelic_world_anagogy_felicitas",
        "Wirszubski": "kabbalistic_angelology_source_control",
        "Farmer": "900_conclusions_correlative_hierarchy_and_thesis_collation",
        "Allen": "ficino_pico_platonism_and_neoplatonic_architecture",
        "Copenhaver": "oration_angelic_transformation_and_dionysian_darkness",
        "Edelheit": "scholastic_theological_controls",
        "Salas": "thomistic_being_unity_and_created_intellect",
    }
    payload.setdefault("guide_scholars", {})
    payload["guide_scholars"]["Black"] = sorted(set(payload["guide_scholars"].get("Black", []) + ["angelic_world", "heptaplus_angelology", "felicitas_and_grace"]))
    payload["guide_scholars"]["Wirszubski"] = sorted(set(payload["guide_scholars"].get("Wirszubski", []) + ["kabbalistic_angelology", "Metatron", "Michael", "angelic_hierarchies"]))
    payload["guide_scholars"]["Farmer"] = sorted(set(payload["guide_scholars"].get("Farmer", []) + ["angelic_mind", "first_created_mind", "correlative_hierarchy"]))
    payload["guide_scholars"]["Allen"] = sorted(set(payload["guide_scholars"].get("Allen", []) + ["ficino_angelic_intelligences", "neoplatonic_hypostasis", "Idea_of_Man"]))
    payload["guide_scholars"]["Copenhaver"] = sorted(set(payload["guide_scholars"].get("Copenhaver", []) + ["oration_angelic_ascent", "Dionysian_darkness", "Metatron_in_Oration"]))
    write_json(path, payload)


def refresh_catalog_and_manifest(conn: sqlite3.Connection) -> None:
    conn.row_factory = sqlite3.Row
    docs = []
    for row in conn.execute(
        "SELECT id,title,source_file,markdown_path,document_type,themes_json,pico_works_json,page_count,word_count,duplicate_of FROM documents ORDER BY title"
    ):
        d = dict(row)
        d["themes"] = json.loads(d.pop("themes_json") or "[]")
        d["pico_works_discussed"] = json.loads(d.pop("pico_works_json") or "[]")
        docs.append(d)
    write_json(DATA / "corpus_catalog.json", {"documents": docs})
    manifest_path = DATA / "pico_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["corpus_counts"] = {
        "documents": conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0],
        "pages": conn.execute("SELECT COUNT(*) FROM pages").fetchone()[0],
        "sections": conn.execute("SELECT COUNT(*) FROM sections").fetchone()[0],
        "words": conn.execute("SELECT COALESCE(SUM(word_count), 0) FROM documents").fetchone()[0],
    }
    write_json(manifest_path, manifest)


def update_docs() -> None:
    append_once(
        DOCS / "SECTION_SUMMARY_STYLE_GUIDE.md",
        "## Pass 011 Angelology Overlay",
        """## Pass 011 Angelology Overlay

When summarizing angelology passages, identify the angelology register, source family, authority named, metaphysical level, function in the argument, transformation status, and textual risk. Do not use "angelology" as a naked tag. Separate angelic imitation, angelic hierarchy, angelic/intellectual world, angelic mind, Kabbalistic angels, Arabic intellect, Ficinian/Neoplatonic mediation, Thomistic separate substances, Christological access, and demonic boundary questions. See `docs/ANGELOLOGY_READING_PROTOCOL.md`.
""",
    )
    append_once(
        DOCS / "PICO_TEXT_GAPS.md",
        "## Angelology Primary Text Control Pass 011",
        """## Angelology Primary Text Control Pass 011

- Status: `primary_loci_identified_passage_table_needed`
- Reason: Oration and Heptaplus primary passages are locally available, and Farmer/Wirszubski/Black/Copenhaver/Allen give strong scholarly controls. The project still needs a thesis-by-thesis angelology table for the 900 Conclusions, especially for Michael, Metatron, mundane angels, six-winged angels, Dionysian hierarchy, first created mind, angelic intellect, and Arabic Active Intellect/conjunction claims.
""",
    )


def main() -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    for path, text in FILES.items():
        write(path, text)
    update_ontology()
    update_docs()

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
    conn.execute(
        """
        INSERT OR REPLACE INTO website_pages(id, entity_type, title, markdown_path, status, source_artifact_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        ("page-pico-angels-angelology", "essay", "Pico's Angels and Angelology", "artifacts/essays/pico_angels_angelology_synthesis_draft.md", "DRAFT", "essay_pico_angels_angelology"),
    )
    conn.commit()
    refresh_catalog_and_manifest(conn)
    seed = load_seed_module()
    seed.export_data(conn)
    seed.build_site(conn)
    conn.close()
    print("Study pass 011 complete.")


if __name__ == "__main__":
    main()
