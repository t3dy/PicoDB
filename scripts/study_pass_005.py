"""Study pass 005: scholarly values and Kabbalah reading protocol.

This pass close-reads the methodological values of Copenhaver, Edelheit,
Dougherty, and Howlett, then folds Busi and Wirszubski into the operating
protocol for Pico's Kabbalah, biblical allegory, and Heptaplus readings.
"""

from __future__ import annotations

import importlib.util
import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "pico.db"

DOCS = ROOT / "docs"
DATA = ROOT / "data"

DOC_IDS = {
    "copenhaver_magic": "Brian_P_Copenhaver_Magic_and_the_Dignity_of_Man__Pico_della_Mirandola_and_His_Oration_in_Modern__pdf_f7f272e1",
    "copenhaver_trial": "Brian_P_Copenhaver_Pico_della_Mirandola_on_Trial__Heresy_Freedom_and_Philosophy_libgen_li_pdf_753eb1fa",
    "edelheit_crossroads": "Amos_Edelheit_Maynooth_University_-_A_Philosopher_at_the_Crossroads_Giovanni_Pico_Della_Mirandol_pdf_dd0f01e6",
    "dougherty_new_essays": "M_V_Dougherty_Pico_della_Mirandola__New_Essays_libgen_li_pdf_78172345",
    "howlett_reevaluating": "Critical_Political_Theory_and_Radical_Practice_Sophia_Howlett_-_Re-evaluating_Pico__Aristotelian_pdf_3c6c4fa3",
    "busi_mito": "Giulio_Busi_Raphael_Ebgi_Giovanni_Pico_della_Mirandola_Mito_magia_Qabbalah_Einaudi_pdf_c382f352",
    "wirszubski_encounter": "Chaim_Wirszubski_Paul_Oskar_Kristeller_Pico_della_Mirandola_s_Encounter_with_Jewish_Mysticism_Ha_pdf_cd8c112f",
}


