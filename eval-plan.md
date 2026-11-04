# Plan de evaluare – agentul dsdoc

Specificație de implementare pentru evaluarea skill-urilor și agenților `dsdoc-*`. Destinat lui Claude Code: citește tot documentul înainte de a implementa ceva.

**În afara scopului (deocamdată):** evaluarea reviewer-ilor și a buclei writer → reviewer. Se evaluează doar output-ul writer-ilor. Reviewer-ii există și rămân neschimbați.

---

## 1. Sistemul evaluat

### Structura existentă (nu se modifică)

```
.claude/
├── agents/
│   ├── dsdoc-business-context-writer.md / -reviewer.md
│   ├── dsdoc-code-doc-writer.md
│   ├── dsdoc-convert-writer.md
│   ├── dsdoc-model-card-writer.md / -reviewer.md
│   └── dsdoc-stake-summary-writer.md / -reviewer.md
├── settings.local.json
└── skills/
    ├── dsdoc/                    # orchestrator
    │   └── scripts/check_sensitive.sh, sensitive_patterns.txt
    ├── dsdoc-business-context/   # SKILL.md, check.sh, criteria.md
    ├── dsdoc-code-doc/           # SKILL.md, scripts/check_unchanged.py
    ├── dsdoc-convert/            # SKILL.md
    ├── dsdoc-model-card/         # SKILL.md, check.sh, criteria.md
    └── dsdoc-stake-summary/      # SKILL.md, check.sh, criteria.md
```

`.claude/` se copiază în proiectele de lucru. **Nimic legat de evaluare nu intră în `.claude/`.**

### Pipeline

```
Cod ──► code-doc ─────────────────────┐
                                      ├──► model-card ──► stake-summary
Lean Canvas PDF / Confluence MD ──► business-context ──┘      ▲
                                        Developer notes ──────┘
```

Erorile se propagă de-a lungul lanțului. De aceea fiecare skill se evaluează **izolat, pe input de referință**, apoi lanțul întreg (**end-to-end**).

### Mapare skill → evaluare

| Skill | Writer | Scripturi statice existente | Judges |
|---|---|---|---|
| `dsdoc-code-doc` | `code-doc-writer` | `scripts/check_unchanged.py` | hallucination, return_exceptions, planted_error_fixed |
| `dsdoc-business-context` | `business-context-writer` | `check.sh` | recall, precision, source_correct, conflicts |
| `dsdoc-model-card` | `model-card-writer` | `check.sh` | claim_support, conflicts, limitations_specific |
| `dsdoc-stake-summary` | `stake-summary-writer` | `check.sh` | fidelity, critical_facts, comprehension_answer, comprehension_grade, business_link |
| `dsdoc-convert` | `convert-writer` | — | **de definit** (scopul skill-ului nu e încă specificat) |
| toate | — | `dsdoc/scripts/check_sensitive.sh` | — (prag obligatoriu pe orice output) |

---

## 2. Principii

1. **Trei verificatori:**
   - **Scripturi statice** (existente în `.claude/`): exacte, deterministe. Prag minim.
   - **LLM-judge**: verificări de sens (fidelitate, halucinații, recall). Apel API din `eval/`, niciodată agent în `.claude/agents/`.
   - **Om**: creează datele de referință, calibrează judge-ii, validează pe eșantion.
2. **Scripturile statice nu se reimplementează și nu se copiază.** Evaluarea le apelează din `.claude/skills/`, exact ca reviewer-ii.
3. **Datele de referință nu ajung niciodată la agent.** Agentul rulează într-un sandbox care conține doar `.claude/` și input-ul testului.
4. **`criteria.md` nu e rubrica judge-ului.** Reviewer-ii verifică după ele, deci output-ul final le respectă prin construcție. Judge-ii au rubricile lor, legate de datele de referință.
5. **Judge-ul folosește alt model decât agentul**, temperatura 0.
6. **Niciun judge nu e folosit înainte de testare și calibrare** (secțiunile 9–10).
7. **Fiecare test rulează de 3–5 ori**; se raportează media și variația.
8. **Greșeli plantate intenționat** în seturile de test, ca să știm exact ce trebuie găsit.
9. Setul de test devine **test de regresie**: rulat complet la orice modificare a unui skill sau agent.

---

