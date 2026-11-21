# Price Action V1 — Signal Quality and Distribution Audit

Purpose: descriptive analysis of signal frequency and overlap.

This report does not measure trade profitability or predict future returns.
Pivot confirmations are structural events, not entry signals.

## 1. Asset summary

| Asset | Rows | Candles with signals | Total signal events | Multi-signal candles | Max signals on one candle | Pivot-event candles |
|---|---:|---:|---:|---:|---:|---:|
| BTC | 37,941 | 26,627 | 39,180 | 10,633 | 4 | 7,398 |
| ETH | 37,941 | 25,857 | 37,943 | 10,137 | 5 | 7,586 |
| SOL | 37,941 | 27,005 | 39,416 | 10,523 | 4 | 7,125 |
| DOGE | 37,941 | 27,607 | 41,093 | 11,436 | 4 | 7,142 |
| AVAX | 37,941 | 27,692 | 41,447 | 11,692 | 4 | 7,087 |

## 2. Signal counts by asset

| Asset | bullish_engulfing | bearish_engulfing | bullish_pinbar | bearish_pinbar | support_rejection | resistance_rejection | bullish_ob_created | bearish_ob_created | bullish_ob_first_retest | bearish_ob_first_retest |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 3,730 | 3,526 | 1,270 | 1,319 | 13,659 | 14,149 | 579 | 647 | 136 | 165 |
| ETH | 3,712 | 3,563 | 1,198 | 1,182 | 13,284 | 13,514 | 591 | 613 | 145 | 141 |
| SOL | 3,536 | 3,611 | 1,164 | 1,197 | 13,912 | 14,634 | 522 | 579 | 116 | 145 |
| DOGE | 3,589 | 3,578 | 1,187 | 1,185 | 14,832 | 15,279 | 556 | 584 | 157 | 146 |
| AVAX | 3,505 | 3,448 | 1,247 | 1,329 | 14,745 | 15,655 | 605 | 615 | 154 | 144 |

## 3. Pivot confirmations by asset

| Asset | Confirmed pivot highs | Confirmed pivot lows |
|---|---:|---:|
| BTC | 3,699 | 3,755 |
| ETH | 3,805 | 3,841 |
| SOL | 3,560 | 3,610 |
| DOGE | 3,549 | 3,640 |
| AVAX | 3,524 | 3,614 |

## 4. Signal counts by market regime

Counts below are event counts, not unique candles.

### BULLISH

| Asset | bullish_engulfing | bearish_engulfing | bullish_pinbar | bearish_pinbar | support_rejection | resistance_rejection | bullish_ob_created | bearish_ob_created | bullish_ob_first_retest | bearish_ob_first_retest |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 292 | 263 | 111 | 144 | 1,057 | 1,294 | 50 | 46 | 10 | 12 |
| ETH | 183 | 153 | 60 | 64 | 584 | 634 | 25 | 24 | 11 | 8 |
| SOL | 206 | 204 | 57 | 89 | 755 | 834 | 34 | 36 | 10 | 6 |
| DOGE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| AVAX | 83 | 84 | 25 | 38 | 463 | 478 | 15 | 18 | 4 | 3 |

### BEARISH

| Asset | bullish_engulfing | bearish_engulfing | bullish_pinbar | bearish_pinbar | support_rejection | resistance_rejection | bullish_ob_created | bearish_ob_created | bullish_ob_first_retest | bearish_ob_first_retest |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 498 | 464 | 166 | 184 | 1,485 | 1,696 | 86 | 84 | 11 | 24 |
| ETH | 458 | 479 | 157 | 143 | 1,672 | 1,734 | 65 | 77 | 10 | 18 |
| SOL | 437 | 408 | 150 | 143 | 1,594 | 1,692 | 62 | 62 | 8 | 17 |
| DOGE | 828 | 851 | 326 | 324 | 3,289 | 3,573 | 118 | 148 | 26 | 37 |
| AVAX | 365 | 359 | 175 | 154 | 1,628 | 1,524 | 69 | 60 | 15 | 13 |

### SIDEWAYS

