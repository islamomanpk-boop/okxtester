# G0-05 Canonical Source Manifest and Retrieval Status — V1

**Date:** 2026-11-26  
**Branch:** `price-action-v1`  
**Purpose:** Pin all currently identifiable canonical inputs for the G0-05 three-family candidate contract.  
**Status:** Repository-side blob pins recorded; G0-04 workflow artifact extraction and final SHA-256 manifest verification remain pending. No candidate rows generated.

## 1. G0-04 causal breakout artifact (required for continuation and failed-breakout linkage)

- Workflow: [45756061179](https://github.com/islamomanpk-boop/okxtester/actions/runs/45756061179)
- Checked-out source revision: `86b49598d676b6ab00649bf31d4490ffbb1e608f`
- Job: `139694830125`
- Artifact ID: `15087542445`
- Artifact name: `phase3-g0-04-causal-reconstruction-45756061179`
- ZIP SHA-256: `ef6204b546b49880675514ff76b4f6cb86e2821ba2b0d1d5412549927388f0a1`
- Retention expiry recorded by GitHub: 2026-12-10.

The G0-04 reconstruction code emits these required files:
- `input_manifest.csv`
- `historical_baseline_reproduction.csv`
- `context_coverage_and_cross_pipeline_audit.json`
- `causal_thresholds_by_context.csv`
- `unique_raw_crossing_events_with_six_variants.csv`
- `historical_932_identity_reconciliation.csv`
- `raw_crossing_summary.csv`
- `run_metadata.json`

The raw crossing ledger is `unique_raw_crossing_events_with_six_variants.csv`. It is the sole primary source population for breakout continuation; the retrospective 932 selected identities and Module B's 1,592 historical event cohort are reconciliation references only. The artifact ZIP was re-downloaded and independently hashed in this work session; its SHA-256 matches the recorded digest. All seven output-file SHA-256 values below were independently recomputed and match `run_metadata.json`:

| Artifact member | SHA-256 |
|---|---|
| `causal_thresholds_by_context.csv` | `39bc0a66112bdce96282a46ef9caac82765131d0ff36ee9e722497bd5c908b0d` |
| `historical_932_identity_reconciliation.csv` | `137d573e3f817465847b03179409ded4ceb5d884c7ba502e7d9fdf3a95d45ccf` |
| `context_coverage_and_cross_pipeline_audit.json` | `8eaab44b6e5f5523310a01c2a7150741b5d86ed6cff27fbef5b1d279aec7dfa3` |
| `historical_baseline_reproduction.csv` | `cf280aad8961d76eca88ffe3993d6c6ec1a6e024c94986039864d28ae1d77a54` |
| `input_manifest.csv` | `86ef3c95732b9026792f9736ac950983a59a092d71345c62bc7059234873fbd7` |
| `raw_crossing_summary.csv` | `8ad347fbbdf6d66eefd4379b25726e32a1871a95fc4fe20697eb769a921abb4a` |
| `unique_raw_crossing_events_with_six_variants.csv` | `d8c5958f74b4fe4b75b876eb057642a2dae56167c7fc616764d170983901df20` |

Direct artifact checks:
- ZIP digest matches: PASS.
- Raw crossing ledger: 2,861 rows and 2,861 unique full-grain keys.
- Historical selected identities in raw ledger: 932.
- Historical baseline: 20/20 passed.
- Historical reconciliation: 120 rows, zero raw-source mismatches.
- Threshold table: 65,310 rows; 21,770 per policy; P25 <= P40 in every row; prior-context count minimum 180.
- Six policy/population variants reproduce the recorded event totals exactly.

## 2. Rejection family inputs

Git blob IDs are pinned by the accepted V1.1 rejection lifecycle implementation's `EXPECTED_BLOBS` and re-confirmed against the current `price-action-v1` tree.

| Input | Git blob SHA-1 |
|---|---|
| `reports/sideways_boundary_events_historical_v1/boundary_tests_historical_v1.csv` | `2af6f85cd60194019f903a17f16216841ae61f8c` |
| `reports/sideways_phase3_research_archive_v1/episode_retest_anatomy_v1/event_anatomy_v1.csv` | `c58de65ec1936607790c2ee40b828897e6f726dc` |
| `reports/sideways_detector_original_v1/BTC_features_original_v1.csv` | `e422073b993cf5d9d11050216509165277339710` |
| `reports/sideways_detector_original_v1/ETH_features_original_v1.csv` | `c38641d3846931afd6e44a7f39318251fe3c5653` |
| `reports/sideways_detector_original_v1/SOL_features_original_v1.csv` | `5ba90a99a33924f3de6bcbe9cd1d76aa0a9dd207` |
| `reports/sideways_detector_original_v1/DOGE_features_original_v1.csv` | `5fb8cb621628e069b1e2500f8047eb908b031909` |
| `reports/sideways_detector_original_v1/AVAX_features_original_v1.csv` | `06b6f7ee947ef5e62b8cf2b9cc64fb7caaa523e5` |

Accepted source expectations from `research/phase3_rejection_lifecycle_v1_1.py`:
- boundary ledger: 2,452 rows;
- accepted event-anatomy ledger: 1,992 rows;
- nested cohorts: 1,154 broad and 838 strict;
- eligible event identity: asset + definition + direction + snapshot index + segment ID + test rank + test-start timestamp;
- rejection confirmation: first strong rejection 15-minute candle open + 900,000 ms;
- existing 10%-of-channel retest band and 20%-of-channel inward-separation rule are descriptive lifecycle geometry, not G0-05 execution rules.

The 40 broad / 29 strict snapshot-expiry cases remain source records with explicit exclusion disposition. The read-only source-audit workflow calculated these SHA-256 values from the exact checked-out bytes:

| Input | SHA-256 |
|---|---|
| `boundary_tests_historical_v1.csv` | `a58060c7699e8c7be27b0551ec6fd88bf6a97eb0a943e2228f62b981fab7019b` |
| `event_anatomy_v1.csv` | `d808f3f93848bd9063b368ca7435798c7b06fb2c6144192b7bf8bbe854392261` |
| `BTC_features_original_v1.csv` | `c8c3bbb2e3942eb22dc78fae8f310ce8dd9963f58b3865500ea8225bc55c395f` |
| `ETH_features_original_v1.csv` | `88a0131775977bf30c914be5118c7998dd1570f1b42340a4201477b5388bfb44` |
| `SOL_features_original_v1.csv` | `d8766f8071d48c77fa7bd7dbe5b5f8f787b886f0ba74d06238b27b1e6f409228` |
| `DOGE_features_original_v1.csv` | `f8b4e60a0feb1784521694ffd7008ca8a7b806c260b9cc3f8c8ee020f6c2d05f` |
| `AVAX_features_original_v1.csv` | `d5394e5fce3a642a452a854101c6b60a7012e2a257a13867bfe2cd74f7bc87cf` |

All seven Git blob pins and the above SHA-256 values passed the G0-05 read-only source-audit workflow.

## 3. Canonical 1-minute market data

The five 1-minute files have both Git blob pins and the SHA-256 hashes verified in G0-04 raw-source audit and embedded in the G0-04 reconstruction source.

| Asset | Git blob SHA-1 | SHA-256 | Rows |
|---|---|---|---:|
| BTC | `639f7b8a6d54747dd3eb3370dc133d53f6382bfd` | `3afab3d60387c87fc4b96f54911538fea6bbb7682b2e18001537bc4359da6633` | 569,125 |
| ETH | `3017d870fe1cb764e1acb8fdec04138592749d69` | `8a2924bcb23bd5963cd1c46b8871475ff7ff4a3c8d8bed6325dbd406ec0552d2` | 569,125 |
| SOL | `a850c2dc4a2c14b34b59737ccfbb2e4c59d97bf3` | `8ed0a2efade22a11aa50f4511cdab3d32f438759f7acd7819ccbe41ab92ac0b3` | 569,126 |
| DOGE | `2162df0f277bef6c04bd191b459a35d735c68f2d` | `eabf087b1a782d316fa1560b10fc4ee7adfc0adb426ef3d1158dc18c248c40f4` | 569,126 |
| AVAX | `6e0cb0c55aa2aafb4118d62522826bcf1a2aeb62` | `44ac7db951247a374aecba845336517b82b2655489920d62ec70f9b02fccdfd5` | 569,127 |

The exact common index is 569,125 timestamps at 60-second cadence. This is inherited verified G0-04 evidence; G0-05 must still assert the source hashes at run time before using the files.

## 4. Failed-breakout descriptive lifecycle inputs

- Event ledger: `reports/phase3_breakout_lifecycle_v1_1/breakout_lifecycle_events_v1_1.csv`
  - Git blob: `da00c6682719864eaee3a491330d57f4d6fd2b39`
  - SHA-256: `d47cc0c480f5175c7c07bc09b3878d00f30e847223df5aee517435bd6216c861`
- Horizon ledger: `reports/phase3_breakout_lifecycle_v1_1/breakout_lifecycle_horizons_v1_1.csv`
  - Git blob: `068e2b90b9824f7c68818c0eb913608db6b8a568`
  - SHA-256: `532e68ecb7b1394457202b8c4cb4c3252ec11a8c1807ad91087e0d0341b06faf`
- Run metadata: `reports/phase3_breakout_lifecycle_v1_1/run_metadata_v1_1.json`
  - Git blob: `72930564f85fc356faa54115c6f76ffc7c533a58`
- Original lifecycle implementation: `research/phase3_breakout_lifecycle_v1_1.py`
  - Git blob: `f272b90344320c884f84b5c13752377f74a5eb99`
- Frozen amendment: `docs/research_checkpoints/2026-11-25_phase3_breakout_lifecycle_v1_1_amendment.md`
- Original recovered breakout source blob: `95d2975947c449f3813d80ee7b12008db14f071f`.

The descriptive lifecycle metadata records 1,592 events (932 broad, 660 strict), 6,368 horizon rows, 6,368 forward cross-check rows, 20/20 original event-count reproduction, 10/10 quantile reproduction, and 1,537 prior-test links with zero link-count mismatches. These are historical source/reconciliation data, not causal candidate counts. The candidate generator must link failed-breakout reversals to a separately eligible G0-05 breakout-continuation candidate.

## 5. Implementation source pins

- G0-04 causal reconstruction source: `research/phase3_g0_04_causal_breakout_reconstruction_v1.py`, current Git blob `bd09db658dcb4522419a98006cddbaf7d08b8c01`.
- Rejection lifecycle V1.1 source: `research/phase3_rejection_lifecycle_v1_1.py`, current Git blob `e47c9d60f3af019f84ccb82699d990e5a34e9709`.
- Breakout lifecycle V1.1 source: `research/phase3_breakout_lifecycle_v1_1.py`, current Git blob `f272b90344320c884f84b5c13752377f74a5eb99`.

## 6. Provenance and causal source-audit status

All source-manifest and source-only causal-threshold checks listed above have passed in workflow [45782827341](https://github.com/islamomanpk-boop/okxtester/actions/runs/45782827341). The latest report verifies the seven rejection-family Git blob/SHA-256 pairs, Module B event/horizon hashes, 15,594 G0-04 event/threshold recomputations, 262 explicit breakout warm-up exclusions, and the 1,154 unique physical rejection dispositions.

**Remaining G0-05 work is now the row-level source-disposition dry-run, exact first-eligible-minute checks, and full source disposition accounting. No canonical candidate generation is authorized yet.**


## 7. G0-05 source-audit execution evidence

- Workflow: [45782267493](https://github.com/islamomanpk-boop/okxtester/actions/runs/45782267493)
- Job: `139780414670` — SUCCESS.
- Checked-out revision: `123cc54093b7b3a3fbac2351a437664e7edb2a23`.
- Artifact: [phase3-g0-05-source-audit-45782267493](https://github.com/islamomanpk-boop/okxtester/actions/runs/45782267493/artifacts/15097814699).
- Artifact ZIP SHA-256: `9d1522dfaceab459d12e5011275455eaae008eea4fb8d4f3d96b9d66225714e3`.
- The artifact was downloaded and its ZIP SHA-256 independently verified.
- Source audit status: `G0_05_SOURCE_PROVENANCE_AND_IDENTITY_AUDIT_PASS`.
- Rejection family: 2,452 boundary rows; 1,992 confirmed source events; one-to-one anatomy join passed; 1,154 broad / 838 strict; 40 broad / 29 strict confirmation-at-snapshot-endpoint exclusions.
- Module B: 1,592 event rows; 6,368 horizon rows; 932 distinct source identities; all 932 matched the G0-04 raw crossing ledger; zero unmatched identities.
- G0-04 artifact: 2,861 raw crossing rows; 20/20 historical baseline; zero raw-source mismatches; 65,310 threshold rows; all six policy/population totals verified.

The audit is read-only. It generated provenance/reconciliation reports only; it did not generate canonical candidate rows, orders, fills or outcomes.


## 8. Causal source-only rejection disposition and full threshold-join audit — 2026-11-26

Latest read-only source-audit workflow:
- [Run 45782827341](https://github.com/islamomanpk-boop/okxtester/actions/runs/45782827341), job `139782184097` — SUCCESS.
- Checked-out revision: `eb687af43292d06bdbb384caf126993256e8694c`.
- Artifact: [phase3-g0-05-source-audit-45782827341](https://github.com/islamomanpk-boop/okxtester/actions/runs/45782827341/artifacts/15098494434).
- Artifact ZIP SHA-256: `3dad432c4a9c8a81364b93b0a2e0cbd66c70e54716fc2e704536094c2a8f84ea`; independently verified after download.

The latest audit extends the previous source checks:
- **15,594** exact G0-04 event-to-threshold joins and stored-flag recomputations passed (2,599 non-warm-up raw crossings × six policy/population variants).
- **262** raw crossing events had no causal threshold because they preceded the first 180-context calibration point. They are explicitly classified as warm-up, with all six eligibility flags false:
  - BTC 54, ETH 48, SOL 53, DOGE 49, AVAX 58.
- The six stored strict/broad eligibility flags were recomputed from exact snapshot thresholds, channel width, efficiency <= 0.30 and overlap >= 0.70. No mismatch was found.
- Every raw crossing used a context snapshot no later than its signal close; every threshold calibration ended strictly before its classified snapshot.

The 1,154 unique physical rejection events (not 1,992 cohort rows) now have a source-only causal disposition under `EXPANDING_PRIOR + UNIQUE_4H_FEATURE_ROWS`:

| Disposition | Unique physical events |
|---|---:|
| CAUSAL_STRICT_ELIGIBLE | 942 |
| CAUSAL_BROAD_ONLY_ELIGIBLE | 141 |
| CAUSAL_REGIME_NOT_ELIGIBLE | 2 |
| CAUSAL_THRESHOLD_WARMUP | 29 |
| SNAPSHOT_EXPIRED_BEFORE_CONFIRMATION | 40 |
| **Total** | **1,154** |

These are source-only eligibility/disposition counts, not emitted candidates. The audit preserves the 1,992 original definition-specific source rows and 1,992 anatomy rows; strict membership remains nested within broad membership. The 40 snapshot-expired physical events include 29 strict cohort rows and 40 broad cohort rows. No candidate ledger has been generated.

Module B event/horizon file SHA-256 values were also rechecked against its frozen metadata:
- events: `d47cc0c480f5175c7c07bc09b3878d00f30e847223df5aee517435bd6216c861`;
- horizons: `532e68ecb7b1394457202b8c4cb4c3252ec11a8c1807ad91087e0d0341b06faf`.