## 3. Structura `eval/`

`eval/` stă în rădăcina proiectului, lângă `.claude/`, și nu se copiază în proiectele de lucru.

```
eval/
├── README.md
├── config.yaml                  # modele, nr. rulări, căi, praguri
├── run_eval.py                  # dirijorul: agent → scripturi → judges → scor
│
├── runner/
│   ├── sandbox.py               # folder temporar: copie .claude/ + input test, fără eval/
│   └── agent_runner.py          # rulează writer-ul cu `claude -p` în sandbox
│
├── static/
│   └── run_checks.py            # apelează check.sh, check_unchanged.py, check_sensitive.sh
│
├── judges/                      # vezi secțiunea 8
│
├── datasets/
│   ├── code_doc/{cases/, reference.json}
│   ├── business_context/{packages/, reference.json}
│   ├── model_card/{projects/, reference.json}
│   ├── stake_summary/{inputs/, reference.json}
│   ├── convert/                 # de completat
│   └── e2e/projects/
│
├── scoring/
│   ├── metrics.py               # recall, precizie, fidelitate, medie, variație
│   └── weights.yaml             # ponderile verificărilor în scorul per skill
│
├── human_review/
│   ├── export_sample.py
│   └── sheets/
│
└── results/
    ├── runs/<timestamp>/<skill>/<test_id>/run_<n>/
    │   ├── output/
    │   ├── static.json
    │   ├── judges.json
    │   └── score.json
    ├── summary.csv
    └── report.md
```

### `config.yaml` (propunere)

```yaml
claude_dir: ../.claude           # relativ la eval/; schimbă dacă eval/ e în alt repo
agent:
  command: claude -p
judge:
  model: <alt model decât agentul>
  temperature: 0
  max_tokens: 2000
runs_per_test: 3
human_review_sample: 0.1
calibration_targets:
  human_human_agreement: 0.85
  judge_human_agreement: 0.85
  planted_error_recall: 0.90
  precision: 0.85
```

---

## 4. Fluxul `run_eval.py`

Pentru fiecare skill → fiecare test → fiecare rulare:

1. **Sandbox:** `runner/sandbox.py` creează un folder temporar cu o copie a `.claude/` și doar input-ul testului.
2. **Agent:** `runner/agent_runner.py` rulează writer-ul în sandbox cu `claude -p`. Output-ul se copiază în `results/runs/.../output/`.
3. **Scripturi statice:** `static/run_checks.py` rulează scripturile skill-ului + `check_sensitive.sh`. Rezultat în `static.json`.
4. **Judges:** pentru fiecare judge din `judges/registry.yaml` al skill-ului, apel API cu output-ul, input-ul și câmpurile din referință. Rezultat în `judges.json`.
5. **Scor:** `scoring/` combină rezultatele după `weights.yaml`. Rezultat în `score.json`.
6. La final: `summary.csv` și `report.md`.

CLI:
```
python eval/run_eval.py --skill stake_summary
python eval/run_eval.py --skill all
python eval/run_eval.py --e2e
python eval/judges/calibration/run_calibration.py --judge stake_summary/fidelity
```

---

## 5. Apelarea scripturilor statice

Căile se calculează pornind de la locația fișierului, nu de la directorul curent:

```python
import subprocess
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parents[1]          # static/ -> eval/
CLAUDE_DIR = (EVAL_DIR / config["claude_dir"]).resolve()
SKILLS_DIR = CLAUDE_DIR / "skills"

def run_script(script: Path, *args: Path) -> dict:
    cmd = ["bash", str(script)] if script.suffix == ".sh" else ["python", str(script)]
    r = subprocess.run(
        cmd + [str(a.resolve()) for a in args],
        cwd=script.parent,        # la fel ca atunci când îl apelează reviewer-ul
        capture_output=True, text=True, timeout=60,
    )
    return {"passed": r.returncode == 0, "stdout": r.stdout, "stderr": r.stderr}
```

Reguli:
- `bash script.sh`, nu execuție directă (permisiunea `+x` se pierde la copiere).
- `cwd` = folderul scriptului, ca să-și găsească `criteria.md`, `sensitive_patterns.txt` etc. Verifică ce `cwd` folosesc reviewer-ii și folosește același.
- Căile argumentelor sunt absolute.

