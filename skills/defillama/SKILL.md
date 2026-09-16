---
name: defillama
version: 0.1.0
description: >-
  Protocol and chain fundamentals from DefiLlama's free public API — TVL by
  protocol and by chain with history, protocol fees and revenue, stablecoin
  supply, yield pools, and token prices — no API key. Use when the user asks
  about TVL, "how big is protocol X", "which chains are growing", "fees and
  revenue of", "stablecoin supply", "yields on", "is this protocol losing
  users", or wants fundamentals rather than a price. Not for live prices and
  market caps (coingecko) or wallet-level on-chain data (etherscan).
metadata:
  openclaw:
    emoji: "🦙"
---
# DefiLlama — protocol and chain fundamentals, no key needed

DefiLlama aggregates on-chain fundamentals: how much value a protocol or chain
holds (TVL), what protocols earn (fees, revenue), stablecoin supply and yield
pools. It is public, rate-limited but generous, and needs no key. Call it with
`exec curl`. Every figure you report carries the timestamp DefiLlama gives it
and the word "DefiLlama" — it is an aggregator, and its methodology per
protocol is visible on the protocol page.

## Related skills
- **coingecko** — live price, 24h change, market cap.
- **etherscan** — one address, one contract, one transaction.
- **token-due-diligence** — uses TVL, fees and age from here as part of a verdict.
(If a referenced skill is not installed, do the equivalent inline.)

## Endpoints (base `https://api.llama.fi` unless noted)

**Find a protocol slug** — names are not ids:
```bash
exec curl -s "https://api.llama.fi/protocols" | jq -r '.[] | select(.name|test("aave";"i")) | "\(.slug) \(.name) \(.category) tvl=\(.tvl)"'
```

**Protocol TVL, current and history** (per chain, with token breakdown):
```bash
exec curl -s "https://api.llama.fi/protocol/aave" | jq '{name, category, chains, tvl: .currentChainTvls, points: (.tvl|length)}'
```
`.tvl` is `[{date, totalLiquidityUSD}]` — date is a unix timestamp.

**Chains** — TVL of every chain now:
```bash
exec curl -s "https://api.llama.fi/v2/chains" | jq -r 'sort_by(-.tvl)[:15][] | "\(.name) \(.tvl)"'
```
History of one chain: `https://api.llama.fi/v2/historicalChainTvl/Ethereum`.

**Fees and revenue** (daily, all protocols or one):
```bash
exec curl -s "https://api.llama.fi/overview/fees?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true" | jq -r '.protocols | sort_by(-.total24h)[:10][] | "\(.name) fees24h=\(.total24h) rev24h=\(.revenue24h)"'
exec curl -s "https://api.llama.fi/summary/fees/aave?dataType=dailyRevenue" | jq '{name, total24h, total7d, total30d}'
```

**Stablecoins** — supply by asset and by chain:
```bash
exec curl -s "https://stablecoins.llama.fi/stablecoins?includePrices=true" | jq -r '.peggedAssets | sort_by(-.circulating.peggedUSD)[:10][] | "\(.symbol) \(.circulating.peggedUSD)"'
```

**Yield pools** (large response — filter):
```bash
exec curl -s "https://yields.llama.fi/pools" | jq -r '.data[] | select(.project=="aave-v3" and .chain=="Ethereum") | "\(.symbol) apy=\(.apy) tvl=\(.tvlUsd)"'
```

**Prices** by `chain:address` or `coingecko:id`:
```bash
exec curl -s "https://coins.llama.fi/prices/current/ethereum:0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48,coingecko:bitcoin" | jq '.coins'
```

## Standards
- Say "TVL" for value locked and never call it revenue, users or volume.
- A TVL drop is not, by itself, an exodus: price moves change TVL in USD with
  no one leaving. Check the token-denominated series or the price before you
  interpret.
- Fees are what users paid; revenue is what the protocol kept. Report the one
  you were asked for and label it.
- Every figure: value, currency, the DefiLlama timestamp, and the protocol's
  own chain breakdown when a chain is in question.
- If a slug is not found, search the list and show the candidates; do not
  guess a protocol from a similar name.

## Output
Inline for a few figures; a table for a comparison; a dashboard via
`build-dashboard` when they will look at it again. Always: metric, value,
as-of time, source "DefiLlama".

## Defaults
- Currency USD; windows 24h / 7d / 30d when a change is asked.
- History: daily points, the last 90 days unless asked.
- Responses over ~1 MB (yields, all protocols): filter with `jq` before reading.
