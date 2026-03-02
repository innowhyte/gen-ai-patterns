# Integrity

> **Core Question:** How do I keep the context trustworthy?

## Problem

As agents operate over extended sessions, accumulate information from multiple sources, and persist knowledge across turns, the context window becomes vulnerable to corruption in ways that are subtle, compounding, and difficult to detect from the outside.

- **Context poisoning** - When the model hallucinates a fact and that hallucination gets written into a scratchpad, memory system, or conversation history, it becomes ground truth for every subsequent turn. The model has no mechanism to doubt its own prior context. One fabricated number, citation, or entity persisted in state compounds indefinitely, cascading into every downstream decision that builds on it.
- **Context contradiction** - When the model encounters conflicting information, it silently picks one version (often whichever best supports its current generation trajectory), with no consistency across multiple calls.
- **Invisible Quality Degradation** - All the above failure modes are difficult to detect from the outside. The agent continues generating fluent, confident responses that may be internally consistent but factually wrong.

## Condition

When to use this pattern:

- **High-Stakes Decision Domains** - Downstream decisions based on the agent's output carry real consequences, such as medical, financial, legal, or safety-critical applications, where a hallucination or contradiction could cause harm.
- **Multi-Source Information Environments** - The agent routinely combines information from multiple retrieval sources, tools, databases, or external APIs, increasing both the probability of contradictions and the difficulty of maintaining consistency.
- **Long-Running Sessions with Persistent State** - The agent maintains state across many turns or sessions through scratchpads, memory, or conversation history, creating opportunities for hallucinated facts to enter and persist in that state.

## Solution

### Validation Before Persistence

Before any fact, finding, or intermediate conclusion is written to a scratchpad, memory system, or carried forward as established context, it passes through a validation step.

- **Cross-Reference Verification:** Check key claims against source documents or authoritative databases.
- **Structured Verification Prompts:** Use a separate LLM call (or dedicated verification agent) that asks: "Given these sources, is the following claim supported? What is the evidence?"
- **Confidence Thresholds:** Assign confidence levels to claims. Only high-confidence, source-backed claims are persisted. Lower-confidence claims are flagged as tentative.
- **Provenance Tracking:** Each persisted fact should include its provenance: where it came from and how it was verified. This creates an audit trail that enables both runtime verification and post-hoc analysis.

```
WITHOUT VALIDATION:
Model generates  -> "Drug interaction between X and Y causes Z"
                 -> Written directly to scratchpad
                 -> Referenced as fact in all subsequent turns
                 -> If hallucinated, compounds indefinitely

WITH VALIDATION:
Model generates  -> "Drug interaction between X and Y causes Z"
                 -> Validation step: cross-reference drug database
                 -> VERIFIED:     written to scratchpad with source
                    NOT VERIFIED: flagged as unconfirmed, not persisted
```

### Contradiction Detection and Resolution

Implement explicit mechanisms for handling conflicting information:

- **Detection:** When new information enters context (from retrieval, tool calls, or model generation), compare it against existing context for conflicts. This can use:
  - Structured comparison prompts ("Does this new information conflict with anything already established?").
  - Field-level matching for structured data (comparing the same metric from different sources).
  - Consistency checks at defined intervals.
- **Resolution Rules:** Define how contradictions are resolved:
  - **Recency:** Prefer newer information when timestamps are available.
  - **Authority:** Prefer authoritative sources (primary databases over secondary reports, official documentation over forum posts).
  - **Specificity:** Prefer more specific information over more general.
  - **Escalation:** When automated resolution isn't possible or appropriate, flag the contradiction for human review rather than making an arbitrary choice.
  - **Transparency:** When contradictions are resolved, record the resolution in context: "Source A reported $2.3M; Source B reported $2.8M. Using Source A (primary database, more recent update date)."

## Example

A financial analysis agent is tasked with producing an acquisition report for Company X. It pulls revenue figures from two data providers and queries a legal database for outstanding litigation.

Without integrity mechanisms, the agent surfaces a revenue contradiction between the two providers and silently picks the higher figure. Two turns later it generates a valuation based on that unverified number. By the time the report is produced, it is built on a corrupted state with no visible indication that anything went wrong.

With integrity mechanisms in place:

```
Revenue contradiction detected:
Provider A: $2.3B  |  Provider B: $2.8B
Resolution rule: prefer primary database (Provider A, direct filing)
Recorded in context: "Using $2.3B from Provider A. Provider B figure
                      flagged as unverified secondary source."

Litigation claim generated by model:
"Company X has no outstanding litigation as of Q4 2024"
Validation: cross-referenced against legal database
NOT VERIFIED: flagged as unconfirmed, not persisted
Human review triggered.
```

The report is built on a validated, traceable state. Every persisted fact has a source. Every contradiction has a documented resolution. Nothing unverified is carried forward as established fact.
