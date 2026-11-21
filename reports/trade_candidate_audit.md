# Trade Candidate Engine V1 — Five-Asset Audit

Sequential audit of the five 15-minute price-action datasets.

## BTC

- Dataset rows: 37,941
- Candidates: 3,554
- LONG: 1,515
- SHORT: 2,039
- Priority 1: 178
- Priority 2: 316
- Priority 3: 3,060
- Processing seconds: 4.398

### Validation

- PASS — No duplicate signal timestamps
- PASS — Availability exactly +15 minutes
- PASS — Finite stop references
- PASS — Positive finite ATR stop distances
- PASS — Correct asset labels
- PASS — Valid priorities
- PASS — Valid trade directions
- PASS — Correct strategy family

### Signal types

- resistance_rejection: 1,715
- support_rejection: 1,309
- bearish_engulfing_at_resistance: 129
- bullish_engulfing_at_support: 116
- bearish_engulfing: 95
- bearish_pinbar_at_resistance: 39
- bearish_pinbar: 35
- bullish_engulfing: 35
- bullish_pinbar_at_support: 32
- bearish_ob_first_retest: 26
- bullish_pinbar: 13
- bullish_ob_first_retest: 10

## ETH

- Dataset rows: 37,941
- Candidates: 3,199
- LONG: 1,483
- SHORT: 1,716
- Priority 1: 154
- Priority 2: 374
- Priority 3: 2,671
- Processing seconds: 3.508

### Validation

- PASS — No duplicate signal timestamps
- PASS — Availability exactly +15 minutes
- PASS — Finite stop references
- PASS — Positive finite ATR stop distances
- PASS — Correct asset labels
- PASS — Valid priorities
- PASS — Valid trade directions
- PASS — Correct strategy family

### Signal types

- resistance_rejection: 1,364
- support_rejection: 1,272
- bearish_engulfing_at_resistance: 142
- bullish_engulfing_at_support: 140
- bearish_engulfing: 107
- bearish_pinbar_at_resistance: 54
- bullish_pinbar_at_support: 38
- bearish_pinbar: 31
- bearish_ob_first_retest: 18
- bullish_ob_first_retest: 17
- bullish_engulfing: 12
- bullish_pinbar: 4

## SOL

- Dataset rows: 37,941
- Candidates: 4,108
- LONG: 1,859
- SHORT: 2,249
- Priority 1: 169
- Priority 2: 345
- Priority 3: 3,594
- Processing seconds: 3.639

### Validation

- PASS — No duplicate signal timestamps
- PASS — Availability exactly +15 minutes
- PASS — Finite stop references
- PASS — Positive finite ATR stop distances
- PASS — Correct asset labels
- PASS — Valid priorities
- PASS — Valid trade directions
- PASS — Correct strategy family

### Signal types

- resistance_rejection: 1,900
- support_rejection: 1,654
- bearish_engulfing_at_resistance: 132
- bullish_engulfing_at_support: 129
- bearish_engulfing: 110
- bearish_pinbar_at_resistance: 50
- bearish_pinbar: 34
- bullish_pinbar_at_support: 34
- bearish_ob_first_retest: 23
- bullish_engulfing: 20
- bullish_ob_first_retest: 17
- bullish_pinbar: 5

## DOGE

- Dataset rows: 37,941
- Candidates: 4,023
- LONG: 1,046
- SHORT: 2,977
- Priority 1: 230
- Priority 2: 292
- Priority 3: 3,501
- Processing seconds: 4.040

### Validation

- PASS — No duplicate signal timestamps
- PASS — Availability exactly +15 minutes
- PASS — Finite stop references
- PASS — Positive finite ATR stop distances
- PASS — Correct asset labels
- PASS — Valid priorities
- PASS — Valid trade directions
- PASS — Correct strategy family

### Signal types

- resistance_rejection: 2,512
- support_rejection: 948
- bearish_engulfing: 175
- bearish_engulfing_at_resistance: 173
- bullish_engulfing_at_support: 57
- bearish_pinbar: 45
- bearish_pinbar_at_resistance: 43
- bearish_ob_first_retest: 29
- bullish_pinbar_at_support: 19
- bullish_ob_first_retest: 12
- bullish_engulfing: 9
- bullish_pinbar: 1

## AVAX

- Dataset rows: 37,941
- Candidates: 3,061
- LONG: 897
- SHORT: 2,164
- Priority 1: 104
- Priority 2: 224
- Priority 3: 2,733
- Processing seconds: 4.020

### Validation

- PASS — No duplicate signal timestamps
- PASS — Availability exactly +15 minutes
- PASS — Finite stop references
- PASS — Positive finite ATR stop distances
- PASS — Correct asset labels
- PASS — Valid priorities
- PASS — Valid trade directions
- PASS — Correct strategy family

### Signal types

- resistance_rejection: 1,884
- support_rejection: 822
- bearish_engulfing_at_resistance: 122
- bearish_engulfing: 81
- bullish_engulfing_at_support: 51
- bearish_pinbar_at_resistance: 38
- bearish_ob_first_retest: 20
- bearish_pinbar: 19
- bullish_pinbar_at_support: 13
- bullish_ob_first_retest: 7
- bullish_engulfing: 4

## Combined results

- Assets audited: 5
- Total dataset rows: 189,705
- Total candidates: 17,945
- Overall validation: PASS

