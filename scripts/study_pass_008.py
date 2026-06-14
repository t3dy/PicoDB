"""Study pass 008: biographical method, source gaps, and longform biography."""

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
    "howlett": "Critical_Political_Theory_and_Radical_Practice_Sophia_Howlett_-_Re-evaluating_Pico__Aristotelian_pdf_3c6c4fa3",
    "edelheit": "Amos_Edelheit_Maynooth_University_-_A_Philosopher_at_the_Crossroads_Giovanni_Pico_Della_Mirandol_pdf_dd0f01e6",
    "copenhaver_trial": "Brian_P_Copenhaver_Pico_della_Mirandola_on_Trial__Heresy_Freedom_and_Philosophy_libgen_li_pdf_753eb1fa",
    "copenhaver_magic": "Brian_P_Copenhaver_Magic_and_the_Dignity_of_Man__Pico_della_Mirandola_and_His_Oration_in_Modern__pdf_f7f272e1",
    "dougherty": "M_V_Dougherty_Pico_della_Mirandola__New_Essays_libgen_li_pdf_78172345",
    "farmer": "Medieval_Renaissance_Texts_Studies_167_Stephen_A_Farmer_Giovanni_Pico_Della_Mirandola_Syncretism_pdf_c99b971b",
    "busi": "Giulio_Busi_Raphael_Ebgi_Giovanni_Pico_della_Mirandola_Mito_magia_Qabbalah_Einaudi_pdf_c382f352",
    "wirszubski": "Chaim_Wirszubski_Paul_Oskar_Kristeller_Pico_della_Mirandola_s_Encounter_with_Jewish_Mysticism_Ha_pdf_cd8c112f",
    "allen": "Studies_in_the_Platonism_of_Marsilio_Ficino_and_Giovanni_PicoMichael_J._B._AllenRoutledge1080299_epub_65585d05",
    "letters": "Giovanni_Pico_della_Mirandola_Lettere_libgen_li_pdf_5024cbf9",
}

