---
name: explain-like-im-ten
description: Re-explain what was just said in plain language, as if to a smart ten-year-old.
disable-model-invocation: true
---

# Explain Like I'm Ten

The user invokes this when a message didn't land. Re-pitch **that** - the thing that lost them, which is usually bigger than the last message, so decide how far back to go.

The re-pitch, in the ELI10 register:

- Write for a smart ten-year-old: short declarative sentences, ASD-STE100 Simplified Technical English, one idea per sentence.
- **Add the premise that was missing** rather than only deleting words. Comprehension failed because context was absent, not because the message was long.
- Use the project's own vocabulary: the terms in `CONTEXT.md` and the conversation, not invented synonyms. Keep the technical terms that matter and explain each on first use.
- Concrete beats abstract: one small example outweighs a paragraph of definition.

## It's working if

- The re-pitch is shorter *and* clearer, not shorter and blunter.
- It adds the missing premise instead of only trimming.
- Project nouns come back; invented ones disappear.
- It can run twice in a row without degrading into terseness.
