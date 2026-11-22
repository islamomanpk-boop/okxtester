# Sideways Boundary Repeated-Test Audit — Preliminary Results

**Date:** 2026-11-22  
**Status:** PRELIMINARY DESCRIPTIVE AUDIT — NOT AN ACCEPTED OUTCOME STUDY  
**Repository:** `islamomanpk-boop/okxtester`  
**Branch:** `price-action-v1`

## Purpose

Record the user-run read-only repeated boundary-test audit using the predeclared 20% channel-width separation rule. This is a descriptive event/rejection-incidence audit only. It does not measure post-rejection price outcomes, executable fills, costs, or profitability.

## Data and structural checks

- Five assets: BTC, ETH, SOL, DOGE, AVAX.
- Common 1M timestamps: 569,125.
- Non-consecutive common-minute intervals: 0.
- Each asset: 37,941 complete 15M bars and 2,370 complete 4H bars.
- Dynamic 48H channel-width thresholds were reproduced:
  - BTC P25 3.242203%, P40 3.948630%.
  - ETH P25 4.242326%, P40 5.481886%.
  - SOL P25 5.067043%, P40 6.114542%.
  - DOGE P25 5.165724%, P40 6.264058%.
  - AVAX P25 5.703625%, P40 6.916216%.
- Script reported FINAL AUDIT STATUS: PASS. This means only its programmed structural invariants passed; it is not independent validation of the event definition or market conclusions.
- No local files were written or changed by the run.

## Rule used

A boundary touch enters the outer 10% of the frozen channel width. A subsequent touch is counted as a new test only after a close confirms separation by at least 20% of channel width from that same boundary. Upper and lower sides use mirrored rules. Test numbering resets with each 4H snapshot. Strong rejection is determined from the 15M touch candle close relative to the inner edge of the 10% touch zone and the opposite channel boundary.

## Results

Each cell is strong-rejection events / total tests (percentage).

| Asset | Definition | Side | Test 1 | Test 2 | Test 3 | Test 4+ |
|---|---|---|---:|---:|---:|---:|
| BTC | Strict | Upper | 89/119 (74.79%) | 16/27 (59.26%) | 3/3 (100%) | 1/2 (50%) |
| BTC | Strict | Lower | 59/99 (59.60%) | 10/13 (76.92%) | 2/3 (66.67%) | 1/1 (100%) |
| BTC | Broad | Upper | 114/162 (70.37%) | 20/31 (64.52%) | 3/3 (100%) | 1/2 (50%) |
| BTC | Broad | Lower | 90/145 (62.07%) | 11/17 (64.71%) | 2/3 (66.67%) | 1/1 (100%) |
| ETH | Strict | Upper | 82/112 (73.21%) | 15/17 (88.24%) | 4/4 (100%) | 0/0 (N/A) |
| ETH | Strict | Lower | 68/102 (66.67%) | 8/10 (80.00%) | 2/3 (66.67%) | 1/1 (100%) |
| ETH | Broad | Upper | 109/152 (71.71%) | 19/21 (90.48%) | 4/4 (100%) | 0/0 (N/A) |
| ETH | Broad | Lower | 94/149 (63.09%) | 10/13 (76.92%) | 3/4 (75.00%) | 1/1 (100%) |
| SOL | Strict | Upper | 81/117 (69.23%) | 12/17 (70.59%) | 2/2 (100%) | 0/1 (0%) |
| SOL | Strict | Lower | 84/132 (63.64%) | 14/17 (82.35%) | 0/0 (N/A) | 0/0 (N/A) |
| SOL | Broad | Upper | 102/152 (67.11%) | 13/20 (65.00%) | 2/2 (100%) | 0/1 (0%) |
| SOL | Broad | Lower | 124/195 (63.59%) | 17/21 (80.95%) | 0/0 (N/A) | 0/0 (N/A) |
| DOGE | Strict | Upper | 75/110 (68.18%) | 18/21 (85.71%) | 3/4 (75.00%) | 0/1 (0%) |
| DOGE | Strict | Lower | 73/106 (68.87%) | 16/19 (84.21%) | 0/1 (0%) | 0/0 (N/A) |
| DOGE | Broad | Upper | 92/136 (67.65%) | 20/24 (83.33%) | 3/4 (75.00%) | 0/1 (0%) |
| DOGE | Broad | Lower | 109/159 (68.55%) | 19/22 (86.36%) | 0/1 (0%) | 0/0 (N/A) |
| AVAX | Strict | Upper | 83/122 (68.03%) | 10/12 (83.33%) | 1/1 (100%) | 0/0 (N/A) |
| AVAX | Strict | Lower | 87/121 (71.90%) | 11/18 (61.11%) | 1/1 (100%) | 0/0 (N/A) |
| AVAX | Broad | Upper | 126/173 (72.83%) | 17/22 (77.27%) | 1/1 (100%) | 0/0 (N/A) |
| AVAX | Broad | Lower | 109/159 (68.55%) | 16/23 (69.57%) | 1/1 (100%) | 0/0 (N/A) |

## Interpretation limits

1. Test 1 and test 2 rejection incidence varies by asset, side, and strict/broad definition. There is no consistent universal increase or decrease on the second test.
2. Test 3 and 4+ samples are extremely small (often one to four events). Their percentages are unstable and should not be interpreted as evidence of a repeat-test advantage.
3. A strong rejection candle is not proof of successful follow-through. No post-event path has yet been measured.
4. Snapshots with 1/2/3/4+ tests are descriptive counts, not independent samples; the same market episodes and adjacent snapshots may be dependent.
5. The audit's PASS status validates only programmed structural checks. It does not establish that the separation rule is optimal or that all boundary-test events are correctly classified.
6. Older rejection counts remain unreconciled and are not accepted targets.

## Next required work

Before treating this cohort as frozen, perform a focused event-definition review of the 20% separation state machine, especially whether a qualifying separation close on the same candle as a touch should arm the next test. Then validate event timestamps and causal 1M follow-up mapping. Only after that should the research measure next-15M/1H/4H/12H/24H movement, midpoint/opposite-boundary outcomes, retest timing/depth, and rejection failure/continuation.

**No strategy backtest, fills, fees, slippage, funding, or profitability claims are included.**
