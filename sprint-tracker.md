## Sprint Tracker — Check Writing Interactive

Link references: `projectplan.md`, `style-guide.md`

### How to use this document
- **Update cadence**: At least once per day during active sprints.
- **Status options**: Not Started, In Progress, Blocked, Complete.
- **Conventions**:
  - Keep items as checkboxes; check them off as done.
  - Record decisions and changes under Changelog.
  - Artifacts: link to PRs, screenshots, demos.

### Sprint process
- **Length**: 1 week per sprint (adjust if needed).
- **Stack**: Streamlit-only, no backend; no PII; no persistence beyond session.
- **Definition of Done** (per item):
  - Meets acceptance criteria.
  - Passes accessibility checks for keyboard and contrast.
  - Matches `style-guide.md` tokens (colors, typography, spacing).
  - No data persists after refresh/close.

## Roadmap Overview
- Sprint 0: Foundations and scaffolding
- Sprint 1: UI shell and Check component
- Sprint 2: “I do” guided walkthrough
- Sprint 3: “We do” semi-guided with inline correction
- Sprint 4: “You do” independent practice
- Sprint 5: Scenarios, Reset/Replay, and session behavior
- Sprint 6: Accessibility, style polish, and QA
- Sprint 7: Packaging and embedding

---

## Sprint 0 — Foundations and scaffolding
Dates: Start ____ / End ____

**Goals**
- Project bootstrap; visual tokens; Streamlit skeleton and global layout.

**Scope / Stories**
- Initialize repository and basic project structure.
- Define theme tokens from `style-guide.md` and load fonts.
- Implement global layout (header with logo placeholder, content container).

**Tasks**
- [x] Create `app.py` skeleton and run basic Streamlit app
- [x] Extract color and typography tokens from `style-guide.md`
- [ ] Load PT Sans (H1) and Montserrat (UI/body) font stacks
- [ ] Build header (logo placeholder left) and base page container
- [ ] Verify projector-friendly contrast and visible focus states

**Acceptance Criteria**
- [ ] Colors and typography match `style-guide.md`
- [ ] App loads in modern browsers; keyboard focus visible
- [ ] No persistence or external calls

**Risks / Notes**
- Font loading within Streamlit theming; verify fallbacks.

**Artifacts**
- Links to PRs, screenshots: ____

**Status**: In Progress
Owner: ____

---

## Sprint 1 — UI shell and Check component
Dates: Start ____ / End ____

**Goals**
- Build static UI for the check and controls.

**Scope / Stories**
- Reusable Check component (date, payee, numeric amount, amount in words, memo, signature).
- Controls: scenario picker, mode tabs (“I do”, “We do”, “You do”), Reset button.
- Base responsiveness and projector-friendly contrast.

**Tasks**
- [ ] Implement static Check layout with tokens
- [ ] Add scenario picker control
- [ ] Add mode tabs and wire tab state
- [ ] Add Reset button (no logic yet)
- [ ] Ensure responsive layout (≥320px without horizontal scroll)

**Acceptance Criteria**
- [ ] 4.5:1 contrast minimum
- [ ] Tabs fully keyboard navigable with correct roles
- [ ] Layout responsive on mobile/tablet/desktop

**Risks / Notes**
- Tab roles and state management in Streamlit components.

**Artifacts**
- Links: ____

**Status**: In Progress
Owner: ____

---

## Sprint 2 — “I do” guided walkthrough
Dates: Start ____ / End ____

**Goals**
- Automatic step-by-step fill with explanations.

**Scope / Stories**
- Scenario data model and step scripts; cache with `st.cache_data()`.
- Stepper/progress indicator; timed or click-through advance.
- Explanatory callouts per step; Replay.

**Tasks**
- [x] Define scenario schema and 1 example script
- [x] Implement cached scenario loader
- [x] Build progress/stepper with current step highlighting
- [x] Implement auto-fill click-through and explanations
- [x] Add Replay behavior resetting relevant state

**Acceptance Criteria**
- [ ] Progress reflects steps accurately
- [ ] Replay resets state and replays steps deterministically
- [ ] No persistence beyond browser session

**Risks / Notes**
- Timing vs. click-through behavior usability in classrooms.

**Artifacts**
- Links: ____

**Status**: Complete
Owner: ____

---

## Sprint 3 — “We do” semi-guided with inline correction
Dates: Start ____ / End ____

**Goals**
- Prompts/hints and immediate feedback per field.