FILES = {
    "docs/BIOGRAPHICAL_READING_PROTOCOL.md": """# Biographical Reading Protocol

Status: DRAFT  
Created in study pass 008.

## Purpose

Biography in PicoDB is not a decorative chronology. Every life claim should be treated as a situated evidence claim: a date, place, relation, institutional setting, patronage structure, document witness, later editorial transformation, or historiographical interpretation.

## Required Fields

- date_range: exact date, approximate date, or date uncertainty.
- place: historical place and modern location id when possible.
- life_register: family, education, travel, patronage, friendship, romance/scandal, correspondence, composition, publication, trial, imprisonment, pardon, reform, death, posthumous memory.
- source_witness: Pico letter, contemporary testimony, Gianfrancesco Vita, printed edition, manuscript, modern scholarly reconstruction, later legend.
- scholar_governor: Howlett, Edelheit, Copenhaver, Dougherty/Borghesi, Farmer, Busi, Wirszubski, Allen, or another named scholar.
- intellectual_function: what the event changes in Pico's education, corpus, network, method, risk, or reception.
- myth_risk: low, medium, high, or contested.
- missing_source: yes/no, with acquisition target when relevant.

## Scholar Governors

- Howlett governs life as mobility, elite networks, contested coherence, and the rejection of a simple "St. Pico" story.
- Edelheit governs formation: scholastic techniques, university cultures, Padua/Paris, teachers, sources, and the danger of reducing Pico to Platonism or Kabbalah.
- Copenhaver governs the Roman crisis, papal examination, theological danger, and the modern myth of the Oration.
- Dougherty and Borghesi govern corpus, genre, editions, letters, and the principle that life must be read through works rather than detached anecdote.
- Farmer governs the Roman debate project and the 900 Conclusions as a public event with textual machinery.
- Busi and Wirszubski govern Hebrew, Kabbalah, Mithridates, translation dependence, and the fact that 1486 biography is also source-infrastructure biography.
- Allen governs Ficino, Florentine Platonism, poetic theology, and the boundaries between friendship, dispute, and intellectual transformation.

## Biography Style Rules

1. Never make the opening paragraph a miracle-story about genius. Begin with social position, education, and mobility.
2. Separate event from interpretation: "Pico went to Paris" is not the same as "Paris made him a nominalist."
3. Mark Margherita, Savonarola, death, and sexuality claims as high myth-risk unless the source witness is named.
4. Treat every letter as a dated social act: recipient, place, theme, rhetorical posture, and textual witness matter.
5. Treat Gianfrancesco's biography as a source and a posthumous intervention, not as transparent fact.
6. Treat modern biographies and web sources as acquisition/gap aids unless checked against the local scholarly corpus.
""",
    "artifacts/historiography/pico_biography_scholar_method_matrix.md": """# Historiography Node: Biography Scholar Method Matrix

- Artifact ID: `hist_pico_biography_scholar_method`
- Type: historiography node
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Problem

Pico's biography is easy to flatten into a prodigy myth: noble birth, dazzling memory, 900 theses, papal trouble, Savonarolan death. The current scholarship pushes against that myth. A usable biography for PicoDB must preserve the difference between events, networks, institutions, texts, and posthumous mythmaking.

## Scholar Matrix

| Scholar | Biographical Value | PicoDB Rule |
|---|---|---|
| Sophia Howlett | Mobility, elite kinship, networks, active/contemplative tension, and "St. Pico" as a later construction. | Write life as intellectual geography and contested identity, not as a saintly or secular conversion plot. |
| Amos Edelheit | Scholastic formation, school traditions, university cultures, scholastic source traces. | Every biography section must ask which scholastic tools Pico acquired or deployed at that stage. |
| Brian P. Copenhaver | Roman trial, theological danger, anti-mythic Oration reading. | The crisis of 1486-1487 must be juridical and doctrinal, not merely heroic free inquiry. |
| M. V. Dougherty / Borghesi | A life in works, corpus control, letters, genre, edition status. | Biography must be tied to works, letters, and editions; unsupported anecdotes remain flagged. |
| Stephen Farmer | Roman debate project, 900 Conclusions as printed and debated machine. | The debate was an organized public event, not simply the occasion for the Oration. |
| Giulio Busi / Chaim Wirszubski | Hebrew/Kabbalah learning, Mithridates, translations, source dependence. | The 1486 life narrative must include language study, teachers, translators, and source mediation. |
| Michael J. B. Allen | Ficino relation, Florentine Platonism, poetic theology, metaphysical disagreement. | The Florence story must keep friendship and dispute together. |

## Working Synthesis

PicoDB should narrate Pico as a mobile noble scholar whose life repeatedly converts privilege into intellectual risk. His family status gives access to universities, courts, libraries, teachers, translators, and patrons. That same status lets him attempt a gigantic Roman disputation, survive papal danger through diplomacy, and keep moving through elite networks after scandal. But it also distorts the record: nephewly biography, Savonarolan memory, humanist admiration, modern Oration myth, and forensic speculation all compete to define what Pico's life meant.
""",
    "artifacts/source_packets/pico_biographical_source_gaps_pass008.md": """# Source Packet: Pico Biographical Source Gaps

- Artifact ID: `source_pico_biographical_source_gaps`
- Type: source packet
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Locally Held

- Giovanni Pico, `Lettere`, modern critical edition by Francesco Borghesi, is present as Markdown in PicoDB. It still needs letter-by-letter section summaries.
- Howlett's `Re-evaluating Pico` is present and currently governs biography as intellectual geography, elite network, and contested posthumous identity.
- Edelheit's `A Philosopher at the Crossroads` is present and governs scholastic formation, Padua/Paris source tracking, and anti-reductive labels.
- Copenhaver's `Pico on Trial` and `Magic and the Dignity of Man` are present and govern the Roman crisis and Oration myth.
- Dougherty's `Pico della Mirandola: New Essays` is present and includes the crucial "A Life in Works" orientation.
- Farmer, Busi, Wirszubski, and Allen are present for the 900 Conclusions, Kabbalah, Mithridates, and Ficino/Platonism.

## Known But Not Fully Controlled

| Source / Witness | Why It Matters | Current Status |
|---|---|---|
| Gianfrancesco Pico, `Vita` of Giovanni Pico, 1496; modern edition by Bruno Andreolli, 1994. | Major early biography; also a posthumous Savonarolan/editorial intervention. | We have older English access through Thomas More/Rigg; need modern Latin edition/critical apparatus. |
| Giovanni Pico, `Lettere`, Francesco Borghesi ed., Olschki 2018. | First modern critical edition of the letters, needed for chronology and networks. | Present locally, but not yet section-summarized letter by letter. |
| Vatican manuscript Capponi 235. | Important manuscript witness for the letter tradition. | Mentioned in reviews; no manuscript images or full codicological dossier yet. |
| Bologna 1496 printed collection of letters and related posthumous materials. | Early editorial construction of Pico's memory. | Mentioned by scholarship; needs source record and digital witness if available. |
| Thomas More's 1504 English `Life of Pico` and appended letters/devotional works. | Reception and Anglophone saintly Pico tradition. | Public-domain digital copies located through PRDL/Ex-Classics; should be ingested for reception, not treated as transparent biography. |
| Public-domain Pico title clusters in PRDL. | Additional early printed works and editions may help control textual reception. | PRDL reports 60 titles / 75 volumes; needs systematic triage and download plan. |
| Elijah del Medigo letter to Pico, `De nervis et sensu tactus` edition by Giovanni Licata, 2014. | Teacher-student relation, Paduan Aristotelianism, anatomy/sensation, intellectual network. | Identified from SEP bibliography; not yet present locally. |
| Trial documents and papal condemnation witnesses beyond Copenhaver. | Necessary for reconstructing the Roman crisis. | Copenhaver present; primary documentary witnesses need a separate gap audit. |

## Web Search Notes, 2026-06-14

- Stanford Encyclopedia of Philosophy confirms the basic early chronology: born 24 February 1463; Bologna at around 14; Ferrara and Padua soon after; Elia del Medigo at Padua; Florentine connections by 1484. https://plato.stanford.edu/entries/pico-della-mirandola/
- University of Bologna confirms Bologna enrollment in 1477, no degree, move to Ferrara in 1479, Padua 1480-1482, Pavia in 1482, and Florence/Ficino in 1484. https://www.unibo.it/en/university/who-we-are/our-history/famous-people-and-students/giovanni-pico-della-mirandola-1
- BMCR review of Borghesi's `Lettere` confirms publication details and the importance of manuscript/print tradition. https://bmcr.brynmawr.edu/2019/2019.01.17/
- Olschki describes Borghesi's edition as a philologically correct presentation of Pico's epistolary corpus based on exhaustive review. https://www.olschki.it/libro/9788822265746
- PRDL lists 60 public-domain titles / 75 volumes for Giovanni Pico and links to digital-library searches. https://www.prdldev.juniusinstitute.org/author_view.php?a_id=1633&type=Other
- SEP's Gianfrancesco entry lists the modern edition of Giovanni Pico's letters and the modern edition of Gianfrancesco's `Vita`. https://plato.stanford.edu/entries/gianfrancesco-pico/
""",
    "artifacts/essays/pico_biography_scholar_synthesis_draft.md": """# Essay Draft: Giovanni Pico della Mirandola, A Biography for PicoDB

- Artifact ID: `essay_pico_biography_scholar_synthesis`
- Status: DRAFT
- Evidence status: SOURCE_ANCHORED_DRAFT
- Target: portal biography page; later expansion after letter-by-letter reading.

## Thesis

Giovanni Pico della Mirandola's life should be written as the biography of a mobile noble scholar who repeatedly turned privilege into intellectual risk. The standard outlines are familiar: born at Mirandola in 1463, educated across northern Italy and France, drawn into Florence's humanist and Platonist worlds, author of the 900 Conclusions and the speech later called the Oration, condemned in Rome, detained in France, reconciled with the Church, increasingly attached to Savonarolan reform, dead in Florence in 1494. But the scholars in PicoDB teach us that this outline becomes misleading unless each event is tied to institutions, works, letters, teachers, translators, patrons, and later memory.

Howlett is the principal guide for biography because she treats Pico's life as a set of intellectual geographies and contested roles. Pico is not simply the genius of the Oration. He is a count moving between Mirandola, Bologna, Ferrara, Padua, Pavia, Florence, Paris, Rome, France, and late Florence; a younger son whose family status gave him room to study, travel, hire teachers, accumulate books, and survive scandal; a gentleman-philosopher whose preference for contemplation never erased his entanglement with politics, patronage, and reputation. Howlett also guards against Gianfrancesco's posthumous "St. Pico." Pico's late religious seriousness is real, but the saintly conversion plot is an editorial and Savonarolan construction that must be tested rather than repeated.

Edelheit supplies the second rule: biography must be intellectual formation. The places in Pico's life are not picturesque stops on a prodigy's tour. They are school environments. Bologna introduces legal and institutional expectations. Ferrara and Padua expose him to Aristotelian and Averroist culture. Pavia matters for logic, mathematics, and Greek. Paris matters for the via moderna, scholastic debate, and the technical apparatus that later governs the 900 Conclusions and the Apology. If the biography makes Pico only a Platonist, Kabbalist, magician, or humanist, it has failed Edelheit's test. Pico's life is also the acquisition of scholastic habits: distinction, objection, thesis, authority, commentary, and public disputation.

Copenhaver supplies the third rule: crisis must be technical. The Roman controversy was not a melodrama of free thought against repression. It was a juridical and theological event in which propositions, terms, witnesses, and papal authority mattered. Farmer reinforces this by showing that the 900 Conclusions were a printed, numbered, architectonic debate project. Dougherty and Borghesi add the corpus rule: biography must be read through works, letters, genres, and editions. Busi and Wirszubski add the source-infrastructure rule: the year 1486 cannot be written without teachers, Hebrew, Kabbalah, Mithridates, and translation dependence. Allen adds the Florentine boundary rule: Ficino matters deeply, but Pico's relation to Ficino includes admiration, appropriation, and disagreement.

The result is a biography that does not ask, "Was Pico a saint, a magician, a humanist, or a philosopher?" It asks how a young aristocrat constructed a life in which university scholasticism, Florentine Platonism, Jewish Kabbalah, Christian theology, humanist style, public debate, scandal, friendship, patronage, and reform all became parts of one compressed experiment.

## 1. Mirandola: Birth, Rank, and the Conditions of Mobility

Pico was born at Mirandola on 24 February 1463 into the family of the counts of Mirandola and Concordia. His father was Gianfrancesco I Pico; his mother, Giulia Boiardo, belonged to another noble line. The bare fact of noble birth matters because it is the material condition for almost everything that follows. Pico's mobility was not the wandering of a poor scholar. It was aristocratic mobility: travel under protection, access to courts, tuition, books, correspondence, teachers, and diplomatic rescue.

The family setting also established ecclesiastical expectations. As the youngest son, Pico could be aimed toward church office and learned status. That expectation helps explain his early move to Bologna for canon law. But the later life is defined by his refusal to remain inside the line initially marked for him. He repeatedly abandons one expected path for another: canon law for philosophy, ordinary scholastic success for universal disputation, courtly reputation for ascetic seriousness, and perhaps worldly ambition for reform-minded piety.

Biography should therefore begin with power and constraint. Pico's privilege gave him opportunities, but it also made every intellectual act public. A poor student could fail quietly; a count who printed 900 Conclusions and summoned Europe to Rome could not. A romance scandal, a papal investigation, a flight north, or a Savonarolan alignment all mattered because Pico was visible.

## 2. Bologna, Ferrara, Padua, Pavia: Education as Formation

At about fourteen Pico enrolled at Bologna to study canon law. The University of Bologna confirms the broad shape of this early period: 1477 enrollment, no degree, departure after roughly two years. The standard story says he tired of law and turned to philosophy. PicoDB should keep the institutional residue of that abandoned training. Canon law may not have become his vocation, but legal and ecclesiastical categories remain part of the world in which his trial would later unfold.

In 1479 Pico moved to Ferrara. Ferrara matters as a courtly and humanist environment, and it is often associated with his first encounter with figures who would matter later, including Savonarola. The relation between first meetings, later influence, and retrospective memory must be kept under review. Howlett's caution is useful here: later Savonarolan memory can reach backward and make early contact look more teleological than it was.

From 1480 to 1482 Pico studied at Padua, one of the great centers of Aristotelian philosophy. Here the biography becomes decisively Edelheitian. Padua is not just a location; it is a school culture. Pico's contact with Elia del Medigo, a Jewish Averroist Aristotelian, matters for philosophy, language, and the later interface between Latin scholasticism and Jewish learning. If Ficino represents one Florentine Platonist pole, Padua represents an Aristotelian and Averroist counterweight that the mature Pico never simply abandons.

Pavia, reached in 1482, adds further formation: logic, mathematics, Greek, and the enlargement of Pico's technical base. The point is not to assign each doctrine to one university. It is to prevent biography from becoming a chain of picturesque intellectual conversions. Pico did not pass from law to Aristotle to Plato to Kabbalah as if each stage erased the last. He accumulated techniques. The later 900 Conclusions are possible because Pico had learned to let traditions collide in thesis form.

## 3. Florence and the Humanist-Platonist Network

By 1484 Pico was connected with Florence, Ficino, Poliziano, Lorenzo de' Medici, and Girolamo Benivieni. Florence gave Pico friendship, patronage, literary culture, poetic theology, Platonism, and eventually Savonarolan reform. But the Florentine network should not be written as a simple academy that adopted Pico and made him Platonist. Allen's work on Pico and Ficino is essential because it makes the relation both intimate and disputational.

Pico learned from Ficino, admired him, and used Florentine Platonism as one of his major languages. Yet On Being and Unity later shows disagreement over Plato and Aristotle; the Oration and 900 Conclusions show a broader ambition than Ficinian Platonism alone could contain. Pico's Florence is therefore double: a home for intellectual affinity and a stage for rivalry over how ancient wisdom should be organized.

Poliziano and Benivieni matter differently. Poliziano anchors philological humanism, style, friendship, and perhaps the emotional intensity of Pico's Florentine attachments. Benivieni anchors poetic devotion and later Savonarolan religious culture. Lorenzo matters as patron, protector, and political node. Together they make Florence a living network rather than a doctrine. A biography that says "Pico entered the Platonic Academy" is too blunt. Pico entered a dense environment of poetry, philology, patronage, theology, friendship, and dispute.

## 4. Paris and the Scholastic Enlargement

Pico's time in Paris is easy to summarize and hard to control. The usual account makes Paris the great center of scholastic philosophy and theology, the place where Pico encountered the via moderna and where the debate project may have taken shape. Edelheit's rule requires us to treat Paris not as atmosphere but as a source problem. Which Parisian teachers, texts, methods, and controversies can be tied to Pico? Which are inferred from later works? Which scholastic distinctions in the 900 Conclusions or Apology show Parisian marks?

Howlett treats Paris as part of Pico's knowledge and power network. It is the point at which formal education gives way to the life of an independent gentleman-scholar. That transition matters. Pico is no longer simply being trained. He is beginning to build a project large enough to require Europe as its imagined audience.

The Paris section of the biography therefore needs future expansion after closer reading of Edelheit and the letters. For now, the working claim is restrained: Paris helped intensify Pico's scholastic competence and public disputational ambition. It should not be used as a vague synonym for "medieval" or "nominalist" without source anchors.

## 5. 1486: Scandal, Kabbalah, and the Debate Project

The year 1486 is the hinge of Pico's life. Howlett's biography makes the Margherita episode impossible to ignore. Pico likely met Margherita de' Medici in Florence and abducted her in Arezzo in May 1486; he was caught, injured, disgraced, and forced to navigate the political and personal consequences. This event is often uncomfortable for admirers of Pico, and Gianfrancesco's saintly biography tries to transform or contain it. PicoDB should do neither. It should treat the episode as a public scandal that affected reputation, friendship, mobility, and the later preference for a contemplative life.

The same year also concentrates the intellectual work for which Pico is famous. In Florence, Perugia, and related movements, Pico worked with an entourage that included Elia del Medigo and Flavius Mithridates. Busi and Wirszubski make this biographically decisive. Pico's encounter with Kabbalah was not a private mystical download. It required language study, Hebrew and Aramaic materials, Latin translations, and teachers. Mithridates becomes a biographical actor because he enabled Pico's access to Jewish mystical sources while also mediating and possibly reshaping them.

This means 1486 must be written as a collision between scandal and system. Pico's personal reputation is damaged at the same time that his intellectual ambition grows. The 900 Conclusions gather Aristotle, Plato, scholastic theology, magic, Kabbalah, ancient wisdom, and Pico's own theses into a public debate machine. The Oration was meant to introduce that project, not to stand alone as a modern manifesto of dignity. Copenhaver and Farmer together correct the biography: the famous speech belongs to a planned disputation whose printed theses drew papal scrutiny.

## 6. Rome: Ambition Becomes Trial

Pico's Roman project was audacious in a specifically institutional way. He did not merely write a book. He printed and circulated 900 theses and invited disputation before a learned audience, including cardinals and theologians. Farmer's account of the 900 Conclusions as an architectonic system changes the life story: Pico's ambition was public, procedural, numbered, and argumentative.

The project collapsed when papal authorities examined a subset of the theses. Copenhaver insists that this was a technical theological crisis. The condemned or suspect propositions touched issues such as magic, Kabbalah, Christ's descent, Eucharistic theology, the cross, and doctrinal authority. Pico wrote the Apology to defend himself, but defense did not simply settle the matter. The crisis moved from intellectual performance to juridical danger.

The biography should avoid two temptations. The first is romantic: Pico as martyr of free thought. The second is dismissive: the Church as merely fearful of novelty. Copenhaver's method keeps both away. The papal commission had doctrinal concerns; Pico's claims really did rearrange authorities, disciplines, and proofs. The crisis is part of the content of his philosophy, not an external accident.

## 7. France and Vincennes: Flight, Detention, and Diplomacy

After the Roman crisis, Pico left Italy and was detained in France, associated in the scholarly record with Vincennes. Howlett's phrasing is important: imprisonment at the royal palace/castle of Vincennes may also have functioned as protection from papal agents, or at least as a diplomatically complex detention. This is a perfect example of why biography needs evidence fields. "Imprisonment" is true enough for a public timeline, but the interpretive status of that imprisonment needs a note.

Pico's survival depended on networks. Royal, Medicean, and ecclesiastical diplomacy mattered. The count's mobility now became forced mobility. The scholar who had invited Europe to Rome was now dependent on political protection. The episode also changes the emotional shape of the life. The universal debate had failed. The Oration never served its intended public function. The 900 Conclusions became a trial archive and a reception problem.

For future work, this section needs tighter source control: dates of arrest, route, royal actors, papal nuncios, correspondence, and pardon documents. The current pass marks trial and detention witnesses as a primary source gap.

## 8. Return, Reconciliation, and the Late Works

Pico returned to Italy and eventually settled into late Florentine life. The late phase includes Heptaplus, On Being and Unity, the Disputations against astrology, letters, religious writing, and proximity to Savonarola. It is tempting to narrate this as conversion: the restless young syncretist becomes a penitent religious thinker. Howlett and Edelheit both complicate that story.

Pico had long been interested in the contemplative life, mystical ascent, and Christian theology. The late works intensify that orientation, but they do not erase the earlier Pico. Heptaplus continues the project of hidden wisdom through biblical interpretation. On Being and Unity continues the concord project but brings it into sharp relation with Ficino. The Disputations against astrology move into late polemic, natural philosophy, providence, and anti-divinatory theology. These works show concentration, not simple repudiation.

Savonarola's role is real and contested. Pico admired him, helped bring him or keep him in Florence according to later accounts, and became increasingly attached to reform-minded religious life. But "Savonarolan Pico" must be separated from "Gianfrancesco's St. Pico." The late life shows ascetic desire and reform sympathy, but not necessarily completed withdrawal from aristocratic privilege, books, friends, and intellectual projects. Howlett's line is useful: religious life was attractive, but "not yet" fully realized.

## 9. Death, Burial, and the Problem of Posthumous Pico

Pico died in Florence on 17 November 1494, at the age of thirty-one, as Charles VIII entered the city and the Medici order collapsed. He was buried at San Marco, near Poliziano. The death has acquired its own mythology, including poisoning narratives and modern forensic interest. PicoDB should record the forensic and historiographical debate, but the biography should not let murder mystery replace intellectual history.

The more important posthumous event is editorial. Gianfrancesco Pico, the nephew, became a decisive mediator of Giovanni's image. His 1496 biography and related editorial choices helped create a saintly, penitential Pico. The Life is indispensable, but it is not neutral. It opens the posthumous reception in which Pico's works could be arranged, omitted, moralized, and made useful for Savonarolan or Christian apologetic purposes.

Modern reception adds another layer. Copenhaver's work shows how the Oration was later transformed into the "Manifesto of the Renaissance" and often separated from the 900 Conclusions, magic, Kabbalah, scholasticism, and trial. This modern Pico is another posthumous construction. The biography must therefore end not with death alone, but with memory: saintly Pico, dignity Pico, magical Pico, scholastic Pico, Kabbalistic Pico, Platonist Pico, and the current effort to hold them together without flattening them.

## 10. Source Gaps and Next Reading Tasks

The next biographical work should be letter-driven. Borghesi's 2018 critical edition of the Lettere is present locally and must be summarized letter by letter. Each letter should become a dated social act: sender, recipient, place, date, topic, rhetorical posture, source witness, and life register. The letters will allow us to test the biography's claims about networks, friendship, style, crisis, patronage, and religious self-presentation.

The project also needs stronger control of Gianfrancesco's Vita. We have access to older English versions through Thomas More/Rigg and web copies, but the modern Andreolli edition and the Latin apparatus should be acquired or at least represented in a source-gap record. We also need manuscript and print witnesses for the letters: Vatican Capponi 235 and the Bologna 1496 print tradition are mentioned in scholarship and web reviews but not yet controlled in the database.

PRDL reports a large public-domain field of Pico titles and links to digital repositories. That is not automatically reliable full text, but it is an acquisition map. The next source pass should triage PRDL for early editions, reception witnesses, devotional appendices, and public-domain translations. The Elijah del Medigo letter edited by Licata is another missing target, important for Padua and the teacher-student network.

## Working Conclusion

Pico's life is short, but it is not simple. It is not the life of pure genius floating above institutions, nor the life of a stable system-builder who calmly reconciled all traditions, nor the life of a saint whose early errors dissolve into penitence. It is the life of an aristocratic scholar who moved fast through powerful institutions, learned from incompatible teachers, gathered languages and traditions through human networks, turned thesis-writing into public theater, collided with papal authority, survived through diplomacy, and died before his late religious and anti-astrological projects could settle into a final shape.

The best biography for PicoDB is therefore synthetic but disciplined. From Howlett it takes mobility, networks, and the critique of saintly myth. From Edelheit it takes scholastic formation and anti-reductive method. From Copenhaver it takes trial danger and the correction of modern Oration myth. From Dougherty and Borghesi it takes works, letters, editions, and genre. From Farmer it takes the Roman debate as event. From Busi and Wirszubski it takes Kabbalah as source infrastructure. From Allen it takes the Ficino relation as both friendship and dispute. Pico's life becomes readable only when those registers remain visible at once.
""",
}

