# Looping

## Problem

Complex or ambiguous tasks often fail in one pass. Looping (including controlled iteration / evaluator-optimizer style loops) adds repeated retrieval-generation cycles until stop criteria are met.

## Condition

Use this pattern when answers need progressive refinement, multi-hop exploration, or confidence-gated retries.
Do not use it when single-pass quality is already sufficient or strict latency budgets prohibit iteration.

Typical fit:
- Multi-hop technical Q&A
- Report drafting with iterative evidence gathering
- Agent flows with judge-based refinement
- Agent engineering/coding tasks that improve through repeated task-run-review cycles

## Solution

Implement an explicit control loop:
1. Generate an initial answer/plan.
2. Evaluate quality/confidence/coverage.
3. If below threshold, refine query and retrieve more evidence.
4. Regenerate or patch answer.
5. Stop when criteria are met (quality threshold or max iterations).

```text
┌──────────────┐    ┌─────────────────┐    ┌────────────────┐
│ Start Query  │ -> │ Generate Draft  │ -> │ Evaluate Judge │
└──────────────┘    └─────────────────┘    └───────┬────────┘
                                                    │
                                  ┌─────────────────┴────────────────┐
                                  │                                  │
                     needs more evidence                    good enough / max iters
                                  │                                  │
                                  v                                  v
                        ┌───────────────────┐              ┌────────────────┐
                        │ Retrieve + Refine │              │ Final Answer   │
                        └─────────┬─────────┘              └────────────────┘
                                  │
                                  └------------------------> Generate Draft
```

Subtypes:
- Iterative retrieval loop
- Recursive decomposition loop
- Adaptive retrieval triggered by uncertainty
- Ralph loop (agent engineering/coding): run one scoped coding task, persist artifacts (code/tests/notes), start the next loop with fresh context, and repeat until acceptance criteria are met

## Example

Compliance Q&A:
1. Draft answer from current corpus.
2. Judge flags missing regional regulation coverage.
3. Retrieve region-specific policies and update answer.
4. Repeat until coverage checklist passes or max 3 cycles reached.

Agent engineering (Ralph-style loop):
1. Agent takes one narrowly scoped coding task from a queue.
2. It implements, runs checks/tests, and commits or records artifacts.
3. A reviewer/judge step decides pass/fail against task criteria.
4. If not done, create the next scoped task and run another fresh loop.

## Tradeoffs

- Gain: improved completeness on hard tasks.
- Cost: higher token/retrieval spend and longer latency.

## Failure Modes

- Infinite/near-infinite loops without hard stop rules.
- Judge module accepting low-quality answers too early.
- Iterations amplifying earlier mistakes.

## References

- Anthropic: Building Effective Agents (evaluator-optimizer loop) - https://www.anthropic.com/engineering/building-effective-agents
- FLARE: Active Retrieval Augmented Generation, 2023 - https://arxiv.org/abs/2305.06983
- Self-Refine, 2023 - https://arxiv.org/abs/2303.17651
- ReAct: Synergizing Reasoning and Acting in Language Models, 2022 - https://arxiv.org/abs/2210.03629
- Letta documentation: Ralph loop (iterative completion loop) - https://docs.letta.com/guides/agents/multi-agentic-systems/ralph-loop
- Geoffrey Huntley: The Ralph loop (fresh-session coding loop concept) - https://ghuntley.com/ralph/
- Snarktank/ai-dev-tasks: reference implementation inspired by the Ralph loop - https://github.com/snarktank/ai-dev-tasks
