# Breakout Prior-Test Count Study V1 — Audit and Archive Checkpoint

Date: 2026-11-24
Branch: price-action-v1
Study: `breakout_prior_test_count_study_v1`
Status: Completed descriptive classification run; primary reconciliation checks passed; representative chronology reviewed; independent candle-by-candle OHLC spot audit remains open.

## 1. Purpose and scope

This study classifies original historical breakout events by the number of prior boundary touch tests and confirmed rejection episodes.

It is descriptive classification only. It does not measure post-breakout forward outcomes, profitability, execution quality, or strategy performance.

The original recovered breakout detector and frozen prior-test study specification were not modified.

## 2. Source identity

Original source:

`research/archive/final_timing_corrected_breakout_and_retest_recovered_original_2026-11-22.py`

Expected and verified Git blob SHA:

`95d2975947c449f3813d80ee7b12008db14f071f`

Specification:

`docs/research_checkpoints/2026-11-24_breakout_prior_test_count_study_spec_v1.md`

Implementation:

`research/breakout_test_count/breakout_test_count_study_v1.py`

Tests:

`tests/test_breakout_test_count_study_v1.py`

The implementation's seven unit tests passed in the recorded run-up to this study.

## 3. Reconstruction and data gates

The completed run reported:

- Five primary assets: BTC, ETH, SOL, DOGE, AVAX.
- Common 1-minute timestamps: 569,125.
- Common 1-minute gaps: zero.
- Complete 15-minute bars per asset: 37,941.
- Complete 4-hour bars per asset: 2,370.
- Joined 15-minute gaps per asset: zero.
- Snapshot changes per asset: 2,369.
- Original breakout event counts reproduced: 20/20.
- Original channel-width quantiles reproduced: 10/10.
- Strict event set is a subset of broad event set: true.

All five source-data SHA256 values are preserved in `run_metadata.json` and `reconstruction_audit_v1.csv`.

The metadata field `original_source_git_blob_sha` matches the Git blob SHA independently checked during the audit.

## 4. Output reconciliation

Output row counts:

| Output | Rows |
|---|---:|
| Classifications | 4,776 |
| Group summaries | 240 |
| Prior-test links | 4,534 |
| Original event reproduction | 20 |
| Reconstruction audit | 5 |

The 4,776 classifications consist of 1,592 events for each of the 5%, 10%, and 15% touch-zone variants.

At the primary 10% zone:

| Definition | Direction | 0 rejections | 1 rejection | 2 rejections | 3+ rejections |
|---|---|---:|---:|---:|---:|
| BROAD_P40 | LOWER | 235 | 212 | 12 | 1 |
| BROAD_P40 | UPPER | 260 | 195 | 17 | 0 |
| STRICT_P25 | LOWER | 149 | 149 | 11 | 0 |
| STRICT_P25 | UPPER | 181 | 154 | 16 | 0 |

The zero-rejection category is not synonymous with direct breakout. It includes both:
- Direct events with zero prior touch tests.
- Contact-only events with one or more touch tests and zero confirmed rejections.

The event-level output preserves touch-test, confirmed-rejection, and contact-only counts so these categories can be separated.

## 5. Primary-zone link reconciliation

At the 10% zone:

- Classification events: 1,592.
- Prior-test links: 1,537.
- Sum of event-level prior touch-test counts: 1,537.
- Per-event link-count mismatches: zero.

Link statuses:

- Confirmed rejection: 825.
- Contact-only: 712.

Chronology checks previously performed:

- All 1,537 linked tests started strictly before their breakout event.
- All 825 confirmed rejection timestamps were strictly before their breakout event.
- No rejection timestamp was at or after the breakout event.
- Active-at-end tests are retained as active; they must not be interpreted as having a known end timestamp.

## 6. Representative sequence review

Representative BTC examples were inspected from the 10% zone, STRICT_P25 definition:

- Direct upper breakout on 2025-10-26 09:30 UTC: zero prior touch tests.
- Contact-only upper breakout on 2025-12-22 00:45 UTC: one prior touch test, no confirmed rejection.
- One-rejection upper breakout on 2025-12-22 10:00 UTC.
- Two-rejection upper breakout on 2025-12-22 07:15 UTC.
- One-rejection lower breakout on 2025-11-03 02:30 UTC.
- Two-rejection lower breakout on 2026-07-13 02:00 UTC.

The two-rejection examples contain two distinct test episodes. In the upper example, the first test was separated before the second test began.

These are representative chronology checks, not a complete independent OHLC candle audit.

## 7. Output file hashes

SHA256:

- `breakout_prior_test_classifications_v1.csv`
  `6f85c221fde408878df779d2938ed7432d6067ac2cad45c35ed101ae0cdda4e2`

- `breakout_prior_test_group_counts_v1.csv`
  `a39a7f0371964654679690e44f963784c2c58c744ad774c26b277b99a89ce254`

- `breakout_prior_test_links_v1.csv`
  `0046092afe4d4fcc7280736c5dcb561fea032acab115463ad1d7d9ab261275cc`

- `original_event_reproduction_v1.csv`
  `954736383fa28b7382554bf7ac7235091713e33c43c3b2078f5434de8f0a2267`

- `reconstruction_audit_v1.csv`
  `149002e89ebced2aaab78c0427b12a6544e5cc98276dedf16934e1340140b978`

- `run.log`
  `8ffc9257d47a3090d2ded6c4f34c741e311292572229797f2edb32e2065885e9`

- `run_metadata.json`
  `b9e6f37ed9cd82f5edd7b86c4cc1c92bbac928b767758137ba5289e2de279804`

External run log:

`reports/breakout_prior_test_count_v1_run_2026-11-24.log`

SHA256:

`87d80c66fc93913b6988023590a4b50e8d85a77dde4a6bf5a87e4f1ad7fd49d1`

## 8. Interpretation limits and open audit items

- The study is descriptive; no forward price movement or trading profitability was tested.
- Broad/strict definitions and zone variants overlap and are not independent samples.
- Channel-width quantiles are full-sample retrospective values, not live-calibrated thresholds.
- Volume remains excluded because source units are unverified.
- Representative event sequences were inspected, but independent OHLC spot verification of the underlying touch, rejection, and separation candles remains an open audit item.
- Sparse three-plus rejection groups must not support strong conclusions.
- A zero-rejection group must be split into direct and contact-only before interpreting breakout behaviour.

## 9. Next research stage

The next authorized research stage is the separately frozen forward-outcome study:

`docs/research_checkpoints/2026-11-24_breakout_forward_outcome_study_spec_v1.md`

That study will measure post-entry MFE, MAE, directional close returns, time to extremes, and boundary failures using the specified next-1-minute-open timing convention.

No strategy profitability or live-trading claim is authorized by this checkpoint.