FILES = {
    "docs/SCHOLARLY_VALUES_STYLE_GUIDE.md": """# Scholarly Values Style Guide

This guide records the methodological values that must shape the next close-reading pass through Pico's writings and the scholarship around them. The goal is not merely to summarize what each scholar says, but to learn how each scholar teaches us to see evidence, arguments, omissions, and risks.

## Core Rule

Every close reading must identify the scholarly value being applied. A note should say whether it is working in a Copenhaver mode, an Edelheit mode, a Dougherty mode, a Howlett mode, a Busi mode, a Wirszubski mode, or some combination.

## Guide-Scholar Matrix

| Scholar | Values to Preserve | What to Look For in Pico | Risk if Ignored |
|---|---|---|---|
| Brian P. Copenhaver | Anti-mythic reconstruction, reception history, philological and theological precision, attention to juridical danger, willingness to formalize arguments. | Oration as ascetic and mystical program, Apology as scholastic defense, the thirteen condemned conclusions, Latin technical terms, public fame versus actual textual function. | We repeat the modern dignity myth, detach the Oration opening from the speech, or miss the doctrinal stakes of Pico's formulations. |
| Amos Edelheit | Resistance to reductive isms, restored Renaissance scholasticism, formation history, direct and indirect scholastic source tracing. | Padua and Paris formation, teachers, scholastic vocabulary, Albertist/Thomist/Scotist/Gilesian traces, manuscript or rare reception evidence. | Pico becomes only a Platonist, Kabbalist, or humanist and the philosophical medium of his work disappears. |
| M. V. Dougherty | Corpus breadth, collaborative specialism, edition status, reception range, genre awareness. | How each claim depends on a genre, edition, translation, bibliography, disciplinary boundary, or neglected work beyond the Oration. | The project becomes Oration-centered and overconfident about texts whose edition and reception histories are unstable. |
| Sophia Howlett | Pico as contested site, coherence across fragments, three pillars of Aristotelianism, Platonism, and Jewish Kabbalah, concord as both success and failure, exceptionalist ascent. | Whether a passage balances or privileges the three pillars; where concord reveals real difference; where Pico's mystical ascent is solitary, noetic, and exceptionalist. | We either flatten Pico into Ficino's orbit or assume concord is simple harmony rather than an experiment that exposes fractures. |
| Chaim Wirszubski | Hebrew/Kabbalistic philology, source identification, translation mediation, Mithridates' role, doctrinal specificity, evidentiary restraint. | Abulafia, Recanati, sefirot, Eyn-Sof, divine names, Hebrew-letter arguments, gematria, Mithridates translations and interpolations, Christianizing transformations. | Kabbalah becomes a vague aura instead of a recoverable source-field with language, witnesses, and uncertain degrees of proof. |
| Giulio Busi | Semitic canon expansion, Mithridates as shaping mediator, Kabbalah as praxis, symbolic inclusion, correspondences, theurgy and ars combinatoria. | Operational rather than merely contemplative Kabbalah, symbolic logic, scales of correspondence, rough debate architecture of the Conclusions, concrete technique versus abstract aim. | We miss Pico's practical, magical, and combinatory ambitions and reduce Kabbalah to doctrine alone. |

## Close-Reading Prompts

For every section of Pico or scholarship, answer these questions:

1. What myth, inherited label, or common simplification is this passage resisting or confirming?
2. What technical language must be checked in Latin, Greek, Hebrew, Aramaic, or a modern critical translation?
3. Which discipline or genre controls the passage: scholastic disputation, humanist rhetoric, biblical allegory, Kabbalah, magic, metaphysics, theology, philology, biography, or reception history?
4. What source-chain is active: direct quotation, indirect allusion, mediated translation, scholastic commonplace, manuscript witness, or later reception story?
5. Does concord succeed, fail, or expose a difference that Pico wants to preserve?
6. What is the practical or spiritual action implied by the argument: debate, ascent, purgation, illumination, perfection, magical operation, allegorical exegesis, or doctrinal defense?
7. What uncertainty must remain visible in the database and website prose?

## Artifact Requirements

Every scholarly-values source packet must include:

- methodological value extracted;
- evidence anchor in the scholarship;
- Pico passages affected;
- ontology fields to update;
- style-guide consequences;
- open problems for the next reading pass.

Every Pico primary-text section summary must now include a **Scholarly Values Overlay** naming which guide scholars should govern the next revision.
""",
    "docs/KABBALAH_READING_PROTOCOL.md": """# Kabbalah Reading Protocol

This protocol governs readings of Pico's Kabbalah in the Oration and 900 Conclusions, and readings of allegorical biblical hermeneutics or implicit Kabbalistic structures in the Heptaplus.

## Authority Order for Kabbalah Passes

Use Wirszubski and Busi as guide scholars whenever Pico's text involves Kabbalah, Hebrew, divine names, sefirot, Eyn-Sof, Abulafia, Recanati, Mithridates, magical operation, combinatory practice, or biblical allegory that may depend on Kabbalistic structures.

Use Wirszubski especially for:

- Hebrew and source-language dependence;
- Mithridates translations and interpolations;
- source identification;
- Abulafian and Recanatian materials;
- Christianizing transformation;
- evidentiary restraint.

Use Busi especially for:

- the practical and operational character of Kabbalah;
- the scale of correspondences;
- symbolic inclusion rather than only syllogistic logic;
- the rough debate architecture of the Conclusions;
- Mithridates as a brilliant, unstable, formative mediator;
- the extension of the humanist canon into Hebrew, Aramaic, and Arabic materials.

## Required Fields

Every Kabbalah-related note must fill these fields:

| Field | Question |
|---|---|
| Pico text | Oration, 900 Conclusions, Apology, Heptaplus, Commento, or another work. |
| Passage anchor | Page, thesis number, chapter, or section. |
| Kabbalistic source tradition | Abulafia, Recanati, Zoharic, sefirotic, divine-name, gematria, combinatory, or uncertain. |
| Source-language dependency | Does the argument require Hebrew, Aramaic, letter forms, numerical equivalence, or wordplay? |
| Translation witness | Is there evidence of Mithridates' Latin translations or another mediation? |
| Mediation risk | Low, medium, or high risk of translator interpolation, adaptation, or doctrinal coloring. |
| Doctrine class | Eyn-Sof, sefirot, divine names, angelology, creation, messianism, magic, ascent, prophecy, or hermeneutics. |
| Praxis/operation | Is this contemplative doctrine, ritual action, theurgy, ars combinatoria, magical operation, or disputational technique? |
| Christianizing move | How does Pico convert, redirect, or use the Jewish material for Christian theology? |
| Concord relation | Does the passage align Kabbalah with Plato, Aristotle, Dionysius, Orphic/Hermetic material, Chaldean Oracles, Lull, or scholastic theology? |
| Confidence | Verified, likely, interpretive, needs review, or contradicted. |

## Rules for Oration, 900 Conclusions, and Heptaplus

1. Do not call a passage Kabbalistic merely because it is allegorical, symbolic, or mystical. Name the evidence chain.
2. When reading the Oration, separate the famous opening anthropology from the later ascent, angelology, Kabbalah, and magic program.
3. When reading the 900 Conclusions, treat Kabbalistic conclusions as thesis nodes requiring source identification, language analysis, and debate context.
4. When reading the Heptaplus, test biblical allegory for Kabbalistic structures without assuming every correspondence is Kabbalah.
5. Always mark whether the Kabbalah is doctrinal, hermeneutical, magical, operational, or all of these.
6. Track how Pico changes Jewish materials to serve Christian theology.
7. Keep uncertain claims usable but visibly provisional.

## Output Pattern

Each Kabbalah source packet should end with:

- **Wirszubski check:** source, translation, Hebrew dependence, doctrinal precision, confidence.
- **Busi check:** praxis, symbolic inclusion, correspondence-scale, Mithridates effect, Semitic canon expansion.
- **Next Pico pass:** exact passages to revisit in Oration, 900 Conclusions, Heptaplus, or Apology.
""",
    "artifacts/historiography/scholarly_values_matrix.md": """# Scholarly Values Matrix

- Artifact ID: `hist_scholarly_values_matrix`
- Type: historiography node
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Problem

PicoDB needs a reading method that learns from the strongest Pico scholars before it returns to Pico's own texts. Copenhaver, Edelheit, Dougherty, and Howlett teach different scholarly virtues. Busi and Wirszubski supply the required guardrails for Kabbalah, biblical allegory, and the Heptaplus.

## Matrix

| Value | Copenhaver | Edelheit | Dougherty | Howlett | Busi | Wirszubski |
|---|---|---|---|---|---|---|
| Anti-mythic correction | Central | Strong | Moderate | Strong | Moderate | Strong |
| Scholastic precision | Strong | Central | Strong | Moderate | Moderate | Moderate |
| Corpus breadth | Strong | Strong | Central | Strong | Strong | Strong |
| Reception history | Central | Moderate | Strong | Strong | Moderate | Moderate |
| Kabbalistic source control | Strong | Moderate | Strong | Strong | Strong | Central |
| Praxis and magic | Strong | Moderate | Moderate | Moderate | Central | Strong |
| Concord as problem | Strong | Strong | Strong | Central | Strong | Strong |
| Edition and witness awareness | Strong | Strong | Central | Moderate | Strong | Central |

## Operating Consequence

The next primary-text pass should not ask only, "What does Pico say?" It should ask which disciplinary register and scholarly value makes the passage intelligible. Oration sections need Copenhaver and Howlett overlays; 900 Conclusions sections need Copenhaver, Farmer, Busi, Wirszubski, Dougherty, and Edelheit overlays; Heptaplus sections need Howlett, Busi, Wirszubski, and Edelheit overlays.

## Open Problems

- Build a thesis-level Kabbalah table for the 900 Conclusions.
- Add a witness table for Mithridates translations and known Hebrew sources.
- Separate Kabbalistic allegory from broader biblical, Platonic, Dionysian, and scholastic allegory in Heptaplus.
""",
    "artifacts/concepts/kabbalah_reading_protocol_seed.md": """# Concept Dossier: Kabbalah Reading Protocol Seed

- Artifact ID: `concept_kabbalah_protocol_seed`
- Type: concept dossier
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Concept

For PicoDB, "Kabbalah" is not a decorative label for Jewish-sounding mysticism. It is a source-sensitive, language-sensitive, and practice-sensitive field that includes Hebrew and Aramaic materials, mediated Latin translations, divine names, letter and number operations, sefirotic doctrine, Abulafian and Recanatian sources, Christian theological appropriation, and magical or theurgical praxis.

## Guide Scholars

Wirszubski supplies the main philological and source-control discipline: identify sources, translation witnesses, Mithridates' role, Hebrew dependence, and the exact doctrine being used.

Busi supplies the main operational and cultural discipline: treat Pico's Kabbalah as an expansion of the humanist canon into Semitic materials, and look for the practical, combinatory, symbolic, magical, and theurgical dimensions of the material.

## Reading Use

This concept dossier should be attached to all future summaries of:

- Oration passages on magic, Kabbalah, angelic ascent, and hidden wisdom;
- 900 Conclusions Kabbalistic, magical, Hermetic, Orphic, Chaldean, and Lullian thesis clusters;
- Heptaplus passages where biblical allegory, world-level correspondences, Hebrew etymology, or hidden Mosaic wisdom may depend on Kabbalistic structures.

## Open Problems

- Determine which Heptaplus correspondences are specifically Kabbalistic and which are broader Platonist, Aristotelian, Dionysian, or biblical allegory.
- Build a table of Mithridates translation witnesses and possible interpolation risks.
- Identify where Pico's Christianizing transformations change the doctrinal meaning of Jewish materials.
""",
}


