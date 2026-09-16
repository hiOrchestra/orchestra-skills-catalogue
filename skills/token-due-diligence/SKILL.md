---
name: token-due-diligence
version: 0.1.0
description: >-
  Check a token or contract before anyone acts on it — verified source, owner
  powers (mint, pause, blacklist, fee change), holder concentration, liquidity
  and its lock, age and activity, listings and fundamentals — and give a
  red-flag list with a verdict. Use when the user says "is this token legit",
  "check this contract", "rug pull", "honeypot", "should I worry about",
  "due diligence on", "look into this token", or pastes a contract address.
  Not for price questions (coingecko), a wallet's activity (wallet-watch), or
  advice on whether to buy — it describes risk, it does not recommend.
metadata:
  openclaw:
    emoji: "🔬"
  orchestra:
    requires:
      skills:
        - etherscan
        - coingecko
---
# Token Due Diligence — what this contract can do to its holders

Most losses in tokens are not market moves; they are powers the contract gave
someone and a structure that let them use it. This skill reads the contract and
the chain for those powers and structures, checks the market and fundamentals
around it, and reports a red-flag list with a verdict on the scale below. It
describes risk; the decision is the person's.

## Related skills
- **etherscan** — contract source, ABI, holders, transactions.
- **coingecko** / **defillama** — listings, market cap, TVL, fees.
- **research-brief** — the team and the project behind the token.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- A contract address, a token name or a "is this safe" question.
- **Do NOT use** to say buy or sell. Do not run it on a token you cannot
  identify unambiguously (chain + address); ask for the address.

## Workflow
1. **Pin the identity.** Chain and address, checksummed. If given a name, find
   the address on `coingecko` (`platforms`) and confirm it with the person —
   copycat tokens share names.
2. **Contract.** With `etherscan`: is the source verified (unverified is a
   red flag on its own); proxy or not, and who can upgrade it; owner address
   and whether ownership is renounced or a multisig/timelock; functions that
   matter — `mint`, `pause`, `blacklist`/`freeze`, fee setters, max-tx and
   max-wallet limits, transfer hooks. Read the code for these, not the ABI
   names only.
3. **Supply and holders.** Total supply vs. circulating; the top 10 holders and
   their share, excluding known contracts (pool, staking, bridge, burn); the
   deployer's balance; how many holders and how the count moved.
4. **Liquidity.** Which pool, how deep, who holds the LP tokens and whether
   they are locked or burned and until when. Thin liquidity plus a large
   holder is the classic exit.
5. **Age and activity.** Contract creation date, first liquidity, transaction
   count over the last 7 and 30 days, unusual patterns (many small buys from
   fresh wallets, sells failing).
6. **Fundamentals and listings.** CoinGecko listing and market cap; DefiLlama
   TVL and fees if it is a protocol token; audits linked from the project and
   whether the audited address is this one; the team, via `research-brief`
   if it matters.
7. **Write the report** under Output and grade it.

## Standards
- Every flag cites what you read: the function, the holder address, the pool,
  the date. No flag from vibes.
- A power is a risk even if unused. "Owner can mint" is reported whether or
  not they ever did.
- Say what you could not check (no verified source, a chain Etherscan does not
  cover) — an unchecked item is not a pass.
- Never call a token safe. The best grade says no red flags were found in
  what was checked, on that date.
- No buy/sell/hold language anywhere in the report.

## Verdict
- **Red** — a power or structure that can take holders' value at will (mint
  without cap, unlocked liquidity with a dominant holder, transfer can be
  blocked, unverified source with owner powers).
- **Amber** — concentration or powers mitigated by a timelock, multisig, lock
  or track record; or important items unchecked.
- **Green** — no red flags found in the checks listed, on the date given.

## Output
- **Token** — name, chain, address, as-of date.
- **Verdict** — one word from the scale, one line why.
- **Red flags** — each with evidence; then **Amber items**; then **Checked,
  no issue**.
- **Not checked** — and why.
- **Figures** — supply, holders, top-10 share, liquidity depth and lock,
  age, market cap, source and time for each.

## Defaults
- Chain unknown → Ethereum mainnet first, then ask.
- Report saved to `orch-files` under `due-diligence/<symbol>-<date>.md` when
  longer than a screen.
