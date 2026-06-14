"""Study pass 009: Crofton Black, Heptaplus, and parallel essay program."""

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
    "black": "Studies_in_Medieval_and_Reformation_Traditions_66_Crofton_Black_-_Picos_Heptaplus_and_Biblical_H_pdf_98e6bcc6",
    "black_old": "Studies_in_Medieval_and_Reformation_Traditions_116_Pico_della_Mirandola_Giovanni_Black_Crofton_P_pdf_c20489cd",
    "black_balserak_review": "Sixteenth_Century_Journal_2008-oct_01_vol._39_iss._3_Pico_and__039_s_Heptaplus_and_Biblical_Herm_pdf_22679f7f",
    "black_aranoff_review": "The_Journal_of_Ecclesiastical_History_2008-oct_17_vol._59_iss._4_Pico_and__039_s_Heptaplus_and_b_pdf_29364950",
    "farmer": "Medieval_Renaissance_Texts_Studies_167_Stephen_A_Farmer_Giovanni_Pico_Della_Mirandola_Syncretism_pdf_c99b971b",
    "allen": "Studies_in_the_Platonism_of_Marsilio_Ficino_and_Giovanni_PicoMichael_J._B._AllenRoutledge1080299_epub_65585d05",
    "howlett": "Critical_Political_Theory_and_Radical_Practice_Sophia_Howlett_-_Re-evaluating_Pico__Aristotelian_pdf_3c6c4fa3",
    "edelheit": "Amos_Edelheit_Maynooth_University_-_A_Philosopher_at_the_Crossroads_Giovanni_Pico_Della_Mirandol_pdf_dd0f01e6",
    "salas": "The_Thomist__A_Speculative_Quarterly_Review_2014_jul_1_vol_78_iss_3_Salas_Victor_M_Giovanni_Pico_pdf_7f997dd5",
}

