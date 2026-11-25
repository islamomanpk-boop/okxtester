# Research Governance Rules V1

**Status:** Mandatory project-wide research standard  
**Adopted:** 2026-11-25  
**Applies to:** Every research phase, diagnostic, validation, backtest, and strategy study in OKX Price Action V1.

## Core principle

The purpose of this project is to produce reliable knowledge and better decisions, not to maximize the number of scripts, workflow runs, charts, CSV files, or experiments. A technically successful run is not, by itself, a successful research result.

Every study must answer a meaningful question, explain what the evidence means, and state what decision follows. If a proposed study cannot plausibly change knowledge, confidence, or a project decision, do not run it without first explaining why it is still necessary.

## Required study contract (before coding)

Every new study must have a short, version-controlled protocol that states:

1. **Research question:** The precise uncertainty being investigated.
2. **Motivation:** Why the answer matters to market understanding or a later system decision.
3. **Hypothesis / competing explanations:** What patterns are expected and what would contradict them. Exploratory studies must be explicitly labelled exploratory.
4. **Data and population:** Assets, dates, source files, inclusion/exclusion rules, unit of analysis, and known limitations.
5. **Method:** Definitions, calculations, comparison groups, sampling, and dependence treatment.
6. **Causality and timing safeguards:** What information is available at each timestamp; no look-ahead, future leakage, fabricated bars, or gap-bridging.
7. **Decision criteria:** What evidence would support, weaken, reject, or leave the question unresolved.
8. **Stopping rule:** When the question is sufficiently answered, infeasible, or not worth further work.
9. **Expected practical consequence:** Which later decision could change based on the result.

Thresholds and parameters must be justified and frozen before examining the outcomes they could influence. If the work is exploratory, say so and do not relabel it as confirmatory afterward.

## Required study closeout (after execution)

Every completed or rejected study must record:

1. **Question revisited** — what was actually tested.
2. **Evidence** — sample sizes, coverage, effect estimates/distributions, uncertainty, robustness, and relevant negative findings.
3. **Lesson** — what we learned in plain language.
4. **Decision** — accept, reject, defer, or investigate; explain why.
5. **Practical implication** — what this changes (or does not change) for the future system.
6. **Limitations / unknowns** — what the study cannot establish.
7. **Reproducibility** — code/version, source hashes, tests, workflow run, and permanent archive locations.
8. **Follow-up or stop** — the single next research question, or an explicit statement that no further work is justified.

## Evidence and interpretation rules

- Distinguish descriptive association, predictive evidence, causal evidence, and executable/trading performance. They are not interchangeable.
- A positive historical association is not automatically a tradable edge.
- A failed test, rejected method, null result, weak effect, or infeasible design is a valid research result when correctly documented.
- Do not force sample size, balance, thresholds, or a preferred conclusion by repeatedly changing definitions after seeing results.
- Report adverse, contradictory, asset-specific, and time-period-specific findings; do not report only favorable pooled results.
- Treat overlapping events, nested cohorts, repeated candles, and serially dependent observations as dependent unless the method explicitly addresses that dependence.
- Report uncertainty and sample sizes beside estimates. Do not treat narrow bootstrap intervals as proof against selection bias, confounding, multiple testing, or measurement error.
- Preserve all prior versions, failed runs, and rejected methods. Never silently overwrite historical evidence.
- No strategy optimization, parameter sweeps, profitability claims, or live-readiness claims before the relevant descriptive and validation gates are passed.

## Completion gate

A study is **not complete** merely because code ran, tests passed, or files were uploaded. It is complete only when:
- the protocol and implementation are archived;
- tests and workflow are verified;
- outputs are permanently archived and checked;
- the evidence has been interpreted;
- a written lesson and decision exist;
- limitations and remaining unknowns are explicit; and
- the project records what should happen next or why it should stop.

A research phase may be closed as *core scope complete* without claiming that every possible question in that market regime has been answered. The closeout must identify the scope boundary and unresolved questions.

## Required final communication

For each substantial study, provide the user a plain-language report covering: question, what was done, key findings, what was learned, what was not proven, decision, practical consequence, and next step. Avoid dumping raw output without interpretation.

## Project-level rule

**Research must produce knowledge, and knowledge must inform decisions. If neither happens, the work is not justified.**
