"""Study pass 004: style guides and formal section summaries.

This pass turns the user's requirement for detailed section-by-section
summaries into operating files and seeds the first summaries using the
coverage standard.
"""

from __future__ import annotations

import importlib.util
import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "pico.db"

ANTHOLOGY = "Heptaplus_Pico_della_Mirandola_On_the_Dignity_of_Man_Being_and_One_pdf_29945776"
FARMER = "Medieval_Renaissance_Texts_Studies_167_Stephen_A_Farmer_Giovanni_Pico_Della_Mirandola_Syncretism_pdf_c99b971b"


SECTION_SUMMARIES = {
    "artifacts/section_summaries/anthology/oration_001_wonder_indeterminacy.md": """# Section Summary: Oration, Wonder and Human Indeterminacy

- Document ID: `Heptaplus_Pico_della_Mirandola_On_the_Dignity_of_Man_Being_and_One_pdf_29945776`
- Source file: `Heptaplus Pico della Mirandola On the Dignity of Man Being and One.pdf`
- Work / book: *On the Dignity of Man*
- Section title: Opening: wonder, Adam, and indeterminate form
- Page range: extracted pages 38-42
- Section boundary basis: generated page range within the Oration opening
- Coverage level: SECTION_SUMMARIZED
- Review status: SOURCE_ANCHORED
- Evidence status: likely

## Section Function

This section establishes the anthropological premise of the Oration. It asks why man is more wonderful than angels and answers by defining human nature as indeterminate, self-shaping, and capable of descent or ascent.

## Exhaustive Argument Summary

Pico begins from authorities outside ordinary Latin Christian scholasticism: Abdul the Saracen and Mercury/Asclepius say that man is a great wonder. He then tests inherited explanations for that wonder. Man has been praised as messenger between creatures, familiar of the upper realm, king of the lower realm, interpreter of nature, midpoint between eternity and time, bond of the world, and a little lower than the angels. Pico does not deny these praises, but he says they are not sufficient, because they do not explain why man should be more wonderful than angelic beings themselves.

The decisive account is a creation narrative. God has already filled the supercelestial, celestial, and lower regions. When he wishes to make a contemplator of the world, no fixed archetype, inheritance, or cosmic seat remains. God therefore makes man a work of indeterminate form and places him at the center of the world. Adam receives no fixed seat, form, or peculiar gift; he receives the ability to choose and possess whatever form he cultivates.

This freedom is vertical and moral. Man can degenerate into plant or brute by cultivating vegetative or sensual seeds. He can rise into rational life, angelic intellect, sonship of God, and finally into unity with God in the darkness of the Father. Pico then names man a chameleon and uses metamorphosis traditions to explain that humanity is not a stable species-position but a condition of transformability.

The section closes by making the doctrine practical. Because human freedom can be abused, the proper response is holy ambition: spurn lower things, struggle toward heavenly things, and compete with angels. Human dignity is therefore not a static possession; it is a dangerous openness that must be disciplined toward ascent.

## Argument Map

| Move | Type | Content | Evidence |
|---|---|---|---|
| 1 | defines | Man is introduced as the most wonderful creature through Arabic and Hermetic authorities. | extracted p. 38 |
| 2 | rejects | Standard praises of man are great but insufficient because angels would seem more admirable. | extracted pp. 38-39 |
| 3 | narrates | God finds no fixed archetype or seat left and creates man as indeterminate. | extracted pp. 39-40 |
| 4 | distinguishes | Human seeds produce plant, brute, rational, angelic, or divine modes depending on cultivation. | extracted pp. 40-41 |
| 5 | allegorizes | Chameleon, Prometheus, Enoch, Pythagorean/Jewish metamorphosis, and Mohammedan moral transformation all illustrate mutable humanity. | extracted pp. 40-41 |
| 6 | exhorts | The proper response is holy ambition and ascent beyond worldly things toward angelic life. | extracted p. 42 |

## Claims and Subclaims

| Claim | Evidence | Claim type | Theme | Target | Confidence |
|---|---|---|---|---|---|
| Pico's opening does not rest content with inherited praises of man as cosmic mediator. | extracted pp. 38-39 | textual | Oration | Oration opening | high |
| Human dignity is grounded in indeterminate form and self-shaping capacity. | extracted pp. 39-40 | textual | human dignity | Adam | high |
| Human freedom is hierarchical: the same creature can become lower, rational, angelic, or united with God. | extracted pp. 40-41 | textual | ascent | human nature | high |
| The chameleon image marks mutable anthropology rather than secular individuality. | extracted p. 40 | interpretive | anthropology | chameleon | medium |
| The section requires readers to treat dignity as vocation and risk, not simply empowerment. | extracted p. 42 | interpretive | historiography | Oration reception | medium |

## Reference Register

| Reference | Type | Tradition/Field | Local Role | Evidence | Status |
|---|---|---|---|---|---|
| Abdul the Saracen | person | Arabic/legendary wisdom | Opens the wonder motif. | extracted p. 38 | needs_review |
| Mercury / Asclepius | work/person | Hermetic | Confirms man as a great wonder. | extracted p. 38 | identified |
| David / Psalm 8 | biblical_text | Hebrew Bible/Christian scripture | Supplies "little lower than the angels." | extracted p. 38 | identified |
| Moses and Timaeus | work/person | Biblical and Platonic cosmology | Witness creation after cosmic completion. | extracted p. 39 | identified |
| Adam | biblical_person | Genesis | Addressee of divine speech on indeterminacy. | extracted pp. 39-40 | identified |
| Lucilius | person/work | Roman satire | Used for innate possession of brutes. | extracted p. 40 | identified |
| Prometheus | figure | Greek myth/rites | Symbol of mutable human nature. | extracted p. 40 | identified |
| Enoch / malach hashechina | biblical/Kabbalistic figure | Jewish mystical tradition | Example of human reshaped into angelic/divine form. | extracted p. 41 | needs_review |
| Pythagoreans / Empedocles | school/person | Greek philosophy | Metamorphosis and moral deformation. | extracted p. 41 | identified |
| Mohammed | person | Islamic tradition | Moral regression into brute life. | extracted p. 41 | identified |
| Asaph / Psalm 82 | biblical_text | Psalms | Humans as gods/sons of the Most High. | extracted p. 42 | identified |

## Pico Texts Discussed

- *On the Dignity of Man*

## Concepts and Themes

- Human dignity
- Indeterminate form
- Self-fashioning
- Ascent and descent
- Angelic imitation
- Hermetic and Kabbalistic anthropology

## Named Persons, Works, and Places

Abdul the Saracen, Mercury/Asclepius, David, Moses, Plato's *Timaeus*, Adam, Lucilius, Prometheus, Enoch, Pythagoreans, Empedocles, Mohammed, Asaph.

## Historiographical Position

This section supports Copenhaver/Farmer/Howlett-style resistance to an Oration-only modern dignity myth. The text does speak of freedom, but the freedom is embedded in ascetic, mystical, theological, and concordist ascent.

## Textual / Philological Notes

Several references require verification against Latin and notes: Abdul the Saracen, malach hashechina, and the exact Hebrew/Kabbalistic framing of Enoch.

## Knowledge Product Hooks

- Oration page: opening as indeterminacy.
- Concept dossier: human dignity as vocation.
- Concept dossier: metamorphosis and angelic ascent.
- Reference graph: Hermetic, Jewish, Pythagorean, Islamic witnesses.

## Open Problems and Follow-Up Tasks

- Verify the Latin terms for "indeterminate form," "center of the world," and the chameleon image.
- Compare Copenhaver's reading of this opening against the anthology translation.
- Add references to the reference graph when that table is created.

## Coverage Checklist

- [x] Section function stated.
- [x] All major argument moves listed.
- [x] All named references registered or deferred.
- [x] Claims are atomic and source-tethered.
- [x] Technical terms are explained.
- [x] Pico works and cross-links identified.
- [x] Uncertainties marked.
""",
    "artifacts/section_summaries/anthology/oration_002_disciplines_ladder.md": """# Section Summary: Oration, Angelic Models and the Ladder of Disciplines

- Document ID: `Heptaplus_Pico_della_Mirandola_On_the_Dignity_of_Man_Being_and_One_pdf_29945776`
- Source file: `Heptaplus Pico della Mirandola On the Dignity of Man Being and One.pdf`
- Work / book: *On the Dignity of Man*
- Section title: Seraph, cherub, throne, Jacob's ladder, and the philosophical disciplines
- Page range: extracted pages 42-49
- Section boundary basis: generated page range following the opening anthropology
- Coverage level: SECTION_SUMMARIZED
- Review status: SOURCE_ANCHORED
- Evidence status: likely

## Section Function

This section turns the opening anthropology into a curriculum. Pico explains how the human being can become angelic: charity, intelligence, judgment, moral philosophy, dialectic, natural philosophy, and theology form a staged ascent.

## Exhaustive Argument Summary

Pico asks how humans can equal the angels if they choose to aspire upward. He answers by examining angelic offices. The seraph burns with charity, the cherub shines with intelligence, and the throne stands in judgment. These are not merely decorative angel names; they become models of life. Active life rightly ordered corresponds to the thrones; contemplation of the workman in the work corresponds to cherubic light; love of the divine Workman corresponds to seraphic fire.

The cherub occupies the middle and therefore mediates the ascent. Because one cannot judge or love what one does not know, contemplative illumination prepares both judgment and love. Pico then turns to Dionysius and Paul: the cherubic life proceeds by purgation, illumination, and perfection. This yields the curriculum. Moral science confines passions; dialectic clears reason; natural philosophy illuminates the ordered soul; divine knowledge perfects it.

Jacob's ladder provides the next figure. The ladder marks ascent and descent, but one cannot touch it with impure feet and hands. Pico allegorizes the feet as the nutritive/appetitive powers and the hands as anger or spirited force. Moral philosophy washes these lower powers; the reasoning art trains movement from rung to rung; natural philosophy lets the soul move through the ladder of nature by dividing unity into multiplicity and gathering multiplicity into unity; theology brings rest in the Father.

The Job/Empedocles passage then reframes ascent as peace. The soul is internally divided by war and friendship, strife and peace. Moral philosophy quiets the brute and wrathful powers, dialectic calms reason's turmoil, natural philosophy still deals with nature's conflict, and theology alone gives the peace nature cannot give. The section ends by converting philosophy into bridal and mystical imagery: the purified soul becomes a house of God and bride of the divine bridegroom.

## Argument Map

| Move | Type | Content | Evidence |
|---|---|---|---|
| 1 | distinguishes | Seraph, cherub, and throne correspond to charity, intelligence, and judgment. | extracted pp. 42-43 |
| 2 | hierarchizes | Cherubic contemplation mediates judgment and love because one must know before judging or loving. | extracted pp. 43-44 |
| 3 | transmits | Dionysian purgation, illumination, and perfection become the structure of philosophical ascent. | extracted pp. 43-44 |
| 4 | allegorizes | Jacob's ladder becomes the image for disciplined ascent and descent. | extracted pp. 44-45 |
| 5 | defines | Moral philosophy, dialectic, natural philosophy, and theology each receive a distinct task. | extracted pp. 44-47 |
| 6 | reconciles | Job and Empedocles are read together through peace/strife as internal anthropology. | extracted pp. 45-46 |
| 7 | culminates | Theology gives the final peace and mystical union that nature cannot provide. | extracted pp. 46-49 |

## Claims and Subclaims

| Claim | Evidence | Claim type | Theme | Target | Confidence |
|---|---|---|---|---|---|
| The angelic triad is a practical model for human transformation. | extracted pp. 42-43 | textual | angelology | Oration | high |
| The Oration's philosophical curriculum follows purgation, illumination, and perfection. | extracted pp. 43-44 | textual | philosophy | Dionysian ascent | high |
| Moral philosophy purifies appetite and anger before higher disciplines can operate. | extracted pp. 44-46 | textual | moral philosophy | discipline ladder | high |
| Dialectic disciplines reason and trains ordered movement up and down Jacob's ladder. | extracted p. 45 | textual | dialectic | discipline ladder | high |
| Natural philosophy handles multiplicity and conflict but does not supply final peace. | extracted pp. 45-47 | textual | natural philosophy | discipline ladder | high |
| Theology crowns the ascent with peace, union, and divine indwelling. | extracted pp. 46-49 | textual | theology | discipline ladder | high |

## Reference Register

| Reference | Type | Tradition/Field | Local Role | Evidence | Status |
|---|---|---|---|---|---|
| Seraphim, cherubim, thrones | doctrine | angelology | Models of love, intelligence, and judgment. | extracted pp. 42-43 | identified |
| Moses | person | Biblical/exemplary contemplation | Model of seeing God then judging people. | extracted p. 43 | identified |
| Pseudo-Dionysius | person/work | Christian Neoplatonism | Supplies purgation, illumination, perfection. | extracted pp. 43-44 | identified |
| Paul | person | New Testament | Witness to third heaven and cherubic action. | extracted p. 43 | identified |
| Jacob's ladder | biblical_text | Genesis | Image of ascent/descent. | extracted pp. 44-45 | identified |
| Osiris, Isis, Apollo | figures | Egyptian/Greek myth | Images for division into many and gathering into one. | extracted p. 45 | identified |
| Job | biblical_text | Wisdom literature | Peace in the highest. | extracted p. 45 | identified |
| Empedocles | person | Greek philosophy | Strife and friendship interpret internal conflict. | extracted pp. 45-46 | identified |
| Heraclitus, Homer | persons/texts | Greek philosophy/poetry | Nature born of war/struggle. | extracted p. 46 | identified |
| Matthew and John | biblical_text | New Testament | Theology's peace and divine indwelling. | extracted pp. 46-47 | identified |
| Pythagoreans | school | Greek philosophy | Friendship as end of philosophy. | extracted p. 47 | identified |

## Pico Texts Discussed

- *On the Dignity of Man*

## Concepts and Themes

- Angelic ascent
- Purgation, illumination, perfection
- Moral philosophy, dialectic, natural philosophy, theology
- Concord of biblical, Greek, and Christian Neoplatonic authorities
- Peace as theological union

## Named Persons, Works, and Places

Moses, Paul, Dionysius, Jacob, Osiris, Isis, Apollo, Job, Empedocles, Heraclitus, Homer, Matthew, John, Pythagoreans.

## Historiographical Position

This section strongly supports reading the Oration as an ascetic and theological curriculum. It complicates any account that isolates the opening freedom passage from the rest of the speech.

## Textual / Philological Notes

The discipline sequence should be compared with the Latin terminology for moral science, dialectic, natural philosophy, and theology. Osiris/Apollo imagery should be cross-linked to Farmer's discussion of correlative thought.

## Knowledge Product Hooks

- Concept dossier: ladder of disciplines.
- Oration page: the disciplines as the engine of dignity.
- Theology/magic page: concordist use of pagan and biblical mysteries.

## Open Problems and Follow-Up Tasks

- Verify whether Pico's discipline sequence matches scholastic curricular order or intentionally revises it.
- Compare this passage with Copenhaver's claim that the Oration promotes ascetic mysticism.
- Link Osiris/Apollo division/gathering to Heptaplus mutual containment.

## Coverage Checklist

- [x] Section function stated.
- [x] All major argument moves listed.
- [x] All named references registered or deferred.
- [x] Claims are atomic and source-tethered.
- [x] Technical terms are explained.
- [x] Pico works and cross-links identified.
- [x] Uncertainties marked.
""",
    "artifacts/section_summaries/anthology/being_one_001_concord_problem.md": """# Section Summary: On Being and the One, Concord Problem and Plato

- Document ID: `Heptaplus_Pico_della_Mirandola_On_the_Dignity_of_Man_Being_and_One_pdf_29945776`
- Source file: `Heptaplus Pico della Mirandola On the Dignity of Man Being and One.pdf`
- Work / book: *On Being and the One*
- Section title: Proem, Chapter One, and Chapter Two
- Page range: extracted pages 72-76
- Section boundary basis: authorial proem and chapter headings
- Coverage level: SECTION_SUMMARIZED
- Review status: SOURCE_ANCHORED
- Evidence status: likely

## Section Function

This opening defines the problem of the work: whether Plato and Aristotle disagree about being and the one, and whether Platonists are right that the one is superior to being.

## Exhaustive Argument Summary

The proem places the treatise inside a Florentine conversation. Lorenzo de' Medici discussed being and the one with Angelo Poliziano, who was publicly commenting on Aristotle's *Ethics*. Lorenzo argued from Platonist reasons against Aristotle. Pico writes because Poliziano asked him how Aristotle could be defended and reconciled with Plato. The work is therefore not only metaphysical; it is explicitly concordist and social, tied to Lorenzo, Poliziano, Benivieni, and Pico's projected *Concord of Plato and Aristotle*.

Chapter One states the Platonist argument. Aristotle says that one, being, true, and good correspond and are coextensive. The Academy opposes this by claiming the one is prior because it is simpler and more universal. They call God one but not being, place prime matter under the one but outside being, and distinguish the opposite of being (nothing) from the opposite of one (multitude). Their conclusion is that being and one are not convertible.

Chapter Two asks where Plato actually speaks about being and the one. Pico identifies the *Parmenides* and the *Sophist*. He argues that the *Parmenides* does not clearly teach Platonist doctrine because it is a dialectical exercise, not a doctrinal work. Parmenides instructs Socrates in a method of considering what follows if something is and if it is not. Pico therefore treats the dialogue's claim that the one would not be being as hypothetical, not as proof that the one is absolutely above being. He then turns to the *Sophist*, where Plato's language supports the equality of one and something/being rather than the superiority of the one.

## Argument Map

| Move | Type | Content | Evidence |
|---|---|---|---|
| 1 | contextualizes | The treatise responds to Lorenzo, Poliziano, and Benivieni and anticipates the larger *Concord*. | extracted pp. 72-73 |
| 2 | defines | Platonists argue the one is prior to being because it is simpler and more universal. | extracted p. 73 |
| 3 | distinguishes | Opposites of being and one differ: nothing versus multitude. | extracted p. 73 |
| 4 | textualizes | Pico asks where Plato actually discusses the issue. | extracted p. 74 |
| 5 | rejects | The *Parmenides* is not clear doctrine but dialectical exercise. | extracted pp. 74-76 |
| 6 | qualifies | Even if the first hypothesis says the one would not be being, the statement is hypothetical. | extracted p. 76 |
| 7 | supports | The *Sophist* better supports equality between one and being/something. | extracted p. 76 |

## Claims and Subclaims

| Claim | Evidence | Claim type | Theme | Target | Confidence |
|---|---|---|---|---|---|
| The treatise is explicitly framed as a concordist defense of Aristotle and Plato. | extracted pp. 72-73 | textual | concord | On Being and the One | high |
| Pico presents the Platonist argument before refuting or qualifying it. | extracted p. 73 | textual | Platonism | being and one | high |
| Pico denies that the *Parmenides* straightforwardly teaches the one above being. | extracted pp. 74-76 | textual | Plato | Parmenides | high |
| Pico reads the *Parmenides* as dialectical method rather than doctrinal metaphysics. | extracted pp. 74-76 | interpretive | dialectic | Parmenides | high |
| Pico uses the *Sophist* to support convertibility of one and being. | extracted p. 76 | textual | Plato | Sophist | medium |

## Reference Register

| Reference | Type | Tradition/Field | Local Role | Evidence | Status |
|---|---|---|---|---|---|
| Lorenzo de' Medici | person | Renaissance patronage/philosophy | Raises the being/one problem. | extracted p. 72 | identified |
| Angelo Poliziano | person | Humanism/Aristotelian teaching | Addressee and participant in discussion. | extracted pp. 72-73 | identified |
| Aristotle's *Ethics* | work | Aristotelian philosophy | Poliziano's public commentary context. | extracted p. 72 | identified |
| Domenico Benivieni | person | Florentine network | Present at discussion. | extracted p. 72 | identified |
| *Concord of Plato and Aristotle* | work | Pico projected work | Larger project promised by Pico. | extracted p. 72 | identified |
| Aristotle, *Metaphysics* | work | Aristotelian metaphysics | Source for convertibility of being and one. | extracted p. 73 | identified |
| Plato, *Parmenides* | work | Platonism/dialectic | Platonist proof text reinterpreted by Pico. | extracted pp. 74-76 | identified |
| Plato, *Sophist* | work | Platonism/metaphysics | Supports equality of one and being. | extracted p. 76 | identified |
| Zeno | person | Eleatic/Platonic dialogue | Confirms dialectical exercise frame. | extracted pp. 74-75 | identified |

## Pico Texts Discussed

- *On Being and the One*
- Projected *Concord of Plato and Aristotle*

## Concepts and Themes

- Concord
- Being and one
- Dialectic
- Platonist interpretation
- Aristotelian convertibility

## Named Persons, Works, and Places

Lorenzo de' Medici, Poliziano, Benivieni, Aristotle, Plato, *Parmenides*, *Sophist*, Zeno.

## Historiographical Position

The section supports reading Pico as a semantic and scholastic reconciler, not merely a vague syncretist. Concord depends on disciplined reading of authorities.

## Textual / Philological Notes

Compare the translation's "one," "being," "something," and "nothing" with the Latin and Greek terms in Pico's argument.

## Knowledge Product Hooks

- Concept dossier: concord as semantic discipline.
- Work page: *On Being and the One*.
- Scholar synthesis: Howlett and Farmer on concord.

## Open Problems and Follow-Up Tasks

- Verify how Pico's reading of *Parmenides* compares with Ficino's.
- Track whether this argument anticipates Copenhaver's scholastic Pico.

## Coverage Checklist

- [x] Section function stated.
- [x] All major argument moves listed.
- [x] All named references registered or deferred.
- [x] Claims are atomic and source-tethered.
- [x] Technical terms are explained.
- [x] Pico works and cross-links identified.
- [x] Uncertainties marked.
""",
    "artifacts/section_summaries/anthology/heptaplus_001_moses_hidden_wisdom.md": """# Section Summary: Heptaplus, First Proem and Hidden Mosaic Wisdom

- Document ID: `Heptaplus_Pico_della_Mirandola_On_the_Dignity_of_Man_Being_and_One_pdf_29945776`
- Source file: `Heptaplus Pico della Mirandola On the Dignity of Man Being and One.pdf`
- Work / book: *Heptaplus*
- Section title: Publisher dedication and First Proem through hidden wisdom defense
- Page range: extracted pages 101-106
- Section boundary basis: authorial dedication/proem, generated subrange
- Coverage level: SECTION_SUMMARIZED
- Review status: SOURCE_ANCHORED
- Evidence status: likely

## Section Function

This section justifies the *Heptaplus* as a Genesis commentary and defends Moses against the charge that the creation account is philosophically crude or superficial.

## Exhaustive Argument Summary

The publisher's dedication presents the *Heptaplus* as Pico's Sevenfold Narration of the Six Days of Genesis, dedicated to Lorenzo de' Medici and worthy of correct publication because it contains natural and divine mysteries. Pico's own proem begins with Lorenzo's interest in Moses and with Pico's related work on the Psalms. Genesis matters because the six days of creation contain the secrets of all nature.

Pico then defends Moses as a philosophical and theological authority. Moses is inspired by God and the Holy Spirit, but he is also reported by Hebrew and gentile tradition as learned in human wisdom. Luke and Philo testify that Moses was learned in Egyptian lore; Greek philosophers such as Pythagoras, Plato, Empedocles, and Democritus took the Egyptians as teachers; Numenius called Plato an Attic Moses; Hermippus says Pythagoras borrowed from Mosaic law.

The core defense is esoteric. Ancient sages often either did not write religious matters or wrote them under coverings. Pico lists Indians, Ethiopians, Egyptians, sphinxes, Pythagorean silence, Platonic allegory, mathematical images, and unintelligible signs. He then shows the same principle in Christianity: Christ taught crowds in parables and disciples more openly; Matthew, John, Paul, and Dionysius all support graded disclosure. The plain surface of Moses therefore does not prove shallowness. It may indicate a text that veils wisdom for mixed audiences.

The result is a hermeneutic rule. If Moses treats the creation of the world, he must do so as the place where treasures of true philosophy are hidden. The creation narrative is privileged because it addresses the emanation of all things from God and the grade, number, and order of the world's parts.

## Argument Map

| Move | Type | Content | Evidence |
|---|---|---|---|
| 1 | contextualizes | Publisher and Pico tie the work to Lorenzo and to Genesis as natural/divine mystery. | extracted pp. 101-102 |
| 2 | defines | Genesis contains the secrets of all nature. | extracted p. 102 |
| 3 | authorizes | Moses is inspired and learned in Egyptian/human wisdom. | extracted pp. 102-103 |
| 4 | transmits | Greek philosophy is linked to Egyptian and Mosaic wisdom. | extracted p. 103 |
| 5 | historicizes | Ancient religious writers veil truth through silence, allegory, images, and figures. | extracted pp. 103-104 |
| 6 | parallels | Christian revelation also uses graded disclosure and parable. | extracted pp. 104-105 |
| 7 | concludes | Moses' surface simplicity can conceal philosophical depth. | extracted pp. 105-106 |

## Claims and Subclaims

| Claim | Evidence | Claim type | Theme | Target | Confidence |
|---|---|---|---|---|---|
| Pico treats Genesis as the place where secrets of all nature are contained. | extracted p. 102 | textual | Genesis | Heptaplus | high |
| The proem defends Moses as both inspired prophet and learned authority. | extracted pp. 102-103 | textual | Moses | Heptaplus | high |
| Pico's hermeneutics depends on a theory of veiled ancient wisdom. | extracted pp. 103-105 | interpretive | hermeneutics | hidden wisdom | high |
| The plain surface of Mosaic prose is not evidence of philosophical poverty. | extracted pp. 105-106 | textual | biblical exegesis | Moses | high |
| Creation is privileged because it concerns emanation from God and the order of the world's parts. | extracted p. 106 | textual | cosmology | Genesis | high |

## Reference Register

| Reference | Type | Tradition/Field | Local Role | Evidence | Status |
|---|---|---|---|---|---|
| Lorenzo de' Medici | person | Renaissance patronage | Dedicatee and reader of Moses. | extracted pp. 101-102 | identified |
| Psalms of David | biblical_text | Biblical exegesis | Pico's related interpretive project. | extracted p. 102 | identified |
| Moses | person/text | Biblical/Jewish/Christian | Central author and wisdom authority. | extracted pp. 102-106 | identified |
| Solomon/Wisdom | work/person | Jewish wisdom tradition | Secret-language wisdom source. | extracted p. 103 | needs_review |
| Luke and Philo | persons/texts | Christian/Jewish Hellenistic | Witness Moses' Egyptian learning. | extracted p. 103 | identified |
| Pythagoras, Plato, Empedocles, Democritus | persons | Greek philosophy | Greek recipients of Egyptian wisdom. | extracted p. 103 | identified |
| Numenius | person | Middle Platonism | Calls Plato an Attic Moses. | extracted p. 103 | identified |
| Hermippus | person | Greek grammar/Pythagorean tradition | Claims Pythagoras copied Mosaic law. | extracted p. 103 | identified |
| Indians, Ethiopians, Egyptians, sphinxes | peoples/symbols | Ancient wisdom | Examples of hidden religious communication. | extracted pp. 103-104 | needs_review |
| Dama, Philolaus, Lysis, Hipparchus | persons | Pythagorean tradition | Pythagorean secrecy examples. | extracted pp. 103-104 | identified |
| Christ, Matthew, John, Paul, Dionysius | persons/texts | Christian revelation | Graded disclosure and esoteric teaching. | extracted pp. 104-105 | identified |
| Jerome | person | Patristic/medieval exegesis | Reports age restriction on creation account. | extracted p. 106 | identified |

## Pico Texts Discussed

- *Heptaplus*
- Pico's Psalms project

## Concepts and Themes

- Genesis
- Hidden wisdom
- Esoteric communication
- Mosaic philosophy
- Emanation and order of creation

## Named Persons, Works, and Places

Lorenzo, Moses, David, Solomon, Luke, Philo, Pythagoras, Plato, Empedocles, Democritus, Numenius, Hermippus, Pythagorean figures, Christ, Matthew, John, Paul, Dionysius, Jerome.

## Historiographical Position

This section shows why the *Heptaplus* must be central to the portal: it directly states Pico's theory of hidden wisdom, Mosaic philosophy, and disciplined allegorical interpretation.

## Textual / Philological Notes

Several names and traditions need verification because the anthology notes include uncertain identifications. The reference to a secret language called Hierosolyma should be checked against Latin and modern scholarship.

## Knowledge Product Hooks

- Heptaplus page: Genesis as hidden natural philosophy.
- Concept dossier: esotericism and veiled wisdom.
- Reference graph: Moses-to-Greek-philosophy transmission claims.

## Open Problems and Follow-Up Tasks

- Compare Crofton Black's treatment of the *Heptaplus* with this proem.
- Check Wirszubski for how Kabbalah changes Pico's Mosaic hermeneutics.
- Track all Jewish commentators named later in the proem.

## Coverage Checklist

- [x] Section function stated.
- [x] All major argument moves listed.
- [x] All named references registered or deferred.
- [x] Claims are atomic and source-tethered.
- [x] Technical terms are explained.
- [x] Pico works and cross-links identified.
- [x] Uncertainties marked.
""",
    "artifacts/section_summaries/anthology/heptaplus_002_four_worlds_allegory.md": """# Section Summary: Heptaplus, Second Proem and the Four Worlds

- Document ID: `Heptaplus_Pico_della_Mirandola_On_the_Dignity_of_Man_Being_and_One_pdf_29945776`
- Source file: `Heptaplus Pico della Mirandola On the Dignity of Man Being and One.pdf`
- Work / book: *Heptaplus*
- Section title: Second Proem: three worlds, man as fourth world, and allegory
- Page range: extracted pages 110-114
- Section boundary basis: authorial second proem
- Coverage level: SECTION_SUMMARIZED
- Review status: SOURCE_ANCHORED
- Evidence status: likely

## Section Function

This section gives the cosmological structure that makes the *Heptaplus* possible: three worlds mutually contain one another, man contains them as a fourth lesser world, and allegory works because corresponding natures cross world-levels.

## Exhaustive Argument Summary

Pico begins with the ancient doctrine of three worlds. The highest is the ultramundane or angelic/intelligible world; the middle is the celestial world; the lowest is the sublunary world. He distinguishes them by light and darkness, fire and water, life and death, body and mind, stability and change. The sublunary world is unstable and corruptible; the angelic world is divine mind and eternal activity; the heavens mediate between them.

He then uses Moses' tabernacle as a diagram of the three worlds. The outer court, open to weather and containing clean and unclean men and animals, images the sublunary world. The sanctuary and Holy of Holies image the celestial and angelic worlds. The seven-branched candlestick marks the seven planets; the winged cherubim mark the angelic region. The tearing of the temple veil at Christ's death becomes a sign that the way to the supercelestial world has been opened.

The main metaphysical principle follows: the three worlds are one world not merely by common origin, end, harmony, or rank, but because whatever is in any one is contained in each of the others. Lower things exist in higher worlds in nobler form; higher things appear in lower worlds in degenerate or adulterated form. Fire exists as elemental fire, solar life-giving fire, and seraphic loving fire. Water exists as elemental moisture, lunar power, and cherubic understanding.

This mutual containment grounds allegory. Ancient fathers could symbolize one thing by another because they knew hidden alliances and affinities across nature. Without this correspondence, allegorical figures would be arbitrary. Finally, Pico adds a fourth world: man. Man is a lesser world containing elemental body, heavenly spirit, vegetative soul, sense, reason, angelic mind, and likeness of God. Moses, if he speaks fully of the world, must therefore speak of all four worlds, and Mosaic scripture becomes the exact image of the world.

## Argument Map

| Move | Type | Content | Evidence |
|---|---|---|---|
| 1 | defines | Antiquity imagined three worlds: angelic/intelligible, celestial, sublunary. | extracted pp. 110-111 |
| 2 | distinguishes | The worlds differ by light, fire/water, life/death, body/mind, motion, and governance. | extracted pp. 110-111 |
| 3 | allegorizes | Moses' tabernacle diagrams the three worlds. | extracted pp. 111-112 |
| 4 | Christianizes | Christ's death tears the veil and opens access to the supercelestial world. | extracted p. 112 |
| 5 | states principle | Whatever is in any world is contained in each of the others. | extracted pp. 112-113 |
| 6 | exemplifies | Fire and water appear differently across elemental, celestial, and angelic levels. | extracted pp. 112-113 |
| 7 | grounds method | Allegory depends on real cross-world affinities, not arbitrary comparison. | extracted pp. 113-114 |
| 8 | adds anthropology | Man is a fourth lesser world containing all the rest. | extracted p. 114 |

## Claims and Subclaims

| Claim | Evidence | Claim type | Theme | Target | Confidence |
|---|---|---|---|---|---|
| Pico's second proem defines a three-world cosmology of angelic, celestial, and sublunary worlds. | extracted pp. 110-111 | textual | cosmology | Heptaplus | high |
| The tabernacle is used as a Mosaic diagram of the worlds. | extracted pp. 111-112 | textual | allegory | tabernacle | high |
| Mutual containment of worlds is the core principle of the section. | extracted pp. 112-113 | textual | concord | worlds | high |
| Allegorical interpretation is justified by real affinities among worlds. | extracted pp. 113-114 | interpretive | hermeneutics | allegory | high |
| Man is the fourth world and contains all levels of reality in miniature. | extracted p. 114 | textual | anthropology | microcosm | high |

## Reference Register

| Reference | Type | Tradition/Field | Local Role | Evidence | Status |
|---|---|---|---|---|---|
| Plato, *Phaedrus* | work | Platonism | Authority for difficulty of singing the intelligible region. | extracted p. 110 | identified |
| Hebrew `asciamaim` | term | Hebrew/cosmology | Etymological fire/water explanation of heavens. | extracted p. 110 | needs_review |
| Moses' tabernacle | biblical_text/object | Exodus/biblical symbolism | Diagram of three worlds. | extracted pp. 111-112 | identified |
| Seven-branched candlestick | object | Biblical/celestial symbolism | Seven planets. | extracted p. 112 | identified |
| Cherubim | doctrine/figure | Angelology | Holy of Holies / angelic world. | extracted p. 112 | identified |
| Christ's death and temple veil | biblical_event | Gospel theology | Opens access to supercelestial world. | extracted p. 112 | identified |
| Anaxagoras | person | Greek philosophy | Possible source for mutual containment. | extracted p. 112 | identified |
| Pythagoreans and Platonists | schools | Greek philosophy | Expositors of mutual containment. | extracted p. 112 | identified |
| Psalms, Hebrews, Ezekiel | biblical_texts | Biblical symbolism | Scriptural support for cross-world names. | extracted pp. 113-114 | identified |
| Catholic doctors / schools | doctrine | Christian scholastic anthropology | Man as lesser world. | extracted p. 114 | identified |

## Pico Texts Discussed

- *Heptaplus*

## Concepts and Themes

- Three worlds
- Microcosm
- Mutual containment
- Allegory
- Tabernacle symbolism
- Angelic/celestial/sublunary hierarchy

## Named Persons, Works, and Places

Plato, Moses, Christ, Anaxagoras, Pythagoreans, Platonists, Psalms, Hebrews, Ezekiel.

## Historiographical Position

This section gives the portal a core ontology for Pico's biblical hermeneutics and natural correspondences. It also helps link the *Heptaplus* to Farmer's correlative-system account of Pico.

## Textual / Philological Notes

The Hebrew etymology of the heavens should be checked. The translation's "asciamaim" likely represents a transliterated form that needs standardization.

## Knowledge Product Hooks

- Concept dossier: mutual containment.
- Ontology: world-level, correspondence, microcosm.
- Website visualization: four-world diagram.
- Heptaplus page: allegory grounded in real affinities.

## Open Problems and Follow-Up Tasks

- Compare the four-world model with the Oration's human center and ascent.
- Compare Farmer's correlative systems with Pico's mutual containment.
- Build a cross-reference table for elemental/celestial/angelic analogues.

## Coverage Checklist

- [x] Section function stated.
- [x] All major argument moves listed.
- [x] All named references registered or deferred.
- [x] Claims are atomic and source-tethered.
- [x] Technical terms are explained.
- [x] Pico works and cross-links identified.
- [x] Uncertainties marked.
""",
    "artifacts/section_summaries/farmer/farmer_003_deciphering_substance_accident.md": """# Section Summary: Farmer, Deciphering the 900 Theses, Substance/Accident

- Document ID: `Medieval_Renaissance_Texts_Studies_167_Stephen_A_Farmer_Giovanni_Pico_Della_Mirandola_Syncretism_pdf_c99b971b`
- Source file: `Medieval Renaissance Texts Studies 167 Stephen A Farmer Giovanni Pico Della Mirandola Syncretism in the West_ Pico s 900 Theses The Evolution of Traditional Religious and Philosophical Systems 2003.pdf`
- Work / book: Stephen A. Farmer, *Syncretism in the West*
- Section title: Chapter 3 opening and "Pico's Syncretic Reading of the Substance/Accident Distinction"
- Page range: extracted pages 115-120
- Section boundary basis: authorial chapter/section heading
- Coverage level: SECTION_SUMMARIZED
- Review status: SOURCE_ANCHORED
- Evidence status: likely

## Section Function

This section demonstrates Farmer's method for reading the 900 Conclusions: isolate an apparently technical problem, collate scattered theses, and show how Pico's hidden syncretic system links metaphysics, epistemology, mysticism, and theological danger.

## Exhaustive Argument Summary

Farmer begins the chapter with Pico's own explanation from the *Apology*: debate propositions are brief, concise, and unexplained because their difficulties are meant to be resolved in disputation. The 900 Conclusions should therefore not be read as transparent standalone aphorisms. They are compressed debate nodes, often ambiguous by design.

The chapter's first test case is the Aristotelian substance/accident distinction. Farmer explains the ordinary distinction and then argues that Pico sometimes hierarchicalized it in an idiosyncratic way, especially in his "new philosophy." Thesis 3>23 reverses ordinary language: substantial forms exist in the second world as accidents, while accidental forms exist in the first world as substances. Farmer reads this as a Neoplatonic restatement of true substance existing in the intellectual realm and material forms as secondary images.

The method is comparative and collational. Farmer brings in the *Heptaplus* to support the reading and then compares several theses that appear to conflict. Thesis 3>61 says the whole substance of the rational soul is the intellectual part; thesis 2>65 says intellective power is an accident in us but substance in angels. The contradiction dissolves if substance and accident are read proportionally across levels. A nature can be substantial at one level and accidental relative to a higher level.

This flexibility has theological consequences. Medieval theologians used separable accidents to explain the Eucharist: bread and wine appearances remain while substance changes. Pico's view makes accidents inferior images of substance and pressures the ordinary doctrine. Farmer shows that several condemned theses attempt to preserve Eucharistic truth without separable accidents, which helps explain why the papal commission attacked them. The section ends by connecting the issue to intelligible species and epistemology: the substance/accident problem is not isolated but tied to how intellect, images, and hierarchy work in Pico's system.

## Argument Map

| Move | Type | Content | Evidence |
|---|---|---|---|
| 1 | defines | Debate propositions are concise because disputation resolves their difficulties. | extracted p. 115 |
| 2 | methodological | Farmer reads the theses by collation and commentary, not isolation. | extracted p. 115 |
| 3 | defines | Substance/accident distinction is introduced in ordinary Aristotelian terms. | extracted p. 115 |
| 4 | hierarchizes | Pico reworks substance/accident through world-level correspondence. | extracted pp. 116-117 |
| 5 | reconciles | Apparently conflicting theses harmonize when read proportionally. | extracted p. 117 |
| 6 | warns | The metaphysical strategy creates Eucharistic theological danger. | extracted pp. 117-118 |
| 7 | extends | The same problem connects to intelligible images, epistemology, and mystical theory. | extracted pp. 118-120 |

## Claims and Subclaims

| Claim | Evidence | Claim type | Theme | Target | Confidence |
|---|---|---|---|---|---|
| Farmer reads the 900 Conclusions as compressed debate propositions requiring reconstruction. | extracted p. 115 | methodological | 900 Conclusions | Farmer method | high |
| Pico's substance/accident usage can shift by hierarchical level. | extracted pp. 116-117 | interpretive | metaphysics | substance/accident | high |
| Collating theses resolves apparent contradiction between rational soul and angelic intellect claims. | extracted p. 117 | interpretive | thesis collation | 900 Conclusions | high |
| Pico's metaphysics of accidents made some Eucharistic theses dangerous. | extracted pp. 117-118 | historical | heresy | Eucharist | high |
| Farmer links substance/accident to epistemology and intelligible images. | extracted pp. 118-120 | interpretive | epistemology | intelligible species | high |

## Reference Register

| Reference | Type | Tradition/Field | Local Role | Evidence | Status |
|---|---|---|---|---|---|
| Pico's *Apology* | work | Pico/trial | Explains concise disputation propositions. | extracted p. 115 | identified |
| Aristotle / Aristotelian distinction | doctrine | Aristotelian metaphysics | Substance/accident baseline. | extracted p. 115 | identified |
| Thesis 3>23 | thesis | 900 Conclusions | Main reversal of substance/accident by world. | extracted p. 116 | identified |
| *Heptaplus* I.3 | work | Pico/cosmology | Supports Neoplatonic reading of substance. | extracted p. 116 | identified |
| Thesis 3>61 | thesis | 900 Conclusions | Rational soul substance claim. | extracted p. 117 | identified |
| Thesis 2>65 | thesis | 900 Conclusions | Intellective power as accident/substance by level. | extracted p. 117 | identified |
| Thomas Aquinas / medieval theologians | person/school | Scholastic theology | Separable accidents and Eucharist. | extracted pp. 117-118 | identified |
| Theses 4>1 and 4>2 | theses | 900 Conclusions/trial | Eucharistic alternatives attacked by papal commission. | extracted p. 118 | identified |
| Averroes and Albert | persons | Arabic/Latin Aristotelianism | Authorities in intelligible species debate. | extracted pp. 118-120 | identified |

## Pico Texts Discussed

- 900 Conclusions
- *Apology*
- *Heptaplus*

## Concepts and Themes

- Substance and accident
- Correlative hierarchy
- Thesis collation
- Eucharist and heresy risk
- Intelligible species

## Named Persons, Works, and Places

Pico, Farmer, Aristotle, Aquinas, Averroes, Albert, papal commission, *Apology*, *Heptaplus*, 900 Conclusions.

## Historiographical Position

This section is central to Farmer's claim that Pico's theses have hidden systematic links. It also supports Copenhaver's emphasis on scholastic/theological stakes in the trial.

## Textual / Philological Notes

Thesis numbering must be tracked consistently using Farmer's system. Eucharistic theses need comparison with Copenhaver's *Pico on Trial*.

## Knowledge Product Hooks

- Reading protocol: cluster-first thesis interpretation.
- Trial page: Eucharist and accidents.
- Ontology: `thesis_cluster`, `danger_level`, `doctrinal_risk`.

## Open Problems and Follow-Up Tasks

- Add a dedicated 900 Conclusions thesis table.
- Cross-link condemned theses with Copenhaver's thirteen-conclusions analysis.
- Track whether Farmer's claims about separable accidents are contested by later scholarship.

## Coverage Checklist

- [x] Section function stated.
- [x] All major argument moves listed.
- [x] All named references registered or deferred.
- [x] Claims are atomic and source-tethered.
- [x] Technical terms are explained.
- [x] Pico works and cross-links identified.
- [x] Uncertainties marked.
""",
}