FILES = {
    "docs/HEPTAPLUS_BLACK_READING_PROTOCOL.md": """# Heptaplus and Crofton Black Reading Protocol

Status: DRAFT  
Created in study pass 009.

## Purpose

Crofton Black becomes PicoDB's guide scholar for the Heptaplus as biblical hermeneutics. Future Heptaplus notes must not treat the work as loose allegory. They should track its structure, exegetical theory, source traditions, and relation to the 900 Conclusions, Apology, Commento, and Pico's post-trial intellectual recovery.

## Required Tags

- genesis_anchor: Genesis 1.1-27, Bereshit, sabbath, or proem.
- heptaplus_unit: proem, exposition 1-7, first-word exposition, conclusion.
- exegetical_register: literal, allegorical, tropological, anagogical, kabbalistic, philosophical, cosmological.
- black_problem: outline, exegetical_context, esotericism, cosmic_model, anagogy, felicitas_intellect, bereshit_sabbath.
- source_family: patristic, scholastic, Dionysian, Neoplatonic, Arabic, Jewish, Kabbalistic, Ficinian, Pico-primary.
- authority_named: Aquinas, Pseudo-Dionysius, Proclus, Averroes, Avicenna, Al-Farabi, Ibn Bajja, Maimonides, Nahmanides, Gersonides, Recanati, Abulafia, Mithridates, Ficino, Lorenzo.
- relation_to_900: repeated source, thesis echo, post-trial recoding, silence, correction, expansion.
- concord_status: harmonizes, hierarchizes, strains, masks conflict, fails, unresolved.
- myth_risk: dignity myth, simple Kabbalah label, simple Platonism label, simple Thomism label, simple Averroism label.

## Black's Governing Rules

1. The Heptaplus has an architecture. Its sevenfoldness is not merely ornamental.
2. Pico's Genesis reading is anagogical in a Dionysian sense: interpretation leads the reader upward.
3. Biblical hermeneutics is tied to epistemology: exegesis concerns the ascent of intellect and felicitas.
4. Kabbalah is present, but it must be separated into specific traditions, witnesses, and functions.
5. Arabic and Jewish philosophical sources matter for the Heptaplus, especially in problems of intellect, felicity, and Moses' hidden knowledge.
6. Thomas Aquinas supplies crucial rules for scriptural senses and for anti-Averroist control, but Pico does not simply become Thomist.
7. The Heptaplus must be read after the Roman crisis: the 900 Conclusions and Apology are still in the background.
""",
    "artifacts/scholar_profiles/crofton_black_values_profile.md": """# Scholar Profile: Crofton Black

- Artifact ID: `scholar_crofton_black_values`
- Type: scholar profile
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Core Contribution

Crofton Black's *Pico's Heptaplus and Biblical Hermeneutics* gives PicoDB the strongest local guide to the Heptaplus as a biblical, philosophical, and hermeneutical system. Black's value is not just that he summarizes the work. He makes the Heptaplus legible as a structured interpretation of Genesis 1.1-27, governed by sevenfold architecture, esoteric theory, anagogical ascent, and a dense source field that includes Aquinas, Pseudo-Dionysius, Proclus, Averroes, Avicenna, Maimonides, Nahmanides, Gersonides, Recanati, and Abulafia.

## Scholarly Values

- Structure before paraphrase: the Heptaplus must be mapped by proems, seven expositions, Bereshit, sabbath, and final architecture.
- Hermeneutics before theme-tagging: Pico's biblical reading must be understood as a theory of interpretation.
- Source ecology: Black keeps patristic, scholastic, Dionysian, Neoplatonic, Jewish, Kabbalistic, and Arabic materials in play.
- Post-crisis continuity: the Heptaplus retains links to the Commento, Apology, and 900 Conclusions while changing genre and tone.
- Anagogy as method: exegesis is not only meaning extraction; it is ascent toward God.

## PicoDB Use

Use Black for every Heptaplus artifact, every essay on Pico's biblical hermeneutics, every study of Pico's Genesis sources, every comparison of the Heptaplus with the 900 Conclusions, and every claim about Pseudo-Dionysius, Aquinas, Averroes, Avicenna, Maimonides, Nahmanides, or Kabbalah inside the Heptaplus.
""",
    "artifacts/source_packets/black_heptaplus_structure_packet.md": """# Source Packet: Black's Heptaplus Structure

- Artifact ID: `source_black_heptaplus_structure`
- Type: source packet
- Status: SOURCE_ANCHORED
- Evidence status: likely
- Document: `Studies_in_Medieval_and_Reformation_Traditions_66_Crofton_Black_-_Picos_Heptaplus_and_Biblical_H_pdf_98e6bcc6`

## Table of Contents Control

Black divides the study into seven main chapters after the introduction:

1. Pico's life and works, including Hebrew studies.
2. The Heptaplus in outline: seven expositions, Bereshit, and conclusion.
3. Exegetical contexts: fifteenth-century biblical interpretation, rejected authorities, other commentaries.
4. First proem: Moses, philosophers, esotericism, early Christian hermeneutics, Neoplatonism, Pseudo-Dionysius, and Kabbalah.
5. Second proem: cosmic model and exegesis as anagogy.
6. Knowledge, felicitas, and hermeneutics: intellect in medieval philosophy, Pico's ascent to perfection, Gersonides, Genesis and knowledge.
7. Beginning and end: Bereshit, sabbath, jubilee, and forty-nine gates.

## Immediate Research Consequences

- The Heptaplus essay must be structured by Black's chapter problems, not merely by Pico's seven expositions.
- The Heptaplus must be connected backward to the 900 Conclusions and Apology and sideways to Commento.
- The key source families are: Aquinas/scholastic senses of scripture, Dionysian anagogy, Neoplatonic hierarchy, Arabic intellect tradition, Jewish Genesis commentary, and Kabbalistic gates/letters.
- The final Bereshit/sabbath problem is not decorative numerology; it is the key to the work's claim that Moses' text condenses the knowledge of created orders.
""",
    "artifacts/section_summaries/black/black_heptaplus_chapter_summaries_pass009.md": """# Section Summary: Black, Pico's Heptaplus and Biblical Hermeneutics

- Artifact ID: `summary_black_heptaplus_chapters`
- Type: section summary
- Status: SOURCE_ANCHORED_DRAFT
- Evidence status: likely

## Introduction

Black frames the Heptaplus as a unique intervention in allegorical biblical interpretation. The work is not simply a commentary on Genesis, nor simply a mystical appendix to Pico's more famous texts. It is a sevenfold philosophical exegesis that asks how Moses' apparently simple text can conceal natural, metaphysical, angelic, anthropological, and salvific knowledge.

## Chapter 1: Pico's Life and Works

Black places the Heptaplus after the 900 Conclusions crisis and in relation to Pico's Hebrew studies. The Roman scandal, the Apology, the Oration, Mithridates, Del Medigo, and the translated Hebrew/Kabbalistic corpus form the prehistory of the Heptaplus. The life chapter matters for PicoDB because it makes the Heptaplus a post-crisis work of synthesis rather than a detached Genesis exercise.

## Chapter 2: The Heptaplus in Outline

Black gives the structural map needed for section-by-section summary: first exposition on the elemental world; second on the celestial world; third on the angelic/invisible world; fourth on the human world; fifth on all worlds separately; sixth on the kinship of all things; seventh on felicity and eternal life; then the exposition of the first word, Bereshit. Pico's method is cumulative: Genesis becomes an image of ordered reality.

## Chapter 3: Exegetical Contexts

Black situates Pico in fifteenth-century biblical interpretation and compares him with authorities he uses, refuses, or exceeds. Aquinas is crucial for the theory of scriptural senses, but Black also shows that Pico's practice moves beyond ordinary scholastic exegesis. The chapter makes "biblical hermeneutics" an institutional and historical field rather than a vague spiritual label.

## Chapter 4: The First Proem

The first proem argues that Moses is a philosopher and that divine wisdom can be intentionally veiled. Black tracks three redactions of Pico's esoteric argument across Commento, Apology, and Heptaplus. This is essential: the Heptaplus does not invent esotericism from nowhere; it recasts a problem already active in Pico's earlier works and in the crisis around the Conclusions.

## Chapter 5: The Second Proem

The second proem supplies Pico's cosmic model and theory of exegesis as anagogy. The world structure is not only cosmological; it is interpretive. If worlds correspond, then Genesis can speak across registers. Pseudo-Dionysius becomes a governing source because anagogical reading leads the mind upward through sensible and symbolic forms toward divine realities.

## Chapter 6: Knowledge, Felicitas, and Hermeneutics

Black ties the Heptaplus to medieval theories of intellect and felicity. Averroes, Avicenna, Al-Farabi, Ibn Bajja, Maimonides, Gersonides, and Aquinas are not background names; they define the problem of what kind of intellectual perfection is possible. Pico's biblical hermeneutics becomes a theory of ascent: interpretation is related to the perfection and final happiness of the intellect.

## Chapter 7: Bereshit and the Sabbath

Black's final chapter makes the beginning and the end of Genesis bear the weight of the whole system. The opening word, Bereshit, and the sabbath/jubilee/forty-nine gates complex connect Kabbalistic and Jewish exegetical materials to Pico's claim that Moses condensed the knowledge of all created orders. This is one of the strongest places to connect Busi and Wirszubski with Black.

## Conclusion

Black's governing claim for PicoDB: the Heptaplus is an anagogical, source-dense, post-crisis biblical machine. It reads Genesis not by arbitrary allegory but by disciplined correspondences, source traditions, and a theory of intellectual ascent.
""",
    "artifacts/essays/pico_heptaplus_black_biblical_hermeneutics_draft.md": """# Essay Draft: Pico's Heptaplus and Biblical Hermeneutics

- Artifact ID: `essay_heptaplus_black_biblical_hermeneutics`
- Status: DRAFT
- Evidence status: SOURCE_ANCHORED_DRAFT

## Thesis

Pico's Heptaplus should be read as a post-Roman-crisis theory of biblical interpretation. It is not a loose allegorical flourish after the 900 Conclusions, and it is not merely a safer devotional work. Following Crofton Black, PicoDB should treat the Heptaplus as a sevenfold system in which Genesis 1.1-27 becomes a condensed map of creation, intellect, correspondence, and ascent. Its governing problem is how Moses' apparently simple words can contain natural philosophy, angelic hierarchy, human anthropology, eternal felicity, and the hidden structure of knowledge.

Black changes the portal's Heptaplus essay in three ways. First, he gives the work a durable architecture: proems, seven expositions, the exposition of Bereshit, sabbath, jubilee, and forty-nine gates. Second, he locates the Heptaplus inside traditions of biblical hermeneutics: scholastic fourfold senses, early Christian and patristic exegesis, Dionysian anagogy, Jewish Genesis commentary, and Kabbalistic secrecy. Third, he connects biblical interpretation to epistemology. The Heptaplus is not only about what Genesis means. It is about how the intellect ascends to knowledge and felicity.

The first proem presents Moses as philosopher. Pico confronts the problem that Moses' text looks rough, simple, and popular beside the philosophers. His answer is not that Moses lacks philosophy, but that Moses conceals it. This places the Heptaplus in the same esoteric family as the Commento and Apology. Pico had already used arguments about hidden wisdom to defend poetic, philosophical, and theological secrecy; now he brings that machinery to Genesis.

The second proem gives the cosmological key. Pico's worlds are not inert regions. They mutually contain and signify one another. The angelic, celestial, elemental, and human worlds are ordered in such a way that interpretation can pass between them. This is where the Heptaplus becomes Dionysian: symbols lead upward. Anagogy is not a label for a hidden meaning stored behind the literal sense; it is the movement of the reader through ordered symbols toward God.

Aquinas matters here, but not because Pico simply becomes Thomist. Aquinas provides a powerful account of scriptural senses and a disciplined Christian framework for allegory and anagogy. Yet Pico pushes that framework through Neoplatonic hierarchy, Kabbalistic concealment, Arabic theories of intellect, and Jewish Genesis traditions. The result is neither standard scholastic exegesis nor free allegorical invention.

The Arabic and Jewish philosophical materials are especially important. Black's chapter on knowledge and felicitas links the Heptaplus to Al-Farabi, Avicenna, Averroes, Ibn Bajja, Maimonides, Gersonides, and the broader debate over intellect. This gives the Heptaplus a sharper relation to the 900 Conclusions. The same problems of intellect, felicity, Averroism, and concord that appear in thesis form return in biblical form. Pico is not abandoning debate; he is recoding it through Moses.

The final Bereshit and sabbath material brings Kabbalah into the center without letting it absorb the whole text. The forty-nine gates of understanding, the sabbath, jubilee, and Mosaic ascent make Genesis a compressed archive of creation and knowledge. Here Busi and Wirszubski must govern source precision, while Black governs structure and hermeneutic function. The question is not "is the Heptaplus Kabbalistic?" but where Kabbalistic materials help Pico explain how Moses concealed the created orders and the path of ascent.

The Heptaplus therefore belongs near the center of the portal. It ties together Genesis, Dionysius, Aquinas, Proclus, Arabic intellect theory, Jewish exegesis, Kabbalah, the 900 Conclusions, and Pico's late religious seriousness. It is the best test case for PicoDB's method: a work cannot be understood by one label. It must be read as a structured field of sources, genres, arguments, and transformations.
""",
    "artifacts/essays/pico_platonism_aristotelianism_concord_draft.md": """# Essay Draft: Pico Between Plato and Aristotle

- Artifact ID: `essay_pico_plato_aristotle_concord`
- Status: DRAFT
- Evidence status: SOURCE_ANCHORED_DRAFT

## Thesis

Pico's relation to Platonism and Aristotelianism should be treated as controlled instability rather than simple concord. Howlett's three-pillar Pico, Edelheit's scholastic Pico, Allen's contentious co-Platonism, and Farmer's thesis architecture all point to the same conclusion: Pico does not merely harmonize Plato and Aristotle; he builds a machine in which their agreement can be asserted, tested, strained, and sometimes left unresolved.

The 900 Conclusions stage this problem most publicly. Pico arranges traditions in thesis clusters and adds theses according to his own opinion. Aristotle, Averroes, Avicenna, Alexander, Themistius, Simplicius, Proclus, Iamblichus, and Plato are not ornamental authorities. They become nodes in a public system. The form of the work matters: concord is proposed as disputation, not as quiet synthesis.

On Being and Unity sharpens the question. Pico wants to reconcile Plato and Aristotle on being and the One, but Allen shows that the treatise is also a correction of Ficino's Proclean Plato. The apparent concord is polemical. Pico can defend Aristotle while still working inside a Platonic and Neoplatonic source field. The essay should therefore ask: when Pico invokes concord, whose interpretation is being corrected?

The Heptaplus gives a biblical version of the same method. Moses becomes the philosopher whose text can contain what the schools dispute. Black shows that the Heptaplus harmonizes Aristotle, Avicenna, Averroes, Dionysius, Jewish commentary, and Kabbalah through Genesis. But this is not a flattening harmony. It is a hierarchy of meanings governed by scriptural concealment and anagogical ascent.

The core essay should argue that Pico's concord is not a doctrine of easy agreement. It is a practice: collect authorities, translate them into common problems, distinguish registers, defend compatibility where possible, and let unresolved tensions remain productive.
""",
    "artifacts/essays/pico_being_unity_aquinas_dionysius_draft.md": """# Essay Draft: Aquinas and Dionysius in On Being and Unity

- Artifact ID: `essay_being_unity_aquinas_dionysius`
- Status: DRAFT
- Evidence status: SOURCE_ANCHORED_DRAFT

## Thesis

On Being and Unity should be read as a Christian metaphysical intervention in the dispute over Plato, Aristotle, Ficino, Aquinas, and Dionysius. Pico's surface aim is concord: being and unity are not divided in such a way that Plato and Aristotle truly oppose one another. But the treatise is more than a diplomatic settlement. It is a test of how far Neoplatonic transcendence can be accepted without damaging Christian doctrine.

Aquinas is crucial because he gives Pico a way to speak of being, unity, creation, and the convertibility of transcendentals without surrendering to a Proclean hierarchy in which the One stands above being in a way that threatens Christian metaphysics. Salas and Edelheit can govern the Thomistic and scholastic side of this problem. The close reading should track where Pico's distinctions echo or resist Aquinas: being as common, divine simplicity, created participation, and the relation between names and God.

Dionysius complicates the picture. Dionysian negative theology and hierarchy give Christian authority to the language of ascent, excess, hiddenness, and divine transcendence. Allen's work on Ficino and Pico suggests that Pico is not simply rejecting Neoplatonism. He is policing it. Dionysius allows a Christian Platonism that can speak of God's supereminence while avoiding an un-Christian separation of the One from being.

This essay should therefore be built as a triangle: Aquinas disciplines metaphysical language; Dionysius authorizes apophatic ascent; Ficino's Proclean reading creates the pressure Pico answers. The resulting Pico is neither anti-Platonic nor merely Thomist. He is trying to Christianize the deepest Platonic metaphysical problem by forcing it through scholastic distinctions.
""",
    "artifacts/essays/pico_900_own_opinion_theses_draft.md": """# Essay Draft: Pico's Theses According to His Own Opinion

- Artifact ID: `essay_900_own_opinion_theses`
- Status: DRAFT
- Evidence status: SOURCE_ANCHORED_DRAFT

## Thesis

The theses "according to Pico's own opinion" should become a separate database object. They are the place where Pico stops acting only as collector of authorities and openly becomes architect. Farmer's edition and numbering make this possible: the project should isolate every "secundum opinionem propriam" cluster and tag its theme, source dependencies, linked traditions, doctrinal risk, and relation to Pico's other works.

This essay should ask what "own opinion" means in a syncretic work. It does not mean pure originality. Pico's own positions often depend on inherited materials: Platonic, Aristotelian, Kabbalistic, magical, theological, and scholastic. The originality lies in recombination, hierarchy, and argumentative placement.

The Kabbalistic conclusions according to his own opinion are especially important. Black, Busi, and Wirszubski show that Pico's Kabbalah depends on translations, Jewish sources, Mithridates, Recanati, Abulafia, and Christianizing transformation. "Own opinion" may mark Pico's most creative and risky appropriation of source materials.

The metaphysical own-opinion theses should be read with Allen and Edelheit: hypostasis, soul, intellect, being, unity, and concord are not separable from scholastic forms. The magical and Orphic/Hermetic own-opinion materials should be read with Copenhaver and Farmer as part of the trial danger-field.

The deliverable should be a thesis table, then an essay. Fields: thesis number, cluster, Latin incipit, source family, source witness, doctrine, Pico transformation, related work, danger status, and confidence.
""",
    "artifacts/essays/pico_neoplatonist_arab_authors_900_draft.md": """# Essay Draft: Neoplatonist and Arabic Authors in the 900 Conclusions

- Artifact ID: `essay_900_neoplatonist_arab_authors`
- Status: DRAFT
- Evidence status: SOURCE_ANCHORED_DRAFT

## Thesis

The 900 Conclusions should be read as Pico's most explicit map of learned transmission. The Neoplatonist and Arabic authors are not marginal ornaments. They let Pico build a larger genealogy of wisdom in which Plato, Aristotle, their commentators, Arabic philosophers, Jewish thinkers, and Christian theologians become disputable witnesses to one structure of truth.

For the Neoplatonists, Allen and Farmer should govern the pass. Proclus, Plotinus, Iamblichus, Porphyry, the Chaldean Oracles, Orphic materials, and Pseudo-Dionysius must be separated rather than merged into a single "Neoplatonism" tag. The question is always: is Pico using a doctrine of hypostases, a symbolic theology, a theory of ascent, a magical/theurgical register, or a thesis inherited through Ficino?

For the Arabic authors, Black and Edelheit are crucial. Averroes, Avicenna, Al-Farabi, Ibn Bajja, and related traditions enter through problems of intellect, felicity, soul, and Aristotle's interpreters. Pico's Arabic field is not simply "Averroism." It includes disagreement among Arabic philosophers, Latin scholastic reception, Jewish transmission, and Christian correction.

The essay should make the 900 Conclusions a source-network map: each author cluster must be tagged by doctrine, mediation, language route, relation to Aristotle/Plato, and later reuse in Heptaplus, On Being and Unity, or Apology.
""",
    "artifacts/essays/pico_arab_intellect_felicitas_draft.md": """# Essay Draft: Pico and the Arabic Intellect Tradition

- Artifact ID: `essay_pico_arab_intellect_felicitas`
- Status: DRAFT
- Evidence status: SOURCE_ANCHORED_DRAFT

## Thesis

Pico's engagement with Arabic philosophy should be organized around intellect and felicitas. Black's Heptaplus study makes this especially clear: Averroes, Avicenna, Al-Farabi, Ibn Bajja, Maimonides, and Gersonides form a problem-field around whether human perfection involves conjunction with intellect, what kind of knowledge is possible in this life, and how philosophical felicity relates to Christian beatitude.

This topic links Padua, Elia del Medigo, the 900 Conclusions, the Heptaplus, and Aquinas. Aquinas matters as the anti-Averroist and as a guide to what Christian theology can accept. Averroes matters not only as a condemned or dangerous thinker but as a transmitter of Aristotle and as an author whose views on intellect force Pico to distinguish philosophical, theological, and biblical registers.

The Heptaplus recodes this debate through Genesis. Moses' hidden knowledge and the ascent of the intellect turn philosophical felicity into biblical hermeneutics. Pico does not simply quote Arab authors; he translates their problem into a Christian-Mosaic theory of ascent.
""",
    "artifacts/essays/pico_dionysian_anagogy_draft.md": """# Essay Draft: Pseudo-Dionysius and Pico's Anagogical Method

- Artifact ID: `essay_pico_dionysian_anagogy`
- Status: DRAFT
- Evidence status: SOURCE_ANCHORED_DRAFT

## Thesis

Pseudo-Dionysius is one of the bridges that lets Pico move between Platonism, Christian theology, biblical hermeneutics, and mystical ascent. In the Oration, Dionysian hierarchy helps explain ascent through angelic orders. In On Being and Unity, Dionysian apophasis helps control the language of divine transcendence. In the Heptaplus, Black shows that Dionysian anagogy becomes a theory of how scriptural symbols lead the intellect upward.

The key move is to stop treating Dionysius as a decorative authority. Dionysius gives Pico a Christian version of Neoplatonic hierarchy and hidden teaching. That is why Aquinas's commentary on Dionysius matters: the Dionysian material reaches Pico through scholastic as well as Platonist channels.

This essay should compare three Dionysian functions: hierarchy, negative theology, and anagogical exegesis. It should ask how each function appears in Oration, On Being and Unity, Heptaplus, and the 900 Conclusions.
""",
    "artifacts/essays/pico_heptaplus_after_oration_draft.md": """# Essay Draft: The Heptaplus After the Oration

- Artifact ID: `essay_heptaplus_after_oration`
- Status: DRAFT
- Evidence status: SOURCE_ANCHORED_DRAFT

## Thesis

The Heptaplus should be read as Pico's post-Oration and post-trial reconfiguration of the same ambition. The Oration introduces a public debate that fails under papal scrutiny. The Heptaplus turns from public disputation to Mosaic interpretation, but it does not abandon concord, ascent, Kabbalah, or philosophical ambition.

Copenhaver corrects the modern myth of the Oration; Black corrects the neglect of the Heptaplus. Together they show that Pico's central work is not the opening dignity passage but the larger project of ascent through disciplines, sources, and hidden wisdom. The Heptaplus shifts the stage from Rome to Genesis.

The essay should argue that the Heptaplus is not retreat but recoding. It keeps the 900 Conclusions' source density while changing genre. It keeps Kabbalah while embedding it in Genesis and sabbath structure. It keeps Neoplatonic ascent while giving it Dionysian and biblical form.
""",
}