### Contract recomandat pentru scripturile existente

Ca evaluarea să obțină valori, nu doar pass/fail, fiecare `check.sh` ar trebui să:
- iasă cu cod `0` (pass) sau `1` (fail);
- scrie pe stdout un JSON, de exemplu:
  ```json
  {"checks": [{"check": "length", "value": 437, "limit": 400, "passed": false}]}
  ```

Reviewer-ii pot citi același JSON. **Dacă scripturile nu au încă acest format, adaptarea lor se face cu grijă, fără a schimba ce verifică, și se testează că reviewer-ii funcționează la fel.**

`check_sensitive.sh` e prag obligatoriu: un output care pică aici are scorul 0 pentru acel test, indiferent de rest.

---

## 6. Seturi de test per skill

### 6.1 `code_doc`
30–50 funcții/clase, în categoriile:

| Categorie | Descriere | Pondere |
|---|---|---|
| `undocumented` | fără documentație | ~30% |
| `correct_doc` | docstring corect | ~20% |
| `wrong_doc` | docstring **greșit intenționat** | ~25% |
| `complex` | excepții, side effects, `**kwargs` | ~25% |

`reference.json`: parametri, tipuri, return, excepții, side effects, eroarea plantată.

### 6.2 `business_context`
10–15 pachete (Lean Canvas PDF + 1–3 pagini Confluence), incluzând: PDF curat, PDF scanat, layout pe grilă, cel puțin 2 pachete cu **contradicții** PDF vs Confluence, cel puțin 2 cu **câmpuri lipsă**, pagini învechite.

`reference.json`: fapte-cheie pe câmpuri (problemă, segment, propunere de valoare, metrici, constrângeri), sursa fiecărui fapt, conflictele, câmpurile care trebuie marcate lipsă.

### 6.3 `model_card`
8–12 proiecte, fiecare în variantele `documented` și `undocumented`. Input-uri **de referință** (context business corect, nu output-ul agentului). În 3–4 proiecte: conflicte plantate între note și cod (ex. note: AUC 0.91, cod: 0.84).

`reference.json`: valori numerice corecte, conflicte plantate, limitări cunoscute.

### 6.4 `stake_summary`
8–12 model card-uri de referință + contextul business.

`reference.json`: 2–3 **fapte critice** obligatorii (de obicei limitări), 5 întrebări fixe cu răspunsuri corecte:
1. Pentru ce este folosit modelul?
2. Când NU trebuie folosit?
3. Cât de bine funcționează, în termeni de business?
4. Care este principalul risc?
5. Ce impact are asupra metricii de business?

### 6.5 `convert`
De definit după specificarea scopului skill-ului.

### 6.6 `e2e`
5–10 proiecte reale complete (cod + documente business + note developer + referință). Lanțul întreg, comparat cu scorurile pe input curat. Pentru fiecare eroare din `stake_summary` se identifică etapa la care a apărut.

---

## 7. Verificări per skill

| Skill | Script (existent) | Judge | Om |
|---|---|---|---|
| code_doc | cod neschimbat (`check_unchanged.py`); sensibil | halucinații; return/excepții corecte; eroare plantată corectată | utilitate, eșantion 10% |
| business_context | `check.sh`; sensibil | recall fapte; precizie; sursă corectă; conflicte semnalate | calitatea extragerii PDF, o dată |
| model_card | `check.sh`; sensibil | afirmații susținute / nesusținute / contrazise; conflicte; limitări specifice | developer, eșantion 3–4 proiecte |
| stake_summary | `check.sh` (lungime, jargon, structură); sensibil | fidelitate; fapte critice; înțelegere (persona manager); legătură business | persoană din business, eșantion |

Ponderi: scripturile statice sunt **prag** (pondere mică, sau fail = 0 pentru `check_sensitive.sh`). Scorul de calitate vine din judges și referință.

---

## 8. `judges/`