ARTIFACT_ROWS = [
    ("sec_oration_001_wonder_indeterminacy", "section_summary", "Oration 001: Wonder and Human Indeterminacy", "artifacts/section_summaries/anthology/oration_001_wonder_indeterminacy.md", ANTHOLOGY, "Oration on the Dignity of Man", "SOURCE_ANCHORED", "likely"),
    ("sec_oration_002_disciplines_ladder", "section_summary", "Oration 002: Angelic Models and the Ladder of Disciplines", "artifacts/section_summaries/anthology/oration_002_disciplines_ladder.md", ANTHOLOGY, "Oration on the Dignity of Man", "SOURCE_ANCHORED", "likely"),
    ("sec_being_one_001_concord_problem", "section_summary", "On Being and the One 001: Concord Problem and Plato", "artifacts/section_summaries/anthology/being_one_001_concord_problem.md", ANTHOLOGY, "On Being and the One", "SOURCE_ANCHORED", "likely"),
    ("sec_heptaplus_001_moses_hidden_wisdom", "section_summary", "Heptaplus 001: Moses and Hidden Wisdom", "artifacts/section_summaries/anthology/heptaplus_001_moses_hidden_wisdom.md", ANTHOLOGY, "Heptaplus", "SOURCE_ANCHORED", "likely"),
    ("sec_heptaplus_002_four_worlds_allegory", "section_summary", "Heptaplus 002: Four Worlds and Allegory", "artifacts/section_summaries/anthology/heptaplus_002_four_worlds_allegory.md", ANTHOLOGY, "Heptaplus", "SOURCE_ANCHORED", "likely"),
    ("sec_farmer_003_substance_accident", "section_summary", "Farmer 003: Substance/Accident and Deciphering the 900 Theses", "artifacts/section_summaries/farmer/farmer_003_deciphering_substance_accident.md", FARMER, "900 Conclusions", "SOURCE_ANCHORED", "likely"),
]


