# Matched non-breakout control study: first run audit and hold (2026-11-22)

**Status: preliminary output received; NOT accepted as empirical findings. Do not use for strategy decisions.**

## Run conditions
- User ran the supplied read-only Python script against the existing five 1-minute CSVs.
- Common minute timestamps: 569,125.
- Complete bars reported per asset: 37,941 15M and 2,370 4H.
- Script reported 1,290 matched pairs across asset / definition / direction groups.
- No local files were written or changed, according to the script.

## Audit findings requiring correction

1. **Breakout event counts do not reproduce the accepted timing-corrected study.** The accepted broad-P40 counts are BTC 91 lower / 115 upper; ETH 87 / 77; SOL 117 / 96; DOGE 81 / 75; AVAX 84 / 109. The matched-control script instead reported BTC 84 / 102; ETH 74 / 66; SOL 103 / 86; DOGE 74 / 63; AVAX 74 / 96. Strict counts also differ. The candidate construction therefore is not yet a verified reproduction of the prior signal set.
2. **Channel-width thresholds were hard-coded in the supplied matched-control script and differed from the recovered original values.** Exact full-sample thresholds recovered from the original research are:
   | Asset | P25 | P40 |
   |---|---:|---:|
   | BTC | 3.2422% | 3.9486% |
   | ETH | 4.2481% | 5.4819% |
   | SOL | 5.0673% | 6.1145% |
   | DOGE | 5.1657% | 6.2641% |
   | AVAX | 5.7061% | 6.9162% |
   The first matched-control script used different P25 values for ETH (4.2423), SOL (5.0670), and AVAX (5.7036). BTC and DOGE P25 values and all P40 values matched the recovered table.
3. **MAE convention is incorrect for observations with no adverse excursion.** The script can report positive MAE when every observed price excursion is favourable relative to the follow-up start. For the matched-control study, use a non-positive adverse-excursion convention: upper direction `min(0.0, min((low / entry - 1) * 100))`; lower direction `min(0.0, min((entry / high - 1) * 100)`.
4. The candidate-control construction and matching choices need to be explicitly checked against the agreed plan. The current script uses greedy sorted-edge matching, not a globally optimal one-to-one assignment. This can be retained only if explicitly labelled as greedy matching.
5. Strict and broad samples can overlap, and follow-up windows overlap. Any inferential intervals remain approximate and must not be interpreted as independent-event confidence intervals.
6. The first matched-control script's timestamp lookup selected the next available common timestamp without proving it was exactly one minute after the signal's final 1M candle. Follow-up windows also need explicit 1-minute continuity validation through their final horizon candle.
7. The script does not fully deliver the agreed outcome report: it omits most calculated threshold-hit and time-to-threshold results, mean/P75/P90 MFE and MAE, net movement summaries, and matching balance diagnostics (standardized differences before and after matching).
8. The fixed feature scales, distance threshold, and calendar-time contribution need a transparent matching-quality review. Counts and median distance alone do not demonstrate covariate balance. These choices must not be silently relaxed to increase match count.

## Correction: recovered original final breakout event construction

The user subsequently supplied the complete **final timing-corrected breakout and retest script**. A focused recovery of the earlier research conversation confirms that the accepted final script's event masks are:

- `same_snapshot = joined["snapshot"].eq(joined["snapshot"].shift(1))`
- Upper: `sideways & same_snapshot & (previous_close <= upper) & (current_close > upper)`
- Lower: `sideways & same_snapshot & (previous_close >= lower) & (current_close < lower)`

Important clarification: the accepted **final timing-corrected** script does **not** require `previous_sideways = sideways.shift(1)`. That condition appeared in an earlier construction, but was not part of the final accepted timing-corrected event mask. The earlier audit note claiming it was required by the accepted final script was incorrect and is superseded by this correction.

The accepted final script also has **no explicit breakout de-clustering or cooldown**. It iterates every qualifying crossing in the signal mask. Overlapping breakout follow-up windows are allowed. Do not add de-clustering to the reproduction check; doing so would change the accepted event definition and likely change the counts.

The final timing convention is:
- 15M labels represent candle closing times.
- The final 1M candle inside the signal is timestamped at `signal_time - 1 minute`.
- Follow-up begins at the next 1M candle open.
- The first follow-up minute is included in the retest search.

The user's newly pasted final timing-corrected script matches the recovered final event-mask structure. It should be used as the reference for the accepted event definition, rather than the earlier preliminary variant.

## Accepted breakout counts to reproduce

| Asset | Broad lower | Broad upper | Strict lower | Strict upper |
|---|---:|---:|---:|---:|
| BTC | 91 | 115 | 62 | 81 |
| ETH | 87 | 77 | 51 | 51 |
| SOL | 117 | 96 | 77 | 71 |
| DOGE | 81 | 75 | 55 | 65 |
| AVAX | 84 | 109 | 64 | 83 |

## Current interpretation and hold

The first matched-control output is useful only as a debugging run. No conclusion that breakouts outperform, underperform, or resemble controls is accepted. Do not combine its figures with the final timing-corrected breakout study, and do not use them to choose a strategy.

The original breakout/retest study remains the accepted descriptive study. The first matched-control run remains NOT VALIDATED. Before any new matched-control run:
- Reproduce all 20 accepted breakout counts using the final event-mask structure above and the exact recovered thresholds.
- Preserve the original event definition: no added previous-sideways requirement and no de-clustering.
- Correct MAE and enforce exact minute continuity for follow-up windows.
- Validate the control eligibility, matching procedure, covariate balance, and full outcome report.
- Keep the new calculation read-only.

No empirical matched-control conclusion is accepted until these checks pass.
