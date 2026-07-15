# Knowledge Base & Documentation Humanization Patterns

Supplement to existing humanizer skills. Covers AI patterns specific to
knowledge base articles, API docs, user manuals, FAQs, and technical
documentation (Chinese + English).

Draws on shuorenhua's `docs` scene as base, adds depth for KB-specific
and manual-specific patterns.

## Positive Style Guide

Good KB/documentation prose is:
- **Scannable** — readers hunt for answers; structure serves lookup, not narrative
- **Precise** — every statement is testable; no vague guarantees
- **Neutral** — no marketing voice, no "we're excited to announce" in docs
- **Consistent** — same term for same concept across all articles
- **Self-contained** — each article can stand alone (readers arrive via search)

## AI Patterns

### D1: Article-Beginning Context Dump

AI opens every KB article with a 3-sentence context paragraph that search-
landing readers already know.

**Pattern:**
- "The X feature allows users to manage their Y settings. This article
  explains how to configure Z. Before starting, make sure you have admin
  access."
- → Reader who searched "how to configure Z" already knows this.

**Fix:** Open with the exact task + the minimum context needed for that task.
Move background to a collapsible "Overview" section.

---

### D2: Cross-Reference Overload

AI links to every related article, creating noise that distracts from the
current task.

**Pattern:**
- "For more information, see: [A], [B], [C], [D], [E]" at the end of every
  section
- Inline links on every other sentence

**Fix:** Max 3 "See also" links per article. Group by relevance. Inline links
only when the reader genuinely needs the linked info to understand the
current sentence.

---

### D3: FAQ Question AI-isms

AI-generated FAQs have telltale patterns.

**Patterns:**
- Questions are too generic: "What is X?" (should be the specific thing
  users actually ask)
- Answers are too long (FAQ answers should be 1-3 sentences)
- Every question follows the same structure

**Fix:** Use real user questions from support tickets. 1-3 sentence answers.
Vary question format (what/how/why/when).

---

### D4: API Doc Parameter Padding

AI generates parameter descriptions that restate the parameter name
without adding information.

**Pattern:**
- `timeout` — "The timeout value in milliseconds"
- `retries` — "Number of retry attempts"
- → Every parameter gets the same template: "The [param-name]"

**Fix:** Describe what the parameter DOES, not what its name says:
- `timeout` — "Maximum time to wait before failing the request"
- `retries` — "How many times to reattempt on 5xx errors"

---

### D5: Example Over-Fitting

AI examples are too clean: they show only the happy path, never the error
cases or edge conditions.

**Pattern:**
- API example shows a successful response but never error responses
- Config example shows default values but never explains what happens
  if a value is missing

**Fix:** Every major example should show:
1. The happy path
2. At least one error/edge case
3. What to do when it fails

---

### D6: Procedure Voice Confusion

AI mixes instructional voice ("you") with descriptive voice ("the system")
in the same procedure, causing reader confusion.

**Pattern:**
- "First, you navigate to Settings. The system will display the config
  page. Then, you should enter your API key." — switches between
  instruction and description mid-stream

**Fix:** Pick ONE voice per procedure:
- **Imperative (recommended for most docs):** "1. Go to Settings.
  2. Enter your API key. 3. Click Save."
- **Descriptive:** "When the user navigates to Settings, the system
  displays the config page. The user can then enter their API key."

---

### D7: KB Article Voice Drift

AI writes each KB article in isolation, causing voice inconsistency
across the knowledge base.

**Pattern:**
- Article A: "You can configure this in Settings"
- Article B: "The configuration can be performed in the Settings panel"
- Article C: "Navigate to Settings to configure"

**Fix:** If rewriting part of a KB, check 2-3 existing articles. Match
their voice. Common dimensions: active vs passive, "you" vs "the user",
contractions allowed or not.

---

### D8: Troubleshooting Section AI-isms

AI troubleshooting sections are too structured and miss the real world.

**Patterns:**
- Every error has exactly one cause and one fix
- "If the problem persists, contact support" — the universal cop-out
- No diagnosis steps, just "fix: do X"

**Fix:** Include:
1. How to verify the cause (diagnosis command, log check)
2. The actual fix
3. How to verify the fix worked
4. When to escalate

---

### D9: User Manual Noun-Stacking

AI generates noun stacks (long chains of nouns modifying a head noun)
that are grammatically valid but hard to parse.

**Pattern:**
- "The server-side data processing pipeline configuration module"
- "用户权限管理界面配置选项"

**Fix:** Break noun stacks: use prepositions, relative clauses, or split
into two sentences:
- "The configuration module for the data processing pipeline on the
  server side"
- "配置选项位于用户权限管理界面中"

---

### D10: Release Note Formula

AI writes release notes that all follow the same template, blurring
the significance of each change.

**Pattern:**
- "Added: New feature X" — for every item regardless of impact
- "Fixed: Bug Y" — no context on what was broken
- Every item is the same length and structure

**Fix** (extends shuorenhua's release-note scene pack):
- Distinguish: **major** (needs migration/attention) vs **minor** (transparent)
- For major changes: add migration note or impact description
- For fixes: state what broke, the symptom, and the fix
- Vary item format: some short, some with sub-items

---

### D11: Chinese Technical Documentation Patterns

AI-generated Chinese technical docs have specific patterns not covered
by general humanizers.

**Chinese triggers:**
- 过度使用"您可以"（every step starts with "您可以"）
- 操作步骤间的"从而"过渡
- "需要注意的是"在每个关键步骤前
- "请确保"堆叠（3+次/文）

**Fix:**
- "您可以" → 直接使用祈使句
- "从而" → 删除或用逗号连接
- "需要注意的是" → 每篇文章≤1次，仅用于易错步骤
- "请确保" → 每篇文章≤2次，仅用于不可逆操作

---

## Quality Metrics

| Dimension | Criteria |
|-----------|----------|
| **Task-completion rate** | Can a user complete the task by following the doc alone? |
| **Scannability** | Headers, lists, and bold serve lookup, not narrative. |
| **Consistency** | Voice and terminology match existing docs in the same KB. |
| **Precision** | Every statement is testable. No vague guarantees. |
| **Troubleshooting quality** | Error cases include diagnosis + verification, not just "contact support". |

## Scene Differentiation

| Scene | Default Gear | Key Difference |
|-------|-------------|----------------|
| **API reference** | minimal | Max precision. No narrative. Every param has a real description. |
| **User manual** | standard | More explanatory. Procedures in imperative voice. |
| **FAQ** | standard + bounded | Real questions, 1-3 sentence answers. |
| **Release notes** | minimal | Impact-first. Distinguish major vs minor. |
| **Troubleshooting** | standard | Include diagnosis, fix, verification, escalation. |

## References

- `skills/shuorenhua/` — shuorenhua's `docs` scene and scene packs
  (README, release-note, issue-reply)
- This module extends shuorenhua — do not duplicate what it already covers.
