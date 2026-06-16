---
name: coingecko
version: 0.2.0
description: >-
  Live cryptocurrency prices and market data from CoinGecko. Use to answer
  questions about the current price, 24h change, or market cap of any coin or
  token (Bitcoin, Ethereum, etc.). Authenticates with the CoinGecko Demo API
  key stored in config as USR_COINGECKO_API_KEY.
triggers:
  - crypto
  - cryptocurrency
  - bitcoin
  - ethereum
  - coin
  - token
  - price of
  - market cap
requires:
  bins: []
  env:
    - USR_COINGECKO_API_KEY
  config: []
---

# CoinGecko — live crypto prices

Answer crypto price / market questions by calling CoinGecko's REST API directly
with `exec curl`.

Base URL: `https://api.coingecko.com/api/v3`

## Auth — use the stored API key

The CoinGecko **Demo** API key is stored in config as `USR_COINGECKO_API_KEY`
and is available as an environment variable in `exec`. Send it on every request
with the `x-cg-demo-api-key` header — do NOT print the key:

```bash
exec curl -s -H "x-cg-demo-api-key: $USR_COINGECKO_API_KEY" \
  "https://api.coingecko.com/api/v3/ping"
```

(If `USR_COINGECKO_API_KEY` is a **Pro** key instead of a Demo key, use base URL
`https://pro-api.coingecko.com/api/v3` and header `x-cg-pro-api-key`.)

## Important: resolve the coin id first

CoinGecko endpoints take a **coin id** (e.g. `bitcoin`, `ethereum`, `solana`),
NOT a ticker symbol (`BTC`, `ETH`). Common ones you can use directly:
`bitcoin`, `ethereum`, `solana`, `cardano`, `dogecoin`, `ripple`, `tether`,
`binancecoin`, `usd-coin`.

If the user names something you're unsure of, resolve it first:

```bash
exec curl -s -H "x-cg-demo-api-key: $USR_COINGECKO_API_KEY" \
  "https://api.coingecko.com/api/v3/search?query=arbitrum"
```

Read `coins[0].id` from the JSON and use that id below.

## Get current price (the main one)

```bash
exec curl -s -H "x-cg-demo-api-key: $USR_COINGECKO_API_KEY" \
  "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd,eur&include_24hr_change=true&include_market_cap=true"
```

Returns, per coin: price in each currency, 24h % change (`*_24h_change`), and
market cap (`*_market_cap`). Example response shape:

```json
{ "bitcoin": { "usd": 68000, "usd_24h_change": 2.1, "usd_market_cap": 1.3e12 } }
```

## Trending coins (optional)

```bash
exec curl -s -H "x-cg-demo-api-key: $USR_COINGECKO_API_KEY" \
  "https://api.coingecko.com/api/v3/search/trending"
```

## Rules

- **Always send the `x-cg-demo-api-key: $USR_COINGECKO_API_KEY` header.** Never
  print or echo the key value in your reply or in command output.
- **One call is usually enough** — batch multiple coins into a single
  `simple/price` call with a comma-separated `ids` list. Do not loop one request
  per coin.
- If you get HTTP 401/403, the key is missing or invalid — say so and tell the
  user to set `USR_COINGECKO_API_KEY` in config. If you get HTTP 429, you hit the
  rate limit; wait and retry once, then report it succinctly.
- Always parse the JSON from stdout and answer in plain language with the
  number(s) the user asked for; mention the 24h change when relevant.
- Do not invent prices. If the call fails, say so and show the error briefly.
