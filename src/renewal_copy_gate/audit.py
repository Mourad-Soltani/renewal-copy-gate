# Mourad.Soltani
"""Rule engine for SaaS auto-renewal and checkout copy.

This is a drafting aid, not a legal opinion. Rules follow public checklist
themes (price, cadence, renewal, cancel path, notice, trial conversion).
"""

from __future__ import annotations

import re
from typing import Any

PRICE_RE = re.compile(
    r"(?:(?:usd|eur|gbp|cad|aud|\$|€|£)\s?\d{1,6}(?:[.,]\d{2})?)|(?:\d{1,6}(?:[.,]\d{2})?\s?(?:usd|eur|gbp|cad|aud|\$|€|£|/mo|/month|/yr|/year))",
    re.I,
)
CURRENCY_RE = re.compile(r"\b(usd|eur|gbp|cad|aud|chf)\b|[$€£]", re.I)
CADENCE_RE = re.compile(
    r"\b(per month|monthly|each month|/mo\b|per year|annual|annually|yearly|/yr\b|billed every|every \d+ (days|months))\b",
    re.I,
)
SUBSCRIPTION_RE = re.compile(
    r"\b(subscription|subscribe|recurring|membership|plan|billed|auto-?renew)\b",
    re.I,
)
RENEW_RE = re.compile(
    r"\b(auto-?renew|automatically renew|renews automatically|will renew|renewal)\b",
    re.I,
)
CANCEL_RE = re.compile(
    r"\b(cancel|cancellation|unsubscribe)\b.{0,80}\b(account|settings|dashboard|email|portal|button|link|online)\b|"
    r"\b(cancel anytime|cancel online|self-serve cancel|cancel in (your )?account)\b",
    re.I,
)
NOTICE_RE = re.compile(
    r"\b(\d+\s*(day|days)\s*(notice|before)|notice period|cancel before|prior to renewal|before the renewal)\b",
    re.I,
)
ANNUAL_RE = re.compile(r"\b(annual|annually|yearly|per year|/yr\b|12[- ]month)\b", re.I)
TRIAL_RE = re.compile(r"\b(free trial|trial period|\d+[- ]day trial|start (your )?trial)\b", re.I)
TRIAL_CONVERT_RE = re.compile(
    r"\b(after the trial|when the trial ends|trial converts|then billed|converts to|unless you cancel before)\b",
    re.I,
)
FREE_RE = re.compile(r"\bfree\b", re.I)
FREE_QUAL_RE = re.compile(
    r"\b(free trial|free for \d+|free plan|free tier|no credit card|limits apply|then)\b",
    re.I,
)


def _finding(code: str, severity: str, message: str) -> dict[str, str]:
    return {"code": code, "severity": severity, "message": message}


def audit_copy(text: str) -> dict[str, Any]:
    raw = (text or "").strip()
    findings: list[dict[str, str]] = []
    if len(raw) < 20:
        findings.append(
            _finding("R000", "error", "Paste at least a short pricing or checkout paragraph.")
        )
        return _report(raw, findings)

    if not PRICE_RE.search(raw):
        findings.append(_finding("R001", "error", "No concrete price amount found."))
    if not CURRENCY_RE.search(raw):
        findings.append(_finding("R002", "error", "No currency marker (USD, EUR, $, €, £) found."))
    if SUBSCRIPTION_RE.search(raw) and not CADENCE_RE.search(raw):
        findings.append(
            _finding("R003", "error", "Subscription language without a billing cadence.")
        )
    if SUBSCRIPTION_RE.search(raw) and not RENEW_RE.search(raw):
        findings.append(
            _finding(
                "R004",
                "error",
                "Recurring offer does not say whether it renews automatically.",
            )
        )
    if SUBSCRIPTION_RE.search(raw) and not CANCEL_RE.search(raw):
        findings.append(
            _finding(
                "R005",
                "error",
                "No cancel path (account, settings, email, or portal) is named.",
            )
        )
    if ANNUAL_RE.search(raw) and not NOTICE_RE.search(raw):
        findings.append(
            _finding(
                "R006",
                "warn",
                "Annual term without a notice window before renewal.",
            )
        )
    if TRIAL_RE.search(raw) and not TRIAL_CONVERT_RE.search(raw):
        findings.append(
            _finding(
                "R007",
                "error",
                "Trial is mentioned without what happens when it ends.",
            )
        )
    if FREE_RE.search(raw) and not FREE_QUAL_RE.search(raw) and not TRIAL_RE.search(raw):
        findings.append(
            _finding("R008", "warn", "'Free' appears without a qualifier or limit.")
        )
    return _report(raw, findings)


def _report(raw: str, findings: list[dict[str, str]]) -> dict[str, Any]:
    errors = sum(1 for item in findings if item["severity"] == "error")
    warns = sum(1 for item in findings if item["severity"] == "warn")
    score = max(0, 100 - errors * 18 - warns * 8)
    status = "pass" if errors == 0 else "fail"
    return {
        "service": "renewal-copy-gate",
        "author": "Mourad.Soltani",
        "status": status,
        "score": score,
        "error_count": errors,
        "warn_count": warns,
        "findings": findings,
        "chars": len(raw),
        "disclaimer": "Drafting aid only. Not legal advice.",
    }
