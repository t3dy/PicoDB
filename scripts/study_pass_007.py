"""Study pass 007: longform Kabbalah synthesis essay."""

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
    "wirszubski": "Chaim_Wirszubski_Paul_Oskar_Kristeller_Pico_della_Mirandola_s_Encounter_with_Jewish_Mysticism_Ha_pdf_cd8c112f",
    "busi": "Giulio_Busi_Raphael_Ebgi_Giovanni_Pico_della_Mirandola_Mito_magia_Qabbalah_Einaudi_pdf_c382f352",
    "copenhaver_magic": "Brian_P_Copenhaver_Magic_and_the_Dignity_of_Man__Pico_della_Mirandola_and_His_Oration_in_Modern__pdf_f7f272e1",
    "copenhaver_trial": "Brian_P_Copenhaver_Pico_della_Mirandola_on_Trial__Heresy_Freedom_and_Philosophy_libgen_li_pdf_753eb1fa",
    "farmer": "Medieval_Renaissance_Texts_Studies_167_Stephen_A_Farmer_Giovanni_Pico_Della_Mirandola_Syncretism_pdf_c99b971b",
    "howlett": "Critical_Political_Theory_and_Radical_Practice_Sophia_Howlett_-_Re-evaluating_Pico__Aristotelian_pdf_3c6c4fa3",
    "edelheit": "Amos_Edelheit_Maynooth_University_-_A_Philosopher_at_the_Crossroads_Giovanni_Pico_Della_Mirandol_pdf_dd0f01e6",
    "dougherty": "M_V_Dougherty_Pico_della_Mirandola__New_Essays_libgen_li_pdf_78172345",
    "allen": "Studies_in_the_Platonism_of_Marsilio_Ficino_and_Giovanni_PicoMichael_J._B._AllenRoutledge1080299_epub_65585d05",
}


