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

The raw crossing ledger is `unique_raw_crossing_events_with_six_variants.csv`. It is the sole primary source population for breakout continuation; the retrospective 932 selected identities and Module B's 1,592 historical event cohort are reconciliation references only. The artifact ZIP hash is known, but the individual file SHA-256 values and artifact contents have not yet been re-extracted in this G0-05 work session. Do not proceed to canonical joins until the exact artifact members and their internal hashes are independently verified.

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

The 40 broad / 29 strict snapshot-expiry cases remain source records with explicit exclusion disposition. The source blob IDs are verified; SHA-256 for the two event CSVs and five feature CSVs must be calculated in the final source-manifest run before canonical generation.

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
- Horizon ledger: `reports/phase3_breakout_lifecycle_v1_1/breakout_lifecycle_horizons_v1_1.csv`
  - Git blob: `068e2b90b9824f7c68818c0eb913608db6b8a568`
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

## 6. Remaining provenance blockers

1. Re-extract G0-04 artifact 15087542445 and verify all expected member paths, file sizes, per-file SHA-256 values and the metadata's code revision.
2. Verify the exact six-variant raw-crossing ledger schema, unique key grain, row count, threshold joins and all 20/20 baseline evidence directly from the artifact.
3. Calculate SHA-256 for rejection boundary, event-anatomy and five detector-feature CSVs; compare with a frozen manifest.
4. Calculate SHA-256 for Module B event and horizon CSVs and compare with their run metadata output hashes.
5. Validate one-to-one/one-to-many source joins and explicit disposition coverage before any candidate row is emitted.

**No canonical candidate generation is authorized until these blockers are closed.**
