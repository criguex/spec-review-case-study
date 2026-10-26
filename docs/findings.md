[Leer en español](findings.es.md) · [Back to README](../README.md)

# The 19 findings

Every finding below comes from the written review of the spec (section "Gaps and doubts", items 1 to 19) and from the three places where the spec itself left a formula blank. Nothing was added afterwards. Names are anonymized and spec text is paraphrased, never copied.

**Severity scale used here**

| Level | Meaning |
|---|---|
| Blocker | You cannot build or test this part until someone answers |
| High | If built as written, the product shows a wrong number, does the wrong thing, costs more than promised or carries legal risk |
| Medium | Misleading or unexplained, but it does not stop the build |

**Status:** *Proposed* means the review suggested a concrete change. *Open* means it became a question for the product owner.

Findings F01 to F08 are recomputed by [`check_numbers.py`](../check_numbers.py).

## A. Numbers that do not add up

### F01 · Deduplication happens only on one side, and nobody says why
- **The spec said:** social sources bring about 1,334 signals and web sources about 1,158; after deduplication there are 2,070 unique signals. The KPI card splits them as "1,334 social · 736 web".
- **Why it is a problem:** 1,334 + 1,158 = 2,492, so 422 signals (17 %) were removed. The card keeps all 1,334 social ones, which means every duplicate was web: 36 % of web signals removed, 0 % of social. That can be true, but the dedup rule is never described, so nobody can build or test it.
- **How it was detected:** adding the two source totals and comparing with the unique total, then cross-checking against the card subtitle.
- **Severity:** Medium.
- **Decision / proposal:** Proposed. Deduplicate by the post or ad's own external id, in code, and treat the demo figures as examples, not requirements.

### F02 · 85 % threats and 67 % noise cannot both be true
- **The spec said:** "Threats flagged: 1,753" out of 2,070 signals, and a noise filter at 67 %.
- **Why it is a problem:** 1,753 is 85 % of 2,070. If 67 % is noise, at most 33 % (683 signals) can be anything else. The two headline numbers contradict each other.
- **How it was detected:** turning both KPIs into percentages of the same total.
- **Severity:** High. These are the two numbers the dashboard leads with.
- **Decision / proposal:** Open. The owner has to define what counts as a threat and what counts as noise.

### F03 · "Noise" is 67 % in one place and 4 % in another
- **The spec said:** noise filtered = 67 %; in the label taxonomy, `ignore` = 4 %.
- **Why it is a problem:** two different ideas of "noise" (a classification and a move type) are mixed, and the numbers do not reconcile.
- **How it was detected:** comparing the KPI with the label distribution given in the business-rules section.
- **Severity:** Medium.
- **Decision / proposal:** Open, together with F02.

### F04 · Escalations: 31, 2 or 2? And the brief promises 3 actions but shows 2
- **The spec said:** the KPI card reads "31 escalated to a human"; the pipeline bar reads "2 escalated"; the human-review panel lists 2. The bar also says "3 actions" and the brief shows 2.
- **Why it is a problem:** the human inbox is the main output of the system. Three parts of the same screen give two different counts.
- **How it was detected:** finding every place the same quantity appears and comparing them.
- **Severity:** High.
- **Decision / proposal:** Open.

### F05 · The competitor list is short by 2 competitors and 553 signals
- **The spec said:** 14 competitors are monitored. It lists 12 with their weekly volumes. The graph component draws 7.
- **Why it is a problem:** the 12 listed volumes add up to 1,517, not 2,070. 553 signals (27 %) belong to nobody. Three counts of competitors: 14, 12, 7.
- **How it was detected:** adding the per-competitor list and counting its items.
- **Severity:** Medium.
- **Decision / proposal:** Open. The owner names 3 to 5 real competitors for the first version.

### F06 · A "weekly" window that lasts 38 days
- **The spec said:** "weekly window (e.g. 20 Aug – 27 Sep)".
- **Why it is a problem:** that range is 38 days. Every weekly count depends on what "a week" means.
- **How it was detected:** date arithmetic on the example.
- **Severity:** Medium.
- **Decision / proposal:** Open.