```
judges/
├── registry.yaml                # ce judges rulează pe fiecare skill, cu ce input
├── judge_client.py              # apel API comun
├── schemas/
│   ├── claim_verdicts.json      # afirmații: susținută / nesusținută / contrazisă
│   ├── match.json               # elemente: găsit / negăsit
│   └── binary.json              # da/nu cu justificare
├── prompts/<skill>/<judge>.md   # un fișier = o singură întrebare
├── examples/<skill>/<judge>.jsonl   # 2–3 exemple notate de om, inclusiv unul negativ
├── tests/                       # testele judge-ului (secțiunea 9)
└── calibration/
    ├── cases/<skill>/<judge>/
    ├── holdout/<skill>/<judge>/ # 10–15 cazuri ținute deoparte
    ├── human_labels/<judge>.json
    ├── run_calibration.py
    └── reports/<judge>_<data>.md
```

### `registry.yaml` (exemplu)

```yaml
stake_summary:
  - judge: fidelity
    prompt: prompts/stake_summary/fidelity.md
    schema: schemas/claim_verdicts.json
    inputs:
      rezumat: output
      documentatie_model: input
  - judge: critical_facts
    prompt: prompts/stake_summary/critical_facts.md
    schema: schemas/match.json
    inputs:
      rezumat: output
      fapte_critice: reference.critical_facts
```

### Format prompt

```markdown
---
version: 1.0
calibrated: null            # data ultimei calibrări reușite
---
# Rol
# Întrebare (una singură)
# Pași
1. Împarte în elemente (afirmații / fapte).
2. Pentru fiecare, citează fragmentul din sursă care susține sau contrazice.
3. Abia apoi dă verdictul.
# Ce NU notezi
Stil, lungime, ton (dacă nu sunt subiectul întrebării).
# Format răspuns
Doar JSON, conform schemei.
# Exemple
{{examples}}
```

### `judge_client.py`
- încarcă promptul și exemplele;
- construiește input-ul după `registry.yaml`, fiecare câmp într-un tag XML;
- apelează modelul din `config.yaml` (Anthropic SDK, cheie din `ANTHROPIC_API_KEY`);
- validează JSON-ul față de schemă; o reîncercare dacă e invalid;
- refuză un judge cu `calibrated: null` sau a cărui versiune nu are raport de calibrare (flag `--allow-uncalibrated` doar pentru dezvoltare).

### Lista judge-ilor

| Skill | Judge | Întrebare | Schemă |
|---|---|---|---|
| code_doc | hallucination | Docstring-ul conține afirmații nesusținute de cod? | claim_verdicts |
| code_doc | return_exceptions | Return și excepțiile corespund codului? | match |
| code_doc | planted_error_fixed | Eroarea plantată a fost corectată? | binary |
| business_context | recall | Ce fapte de referință apar în output? | match |
| business_context | precision | Fiecare fapt extras apare în surse? | claim_verdicts |
| business_context | source_correct | Sursa citată conține faptul? | match |
| business_context | conflicts | Conflictele cunoscute sunt semnalate? | match |
| model_card | claim_support | Afirmațiile sunt susținute de cod / note / context? | claim_verdicts |
| model_card | conflicts | Conflictele plantate sunt semnalate? | match |
| model_card | limitations_specific | Limitările sunt specifice sau generice? | match |
| stake_summary | fidelity | Există afirmații absente sau distorsionate față de model card? | claim_verdicts |
| stake_summary | critical_facts | Faptele critice apar în rezumat? | match |
| stake_summary | comprehension_answer | (manager non-tehnic) Răspunde folosind doar rezumatul. | — (text) |
| stake_summary | comprehension_grade | Răspunsurile corespund celor corecte? | match |
| stake_summary | business_link | Performanța e legată de metricile de business? | binary |

---

## 9. Testarea judge-ului

Se face **înainte de calibrare**, pe cazuri construite, cu răspuns cunoscut. Testele stau în `judges/tests/` și rulează la orice modificare de prompt.

| Test | Cum | Așteptat |
|---|---|---|
| Format | 10–20 cazuri | JSON valid conform schemei, mereu |
| Prinde greșeala | output corect + aceeași variantă cu **o singură** greșeală plantată | verdict diferit, greșeala identificată |
| Nu inventează | output complet corect | niciun verdict negativ |
| Consistență | același caz × 5 rulări | același verdict |
| Robustețe la formă | același conținut reformulat / reordonat | același verdict |
| Fără preferință de lungime | variantă scurtă corectă vs lungă cu greșeală | scurta trece, lunga pică |
| Rămâne la întrebare | conținut corect, formulare slabă | nepenalizat (dacă stilul nu e subiectul) |

