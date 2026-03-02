# Linear

## Problem

Many AI systems need a predictable sequence of steps where each stage hands off output to the next. Without a linear flow, workflows become ad hoc, harder to debug, and harder to evaluate stage by stage.

RAG is one common example (query preprocessing -> retrieval -> post-processing -> generation), but the same pattern is also widely used in agentic workflows.

## Condition

Use this pattern when the task fits a single pass with clear handoffs between modules.
Do not use it when the task requires dynamic routing, parallel fan-out, or repeated refinement loops.

Typical fit:
- Agentic workflows with fixed stage ordering
- Simple question answering
- Summarization with light pre/post processing
- Rewrite-Retrieve-Read style flows

## Solution

Run a fixed pipeline:
1. Ingest input and normalize it into a stable schema.
2. Execute stage A (for example: classify, transform, retrieve, or call a tool).
3. Execute stage B (for example: validate, enrich, or summarize output from stage A).
4. Execute final response/action stage.
5. Return output plus stage-level traces/metadata for observability.

```text
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Input        │ -> │ Stage A      │ -> │ Stage B      │ -> │ Stage C      │ -> │ Final Output │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

This keeps ownership clear per stage and supports modular upgrades (swap one stage without redesigning the full workflow).

## Example

Customer-support copilot (agentic workflow):
1. Normalize user issue and extract account/product metadata.
2. Classify issue type and severity.
3. Call relevant tools (knowledge base, ticket history, order status API) in a fixed order.
4. Generate a resolution draft and next action for the support agent.

## Tradeoffs

- Gain: simple, interpretable pipeline with straightforward testing.
- Cost: less adaptable when tasks need dynamic decisions, parallel exploration, or iterative refinement.

## Failure Modes

- Early-stage errors propagate downstream because each stage depends on prior output.
- Over-constrained stage ordering can block better paths for edge cases.
- Missing observability makes it hard to identify which stage causes quality issues.

## References

- Anthropic: Building Effective Agents (prompt chaining workflow) - https://www.anthropic.com/engineering/building-effective-agents
- Lewis et al., Retrieval-Augmented Generation (RAG), 2020 - https://arxiv.org/abs/2005.11401
- Ma et al., Query Rewriting in Retrieval-Augmented Large Language Models (Rewrite-Retrieve-Read), 2023 - https://arxiv.org/abs/2305.14283
- Haystack documentation: Pipelines - https://docs.haystack.deepset.ai/docs/pipelines
- AutoGen documentation: Sequential Workflow - https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/sequential-workflow.html
- Microsoft Agent Framework: Sequential Orchestration - https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/sequential
