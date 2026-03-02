# Branching

## Problem

Single-path execution can miss coverage for broad or multi-faceted requests. Branching addresses this by running multiple paths in parallel so the system can explore different sub-queries, tools, or reasoning tracks.

## Condition

Use this pattern when one query benefits from parallel exploration.
Do not use it for narrowly scoped requests where one path is enough.

Typical fit:
- Broad research questions
- Multi-perspective summarization
- Creative ideation where multiple candidates are valuable

## Solution

Fan out work into parallel branches, then return branch outputs for later synthesis:
1. Split query into sub-queries or branch tasks.
2. Execute retrieval/generation per branch in parallel.
3. Return branch results and branch metadata (confidence/source).
4. Hand off outputs to a merge/fusion step (often the `fusion` pattern).

```text
                 ┌─────────────────────────────┐
                 │ Branch 1: Retrieve/Generate │
                 └──────────────┬──────────────┘
                                │
┌──────────────┐    ┌───────────▼───────────┐     ┌─────────────────┐
│ User Query   │ -> │ Split / Decompose     │ --> │ Merge Candidate │
└──────────────┘    └───────────┬───────────┘     └────────┬────────┘
                                │                          │
                 ┌──────────────▼──────────────┐           │
                 │ Branch 2: Retrieve/Generate │           │
                 └──────────────┬──────────────┘           │
                                │                          │
                 ┌──────────────▼──────────────┐           │
                 │ Branch N: Retrieve/Generate │-----------┘
                 └─────────────────────────────┘
```

Variants:
- Pre-retrieval branching: branch on multiple sub-queries before retrieval.
- Post-retrieval branching: retrieve once, then process documents in parallel.

## Example

Research assistant for "AI policy in healthcare":
1. Create branches for US regulation, EU regulation, clinical safety, and reimbursement.
2. Retrieve and summarize each branch independently.
3. Pass outputs to fusion for a consolidated report.

## Tradeoffs

- Gain: higher diversity and coverage.
- Cost: increased compute, latency coordination, and merge complexity.

## Failure Modes

- Duplicate or contradictory branch outputs.
- One failed branch silently reducing coverage.
- Poorly designed branch prompts causing redundant work.

## Relationship To Other Patterns

- `branching` is fan-out (parallel exploration).
- Its outputs commonly feed [`fusion`](./fusion.md), which performs fan-in consolidation.

## References

- Anthropic: Building Effective Agents (parallelization, orchestrator-workers) - https://www.anthropic.com/engineering/building-effective-agents
- LangGraph workflows (parallel and routing patterns) - https://docs.langchain.com/oss/python/langgraph/workflows-agents
- LlamaIndex Sub Question Query Engine (query decomposition + parallel sub-queries) - https://docs.llamaindex.ai/en/stable/examples/query_engine/sub_question_query_engine/