SOURCE_PACKETS = {
    "artifacts/source_packets/copenhaver_scholarly_values.md": """# Source Packet: Copenhaver's Scholarly Values

- Artifact ID: `sp_copenhaver_scholarly_values`
- Documents: Copenhaver, *Magic and the Dignity of Man*; Copenhaver, *Pico della Mirandola on Trial*
- Evidence status: SOURCE_ANCHORED

## Local Summary

Copenhaver teaches PicoDB to resist the modern dignity myth and to read the Oration, 900 Conclusions, Apology, and Heptaplus through their actual theological, scholastic, juridical, Kabbalistic, and reception contexts. In *Magic and the Dignity of Man*, he treats the famous Oration as a text whose first pages have been detached from the speech's wider ascetic and mystical program. In *Pico on Trial*, he shifts attention to the Apology and the thirteen condemned conclusions, insisting that Pico's trial requires scholastic terminology, Latin precision, and theological logic.

## Scholarly Values

- Correct modern myths by returning to the whole text and its reception.
- Read fame, memory, art, popular culture, and scholarship as part of Pico's afterlife.
- Refuse to isolate the Oration's opening from the rest of the speech.
- Treat the Apology as public, juridical, academic, and scholastic.
- Track Latin terms, especially where translation hides technical danger.
- Use formalization, tables, and argument reconstruction when the theology requires it.
- Treat Pico's late works as late medieval as much as humanist.

## Pico Passes Affected

- Oration: reread beyond the opening dignity passage.
- 900 Conclusions: cluster condemned theses by doctrinal issue.
- Apology: track scholastic terms, theological constraints, and heresy risk.
- Heptaplus: read as part of a late medieval theological project, not only humanist allegory.

## Style-Guide Consequence

Every section summary must include a "myth corrected" field when the passage intersects modern myths of dignity, freedom, humanism, or proto-modernity.
""",
    "artifacts/source_packets/edelheit_scholarly_values.md": """# Source Packet: Edelheit's Scholarly Values

- Artifact ID: `sp_edelheit_scholarly_values`
- Document: Edelheit, *A Philosopher at the Crossroads*
- Evidence status: SOURCE_ANCHORED

## Local Summary

Edelheit teaches PicoDB to resist the easy labels that have long governed Pico studies. Pico should not be reduced to scholastic, Platonist, Kabbalist, or humanist. The reading task is to recover Renaissance scholasticism as a living medium of Pico's thought and to trace formation, references, teachers, school traditions, and reception.

## Scholarly Values

- Avoid reductive "Pico was X" formulas.
- Restore Renaissance scholasticism to the center of interpretation.
- Treat Padua and Paris formation as philosophically consequential.
- Track direct and indirect scholastic citations and traces.
- Recognize multiple scholasticisms rather than one inert scholastic background.
- Use manuscript-only and rarely discussed reactions where possible.

## Pico Passes Affected

- Oration: mark scholastic philosophical content beneath rhetorical performance.
- 900 Conclusions: tag Albertist, Thomist, Scotist, Gilesian, and other school traces.
- Apology: treat scholastic Latin as Pico's main argumentative medium.
- De ente et uno: read concord through scholastic metaphysical precision.

## Style-Guide Consequence

Every summary of Pico's philosophical argument must include a scholastic-source field: authority, school, citation type, and confidence.
""",
    "artifacts/source_packets/dougherty_scholarly_values.md": """# Source Packet: Dougherty's Scholarly Values

- Artifact ID: `sp_dougherty_scholarly_values`
- Document: Dougherty, ed., *Pico della Mirandola: New Essays*
- Evidence status: SOURCE_ANCHORED

## Local Summary

Dougherty teaches PicoDB to keep Pico's entire corpus, reception, editions, translations, and collaborative scholarly infrastructure in view. The introductory frame of *New Essays* emphasizes the variety of Pico's works and the impossibility of mastering Pico through a single disciplinary lens.

## Scholarly Values

- Resist Oration-only Pico by mapping the whole corpus.
- Track genre: speech, theses, defense, commentary, metaphysical treatise, biblical exegesis, letters, anti-astrology.
- Note edition and translation status before using a passage.
- Use specialist collaboration because Pico's learning outruns single-discipline reading.
- Register reception from Renaissance figures to modern historians.
- Track disciplinary boundaries, especially natural philosophy versus theology.

## Pico Passes Affected

- All primary texts: identify genre and edition status.
- 900 Conclusions and Apology: note disputational and juridical genre.
- Disputationes: distinguish science, superstition, and anti-astrology reception.
- Commento and De ente et uno: situate relative to Ficino and Aristotle/Plato concord.

## Style-Guide Consequence

Every source packet must state edition/translation status, genre, and whether a specialist bibliography check is needed.
""",
    "artifacts/source_packets/howlett_scholarly_values.md": """# Source Packet: Howlett's Scholarly Values

- Artifact ID: `sp_howlett_scholarly_values`
- Document: Howlett, *Re-evaluating Pico*
- Evidence status: SOURCE_ANCHORED

## Local Summary

Howlett teaches PicoDB to read Pico as a contested site rather than a fixed emblem. She moves away from Ficino-satellite and simple Platonic Academy models, stresses the coherence of Pico's fragmentary corpus, and organizes interpretation around Aristotelianism, Platonism, and Jewish Kabbalism.

## Scholarly Values

- Treat Pico's fragmentary works as potentially contiguous and coherent.
- Balance the three pillars: Aristotelianism, Platonism, Jewish Kabbalism.
- Ask where concord succeeds and where it exposes irreducible differences.
- Track Pico's exceptionalist ascetic and noetic ascent.
- Distinguish Pico from Ficino's renovatio and return-to-world model.
- Preserve the puzzle quality of Pico without turning it into vagueness.

## Pico Passes Affected

- Oration: solitary ascent and self-fashioning beyond modern dignity.
- 900 Conclusions: three-pillar concord and failure points.
- Heptaplus: allegorical coherence across biblical, philosophical, and Kabbalistic registers.
- De ente et uno and Commento: Plato/Aristotle concord and Ficino tension.

## Style-Guide Consequence

Every section summary must tag whether a passage is Aristotelian, Platonic, Kabbalistic, mixed, or a site where concord fails productively.
""",
    "artifacts/source_packets/wirszubski_kabbalah_method.md": """# Source Packet: Wirszubski's Kabbalah Method

- Artifact ID: `sp_wirszubski_kabbalah_method`
- Document: Wirszubski, *Pico della Mirandola's Encounter with Jewish Mysticism*
- Evidence status: SOURCE_ANCHORED

## Local Summary

Wirszubski gives PicoDB the source-critical foundation for Pico's Kabbalah. His method centers on Hebrew knowledge, the Latin translations made by Flavius Mithridates, Kabbalistic source identification, doctrinal precision, and the difference between what Pico received and how Pico Christianized it.

## Scholarly Values

- Identify Hebrew and Kabbalistic sources before interpreting doctrine.
- Track Mithridates' translations, interpolations, and explanatory notes.
- Distinguish Pico's knowledge before and after his Hebrew training.
- Treat Hebrew letter, name, and number arguments as language-dependent.
- Name doctrine: Eyn-Sof, sefirot, divine names, Abulafia, Recanati, or uncertain.
- Mark confidence and uncertainty carefully.

## Pico Passes Affected

- Oration: Kabbalah and magic claims.
- 900 Conclusions: Kabbalistic thesis clusters and source identification.
- Apology: defense of suspect Kabbalistic and theological claims.
- Heptaplus: three-world and hidden Mosaic wisdom structures where Kabbalistic origin is argued.

## Style-Guide Consequence

Every Kabbalah note must state source tradition, translation witness, Hebrew dependence, Mithridates mediation risk, Christianizing move, and confidence.
""",
    "artifacts/source_packets/busi_qabbalah_method.md": """# Source Packet: Busi's Qabbalah Method

- Artifact ID: `sp_busi_qabbalah_method`
- Document: Busi and Ebgi, *Mito, magia, Qabbalah*
- Evidence status: SOURCE_ANCHORED

## Local Summary

Busi teaches PicoDB to read Pico's qabbalah as a practical, symbolic, magical, and combinatory expansion of humanist learning into Semitic sources. Mithridates is not a neutral pipeline: he is brilliant, unstable, multilingual, and formative for Pico's project.

## Scholarly Values

- Treat Mithridates as teacher, translator, mediator, and distortion-risk.
- Read Kabbalah as action and operation, not only contemplation.
- Track symbolic inclusion: the logic in which everything can be contained in everything.
- Follow scales of correspondence from microcosm to macrocosm.
- Note the movement from syllogistic scholastic logic to symbolic ancient logic.
- Treat the Conclusions as raw debate architecture awaiting oral defense.

## Pico Passes Affected

- 900 Conclusions: magical, Kabbalistic, Hermetic, Orphic, Chaldean, and Lullian thesis clusters.
- Oration: practical ascent, magic, and Kabbalah as capstone of knowledge.
- Heptaplus: correspondences, hidden Mosaic wisdom, and possible Kabbalistic allegory.

## Style-Guide Consequence

Every Kabbalah or magic note must ask whether the passage describes an operation, a correspondence scale, a symbolic inclusion, a doctrinal proposition, or a debate tactic.
""",
}


