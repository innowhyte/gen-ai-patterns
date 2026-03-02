# Fusion

## Problem

After parallel retrieval/generation, results are often overlapping, incomplete, or conflicting. Fusion combines branch outputs into one coherent answer.

## Condition

Use this pattern when multiple branches/sources must be consolidated.
Do not use it when only one branch exists or when raw ranked results are sufficient.

Typical fit:
- Multi-index retrieval
- Ensemble pipelines
- Broad questions requiring synthesis across sources

## Solution

Apply a fan-in stage:
1. Collect outputs from multiple branches.
2. Normalize/clean and optionally summarize each branch result.
3. Merge with a fusion method:
   - LLM synthesis
   - weighted ensemble
   - rank fusion (for retrieval lists)
4. Resolve conflicts and produce a single final output.

```text
┌──────────────────┐
│ Branch A Output  │---+
└──────────────────┘   |
┌──────────────────┐   |    ┌──────────────────────┐    ┌────────────────┐    ┌──────────────┐
│ Branch B Output  │---+--> │ Normalize/Summarize  │ -> │ Fusion Engine  │ -> │ Final Answer │
└──────────────────┘   |    └──────────────────────┘    └────────────────┘    └──────────────┘
┌──────────────────┐   |
│ Branch N Output  │---+
└──────────────────┘
```

Fusion is typically downstream of `branching`, but can also combine heterogeneous retrievers directly.

## Example

Multi-source research assistant:
1. Run branches over arXiv, internal docs, and product analytics notes.
2. Summarize each branch to fixed token budgets.
3. Fuse with an LLM synthesizer and source-priority rules.
4. Return one answer with consolidated citations.

## Tradeoffs

- Gain: better completeness and robustness to weak single branches.
- Cost: extra orchestration, conflict resolution logic, and potential context-window pressure.

## Failure Modes

- Conflicting branch claims merged without contradiction handling.
- Over-compression losing key details during pre-fusion summarization.
- Fusion bias toward verbose branches instead of reliable branches.

## Relationship To Other Patterns

- `fusion` is fan-in (consolidation of multiple outputs).
- It is often downstream of [`branching`](./branching.md), but can also combine outputs from multiple retrievers without explicit branching.

## References

- Anthropic: Building Effective Agents (parallel + synthesis patterns) - https://www.anthropic.com/engineering/building-effective-agents
- LangChain Ensemble Retriever (rank fusion / weighted combination) - https://python.langchain.com/docs/how_to/ensemble_retriever/
- Azure AI Search reciprocal rank fusion - https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking
- Cormack et al., Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods, 2009 - https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
