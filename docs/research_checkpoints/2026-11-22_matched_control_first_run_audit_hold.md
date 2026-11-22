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
2. **Channel-width thresholds were hard-coded in the supplied script but their exact numeric values are not recorded in the accepted breakout-results document.** They must be recovered from the original calculation or recomputed using the identical quantile procedure before matching results can be trusted.
3. **MAE convention is incorrect for observations with no adverse excursion.** The script can report positive MAE when every observed price excursion is favourable relative to the follow-up start. For consistency with the prior breakout study's adverse-excursion convention, MAE must be floored at zero (never positive): for upper direction, min(0, minimum(low / entry - 1) times 100); for lower direction, min(0, minimum(entry / high - 1) times 100).
4. The current script uses its own reconstructed candidate-control episode logic and greedy matching. These choices need to be explicitly validated against the agreed plan before accepting the matched sample.
5. Strict and broad samples can overlap, and follow-up windows overlap. Any inferential intervals remain approximate and must not be interpreted as independent-event confidence intervals.

## Current interpretation
The output is useful as a debugging run only. No conclusion that breakouts outperform, underperform, or resemble controls is accepted. Do not combine these figures with the final timing-corrected breakout study, and do not use them to choose a strategy.

## Required next steps
- Recover or reproduce the exact original 48H channel quantiles and breakout-event construction.
- Make the matched script reproduce the accepted breakout counts before matching.
- Correct MAE to be non-positive and validate control follow-up calculations.
- Then rerun the matched comparison read-only and audit the output before publishing empirical results.

The original timing-corrected breakout study remains the accepted descriptive study; this first matched-control run is held pending correction.