| Asset | bullish_engulfing | bearish_engulfing | bullish_pinbar | bearish_pinbar | support_rejection | resistance_rejection | bullish_ob_created | bearish_ob_created | bullish_ob_first_retest | bearish_ob_first_retest |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 373 | 359 | 150 | 105 | 1,340 | 1,546 | 62 | 69 | 12 | 18 |
| ETH | 575 | 543 | 214 | 205 | 1,883 | 2,071 | 129 | 86 | 33 | 22 |
| SOL | 370 | 399 | 156 | 147 | 1,586 | 1,892 | 58 | 72 | 14 | 18 |
| DOGE | 472 | 487 | 187 | 172 | 2,359 | 2,388 | 64 | 90 | 24 | 23 |
| AVAX | 717 | 741 | 305 | 308 | 3,530 | 3,777 | 112 | 138 | 27 | 32 |

### TRANSITION

| Asset | bullish_engulfing | bearish_engulfing | bullish_pinbar | bearish_pinbar | support_rejection | resistance_rejection | bullish_ob_created | bearish_ob_created | bullish_ob_first_retest | bearish_ob_first_retest |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 678 | 629 | 253 | 255 | 2,703 | 2,790 | 105 | 111 | 28 | 25 |
| ETH | 588 | 581 | 193 | 213 | 2,195 | 2,411 | 85 | 99 | 22 | 17 |
| SOL | 701 | 738 | 259 | 272 | 2,866 | 3,071 | 96 | 107 | 19 | 30 |
| DOGE | 396 | 406 | 147 | 121 | 2,028 | 2,021 | 58 | 57 | 12 | 16 |
| AVAX | 432 | 442 | 150 | 195 | 2,068 | 2,331 | 68 | 73 | 14 | 15 |

### WARMUP

| Asset | bullish_engulfing | bearish_engulfing | bullish_pinbar | bearish_pinbar | support_rejection | resistance_rejection | bullish_ob_created | bearish_ob_created | bullish_ob_first_retest | bearish_ob_first_retest |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 1,887 | 1,808 | 589 | 630 | 7,074 | 6,823 | 276 | 337 | 75 | 86 |
| ETH | 1,903 | 1,803 | 574 | 557 | 6,950 | 6,664 | 287 | 327 | 69 | 76 |
| SOL | 1,815 | 1,859 | 541 | 545 | 7,111 | 7,145 | 272 | 302 | 65 | 74 |
| DOGE | 1,891 | 1,830 | 527 | 568 | 7,156 | 7,297 | 316 | 289 | 95 | 70 |
| AVAX | 1,906 | 1,818 | 591 | 634 | 7,056 | 7,545 | 341 | 326 | 94 | 81 |

### NO_REGIME_AVAILABLE

| Asset | bullish_engulfing | bearish_engulfing | bullish_pinbar | bearish_pinbar | support_rejection | resistance_rejection | bullish_ob_created | bearish_ob_created | bullish_ob_first_retest | bearish_ob_first_retest |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 2 | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| ETH | 5 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| SOL | 7 | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| DOGE | 2 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| AVAX | 2 | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## 5. Signal overlap

| Asset | No signals | Exactly 1 | Exactly 2 | 3 or more |
|---|---:|---:|---:|---:|
| BTC | 11,314 | 15,994 | 8,846 | 1,787 |
| ETH | 12,084 | 15,720 | 8,341 | 1,796 |
| SOL | 10,936 | 16,482 | 8,752 | 1,771 |
| DOGE | 10,334 | 16,171 | 9,501 | 1,935 |
| AVAX | 10,249 | 16,000 | 9,752 | 1,940 |

## 6. Regime candle coverage

| Asset | BULLISH | BEARISH | SIDEWAYS | TRANSITION | WARMUP | NO_REGIME_AVAILABLE |
|---|---:|---:|---:|---:|---:|---:|
| BTC | 2,976 | 4,938 | 3,920 | 6,848 | 19,232 | 27 |
| ETH | 1,792 | 4,682 | 6,096 | 6,112 | 19,232 | 27 |
| SOL | 2,272 | 4,602 | 4,352 | 7,456 | 19,232 | 27 |
| DOGE | 0 | 9,066 | 5,344 | 4,272 | 19,232 | 27 |
| AVAX | 1,008 | 4,154 | 8,400 | 5,120 | 19,232 | 27 |

## Interpretation and limitations

- High signal frequency does not imply profitability.
- Multiple signals on one candle are counted separately as events.
- Multi-signal candle counts identify overlap, not independent opportunities.
- Regime counts depend on the available historical regime labels.
- WARMUP and NO_REGIME_AVAILABLE observations are reported separately.
- This audit does not evaluate entries, stops, targets, fees, slippage, or funding.
- No strategy selection or parameter optimization is performed.

The five input CSVs remain local and are not committed to Git.
