# G0-05 Overlap and Canonical Mapping Validation Follow-up — V1

**Date:** 2026-11-26  
**Branch:** `price-action-v1`  
**Scope:** Source-only overlap-cluster verification and non-materializing review of canonical field mapping.  
**Status:** Overlap metadata validated in source-only ledgers; canonical serializer remains synthetic-only and has not been run on real rows.

## 1. Frozen overlap conventions checked

- **Rejection:** Reuse accepted Module A V1.1 24-hour interval-graph clusters. Windows begin at completed rejection confirmation; cluster IDs and bounds remain those of the accepted lifecycle output. Physical cluster sizes are recounted after strict/broad cohort collapse so duplicate cohort rows do not inflate the 1,154-event physical population.
- **Breakout continuation:** Apply the Module B V1.1 12-hour interval-graph convention to all 2,861 unique raw crossings, not only the 932 historical Module B source events. Windows begin at exact signal availability, use contiguous observed 1-minute bars capped at 720, and are half-open. Touching windows are separate; transitive overlaps remain connected.
- **Failed-breakout reversal:** Inherit the exact overlap-cluster metadata of the linked source breakout. Failed-breakout rows are a subset of source breakout events and are not counted as additional clusters.
- Clusters are dependence metadata only. No source event is removed, merged, or re-labelled.

## 2. Latest source-audit evidence

- Source-audit workflow: [45811346908](https://github.com/islamomanpk-boop/okxtester/actions/runs/45811346908) — SUCCESS.
- Source-audit code revision: `262915859efe042e14818fe7ce9d46235b19da11`.
- Artifact ID: `15113661075`.
- Artifact ZIP SHA-256: `994816fd3b25b50096f1ab4a385b7e1907a7f3feb93938c037f9cff7ff707f07` (recomputed after download).
- Source manifest ID: `b20ba1b40688c49199649e3b887c3ec828cd30056967f8d1f80fea94c3da2002`.
- The artifact contains 1,154 rejection, 2,861 breakout, and 932 failed-breakout physical source rows (4,947 total).

### 2.1 Cluster counts

| Family source population | Clusters | Largest physical cluster | Clusters by asset |
|---|---:|---:|---|
| Rejection (1,154 physical events; 24H) | 380 | 16 | AVAX 76; BTC 76; DOGE 71; ETH 79; SOL 78 |
| Breakout (2,861 raw crossings; 12H) | 1,037 | 14 | AVAX 211; BTC 220; DOGE 193; ETH 201; SOL 212 |
| Failed breakout (932 linked events) | Inherits source breakout IDs | Inherited | Not an additional cluster population |

Rejection cluster-size distribution (size: number of clusters): 1:120, 2:86, 3:53, 4:47, 5:26, 6:18, 7:7, 8:6, 9:6, 10:5, 11:3, 12:1, 15:1, 16:1.

Breakout cluster-size distribution: 1:382, 2:220, 3:145, 4:110, 5:68, 6:48, 7:25, 8:19, 9:7, 10:6, 11:2, 12:2, 13:2, 14:1.

### 2.2 Independent artifact checks

After downloading the source-audit ZIP, the archive digest and all five member SHA-256 values were recomputed. Row-level checks confirmed:
- unique source identities in each family ledger;
- rejection and breakout cluster sizes equal the physical rows assigned to each cluster;
- failed-breakout cluster ID, size, start/end bounds, and repeated-signal group exactly match the linked breakout source row (zero mismatches);
- dispositions reconcile to rejection 1,083 eligible / 31 rejected / 40 expired; breakout 1,038 eligible / 1,823 rejected; failed breakout 736 eligible / 30 rejected / 166 expired.

## 3. Test and exact-minute evidence

- Candidate/source contract synthetic workflow: [45811248864](https://github.com/islamomanpk-boop/okxtester/actions/runs/45811248864) — SUCCESS, **126/126 tests passed**. Includes interval-graph transitive/half-open behavior, deterministic order, exact observed-minute window starts, cohort cluster consistency, and canonical serializer synthetic-ledger tests.
- Independent exact-minute verifier: [45811488064](https://github.com/islamomanpk-boop/okxtester/actions/runs/45811488064) — SUCCESS.
- Independent artifact ID: `15112647566`; ZIP SHA-256: `6835f98f8992e4413c8a12d2c10fb7bdd9aaddeb261d8a1754a0a2a4d3d3191a` (recomputed after download).
- Independent verifier status: `INDEPENDENT_EXACT_MINUTE_MEMBERSHIP_PASS`; all five frozen raw 1-minute hashes and grids passed, and all 2,857 eligible timestamps were verified as exact minute opens. All 2,090 non-eligible rows had blank first-eligible timestamps.
- The verifier explicitly states that its scope is exact-minute membership, **not G0-05 gate approval**.

## 4. Canonical field-mapping status

The shared contract currently declares 60 required canonical fields and provides a row validator, ledger validator, deterministic identity helper, and serializer. The 126-test synthetic suite exercises the serializer against synthetic source ledgers.

A separate non-materializing review of the downloaded 4,947 source-only rows checked the serializer's source inputs, required lineage/provenance fields, timestamp availability, snapshot interval validity, cluster metadata, disposition/reason/censor semantics, and failed-breakout source-link/expiry presence. No field-presence or basic value-contract issue was found in that review. This was a reviewer-side inspection, not a new CI workflow or a canonical ledger validation.

**Important boundary:** The serializer has not been executed on these real source rows. No canonical candidate/disposition rows have been created, no real-row candidate IDs have been materialized or collision-checked, and no candidate-generation authorization is implied.

## 5. Next safe work

1. Convert the non-materializing field-mapping review into explicit automated mapping-coverage checks for each family, without invoking the serializer on real rows.
2. Finish family-specific nullability and confirmation/ambiguity mapping checks, especially unresolved failed-breakout events.
3. Independently review the exact failed-breakout-to-source-breakout identity and 12-hour expiry relationship at the mapping-contract level.
4. Keep G0-05 OPEN until the remaining evidence and gate criteria are independently satisfied.

No orders, fills, positions, execution simulation, PnL, strategy backtests, or phase transition were produced or authorized.
