---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a cited Markdown file in the repo, run as a background agent so the main conversation keeps moving. Use when the user wants a topic researched, docs or API facts verified, or reading legwork delegated instead of guessed at.
---

# Research

## Overview

Answer a factual question by chasing it back to the source that actually owns the claim, rather than repeating a secondary write-up of it. Delegate the reading to a background agent so the main conversation isn't blocked waiting on it.

## Process

1. **Spin up a background agent** to do the digging, so the main thread can keep working while it reads.
2. **Chase primary sources.** Official docs, source code, specs, first-party APIs: not blog posts or summaries about them, unless a primary source genuinely doesn't exist. Follow every claim back to the source that owns it before trusting it.
3. **Write the findings to a single Markdown file**, citing each claim's source inline (a link or exact reference, not a vague "per the docs").
4. **Save it where the repo already keeps this kind of note.** Match the existing convention if one exists; if there isn't one yet, pick a sensible location under `docs/` and say where, so the next research pass has a convention to follow. If a caller named a location or branch, that wins.

## What good output looks like

- Every non-obvious claim has a citation next to it, not just a source list at the bottom.
- Contradictions between sources are called out, not silently resolved by picking one.
- The file states the question it was answering up top, so a reader doesn't have to reverse-engineer scope from the findings.

## When NOT to use this

For something the agent can verify directly in seconds (reading a local file, running a command), just do that: don't spin up a background research pass for questions the current session can answer itself.
