# Code-t-Word Standard (KJV)

## What Code-t-Word is
Code-t-Word (CTW) is a lightweight documentation and commenting pattern that ties engineering intent to concise Scripture references.

It is designed to be:
- **Consistent**: same format in every language.
- **Low-conflict**: short, placement-aware, and non-intrusive.
- **Reviewable**: clear intent line tied to behavior, not theology debates.

Default translation: **KJV**.

## Rules of engagement

### 1) Required tag and structure
Use `CTW:` and keep each insertion to **max 3 lines total**:

1. `CTW: <Book Chapter:Verse> — “<short excerpt>”`
2. `Intent: <1 sentence tying verse to code behavior>`
3. Optional: `Theme: <one word>`

### 2) Placement rules
- Preferred locations:
  - top-of-file module docstring/header
  - above major classes/functions
- Avoid placing CTW blocks:
  - inside tight loops
  - on every helper
  - repeatedly in the same file without clear need

### 3) Scope and frequency
- Baseline: **1 CTW per file**.
- Optional: add one more only for a major class/module boundary.

### 4) Quoting rules
- KJV wording for excerpts.
- Keep excerpts short (phrase-level preferred).
- If quote length is awkward, use reference-only.

### 5) Tone and intent
- Intent line must describe software behavior (validation, safety, truthfulness, reliability, stewardship).
- Keep neutral and professional.

## Examples

### Python
```python
"""
CTW: Proverbs 12:22 — “lying lips are abomination to the LORD”
Intent: Ensure config validation rejects false or malformed inputs early.
Theme: Truth
"""
```

### JavaScript
```js
// CTW: 1 Corinthians 14:40 — “Let all things be done decently and in order.”
// Intent: Keep command routing deterministic and explicit for maintainability.
// Theme: Order
```

### TypeScript
```ts
/**
 * CTW: James 1:5 — “If any of you lack wisdom, let him ask of God”
 * Intent: Favor explicit typing and safe defaults when behavior could be ambiguous.
 * Theme: Wisdom
 */
```

### README
```md
> CTW: Colossians 3:23 — “whatsoever ye do, do it heartily”
> Intent: Build this project with diligence and high workmanship standards.
> Theme: Workmanship
```
