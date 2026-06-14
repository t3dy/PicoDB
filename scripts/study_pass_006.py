"""Study pass 006: Michael J. B. Allen and the Pico-Ficino dispute."""

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

ALLEN_VOL = "Studies_in_the_Platonism_of_Marsilio_Ficino_and_Giovanni_PicoMichael_J._B._AllenRoutledge1080299_epub_65585d05"
DOUGHERTY = "M_V_Dougherty_Pico_della_Mirandola__New_Essays_libgen_li_pdf_78172345"
ANTHOLOGY = "Heptaplus_Pico_della_Mirandola_On_the_Dignity_of_Man_Being_and_One_pdf_29945776"
FARMER = "Medieval_Renaissance_Texts_Studies_167_Stephen_A_Farmer_Giovanni_Pico_Della_Mirandola_Syncretism_pdf_c99b971b"


FILES = {
    "docs/FICINO_PICO_READING_PROTOCOL.md": """# Ficino-Pico Reading Protocol

Michael J. B. Allen now governs PicoDB's readings of Pico's relationship to Ficino. The relation is not reducible to influence, discipleship, rivalry, or rejection. It is a technical field of shared Platonism, selective borrowing, pointed disagreement, and competing Christian uses of Neoplatonic metaphysics.

## Core Rule

When Pico touches Ficino, ask which level of the dispute is active:

| Level | Question |
|---|---|
| Personal network | Is Pico addressing Ficino, receiving correction, praising him, or being protected by him? |
| Textual history | Is the evidence affected by draft, marginalia, suppression, expurgation, edition, or later reprinting? |
| Platonic exegesis | Which Platonic dialogue is being interpreted: Symposium, Phaedrus, Timaeus, Parmenides, Sophist, Philebus, Protagoras, Republic? |
| Neoplatonic architecture | Which hypostasis or metaphysical structure is at stake: One, Mind, Soul, Ideas, World Soul, henads, angelic mind, matter, body? |
| Christian transformation | How is the Platonic structure converted into Christology, Trinity, creation, grace, or biblical exegesis? |
| Concord problem | Is Pico harmonizing Plato with Aristotle, out-Platonizing Ficino, or rejecting a Ficinian/Proclean reading? |
| Anthropology | Does the passage center Ficino's Soul/world-soul mediation or Pico's Idea-of-Man/Christological anthropology? |

## Allen Fields for Artifacts

Every relevant artifact must add these fields:

- Ficino relation: source, correction, target, ally, foil, or co-Platonist.
- Platonic dialogue(s): exact dialogue and passage where possible.
- Neoplatonic structure: One, Mind, Soul, Ideas, World Soul, angelic mind, henads, or indeterminate dyad.
- Pico transformation: scholastic, Aristotelian, Kabbalistic, Christological, poetic-theological, or disputational.
- Dispute status: explicit polemic, implicit correction, shared inheritance, later concealment, or modern scholarly reconstruction.
- Edition/witness issue: especially for Commento drafts, Ficino marginalia, Benivieni suppression, Gianfrancesco omission, and Garin's recovery.

## Application to Primary Texts

### Oration

Read the opening anthropology through the Philebus problem of limit/indeterminate, the Timaeus/Parmenides Idea of Man, and the Phaedrus/Proclus whole-in-part logic. Pico's freedom is not absolute modern self-creation. It is the capacity of an indeterminate creature to assume form within a metaphysical ladder and, in the strongest reading, to move toward the Christological Idea of Man later clarified in the Heptaplus.

### On Being and Unity

Treat the work as the second Ficino-Pico controversy. Pico's claim that Plato and Aristotle agree about being and the one is also a challenge to Ficino's Proclean/Parmenidean reading of Plato. Track the Sophist, Parmenides, Aquinas, essence/existence, convertibility, dialectical exercise, and the charge of temerity.

### 900 Conclusions

Read the metaphysical conclusions as a compressed system of Platonic and Aristotelian reconciliation. Track Pico's first created mind/angelic intellect, unity and multiplicity, modal correspondence, contradictions at different levels, thesis clusters, and Farmer's warning that the Conclusions are debate nodes rather than transparent aphorisms.

### Heptaplus

Use Allen with Busi and Wirszubski. Allen highlights Ficinian and Neoplatonic structures: mutual containment, Idea of Man, Christ as perfect man, and the world as great man. Busi and Wirszubski govern Kabbalistic source-control and praxis questions.
""",
    "artifacts/scholar_profiles/allen_values_profile.md": """# Scholar Profile: Michael J. B. Allen

- Artifact ID: `profile_allen_values`
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Scholarly Identity

Michael J. B. Allen is PicoDB's guide scholar for the Ficino-Pico relationship, Renaissance Platonism, Ficino's Platonic commentaries, and Pico's technical engagement with Platonic and Neoplatonic metaphysics. His work makes the relationship between Pico and Ficino a matter of exact philosophical architecture rather than vague influence.

## Arguments and Contributions

Allen argues that Pico was not simply a Ficinian Neoplatonist, but he also was not intelligible without Ficino's Plato, Plotinus, Proclus, and commentary tradition. Pico was Aristotelian by training and eclectic by conviction, yet he acquired in Florence a rare grasp of Platonic methodology and then used it in combative, selective, and often brilliant ways.

In "Cultura hominis," Allen rereads the Oration's opening through the Philebus, Sophist, Timaeus, Parmenides, Phaedrus, Proclus, Ficino, and the Idea of Man. The chameleon is not a modern sovereign self. The indeterminate Adam belongs to a metaphysical problem of limit, potentiality, form, world-soul, and the Idea of Man. Allen then shows how the Heptaplus recasts this anthropology into Christological cosmology: Christ becomes the perfection of man, the new Adam, and the Idea of Man.

In "The Birth Day of Venus," Allen close-reads the Commento and Heptaplus as exercises in Platonic exegesis, poetic theology, and myth interpretation. Pico's Commento attacks Ficino sharply but remains inside a shared world of Platonic myth, Orphic theology, Symposium exegesis, and Neoplatonic metaphysics. Ficino's corrections, Pico's partial rebuttals, Benivieni's later suppression, and Garin's recovery make the textual history itself part of the dispute.

Allen's treatment of the second Ficino-Pico controversy shows that On Being and Unity is not merely a small metaphysical treatise. It is a polemical intervention against Ficino's Proclean reading of Parmenides and Sophist. Pico takes the Aristotelian/Thomist side that being and one are convertible while arguing that Plato's apparent disagreement is verbal or dialectical.

## Historiographical Position

Allen corrects two distortions at once: a Ficino-satellite Pico and an anti-Platonic, purely scholastic Pico. Pico is a contentious co-Platonist. He borrows Ficino's tools, resists Ficino's conclusions, out-Platonizes him at moments, and converts Platonic structures into Christological, anthropological, and concordist forms.

## Use in PicoDB

Use Allen for Ficino relation, Platonic dialogue source-mapping, Neoplatonic hypostasis analysis, Idea of Man, poetic theology, Commento textual history, On Being and Unity, and the metaphysics of the Oration and 900 Conclusions.
""",
    "artifacts/source_packets/allen_cultura_hominis.md": """# Source Packet: Allen, Cultura Hominis

- Artifact ID: `sp_allen_cultura_hominis`
- Document ID: `Studies_in_the_Platonism_of_Marsilio_Ficino_and_Giovanni_PicoMichael_J._B._AllenRoutledge1080299_epub_65585d05`
- Work: Michael J. B. Allen, "Cultura hominis: Giovanni Pico, Marsilio Ficino and the Idea of Man"
- Evidence status: SOURCE_ANCHORED

## Local Summary

Allen rereads the famous opening of the Oration as a dense Platonic and Neoplatonic construction. The chameleon passage draws not only on Hermetic and biblical praise of man but also on the Philebus distinction between limit and the indeterminate, the Timaeus paradigm of the world, the Parmenides problem of the Idea of Man, the Phaedrus all-soul logic, and Ficino's commentary tradition.

The crucial term is `indiscretus`: Adam is not modern unbounded autonomy but potentiality awaiting form. Pico's Adam can choose a determination, but this operates inside a hierarchy of forms and ends. Wrong choices trap the human being in partial actuality; right determination brings the creature toward full being.

Allen then links the Oration to the Heptaplus. In the Heptaplus, man is not simply a fourth world; he is the bond of the three worlds and contains the fullness of the universe as center. The world can be called a great man, and Christ becomes the perfect man, the new Adam, the firstborn of creation, and the perfection of all men. The Hermetic moment of the Oration becomes a Christological cosmology.

## Scholarly Values Extracted

- Track Platonic dialogues behind Pico's metaphysical language.
- Treat Ficino as a necessary context even when Pico disagrees.
- Convert anthropology into metaphysics: Adam, form, potentiality, Idea of Man, World Soul, and Christology.
- Avoid modern absolute-freedom readings of Pico.
- Treat Heptaplus as a refinement of Oration anthropology.

## Next Primary-Text Pass

- Oration opening: add Philebus limit/indeterminate and Idea-of-Man fields.
- Heptaplus general proem 2, 5.6, 5.7, 6.7, final exposition: tag man as bond, great man/world inversion, and Christological completion.
- 900 Conclusions: track soul/all things, all soul, intellect, angelic mind, and unity theses against Allen's reading.
""",
    "artifacts/source_packets/allen_birth_day_venus.md": """# Source Packet: Allen, The Birth Day of Venus

- Artifact ID: `sp_allen_birth_day_venus`
- Documents: Allen collected volume and Dougherty, *Pico della Mirandola: New Essays*
- Evidence status: SOURCE_ANCHORED

## Local Summary

Allen reads Pico's Commento and Heptaplus as works about Platonic exegesis itself: how to explain, allegorize, extrapolate, and theologize myth. Pico's Commento was drafted in autumn 1486 while he prepared the Roman debate. It responded to Benivieni's Platonizing canzone, itself derived from Ficino's De amore. Pico sent the draft to Ficino, who found attacks on his views and returned corrections. Pico incorporated some, rebutted others, and still later remained personally allied with Ficino, who defended him after the Roman crisis.

The textual history matters. Gianfrancesco omitted the Commento from the 1496 Opera; Benivieni suppressed and rewrote the original; later editions muted references to Ficino; Garin recovered the unexpurgated version. PicoDB must therefore treat the Commento as a witness-rich, intervention-laden text where disagreement was partly concealed by friends and editors.

Philosophically, Allen argues that Pico's Commento is less a mature love theory than a rapid, brilliant exercise in metaphysics and poetic theology. Pico challenges Ficino over Orpheus, love, Venus, Mind, the Ideas, and the birth of beauty. The same speculative concerns pass into the Heptaplus, where Mosaic creation receives Platonic and theological interpretation.

## Scholarly Values Extracted

- Ficino-Pico disagreement can coexist with personal alliance.
- Textual suppression and edition history are part of intellectual history.
- Myth interpretation must be tagged as poetic theology, not merely literary ornament.
- The Commento is a key bridge between Ficino's De amore, the Oration, the 900 Conclusions, and the Heptaplus.

## Next Primary-Text Pass

- Add Commento to Pico text gaps as a high-priority primary text for full access and section summary.
- Cross-link Heptaplus proems to Commento metaphysics.
- Add a website essay on the Ficino-Pico dispute centered on De amore, Commento, On Being and Unity, and Heptaplus.
""",
    "artifacts/source_packets/allen_second_ficino_pico_controversy.md": """# Source Packet: Allen, The Second Ficino-Pico Controversy

- Artifact ID: `sp_allen_second_ficino_pico`
- Document ID: `Studies_in_the_Platonism_of_Marsilio_Ficino_and_Giovanni_PicoMichael_J._B._AllenRoutledge1080299_epub_65585d05`
- Evidence status: SOURCE_ANCHORED

## Local Summary

Allen's second Ficino-Pico controversy frames *On Being and Unity* as a technical challenge to Ficino's reading of Plato. The central problem is whether the One is beyond being, as Neoplatonists and Ficino read Plato, or convertible with being, as Aristotle and scholastic metaphysics maintain. Pico argues that the disagreement is verbal or methodological rather than real: Plato does not teach a doctrine contrary to Aristotle in the Parmenides, because the dialogue is a dialectical exercise rather than a straightforward metaphysical treatise.

This makes *On Being and Unity* a site where Pico both depends on Ficino's Platonic recovery and resists Ficino's Proclean interpretation. Pico's argument uses Aristotle and Aquinas, but it also displays sharp awareness of the Parmenides and Sophist as Ficinian texts.

## Scholarly Values Extracted

- Read *On Being and Unity* as controversy, not only concord.
- Track Parmenides and Sophist as contested exegetical objects.
- Mark whether Pico's concord is real reconciliation, verbal harmonization, or polemical correction.
- Treat Ficino's annoyance as evidence of the dispute's stakes.

## Next Primary-Text Pass

- Re-read *On Being and Unity* chapter by chapter for Parmenides/Sophist handling.
- Add fields for convertibility, beyond-being, dialectical exercise, essence/existence, and Ficinian objection.
- Compare with 900 Conclusions metaphysical theses about unity, intellect, soul, and contradiction.
""",
    "artifacts/section_summaries/anthology/being_one_002_allen_reread.md": """# Section Summary: On Being and Unity, Allen-Ficino Reread

- Artifact ID: `sec_being_one_002_allen_reread`
- Document ID: `Heptaplus_Pico_della_Mirandola_On_the_Dignity_of_Man_Being_and_One_pdf_29945776`
- Work: *On Being and Unity*
- Coverage level: SECTION_SUMMARIZED
- Review status: SOURCE_ANCHORED

## Section Function

This reread reframes the opening chapters of *On Being and Unity* as a Ficino-Pico controversy over how to read Plato's *Parmenides* and *Sophist*.

## Exhaustive Argument Summary

The work begins in a Florentine social setting: Lorenzo de' Medici, Poliziano, Benivieni, and Pico are debating whether Plato and Aristotle disagree about being and the one. The Platonist position, associated with Ficino's Proclean tradition, makes the One prior to being. Aristotle makes being and one convertible. Pico enters as the harmonizer, but Allen teaches us that this harmony is also a polemical correction of Ficino.

Pico first states the Platonist case: if the one is simpler and more universal, if God can be called one rather than being, if matter is somehow one while lacking being, and if the opposites of being and one differ, then the one seems higher than being. Pico then asks where Plato actually teaches this. The answer should be the *Parmenides* and *Sophist*, the very texts prized by later Neoplatonists and Ficino. But Pico refuses to read the *Parmenides* as direct metaphysical doctrine. It is a dialectical exercise: Plato is training Socrates to examine consequences, not delivering a theorem that the One is simply beyond being.

This makes the treatise a double act. It defends concord between Plato and Aristotle, but it also restricts Ficino's Proclean Plato. The work is therefore not anti-Platonic; it is anti-Ficinian in a precise sense. Pico claims the right to read Plato better by making Plato agree with Aristotle and Aquinas.

## Argument Map

| Move | Type | Content | Allen Overlay |
|---|---|---|---|
| 1 | contextualizes | The treatise answers a Florentine debate on Plato and Aristotle. | Ficino is the absent but necessary Platonist background. |
| 2 | defines | The Platonist position makes one prior to being. | Proclean/Parmenidean reading. |
| 3 | textualizes | Pico asks where Plato teaches this. | The dispute turns on dialogue exegesis. |
| 4 | reclassifies | The *Parmenides* is a dialectical exercise, not direct doctrine. | Pico limits Ficino's metaphysical use of the dialogue. |
| 5 | reconciles | Plato and Aristotle can agree if terms are properly distinguished. | Concord is also polemical correction. |

## Scholarly Values Overlay

Guide scholars: Allen, Edelheit, Copenhaver, Dougherty.

Allen supplies the core: Ficino relation, Parmenides/Sophist, Proclean ontology, and controversy. Edelheit supplies scholastic terminology and Aquinas. Copenhaver supplies anti-mythic correction and late-medieval precision. Dougherty supplies genre and edition awareness.

## Claims

- *On Being and Unity* should be cataloged as both concordist treatise and Ficino-Pico controversy.
- Pico's dismissal of doctrinal readings of *Parmenides* is a methodological attack on Ficino's Proclean Plato.
- The treatise's Aristotelian/Thomist position does not remove Pico from Platonism; it defines a contested co-Platonism.
""",
    "artifacts/section_summaries/anthology/oration_003_allen_metaphysics.md": """# Section Summary: Oration, Allen Metaphysics Reread

- Artifact ID: `sec_oration_003_allen_metaphysics`
- Document ID: `Heptaplus_Pico_della_Mirandola_On_the_Dignity_of_Man_Being_and_One_pdf_29945776`
- Work: *Oration*
- Coverage level: SECTION_SUMMARIZED
- Review status: SOURCE_ANCHORED

## Section Function

This reread adds Allen's metaphysical anthropology to the existing Oration summaries. The opening freedom passage is not modern self-invention; it is a Platonic, Neoplatonic, Hermetic, biblical, and Christologically charged theory of indeterminate potentiality seeking form.

## Exhaustive Argument Summary

Pico's Adam is placed at the center after the angelic, celestial, animal, and vegetative orders have received determinate natures. Allen focuses on the technical meaning of indeterminate form. `Indiscretus` means lacking distinction, face, fixed seat, or determinate gift. In Platonic terms, this recalls the *Philebus* problem of the indeterminate and the limit: potentiality needs determination to become full actuality.

The Oration's freedom is therefore not absolute power to invent reality. Adam receives all seeds, but the seeds belong to an ordered hierarchy. The human task is to cultivate the form that brings the creature into the right actuality. Descent into plant or beast is not creative liberation but partial and defective determination. Ascent toward angelic and divine life is the realization of the human capacity to become all things in the right way.

Allen also connects the Oration to the *Timaeus*, *Parmenides*, *Phaedrus*, and Proclus. The human being is tied to the Idea of Man, the intelligible world, whole-in-part metaphysics, and the problem of the soul's relation to World Soul. This does not erase Hermetic and biblical sources; it thickens them. The Oration's famous images now become nodes in a metaphysical network: Adam, chameleon, Prometheus, Enoch, Jacob's ladder, Osiris/Isis, and angelic ascent all point toward the transformation of potentiality into rightly ordered form.

## Argument Map

| Move | Type | Content | Allen Overlay |
|---|---|---|---|
| 1 | defines | Man has indeterminate form and no fixed seat. | Philebus: indeterminate/potentiality. |
| 2 | qualifies | Freedom occurs inside a hierarchy of seeds and forms. | Not modern absolute self-creation. |
| 3 | hierarchizes | Descent and ascent are determinations of potentiality. | Wrong form versus full actuality. |
| 4 | textualizes | Timaeus, Parmenides, Phaedrus, Proclus, and Ficino become needed controls. | Platonic anthropology and Idea of Man. |
| 5 | cross-links | Heptaplus Christology later completes the anthropology. | Christ as perfect man/new Adam. |

## Scholarly Values Overlay

Guide scholars: Allen, Copenhaver, Howlett, Edelheit.

Allen supplies the metaphysical source-map; Copenhaver prevents dignity-myth isolation; Howlett keeps exceptionalist ascent and three-pillar coherence visible; Edelheit keeps Aristotelian potentiality/act and scholastic language in play.
""",
    "artifacts/section_summaries/farmer/conclusions_004_allen_metaphysics.md": """# Section Summary: 900 Conclusions, Allen-Farmer Metaphysics Reread

- Artifact ID: `sec_conclusions_004_allen_metaphysics`
- Document ID: `Medieval_Renaissance_Texts_Studies_167_Stephen_A_Farmer_Giovanni_Pico_Della_Mirandola_Syncretism_pdf_c99b971b`
- Work: 900 Conclusions
- Coverage level: SECTION_SUMMARIZED
- Review status: SOURCE_ANCHORED

## Section Function

This reread connects Allen's Ficino/Pico metaphysics with Farmer's thesis-cluster method. The 900 Conclusions are not a list of isolated propositions but a compressed metaphysical machine in which Pico tests unity, multiplicity, intellect, soul, angels, contradiction, and concord across traditions.

## Exhaustive Argument Summary

Farmer shows that Pico's theses must be collated by clusters. Allen helps explain why many of the most compressed clusters are metaphysical and Platonic. Pico's "new philosophy" works through a hierarchy in which God, intellectual nature, soul, and lower nature correspond without simply collapsing into each other. The first created mind may be called intellect, angelic mind, angel, or intellectual nature, and this flexible naming itself needs ontology support.

The metaphysical pattern is modal: what exists in one mode at one level may reappear in another mode elsewhere. Unity and multiplicity, contradiction and noncontradiction, whole and part, intellect and soul cannot be read univocally across all levels. In God, unity is without otherness; in soul, unity is extended or mixed with otherness; in intellect, Pico struggles to describe compatibility, distinction, and identity without ordinary contradiction.

Allen's Ficino frame matters because these thesis clusters are Pico's way of appropriating and revising post-Plotinian Platonism. Ficino supplies Proclean and Plotinian architecture, but Pico maps it into scholastic, Aristotelian, angelological, Kabbalistic, and disputational forms. The 900 Conclusions therefore need fields for hypostasis, mode, correspondence, contradiction status, authority chain, and debate function.

## Argument Map

| Move | Type | Content | Allen-Farmer Overlay |
|---|---|---|---|
| 1 | methodological | Theses are debate nodes requiring cluster collation. | Farmer control. |
| 2 | identifies | God, intellect/angelic mind, soul, and nature form a hierarchy. | Allen/Ficino hypostasis control. |
| 3 | modalizes | Properties recur differently at different levels. | `modo suo`, whole-in-part, correspondence. |
| 4 | problematizes | Contradiction behaves differently in soul, intellect, and God. | Ordinary logic versus higher unity. |
| 5 | synthesizes | Pico translates Platonism into scholastic, Kabbalistic, and disputational idioms. | Concord as active transformation. |

## Scholarly Values Overlay

Guide scholars: Allen, Farmer, Edelheit, Copenhaver, Busi, Wirszubski.

Allen supplies Ficinian/Neoplatonic architecture; Farmer supplies thesis-cluster method; Edelheit supplies scholastic source tracing; Copenhaver supplies juridical and theological risk; Busi and Wirszubski control Kabbalah and magic when the metaphysical clusters cross into Cabala.
""",
    "artifacts/essays/pico_ficino_dispute_longform_draft.md": """# Essay Draft: Pico's Dispute with Ficino

- Artifact ID: `essay_pico_ficino_dispute_draft`
- Target length: 6,000-10,000 words for the next full draft. The user's phrase "6,000-10,000 page essay" is treated here as a long-form essay target rather than literal page count.
- Status: DRAFT
- Evidence status: SOURCE_ANCHORED_DRAFT

## Thesis

Pico's dispute with Ficino was not a simple quarrel between a rebellious prodigy and an older master. It was a sustained argument inside a shared Christian Platonist world. Ficino had given Florence a vast architecture of Plato, Plotinus, Proclus, ancient theology, love, soul, cosmic sympathy, and ascent. Pico entered that architecture with astonishing speed, learned its technical grammar, and then began to revise its foundations. The result was a relationship of dependence, correction, rivalry, gratitude, and concealed disagreement.

The dispute has at least four centers. First is the *Commento*, where Pico responds to a Ficinian love-theory tradition and attacks points in Ficino's *De amore*. Second is *On Being and Unity*, where Pico challenges Ficino's Proclean reading of Plato's *Parmenides* and *Sophist* by defending the convertibility of being and one. Third is the metaphysics of the *Oration* and *900 Conclusions*, where Pico turns Ficinian and post-Plotinian structures into a disputational machine that includes Aristotle, scholasticism, Kabbalah, magic, and angelology. Fourth is the *Heptaplus*, where Pico's anthropology of indeterminate Adam becomes a Christological cosmology centered on the Idea of Man.

## 1. Friendship, Correction, and Concealed Conflict

Allen's most useful correction is that disagreement did not cancel intimacy. Pico sent his *Commento* draft to Ficino. Ficino read it, objected sharply, and returned corrections. Pico adopted some corrections and rejected others. Yet Ficino later defended Pico after the Roman crisis and helped secure his Florentine refuge under Lorenzo de' Medici. Pico could praise Ficino as a master and father of the Platonic family while also writing as if Ficino had erred badly in the interpretation of love, Venus, Mind, and the Platonic myths.

This matters for PicoDB because the social relation and the textual record do not align simply. Friends and editors later softened the controversy. Gianfrancesco did not include the *Commento* in the first collected works. Benivieni reworked and suppressed material. Later editions transmitted an altered form. The dispute therefore survives as both philosophy and textual event. Any account of Pico against Ficino must ask which version of Pico is speaking and which later hand has shaped the evidence.

## 2. The First Controversy: Love, Venus, and Poetic Theology

The *Commento* began in Ficino's territory. Benivieni's canzone depends on Ficino's *De amore*, itself a Platonizing commentary on the *Symposium*. Pico's commentary is therefore not just commentary on a poem; it is commentary on a Ficinian commentary. Allen shows that Pico is less interested in mature love theory than in metaphysics and poetic theology. The myths of Venus, Love, Porus, Penia, Orpheus, Eurydice, Mind, Ideas, and Beauty become problems about procession, return, intelligible form, and the birth of thought.

Pico's boldness lies in treating myth as a technical metaphysical language. Ficino also does this, but Pico pushes the practice into pointed corrections. Ficino had been cautious with Orpheus in the *Symposium*; Pico uses Orpheus to argue that the soul cannot attain true intelligible vision without a kind of death to imagination and reason. Ficino's musical Orphism, his gentler theory of love, and his cosmic harmonics remain in the background, but Pico's version is sharper and more ascetic.

## 3. The Second Controversy: Being, Unity, and the Parmenides

*On Being and Unity* is the cleanest metaphysical dispute. Ficino's Plato, shaped by late Neoplatonism and Proclus, places the One beyond being. Pico, answering a Florentine debate involving Lorenzo and Poliziano, argues that Plato and Aristotle do not truly disagree. Being and one are convertible. If Plato seems to place the One beyond being, this is because readers have mistaken dialectical exercise for doctrine or have failed to distinguish senses of being.

Allen makes clear that Pico is not merely retreating into Aristotle. He is fighting over Plato. The *Parmenides* and *Sophist* are not neutral citations. They are Ficino's great Platonic texts, the very dialogues through which later Neoplatonism built its hierarchy of One, Mind, Soul, and lower being. Pico's claim that the *Parmenides* is methodological rather than doctrinal limits Ficino's authority at its source.

The argument is concordist, but not irenic in a bland sense. Pico's concord says: Plato agrees with Aristotle when rightly read. But that means Ficino, as reader of Plato, may be wrong. Concord becomes correction.

## 4. Oration: Freedom as Metaphysical Potentiality

Allen also changes how we read the *Oration*. The modern dignity myth isolates the passage in which Adam receives no fixed place and becomes what he wills. Allen pushes us into the metaphysical grammar behind that claim. The key is not absolute modern freedom but indeterminate potentiality. Adam is an `indiscreta imago`, an image without fixed determination. This recalls the *Philebus* distinction between the indeterminate and limit, potentiality and form.

The human being is free because he can assume forms within the created hierarchy. He is not free because he stands outside hierarchy. Wrong form is defective actuality: plant, brute, or partial being. Right form is ascent toward intellect, angelic life, and union with God. The metaphysics of the *Oration* therefore belongs with act/potency, Platonic Ideas, Timaean paradigm, Phaedran soul, Proclean whole-in-part logic, and finally Christian perfection.

Here Pico differs from Ficino but also depends on him. Ficino's anthropology centers the soul as the middle hypostasis, the bond of the world, the participant in World Soul. Pico's anthropology centers the indeterminate Adam and the Idea of Man. Ficino gives a cosmos of harmony, Soul, proportion, and musical mediation. Pico gives a dramatic anthropology of choice, ascent, and Christological completion.

## 5. The 900 Conclusions as Metaphysical Machine

The *900 Conclusions* make the Pico-Ficino dispute harder to see because the theses are compressed and cross-disciplinary. Farmer teaches us to collate thesis clusters. Allen teaches us what kind of metaphysical architecture to look for. Pico's theses work through God, intellectual nature, angelic mind, soul, lower nature, unity, multiplicity, contradiction, whole and part, and correspondence. These are not merely scholastic puzzles. They are Pico's attempt to build a universal debate system that can absorb post-Plotinian Platonism, Aristotle, scholastic distinctions, Kabbalah, magic, and ancient theology.

In this system, terms shift by level. What is true in God is true without otherness; what is true in soul is extended and divided; what is true in intellectual nature strains ordinary contradiction. Pico's metaphysics is therefore modal and hierarchical. A term such as intellect, angel, first mind, or intellectual nature may name the same level under different traditions. This is exactly where the database needs stronger ontology fields: hypostasis, tradition label, authority chain, mode of predication, contradiction status, and debate function.

## 6. Heptaplus: The Idea of Man Becomes Christological Cosmology

The *Heptaplus* does not abandon the *Oration*. It transforms it. Allen shows that the fourth-world anthropology becomes a richer cosmology. Man is the bond of the three worlds, not merely another world beside them. He contains the universe as center, while God contains all things as origin. The microcosm motif becomes reciprocal: man is a little world, but the world is also a great man.

The decisive transformation is Christological. Christ is the perfect man, the new Adam, the firstborn of creation, the perfection of all men, and the one through whom human ascent becomes more than philosophical self-cultivation. The Idea of Man becomes Christ. This does not remove Kabbalah, biblical allegory, or Dionysian hierarchy from the *Heptaplus*; it sets the metaphysical question Allen sees beneath them. Busi and Wirszubski remain necessary for Kabbalistic structures, but Allen shows why Ficino's Platonism remains pervasive.

## 7. Working Conclusion

Pico's dispute with Ficino is best described as contentious co-Platonism. Pico is not Ficino's disciple in any docile sense. He corrects Ficino, attacks him, absorbs him, praises him, and depends on the very Platonist textual world Ficino made available. Ficino is not simply the older thinker whom Pico surpasses. He is the condition of possibility for much of Pico's Platonic ambition, and also the thinker Pico must contest if his own concord is to stand.

The next full draft should expand this essay into four evidence-heavy chapters: the *Commento* controversy; *On Being and Unity* and the Parmenides/Sophist; the *Oration* and *900 Conclusions* as metaphysical anthropology and thesis machine; and the *Heptaplus* as Christological cosmology. It should also include a timeline of Pico-Ficino contacts, a textual witness appendix for the *Commento*, and a table of disputed metaphysical terms.
""",
}