PROFILES = {
    "artifacts/scholar_profiles/copenhaver_values_profile.md": """# Scholar Profile: Brian P. Copenhaver

- Artifact ID: `profile_copenhaver_values`
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Scholarly Identity

Brian P. Copenhaver is a major historian of Renaissance philosophy, magic, and Pico's modern reception. In the current PicoDB reading system, he is the guide scholar for anti-mythic reconstruction, the Oration's afterlife, the trial, the Apology, and the scholastic-theological stakes of Pico's dangerous claims.

## Arguments and Contributions

Copenhaver argues that modern readers have often invented a Pico who wrote a timeless manifesto of human dignity. His work redirects attention to the whole Oration, to ascetic mysticism, to Kabbalah, to magic, to the reception history that made Pico famous, and to the juridical-theological context of the 1487 crisis. In *Pico on Trial*, he makes the Apology and thirteen condemned conclusions central and shows why tiny technical terms could matter in a heresy proceeding.

## Historiographical Position

Copenhaver stands against celebratory humanist and proto-modern readings. His Pico is not a simple herald of modern freedom but a late medieval, scholastic, Kabbalistic, magical, and Christian thinker whose fame has often obscured the text.

## Use in PicoDB

Use Copenhaver whenever a passage touches the Oration myth, the Apology, the thirteen conclusions, scholastic semantics, theological danger, dignity reception, or Pico's fame.
""",
    "artifacts/scholar_profiles/edelheit_values_profile.md": """# Scholar Profile: Amos Edelheit

- Artifact ID: `profile_edelheit_values`
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Scholarly Identity

Amos Edelheit is a key guide for reading Pico through Renaissance scholasticism and intellectual formation. His value for PicoDB is methodological: he makes the project suspicious of labels and attentive to the scholastic languages Pico actually used.

## Arguments and Contributions

Edelheit argues that Pico cannot be understood by assigning him one label such as Platonist, Kabbalist, humanist, or scholastic. The task is to reconstruct how these worlds interact, especially through scholastic formation in Padua and Paris and through direct and indirect engagement with Albert, Aquinas, Scotus, Henry of Ghent, Giles of Rome, and other scholastic authorities.

## Historiographical Position

Edelheit corrects the humanist anti-scholastic prejudice that made scholasticism look like a dead background. For PicoDB, this means scholastic Latin and university formation are not background noise but primary evidence.

## Use in PicoDB

Use Edelheit for formation context, scholastic terminology, school-trace tagging, manuscript and reception evidence, and any place where Pico's philosophical argument risks being reduced to Platonism or Kabbalah alone.
""",
    "artifacts/scholar_profiles/dougherty_values_profile.md": """# Scholar Profile: M. V. Dougherty

- Artifact ID: `profile_dougherty_values`
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Scholarly Identity

M. V. Dougherty is a guide for corpus breadth, collaborative scholarship, edition awareness, and the many genres of Pico's writing. His edited volume *Pico della Mirandola: New Essays* models a multi-specialist approach to Pico.

## Arguments and Contributions

Dougherty frames Pico as a figure whose works and reception cannot be mastered from the Oration alone. The corpus includes theses, defenses, metaphysics, biblical commentary, letters, commentaries, and anti-astrology. The edition history and translation situation matter, and recent scholarship depends on tools, bibliographies, and collaborative projects.

## Historiographical Position

Dougherty's value is pluralist and infrastructural. PicoDB should treat every reading as dependent on genre, edition, translation, bibliography, and specialist competence.

## Use in PicoDB

Use Dougherty when cataloging genre, editions, translations, reception, bibliographies, disciplinary boundaries, and collaborative needs for future knowledge products.
""",
    "artifacts/scholar_profiles/howlett_values_profile.md": """# Scholar Profile: Sophia Howlett

- Artifact ID: `profile_howlett_values`
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Scholarly Identity

Sophia Howlett is a guide for re-evaluating Pico beyond Ficino-centered and Oration-centered frames. She treats Pico as a contested site organized around Aristotelianism, Platonism, and Jewish Kabbalism.

## Arguments and Contributions

Howlett argues for coherence across Pico's apparently fragmentary work and reads his central projects through poetic theology, philosophical concord, and the concord of Aristotle and Plato. She emphasizes that concord is not bland synthesis: it can reveal real differences. She also distinguishes Pico's exceptionalist, solitary, ascetic ascent from Ficino's broader renovatio.

## Historiographical Position

Howlett's Pico is neither simply Ficinian nor merely proto-modern. He is an exceptionalist thinker whose noetic ascent, Kabbalah, Aristotelianism, and Platonism must be held together.

## Use in PicoDB

Use Howlett to tag three-pillar balance, coherence across works, concord success and failure, exceptionalist ascent, and differences from Ficino.
""",
    "artifacts/scholar_profiles/busi_values_profile.md": """# Scholar Profile: Giulio Busi

- Artifact ID: `profile_busi_values`
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Scholarly Identity

Giulio Busi is a guide for Pico's qabbalah, magic, Semitic learning, and the operational character of symbolic knowledge. In PicoDB, Busi helps prevent Kabbalah from becoming a vague theme by making it practical, linguistic, mediated, and technical.

## Arguments and Contributions

Busi emphasizes Mithridates' formative role as translator, teacher, multilingual scholar, and unstable mediator. Pico's qabbalah is tied to action, theurgy, ars combinatoria, symbolic inclusion, and scales of correspondence. The 900 Conclusions are a raw debate machine in which scholastic syllogism and ancient symbolic logic coexist.

## Historiographical Position

Busi's Pico expands the humanist canon into Hebrew, Aramaic, and Arabic materials and makes Kabbalah part of a practical and magical path of intellectual ascent.

## Use in PicoDB

Use Busi for qabbalah as praxis, correspondence scales, Mithridates mediation, symbolic logic, magical operation, and the structure of the Conclusions.
""",
    "artifacts/scholar_profiles/wirszubski_values_profile.md": """# Scholar Profile: Chaim Wirszubski

- Artifact ID: `profile_wirszubski_values`
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Scholarly Identity

Chaim Wirszubski is the foundational guide for Pico's encounter with Jewish mysticism. His work gives PicoDB the source-critical discipline required for Kabbalah in the Oration, 900 Conclusions, Apology, and Heptaplus.

## Arguments and Contributions

Wirszubski reconstructs Pico's Hebrew learning, the Latin translations produced by Flavius Mithridates, the Jewish sources behind Pico's Kabbalistic conclusions, and the way Pico selected and transformed Jewish materials for Christian purposes. He is especially important for Abulafia, Recanati, divine names, sefirot, Eyn-Sof, magic, and the source-language dependence of Kabbalistic arguments.

## Historiographical Position

Wirszubski makes Christian Kabbalah a precise historical and philological object rather than a romantic generality. His restraint is as important as his discoveries: uncertainty must be marked, not hidden.

## Use in PicoDB

Use Wirszubski for source identification, translation witnesses, Hebrew dependence, Mithridates, doctrinal categories, Christianizing moves, and confidence ratings in every Kabbalah-related artifact.
""",
}


