# Distribution

> **Core Question:** Should one agent see everything, or many agents see less?

## Problem

Complex tasks ask a single agent to juggle multiple concerns at once: researching different sub-questions, calling different tools, applying different domain expertise, and synthesizing everything into a coherent output.

When all of this happens in one shared context, it creates four compounding failure modes.

- **Cross-contamination** - Noisy search results from one sub-question pollute the reasoning space for another. A failed tool call's verbose error trace distracts from unrelated analytical work. Intermediate reasoning for one subtask bleeds into conclusions about a different one.
- **Attention dilution.** As a single context accumulates the full breadth of a complex task, the model's attention is spread thin. It cannot go deep on any one thread because it must maintain awareness of everything simultaneously.
- **Sequential bottleneck.** A single agent processes one step at a time, even when multiple lines of investigation could run in parallel.
- **Boundary pollution.** When results do pass between agents, transferring raw context, full conversation histories, verbose tool outputs, and unfiltered intermediate reasoning reintroduces the exact problems that isolation was meant to solve.

## Condition

This pattern is best suited when:

- A task requires pursuing multiple independent lines of inquiry, each benefiting from deep, focused investigation rather than shallow parallel tracking in one context.
- Different parts of the task require different domain expertise, different tool sets, or different analytical approaches. Mixing them in one context creates confusion.
- Processing flows through sequential stages such as extract, validate, enrich, and generate, and each stage's concerns should be isolated from the others.
- The total information needed for a task exceeds the model's effective attention range, not necessarily the window limit, but the range where quality remains high.

## Solution

### Task Decomposition and Delegation

Before any agent starts working, the task needs to be broken into subtasks that can be handled independently. Each subtask should have a clear scope, a clear deliverable, and a defined set of required capabilities. How this decomposition happens depends on the architecture.

In hierarchical systems, an orchestrator analyzes the task at runtime and delegates scoped subtasks to workers. In pipeline systems, the decomposition is designed upfront as stages. In peer systems, each agent is pre-assigned a domain or capability boundary.

What is constant across all three is this: each agent receives a context built for its specific subtask, not the full task. The scope definition is what makes focused context possible in the first place.

### Context Boundary Enforcement

Regardless of architecture, each agent should start with a context that contains only what it needs to complete its part of the task. Nothing more, nothing less.

In a pipeline, that means the handoff from stage to stage carries only the output relevant to the next stage, not the full working history of the previous one. In a peer system, each agent's context is scoped to its assigned domain from the start. In a hierarchical system, the orchestrator constructs a focused sub-context for each worker rather than passing down its own full context.

The boundary is not enforced by the architecture alone. It requires a deliberate construction step for every agent context, every time.

### Handoff Distillation

hen one agent's output enters another agent's context, the question to ask is: what does the receiving agent actually need to complete its part of the task? That is all that should cross the boundary.

Extract findings, decisions, validated facts, and key artifacts. Discard intermediate reasoning, failed attempts, raw tool outputs, and working notes. Preserve enough provenance that the receiving agent understands why a conclusion was reached, not just what it was, since it may need to reason about confidence or gaps.

If agents pass their full working context rather than a distilled result, the receiving agent inherits all the noise the sending agent accumulated. Distribution without distillation at handoffs recreates single-agent context pollution in a more complex system.

## Example

A due diligence workflow is triggered for a company acquisition. The task involves legal review, financial health analysis, operational risk assessment, and reputational research. An orchestrator decomposes the task into four subtasks and assigns each to a specialized agent.

```
ORCHESTRATOR
Task: Acquisition due diligence for Company X
Decompose into subtasks:
├── Legal agent
│   Context: legal docs, contracts, compliance tool
├── Financial agent
│   Context: financial statements, ratio calculator, filings tool
├── Operational agent
│   Context: ops reports, supply chain data, risk framework
└── Reputational agent
    Context: news search tool, litigation database

All four run concurrently.

Each returns a distilled result:
├── Legal: 3 flagged clauses, 1 open litigation risk
├── Financial: Revenue stable, debt-to-equity elevated
├── Operational: Single-supplier dependency identified
└── Reputational: Negative press from 2022 resolved

Orchestrator synthesizes into unified assessment.
```

Each agent worked on its subtask without noise from the others. The orchestrator only ever saw distilled conclusions, not raw research trails. The synthesis context stayed lean enough to reason clearly across all four inputs.

The critical implementation detail is distillation at the boundary. If agents return their full working context rather than a distilled result, the orchestrator's synthesis context becomes as polluted as if distribution never happened.