Un judge care nu trece de aceste teste nu merge la calibrare.

---

## 10. Calibrarea judge-ului

1. **Cazuri:** 20–50 per judge, din output-uri **reale** ale agentului, plus câteva cu greșeli plantate. Amestec de bune, proaste, la limită. Plus 10–15 cazuri în `holdout/`.
2. **Doi oameni notează independent**, cu aceeași rubrică ca judge-ul.
3. **Acord om–om** > 85%. Altfel: rubrica e neclară → discuție, rescriere, renotare.
4. **Nota finală** per caz (acord sau după discuție) în `human_labels/`.
5. **Rulare judge** pe cazuri, de 3–5 ori (`run_calibration.py`).
6. **Comparare cu țintele:**

   | Metrică | Țintă |
   |---|---|
   | Acord judge–om (sau Cohen's kappa) | > 85% |
   | Recall pe greșeli plantate | > 90% |
   | Precizie | > 85% |
   | Consistență între rulări | același verdict în aproape toate cazurile |

7. **Analiza dezacordurilor**, caz cu caz (prea îngăduitor, regulă de domeniu neînțeleasă, criterii confundate).
8. **Ajustare prompt:** instrucțiune mai clară, exemplu nou în `examples/`, sau împărțirea în două judge-uri.
9. **Repetă 5–8** până la ținte. Verificare finală pe `holdout/`, ca promptul să nu fie supra-ajustat pe cazurile de calibrare.
10. **Raport** în `calibration/reports/` cu versiunea promptului; actualizare `calibrated` în frontmatter.

Recalibrare la orice schimbare de prompt, model sau rubrică. Verificare lunară: câteva cazuri noi notate de om.

---

## 11. Raportul final

`results/report.md`, generat automat:

| Skill | Metrica principală | Scor | Variație | Problema principală |
|---|---|---|---|---|
| code_doc | acuratețe | | | |
| business_context | F1 fapte | | | |
| model_card | fidelitate | | | |
| stake_summary | fidelitate + înțelegere | | | |
| convert | de definit | | | |
| e2e | fidelitate stake_summary față de realitate | | | |

Plus, per skill: cele mai slabe 5 teste, cu link la output și la detalii. Plus: rata de pică pe `check_sensitive.sh` (ținta: 0).

---

## 12. Ordinea de implementare

1. `eval/config.yaml`, structura de foldere, `README.md`.
2. `static/run_checks.py` + test că apelează corect fiecare script existent (fără a modifica scripturile).
3. Discuție: adaptarea output-ului scripturilor la contractul JSON (secțiunea 5), cu verificare că reviewer-ii funcționează la fel.
4. `runner/sandbox.py` + `runner/agent_runner.py`; test că sandbox-ul **nu conține** `eval/`.
5. Seturile de test și `reference.json` (om), începând cu `business_context` și `model_card`.
6. `judges/judge_client.py`, `schemas/`, `registry.yaml`, prompturile.
7. `judges/tests/` (secțiunea 9).
8. Calibrarea (secțiunea 10).
9. `scoring/`, `run_eval.py`, raportul.
10. `e2e`.
11. Integrare ca test de regresie.

---

## 13. Reguli pentru `CLAUDE.md`

```
## Evaluare (eval/)
- Planul complet: docs/dsdoc-eval-plan.md.
- eval/ nu intră niciodată în .claude/ și nu se copiază în proiectele de lucru.
- Datele de referință (eval/datasets/**/reference.json, eval/judges/calibration/**) nu sunt citite de agenți sau skill-uri.
- Agentul evaluat rulează doar în sandbox (copie .claude/ + input test, fără eval/).
- Scripturile statice din .claude/skills/ se apelează, nu se copiază și nu se reimplementează în eval/.
- Judge-ii sunt apeluri API din eval/, nu agenți în .claude/agents/; alt model decât agentul, temperatura 0.
- criteria.md ale reviewer-ilor nu se folosesc ca rubrică pentru judge.
- Un judge = o întrebare; output JSON; justificare înainte de verdict.
- Niciun judge necalibrat în evaluarea propriu-zisă.
- Fiecare test rulează de N ori (config.yaml); se raportează media și variația.
- Reviewer-ii nu sunt evaluați deocamdată.
```