ARTIFACT_ROWS = [
    ("sp_copenhaver_scholarly_values", "source_packet", "Copenhaver's Scholarly Values", "artifacts/source_packets/copenhaver_scholarly_values.md", DOC_IDS["copenhaver_magic"], "Copenhaver method", "SOURCE_ANCHORED", "likely"),
    ("sp_edelheit_scholarly_values", "source_packet", "Edelheit's Scholarly Values", "artifacts/source_packets/edelheit_scholarly_values.md", DOC_IDS["edelheit_crossroads"], "Edelheit method", "SOURCE_ANCHORED", "likely"),
    ("sp_dougherty_scholarly_values", "source_packet", "Dougherty's Scholarly Values", "artifacts/source_packets/dougherty_scholarly_values.md", DOC_IDS["dougherty_new_essays"], "Dougherty method", "SOURCE_ANCHORED", "likely"),
    ("sp_howlett_scholarly_values", "source_packet", "Howlett's Scholarly Values", "artifacts/source_packets/howlett_scholarly_values.md", DOC_IDS["howlett_reevaluating"], "Howlett method", "SOURCE_ANCHORED", "likely"),
    ("sp_wirszubski_kabbalah_method", "source_packet", "Wirszubski's Kabbalah Method", "artifacts/source_packets/wirszubski_kabbalah_method.md", DOC_IDS["wirszubski_encounter"], "Kabbalah method", "SOURCE_ANCHORED", "likely"),
    ("sp_busi_qabbalah_method", "source_packet", "Busi's Qabbalah Method", "artifacts/source_packets/busi_qabbalah_method.md", DOC_IDS["busi_mito"], "Kabbalah method", "SOURCE_ANCHORED", "likely"),
    ("profile_copenhaver_values", "scholar_profile", "Brian P. Copenhaver Values Profile", "artifacts/scholar_profiles/copenhaver_values_profile.md", DOC_IDS["copenhaver_magic"], "Brian P. Copenhaver", "SOURCE_ANCHORED", "likely"),
    ("profile_edelheit_values", "scholar_profile", "Amos Edelheit Values Profile", "artifacts/scholar_profiles/edelheit_values_profile.md", DOC_IDS["edelheit_crossroads"], "Amos Edelheit", "SOURCE_ANCHORED", "likely"),
    ("profile_dougherty_values", "scholar_profile", "M. V. Dougherty Values Profile", "artifacts/scholar_profiles/dougherty_values_profile.md", DOC_IDS["dougherty_new_essays"], "M. V. Dougherty", "SOURCE_ANCHORED", "likely"),
    ("profile_howlett_values", "scholar_profile", "Sophia Howlett Values Profile", "artifacts/scholar_profiles/howlett_values_profile.md", DOC_IDS["howlett_reevaluating"], "Sophia Howlett", "SOURCE_ANCHORED", "likely"),
    ("profile_busi_values", "scholar_profile", "Giulio Busi Values Profile", "artifacts/scholar_profiles/busi_values_profile.md", DOC_IDS["busi_mito"], "Giulio Busi", "SOURCE_ANCHORED", "likely"),
    ("profile_wirszubski_values", "scholar_profile", "Chaim Wirszubski Values Profile", "artifacts/scholar_profiles/wirszubski_values_profile.md", DOC_IDS["wirszubski_encounter"], "Chaim Wirszubski", "SOURCE_ANCHORED", "likely"),
    ("hist_scholarly_values_matrix", "historiography_node", "Scholarly Values Matrix", "artifacts/historiography/scholarly_values_matrix.md", None, "Pico studies methodology", "SOURCE_ANCHORED", "likely"),
    ("concept_kabbalah_protocol_seed", "concept_dossier", "Kabbalah Reading Protocol Seed", "artifacts/concepts/kabbalah_reading_protocol_seed.md", DOC_IDS["wirszubski_encounter"], "Kabbalah reading protocol", "SOURCE_ANCHORED", "likely"),
]


