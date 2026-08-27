# Sources - the reading behind the modules

One list for the whole set. Each entry says who the source is, why it's worth trusting, and
which modules lean on it. The modules themselves stay citation-free; claims marked "this has
been measured" trace back here.

## Anthropic (the maker of Claude)

- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) -
  what an "agent" actually is: the loop, defined. Backs: *The agentic loop*, *Deciding
  before building*.
- [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices) -
  official best practices for agentic coding; the give-the-agent-a-way-to-check-its-work
  advice comes from here. Backs: *The agentic loop*, *What the agent reads*, *Verifying
  agent work*.
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) -
  why the context window is a budget and what fills it. Backs: *The context window*, *What
  the agent reads*.
- [How Claude remembers your project](https://docs.claude.com/en/docs/claude-code/memory) -
  the instruction-file mechanics: what gets read, every session. Backs: *What the agent
  reads*.
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) -
  what delegation to subagents buys and costs, from production experience. Backs: *Handing
  work off*, *Many agents on one job*.
- [Beyond permission prompts: sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing) -
  containment instead of click-to-approve supervision. Backs: *Working unattended*.
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) -
  running agents beyond a sitting, and why harness rules go stale as models improve. Backs:
  *Working unattended*, *When rules expire*, *Many agents on one job*.

## Independent research

- [METR - the AI developer-productivity studies](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
  ([2026 follow-up](https://metr.org/blog/2026-02-24-uplift-update/)) - independent research
  lab; ran the controlled studies on whether AI actually makes developers faster. The
  measured gap between how fast developers *felt* and how fast they *were* comes from here.
  Backs: *Verifying agent work*.
- [Chroma - Context Rot](https://research.trychroma.com/context-rot) - the study behind
  "quality decays as the window fills". Backs: *The context window*.
- [Do unnecessary context files help?](https://arxiv.org/abs/2602.11988) - measured finding
  that surplus instruction files make tasks harder, not easier. Backs: *What the agent
  reads*.
- [DORA - State of AI-assisted Software Development](https://dora.dev/) - the largest
  ongoing survey of how AI changes real engineering teams. Backs: *Working as a team*.

## Practitioners

- [Simon Willison - Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/) -
  a veteran engineer's ongoing field guide to working with coding agents. Backs: *The
  agentic loop*, *Deciding before building*, *Handing work off*, *Verifying agent work*.
- [Matt Pocock](https://github.com/mattpocock/skills) - a working practitioner teaching agentic
  coding as an engineering discipline. A lot of the skills in this repo began as his, and some are
  our own ([ATTRIBUTION.md](../ATTRIBUTION.md) has the detail).
- [Google - engineering practices for code review](https://google.github.io/eng-practices/review/) -
  the review-culture baseline most teams start from. Backs: *Working as a team*.

## Other vendors

First-party engineering writing about a vendor's own system. Useful for what they measured; read
with the caution any first-party result deserves.

- [NVIDIA - AVO reaches 100% on ARC-AGI-3](https://developer.nvidia.com/blog/nvidia-avo-reaches-100-on-arc-agi-3-demonstrating-a-frontier-level-general-purpose-architecture-for-long-horizon-autonomous-agents/) -
  the harness, not the model: Claude Opus 5 went from a 30% baseline to solving all 183 levels of a
  long-horizon benchmark inside NVIDIA's agent architecture, with no change to the model itself.
  Backs: *The agentic loop*.
