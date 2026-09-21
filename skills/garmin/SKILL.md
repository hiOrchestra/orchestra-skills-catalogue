---
name: garmin
version: 0.1.0
description: >-
  The user's own Garmin Connect data — sleep, HRV, resting heart rate, stress,
  body battery, training readiness, training load, VO2 max, and every recorded
  activity. Use whenever they ask how they slept, whether they are recovered,
  what they trained, how a metric has moved over weeks, or want their health
  read against how their work and calendar are going. Needs the GARMIN_TOKENS
  blob from `orch-garmin login`, run once on the user's own machine.
metadata:
  openclaw:
    emoji: "⌚"
    requires:
      env:
        - GARMIN_TOKENS
  orchestra:
    secrets:
      GARMIN_TOKENS:
        kind: env
        hosts:
          - connect.garmin.com
          - connectapi.garmin.com
        label:
          en: "Garmin session tokens"
          es: "Tokens de sesión de Garmin"
        where:
          en: "Install orch-garmin locally and run `orch-garmin login` — it prints a token blob to paste here. Garmin has no third-party OAuth, so the password never leaves your machine."
          es: "Instala orch-garmin en tu equipo y ejecuta `orch-garmin login` — imprime un bloque de tokens para pegar aquí. Garmin no tiene OAuth para terceros, así que la contraseña nunca sale de tu equipo."
---
# orch-garmin — the user's Garmin Connect data

Run `orch-garmin --help` for every command and flag.

## Is it connected?

```bash
orch-garmin status
```

If it answers `"connected": true` with an account name, everything below works.
If it answers `Not connected to Garmin`, see **When it is not connected** — and
do **not** try to work around it.

## Reading data

```bash
orch-garmin day                          # today: sleep, body, stress, readiness, training, activities
orch-garmin day --date 2026-08-24        # a specific day
orch-garmin day --days 7 --markdown      # the last week, human-readable
orch-garmin trend --metric hrv --days 30 # one metric over time, with average/min/max
orch-garmin activities --days 14         # every activity in a window
orch-garmin races                        # Garmin's current race time predictions
```

`trend --metric` takes: `sleep`, `sleep_score`, `hrv`, `rhr`, `steps`, `weight`,
`body_battery`, `stress`, `readiness`, `vo2_max`.

**Prefer `trend` over looping `day`.** A trend is one Garmin call per day; a day
snapshot is about eleven. Asking for thirty snapshots to answer "how has my HRV
been this month" will get the account rate-limited.

## The stored record

```bash
orch-garmin sync --days 7
```

Writes one markdown file per day to `~/.openclaw/workspace/health/YYYY-MM-DD.md`.
Read those files directly for anything older than a few days — they are already
on disk, and re-fetching history from Garmin is slow and rate-limited. Sync is
what the daily routine runs; you rarely need to call it by hand.

## Interpreting it

The CLI returns numbers, never verdicts — the reading is yours to do, and it is
the whole point of having this. What the data actually supports:

- **Recovery vs. load.** `readiness.score` and `hrv_last_night` against
  `training.load_ratio_status`. HRV below the person's own weekly average for
  several days while load climbs is the classic overreaching shape.
- **Sleep debt.** `sleep.total_minutes` and `sleep.score` across a week, not one
  night. One bad night means nothing.
- **Resting HR drift.** A resting HR trending up over two weeks with flat
  training usually means illness, alcohol, or stress — not fitness loss.
- **Cross-reference their life.** This is the part a generic fitness app cannot
  do: line the health record up against their calendar, their work, what they
  told you they were doing. "Your worst four sleep scores this month were all
  the night before a client call" is a conclusion worth having.

Always ground a claim in the numbers you fetched, and say the window you looked
at. Never invent a metric Garmin did not return — a `null` means the watch did
not record it, and saying so is more useful than a guess.

Be careful and plain about health. Report what the data says and what it
suggests; do not diagnose, and if something looks genuinely off (resting HR far
outside their normal, sustained abnormal SpO2), say it looks worth a doctor
rather than interpreting it yourself.

## When it is not connected

Garmin has no public OAuth for third parties, so connecting needs a real
email + password login against Garmin's SSO, plus an MFA code if the account has
it on. **That login cannot happen here, and must not.**

Tell the user to run this **on their own computer**, from a checkout of the
openclaw-railway repo (the login command ships with this tool, and installing it
locally is what makes it available there):

```bash
python3 -m venv ~/.venvs/orch-garmin
~/.venvs/orch-garmin/bin/pip install ./tools/orch-garmin
~/.venvs/orch-garmin/bin/orch-garmin login --email them@example.com
```

The venv is not optional politeness: a current macOS or Debian refuses a plain
`pip install` into the system Python (PEP 668, "externally-managed-environment").
Keep the venv — the tokens expire yearly and this is the command they re-run.

It prompts for the password locally (never echoed, never stored) and for the MFA
code, then prints one long token blob. They paste that blob into the portal
under **Settings → Secrets → Add**, named **`GARMIN_TOKENS`**, kind *plain
value* (the SDK needs the blob itself). That is the whole setup.

**Never ask the user for their Garmin password, and never accept it if offered.**
Do not offer to run the login for them, do not suggest putting the password in an
env var, and do not propose disabling their MFA. If they paste a password into
the chat anyway, tell them plainly to change it — a password in a conversation
log is a password that has leaked.

The token blob expires roughly yearly, and a `Garmin tokens rejected` error means
exactly that: they re-run the same local login and update the secret.

## Keeping it current

The data is only useful if it is there without anyone asking. Set up a routine
with `orch-jobs` (ask them first — it is their data and their schedule):

```bash
orch-jobs create \
  --name "Garmin daily sync" \
  --message "Run: orch-garmin sync --days 2. Then read today's file in ~/.openclaw/workspace/health/ and note anything worth flagging — poor recovery, a resting HR jump, a heavy load ratio. Stay quiet if the day is unremarkable." \
  --schedule "0 9 * * *" \
  --timezone "Europe/Madrid"
```

`--days 2` rather than `--days 1` on purpose: Garmin finishes processing the
previous night some hours after waking, so yesterday is often still incomplete
at sync time and worth rewriting.

A weekly review is the one that produces the conclusions people actually want —
same shape, `--schedule "0 19 * * 0"`, reading the week's files plus
`orch-garmin trend` for the metrics that matter, and reporting the pattern
rather than the numbers.