ARTIFACT_ROWS = [
    ("hist_pico_biography_scholar_method", "historiography_node", "Pico Biography Scholar Method Matrix", "artifacts/historiography/pico_biography_scholar_method_matrix.md", DOCS_BY_KEY["howlett"], "Pico biography method", "SOURCE_ANCHORED", "likely"),
    ("source_pico_biographical_source_gaps", "source_packet", "Pico Biographical Source Gaps", "artifacts/source_packets/pico_biographical_source_gaps_pass008.md", DOCS_BY_KEY["letters"], "Pico biography source gaps", "SOURCE_ANCHORED", "likely"),
    ("essay_pico_biography_scholar_synthesis", "website_page", "Giovanni Pico Biography Scholar Synthesis", "artifacts/essays/pico_biography_scholar_synthesis_draft.md", DOCS_BY_KEY["howlett"], "Giovanni Pico della Mirandola", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
]

CLAIMS = [
    ("claim_bio_008_001", "essay_pico_biography_scholar_synthesis", DOCS_BY_KEY["howlett"], "Pico's biography should be written as intellectual geography: mobility through Mirandola, Bologna, Ferrara, Padua, Pavia, Florence, Paris, Rome, France, and late Florence shaped the corpus and its risks.", "historiographical", "biography", "Pico", "Howlett synthesis", "high", "DRAFT", "Pass 008 biography synthesis."),
    ("claim_bio_008_002", "essay_pico_biography_scholar_synthesis", DOCS_BY_KEY["edelheit"], "Pico's educational biography must track scholastic formation rather than reducing him to Platonism, Kabbalah, magic, or humanism.", "methodological", "scholasticism", "Pico", "Edelheit synthesis", "high", "DRAFT", "Pass 008 biography synthesis."),
    ("claim_bio_008_003", "essay_pico_biography_scholar_synthesis", DOCS_BY_KEY["copenhaver_trial"], "The Roman crisis should be represented as a juridical-theological event involving technical doctrinal danger, not merely as a heroic free-thought episode.", "historiographical", "trial", "Pico trial", "Copenhaver synthesis", "high", "DRAFT", "Pass 008 biography synthesis."),
    ("claim_bio_008_004", "essay_pico_biography_scholar_synthesis", DOCS_BY_KEY["farmer"], "The 900 Conclusions were a printed, numbered public debate machine, so the Oration must be biographically tied to the planned Roman disputation.", "textual", "900 Conclusions", "Oration", "Farmer synthesis", "high", "DRAFT", "Pass 008 biography synthesis."),
    ("claim_bio_008_005", "essay_pico_biography_scholar_synthesis", DOCS_BY_KEY["busi"], "Pico's 1486 biography requires source-infrastructure tracking: Hebrew study, Mithridates, Kabbalistic translations, teachers, and mediation.", "methodological", "Kabbalah", "Pico 1486", "Busi/Wirszubski synthesis", "high", "DRAFT", "Pass 008 biography synthesis."),
    ("claim_bio_008_006", "source_pico_biographical_source_gaps", DOCS_BY_KEY["letters"], "The Borghesi 2018 Lettere are present locally but require letter-by-letter summaries before the biography can become reviewed.", "open_problem", "letters", "Pico letters", "local corpus and web review", "high", "DRAFT", "Pass 008 source gap."),
    ("claim_bio_008_007", "source_pico_biographical_source_gaps", None, "Gianfrancesco Pico's Vita is essential but must be treated as both source witness and posthumous editorial intervention; the modern Andreolli edition is still an acquisition/control gap.", "open_problem", "Vita", "Gianfrancesco Pico", "SEP/PRDL/web source audit", "medium", "DRAFT", "Pass 008 source gap."),
    ("claim_bio_008_008", "source_pico_biographical_source_gaps", None, "PRDL identifies a public-domain field of 60 Pico titles and 75 volumes that should be triaged for early editions, translations, and reception witnesses.", "bibliographic", "source acquisition", "Pico sources", "PRDL web search", "medium", "DRAFT", "Pass 008 source gap."),
    ("claim_bio_008_009", "essay_pico_biography_scholar_synthesis", DOCS_BY_KEY["allen"], "Pico's Florentine biography must preserve both Ficinian affinity and Ficinian disagreement, especially around Platonism, Aristotle, and On Being and Unity.", "interpretive", "Ficino", "Pico and Ficino", "Allen synthesis", "high", "DRAFT", "Pass 008 biography synthesis."),
]

CARDS = [
    ("essay-pico-biography-synthesis", "essay", "Pico Biography", "Scholar-synthesis draft", "A new biographical essay treats Pico as a mobile noble scholar whose family privilege, universities, Florentine networks, Kabbalah infrastructure, Roman trial, French detention, and late Savonarolan proximity must be read together.", "DRAFT", "essay_pico_biography_scholar_synthesis"),
    ("hist-pico-biography-method", "historiography", "Biography Method Matrix", "How to write Pico's life", "The biographical protocol assigns Howlett, Edelheit, Copenhaver, Dougherty/Borghesi, Farmer, Busi, Wirszubski, and Allen distinct roles in controlling life claims.", "DRAFT", "hist_pico_biography_scholar_method"),
    ("source-pico-biography-gaps", "source_gap", "Biography Source Gaps", "Letters, Vita, witnesses", "A new source-gap packet marks the Borghesi Lettere for letter-by-letter summary and identifies Gianfrancesco's Vita, Capponi 235, the 1496 print tradition, PRDL titles, and the del Medigo letter as acquisition/control targets.", "DRAFT", "source_pico_biographical_source_gaps"),
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
    path = DATA / "reading_artifact_ontology.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version"] = "0.7.0"
    for field in [
        "biographical_source_packet",
        "source_gap_record",
        "biographical_synthesis",
    ]:
        if field not in payload["artifact_types"]:
            # artifact_types is a list of objects, so this guard intentionally no-ops for strings.
            pass
    payload["biographical_reading_fields"] = [
        "date_range",
        "place",
        "life_register",
        "source_witness",
        "scholar_governor",
        "intellectual_function",
        "network_relation",
        "work_relation",
        "institutional_context",
        "myth_risk",
        "missing_source",
        "confidence",
    ]
    payload["life_register_taxonomy"] = [
        "family_status",
        "education",
        "travel",
        "patronage",
        "friendship",
        "romance_scandal",
        "correspondence",
        "composition",
        "publication",
        "trial",
        "imprisonment",
        "pardon_reconciliation",
        "reform",
        "death",
        "posthumous_memory",
    ]
    payload["biography_scholar_synthesis"] = {
        "Howlett": "mobility_networks_and_st_pico_correction",
        "Edelheit": "scholastic_formation_and_source_trace",
        "Copenhaver": "trial_danger_and_oration_myth_correction",
        "Dougherty_Borghesi": "life_in_works_letters_genre_and_edition",
        "Farmer": "roman_debate_architecture",
        "Busi_Wirszubski": "kabbalah_source_infrastructure",
        "Allen": "ficino_affinity_and_dispute",
    }
    if "biographical_source_witness" not in payload["claim_types"]:
        payload["claim_types"].append("biographical_source_witness")
    write_json(path, payload)


def main() -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    for path, text in FILES.items():
        write(path, text)
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
    conn.execute(
        """
        INSERT OR REPLACE INTO website_pages(id, entity_type, title, markdown_path, status, source_artifact_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "page-pico-biography-synthesis",
            "biography",
            "Giovanni Pico della Mirandola: Biography",
            "artifacts/essays/pico_biography_scholar_synthesis_draft.md",
            "DRAFT",
            "essay_pico_biography_scholar_synthesis",
        ),
    )
    conn.commit()
    seed = load_seed_module()
    seed.export_data(conn)
    seed.build_site(conn)
    conn.close()
    print("Study pass 008 complete.")


if __name__ == "__main__":
    main()