ARTIFACT_ROWS = [
    ("profile_allen_values", "scholar_profile", "Michael J. B. Allen Values Profile", "artifacts/scholar_profiles/allen_values_profile.md", ALLEN_VOL, "Michael J. B. Allen", "SOURCE_ANCHORED", "likely"),
    ("sp_allen_cultura_hominis", "source_packet", "Allen: Cultura Hominis", "artifacts/source_packets/allen_cultura_hominis.md", ALLEN_VOL, "Oration and Heptaplus metaphysics", "SOURCE_ANCHORED", "likely"),
    ("sp_allen_birth_day_venus", "source_packet", "Allen: The Birth Day of Venus", "artifacts/source_packets/allen_birth_day_venus.md", DOUGHERTY, "Commento and Heptaplus", "SOURCE_ANCHORED", "likely"),
    ("sp_allen_second_ficino_pico", "source_packet", "Allen: Second Ficino-Pico Controversy", "artifacts/source_packets/allen_second_ficino_pico_controversy.md", ALLEN_VOL, "On Being and Unity", "SOURCE_ANCHORED", "likely"),
    ("sec_being_one_002_allen_reread", "section_summary", "On Being and Unity 002: Allen-Ficino Reread", "artifacts/section_summaries/anthology/being_one_002_allen_reread.md", ANTHOLOGY, "On Being and Unity", "SOURCE_ANCHORED", "likely"),
    ("sec_oration_003_allen_metaphysics", "section_summary", "Oration 003: Allen Metaphysics Reread", "artifacts/section_summaries/anthology/oration_003_allen_metaphysics.md", ANTHOLOGY, "Oration", "SOURCE_ANCHORED", "likely"),
    ("sec_conclusions_004_allen_metaphysics", "section_summary", "900 Conclusions 004: Allen-Farmer Metaphysics Reread", "artifacts/section_summaries/farmer/conclusions_004_allen_metaphysics.md", FARMER, "900 Conclusions", "SOURCE_ANCHORED", "likely"),
    ("essay_pico_ficino_dispute_draft", "website_page", "Pico's Dispute with Ficino Longform Draft", "artifacts/essays/pico_ficino_dispute_longform_draft.md", ALLEN_VOL, "Pico-Ficino dispute", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
]


CLAIMS = [
    ("claim_allen_001", "sp_allen_cultura_hominis", ALLEN_VOL, "Allen reads the Oration's indeterminate Adam through the Philebus problem of indeterminate potentiality and determinate limit.", "interpretive", "Oration metaphysics", "Oration", "Cultura hominis", "high", "DRAFT", "Pass 006 Allen close reading."),
    ("claim_allen_002", "sp_allen_cultura_hominis", ALLEN_VOL, "Allen argues that the Heptaplus refines the Oration's anthropology by making man the bond of the three worlds and by developing a Christological Idea of Man.", "interpretive", "Heptaplus", "Heptaplus", "Cultura hominis", "high", "DRAFT", "Pass 006 Allen close reading."),
    ("claim_allen_003", "sp_allen_birth_day_venus", DOUGHERTY, "Allen treats the Commento as a combative exercise in Platonic exegesis and poetic theology rather than a full mature theory of love.", "interpretive", "Commento", "Commento", "The Birth Day of Venus", "high", "DRAFT", "Pass 006 Allen close reading."),
    ("claim_allen_004", "sp_allen_birth_day_venus", DOUGHERTY, "Allen shows that Pico's Commento disagreement with Ficino was later softened or concealed through omission, suppression, rewriting, and edition history.", "historical", "textual history", "Commento", "The Birth Day of Venus", "high", "DRAFT", "Pass 006 Allen close reading."),
    ("claim_allen_005", "sp_allen_second_ficino_pico", ALLEN_VOL, "Allen frames On Being and Unity as a second Ficino-Pico controversy over Parmenides, Sophist, the One, and being.", "historiographical", "Ficino-Pico dispute", "On Being and Unity", "Second Ficino-Pico controversy", "high", "DRAFT", "Pass 006 Allen close reading."),
    ("claim_allen_006", "sec_being_one_002_allen_reread", ANTHOLOGY, "On Being and Unity should be tagged as both a concordist text and a polemical correction of Ficino's Proclean Plato.", "interpretive", "concord", "On Being and Unity", "Allen reread", "high", "DRAFT", "Pass 006 primary reread."),
    ("claim_allen_007", "sec_oration_003_allen_metaphysics", ANTHOLOGY, "The Oration's freedom passage should be read as ordered metaphysical potentiality rather than absolute modern self-creation.", "interpretive", "human dignity", "Oration", "Allen reread", "high", "DRAFT", "Pass 006 primary reread."),
    ("claim_allen_008", "sec_conclusions_004_allen_metaphysics", FARMER, "The metaphysical theses of the 900 Conclusions need hypostasis, mode, correspondence, and contradiction-status fields to capture Pico's translation of Neoplatonism into scholastic and disputational forms.", "methodological", "900 Conclusions", "900 Conclusions", "Allen-Farmer reread", "high", "DRAFT", "Pass 006 primary reread."),
]


CARDS = [
    ("values-allen", "scholar", "Allen's Ficino-Pico Protocol", "Contentious co-Platonism", "Michael J. B. Allen now anchors the portal's treatment of Pico and Ficino: shared Platonism, pointed correction, textual concealment, and technical disputes over One, being, Mind, Soul, Ideas, and the Idea of Man.", "DRAFT", "profile_allen_values"),
    ("ficino-pico-dispute", "essay", "Pico's Dispute with Ficino", "Longform essay draft", "A new longform essay seed frames the Pico-Ficino dispute through the Commento, On Being and Unity, Oration, 900 Conclusions, and Heptaplus.", "DRAFT", "essay_pico_ficino_dispute_draft"),
    ("being-one-allen", "work", "On Being and Unity: Ficino Controversy", "Parmenides, Sophist, One", "The On Being and Unity dossier now treats the work as both concordist metaphysics and a polemical correction of Ficino's Proclean Plato.", "DRAFT", "sec_being_one_002_allen_reread"),
    ("oration-allen-metaphysics", "work", "Oration: Indeterminate Adam", "Philebus and Idea of Man", "Allen's metaphysical reread turns the Oration opening from a modern freedom slogan into a Platonic problem of potentiality, form, whole-in-part logic, and Christological anthropology.", "DRAFT", "sec_oration_003_allen_metaphysics"),
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
    payload["version"] = "0.5.0"
    payload.setdefault("guide_scholars", {})["Allen"] = [
        "ficino_relation",
        "platonic_dialogue_source",
        "neoplatonic_hypostasis",
        "idea_of_man",
        "poetic_theology",
        "commento_textual_history",
        "being_one_controversy",
    ]
    payload["ficino_pico_reading_fields"] = [
        "ficino_relation",
        "platonic_dialogues",
        "neoplatonic_structure",
        "pico_transformation",
        "dispute_status",
        "edition_witness_issue",
        "christian_transformation",
        "concord_outcome",
    ]
    payload["scholarly_value_dimensions"] = list(
        dict.fromkeys(
            payload.get("scholarly_value_dimensions", [])
            + [
                "ficino_relation",
                "platonic_dialogue_source",
                "neoplatonic_hypostasis",
                "idea_of_man",
                "poetic_theology",
                "commento_textual_history",
                "being_one_controversy",
            ]
        )
    )
    write_json(path, payload)


def update_docs() -> None:
    for path, text in FILES.items():
        write(path, text)
    append_once(
        DOCS / "SCHOLARLY_VALUES_STYLE_GUIDE.md",
        "## Pass 006 Allen Overlay",
        """## Pass 006 Allen Overlay

Add Allen as the guide scholar for Pico's relationship to Ficino. Use him whenever a passage involves Ficino, Platonic exegesis, the Commento, On Being and Unity, the Idea of Man, poetic theology, or Neoplatonic structures behind the Oration, 900 Conclusions, and Heptaplus.

Allen's core warning: do not reduce Pico to Ficino's disciple, Ficino's enemy, or a non-Platonic scholastic. Pico is a contentious co-Platonist who uses Ficino's recovered Plato and then revises it.
""",
    )
    append_once(
        DOCS / "SECTION_SUMMARY_STYLE_GUIDE.md",
        "## Pass 006 Ficino-Pico Overlay",
        """## Pass 006 Ficino-Pico Overlay

When a section touches Ficino or Platonism, include: Ficino relation, Platonic dialogue source, Neoplatonic structure, Pico transformation, dispute status, edition/witness issue, Christian transformation, and concord outcome. See `docs/FICINO_PICO_READING_PROTOCOL.md`.
""",
    )


def main() -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    update_docs()
    update_ontology()

    conn = sqlite3.connect(DB)
    for path, text in FILES.items():
        if path.startswith("artifacts/"):
            write(path, text)
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
        "INSERT OR REPLACE INTO pico_text_gaps(title,status,reason,evidence,updated_at) VALUES (?,?,?,?,?)",
        (
            "Commento sopra una canzone d'amore composta da Girolamo Benivieni",
            "high_priority_primary_text_needed",
            "Allen shows the Commento is central to the Ficino-Pico dispute and was affected by suppression, rewriting, and later editions; a complete primary text and witness notes are required.",
            "Allen, Birth Day of Venus; Garin 1942; Jayne translation noted by Allen.",
            now,
        ),
    )
    conn.commit()

    seed = load_seed_module()
    seed.export_data(conn)
    seed.build_site(conn)
    conn.close()
    print("Study pass 006 complete.")


if __name__ == "__main__":
    main()