### F07 · "Tokens processed" leaves out 99 % of the tokens
- **The spec said:** "Tokens processed: 24,849", described as 12 output tokens per signal; elsewhere it says input is about 1,000 tokens per signal.
- **Why it is a problem:** input is about 2.07 million tokens, 99 % of the total, and does not appear in the KPI that claims to count tokens.
- **How it was detected:** multiplying the spec's own per-signal input by the number of signals.
- **Severity:** Medium.
- **Decision / proposal:** Open. The KPI has to say which tokens it counts.

## B. Costs and latencies given as facts

### F08 · The weekly spend only covers one part of the bill
- **The spec said:** week spend $0.2087, "$0.0001 per 4-judgment call".
- **Why it is a problem:** $0.2087 matches about 2.07 M input tokens at $0.10 per million, so it counts only the classifier's input. Scraping, web search and the weekly brief model are not in it. The real weekly cost is higher.
- **How it was detected:** working backwards from the price to tokens × unit price, then listing every paid component in the architecture and checking which ones the number covers.
- **Severity:** High. Budget decisions are made with this number.
- **Decision / proposal:** Proposed. A cost table per component: about $0–1 a month for a first version with 5 competitors, about $6–20 a month at 14. Prices to be verified before paying.

### F09 · A latency requirement for a job that runs once a week
- **The spec said:** P50 latency of 214 ms per signal is a non-functional requirement, and the UI shows a "LIVE / real time" badge.
- **Why it is a problem:** in a weekly batch latency does not matter. A batch mode that takes hours is about 50 % cheaper. "Real time" contradicts "weekly".
- **How it was detected:** checking each non-functional requirement against how the system actually runs.
- **Severity:** Medium.
- **Decision / proposal:** Proposed. Classify in batch mode; drop the latency requirement and the "LIVE" claim.

### F10 · Three acceptance tests that replay the demo's numbers
- **The spec said:** one test expects week spend $0.2087 ± $0.01, another expects the noise meter at 67 %, another expects P50 between 200 and 250 ms.
- **Why it is a problem:** a test must check behaviour, not reproduce one week of someone else's data. With real data these tests fail even when the system works, or pass when it does not.
- **How it was detected:** asking, for each test, "what behaviour does this prove?"
- **Severity:** High.
- **Decision / proposal:** Proposed. One test with 10 fixed signals that checks the output contract (strict JSON) and the escalation rules.

## C. Things that are not defined

### F11 · The classifier has a name and nothing else
- **The spec said:** every signal is judged by "Classifier X".
- **Why it is a problem:** no vendor, no endpoint, no price. It cannot be built or costed.
- **How it was detected:** tracing every box in the architecture to a provider, an API and a price.
- **Severity:** Blocker.
- **Decision / proposal:** Proposed. Use a small, low-cost general LLM with structured JSON output.

### F12 · Three of the six KPI formulas are blank
- **The spec said:** the formulas for "signals ingested", "week spend" and "noise %" are empty (the spec itself marks them as blank in the original); `threat_score` has no formula at all.
- **Why it is a problem:** you cannot implement or test a number nobody has defined.
- **How it was detected:** checking that every KPI and every score has a formula.
- **Severity:** Blocker.
- **Decision / proposal:** Open.

### F13 · The 0.85 threshold sits on probabilities nobody calibrated
- **The spec said:** escalate when the model's "same buyer" and "respond this week" probabilities are both ≥ 0.85; one test expects the model to "discriminate with precision".
- **Why it is a problem:** probabilities an LLM writes are not calibrated. Without a labelled set, 0.85 is arbitrary and "precision" cannot be measured.
- **How it was detected:** asking what ground truth the threshold and the test would be measured against.
- **Severity:** High.
- **Decision / proposal:** Proposed. A calibration phase: the owner labels about 100 signals as useful or noise; precision is measured and the prompt and thresholds are tuned with that.