CLAIMS = [
    ("claim_sec_oration_001", "sec_oration_001_wonder_indeterminacy", ANTHOLOGY, "The Oration's opening rejects standard praises of man as insufficient before defining human dignity through indeterminate form.", "textual", "human dignity", "Oration opening", "extracted pp. 38-40", "high", "DRAFT", "Pass 004 section summary claim."),
    ("claim_sec_oration_002", "sec_oration_002_disciplines_ladder", ANTHOLOGY, "The Oration's angelic ascent gives moral philosophy, dialectic, natural philosophy, and theology distinct ordered roles.", "textual", "philosophy", "Oration discipline ladder", "extracted pp. 42-49", "high", "DRAFT", "Pass 004 section summary claim."),
    ("claim_sec_being_001", "sec_being_one_001_concord_problem", ANTHOLOGY, "On Being and the One opens as a social and philosophical defense of concord between Plato and Aristotle.", "textual", "concord", "On Being and the One", "extracted pp. 72-73", "high", "DRAFT", "Pass 004 section summary claim."),
    ("claim_sec_heptaplus_001", "sec_heptaplus_001_moses_hidden_wisdom", ANTHOLOGY, "The Heptaplus first proem defends Moses' surface simplicity as veiled philosophical and theological depth.", "textual", "hermeneutics", "Heptaplus first proem", "extracted pp. 101-106", "high", "DRAFT", "Pass 004 section summary claim."),
    ("claim_sec_heptaplus_002", "sec_heptaplus_002_four_worlds_allegory", ANTHOLOGY, "The Heptaplus second proem grounds allegory in the mutual containment of angelic, celestial, sublunary, and human worlds.", "interpretive", "allegory", "Heptaplus second proem", "extracted pp. 110-114", "high", "DRAFT", "Pass 004 section summary claim."),
    ("claim_sec_farmer_001", "sec_farmer_003_substance_accident", FARMER, "Farmer's substance/accident example shows why the 900 Conclusions must be read by collating thesis clusters rather than isolating propositions.", "methodological", "900 Conclusions", "Farmer reading method", "extracted pp. 115-120", "high", "DRAFT", "Pass 004 section summary claim."),
]


