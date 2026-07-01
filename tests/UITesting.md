# UI Testing Report — SH04-AI-Chatbot-LEXA

**Project:** SH04-AI-Chatbot-LEXA  
**Version:** 1.0.0  
**Tester:** QA Engineering Team  
**Date:** 2025-07-01  
**Interface:** Streamlit Web UI (`app.py`)  
**URL:** `http://localhost:8501`

---

## 1. Overview

This document covers UI testing for the Lexa chatbot Streamlit interface. Tests include layout validation, chat components, sidebar behavior, button interactions, responsive design, dark mode compatibility, and broken UI scenarios.

---

## 2. Test Environment

| Item            | Value                          |
|-----------------|--------------------------------|
| Browser         | Google Chrome 124.0            |
| OS              | Windows 11 / Ubuntu 22.04      |
| Streamlit       | 1.32.0                         |
| Screen (Desktop)| 1920 × 1080 px                 |
| Screen (Mobile) | 375 × 812 px (DevTools)        |
| Theme           | Light (default) / Dark (toggle)|

---

## 3. Test Results

---

### UT-001 — Page Load & Title Verification

**Component:** Browser Tab  
**Test:** Verify page title and favicon on load.

**Steps:**
1. Run `streamlit run app.py`.
2. Browser auto-opens at `http://localhost:8501`.
3. Check browser tab title and icon.

**Expected:** Tab shows `"Lexa Chatbot - CS Assistant"` with 💬 emoji icon.  
**Actual:** ✅ Title and icon displayed correctly per `st.set_page_config()`.

**Tester Comment:** The favicon emoji (💬) renders in Chrome and Edge. Firefox may show a generic favicon — minor cross-browser cosmetic issue.  
**Result:** ✅ **PASS**

---

### UT-002 — Main Header Rendering

**Component:** `st.title()` / `st.caption()`  
**Test:** Verify main page heading and subtitle.

**Steps:**
1. Open app.
2. Inspect page header area.

**Expected:** 
- Title: `"💬 Lexa Customer Service"`
- Caption: `"Asisten Customer Service Interaktif berbasis Groq API (gpt-oss-120b)"`
- Horizontal rule separator visible.

**Actual:** ✅ All three elements rendered correctly in centered layout.

**Tester Comment:** `layout="centered"` provides clean presentation on widescreen monitors. Text is crisp with custom Inter font applied via CSS.  
**Result:** ✅ **PASS**

---

### UT-003 — Chat Input Box

**Component:** `st.chat_input()`  
**Test:** Verify chat input is present, focusable, and has correct placeholder.

**Steps:**
1. Scroll to bottom of page.
2. Inspect chat input field.
3. Click on it.
4. Type a test message.

**Expected:** Input box fixed at bottom, placeholder = `"Ada yang bisa saya bantu hari ini?"`, accepts text.  
**Actual:** ✅ Input box present and functional. Placeholder text correct. Submits on Enter.

**Tester Comment:** Streamlit's `st.chat_input()` is sticky at the bottom — good UX. However, no character counter or max-length indicator is shown.  
**Result:** ✅ **PASS**

---

### UT-004 — Chat Message Bubbles

**Component:** `st.chat_message()`  
**Test:** Verify distinct visual rendering for user and assistant messages.

**Steps:**
1. Send `"Halo Lexa"`.
2. Observe chat rendering.

**Expected:**
- User message: appears in user-styled bubble (right-aligned in default Streamlit).
- Assistant message: appears in assistant-styled bubble with bot avatar.

**Actual:** ✅ Both bubbles rendered with distinct styling. Streamlit's default chat icons applied. Markdown in responses renders correctly (bold, lists).

**Tester Comment:** Markdown rendering in chat bubbles works well. Long responses scroll correctly within the chat area.  
**Result:** ✅ **PASS**

---

### UT-005 — Streaming Cursor (▌) Behavior

**Component:** `response_placeholder.markdown()`  
**Test:** Verify streaming cursor appears during response and disappears on completion.

**Steps:**
1. Send a message.
2. Observe assistant response rendering in real-time.

**Expected:** `▌` cursor visible while streaming. Removed from final rendered text.  
**Actual:** ✅ Cursor appears during token streaming, removed on completion. Gives a typewriter effect.

**Tester Comment:** This is an excellent UX detail. The cursor blinks naturally as tokens arrive. No flash or double-render observed.  
**Result:** ✅ **PASS**

---

### UT-006 — Sidebar — Layout & Content

**Component:** `st.sidebar`  
**Test:** Verify sidebar structure and elements.

**Steps:**
1. Open sidebar (click `>` arrow or it auto-opens).
2. Verify contents.

**Expected:**
- Bot icon image (from `img.icons8.com`)
- Title: `"Lexa CS Control Panel"`
- Description text visible
- Reset button present

**Actual:** ✅ All elements present. Bot icon loads from external URL.

**Tester Comment:** External image dependency (icons8.com) — if the URL becomes unavailable, icon will break. Recommend bundling the icon locally.  
**Result:** ✅ **PASS**

---

### UT-007 — Reset Button — Functionality

**Component:** `st.button("Reset Percakapan")`  
**Test:** Verify reset button clears chat history.

**Steps:**
1. Conduct a 3-turn conversation.
2. Click `"Reset Percakapan"`.
3. Observe chat area.

**Expected:** Chat history cleared; `st.rerun()` refreshes page with empty conversation.  
**Actual:** ✅ History cleared via `reset_chat()`; page reloads cleanly.

**Tester Comment:** Button click triggers immediate visual refresh. No confirmation dialog — accidental clicks will lose all history. A confirmation prompt would improve UX.  
**Result:** ✅ **PASS** *(UX improvement recommended)*

---

### UT-008 — Reset Button — Styling & Hover

