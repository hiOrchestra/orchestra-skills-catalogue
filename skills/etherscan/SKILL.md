---
name: etherscan
version: 0.1.0
description: >-
  On-chain data for Ethereum and 60+ EVM chains via the Etherscan API (V2):
  address balances, transactions, ERC-20 transfers/holdings, contract ABI &
  source, gas oracle, ETH price, and PRO analytics (historical balances, token
  info, daily stats). Authenticates with USR_ETHERSCAN_API_KEY.
triggers:
  - etherscan
  - ethereum
  - on-chain
  - onchain
  - wallet
  - address balance
  - transactions
  - erc20
  - token holdings
  - contract abi
  - gas price
  - gwei
metadata:
  openclaw:
    emoji: "⛓️"
requires:
  bins: []
  env:
    - USR_ETHERSCAN_API_KEY
  config: []
---

# Etherscan (API V2 + PRO)

Query on-chain data with `exec curl` against the Etherscan **V2** API. One API
key works across 60+ chains via the `chainid` param. Key is in
`USR_ETHERSCAN_API_KEY` — **send it as the `apikey` query param; never print it.**

## Request shape

```
https://api.etherscan.io/v2/api?chainid=<ID>&module=<MODULE>&action=<ACTION>&<PARAMS>&apikey=$USR_ETHERSCAN_API_KEY
```

Common `chainid`s: `1` Ethereum · `8453` Base · `42161` Arbitrum · `10` Optimism
· `137` Polygon · `56` BNB Chain. Default to `1` (Ethereum) unless the user names a chain.

**Response:** `{ "status": "1", "message": "OK", "result": ... }`.
`status: "0"` means error — read `result`/`message` (e.g. rate limit, or a PRO
endpoint called with a free key). For `proxy` JSON-RPC actions the shape is
`{ "jsonrpc": "2.0", "result": ... }` instead.

**Units:** native balances are in **wei** (÷ 1e18 = ETH). ERC-20 amounts are in
the token's smallest unit (÷ 10^decimals).

## Free endpoints

```bash
# Native balance of an address (wei)
exec curl -s "https://api.etherscan.io/v2/api?chainid=1&module=account&action=balance&address=0xADDRESS&tag=latest&apikey=$USR_ETHERSCAN_API_KEY"

# Normal transactions (paginate with page/offset; sort=desc for newest)
exec curl -s "https://api.etherscan.io/v2/api?chainid=1&module=account&action=txlist&address=0xADDRESS&startblock=0&endblock=99999999&page=1&offset=20&sort=desc&apikey=$USR_ETHERSCAN_API_KEY"

# ERC-20 transfer events for an address (optionally &contractaddress=0xTOKEN)
exec curl -s "https://api.etherscan.io/v2/api?chainid=1&module=account&action=tokentx&address=0xADDRESS&page=1&offset=20&sort=desc&apikey=$USR_ETHERSCAN_API_KEY"

# ERC-20 balance of one token for an address
exec curl -s "https://api.etherscan.io/v2/api?chainid=1&module=account&action=tokenbalance&contractaddress=0xTOKEN&address=0xADDRESS&tag=latest&apikey=$USR_ETHERSCAN_API_KEY"

# Verified contract ABI / source code
exec curl -s "https://api.etherscan.io/v2/api?chainid=1&module=contract&action=getabi&address=0xCONTRACT&apikey=$USR_ETHERSCAN_API_KEY"
exec curl -s "https://api.etherscan.io/v2/api?chainid=1&module=contract&action=getsourcecode&address=0xCONTRACT&apikey=$USR_ETHERSCAN_API_KEY"

# Latest ETH price (USD + BTC) and gas oracle (gwei: Safe/Propose/Fast)
exec curl -s "https://api.etherscan.io/v2/api?chainid=1&module=stats&action=ethprice&apikey=$USR_ETHERSCAN_API_KEY"
exec curl -s "https://api.etherscan.io/v2/api?chainid=1&module=gastracker&action=gasoracle&apikey=$USR_ETHERSCAN_API_KEY"
```

## PRO endpoints (require an Etherscan API **Pro** plan)

With a free key these return `status: "0"`. If that happens, tell the user the
endpoint needs an Etherscan Pro key.

```bash
# All ERC-20 token holdings for an address
exec curl -s "https://api.etherscan.io/v2/api?chainid=1&module=account&action=addresstokenbalance&address=0xADDRESS&page=1&offset=100&apikey=$USR_ETHERSCAN_API_KEY"

# Historical native balance at a block
exec curl -s "https://api.etherscan.io/v2/api?chainid=1&module=account&action=balancehistory&address=0xADDRESS&blockno=12345678&apikey=$USR_ETHERSCAN_API_KEY"

# Historical ERC-20 balance at a block
exec curl -s "https://api.etherscan.io/v2/api?chainid=1&module=account&action=tokenbalancehistory&contractaddress=0xTOKEN&address=0xADDRESS&blockno=12345678&apikey=$USR_ETHERSCAN_API_KEY"

# Token project info; ERC-20 holder list
exec curl -s "https://api.etherscan.io/v2/api?chainid=1&module=token&action=tokeninfo&contractaddress=0xTOKEN&apikey=$USR_ETHERSCAN_API_KEY"
exec curl -s "https://api.etherscan.io/v2/api?chainid=1&module=token&action=tokenholderlist&contractaddress=0xTOKEN&page=1&offset=50&apikey=$USR_ETHERSCAN_API_KEY"

# Daily network stats (need startdate/enddate=YYYY-MM-DD & sort)
#   dailytx · dailynewaddress · dailytxnfee · dailyavggasprice · dailygasused
#   dailyavggaslimit · ethdailyprice (historical ETH price)
exec curl -s "https://api.etherscan.io/v2/api?chainid=1&module=stats&action=dailytx&startdate=2026-06-01&enddate=2026-06-15&sort=asc&apikey=$USR_ETHERSCAN_API_KEY"
```

## Rules

- **Always pass `apikey=$USR_ETHERSCAN_API_KEY`.** Never print or echo the key.
- Validate addresses look like `0x` + 40 hex chars before calling.
- Convert wei/token units to human numbers in your answer; don't dump raw wei.
- Check `status`: on `"0"`, report the `result`/`message` succinctly (rate limit,
  no transactions found, or "needs Pro key"). Don't invent data.
- Rate limit: free ~5 calls/s; Pro ~10–30/s. Batch where possible; on a rate-limit
  error wait and retry once.
- Pick `chainid` from what the user asks (default Ethereum `1`).