CARDS = [
    ("system-section-style", "system", "Section Summary Style Guide", "Arguments, references, coverage", "PicoDB now has a formal style guide requiring every section summary to reconstruct argument moves, register references, extract claims, mark uncertainties, and name knowledge-product hooks.", "DRAFT", "sec_oration_001_wonder_indeterminacy"),
    ("system-coverage-protocol", "system", "Summary Coverage Protocol", "UNREAD to PROMOTED", "The reading system now tracks coverage levels from unread catalog entries through source packets, section summaries, claims, cross-links, review, and website promotion.", "DRAFT", "sec_farmer_003_substance_accident"),
]


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")


def load_seed_module():
    spec = importlib.util.spec_from_file_location("seed_research_artifacts", ROOT / "scripts" / "seed_research_artifacts.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load seed_research_artifacts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def update_ontology() -> None:
    path = ROOT / "data" / "reading_artifact_ontology.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version"] = "0.3.0"
    payload["coverage_levels"] = [
        "UNREAD",
        "SKIMMED",
        "SOURCE_PACKETED",
        "SECTION_SUMMARIZED",
        "CLAIM_EXTRACTED",
        "CROSS_LINKED",
        "REVIEWED",
        "PROMOTED",
    ]
    payload["section_summary_required_fields"] = [
        "bibliographic_anchor",
        "section_function",
        "exhaustive_argument_summary",
        "argument_map",
        "claims_and_subclaims",
        "reference_register",
        "pico_texts_discussed",
        "concepts_and_themes",
        "named_persons_works_places",
        "historiographical_position",
        "textual_philological_notes",
        "knowledge_product_hooks",
        "open_problems",
        "coverage_checklist",
    ]
    payload["argument_move_vocabulary"] = [
        "defines",
        "distinguishes",
        "rejects",
        "qualifies",
        "reconciles",
        "hierarchizes",
        "allegorizes",
        "historicizes",
        "textualizes",
        "philologizes",
        "transmits",
        "contests",
        "appropriates",
        "warns",
        "opens_problem",
    ]
    write_json(path, payload)


