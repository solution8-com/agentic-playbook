# Attribution

The S8 Agentic Playbook skills collection is assembled from two excellent
MIT-licensed open-source skill libraries, plus skills written from scratch by
Solution8. We are grateful to the original authors. This collection is itself
MIT-licensed (see [LICENSE](LICENSE)).

Each vendored or adapted skill has been reshaped for this collection:
cross-references point only to other skills in this collection, house
conventions are applied, and dependencies on the original authors' personal
tooling have been removed so every skill stands on its own.

## Sources

- **`mattpocock/skills`** - Matt Pocock (MIT, (c) 2026).
  <https://github.com/mattpocock/skills>
- **`obra/superpowers`** - Jesse Vincent (MIT, (c) 2025).
  <https://github.com/obra/superpowers>

## Per-skill provenance

| Skill | Origin |
|---|---|
| `setup-skills` | Solution8 original |
| `setup-dev-repo` | Solution8 original |
| `update-skills` | Solution8 original |
| `wayfinder` | mattpocock/skills (`wayfinder`), vendored near-verbatim |
| `research` | mattpocock/skills (`research`), reshaped |
| `prototype` | mattpocock/skills (`prototype`, 3 files), vendored near-verbatim |
| `grill-me` | mattpocock/skills (`grill-me`, later `grilling`, + `domain-modeling`), reshaped into rounds |
| `to-spec` | mattpocock/skills (`to-prd`), renamed and reshaped |
| `visual-spec` | Solution8 original |
| `to-issues` | mattpocock/skills (`to-tickets`), reshaped |
| `start-dev` | Solution8 original |
| `pickup-issue` | Solution8 original |
| `writing-plan` | obra/superpowers (`writing-plans`), reshaped |
| `tdd` | **Merge** of mattpocock/skills (`tdd`) + obra/superpowers (`test-driven-development`), reshaped |
| `subagent-driven-development` | obra/superpowers (`subagent-driven-development`), vendored with references localized |
| `code-review` | mattpocock/skills (`code-review`) + obra/superpowers, reshaped |
| `close-issue` | Solution8 original |
| `start` | obra/superpowers, vendored near-verbatim |
| `update-docs` | mattpocock/skills (`handoff` lineage), fully rewritten |
| `systematic-debugging` | **Merge** of obra/superpowers (`systematic-debugging`) + mattpocock/skills (`diagnose`), reshaped |
| `improve-codebase-architecture` | mattpocock/skills (`improve-codebase-architecture`), reshaped |
| `writing-for-agents` | mattpocock/skills (`writing-for-agents`, 2 files), vendored; Solution8 house rules appended in `S8-RULES.md` |
| `wizard` | mattpocock/skills (`wizard`, incl. `template.sh`), vendored verbatim |
| `to-questionnaire` | mattpocock/skills, reshaped - output changed to a fillable Solution8 HTML questionnaire |
| `explain-like-im-ten` | mattpocock/skills (`wait-what`), renamed, ELI10 register |

A line-level audit (2026-08-07) traced every vendored or reshaped line in the
collection back to one of the two libraries above; everything else is
Solution8's own text.

## Upstream licenses

Both source libraries are MIT-licensed. Their notices are reproduced below as
required.

### mattpocock/skills

```
MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### obra/superpowers

```
MIT License

Copyright (c) 2025 Jesse Vincent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
