"""Every catalogue skill must have the SAME shape, and its references must resolve.

This is the same check the platform runs over its own skills
(openclaw-railway test/skill-schema.test.py). It lives here too because these
skills are installed onto tenant instances, so a shape mistake here reaches
every tenant that installs one — and on 2026-08-26 all fifteen carried a
top-level `requires:`, which meant wordpress, coingecko and etherscan installed
WITHOUT their API keys and never prompted for them.

    python3 check-schema.py

WHY. An audit on 2026-08-26 found three independent problems, all invisible
because nothing checked:

  1. THE SCHEMA WAS NOT ONE SCHEMA. OpenClaw follows the AgentSkills spec
     (name + description required; homepage, user-invocable,
     disable-model-invocation, command-dispatch, command-tool, command-arg-mode
     optional; gating in a `metadata.openclaw` block). We shipped `triggers:` on
     12 of 13 skills and `tool:` on 7 — NEITHER is read anywhere in the gateway
     build. Twelve skills carried a discovery mechanism that does not exist.

  2. DESCRIPTION IS THE ENTIRE DISCOVERY SURFACE. The system prompt carries only
     name + description per skill. There is no trigger matching. So a thin
     description means the agent never opens the skill — which is exactly how
     the canvas publish rules failed to reach an agent that HAD the skill loaded.

  3. REFERENCES DID NOT RESOLVE. Support files must be addressed as
     `{baseDir}/references/x.md`; the agent resolves {baseDir} against the
     skill's own directory. Ours said `references/x.md`, which resolves against
     the agent's WORKSPACE and does not exist. ~45,000 chars of design guidance
     sat unreachable behind a path we told the agent to read.

Run: python3 test/skill-schema.test.py    (or via scripts/run-tests.sh)
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SKILLS = ROOT / "skills"

# Keys the gateway actually reads (AgentSkills spec + OpenClaw extensions).
ALLOWED_TOP_LEVEL = {
    "name", "description", "homepage", "metadata",
    "user-invocable", "disable-model-invocation",
    "command-dispatch", "command-tool", "command-arg-mode",
    "license", "version", "allowed-tools",
}

# Keys we shipped that NOTHING reads. Listed by name so the failure message can
# say what to do instead of just "unknown key".
INERT = {
    "triggers": (
        "no trigger matching exists — the prompt carries only name+description. "
        "Fold the phrases into `description` instead, which IS the discovery surface"
    ),
    "tool": "not a spec key; the real one is `command-tool` (with `command-dispatch: tool`)",
    "requires": (
        "at the top level this is IGNORED — proven on staging 2026-08-26: a skill "
        "declaring an unset key there stayed eligible and loaded WITHOUT it. Gating "
        "reads `metadata.openclaw.requires` only"
    ),
    "requirements": (
        "the ignored spelling. Only `requires` is read — `requirements` gates nothing, "
        "for binaries or env"
    ),
    "emoji": "belongs inside `metadata.openclaw.emoji`",
}

# Spellings that LOOK like they declare a dependency and gate nothing. Measured
# on staging by declaring the same unset key each way and reading
# `openclaw skills check --json`:
#
#   metadata.openclaw.requires.bins   absent binary  -> eligible False   HONOURED
#   metadata.openclaw.requires.env    unset key      -> eligible False   HONOURED
#   metadata.openclaw.requirements.*  either         -> eligible True    ignored
#   metadata.openclaw.primaryEnv      unset key      -> eligible True    ignored for gating
#   top-level requires (list or map)  either         -> eligible True    ignored
#
# A skill using an ignored spelling loads and runs WITHOUT its credentials or its
# binaries, and fails at runtime with nothing having warned. One tenant skill
# (granola-direct-api) was in exactly that state.
IGNORED_NESTED = {
    "requirements": "gates nothing — rename to `requires`, with `bins:` / `env:` beneath it",
    "binaries": "gates nothing — the honoured key is `bins:` under `requires:`",
}

# Support-file directories the spec recognises.
SUPPORT_DIRS = {"references", "scripts", "assets", "examples", "templates"}

# A description short enough to be useless for discovery. The agent decides
# whether to open a skill from this text alone.
MIN_DESCRIPTION_CHARS = 80


def frontmatter(text):
    """(raw_block, {top_level_key: True}) — tolerant of YAML we don't fully parse."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, {}
    block = m.group(1)
    keys = {}
    for line in block.splitlines():
        km = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):", line)
        if km:
            keys[km.group(1)] = True
    return block, keys


