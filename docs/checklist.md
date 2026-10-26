[Leer en español](checklist.es.md) · [Back to README](../README.md)

# Spec review checklist

Copy this into the ticket or the review doc and tick it before anyone writes code. Each line exists because a real finding in this case study needed it (in brackets).

## 0. Read once for intent
- [ ] I can say what the system does in 5 lines, and the owner agrees with them.
- [ ] I know where the spec came from. If it was built from a screenshot or someone else's demo, its numbers are examples, not requirements. [F01–F10]

## 1. Recompute every number
- [ ] Parts add up to the totals (sources → unique, per-item list → grand total). [F01, F05]
- [ ] Percentages of the same total are compatible with each other (they cannot add up to more than 100 % when they exclude each other). [F02]
- [ ] Counts of things match their lists (14 claimed = 14 listed = 14 drawn). [F05]
- [ ] Time windows match their names ("weekly" = 7 days). [F06]
- [ ] Units are complete: tokens in **and** out, every paid component in the cost. [F07, F08]

## 2. Cross-check the same fact everywhere
- [ ] The same quantity has the same value in every section, card, bar and panel. [F04]
- [ ] The same word means the same thing everywhere ("noise" as a class vs a label). [F03]
- [ ] What a prompt or rule promises (e.g. "max 3 actions") matches what the mock-up shows. [F04]

## 3. Trace every requirement
- [ ] Every KPI and every score has a written formula. [F12]
- [ ] Every box in the architecture has a provider, an API and a price. [F11]
- [ ] Every field says who knows it: the model, the data or a person. Facts that come from data are computed in code. [F14]
- [ ] Labels in a single-choice list exclude each other. [F14]
- [ ] Each tool can actually do what its rule asks (search ≠ change detection). [F16]
- [ ] The key inputs exist, with content, not just a table for them. [F18]
- [ ] The schema survives the lifecycle: re-run, reclassify, group by period, audit who reviewed what. [F17]

## 4. Check requirements against reality
- [ ] Non-functional requirements fit how the system runs (no latency target for a weekly batch; no "live" badge on a weekly job). [F09]
- [ ] Every rule has a volume estimate, so no single rule floods a human queue. [F15]
- [ ] Thresholds on model probabilities come with a calibration plan and a labelled set. [F13]
- [ ] Data sources are allowed by their terms of use, and the official API covers what you need. [F19]

## 5. Check the tests the spec ships
- [ ] Each acceptance test proves a behaviour; none of them just replays the demo's numbers. [F10]
- [ ] Each "precision" or "accuracy" criterion names what it is measured against. [F13]

## 6. Close the review
- [ ] Every finding has: what it said, why it is a problem, how it was found, severity, decision or question.
- [ ] Blockers become questions for the owner, numbered, answerable in minutes.
- [ ] The build is cut into phases with a gate each; the UI comes after the value is proven.
