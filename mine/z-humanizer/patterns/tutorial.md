# Tutorial Humanization Patterns

Supplement to existing humanizer skills. Covers AI patterns specific to
tutorials, guides, how-tos, and learning content (Chinese + English).

## Positive Style Guide

Good tutorial prose is:
- **Guiding, not dictating** — explains WHY a step matters, not just WHAT to do
- **Imperfect** — includes common mistakes, edge cases, and what to watch for
- **Paced** — alternates explanation with action; doesn't dump all info upfront
- **Respectful** — doesn't over-explain obvious concepts or condescend
- **Scaffolded** — builds complexity gradually; each section assumes only
  what previous sections taught

## AI Patterns

### T1: Perfect Step Syndrome

AI generates steps that always work perfectly on first try, omitting the
common errors and gotchas that real learners encounter.

**Pattern:**
- "运行 `npm install`，然后启动服务器" — never mentions permission errors,
  port conflicts, or missing dependencies
- "Click Save. The system will update automatically" — never mentions what
  to do if it doesn't update

**Fix:** Add a "watch for" note after at least every 3rd step:
- "If you see EACCES errors, prepend with `sudo` or fix npm permissions"
- "如果端口被占用，使用 `lsof -i:3000` 查看并更换端口"

**Hard constraint:** A tutorial with 5+ steps must have at least 2
troubleshooting callouts for common failure points.

---

### T2: Perfect Example Problem

AI examples are too clean — they demonstrate the concept without any of
the messy real-world complications.

**Pattern:**
- "Let's sort an array: `[3, 1, 4, 1, 5, 9]`" — never shows the type
  coercion edge case, the empty array, or the very large array
- Example input is always a perfect case that produces a clean output

**Fix:** Add at least one edge case per major example:
- "What happens when the array is empty? Try it:"
- "注意：如果输入包含 null，代码会报错。先加一个判空："

---

### T3: Information Dump Opening

AI opens tutorials with a definition paragraph that lists every concept
the tutorial will cover, overwhelming the reader before the first step.

**Pattern:**
- "React Hooks are functions that let you use state and other React features
  without writing a class. In this tutorial, we'll cover useState, useEffect,
  useContext, useReducer, useCallback, useMemo, useRef, and custom hooks."

**Fix:** Front-load only the minimal concept needed for Step 1. Introduce
each new concept at the moment it's first needed.

---

### T4: Symmetric Section Structure

AI makes every section the same length and structure, like an outline
expanded mechanically.

**Pattern:**
- Section 1: 3 paragraphs + code block
- Section 2: 3 paragraphs + code block
- Section 3: 3 paragraphs + code block
- Each section ends with a summary sentence

**Fix:** Vary section structure:
- Some sections: heavy on explanation, brief code
- Others: mostly code with minimal annotation
- Allow short transitional sections (1 paragraph, no code)

---

### T5: Missing Prerequisite Context

AI skips telling readers what they need to know before starting, or buries
it in a footnote.

**Pattern:**
- Jumps straight into advanced concepts without establishing baseline
- "First, install the CLI tool" — never says what OS is assumed, what
  version of Node/Python, or what prior knowledge is expected

**Fix:** After the title, include a 1-3 line "You'll need" section:
- "You'll need: Node.js 18+, npm 9+, and basic familiarity with the
  terminal."
- "前置要求：已安装 Python 3.10+，了解基本的 HTTP 概念。"

---

### T6: Recipe-Style (No Reasoning)

AI lists steps like a recipe: do X, then Y, then Z — without explaining
why each step matters.

**Pattern:**
- "Step 1: Create a file called server.js. Step 2: Add the express import.
  Step 3: Define a route." — never says WHY each step exists

**Fix:** After each step that introduces a new concept, add 1 sentence of
reasoning:
- "We isolate the config here so it's testable without loading the full app."

---

### T7: Over-Explained Simple Steps

AI explains trivial operations in the same detail as complex ones, wasting
the reader's attention.

**Pattern:**
- "Click the 'Create' button located at the top right of the navigation
  bar" — for a single obvious button
- "在终端中输入以下命令并按回车键执行" — before every single command

**Fix:** Use minimal instruction for obvious actions. Reserve full detail
for non-obvious, multi-step, or easily-confused operations.

---

### T8: Code-Output-Explanation Triplet Rigidity

Every code block is followed by its output, then an explanation of the
output — making the tutorial plodding and predictable.

**Pattern:**
```
// Code
console.log(hello)
// Output
hello
// Explanation
The console.log function prints the string "hello" to the console.
```

**Fix:** Vary the triplet:
- Sometimes: code + explanation (no output shown — trust reader to run it)
- Sometimes: code only (self-explanatory)
- Sometimes: show output only for surprising results
- Group 2-3 related code blocks before explaining

---

### T9: Artificial Summary Endings

Every section and the tutorial itself ends with a formulaic summary.

**Pattern:**
- "In this section, you learned how to..."
- "Congratulations! You've successfully built a..."
- "In conclusion, we have covered..."

**Fix:** End sections with a transition to what comes next, or a question
that leads into the next section. Delete "congratulations" openers.
Only summarize if the tutorial is >2000 words.

---

### T10: Authority and Prerequisite Avoidance

AI avoids saying "you should already know X" and tries to make every
tutorial self-contained, resulting in shallow coverage.

**Pattern:**
- Tries to teach recursion without assuming the reader knows function
  call stacks
- Explains basic syntax alongside advanced patterns in one tutorial

**Fix:** Be explicit about prerequisites. If a tutorial needs prior
knowledge, say so upfront. Don't pad the tutorial with review sections —
link to a prerequisite tutorial instead.

---

### T11: Exercise/Quiz AI-isms

AI-generated exercises and quizzes have distinctive patterns.

**Patterns:**
- Multiple choice options are obviously right or wrong
- Exercise difficulty doesn't ramp up
- "Think about what would happen if..." rhetorical questions
- Answer keys that say "The correct answer is A because..."

**Fix:**
- Make wrong options plausible (common misconceptions)
- Ramp: recall → apply → evaluate
- Replace rhetorical questions with actual coding challenges
- Answer keys: show the reasoning, not just "because"

---

### T12: Overly Perfect Code Examples

AI code examples never have bugs, never show the wrong way, and never
demonstrate debugging. This teaches rote copying, not understanding.

**Pattern:**
- Every code block compiles and runs correctly
- Never shows what a broken version looks like
- Never demonstrates the debugging process

**Fix:** In every major tutorial, add at least one "common mistake" variant
that shows the wrong code, what happens, and how to fix it.

---

## Quality Metrics

| Dimension | Criteria |
|-----------|----------|
| **Learnability** | Can a beginner with stated prerequisites complete it? |
| **Pacing** | Alternates action and explanation. Sections vary in length. |
| **Robustness** | Includes edge cases, errors, and troubleshooting. |
| **Respect** | Doesn't over-explain the obvious. Assumes intelligence. |

## Scene Differentiation

| Scene | Default Gear | Key Difference |
|-------|-------------|----------------|
| **Quickstart** | standard | Minimal explanation, get-user-running focus |
| **Full tutorial** | standard | Deeper reasoning, more edge cases |
| **Concept guide** | standard + bounded | No step-by-step, principle-first |
| **Exercise/workshop** | minimal | Exercise text should be concise, leave room for discovery |