FILES = {
    "artifacts/historiography/kabbalah_scholar_synthesis_matrix.md": """# Historiography Node: Pico and Kabbalah Scholar Synthesis Matrix

- Artifact ID: `hist_kabbalah_scholar_synthesis`
- Type: historiography node
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Problem

PicoDB needs one synthetic map of how the major scholars govern Pico's Kabbalah. The point is not to average the scholars into a bland consensus. It is to keep their different virtues visible so future close readings can say which kind of claim is being made: source-critical, philological, doctrinal, magical, scholastic, juridical, reception-historical, or metaphysical.

## Scholar Positions

| Scholar | Main Value for Kabbalah | Position for PicoDB |
|---|---|---|
| Chaim Wirszubski | Source control, Hebrew dependence, Mithridates, Abulafia/Recanati, doctrinal precision. | No Kabbalah claim is mature unless it states source, translation witness, language dependence, Christianizing move, and confidence. |
| Giulio Busi | Qabbalah as praxis, correspondence, magic, symbolic inclusion, and Semitic canon expansion. | Kabbalah is an operation and an art of correspondences, not only a doctrine. |
| Brian P. Copenhaver | Anti-mythic Oration reading, magic, trial, theological danger, Latin precision. | Pico's Kabbalah belongs to ascetic mysticism, magic, and the heresy crisis, not modern dignity celebration. |
| Stephen A. Farmer | 900 Conclusions as thesis clusters, hidden connections, correlative systems, debate architecture. | Kabbalistic theses must be read as clustered debate nodes inside a larger syncretic machine. |
| Sophia Howlett | Three pillars and contested coherence: Aristotelianism, Platonism, Jewish Kabbalah. | Kabbalah is one of Pico's structural pillars and often marks where concord succeeds only by exposing difference. |
| Amos Edelheit | Renaissance scholasticism, formation, anti-reductive labels. | Kabbalah must not erase Pico's scholastic medium, university formation, or Latin theological technique. |
| M. V. Dougherty | Corpus breadth, edition status, genre, collaboration. | Kabbalah cannot be studied from the Oration alone; genre and edition status are required metadata. |
| Michael J. B. Allen | Ficino/Pico Platonism, Idea of Man, poetic theology, Heptaplus metaphysics. | Kabbalah in Heptaplus must be read beside Platonist, Ficinian, Dionysian, and Christological structures. |

## Synthesis Rule

For PicoDB, Kabbalah is a multi-register object:

- a Jewish source tradition mediated through Hebrew, Aramaic, and Latin translation;
- a Christianizing theological instrument;
- a magical and operational art;
- a thesis-cluster problem in the 900 Conclusions;
- a metaphysical and allegorical logic of correspondence;
- a source of doctrinal danger in the Roman crisis;
- a historiographical correction to Oration-only Pico;
- one pillar in the larger Aristotelian-Platonic-Kabbalistic structure of Pico's thought.

## Next Work

- Build a thesis-level Kabbalah table for the 900 Conclusions.
- Build a Mithridates witness table.
- Add Heptaplus Kabbalah test fields to every future Heptaplus section summary.
- Expand the longform Kabbalah essay into a 6,000-10,000 word reviewed article.
""",
    "artifacts/essays/pico_kabbalah_synthesis_longform_draft.md": """# Essay Draft: Pico's Kabbalah

- Artifact ID: `essay_pico_kabbalah_synthesis_draft`
- Target length: 6,000-10,000 words for the next full draft.
- Status: DRAFT
- Evidence status: SOURCE_ANCHORED_DRAFT

## Thesis

Pico's Kabbalah should be treated as one of the central engines of his mature project, but it must not be treated as a fog of exotic mysticism. The strongest scholarship in PicoDB points toward a more demanding synthesis. Wirszubski makes Pico's Kabbalah a recoverable philological and source-historical field. Busi makes it practical, magical, symbolic, and combinatory. Copenhaver places it inside the Oration's ascetic mysticism and the theological danger of the Roman trial. Farmer teaches us to read the Kabbalistic conclusions as compressed debate nodes inside the hidden architecture of the 900 Conclusions. Howlett makes Kabbalah one of the three pillars of Pico's intellectual world alongside Aristotelianism and Platonism. Edelheit warns that Kabbalah does not replace scholasticism as Pico's operating philosophical language. Dougherty keeps the whole corpus, genre, edition, and collaboration problem visible. Allen reminds us that Pico's biblical allegory and metaphysics, especially in the Heptaplus, also belong to Ficinian, Platonic, Dionysian, and Christological structures that must not be mislabeled as Kabbalah too quickly.

The resulting picture is sharper than any single slogan. Pico's Kabbalah is a Jewish source tradition mediated through Latin translation; a Christian apologetic instrument; a magical and theurgical practice; a hermeneutic of Scripture; a technique of names, letters, numbers, and correspondences; a contribution to concord; a source of heresy risk; and a later historiographical battleground. To read it well, PicoDB must ask not simply whether a passage is Kabbalistic, but what kind of Kabbalistic claim is being made and what evidence can bear it.

## 1. The Basic Historical Claim: Pico Invents Christian Kabbalah

The portal's starting point remains the Wirszubski line: Pico is the first major Christian thinker to make Jewish Kabbalah a deliberate instrument of Christian philosophy and theology. That does not mean he understood every Jewish source perfectly or that he encountered Kabbalah without mediation. It means that he made the encounter programmatic. In the 900 Conclusions, in the Oration, in the Apology, and in the afterlife of the Roman controversy, Kabbalah becomes part of the Christian intellectual project.

Pico's encounter was historically concrete. He studied Hebrew and Chaldean for the sake of Kabbalah, but his Kabbalistic reading depended heavily on Latin translations produced by Flavius Mithridates. That dependence is not a minor bibliographical footnote. It is the condition of the whole project. It means that every claim about Pico's Kabbalah has to pass through the problem of translation: what text, in what language, with what Hebrew or Aramaic terms preserved, explained, altered, or interpolated?

Wirszubski's contribution is therefore disciplinary. He forces us to slow down. Pico may cite or use Kabbalistic doctrine, but the database must ask whether the doctrine is Abulafian, Recanatian, Zoharic, sefirotic, divine-name, gematric, prophetic, magical, or uncertain. It must ask whether Hebrew letters or numbers are essential to the argument. It must ask whether Mithridates is a transparent translator, an explanatory mediator, a doctrinal adapter, or a risk of distortion. Without this source discipline, "Kabbalah" becomes a decorative label, exactly the thing the project is trying to avoid.

## 2. Mithridates: Infrastructure and Instability

Busi gives the Mithridates problem a vivid intellectual shape. Mithridates is not merely a pipeline from Jewish text to Christian reader. He is a learned convert, teacher, translator, provocateur, and unstable mediator. He expands Pico's humanist library into Hebrew, Aramaic, and Arabic materials. He also imposes his own idiosyncrasies on the material. This means that Pico's Kabbalah is already a collaborative and contested artifact before Pico uses it.

For PicoDB, Mithridates becomes an ontology problem. A source cannot simply be marked "Kabbalistic." It needs fields for witness, mediation, language dependence, interpolation risk, and confidence. A Kabbalistic thesis in the 900 Conclusions might depend on a Hebrew original, on Mithridates' Latin translation, on marginal explanation, on Pico's Christianizing inference, or on some combination of all four. Those are different kinds of evidence.

Mithridates also changes the meaning of Pico's intellectual ambition. Pico is not only adding Jewish material to a Latin scholastic and humanist library. He is extending the canon of wisdom. Busi's point about the Semitic expansion of humanist learning is crucial: Pico's concord is not merely Plato plus Aristotle plus Christianity. It tries to fold in Hebrew and Aramaic secrets, Arabic materials, and traditions that Latin humanists could not command without translators and teachers.

## 3. Kabbalah as Praxis, Not Ornament

Busi's strongest correction is that Pico's qabbalah is not only contemplative doctrine. It is also action. It belongs to magic, theurgy, ars combinatoria, prayer, divine names, and symbolic correspondences. The Kabbalah that matters for Pico is not just a set of propositions about divine structure. It promises a method, an operation, a way to ascend, combine, invoke, prove, and transform.

This matters especially for the Oration and 900 Conclusions. The Oration's famous opening can mislead if isolated from the later speech. Copenhaver already teaches that the Oration is not a modern manifesto of dignity. In the Kabbalah frame, it becomes a preface to an ascetic and mystical program in which philosophy, magic, and Kabbalah form the highest disciplines of transformation. Human indeterminacy is not enough. The human being must be purified, disciplined, and raised through increasingly powerful sciences. Kabbalah is not a side ornament at the end of the ladder. It is one of the disciplines that promises access to the deepest mysteries.

In the 900 Conclusions, the practical character becomes more explicit but also more difficult. Farmer warns that the theses were meant for oral debate. They are not transparent textbook paragraphs. The Kabbalistic conclusions are nodes in a debate machine. Some concern divine names, some Christology, some magic, some numerical or letter procedures, some cross-traditional confirmations. Busi helps us see them as operational; Farmer helps us refuse to read them in isolation.

## 4. Kabbalah and Christian Apologetics

Pico's Kabbalah is Christian Kabbalah. That phrase should be used carefully. It does not mean that Jewish Kabbalah secretly was Christian all along. It means that Pico selected, translated, interpreted, and redirected Jewish mystical materials so they could confirm Christian theology. Wirszubski's language of Christianizing transformation is indispensable here.

The most famous claim is that no science better proves the divinity of Christ than magic and Kabbalah. Whatever exact thesis cluster we attach this to, its significance is enormous. Pico is not merely saying that Kabbalah is compatible with Christianity. He is saying that it can function as proof, perhaps even as privileged proof, of Christian mysteries. This is why Copenhaver's trial-centered approach matters. A Kabbalistic claim is not an antiquarian curiosity when it enters the Roman controversy. It becomes a doctrinal risk.

The Roman case forces us to distinguish ambition from safety. Pico's apologetic strategy tries to expand Christian evidence by recruiting Jewish esoteric materials. But the same move invites suspicion. If Christian truth requires or is best proven by Kabbalah and magic, then the hierarchy of disciplines and authorities shifts. The papal commission did not simply dislike novelty. It confronted claims that blurred theology, magic, Jewish sources, and sacramental danger.

## 5. Kabbalah, Magic, and the Thirteen Conclusions

Copenhaver's *Pico on Trial* keeps the danger concrete. The trial is not a vague clash between freedom and repression. It is a technical theological proceeding in which terms matter. Pico's suspect claims touched the Eucharist, the descent of Christ into hell, the cross, magic, Kabbalah, and the limits of belief. Kabbalah is one part of that larger danger-field.

This is why PicoDB cannot split the "Kabbalah essay" from the "trial essay." Kabbalah became dangerous because it entered claims about Christian doctrine. It was not merely Jewish mysticism sitting beside scholastic theology; it was brought inside Christology and apologetics. When Pico treats Kabbalah as a route to Christian proof, he also makes translation, language, and esoteric interpretation bear theological weight.

The Kabbalah/magic link requires particular care. Some scholars, especially under older Yates-style influence, can over-magnify magic into the master key to Renaissance thought. Copenhaver and Farmer complicate this. Pico's magic is real and important, but it must be specified. Is the passage about natural magic, divine names, talismanic practice, letter-number operations, prophecy, angelic invocation, sacramental analogy, or metaphysical ascent? Busi's praxis model does not excuse vagueness; it increases the demand for classification.

## 6. The 900 Conclusions as a Kabbalistic Database Problem

Farmer's contribution may be the most important for implementing the website. The 900 Conclusions are already a database before we build one. They are numbered, clustered, cross-traditional, compressed, and designed for debate. Pico expected to reveal hidden connections in oral disputation. The Kabbalistic conclusions must therefore be represented as thesis records, not as a prose blur.

A thesis-level Kabbalah table should include:

- thesis number and Farmer numbering where applicable;
- source tradition;
- relevant Hebrew/Aramaic term;
- translation witness;
- Mithridates mediation status;
- doctrine class;
- operation or praxis field;
- Christianizing claim;
- linked non-Jewish traditions;
- related theses;
- doctrinal risk;
- confidence.

This would let PicoDB ask fine-grained questions. Which Kabbalistic claims are Christological? Which are magical? Which depend on divine names? Which correspond to sefirotic doctrine? Which are Abulafian or Recanatian? Which are primarily Pico's own transformations? Which reappear in the Oration, Apology, or Heptaplus? Which later scholars contest?

This is where Busi, Wirszubski, and Farmer meet. Wirszubski asks what the source is. Busi asks what the operation is. Farmer asks where the thesis sits in the hidden machine.

## 7. Howlett's Three-Pillar Pico

Howlett keeps the synthesis from becoming a Kabbalah-only Pico. Her framework is invaluable because she treats Kabbalah as one of three pillars: Aristotelianism, Platonism, and Jewish Kabbalism. The point is balance, not dilution. Kabbalah is central, but it is central inside a structure where Aristotle, Plato, scholastic theology, poetic theology, and biblical exegesis remain active.

This matters for concord. Pico's project does not simply dissolve every tradition into harmony. Howlett emphasizes that concord can reveal real differences. Kabbalah may confirm Christian doctrine in Pico's hands, but it also brings different metaphysical assumptions, language practices, and hermeneutic techniques into the system. The synthesis is productive because it is strained.

For future writing, every Kabbalah section should ask: does Kabbalah harmonize with the other pillars here, or does it expose tension? In the Oration, Kabbalah seems to crown the ascent. In the 900 Conclusions, it enters the disputational structure as proof, technique, and provocation. In the Heptaplus, it may underlie allegorical structures, but it competes with or blends into Platonist, Dionysian, biblical, and Christological frames.

## 8. Edelheit's Warning: Do Not Let Kabbalah Erase Scholasticism

Edelheit's warning is quiet but essential. The current scholarly turn to Pico's Kabbalah is necessary, but it can produce a new distortion if it replaces older Platonist or humanist reductions with a Kabbalist reduction. Pico's central language of philosophical and theological argument remained heavily scholastic. His formation in Padua and Paris, his school references, his Latin terminology, and his disputational technique do not vanish when he turns to Hebrew mysteries.

This has direct consequences for the ontology. A Kabbalistic claim may also be scholastic in form. It may appear as a thesis. It may be defended in the Apology through Latin technical distinctions. It may be dangerous because of how it interacts with Eucharistic, Christological, or metaphysical terms. The close reader must therefore tag both the Kabbalistic source and the scholastic argument form.

Edelheit also helps resist biography-as-magic. Pico was not simply a miraculous young syncretist who discovered Kabbalah and transcended ordinary intellectual categories. He was trained in scholastic habits of distinction, authority, contradiction, and disputation. Kabbalah enters that apparatus.

## 9. Dougherty's Corpus and Collaboration Rule

Dougherty gives the project an infrastructural discipline. Pico's Kabbalah cannot be reconstructed from one famous passage, one thesis, or one modern scholarly school. It requires the Oration, 900 Conclusions, Apology, Heptaplus, Commento, letters, later reception, editions, translations, and secondary scholarship. It also requires specialists: Hebrew/Kabbalah scholars, Latinists, historians of scholasticism, historians of magic, biblical hermeneutics scholars, and Renaissance Platonism scholars.

This is why the portal has to be a knowledge system, not just an essay collection. Kabbalah touches too many entities: texts, scholars, Hebrew sources, Latin translations, doctrines, practices, controversies, places, and reception events. A single essay can synthesize; the database must preserve the pieces.

Dougherty's rule also applies to edition status. The Commento has a complicated textual history. The Disputationes may carry posthumous risk. The 900 Conclusions require numbering systems and edition checks. The Heptaplus has translation and source-identification problems. Kabbalah claims must be attached to textual witnesses and not merely to convenient modern translations.

## 10. Allen's Boundary: Not Every Allegory Is Kabbalah

Allen is not primarily a Kabbalah scholar, but he is crucial for avoiding overreach. His readings of Pico and Ficino show how much of Pico's allegorical and metaphysical work belongs to Platonic, Neoplatonic, Ficinian, Dionysian, Orphic, and Christological contexts. This is especially important for the Heptaplus.

The Heptaplus is full of hidden wisdom, correspondences, worlds, allegorical layers, and biblical interpretation. Some of this may be Kabbalistic. Wirszubski argues that parts of the world-structure have Kabbalistic origin or significance. Busi's scale of correspondences also makes Kabbalistic and magical readings tempting. But Allen reminds us that mutual containment, the Idea of Man, Christological cosmology, and Platonic mythic exegesis can operate without every detail being specifically Kabbalah.

Therefore the Heptaplus rule should be strict: test for Kabbalah, do not assume it. A passage may be biblical allegory, Dionysian hierarchy, Platonist metaphysics, scholastic cosmology, Kabbalistic structure, or several at once. The database should allow multiple tags, but each tag needs evidence.

## 11. Copenhaver and the Anti-Dignity Correction

Copenhaver's work on modern memory matters because Pico's Kabbalah has often been obscured by the myth of the Oration as a manifesto of dignity. If the Oration is reduced to a few opening paragraphs about self-fashioning, Kabbalah appears as an embarrassing or exotic add-on. But if the Oration is read whole, as Copenhaver insists, Kabbalah belongs to the speech's ascetic and mystical trajectory.

The famous dignity passage is not false; it is incomplete when isolated. The human being is indeterminate and capable of ascent. But ascent requires disciplines, purgation, illumination, perfection, angelic imitation, theology, and the highest sciences. Kabbalah participates in that upper register. It belongs to the machinery of transformation.

Copenhaver also places Pico's Kabbalah in the history of fame. Modern Pico was often made useful by forgetting the parts of Pico that were too scholastic, too magical, too Kabbalistic, too theological, or too dangerous. The Kabbalah essay should therefore be a correction to modern Pico, not a decorative specialty chapter.

## 12. Toward a Working Taxonomy of Pico's Kabbalah

The synthesis suggests a working taxonomy:

1. Philological Kabbalah: Hebrew, Aramaic, names, letters, numbers, translation witnesses, Mithridates.
2. Doctrinal Kabbalah: sefirot, Eyn-Sof, angelology, creation, divine names, prophecy.
3. Magical Kabbalah: operations, theurgy, invocation, practical names, combinatory techniques.
4. Apologetic Kabbalah: confirmation of Christ, Trinity, incarnation, and Christian mysteries.
5. Hermeneutical Kabbalah: hidden Mosaic wisdom, biblical allegory, layered interpretation.
6. Concordist Kabbalah: links to Plato, Aristotle, Dionysius, Orphic hymns, Chaldean Oracles, Hermetica, Lull, scholastic theology.
7. Juridical Kabbalah: suspect propositions, Apology defenses, papal condemnation.
8. Historiographical Kabbalah: Scholem, Wirszubski, Idel, Busi, Copenhaver, Howlett, and the modern turn away from Oration-only Pico.

Every future close-reading note should locate its claim in this taxonomy. A claim can occupy more than one class, but it should not be left unclassified.

## 13. Open Problems

The most urgent open problem is the thesis-level Kabbalah table for the 900 Conclusions. Without it, the project risks writing fluent synthesis before it has enough granular control. The second problem is the Mithridates witness map: which translations, which source texts, which interpolations, and which marginal notes feed Pico's claims? The third is the Heptaplus boundary problem: which allegories are specifically Kabbalistic, which are Platonic or Dionysian, and which are Pico's own synthesis? The fourth is the relation between Kabbalah and magic: where does Pico describe operation, where doctrine, where proof, and where metaphor?

There is also a historiographical problem. Older scholarship sometimes magnified magic or Kabbalah into the secret of the Renaissance; other scholarship minimized it to preserve a rational, humanist, or scholastic Pico. The portal should do neither. Pico's Kabbalah is central, but central in a system where centrality does not mean exclusivity.

## 14. Working Conclusion

Pico's Kabbalah is best understood as disciplined audacity. It is disciplined because it depends on texts, languages, translations, doctrines, numbers, names, and arguments that can be studied. It is audacious because Pico uses those materials to expand Christian philosophy, prove Christian mysteries, raise magic to the upper levels of knowledge, and reorganize the map of ancient wisdom.

The scholars do not give us one flat consensus. They give us a method. Wirszubski says: identify the source and do not overclaim. Busi says: ask what the practice does. Copenhaver says: read the whole Oration and the trial danger. Farmer says: collate the theses. Howlett says: hold Kabbalah with Aristotle and Plato. Edelheit says: keep scholasticism visible. Dougherty says: control genre, edition, and corpus. Allen says: distinguish Kabbalah from Platonist and Christological allegory without severing their interactions.

The next full draft should become the portal's central article on Pico's Kabbalah. It should include a scholar-position matrix, a chronology of Pico's Hebrew/Kabbalah learning, a Mithridates translation appendix, a thesis-cluster table for the 900 Conclusions, a section on Kabbalah in the Oration and Apology, a cautious Heptaplus chapter, and a final historiographical map from Scholem and Wirszubski through Busi, Copenhaver, Idel, Howlett, and current Pico studies.
""",
}