### F14 · Labels the model cannot know, and one label where two apply
- **The spec said:** the model picks one label from a list that includes `14_days_live` and `repeat_3_plus_times`.
- **Why it is a problem:** how long an ad has run and how often something repeats come from the data (ad start date, history), not from reading the text. And an ad running for 18 days is both `paid_ad` and `14_days_live`; a single label cannot hold both.
- **How it was detected:** for each field, asking who actually knows the fact; then checking that the labels exclude each other.
- **Severity:** High.
- **Decision / proposal:** Proposed. Compute days running and repeats in code; keep the model for judgment only.

### F15 · One rule alone floods the human inbox
- **The spec said:** any ad running 14 days or more goes straight to human review.
- **Why it is a problem:** the spec's own example says Competitor 6 runs 340 ads, 42 of them 14+ days old. That one competitor already puts 42 items in the inbox.
- **How it was detected:** estimating how many items each rule triggers, using the spec's own numbers.
- **Severity:** High.
- **Decision / proposal:** Open. Raised as a risk.

### F16 · A search tool asked to detect changes
- **The spec said:** escalate when the web source "detects" a new free tool or a change in the homepage headline or price (example: Competitor 7 shipped a free calculator).
- **Why it is a problem:** a search API finds pages; it does not tell you what changed. Detecting a change needs stored copies of each page to compare, and the schema has no table for them.
- **How it was detected:** checking whether each tool can do what its rule needs, then looking for the data in the schema.
- **Severity:** Blocker for this rule.
- **Decision / proposal:** Proposed. Download 2–3 URLs per domain and compare with the previous copy (free, no search API needed for this).

### F17 · The database cannot hold the system's own lifecycle
- **The spec said:** one evaluation per signal (`UNIQUE signal_id`), no week field, no ad start date, a review status with no reviewer.
- **Why it is a problem:** you cannot reclassify a signal, group by week, compute how long an ad ran, or know who reviewed an item and with what note.
- **How it was detected:** walking the schema through the lifecycle: ingest, classify, reclassify, review, report by week.
- **Severity:** High.
- **Decision / proposal:** Open.

### F18 · The key input is missing: our own offer and buyer
- **The spec said:** question 3 ("does it target our same buyer?") reads our offer and our ideal buyer from a config table. The spec gives the table but no content, and the competitors are public figures from someone else's demo.
- **Why it is a problem:** without our offer, our buyer and our real competitors, question 3 answers nothing.
- **How it was detected:** tracing the inputs of each model question back to where the data comes from.
- **Severity:** Blocker.
- **Decision / proposal:** Open. First two questions for the owner: the exact offer and ideal buyer in 2–3 lines, and 3–5 real competitors with their accounts.

### F19 · Scraping the big social networks breaks their terms of use
- **The spec said:** collect posts and ads from three social networks and an ad library through a scraping service.
- **Why it is a problem:** scraping those platforms goes against their terms of use. The scraping service takes care of the technical side, not the legal one. The ad library's official API only covers political or social-issue ads outside the EU.
- **How it was detected:** checking each data source against its terms and its official API.
- **Severity:** High.
- **Decision / proposal:** Open. Which channels go into the first version is one of the owner's decisions.

## What came out of it

The review closed with a phased plan instead of a build:

| Phase | What | Gate |
|---|---|---|
| P0 · Define | No code. The owner answers 7 questions (offer and buyer, 3–5 real competitors, channels, classifier, where the brief arrives, where it runs, UI later) | Answers in hand |
| P1 · MVP (1–2 days) | One script, no UI, weekly schedule. Dedup by external id; days running and web changes computed in code; batch classification with strict JSON; a short brief sent by message | A test with 10 fixed signals: JSON contract and escalation rules |
| P2 · Calibrate (2–4 weeks of use) | The owner labels about 100 signals; measure precision, tune prompt and thresholds; repeats computed from history | Precision measured, not assumed |
| P3 · UI | A read-only dashboard; a table of threats is enough to start | Only if P2 shows value |
| P4 · Scale | 14+ competitors | |

The general reading of the spec: it looked reverse-engineered from a screenshot of another company's demo (a header with that company's name, competitors who are real public figures, one week of numbers written as requirements). That observation explains most of the findings above.