**Component:** Custom CSS on `.stButton>button`  
**Test:** Verify button color and hover effect.

**Steps:**
1. Observe button default state.
2. Hover mouse over button.

**Expected:**
- Default: red background `#ef4444`, white text.
- Hover: darker red `#dc2626`.

**Actual:** ✅ CSS applied correctly. Color transition `0.3s` is smooth.

**Tester Comment:** The red button color is visually prominent and appropriate for a destructive action. Consistent with modern UI standards.  
**Result:** ✅ **PASS**

---

### UT-009 — Desktop Responsive Layout (1920×1080)

**Component:** Full page layout  
**Test:** Verify layout on standard desktop resolution.

**Steps:**
1. Open app on 1920×1080 display.
2. Inspect all elements.

**Expected:** Chat centered, all elements visible, no overflow or cut-off.  
**Actual:** ✅ `layout="centered"` constrains width appropriately. Comfortable reading width achieved.

**Tester Comment:** The centered layout works well on wide screens. White space on sides is a design choice — acceptable for a chat interface.  
**Result:** ✅ **PASS**

---

### UT-010 — Mobile Responsive Layout (375×812)

**Component:** Full page layout  
**Test:** Verify layout on mobile viewport using browser DevTools.

**Steps:**
1. Open Chrome DevTools → Device Toolbar → iPhone SE (375×812).
2. Inspect layout.

**Expected:** App adapts to mobile width; all elements accessible.  
**Actual:** ⚠️ Partial — chat input usable. Sidebar overlaps main content when open on very narrow screens. No dedicated mobile navigation.

**Tester Comment:** Streamlit is not a mobile-first framework. The sidebar behavior is problematic at 375px — it covers the chat area. Users must close it manually. Consider hiding sidebar content on mobile or making the bot icon collapsible.  
**Result:** ⚠️ **PARTIAL PASS**

---

### UT-011 — Dark Mode Compatibility

**Component:** Custom CSS + Streamlit theme  
**Test:** Verify UI in dark mode.

**Steps:**
1. Open Streamlit settings (hamburger menu → Settings).
2. Switch to Dark theme.
3. Inspect all elements.

**Expected:** UI adapts correctly; all text readable against dark backgrounds.  
**Actual:** ❌ Custom CSS `.main { background-color: #f8fafc; }` forces light background even in dark mode. White background + dark sidebar = visual inconsistency. Text colors may clash.

**Tester Comment:** This is a known Streamlit limitation when using custom CSS. The hardcoded `background-color` overrides the Streamlit dark theme. Recommend using CSS variables or conditional theming. **This is a confirmed bug (Bug-003).**  
**Result:** ❌ **FAIL**

---

### UT-012 — Error State UI (Invalid API Key)

**Component:** `st.error()` / `st.info()` / `st.stop()`  
**Test:** Verify graceful error display when chatbot fails to initialize.

**Steps:**
1. Set `GROQ_API_KEY=invalid` in `.env`.
2. Launch Streamlit.

**Expected:**
- Red error banner: "Gagal menginisialisasi Chatbot: ..."
- Blue info banner: guidance to check `.env`
- No chat input shown (app stopped)

**Actual:** ✅ Error banner and info banner displayed correctly. Chat input not rendered. Guidance is clear.

**Tester Comment:** Excellent defensive UI. Error is caught and displayed user-friendly. The `st.stop()` prevents a broken chat interface from rendering.  
**Result:** ✅ **PASS**

---

### UT-013 — System Message Filtering in Chat Display

**Component:** Chat history rendering loop  
**Test:** Verify system prompt is NOT shown in the chat UI.

**Steps:**
1. Open app with a fresh session.
2. Inspect all visible chat messages.

**Expected:** System prompt (`role: "system"`) is filtered out and not displayed.  
**Actual:** ✅ Code confirms: `if message["role"] == "system": continue` — system prompt correctly hidden.

**Tester Comment:** Good practice. Users should not see the system prompt as it could reveal internal instructions.  
**Result:** ✅ **PASS**

---

## 4. UI Testing Summary

| Test ID | Component                     | Result          |
|---------|-------------------------------|-----------------|
| UT-001  | Page Title & Icon             | ✅ PASS         |
| UT-002  | Main Header                   | ✅ PASS         |
| UT-003  | Chat Input Box                | ✅ PASS         |
| UT-004  | Chat Message Bubbles          | ✅ PASS         |
| UT-005  | Streaming Cursor              | ✅ PASS         |
| UT-006  | Sidebar Layout                | ✅ PASS         |
| UT-007  | Reset Button Functionality    | ✅ PASS         |
| UT-008  | Reset Button Styling          | ✅ PASS         |
| UT-009  | Desktop Responsive (1920px)   | ✅ PASS         |
| UT-010  | Mobile Responsive (375px)     | ⚠️ PARTIAL PASS |
| UT-011  | Dark Mode                     | ❌ FAIL         |
| UT-012  | Error State UI                | ✅ PASS         |
| UT-013  | System Message Filter         | ✅ PASS         |

**Total:** 13 | **PASS:** 11 | **PARTIAL:** 1 | **FAIL:** 1 | **Pass Rate:** 84.6%

---

## 5. Tester Recommendations

1. **Dark Mode Fix:** Use Streamlit's `st.get_option("theme.base")` or remove the hardcoded background-color to respect theme settings.
2. **Mobile Sidebar:** Add `st.sidebar.header()` collapse behavior or minimize the sidebar by default on narrow screens.
3. **Reset Confirmation:** Add a confirmation modal or `st.warning()` before executing reset to prevent accidental data loss.
4. **External Image:** Bundle the bot icon locally instead of linking to `img.icons8.com`.
5. **Character Counter:** Add a max-length indicator on the chat input to guide users.
