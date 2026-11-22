# Sideways Boundary Repeated-Test and Post-Rejection Timing Validation

**Date:** 2026-11-22  
**Status:** STRUCTURAL/TIMING VALIDATION PASS — POST-REJECTION OUTCOMES NOT YET STUDIED  
**Branch:** `price-action-v1`  
**Scope:** BTC, ETH, SOL, DOGE, AVAX; read-only analysis of existing 1M CSVs.

## Validation result

- Common 1M timestamps: **569,125**
- Non-consecutive common-minute intervals: **0**
- Complete 15M bars per asset: **37,941**
- Complete 4H bars per asset: **2,370**
- Rejection mapping checks: **2,095**
- Mapping failures: **0**
- Final audit status: **PASS**

The 2,095 figure is the number of checks across overlapping strict/broad definitions and upper/lower directions. It is **not** a count of unique market events.

For every identified rejection in each definition/direction cohort, the script checked that:
1. The 15M candle was represented by exactly 15 consecutive 1M candles.
2. The first and last constituent minute timestamps were rejection label minus 15 minutes and minus 1 minute.
3. The reconstructed 1M open, high, low, and close matched the 15M OHLC.
4. The next 1M timestamp existed exactly at the 15M rejection label.

All checks passed. This validates timing/reconstruction, not subsequent market behaviour.

## Repeated-test definition applied

- 4H context uses the prior 12 completed 4H candles (48 hours).
- Strict/broad channel-width thresholds are dynamic full-sample P25/P40; retrospective and exploratory.
- Sideways conditions: width threshold, directional efficiency <= 0.30, overlap >= 0.70.
- The first 15M candle after a new 4H snapshot is suppressed by the same-snapshot rule.
- Upper/lower wick touch enters the outer 10% of the frozen channel.
- A subsequent test requires a completed **non-touch** 15M candle to close at least 20% of channel width away from the tested boundary. A touch candle cannot confirm separation.
- At most the first strong rejection per test is counted.
- Test rank resets with snapshot/context/continuity reset.

This is the strict non-touch separation interpretation. It is a refinement of the earlier preliminary repeated-test audit; earlier counts are not interchangeable.

## Repeated-test results

Each cell is **tests with first strong rejection / total tests**.

| Asset | Definition | Side | Test 1 | Test 2 | Test 3 | Test 4+ | Total tests | Rejections |
|---|---|---|---:|---:|---:|---:|---:|---:|
| BTC | Strict | Upper | 89/119 | 14/21 | 3/3 | 1/1 | 144 | 107 |
| BTC | Strict | Lower | 59/99 | 5/7 | 0/0 | 0/0 | 106 | 64 |
| BTC | Broad | Upper | 114/162 | 18/25 | 3/3 | 1/1 | 191 | 136 |
| BTC | Broad | Lower | 90/145 | 6/11 | 0/0 | 0/0 | 156 | 96 |
| ETH | Strict | Upper | 82/112 | 14/16 | 3/3 | 0/0 | 131 | 99 |
| ETH | Strict | Lower | 68/102 | 6/8 | 1/2 | 0/0 | 112 | 75 |
| ETH | Broad | Upper | 109/152 | 17/19 | 3/3 | 0/0 | 174 | 129 |
| ETH | Broad | Lower | 94/149 | 8/11 | 1/2 | 0/0 | 162 | 103 |
| SOL | Strict | Upper | 81/117 | 6/10 | 1/1 | 0/0 | 128 | 88 |
| SOL | Strict | Lower | 84/132 | 10/12 | 0/0 | 0/0 | 144 | 94 |
| SOL | Broad | Upper | 102/152 | 7/12 | 1/1 | 0/0 | 165 | 110 |
| SOL | Broad | Lower | 124/195 | 11/14 | 0/0 | 0/0 | 209 | 135 |
| DOGE | Strict | Upper | 75/110 | 15/17 | 2/3 | 0/1 | 131 | 92 |
| DOGE | Strict | Lower | 73/106 | 11/14 | 0/0 | 0/0 | 120 | 84 |
| DOGE | Broad | Upper | 92/136 | 17/20 | 2/3 | 0/1 | 160 | 111 |
| DOGE | Broad | Lower | 109/159 | 14/17 | 0/0 | 0/0 | 176 | 123 |
| AVAX | Strict | Upper | 83/122 | 8/10 | 0/0 | 0/0 | 132 | 91 |
| AVAX | Strict | Lower | 87/121 | 9/14 | 0/0 | 0/0 | 135 | 96 |
| AVAX | Broad | Upper | 126/173 | 13/18 | 0/0 | 0/0 | 191 | 139 |
| AVAX | Broad | Lower | 109/159 | 14/19 | 0/0 | 0/0 | 178 | 123 |

## Interpretation limits

- These are descriptive test/rejection incidence counts, not evidence that a rejection successfully predicts a move.
- Second/third/fourth-test denominators are often small. Do not infer a universal repeated-test effect.
- Strict and broad cohorts overlap; upper/lower cohorts can also overlap in time. Counts must not be summed as unique events.
- The mapping check validates the 15M candle and next-minute timestamp. It does not yet validate every future outcome horizon.
- No MFE, MAE, retest, midpoint/opposite-boundary, continuation/failure, fills, fees, funding, or profitability outcomes were calculated.
- No local files were written or changed.

## Next research step

Freeze this validated event definition and measure post-rejection behaviour from the next eligible 1M candle: immediate continuation versus pullback-first, retest timing/depth, movement toward channel midpoint/opposite boundary, failure through the rejected boundary, directional MFE/MAE, net movement, and threshold-hit timing across 15M, 1H, 4H, 12H, and 24H horizons. Require exact timestamp continuity and report denominators, exclusions, and overlapping-event dependence. This remains descriptive research, not a strategy backtest.