CLAIMS = [
    ("claim_copenhaver_values_001", "sp_copenhaver_scholarly_values", DOC_IDS["copenhaver_magic"], "Copenhaver's Oration work requires PicoDB to read the whole speech and its reception history rather than isolating the famous dignity opening.", "methodological", "Oration reception", "Oration", "introductory pages", "high", "DRAFT", "Pass 005 scholarly-values extraction."),
    ("claim_copenhaver_values_002", "sp_copenhaver_scholarly_values", DOC_IDS["copenhaver_trial"], "Copenhaver's trial work requires close attention to scholastic Latin, theological logic, and the juridical stakes of the thirteen condemned conclusions.", "methodological", "heresy", "Apology and 900 Conclusions", "introductory pages", "high", "DRAFT", "Pass 005 scholarly-values extraction."),
    ("claim_edelheit_values_001", "sp_edelheit_scholarly_values", DOC_IDS["edelheit_crossroads"], "Edelheit's method rejects reductive labels and restores Renaissance scholasticism as a central medium of Pico's thought.", "methodological", "scholasticism", "Pico formation", "introduction", "high", "DRAFT", "Pass 005 scholarly-values extraction."),
    ("claim_edelheit_values_002", "sp_edelheit_scholarly_values", DOC_IDS["edelheit_crossroads"], "Edelheit requires source tracing through Padua, Paris, teachers, school traditions, and direct or indirect scholastic references.", "methodological", "source tracing", "Pico scholastic sources", "introduction", "high", "DRAFT", "Pass 005 scholarly-values extraction."),
    ("claim_dougherty_values_001", "sp_dougherty_scholarly_values", DOC_IDS["dougherty_new_essays"], "Dougherty's editorial frame makes corpus breadth, genre, edition status, translation status, and collaborative specialism mandatory metadata for PicoDB.", "methodological", "corpus", "Pico corpus", "introduction", "high", "DRAFT", "Pass 005 scholarly-values extraction."),
    ("claim_howlett_values_001", "sp_howlett_scholarly_values", DOC_IDS["howlett_reevaluating"], "Howlett's re-evaluation frames Pico as a contested but coherent thinker organized around Aristotelianism, Platonism, and Jewish Kabbalism.", "historiographical", "three pillars", "Pico studies", "preface and introduction", "high", "DRAFT", "Pass 005 scholarly-values extraction."),
    ("claim_howlett_values_002", "sp_howlett_scholarly_values", DOC_IDS["howlett_reevaluating"], "Howlett's concord model requires PicoDB to mark both successful harmonization and points where concord exposes real differences.", "methodological", "concord", "Pico concordism", "introduction", "high", "DRAFT", "Pass 005 scholarly-values extraction."),
    ("claim_wirszubski_values_001", "sp_wirszubski_kabbalah_method", DOC_IDS["wirszubski_encounter"], "Wirszubski requires Pico's Kabbalah to be read through Hebrew dependence, Mithridates' Latin translations, source identification, and Christianizing transformation.", "methodological", "Kabbalah", "Pico Kabbalah", "introductory chapters", "high", "DRAFT", "Pass 005 Kabbalah protocol."),
    ("claim_wirszubski_values_002", "sp_wirszubski_kabbalah_method", DOC_IDS["wirszubski_encounter"], "Wirszubski identifies Heptaplus world-structure and hidden Mosaic wisdom as places where Kabbalistic origin or influence must be tested with source precision.", "interpretive", "Heptaplus", "Heptaplus Kabbalah", "book structure and chapters", "medium", "DRAFT", "Pass 005 Kabbalah protocol."),
    ("claim_busi_values_001", "sp_busi_qabbalah_method", DOC_IDS["busi_mito"], "Busi requires PicoDB to treat qabbalah in Pico as operational praxis involving magic, theurgy, combinatory art, and symbolic correspondences.", "methodological", "magic", "Pico Kabbalah", "introductory sections", "high", "DRAFT", "Pass 005 Kabbalah protocol."),
    ("claim_busi_values_002", "sp_busi_qabbalah_method", DOC_IDS["busi_mito"], "Busi's account makes Mithridates a formative but risky mediator whose multilingual brilliance and instability shaped Pico's Conclusions.", "historiographical", "Mithridates", "900 Conclusions", "introductory sections", "high", "DRAFT", "Pass 005 Kabbalah protocol."),
    ("claim_protocol_001", "concept_kabbalah_protocol_seed", DOC_IDS["wirszubski_encounter"], "Future close readings of Kabbalah in the Oration, 900 Conclusions, and Heptaplus must record source tradition, translation witness, mediation risk, doctrine class, praxis, Christianizing move, concord relation, and confidence.", "methodological", "reading protocol", "Kabbalah reading protocol", "derived from Busi and Wirszubski", "high", "DRAFT", "Pass 005 ontology claim."),
]


