# QA Report — SH04-AI-Chatbot-LEXA

**Project:** SH04-AI-Chatbot-LEXA  
**Version:** 1.0.0  
**QA Lead:** QA Engineering Team  
**Report Date:** 2025-07-01  
**Report Type:** Comprehensive Quality Assessment

---

## 1. Executive Summary

The Lexa Customer Service Chatbot (SH04-AI-Chatbot-LEXA) was subjected to a full QA evaluation covering functional, UI, API, negative, security, and performance testing. The application demonstrates strong core functionality and a clean architecture for an early-stage chatbot prototype. The Groq API integration is well-implemented, streaming works correctly, and the Streamlit interface provides a professional user experience.

However, **2 Critical security vulnerabilities** were identified (missing `.gitignore` and absence of prompt injection defenses), along with **3 High severity bugs** related to input validation, rate limit handling, and unbounded history growth. These issues must be resolved before production deployment.

**Overall QA Verdict: CONDITIONAL PASS** — suitable for development/demo use; requires remediation before production.

---

## 2. Test Coverage Summary

| Test Category       | Cases | PASS | PARTIAL | FAIL | Pass Rate |
|---------------------|-------|------|---------|------|-----------|
| Functional Testing  | 10    | 10   | 0       | 0    | 100%      |
| UI Testing          | 13    | 11   | 1       | 1    | 84.6%     |
| API Testing         | 10    | 8    | 2       | 0    | 80%       |
| Negative Testing    | 11    | 7    | 2       | 3    | 63.6%     |
| Security Testing    | 9     | 5    | 2       | 2    | 55.6%     |
| Performance Testing | 10    | 8    | 2       | 0    | 80%       |
| **TOTAL**           | **63**| **49**| **9** | **6**| **77.8%** |

---

## 3. Bug Statistics

### Bugs by Severity

| Severity | Count | Bugs |
|----------|-------|------|
| 🔴 Critical | 2 | Bug-001 (missing .gitignore), ST-005 (prompt injection) |
| 🟠 High | 3 | Bug-002 (no input validation), Bug-004 (rate limit), Bug-005 (history growth) |
| 🟡 Medium | 3 | Bug-003 (dark mode CSS), Race condition, TC-A-010 (history token growth) |
| 🟢 Low | 2 | External icon dependency, Mobile sidebar overlap |
| **Total** | **10** | |

### Bugs by Component

| Component | Bug Count |
|-----------|-----------|
| `llm.py` | 3 (validation, rate limit, history) |
| `app.py` | 2 (dark mode, race condition) |
| Repository Config | 1 (.gitignore) |
| System Prompt | 1 (injection defense) |
| UI/UX | 2 (mobile, external icon) |
| Performance | 1 (history latency) |

---

## 4. Risk Assessment

| Risk | Likelihood | Impact | Level |
|------|------------|--------|-------|
| API key exposed via VCS | High | Critical | 🔴 **CRITICAL** |
| Prompt injection jailbreak | Medium | High | 🟠 **HIGH** |
| App crash from None/empty input | Medium | High | 🟠 **HIGH** |
| History overflow at 200+ turns | High | Medium | 🟠 **HIGH** |
| Rate limit failure UX | High | Medium | 🟡 **MEDIUM** |
| Dark mode unusable | Low | Low | 🟢 **LOW** |

---

## 5. Findings by Category

### ✅ What Works Well

- Core `LexaChatbot` class is well-structured with proper separation of concerns.
- Streaming implementation is correct and provides excellent UX.
- History rollback on API error prevents corrupted conversation state.
- Streamlit session state management is correctly implemented.
- System message filtering prevents system prompt exposure in UI.
- Error handling surfaces meaningful messages in both CLI and Streamlit.
- Groq API integration is fast (avg 0.92s TTFT) and reliable.
- XSS attack surface is minimal in Streamlit context.

### ❌ What Needs Improvement

- No `.gitignore` — critical security gap.
- No input validation in `send_message()` — edge case vulnerabilities.
- No rate limit error handling — poor UX on 429 errors.
- Prompt injection defenses not in system prompt — moderate risk.
- Unbounded history growth — performance and reliability risk.
- Dark mode CSS override — visual inconsistency.
- No retry logic on transient API failures.
- Model name not validated at startup.

---

## 6. Recommendations

### Immediate Actions (Before Any Public Share/Commit)

1. **Create `.gitignore`** and add `.env` — prevents API key exposure.
2. **Rotate API key** if `.env` was ever committed to VCS.

### Short-Term (Next Sprint)

3. **Add input validation** in `send_message()` and `send_message_stream()`.
4. **Handle `RateLimitError`** with user-friendly message.
5. **Implement history sliding window** (max 20 turns).
6. **Harden system prompt** with anti-injection clauses.

### Medium-Term (Next Release)

7. **Fix dark mode CSS** using Streamlit theming system.
8. **Add retry logic** with exponential backoff.
9. **Bundle bot icon** locally instead of CDN.
10. **Pin dependency versions** in `requirements.txt`.
11. **Add model validation** at startup.
12. **Add Reset confirmation dialog** to prevent accidental history loss.

---

## 7. QA Conclusion

**The Lexa Chatbot is a well-designed, functional prototype** demonstrating solid Python architecture and effective use of the Groq API. The core features work correctly, streaming performance is excellent, and the Streamlit UI provides a pleasant user experience.

The application is **ready for development and internal demo use** but requires the identified critical and high priority fixes before production deployment or public release.

**QA Sign-off:** Conditional Approval — Pending Bug-001 and Bug-002 resolution minimum.

---

*Report prepared by QA Engineering Team — 2025-07-01*