def write_coverage_manifest() -> None:
    records = [
        {
            "id": row[0],
            "document_id": row[4],
            "work_or_book": row[5],
            "section_title": row[2],
            "page_range": {
                "sec_oration_001_wonder_indeterminacy": "extracted pages 38-42",
                "sec_oration_002_disciplines_ladder": "extracted pages 42-49",
                "sec_being_one_001_concord_problem": "extracted pages 72-76",
                "sec_heptaplus_001_moses_hidden_wisdom": "extracted pages 101-106",
                "sec_heptaplus_002_four_worlds_allegory": "extracted pages 110-114",
                "sec_farmer_003_substance_accident": "extracted pages 115-120",
            }[row[0]],
            "artifact_path": row[3],
            "coverage_level": "SECTION_SUMMARIZED",
            "argument_coverage": "complete_for_current_pass",
            "reference_coverage": "registered_named_references_with_uncertainties",
            "claim_count": sum(1 for claim in CLAIMS if claim[1] == row[0]),
            "open_issues": [
                "verify Latin/Greek/Hebrew terms against critical editions",
                "cross-link references into future reference graph",
                "audit against scholarship before REVIEWED status",
            ],
        }
        for row in ARTIFACT_ROWS
    ]
    write_json(ROOT / "data" / "section_summary_coverage.json", records)


def main() -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    for path, text in SECTION_SUMMARIES.items():
        write(path, text)
    update_ontology()
    write_coverage_manifest()

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
    print("Study pass 004 complete.")


if __name__ == "__main__":
    main()