ARTIFACT_ROWS = [
    ("scholar_crofton_black_values", "scholar_profile", "Crofton Black Values Profile", "artifacts/scholar_profiles/crofton_black_values_profile.md", DOCS_BY_KEY["black"], "Crofton Black", "SOURCE_ANCHORED", "likely"),
    ("source_black_heptaplus_structure", "source_packet", "Black's Heptaplus Structure", "artifacts/source_packets/black_heptaplus_structure_packet.md", DOCS_BY_KEY["black"], "Heptaplus", "SOURCE_ANCHORED", "likely"),
    ("summary_black_heptaplus_chapters", "section_summary", "Black Heptaplus Chapter Summaries", "artifacts/section_summaries/black/black_heptaplus_chapter_summaries_pass009.md", DOCS_BY_KEY["black"], "Black Heptaplus", "SOURCE_ANCHORED_DRAFT", "likely"),
    ("essay_heptaplus_black_biblical_hermeneutics", "website_page", "Pico's Heptaplus and Biblical Hermeneutics", "artifacts/essays/pico_heptaplus_black_biblical_hermeneutics_draft.md", DOCS_BY_KEY["black"], "Heptaplus", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("essay_pico_plato_aristotle_concord", "website_page", "Pico Between Plato and Aristotle", "artifacts/essays/pico_platonism_aristotelianism_concord_draft.md", DOCS_BY_KEY["howlett"], "Platonism and Aristotelianism", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("essay_being_unity_aquinas_dionysius", "website_page", "Aquinas and Dionysius in On Being and Unity", "artifacts/essays/pico_being_unity_aquinas_dionysius_draft.md", DOCS_BY_KEY["salas"], "On Being and Unity", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("essay_900_own_opinion_theses", "website_page", "Pico's Own-Opinion Theses", "artifacts/essays/pico_900_own_opinion_theses_draft.md", DOCS_BY_KEY["farmer"], "900 Conclusions", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("essay_900_neoplatonist_arab_authors", "website_page", "Neoplatonist and Arabic Authors in the 900 Conclusions", "artifacts/essays/pico_neoplatonist_arab_authors_900_draft.md", DOCS_BY_KEY["farmer"], "900 Conclusions source networks", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("essay_pico_arab_intellect_felicitas", "website_page", "Pico and the Arabic Intellect Tradition", "artifacts/essays/pico_arab_intellect_felicitas_draft.md", DOCS_BY_KEY["black"], "Arabic intellect tradition", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("essay_pico_dionysian_anagogy", "website_page", "Pseudo-Dionysius and Pico's Anagogical Method", "artifacts/essays/pico_dionysian_anagogy_draft.md", DOCS_BY_KEY["black"], "Dionysian anagogy", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ("essay_heptaplus_after_oration", "website_page", "The Heptaplus After the Oration", "artifacts/essays/pico_heptaplus_after_oration_draft.md", DOCS_BY_KEY["black"], "Heptaplus and Oration", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
]

CLAIMS = [
    ("claim_black_009_001", "scholar_crofton_black_values", DOCS_BY_KEY["black"], "Crofton Black should govern PicoDB's Heptaplus readings because he treats the work as structured biblical hermeneutics rather than loose allegory.", "methodological", "Heptaplus", "Crofton Black", "Black monograph", "high", "DRAFT", "Pass 009."),
    ("claim_black_009_002", "essay_heptaplus_black_biblical_hermeneutics", DOCS_BY_KEY["black"], "The Heptaplus is best read as an anagogical system in which Genesis 1.1-27 encodes knowledge of created orders and intellectual ascent.", "interpretive", "Heptaplus", "Heptaplus", "Black synthesis", "high", "DRAFT", "Pass 009."),
    ("claim_black_009_003", "essay_heptaplus_black_biblical_hermeneutics", DOCS_BY_KEY["black"], "Black links the Heptaplus to the 900 Conclusions, Apology, and Commento, making it a post-crisis recoding of Pico's earlier esoteric and concordist problems.", "historiographical", "Heptaplus", "Heptaplus corpus relation", "Black synthesis", "high", "DRAFT", "Pass 009."),
    ("claim_black_009_004", "essay_pico_arab_intellect_felicitas", DOCS_BY_KEY["black"], "Pico's Arabic source field should be organized around intellect and felicitas, especially Averroes, Avicenna, Al-Farabi, Ibn Bajja, and their Christian/Jewish reception.", "methodological", "Arabic philosophy", "Pico and Arabic authors", "Black chapter 6 synthesis", "high", "DRAFT", "Pass 009."),
    ("claim_black_009_005", "essay_pico_dionysian_anagogy", DOCS_BY_KEY["black"], "Pseudo-Dionysius gives Pico a Christian Neoplatonic model of hierarchy, hidden teaching, and anagogical ascent.", "interpretive", "Dionysius", "Pico's anagogy", "Black/Allen synthesis", "high", "DRAFT", "Pass 009."),
    ("claim_black_009_006", "essay_being_unity_aquinas_dionysius", DOCS_BY_KEY["salas"], "On Being and Unity should be read through Aquinas and Dionysius as well as Ficino, because the treatise disciplines Neoplatonic transcendence through Christian metaphysical language.", "interpretive", "On Being and Unity", "Aquinas and Dionysius", "Salas/Allen/Edelheit synthesis", "medium", "DRAFT", "Pass 009."),
    ("claim_black_009_007", "essay_900_own_opinion_theses", DOCS_BY_KEY["farmer"], "The theses according to Pico's own opinion should become a separate table with source family, doctrine, transformation, danger status, and related-work fields.", "methodological", "900 Conclusions", "own opinion theses", "Farmer synthesis", "high", "DRAFT", "Pass 009."),
    ("claim_black_009_008", "essay_900_neoplatonist_arab_authors", DOCS_BY_KEY["farmer"], "The Neoplatonist and Arabic author clusters in the 900 Conclusions should be treated as a source-network map rather than a generic concordist reading list.", "methodological", "900 Conclusions", "source networks", "Farmer/Black/Allen synthesis", "high", "DRAFT", "Pass 009."),
    ("claim_black_009_009", "essay_pico_plato_aristotle_concord", DOCS_BY_KEY["howlett"], "Pico's concord of Plato and Aristotle is a controlled instability: a method for testing compatibility, correction, and hierarchy rather than a simple assertion of agreement.", "interpretive", "concord", "Plato and Aristotle", "Howlett/Allen/Edelheit synthesis", "high", "DRAFT", "Pass 009."),
]

CARDS = [
    ("scholar-crofton-black", "scholar", "Crofton Black", "Heptaplus and biblical hermeneutics", "Black now anchors PicoDB's Heptaplus readings: structure, Genesis, esotericism, Dionysian anagogy, intellect, felicitas, Bereshit, sabbath, and the forty-nine gates.", "DRAFT", "scholar_crofton_black_values"),
    ("source-black-heptaplus-structure", "source_packet", "Black's Heptaplus Structure", "Seven-part guide to the work", "A source packet maps Black's chapter structure and makes it the control frame for future section summaries of Pico's Heptaplus.", "DRAFT", "source_black_heptaplus_structure"),
    ("essay-heptaplus-black", "essay", "Heptaplus and Hermeneutics", "Black-guided essay draft", "The updated Heptaplus essay reads Genesis as a structured anagogical system involving Aquinas, Dionysius, Arabic intellect theory, Jewish exegesis, Kabbalah, and the 900 Conclusions.", "DRAFT", "essay_heptaplus_black_biblical_hermeneutics"),
    ("essay-plato-aristotle-concord", "essay", "Plato and Aristotle in Pico", "Concord as controlled instability", "A new essay seed treats Pico's concord as a method of testing, correcting, and hierarchizing Aristotle and Plato rather than as easy harmony.", "DRAFT", "essay_pico_plato_aristotle_concord"),
    ("essay-being-unity-aquinas-dionysius", "essay", "Aquinas and Dionysius", "On Being and Unity", "A new essay seed frames On Being and Unity as Pico's Christian metaphysical control of Ficinian-Proclean transcendence through Aquinas and Dionysius.", "DRAFT", "essay_being_unity_aquinas_dionysius"),
    ("essay-900-own-opinion", "essay", "Pico's Own-Opinion Theses", "The 900 as Pico's architecture", "A new essay seed starts a table-driven project for all theses secundum opinionem propriam, tracking source family, doctrine, transformation, danger, and cross-links.", "DRAFT", "essay_900_own_opinion_theses"),
    ("essay-900-source-networks", "essay", "Neoplatonists and Arabs", "Source networks in the 900", "A new essay seed maps Proclus, Iamblichus, Pseudo-Dionysius, Averroes, Avicenna, Al-Farabi, and Ibn Bajja as structured source fields in the 900 Conclusions.", "DRAFT", "essay_900_neoplatonist_arab_authors"),
    ("essay-arab-intellect", "essay", "Arabic Intellect Tradition", "Felicitas and ascent", "A new essay seed follows Black's path from Averroes, Avicenna, Al-Farabi, Ibn Bajja, and Maimonides into Pico's Heptaplus and 900 Conclusions.", "DRAFT", "essay_pico_arab_intellect_felicitas"),
    ("essay-dionysian-anagogy", "essay", "Dionysian Anagogy", "Hierarchy, symbols, ascent", "A new essay seed treats Pseudo-Dionysius as a bridge between Platonism, Christian theology, biblical hermeneutics, and Pico's ascent model.", "DRAFT", "essay_pico_dionysian_anagogy"),
    ("essay-heptaplus-after-oration", "essay", "Heptaplus After the Oration", "Post-trial recoding", "A new essay seed reads the Heptaplus as Pico's post-Oration recoding of concord, ascent, Kabbalah, and source density through Genesis.", "DRAFT", "essay_heptaplus_after_oration"),
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
    payload["version"] = "0.8.0"
    payload["heptaplus_black_reading_fields"] = [
        "genesis_anchor",
        "heptaplus_unit",
        "exegetical_register",
        "black_problem",
        "source_family",
        "authority_named",
        "relation_to_900",
        "concord_status",
        "anagogy_status",
        "intellect_felicitas_status",
        "kabbalah_status",
        "confidence",
    ]
    payload["parallel_essay_program_fields"] = [
        "essay_problem",
        "guide_scholars",
        "primary_texts",
        "source_families",
        "artifact_dependencies",
        "table_needed",
        "next_close_reading_targets",
        "review_threshold",
    ]
    payload["guide_scholars"]["Black"] = [
        "heptaplus_structure",
        "biblical_hermeneutics",
        "dionysian_anagogy",
        "intellect_felicitas",
        "bereshit_sabbath",
        "jewish_arabic_source_ecology",
    ]
    write_json(path, payload)


def update_docs() -> None:
    append_once(
        DOCS / "SECTION_SUMMARY_STYLE_GUIDE.md",
        "## Pass 009 Heptaplus Black Overlay",
        """## Pass 009 Heptaplus Black Overlay

When summarizing the Heptaplus or Crofton Black, add a Black overlay:

- Identify the Heptaplus unit: proem, exposition, Bereshit, sabbath, or conclusion.
- Identify the Genesis anchor and the source family.
- Distinguish Aquinas, Pseudo-Dionysius, Proclus, Arabic intellect tradition, Jewish exegesis, and Kabbalah.
- State whether the passage repeats, recodes, or corrects a problem from the 900 Conclusions, Apology, Commento, or Oration.
- Mark the kind of ascent: cosmological, anagogical, intellectual, mystical, or salvific.
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
    for artifact_id, _artifact_type, title, path, _doc, target, status, _evidence in ARTIFACT_ROWS:
        if artifact_id.startswith("essay_"):
            conn.execute(
                """
                INSERT OR REPLACE INTO website_pages(id, entity_type, title, markdown_path, status, source_artifact_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (f"page-{artifact_id.replace('_', '-')}", "essay", title, path, status, artifact_id),
            )
    conn.commit()
    seed = load_seed_module()
    seed.export_data(conn)
    seed.build_site(conn)
    conn.close()
    print("Study pass 009 complete.")


if __name__ == "__main__":
    main()
