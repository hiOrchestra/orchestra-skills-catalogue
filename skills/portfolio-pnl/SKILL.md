---
name: portfolio-pnl
version: 0.1.0
description: >-
  Turn an exported history of trades and transfers into current holdings,
  cost basis, and realized and unrealized profit and loss at a stated price
  snapshot — every assumption written down (lot method, fees, transfers
  between own wallets). Use when the user says "what's my P&L", "how much am
  I up/down", "cost basis", "what do I hold", "value my portfolio", "did I
  make money on", or hands you an exchange or wallet export. Not for tax
  filings or tax advice, for live prices alone (coingecko), or for judging
  whether the export is trustworthy first (analyze-data-quality).
metadata:
  openclaw:
    emoji: "🧮"
  orchestra:
    requires:
      skills:
        - coingecko
---
# Portfolio P&L — history → holdings, cost basis, profit and loss, stated

An export of trades is not a P&L until someone decides what a "lot" is, what
to do with fees, and how to treat coins that moved between the person's own
wallets. This skill makes those decisions visible, computes holdings and P&L
from the history, values them at a price snapshot with its time, and reports
the result with the assumptions next to it. It is analysis, not tax advice.

## Related skills
- **analyze-data-quality** — first, on the export: gaps, duplicates, missing
  fees or prices are common and change the answer.
- **coingecko** — the price snapshot for unrealized P&L.
- **build-dashboard** / **build-report** — when they want to look at it again
  or hand it to someone.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- An export (CSV/XLSX) from an exchange, a wallet tool or a chain explorer,
  and a question about what is held or what was made or lost.
- **Do NOT use** to produce a tax report; say the figures are analytical and a
  tax adviser applies the local rules. Do not fill missing prices or fees
  silently.

## Workflow
1. **Read the export and say what it is**: source, period, row count, the
   event types present (buy, sell, deposit, withdrawal, swap, fee, staking
   reward, airdrop), currencies and fee columns. Run `analyze-data-quality`;
   carry its verdict.
2. **Ask the three decisions**, once, and write them down: lot method (FIFO by
   default — say so), fee treatment (added to cost / deducted from proceeds by
   default), and whether transfers between listed wallets are the person's own
   (then they are moves, not sales). Rewards and airdrops: cost basis zero
   unless they say otherwise.
3. **Compute** with `exec` and Python/pandas from the export: lots per asset,
   consumption on sale by the method chosen, realized P&L per sale (proceeds −
   cost − fees), holdings remaining with their cost basis. Keep the script in
   `orch-files` so the next export runs through the same path.
4. **Value holdings** with `coingecko` at one snapshot, time labelled;
   unrealized P&L = value − remaining cost basis.
5. **Reconcile**: computed holdings vs. the balances the person sees on the
   exchange or chain. A mismatch is reported, not hidden — it usually means a
   missing export or an unlisted wallet.
6. **Report** under Output.

## Standards
- Every figure: asset, amount, currency, and the price time for anything
  valued.
- Assumptions (method, fees, transfers, rewards) appear on the report, next
  to the totals, every time.
- Missing data is listed by row and its effect stated ("12 sells without
  fees: realized P&L overstated by up to the fee amount").
- Realized and unrealized are never summed into one "profit" line without
  both parts showing.
- No tax language ("taxable gain", "deductible"): analytical P&L only, and
  say so once.

## Output
- **Snapshot** — date/time of prices, source, export period, data verdict.
- **Assumptions** — the four decisions, one line each.
- **Holdings** — table: asset, amount, cost basis, value now, unrealized P&L, %.
- **Realized P&L** — total and per asset for the period; largest ten sales
  with their lots on request.
- **Reconciliation** — computed vs. reported balances, differences named.
- **Missing or uncertain** — rows and effect.
Saved to `orch-files` as `portfolio/pnl-<date>.md` plus the script and the
holdings CSV.

## Defaults
- Reporting currency: the one the export uses; USD if mixed, converted at the
  snapshot price and labelled.
- Dust (value under 1 unit of the reporting currency) is listed once, not in
  the tables.
- Multiple exports → merge by time, dedupe on transaction id or hash, and say
  how many rows were dropped.
