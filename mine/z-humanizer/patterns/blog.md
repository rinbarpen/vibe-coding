# Blog & Personal Writing Humanization Patterns

Supplement to existing humanizer skills. Covers AI patterns specific to
personal blogs, opinion pieces, thought leadership, and platform-native
writing (Chinese + English).

Applies the "Soul/Personality" concept from blader/humanizer as structured,
actionable rules rather than general advice.

## Positive Style Guide

Good blog prose is:
- **Opinionated** — takes a position, doesn't just survey options
- **Specific** — grounded in personal experience, not abstract observation
- **Rhythmic** — sentence length varies; short hits mix with longer builds
- **Imperfect** — allows digressions, asides, self-corrections, humor
- **Reader-aware** — written FOR a specific audience, not "general readers"

## AI Patterns

### B1: Synthesized Authority (AI has no personal experience)

AI generates claims that sound authoritative but are synthesized from
training data, not lived experience. This produces a "Wikipedia voice"
that lacks personal stakes.

**Pattern:**
- "In my experience, agile teams perform better" — AI has no team
  experience
- "I've found that writing daily improves clarity" — AI has never written
  daily
- "很多开发者会犯这个错误" — no actual developer was consulted

**Fix:** Ask: "Did I actually experience this?" If no, the options are:
(a) If the opinion is yours (user's), ground it in a specific anecdote
(b) If it's general knowledge, drop the "in my experience" framing
(c) If you're summarizing research, cite the source

---

### B2: Uniform Sentence Architecture

AI defaults to subject-verb-object with consistent cadence, producing
prose that reads smoothly but monotonously.

**Pattern:**
- Most sentences: 15-25 words, subject first, one clause
- Little variety in opening words (every sentence starts with a noun
  or "The"/"A")
- No fragments, no one-word sentences, no colons mid-sentence

**Fix** (per 100 words of blog text):
- Vary sentence openings: adverb, conjunction, comma phrase, question
- Add 1-2 short sentences (3-8 words) for punch
- Allow 1 fragment for style (only where intentional)
- Mix: sentence that opens with "-ing" phrase, "Because...", or a colon

---

### B3: Opinion Aversion

AI hedges opinions with qualifiers, framing everything as one reasonable
view among many.

**Pattern:**
- "X is one approach that some teams find useful"
- "It could be argued that Y matters more than Z"
- "可能有人认为……但另一部分人觉得……"

**Fix:** Take a position. If you believe X, say "X works because..."
If there's a valid counterargument, address it directly ("Some will say Y,
but here's why X wins in this case").

---

### B4: Platform-Native Voice Erasure

AI writes in the same voice regardless of platform, losing the conventions
that make content feel native.

**Chinese platform differences:**
- **知乎:** Analytical, skeptical, evidence-heavy. Readers expect arguments.
- **公众号:** Narrative, personal, emotional arc. Readers expect stories.
- **小红书:** Direct, experiential, "I tried this and here's what happened."
- **微博:** Punchy, opinionated, maximum impact per character.

**English platform differences:**
- **Medium:** Reflective, personal insight, longer narrative arcs.
- **Substack:** Letter-like, direct address, conversational authority.
- **LinkedIn:** Professional but personal, "here's what I learned."
- **X/ Twitter:** Brutally concise, one clear take, room for replies.

**Fix:** Before rewriting, confirm platform. Then apply platform voice:
- Shift sentence length, paragraph structure, and evidence style
- Match the platform's typical reading mode (scrolling vs. dedicated reading)

---

### B5: Perfect Paragraphs

AI generates paragraphs that are all 3-5 sentences, each with a clear
topic sentence and a concluding wrap-up.

**Pattern:**
- Every paragraph: topic sentence → 2-3 supporting → conclusion
- No one-sentence paragraphs (punch lines, transitions, questions)
- No 8+ sentence paragraphs (deep dives, list-like content)

**Fix:** Vary paragraph length and structure:
- Some: 1 sentence for impact
- Some: 6-8 sentences for a deep point
- Some: a question that transitions
- Let some paragraphs end abruptly (on a detail, a quote, a question)

---

### B6: "As an AI" / Self-Awareness Artifacts

AI-generated text sometimes references its own nature, breaking the
reader's suspension of disbelief.

**Pattern:**
- "As a language model, I don't have personal experiences, but..."
- "While I can't browse the internet, I can tell you that..."
- "截至我的训练数据截止日期……"

**Fix:** Delete entirely. If the content needs a disclaimer, put it in a
footnote or separate meta-note — not inline.

---

### B7: Hook and Title AI-isms

AI titles and opening hooks follow predictable patterns that signal
"generated content" to experienced readers.

**Title patterns:**
- "The Ultimate Guide to X"
- "X: A Comprehensive Overview"
- "Why You Should (or Shouldn't) Do X"
- "X in 2025/2026: Everything You Need to Know"
- 数字列表 + 形容词: "7个让你效率翻倍的方法"

**Hook patterns:**
- "In today's fast-paced world..."
- "Have you ever wondered why..."
- "Let's face it: X is hard"
- "作为一个在X领域深耕多年的从业者……"

**Fix:**
- Titles: 1 specific claim, no cliche frames, max 15 words (EN) / 20 chars (CN)
- Hooks: Start with a specific moment, a surprising fact, or a direct
  challenge. No preamble.

---

### B8: Transition Verbosity

AI over-uses explicit transition words, making the writing feel like
a guided tour rather than natural thought.

**Pattern:**
- "Moreover, ... Furthermore, ... In addition, ..."
- "然而……，另一方面……，与此同时……"
- "First, ... Second, ... Third, ... Finally, ..."

**Fix:** Let content logic carry transitions. Delete 60% of explicit
transition words. Use: one-word transitions ("But", "Yet", "So"),
paragraph breaks as transitions, or rhetorical questions.

---

### B9: Self-Contained Explanation (Explaining the Obvious)

AI explains concepts that the target audience already knows, padding
the post with unnecessary context.

**Pattern:**
- In a post for senior engineers: "Git is a distributed version control
  system that tracks changes in source code"
- In a post for Chinese developers: "Python是一种解释型、面向对象的
  高级编程语言"

**Fix:** For each explanation, ask: "Does my target reader need this?"
If they're in the audience, they already know. Delete or link to external
resource.

---

### B10: Conclusion Template

AI blog conclusions follow a predictable arc: summarize → state importance →
future-looking statement.

**Pattern:**
- "In conclusion, we've covered X, Y, and Z. Each is important for...
  As the field evolves, we can expect..."
- "综上所述，X、Y、Z三个方面对未来发展具有重要意义。我们期待……"

**Fix:** Vary conclusion type:
- **Call to action:** "Try this today. Here's the first step."
- **Open question:** "What do you think? I'm still deciding."
- **Prediction:** "I think X will change this in 2 years. Here's why."
- **Personal note:** "I started this project expecting A, but found B."
- **No conclusion:** End on a quote, a detail, or mid-argument

---

### B11: Cross-Platform Repurposing Artifacts

When AI repurposes content from one platform to another, it leaves traces.

**Patterns:**
- LinkedIn post restructured as blog: has thread-like numbered points
- Blog compressed to tweet thread: still reads like paragraphs, not tweets
- Zhihu answer → 公众号: retains debate-like framing unsuitable for narrative

**Fix:** Rewrite for the target platform from scratch using the source's
core insight. Don't mechanically restructure.

---

## Voice Calibration

When the user provides a writing sample:

1. **Sentence length profile:** Average words/sentence? Variance?
2. **Opening words:** What % start with "But", "And", "The", a verb?
3. **Paragraph density:** What's the typical paragraph length? Do they
   use one-sentence paragraphs?
4. **Punctuation habits:** Em-dashes? Colons? Semicolons? Frequencies.
5. **Register:** Formal, conversational, technical, literary?
   Contractions? First-person?
6. **Recurring phrasings:** Specific pet phrases, transition preferences,
   sentence-ending patterns.

Then match in rewrite. If no sample provided, default to:
- Moderate sentence length (12-20 words EN, 20-40 chars CN)
- 20% of paragraphs are 1 sentence
- Varied openings: ~30% "But/And/So", ~30% noun, ~20% adverbial, ~20% other
- 1-2 em-dashes or colons per 200 words (blog has more flexibility than
  academic/patent)

## Quality Metrics

| Dimension | Criteria |
|-----------|----------|
| **Specificity** | Does it contain personal experience or unique observation? |
| **Voice** | Could this have been written by any AI, or does it sound like one person? |
| **Pacing** | Sentence length varies. Paragraphs vary. Not monotonous. |
| **Opinion** | Does it take a position, or just survey both sides? |
| **Platform-fit** | Would this feel native on the target platform? |

## Scene Differentiation

| Platform | Key Difference |
|----------|---------------|
| **知乎 (Zhihu)** | Evidence-heavy, skeptical audience. Every opinion needs support. |
| **公众号 (WeChat)** | Narrative-driven. Strong emotional or intellectual arc. |
| **小红书 (XHS)** | Direct, experiential. "I tried X → here's what happened." |
| **微博 (Weibo)** | Punchy. One clear take in minimal characters. |
| **Medium** | Reflective. Longer narrative. Personal insight. |
| **Substack** | Letter voice. Direct "you" address. Authoritative but personal. |
| **LinkedIn** | Professional lesson learned. Career/industry specific. |
| **X / Twitter** | Brutal concision. One clear take. Room for reply thread. |

## References

- `skills/humanizer/SKILL.md` — "Soul/Personality" section (lines ~490-540),
  Voice Calibration section, "Signs of Human Writing"
- `skills/de-ai-prompt-enhancer/good-writing/SKILL.md` — Author style
  replication patterns
