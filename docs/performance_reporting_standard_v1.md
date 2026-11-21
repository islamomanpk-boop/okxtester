# Performance Reporting and Validation Standard V1

Status: Agreed project requirement
Project: OKX Multi-Regime Price Action Strategy V1
Branch: price-action-v1

## 1. Purpose

Every completed backtest and experiment must produce consistent performance,
risk, cost, exposure, and robustness reporting. A final balance or win rate
alone is never sufficient to judge a strategy.

This standard applies to:
- The 22 baseline exit experiments.
- The 22 trailing-stop experiments.
- The 22 trailing-take-profit experiments.
- All cost-sensitivity scenarios.
- The 1-minute versus 5-minute execution comparison.
- Subsequent out-of-sample validation.

## 2. Trade-level performance metrics

Calculate using net trade PnL after entry fees, exit fees, and funding:

- Trade count.
- Net PnL and gross PnL.
- Total fees and total funding PnL.
- Winning, losing, and breakeven trade counts.
- Win rate and breakeven rate.
- Profit factor.
- Expectancy (average net PnL per closed trade).
- Average winning trade.
- Average losing trade, shown as a positive loss magnitude.
- Payoff ratio (average win divided by average loss).
- Largest winning trade.
- Largest losing trade.
- Maximum consecutive losing trades.
- Average, median, and maximum trade duration.
- Recovery factor.

Definitions:
- Win: net PnL > 0.
- Loss: net PnL < 0.
- Breakeven: net PnL = 0.
- Profit factor: sum of positive net trade PnL divided by the absolute
  sum of negative net trade PnL.
- Expectancy: total net trade PnL divided by closed trade count.
- Recovery factor: portfolio net PnL divided by maximum drawdown amount.
- Undefined ratios must be reported as unavailable, not infinity or zero.

## 3. Portfolio risk and return metrics

Report:
- Initial equity, final equity, net PnL, and total return.
- Maximum intraday mark-to-market drawdown, in dollars and percent.
- Recovery factor.
- Sharpe ratio.
- Sortino ratio.
- Annualized return (CAGR).
- Calmar ratio.
- Daily portfolio returns.
- Worst daily loss in dollars and percent.
- UTC date of the worst daily loss.

Calculation conventions:
- Portfolio equity includes realized PnL, unrealized mark-to-market PnL,
  fees, and funding.
- Daily equity is sampled at UTC day boundaries using the latest available
  portfolio mark for that day. The final partial UTC day is included.
- Daily Sharpe uses arithmetic daily returns, zero risk-free rate, population
  standard deviation, and sqrt(365) annualization.
- Daily Sortino uses a zero daily target return and downside deviation
  calculated across all daily observations.
- CAGR uses elapsed calendar time and 365 days per year.
- Calmar is CAGR divided by maximum intraday drawdown fraction.
- Ratios are unavailable where their denominator or required observations
  make them undefined.
- Maximum drawdown remains intraday; daily sampling must not replace it.

## 4. Exposure and portfolio utilization

Report:
- Maximum simultaneous open positions.
- Average capital utilization.
- Maximum capital utilization.
- Maximum gross exposure in quote currency.
- Maximum gross exposure as a multiple of portfolio equity.

Capital utilization is gross open exposure divided by positive marked equity.
Calculate average utilization over the synchronized execution-minute
observations, including observations with no open positions.

## 5. Required breakdowns

Produce the same applicable trade metrics for:
- Entire portfolio.
- Each asset: BTC, ETH, SOL, DOGE, AVAX.
- LONG trades versus SHORT trades.
- Each asset and direction combination.

Breakdowns must include trade count, net PnL, gross PnL, fees, funding,
win rate, profit factor, expectancy, average win/loss, and payoff ratio.

Do not hide losing assets or directions in aggregate results.

## 6. Monthly performance

Produce a UTC calendar-month table containing:
- Month.
- Starting equity.
- Ending equity.
- Net PnL.
- Return percentage.

Use the previous month's ending equity as the next month's starting equity.
Use the initial equity for the first observed month. Include partial first
and final months and label them as partial where applicable.

## 7. Costs and execution assumptions

Every report must disclose:
- Taker fee rate per side.
- Slippage assumption per side in basis points.
- Funding data and funding treatment.
- Execution timeframe.
- Whether equity curve storage was full or summary-only.

Fees and funding must be shown separately. Net PnL must include both.
Slippage is reflected in simulated fills; do not claim an independently
measured slippage-cost total unless raw reference prices are available.

Cost sensitivity must preserve the same signals, date window, exit rules,
risk fraction, and portfolio constraints. Cost changes may alter sizing,
fills, accepted entries, and outcomes because sizing is cost-aware. Reports
must disclose this; scenarios are not fixed-quantity comparisons.

## 8. Exit and forced-close reporting

Break down trades by exit reason, including stops, stop gaps, targets,
target gaps, trailing exits, and end-of-data exits where present.

End-of-data closures must be identified separately as forced simulation
closures, not ordinary strategy exits.

The current simulator does not model exchange liquidation. Reports must
explicitly state that liquidation events, maintenance-margin rules, and
exchange liquidation fees are not simulated. Never report a zero liquidation
count as proof that liquidation risk is absent.

## 9. Robustness and validation

Required before selecting a preferred configuration:
1. Run all cost-sensitivity scenarios.
2. Compare all 66 exit configurations without selecting solely on return.
3. Inspect per-asset and long/short consistency.
4. Inspect monthly and time-period consistency.
5. Compare 1-minute and 5-minute execution with equivalent assumptions.
6. Perform chronological out-of-sample validation.
7. Use paper trading before considering live deployment.

The 66 configurations create multiple-comparison and selection-bias risk.
Do not treat the best historical result as proof of a predictive edge.
Keep a holdout period separate from configuration selection.

## 10. Reporting files

For each experiment or scenario, save:
- Main summary CSV.
- Combined closed-trades CSV.
- Overall metrics report.
- Per-asset metrics CSV.
- Per-direction metrics CSV.
- Asset-and-direction metrics CSV.
- Monthly returns CSV.
- Exit-reason breakdown.
- Human-readable Markdown report.

A comparison CSV must summarize all scenarios in a batch.

Keep raw market data, raw funding files, credentials, API keys, and other
secrets out of Git history. Commit compact reports and project code only.

## 11. Quality gates

Before a reporting or experiment change is committed:
- Add unit tests for metric definitions and edge cases.
- Test empty trade sets and undefined ratios.
- Test profitable, losing, and breakeven trades.
- Test long and short breakdowns.
- Test daily and monthly boundary handling.
- Test consistency between full equity-curve and summary-only modes.
- Run the complete unit test suite.
- Run git diff --check.
- Review generated reports for missing or misleading values.

Do not start the next major experiment batch until the current task passes,
is documented, committed, pushed to price-action-v1, and independently
verified on GitHub.

## 12. Interpretation rules

- Never rank configurations on net return alone.
- Consider drawdown, profit factor, expectancy, exposure, and consistency.
- Separate gross trading performance from fees and funding.
- Clearly distinguish measured results from assumptions and estimates.
- Do not call a strategy profitable or robust based on one backtest.
- Preserve losing results and failed experiments; do not cherry-pick reports.
