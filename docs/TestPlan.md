# Test Plan — SH04-AI-Chatbot-LEXA (Lexa Customer Service Chatbot)

---

## Document Information

| Field              | Details                                      |
|--------------------|----------------------------------------------|
| **Project Name**   | SH04-AI-Chatbot-LEXA                         |
| **Document Title** | Test Plan                                    |
| **Version**        | 1.0.0                                        |
| **Prepared By**    | QA Engineering Team                          |
| **Date**           | 2025-07-01                                   |
| **Status**         | Approved                                     |
| **Classification** | Internal / Confidential                      |

---

## 1. Objectives

The primary objectives of this test plan are:

- Verify that the Lexa chatbot correctly initializes and communicates with the Groq Cloud API.
- Validate functional correctness across both the CLI (`main.py`) and Streamlit UI (`app.py`) interfaces.
- Ensure robust handling of edge cases, invalid inputs, and unexpected network conditions.
- Assess the security posture of the application, particularly regarding API key management and prompt injection risks.
- Evaluate performance under normal and stressed conditions (response latency, streaming throughput).
- Identify, document, and track all defects found during testing.
- Produce a complete set of QA deliverables that serve as a living reference for future development.

---

## 2. Scope

### 2.1 In Scope

| Area                     | Details                                                         |
|--------------------------|-----------------------------------------------------------------|
| Core LLM Module          | `llm.py` — `LexaChatbot` class, `send_message`, `send_message_stream`, `reset_chat` |
| CLI Interface            | `main.py` — input loop, exit handling, error display           |
| Streamlit UI             | `app.py` — layout, chat rendering, sidebar, session state      |
| API Integration          | Groq API connectivity, streaming, error propagation            |
| Environment Configuration| `.env` parsing, `GROQ_API_KEY` loading                         |
| Dependency Validation    | `requirements.txt` — groq, streamlit, python-dotenv            |
| Security                 | API key exposure, prompt injection, sensitive data leakage     |
| Performance              | Response latency, streaming speed, memory under repeated use   |

### 2.2 Out of Scope

- Backend infrastructure of Groq Cloud (third-party).
- Deployment pipelines, CI/CD, containerization.
- Database or persistent storage (not implemented).
- Authentication / user login (not implemented).
- Load balancing and horizontal scaling.

---

## 3. Environment

### 3.1 Software Requirements

| Component        | Version / Specification                  |
|------------------|------------------------------------------|
| Python           | 3.9+                                     |
| Streamlit        | Latest stable (≥ 1.30)                  |
| groq (SDK)       | Latest stable                            |
| python-dotenv    | Latest stable                            |
| OS               | Windows 10/11, macOS 13+, Ubuntu 22.04+ |
| Browser (UI)     | Chrome 120+, Firefox 121+, Edge 120+    |

### 3.2 Hardware Requirements

| Component | Minimum         | Recommended     |
|-----------|-----------------|-----------------|
| CPU       | 2 cores         | 4 cores         |
| RAM       | 4 GB            | 8 GB            |
| Network   | 10 Mbps         | 50 Mbps         |

### 3.3 Test Environment Setup

```
Project Root/
├── .env               ← Contains GROQ_API_KEY=<valid_key>
├── requirements.txt
├── llm.py
├── main.py
├── app.py
└── .venv/             ← Isolated virtual environment
```

---

## 4. Test Types

| Type                 | Description                                                          |
|----------------------|----------------------------------------------------------------------|
| Functional Testing   | Verify features work as specified                                    |
| UI Testing           | Validate Streamlit interface layout, components, responsiveness      |
| API Testing          | Test Groq API integration under valid and invalid conditions         |
| Negative Testing     | Test application behavior with invalid, malformed, or extreme inputs |
| Security Testing     | Assess vulnerabilities in key handling and data exposure             |
| Performance Testing  | Measure response time, latency, memory usage                         |

---

## 5. Test Strategy

### 5.1 Approach

Testing is conducted in a **black-box** and **grey-box** hybrid approach:
- **Black-box**: Tester interacts with CLI and Streamlit UI as an end user.
- **Grey-box**: Tester reviews source code to identify potential edge cases and security risks.

### 5.2 Testing Sequence

```
Phase 1: Environment Setup & Smoke Test
Phase 2: Functional Testing (CLI + UI)
Phase 3: UI Testing (Streamlit layout, components)
Phase 4: API Testing (valid / invalid / missing keys)
Phase 5: Negative Testing (bad inputs, injections)
Phase 6: Security Testing (key exposure, prompt injection)
Phase 7: Performance Testing (latency, streaming, memory)
Phase 8: Bug Reporting & Regression
```