def described(block):
    """The description value, flattened — handles `>`/`>-` folded scalars."""
    m = re.search(r"^description:\s*(.*)$", block, re.M)
    if not m:
        return ""
    first = m.group(1).strip()
    if first not in (">", ">-", "|", "|-", ""):
        return first
    out = []
    started = False
    for line in block.splitlines():
        if re.match(r"^description:", line):
            started = True
            continue
        if started:
            if re.match(r"^\S", line):
                break
            out.append(line.strip())
    return " ".join(out).strip()


failures = []
checked = 0

for skill_dir in sorted(SKILLS.glob("*/")):
    md = skill_dir / "SKILL.md"
    if not md.exists():
        failures.append(f"{skill_dir.name}: no SKILL.md")
        continue

    checked += 1
    text = md.read_text()
    label = skill_dir.name
    block, keys = frontmatter(text)

    if block is None:
        failures.append(f"{label}: no YAML frontmatter")
        continue

    # ── required keys ────────────────────────────────────────────────────
    for req in ("name", "description"):
        if req not in keys:
            failures.append(f"{label}: missing required `{req}`")

    # ── nothing inert ────────────────────────────────────────────────────
    for key, why in INERT.items():
        if key in keys:
            failures.append(f"{label}: remove `{key}:` — {why}")

    # ── dependency declared where nothing reads it ───────────────────────
    for key, why in IGNORED_NESTED.items():
        if re.search(rf"^\s+{key}:", block, re.M):
            failures.append(
                f"{label}: `{key}:` inside metadata — {why}. As written the skill "
                f"loads without its dependency and fails at runtime"
            )

    # ── nothing unrecognised ─────────────────────────────────────────────
    for key in keys:
        if key not in ALLOWED_TOP_LEVEL and key not in INERT:
            failures.append(
                f"{label}: `{key}:` is not read by the gateway. "
                f"Put it in `metadata.openclaw` or drop it"
            )

    # ── name matches the directory ───────────────────────────────────────
    nm = re.search(r"^name:\s*(.+)$", block, re.M)
    if nm:
        name = nm.group(1).strip().strip('"').strip("'")
        expected = re.sub(r"-skill$", "", skill_dir.name)
        if name != expected:
            failures.append(
                f"{label}: name is `{name}` but the directory implies `{expected}`. "
                f"The gateway keys skills by this name, so a mismatch is a rename waiting to surprise someone"
            )

    # ── description carries enough to decide on ──────────────────────────
    desc = described(block)
    if desc and len(desc) < MIN_DESCRIPTION_CHARS:
        failures.append(
            f"{label}: description is {len(desc)} chars. It is the ONLY thing the agent "
            f"sees when deciding whether to open this skill — say what it does AND when not to use it"
        )

    # ── every referenced support file uses {baseDir} and exists ──────────
    body = text[len(block) + 8:] if block else text
    # A bare relative path is a REAL bug only when it names a file this skill
    # actually has — that is a live reference written the wrong way. Prose
    # quoting the wrong form as a counter-example names nothing that exists,
    # and a skill SHOULD be able to explain the trap without tripping this.
    bare = re.findall(r"`((?:references|scripts|assets|examples|templates)/[^`]+)`", body)
    for path in dict.fromkeys(bare):
        if (skill_dir / path).exists():
            failures.append(
                f"{label}: `{path}` is a bare relative path to a file this skill really has. "
                f"It resolves against the AGENT'S WORKSPACE, not the skill, so the read fails. "
                f"Write `{{baseDir}}/{path}`"
            )

    for ref in re.findall(r"\{baseDir\}/([^\s`\"')]+)", body):
        if "<" in ref or ">" in ref:
            continue  # a placeholder inside guidance, not a real target
        if not (skill_dir / ref).exists():
            failures.append(f"{label}: references `{{baseDir}}/{ref}` which does not exist")

    # ── support dirs must be ones the spec knows ─────────────────────────
    for child in skill_dir.iterdir():
        if child.is_dir() and child.name not in SUPPORT_DIRS:
            failures.append(
                f"{label}: `{child.name}/` is not a recognised support dir "
                f"({', '.join(sorted(SUPPORT_DIRS))})"
            )

print(f"checked {checked} skills")

if failures:
    print("\nFAILURES:")
    for f in failures:
        print(f"  ✗ {f}")
    sys.exit(1)

print("  ✓ every skill has name + description")
print("  ✓ no inert keys (triggers / tool / top-level requires)")
print("  ✓ name matches directory")
print("  ✓ descriptions carry enough to decide on")
print("  ✓ support files addressed as {baseDir}/… and present on disk")
print("\nAll skill-schema checks passed.")
