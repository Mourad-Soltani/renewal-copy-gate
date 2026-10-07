# Buyer notes

Signature: Mourad.Soltani

Product: renewal-copy-gate v0.1.0
License: MIT
Stack: Python 3.11 stdlib, CLI + `/health` and `/audit`

## Who pays

- Solo SaaS founders rewriting pricing pages before a Stripe launch
- Boutique agencies that ship checkout copy for clients
- Billing ops people who want a pre-ship checklist, not a law firm memo

## What they buy

A deterministic copy gate they can run in CI. No model key. No crawl. Paste or file in, JSON findings out.

## Price sketch

- Self-host / repo license: $149 one-time for the current code drop
- Done-for-you rule pack for one vertical: $400
- Do not promise regulatory compliance

## Honest limits

Rules are keyword and pattern checks. A lawyer can still reject copy that passes. A page can still fail a regulator while passing this gate. Sell it as a preflight, not a certification.

## Handoff

Repo includes tests. Buyer should re-run `PYTHONPATH=src python3 -m unittest discover -s tests -v` after any rule edit.
