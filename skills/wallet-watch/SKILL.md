---
name: wallet-watch
version: 0.1.0
description: >-
  Keep a standing watch on addresses — a baseline of balances and holdings, a
  scheduled check, and a report of movements above a threshold with the
  transaction hashes, or "nothing" when nothing moved. Use when the user says
  "watch this wallet", "alert me if this address moves", "track the treasury",
  "monitor these addresses", "tell me when funds leave", "whale watch". Not
  for a one-off look at an address (etherscan), for prices (coingecko), or
  for news about a project (topic-watch).
metadata:
  openclaw:
    emoji: "👁️"
  orchestra:
    requires:
      skills:
        - etherscan
---
# Wallet Watch — baseline, routine, only what moved

An address that matters — a treasury, a team wallet, a counterparty, a whale —
is watched the same way a topic is: a baseline, a routine with `orch-jobs`,
and a report that says only what changed, with the transaction hash, or
"nothing". Every figure carries the block or time it was read.

## Related skills
- **etherscan** — the reads: balances, transfers, token holdings.
- **coingecko** — USD value of what moved, with the time of the price.
- **topic-watch** — the same shape for news; **orch-jobs** — the routine.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Movements over time on named addresses, reported on a cadence or a threshold.
- **Do NOT use** for "what is in this wallet now" — that is one `etherscan`
  call. Never watch an address the person has not named explicitly, and never
  ask for or hold a private key: a watch is read-only.

## Workflow
1. **Define the watch**: the addresses (checksummed, with the chain, and a
   label for each — "treasury", "founder"), the threshold that counts as a
   movement (an amount in the native token, in a named token, or in USD), the
   cadence (or "as soon as possible", which means the shortest cadence the
   routine allows), the channel for the report, whether to log to a table.
2. **Baseline.** With `etherscan`: native balance, ERC-20 holdings, the latest
   block seen, for each address. Write `watch/wallets/<slug>/baseline.md` in
   `orch-files` with the figures, the block and the time.
3. **Create the routine** with `orch-jobs create`: the message says to read
   the baseline, fetch transfers since the last block for each address,
   compare balances, report movements over the threshold with hashes, update
   the baseline; `--notify` the channel; `--table` if they want a log.
4. **Each run**: transfers in and out since the last block (native and ERC-20),
   balances now vs. baseline, USD value at the time of the run via
   `coingecko` (labelled with that time), counterparties named when they are
   known contracts (an exchange deposit, a bridge, a pool).
5. **Tune**: when they say "too noisy", raise the threshold in the baseline
   and say so; never silently drop a movement.

## Standards
- Every movement: direction, amount, token, USD at run time, counterparty,
  transaction hash, block. A movement without a hash is not reported.
- Balances are read from the chain, never inferred from the last report.
- A large inbound is reported like a large outbound; the person decides what
  matters.
- Chains Etherscan does not cover are stated as not watched.
- "Nothing moved above <threshold> since block <n>" is a report.

## Output
Per run, in the channel they chose:
- **Watch · period · blocks** — one line.
- **Movements** — one line each, or "Nothing above <threshold>".
- **Balances now** — per address, native and named tokens, vs. baseline.
- **Next check** — time.

## Defaults
- Threshold unknown → propose one from the address's size (1% of its
  balance) and ask.
- Cadence unknown → hourly for a treasury, daily for everything else; say so.
- USD value: CoinGecko price at run time, labelled; no historical reprice.
