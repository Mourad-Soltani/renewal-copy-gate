# renewal-copy-gate

Signature: Mourad.Soltani

Local micro-tool that audits SaaS pricing, checkout, and order-form copy for auto-renewal disclosure gaps. It checks for a price, a currency, a billing cadence, renewal language, a named cancel path, an annual notice window, and trial-conversion wording.

This is a drafting aid for founders and billing operators. It is not legal advice and it does not file anything with a regulator.

## Why it exists

Negative-option and auto-renew rules keep showing up in chargebacks and support tickets. Most solo SaaS pages still bury the renewal sentence. This gate is a CI-friendly check before copy ships.

## Run

Python 3.11+ and the standard library only.

```bash
PYTHONPATH=src python3 -m renewal_copy_gate.cli sample.txt
PYTHONPATH=src python3 -m renewal_copy_gate.server
curl -s localhost:8080/health
curl -s localhost:8080/audit -H 'content-type: application/json' -d '{"text":"..."}'
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Exit code is 1 when the audit status is `fail`.

## Checks

| Code | Meaning |
| --- | --- |
| R000 | Input too short |
| R001 | No price amount |
| R002 | No currency marker |
| R003 | Subscription language without cadence |
| R004 | No auto-renew disclosure |
| R005 | No named cancel path |
| R006 | Annual term without notice window |
| R007 | Trial without conversion wording |
| R008 | Unqualified "free" |

## Buyer notes

See `BUYER_NOTES.md` and `OUTREACH.md`. Outreach templates are one-to-one only.
