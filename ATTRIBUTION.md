# Attribution

> Most of this is Matt Pocock's work. Here is exactly which parts.

The S8 Agentic Playbook is a **curated** collection. Most of it is Matt Pocock's
work, vendored under MIT with small or no changes. A handful of skills are
Solution8's own. We are grateful to the original authors, and we would rather
say plainly what we took than imply we wrote it. This collection is itself
MIT-licensed (see [LICENSE](LICENSE)).

Skills marked **verbatim** below are byte-identical to upstream. The one
set-wide exception: Matt ships Codex sidecar YAMLs in some skills' `agents/`
directories, which we do not adopt and strip on vendoring.

Exactly what changed in each tweaked skill is recorded in
[CATALOG.md](CATALOG.md), along with the upstream commit we are pinned to.

## Sources

- **`mattpocock/skills`** - Matt Pocock (MIT, (c) 2026).
  <https://github.com/mattpocock/skills>
- **`obra/superpowers`** - Jesse Vincent (MIT, (c) 2025).
  <https://github.com/obra/superpowers>

## Per-skill provenance

| Skill | Origin |
|---|---|
| `onboarding` | Solution8 original |
| `setup-repo` | Solution8 original |
| `grill-me` | mattpocock/skills (`grill-me` + `grilling`), merged into one file |
| `to-spec` | mattpocock/skills (`to-spec`), tweaked |
| `to-issues` | mattpocock/skills (`to-tickets`), renamed and tweaked |
| `pickup-issue` | Solution8 original |
| `implement` | mattpocock/skills (`implement`), tweaked |
| `wayfinder` | mattpocock/skills (`wayfinder`), tweaked |
| `prototype` | mattpocock/skills (`prototype`), verbatim |
| `research` | mattpocock/skills (`research`), verbatim |
| `visual-spec` | Solution8 original |
| `improve-codebase-architecture` | mattpocock/skills (`improve-codebase-architecture`), tweaked |
| `diagnosing-bugs` | mattpocock/skills (`diagnosing-bugs`), verbatim |
| `wait-what` | mattpocock/skills (`wait-what`), tweaked |
| `verify-feature` | Solution8 original |
| `review-suite` | Solution8 original |
| `suggest` | Solution8 original |
| `wizard` | mattpocock/skills (`wizard`), verbatim |
| `to-questionnaire` | mattpocock/skills (`to-questionnaire`), verbatim |
| `handoff` | mattpocock/skills (`handoff`), tweaked |
| `tdd` | mattpocock/skills (`tdd`), tweaked |

A line-level audit (2026-08-07) traced every vendored or reshaped line in the
collection back to one of the two libraries above; everything else is
Solution8's own text. The 2026-08-14 rescope replaced most reshaped forks with
verbatim upstream copies, which narrows what we claim as ours.

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
