## Follow-up source search command

Use this read-only search to locate the earlier pilot runner by its distinctive configuration keys and strategy names, and to find OHLCV/cache download code. It searches source/configuration text only and excludes Git metadata and Python cache directories.

```bash
echo "===== PILOT CONFIG AND STRATEGY SIGNATURES ====="
grep -RInE \
  --include='*.py' \
  --include='*.sh' \
  --include='*.md' \
  --include='*.json' \
  --exclude-dir=.git \
  --exclude-dir=__pycache__ \
  'start_balance_per_strategy_portfolio|ORDER_BLOCK_LIQUIDITY_SWEEP|BB_SQUEEZE_BREAKOUT|Existing cache is preserved|Only 1m candles are tested in this pilot' \
  ~/okx_adaptive_bot ~/okxtester ~/okx_scalp 2>/dev/null | head -n 200

echo
echo "===== OHLCV DOWNLOAD AND CACHE REFERENCES ====="
grep -RInE \
  --include='*.py' \
  --include='*.sh' \
  --include='*.md' \
  --include='*.json' \
  --exclude-dir=.git \
  --exclude-dir=__pycache__ \
  'fetch_ohlcv|load_markets|ohlcv|cache|since|timeframe' \
  ~/okx_adaptive_bot ~/okxtester ~/okx_scalp 2>/dev/null | head -n 220
```

Do not run any discovered scripts.