**Scope / Stories**
- `st.form()` groups for fields with prompts and examples.
- Inline validation: payee match, date format, numeric amount, amount-in-words format.
- Error style per `style-guide.md` (#D32F2F), aria-describedby for messages.

**Tasks**
- [x] Build forms for date, payee, numeric, words, memo, signature
- [x] Implement validators for each field
- [x] Display validation messages inline with red icon/text
- [x] Ensure keyboard navigation and described-by associations

**Acceptance Criteria**
- [ ] Incorrect entries show red validations immediately
- [ ] Correct entries confirm inline; no blocking modals
- [ ] Fully keyboard accessible

**Risks / Notes**
- Amount-in-words normalization and matching.

**Artifacts**
- Links: ____

**Status**: Complete
Owner: ____

---

## Sprint 4 — “You do” independent practice
Dates: Start ____ / End ____

**Goals**
- Student fills the entire check with minimal prompting; inline correction remains.

**Scope / Stories**
- Single scenario prompt; all fields empty by default.
- Consolidated validation; unobtrusive inline corrections; optional “Check my work”.
- Optional completion state with summary of corrections.

**Tasks**
- [x] Implement independent mode with scenario prompt only
- [x] Reuse validators and unify error presentation
- [x] Add optional “Check my work” CTA
**Acceptance Criteria**
- [ ] All fields validated; minimal prompting
- [ ] Reset clears `st.session_state`
- [ ] Summary clearly communicates corrections
Owner: ____

**Status**: Complete
Owner: ____

**Acceptance Criteria**
- [ ] All fields validated; minimal prompting
- [ ] Reset clears `st.session_state`
- [ ] Summary clearly communicates corrections

**Risks / Notes**
- Balancing feedback density vs. independence.

**Artifacts**
- Links: ____

**Status**: Not Started
Owner: ____

---

## Sprint 5 — Scenarios, Reset/Replay, and session behavior
Dates: Start ____ / End ____

**Goals**
- Scenario breadth and robust state management.

**Scope / Stories**
- Author 3–5 scenarios (e.g., Plumbing Ink 123, rent, utilities, donation).
- Scenario switcher behavior across modes; Reset/Replay finalized.
- Verify tab close/refresh clears all data; no external calls or storage.

**Tasks**
- [x] Write and review 3–5 scenarios
- [x] Implement scenario switching with appropriate resets
- [x] Finalize Reset and Replay behaviors
- [ ] Confirm no data persists after tab close/refresh

**Acceptance Criteria**
- [ ] Switching scenarios resets fields appropriately per mode
- [ ] No PII stored; offline-friendly

**Risks / Notes**
- Consistency of resets across modes.

**Artifacts**
- Links: ____

**Status**: In Progress
Owner: ____

---

## Sprint 6 — Accessibility, style polish, and QA
Dates: Start ____ / End ____

**Goals**
- A11y compliance and visual refinements.

**Scope / Stories**
- Audit roles, labels, tab order, focus behavior; aria-* for tabs, forms, alerts.
- Visual QA: buttons, labels, spacing, tokens per `style-guide.md`.
- Cross-device/browser matrix smoke tests.

**Tasks**
- [x] Add aria-live status on validation feedback
- [x] Style buttons per style guide (bold, radius, padding)
- [ ] Perform accessibility audit and log issues
- [ ] Fix identified a11y issues (roles, labels, focus order)
- [ ] Polish visuals to match tokens and spacing
- [ ] Test on target browsers/devices and projector setups

**Acceptance Criteria**
- [ ] Meets WCAG contrast and keyboard standards
- [ ] No color/spec deviations from `style-guide.md`

**Risks / Notes**
- Projector contrast differences; validate in realistic setting.

**Artifacts**
- Links: ____

**Status**: Not Started
Owner: ____

---

## Sprint 7 — Packaging and embedding
Dates: Start ____ / End ____

**Goals**
- Deliver embeddable build and integration docs.

**Scope / Stories**
- Package Streamlit app for embedding on NGPF site.
- Provide embed instructions (HTML snippet, sizing, allowed origins) and performance checks.
- Final privacy review: confirm no analytics, cookies, or network calls.

**Tasks**
- [ ] Produce build artifact suitable for embedding
- [ ] Write embed guide (container size, theming, snippet)
- [ ] Run performance checks for load and interaction
- [ ] Conduct privacy review; verify no external calls

**Acceptance Criteria**
- [ ] Runs embedded without server-side dependencies
- [ ] Privacy and performance verified

**Risks / Notes**
- Streamlit embedding specifics; document any constraints.

**Artifacts**
- Links: ____

**Status**: Not Started
Owner: ____

---

## Backlog / Nice-to-haves
- Optional progress indicators per mode
- Theming switch for projector vs. normal
- Export to image/PDF locally (no server)

## Decisions Log
- ____

## Changelog
- ____


