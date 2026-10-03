---
name: hubspot-crm
version: 0.1.0
description: >-
  Work inside the person's HubSpot CRM through their connected account — find
  and read contacts, companies, deals, pipelines, notes and tasks; answer
  "who/what/how many" questions from live data; and create or update records,
  log notes and tasks, or merge duplicates only after the person approves the
  exact change, keeping a log of every write. Use when the user says
  "HubSpot", "in the CRM", "update the deal", "log this call", "create a
  contact", "who owns", "deals closing this month", "find the company".
  Needs HubSpot connected. Not for deciding what is dirty (crm-hygiene) or
  reviewing the pipeline (pipeline-review).
metadata:
  openclaw:
    emoji: "🧲"
  orchestra:
    requires:
      integrations:
        - hubspot
---
# HubSpot CRM — read anything, change only what was approved

The CRM is the company's shared memory, and a wrong write there is worse
than no write: someone will trust it. This skill reads HubSpot freely to
answer questions, and changes it only with a preview the person approved —
record by record, field by field — logging every change so it can be undone.

## Related skills
- **crm-hygiene** — finds duplicates, gaps and stale records; this skill
  applies the fixes it proposes.
- **pipeline-review** — the weekly look at deals; this skill fetches them.
- **account-research** — public facts about a company before enriching it.
- **orch-composio** — the tool every call goes through.
(If a referenced skill is not installed, do the equivalent inline.)

## When to use
- Any question answered from, or change made to, HubSpot.
- **Do NOT use** to delete records, change pipelines or properties
  (schema), send marketing email, or change ownership in bulk — those are
  admin decisions; propose them and let the person do them in HubSpot.

## Workflow
1. **Check the connection**: `orch-composio connections`. Not connected →
   say so and stop. More than one HubSpot account → use the one the
   procedure names.
2. **Find the action, then its schema.** Core actions (confirm with
   `orch-composio schema --slug <SLUG>` before the first use — schemas
   change): `HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA`, `HUBSPOT_SEARCH_COMPANIES`,
   `HUBSPOT_SEARCH_DEALS`, `HUBSPOT_GET_DEAL`, `HUBSPOT_GET_COMPANY`,
   `HUBSPOT_LIST_DEALS`, `HUBSPOT_GET_PIPELINE_BY_ID`, `HUBSPOT_LIST_CONTACT_NOTES`,
   `HUBSPOT_LIST_CONTACT_TASKS`, `HUBSPOT_LIST_DEAL_ACTIVITIES`. For anything
   else: `orch-composio tools --toolkit hubspot --search "<what>"`.
3. **Read and answer.** Search narrowly (by email, domain, deal name,
   owner, date range), page through results, and answer in plain language
   with counts and the records behind them. Never paste raw JSON.
4. **Writes are proposals first.** For a create, update, note, task or
   merge (`HUBSPOT_CREATE_CONTACT`, `HUBSPOT_UPDATE_CONTACT`,
   `HUBSPOT_UPDATE_DEAL`, `HUBSPOT_CREATE_NOTE`, `HUBSPOT_CREATE_TASK`,
   `HUBSPOT_MERGE_CONTACTS`, …) show a preview — record, field, current
   value → new value — and wait for the yes on that preview.
5. **Execute exactly the approved preview**, one record or one batch, then
   read the records back to confirm.
6. **Log the write** in the instance database (`orch-database`, table
   `crm_changes`: when, record type, id, field, before, after, approved_by,
   action). Say what changed in one line.

## Standards
- Read before write: every update starts from the record as it is now.
- Never overwrite a non-empty field with a guess; never fill a field from
  inference without saying so in the preview.
- Merges are irreversible in HubSpot: show both records side by side and
  which one survives, and merge only on an explicit yes.
- Personal data from the CRM stays in the conversation.
- If a call fails, say what failed and what was not changed.

## Output
Answers: the answer first, then the records (name · owner · stage/status ·
amount · last activity · link if available). Writes: the preview table,
then "done: n records changed", with the log.

## Defaults
- Date ranges → this month for deals, last 30 days for activity.
- Owner unknown → ask; never assign to the person by default.
- Batch writes → at most 50 records per approval.