### 5.3 Test Data

| Category         | Data                                                   |
|------------------|--------------------------------------------------------|
| Valid Input      | Normal Indonesian customer service questions           |
| Empty Input      | `""`, whitespace-only strings                          |
| Long Input       | Strings > 5,000 characters                            |
| Special Chars    | `!@#$%^&*()`, `<script>`, `'; DROP TABLE`             |
| Unicode          | Arabic, Chinese, emoji (🔥), mixed scripts             |
| Injection        | `Ignore all previous instructions and...`             |
| API Keys         | Valid, invalid format, empty, expired                  |

---

## 6. Entry Criteria

- [ ] All source files (`main.py`, `app.py`, `llm.py`) are present and syntactically valid.
- [ ] `requirements.txt` dependencies are installed in a virtual environment.
- [ ] A valid `GROQ_API_KEY` is configured in `.env`.
- [ ] Groq Cloud API is reachable from the test environment.
- [ ] Python version ≥ 3.9 is confirmed.
- [ ] Test environment is isolated from production.

---

## 7. Exit Criteria

- [ ] All 30+ planned test cases have been executed.
- [ ] All **Critical** and **High** severity bugs are resolved or formally accepted.
- [ ] Test pass rate ≥ 85%.
- [ ] All QA deliverables (TestCases, Bug Reports, Final Report) are complete.
- [ ] Security vulnerabilities classified as Critical are mitigated.
- [ ] Test Summary Report is reviewed and signed off.

---

## 8. Risks

| Risk ID | Risk Description                                     | Likelihood | Impact | Mitigation                                         |
|---------|------------------------------------------------------|------------|--------|----------------------------------------------------|
| R-001   | Groq API rate limit reached during testing           | Medium     | High   | Use test account with high quota; add delays       |
| R-002   | API key accidentally committed to version control    | High       | High   | Enforce `.gitignore` for `.env`; use secret scanning|
| R-003   | Model `openai/gpt-oss-120b` deprecated or renamed    | Medium     | High   | Parameterize model name; test fallback models      |
| R-004   | Groq API downtime during test sessions               | Low        | High   | Schedule testing during off-peak hours             |
| R-005   | Streamlit version incompatibility                    | Low        | Medium | Pin versions in `requirements.txt`                 |
| R-006   | Missing `.env` file in deployment causes silent fail | High       | High   | Add startup validation and clear error message     |
| R-007   | Chat history grows unbounded in long sessions        | Medium     | Medium | Implement history pruning; test with 100+ turns    |
| R-008   | Prompt injection leads to off-topic or harmful output| Medium     | High   | Add input sanitization layer                       |

---

## 9. Deliverables

| Deliverable                          | Location                              | Status      |
|--------------------------------------|---------------------------------------|-------------|
| Test Plan                            | `docs/TestPlan.md`                    | ✅ Complete |
| Test Cases                           | `tests/TestCases.md`                  | ✅ Complete |
| Functional Testing Report            | `tests/FunctionalTesting.md`          | ✅ Complete |
| UI Testing Report                    | `tests/UITesting.md`                  | ✅ Complete |
| API Testing Report                   | `tests/APITesting.md`                 | ✅ Complete |
| Negative Testing Report              | `tests/NegativeTesting.md`            | ✅ Complete |
| Security Testing Report              | `tests/SecurityTesting.md`            | ✅ Complete |
| Performance Testing Report           | `tests/PerformanceTesting.md`         | ✅ Complete |
| Bug Reports (001–005)                | `bug_reports/Bug00X.md`               | ✅ Complete |
| User Guide                           | `docs/UserGuide.md`                   | ✅ Complete |
| Installation Guide                   | `docs/InstallationGuide.md`           | ✅ Complete |
| Technical Documentation              | `docs/TechnicalDocumentation.md`      | ✅ Complete |
| QA Report                            | `reports/QA_Report.md`                | ✅ Complete |
| Test Summary                         | `reports/TestSummary.md`              | ✅ Complete |
| Final Report                         | `reports/FinalReport.md`              | ✅ Complete |

---

## 10. Approval

| Role               | Name              | Signature        | Date       |
|--------------------|-------------------|------------------|------------|
| QA Lead            | QA Engineering    | _(signed)_       | 2025-07-01 |
| Project Owner      | Development Team  | _(pending)_      | —          |
| Technical Reviewer | Senior Dev        | _(pending)_      | —          |

---

*Document prepared in accordance with IEEE 829 Standard for Software Test Documentation.*