CARDS = [
    ("values-copenhaver", "scholar", "Copenhaver's Scholarly Values", "Anti-myth, trial, technical danger", "Copenhaver now anchors the portal's resistance to the modern dignity myth and its close attention to the Oration as a whole, the Apology, scholastic Latin, and heresy stakes.", "DRAFT", "profile_copenhaver_values"),
    ("values-edelheit", "scholar", "Edelheit's Scholastic Trace Method", "Beyond reductive isms", "Edelheit now governs the portal's scholastic-source tagging: Padua, Paris, teachers, school traditions, and the Renaissance scholasticism that keeps Pico from collapsing into a single label.", "DRAFT", "profile_edelheit_values"),
    ("values-dougherty", "scholar", "Dougherty's Corpus Standard", "Genre, editions, collaboration", "Dougherty now supplies the corpus-wide discipline for PicoDB: every reading must know its genre, edition status, translation status, reception frame, and specialist needs.", "DRAFT", "profile_dougherty_values"),
    ("values-howlett", "scholar", "Howlett's Three-Pillar Re-evaluation", "Aristotle, Plato, Kabbalah", "Howlett now shapes readings of Pico as a coherent contested site where Aristotelianism, Platonism, and Jewish Kabbalism converge, succeed, and sometimes expose real differences.", "DRAFT", "profile_howlett_values"),
    ("protocol-busi-wirszubski", "system", "Busi-Wirszubski Kabbalah Protocol", "Source control plus praxis", "PicoDB now has a Kabbalah protocol for Oration, 900 Conclusions, and Heptaplus readings: Wirszubski governs source precision, while Busi governs praxis, correspondences, and Mithridates' formative mediation.", "DRAFT", "concept_kabbalah_protocol_seed"),
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


def update_docs() -> None:
    for path, text in FILES.items():
        write(path, text)
    append_once(
        DOCS / "ARGUMENT_REFERENCE_STYLE_GUIDE.md",
        "## Pass 005 Scholarly Values Overlay",
        """## Pass 005 Scholarly Values Overlay

Every argument and reference summary must now name its governing scholarly values. Use Copenhaver for anti-mythic Oration/trial readings, Edelheit for scholastic source-tracing, Dougherty for corpus/genre/edition awareness, Howlett for three-pillar concord and exceptionalist ascent, Wirszubski for Kabbalistic source control, and Busi for Kabbalah as praxis, correspondence, and symbolic operation.

For Kabbalah, magic, and hidden biblical wisdom, follow `docs/KABBALAH_READING_PROTOCOL.md` before promoting any claim above DRAFT.
""",
    )
    append_once(
        DOCS / "SECTION_SUMMARY_STYLE_GUIDE.md",
        "## Pass 005 Scholarly Values Overlay",
        """## Pass 005 Scholarly Values Overlay

Each section summary must include a short Scholarly Values Overlay:

- guide scholars applied;
- myth or label being tested;
- technical terms and source languages to check;
- scholastic, Kabbalistic, Platonic, Aristotelian, magical, biblical, or juridical register;
- concord outcome: success, failure, unresolved tension, or forced synthesis;
- Kabbalah protocol fields when relevant.
""",
    )


def update_ontology() -> None:
    path = DATA / "reading_artifact_ontology.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version"] = "0.4.0"
    payload["scholarly_value_dimensions"] = [
        "anti_mythic_reconstruction",
        "reception_history",
        "philological_precision",
        "scholastic_terminology",
        "analytic_formalization",
        "anti_reductive_labels",
        "formation_context",
        "scholastic_source_trace",
        "reaction_reception",
        "corpus_breadth",
        "genre_awareness",
        "edition_status",
        "collaborative_specialism",
        "contested_site",
        "three_pillars",
        "concord_success_failure",
        "exceptionalist_ascent",
        "kabbalistic_source_identification",
        "translation_witness",
        "source_language_dependency",
        "christianizing_transformation",
        "praxis_operation",
        "correspondence_scale",
        "symbolic_inclusion",
        "mithridates_mediation",
    ]
    payload["guide_scholars"] = {
        "Copenhaver": ["anti_mythic_reconstruction", "reception_history", "scholastic_terminology", "theological_juridical_risk"],
        "Edelheit": ["anti_reductive_labels", "formation_context", "scholastic_source_trace", "Renaissance scholasticism"],
        "Dougherty": ["corpus_breadth", "genre_awareness", "edition_status", "collaborative_specialism"],
        "Howlett": ["contested_site", "three_pillars", "concord_success_failure", "exceptionalist_ascent"],
        "Wirszubski": ["kabbalistic_source_identification", "translation_witness", "source_language_dependency", "christianizing_transformation"],
        "Busi": ["praxis_operation", "correspondence_scale", "symbolic_inclusion", "mithridates_mediation"],
    }
    payload["kabbalah_reading_fields"] = [
        "pico_text",
        "passage_anchor",
        "kabbalistic_source_tradition",
        "source_language_dependency",
        "translation_witness",
        "mithridates_mediation",
        "interpolation_risk",
        "doctrine_class",
        "praxis_operation",
        "christianizing_move",
        "concord_relation",
        "confidence",
    ]
    payload["section_summary_required_fields"] = list(dict.fromkeys(payload.get("section_summary_required_fields", []) + ["scholarly_values_overlay"]))
    write_json(path, payload)


def main() -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    update_docs()
    update_ontology()
    for path, text in SOURCE_PACKETS.items():
        write(path, text)
    for path, text in PROFILES.items():
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
    conn.commit()

    seed = load_seed_module()
    seed.export_data(conn)
    seed.build_site(conn)
    conn.close()
    print("Study pass 005 complete.")


if __name__ == "__main__":
    main()