ARTIFACT_ROWS = [
    ("hist_kabbalah_scholar_synthesis", "historiography_node", "Pico and Kabbalah Scholar Synthesis Matrix", "artifacts/historiography/kabbalah_scholar_synthesis_matrix.md", DOCS_BY_KEY["wirszubski"], "Pico Kabbalah historiography", "SOURCE_ANCHORED", "likely"),
    ("essay_pico_kabbalah_synthesis_draft", "website_page", "Pico's Kabbalah Longform Synthesis Draft", "artifacts/essays/pico_kabbalah_synthesis_longform_draft.md", DOCS_BY_KEY["wirszubski"], "Pico Kabbalah", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
]


CLAIMS = [
    ("claim_kabbalah_synth_001", "essay_pico_kabbalah_synthesis_draft", DOCS_BY_KEY["wirszubski"], "Pico's Kabbalah must be treated as a source-critical field requiring source tradition, language dependence, translation witness, Mithridates mediation, Christianizing move, and confidence.", "methodological", "Kabbalah", "Pico Kabbalah", "synthesis from Wirszubski", "high", "DRAFT", "Pass 007 Kabbalah synthesis."),
    ("claim_kabbalah_synth_002", "essay_pico_kabbalah_synthesis_draft", DOCS_BY_KEY["busi"], "Busi's contribution requires PicoDB to read qabbalah as praxis: operation, correspondence, magic, theurgy, symbolic inclusion, and combinatory technique.", "methodological", "qabbalah praxis", "Pico Kabbalah", "synthesis from Busi", "high", "DRAFT", "Pass 007 Kabbalah synthesis."),
    ("claim_kabbalah_synth_003", "essay_pico_kabbalah_synthesis_draft", DOCS_BY_KEY["copenhaver_magic"], "Copenhaver's anti-dignity correction makes Kabbalah part of the Oration's ascetic and mystical trajectory rather than an exotic add-on to modern human dignity.", "historiographical", "Oration", "Oration Kabbalah", "synthesis from Copenhaver", "high", "DRAFT", "Pass 007 Kabbalah synthesis."),
    ("claim_kabbalah_synth_004", "essay_pico_kabbalah_synthesis_draft", DOCS_BY_KEY["copenhaver_trial"], "Copenhaver's trial work makes Kabbalah a juridical and theological danger-field when it is used to prove or defend Christian mysteries.", "historiographical", "heresy", "Pico trial", "synthesis from Copenhaver", "high", "DRAFT", "Pass 007 Kabbalah synthesis."),
    ("claim_kabbalah_synth_005", "essay_pico_kabbalah_synthesis_draft", DOCS_BY_KEY["farmer"], "Farmer's thesis-cluster method requires Kabbalistic conclusions to be read as debate nodes inside the hidden architecture of the 900 Conclusions.", "methodological", "900 Conclusions", "Kabbalistic theses", "synthesis from Farmer", "high", "DRAFT", "Pass 007 Kabbalah synthesis."),
    ("claim_kabbalah_synth_006", "essay_pico_kabbalah_synthesis_draft", DOCS_BY_KEY["howlett"], "Howlett's three-pillar framework keeps Kabbalah central without letting it erase Aristotelianism and Platonism.", "historiographical", "three pillars", "Pico Kabbalah", "synthesis from Howlett", "high", "DRAFT", "Pass 007 Kabbalah synthesis."),
    ("claim_kabbalah_synth_007", "essay_pico_kabbalah_synthesis_draft", DOCS_BY_KEY["edelheit"], "Edelheit's scholasticism warning means Kabbalah claims must also preserve Pico's scholastic argument form, Latin terminology, and university formation context.", "methodological", "scholasticism", "Pico Kabbalah", "synthesis from Edelheit", "high", "DRAFT", "Pass 007 Kabbalah synthesis."),
    ("claim_kabbalah_synth_008", "essay_pico_kabbalah_synthesis_draft", DOCS_BY_KEY["allen"], "Allen's Platonism work warns that Heptaplus allegory must be tested for Kabbalistic evidence rather than automatically classified as Kabbalah.", "methodological", "Heptaplus", "Heptaplus Kabbalah", "synthesis from Allen", "high", "DRAFT", "Pass 007 Kabbalah synthesis."),
]


CARDS = [
    ("essay-pico-kabbalah-synthesis", "essay", "Pico's Kabbalah", "Longform scholar synthesis", "A new longform essay seed synthesizes Wirszubski, Busi, Copenhaver, Farmer, Howlett, Edelheit, Dougherty, and Allen into a working account of Pico's Kabbalah as source tradition, praxis, apologetics, magic, thesis system, and historiographical problem.", "DRAFT", "essay_pico_kabbalah_synthesis_draft"),
    ("hist-kabbalah-scholars", "historiography", "Kabbalah Scholar Matrix", "Who governs which claims", "A new synthesis matrix assigns each major scholar a role in future Kabbalah close readings: source control, praxis, trial danger, thesis clustering, three-pillar concord, scholastic form, corpus discipline, and Platonist boundary control.", "DRAFT", "hist_kabbalah_scholar_synthesis"),
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
    payload["version"] = "0.6.0"
    payload["kabbalah_synthesis_fields"] = [
        "scholar_position",
        "claim_register",
        "source_tradition",
        "translation_witness",
        "mithridates_mediation",
        "source_language_dependency",
        "doctrine_class",
        "praxis_operation",
        "christianizing_move",
        "magic_relation",
        "thesis_cluster",
        "scholastic_argument_form",
        "platonic_or_dionysian_boundary",
        "juridical_risk",
        "historiographical_stakes",
        "confidence",
    ]
    payload["kabbalah_taxonomy"] = [
        "philological_kabbalah",
        "doctrinal_kabbalah",
        "magical_kabbalah",
        "apologetic_kabbalah",
        "hermeneutical_kabbalah",
        "concordist_kabbalah",
        "juridical_kabbalah",
        "historiographical_kabbalah",
    ]
    payload["kabbalah_scholar_synthesis"] = {
        "Wirszubski": "source_control",
        "Busi": "praxis_and_correspondence",
        "Copenhaver": "oration_trial_and_danger",
        "Farmer": "thesis_cluster_architecture",
        "Howlett": "three_pillar_concord",
        "Edelheit": "scholastic_form_and_formation",
        "Dougherty": "corpus_genre_edition_collaboration",
        "Allen": "platonic_boundary_and_heptaplus_metaphysics",
    }
    write_json(path, payload)


def update_docs() -> None:
    append_once(
        DOCS / "KABBALAH_READING_PROTOCOL.md",
        "## Pass 007 Scholar Synthesis Overlay",
        """## Pass 007 Scholar Synthesis Overlay

Future Kabbalah notes must identify which scholar-governed register is active:

- Wirszubski: source, Hebrew dependence, Mithridates, doctrine, confidence.
- Busi: praxis, operation, correspondence, magic, symbolic inclusion.
- Copenhaver: Oration whole-text correction, trial danger, theological precision.
- Farmer: thesis clusters, hidden architecture, debate function.
- Howlett: three-pillar balance and concord failure/success.
- Edelheit: scholastic argument form and anti-reductive labeling.
- Dougherty: corpus, genre, edition, collaboration.
- Allen: Platonist, Ficinian, Dionysian, and Christological boundaries, especially in Heptaplus.
""",
    )


def main() -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    for path, text in FILES.items():
        write(path, text)
    update_docs()
    update_ontology()

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
    conn.commit()
    seed = load_seed_module()
    seed.export_data(conn)
    seed.build_site(conn)
    conn.close()
    print("Study pass 007 complete.")


if __name__ == "__main__":
    main()
