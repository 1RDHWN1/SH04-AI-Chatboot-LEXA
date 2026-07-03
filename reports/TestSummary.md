# Test Summary Report — SH04-AI-Chatbot-LEXA

**Project:** SH04-AI-Chatbot-LEXA  
**Version:** 1.0.0  
**Date:** 2025-07-01  
**Prepared By:** QA Engineering Team

---

## Test Execution Summary

| Metric                        | Value      |
|-------------------------------|------------|
| **Total Test Cases Planned**  | 63         |
| **Total Test Cases Executed** | 63         |
| **PASS**                      | 49 (77.8%) |
| **PARTIAL PASS**              | 9 (14.3%)  |
| **FAIL**                      | 6 (9.5%)   |
| **Blocked**                   | 0 (0%)     |
| **Not Executed**              | 0 (0%)     |

---

## Results by Category

```
Functional  ██████████████████████████████  100%  (10/10 PASS)
UI          ████████████████████████░░░░░░   84%  (11/13 PASS)
API         ████████████████████████░░░░░░   80%  (8/10 PASS)
Negative    ████████████████████░░░░░░░░░░   64%  (7/11 PASS)
Security    ████████████████░░░░░░░░░░░░░░   56%  (5/9 PASS)
Performance ████████████████████████░░░░░░   80%  (8/10 PASS)
            0%                          100%
```

---

## Bug Summary

| ID | Title | Severity | Status |
|----|-------|----------|--------|
| Bug-001 | Missing .gitignore | 🔴 Critical | Open |
| Bug-002 | No input validation in llm.py | 🟠 High | Open |
| Bug-003 | Dark mode CSS override | 🟡 Medium | Open |
| Bug-004 | Rate limit error not user-friendly | 🟠 High | Open |
| Bug-005 | Unbounded history growth | 🟠 High | Open |
| ST-005 | No prompt injection defense | 🔴 Critical | Open |
| UT-010 | Mobile sidebar overlap | 🟡 Medium | Open |
| AT-007 | No rate limit retry | 🟠 High | Open |
| NT-011 | Reset race condition | 🟡 Medium | Open |
| AT-010 | History token growth latency | 🟠 High | Open |

**Total Bugs: 10** | Critical: 2 | High: 5 | Medium: 3

---

## Test Environment

| Item | Value |
|------|-------|
| Python | 3.11.4 |
| Streamlit | 1.32.0 |
| groq SDK | 0.9.0 |
| OS | Ubuntu 22.04 LTS |
| Model | openai/gpt-oss-120b |
| Test Duration | 2025-06-30 to 2025-07-01 |

---

## Pass/Fail Trend

```
100% ●─────────────────────────────●
                                    \
 80%                         ●───────●──────●
                            /
 64%                  ●────●
                      |
 56%             ●────●
      |           |    |    |    |    |
    Func        API  Perf  UI  Neg  Sec
```

---

## Exit Criteria Status

| Criterion | Target | Actual | Status |
|-----------|--------|--------|--------|
| Test Cases Executed | 100% | 100% | ✅ |
| Overall Pass Rate | ≥85% | 77.8% | ⚠️ Below Target |
| Critical Bugs Resolved | 100% | 0% | ❌ |
| High Bugs Resolved | 100% | 0% | ❌ |
| All Deliverables Complete | Yes | Yes | ✅ |

**Exit Criteria Status: NOT MET** — Critical bugs must be resolved before sign-off.

---

*QA Engineering Team — 2025-07-01*
