# Assembly

> **Core Question:** What should the model see right now?

## Problem

Context is often assembled by appending everything available: system instructions, retrieval chunks, tool specs, conversation history, and examples. This creates noisy prompts where critical instructions are buried and lower-value tokens compete with higher-value ones.

In long prompts, important constraints can land in low-attention zones and be ignored. Tool misuse also rises when tool descriptions explain what a tool does but not when to use it, when to avoid it, and what output to expect. If output format is underspecified, responses become hard to validate or automate.

## Condition

Use when:

- The prompt combines policy, retrieval, tool use, and strict output requirements in a single turn.
- The agent has multiple tools and repeated tool-selection errors are observed.
- Retrieved content volume is high and only a subset is relevant to the active task.
- Output is consumed by downstream systems and must match a schema.

Do not use when:

- The task is short, single-step, and does not require retrieval or tool calls.
- The goal is early exploration where relevance is still unknown; start with progressive disclosure first.
- A deterministic non-LLM component can solve the task more reliably.

## Solution

### Layer the Context

Arrange the prompt into layers aligned to attention priority:

- Top layer: policy, role, hard constraints.
- Middle layer: selected evidence and brief history.
- Bottom layer: active task, acceptance criteria, output schema.

```
┌─────────────────────────────────────┐
│  SYSTEM INSTRUCTIONS & CONSTRAINTS  │  ← High attention (top)
│  Identity, rules, compliance        │
├─────────────────────────────────────┤
│  RETRIEVED DOCUMENTS & REFERENCE    │  ← Lower attention (middle)
│  Knowledge, history, examples       │
├─────────────────────────────────────┤
│  CURRENT TASK & OUTPUT SCHEMA       │  ← High attention (bottom)
│  User query, constraints, format    │
└─────────────────────────────────────┘
```

### Curate for Signal, Not Volume

For each candidate context block, pass four checks before inclusion:

- Relevance: needed for the current decision.
- Signal density: mostly useful lines, minimal boilerplate.
- Non-redundancy: no repeated facts from other blocks.
- Budget fit: stays within predefined token budget per layer.

### Define Tool Contracts

For every tool, include:

- Purpose in plain language.
- Positive trigger: when to use this tool.
- Negative trigger: when not to use this tool.
- Parameter schema and return semantics.

### Add Schema Steering and End-of-Turn Anchor

Schema steering is not only about output format. It defines the reasoning surface the model must fill.

Design the schema as a contract:

- Required fields for decisions that must always be present.
- Typed fields for safer downstream parsing.
- Bounded fields (enums, min/max ranges) to reduce drift.
- Evidence fields that force grounding (`sources`, `evidence_snippets`).
- Uncertainty fields (`confidence`, `missing_information`) so the model can express limits without guessing.

Use field-level instructions, not only a top-level instruction. Example:

- `root_cause`: one sentence, must be source-backed.
- `next_step`: one concrete action with tool name or query.
- `confidence`: one of `high|medium|low`.
- `missing_information`: empty array if sufficient; otherwise list gaps.

Apply a validation and repair loop:

1. Generate output against the schema.
2. Validate with a parser or JSON schema validator.
3. If invalid, send validation errors back to the model and request repair-only output.
4. Stop after a fixed retry limit and return a controlled failure state.

End each turn with an anchor block that repeats success criteria for the next action. This prevents schema drift in long sessions.

```json
{
  "type": "object",
  "required": ["root_cause", "next_step", "confidence", "sources"],
  "properties": {
    "root_cause": { "type": "string", "minLength": 10 },
    "next_step": { "type": "string", "minLength": 10 },
    "confidence": { "type": "string", "enum": ["high", "medium", "low"] },
    "sources": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    },
    "missing_information": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "additionalProperties": false
}
```

## Example

A support agent must resolve "401 after token refresh" using product docs and tools.

1. Top layer includes security policy and "do not guess missing values."
2. Middle layer includes two selected doc snippets and one recent troubleshooting result.
3. Bottom layer includes the task plus a JSON schema with:
   - Required fields: `root_cause`, `next_step`, `confidence`, `sources`.
   - Optional field: `missing_information` for insufficiency reporting.
4. Tool contract for `check_token_history` includes when-to-use and when-not-to-use.
5. Anchor block repeats: "If docs are insufficient, return insufficiency with cited gaps."

The agent returns a structured answer with source-backed reasoning and no irrelevant history.

## Tradeoffs

- Better reliability and parseability, but higher prompt-engineering overhead.
- Lower hallucination risk, but less flexibility for open-ended brainstorming.
- Strong schema control, but occasional need to revise schema as tasks evolve.

## Failure Modes

- Over-compression removes needed edge-case context.
- Tool descriptions drift from actual tool behavior and mislead selection.
- Anchor block becomes stale and reinforces outdated constraints.

## References

- [The Pyramid](https://contextpatterns.com/patterns/pyramid/)
- [Select, Don't Dump](https://contextpatterns.com/patterns/select/)
- [Schema Steering](https://contextpatterns.com/patterns/schema-steering/)
- [Tool Descriptions as Context](https://contextpatterns.com/patterns/tool-descriptions/)
- [Attention Anchoring](https://contextpatterns.com/patterns/attention-anchoring/)
- [Anchor Turn](https://contextpatterns.com/patterns/anchor-turn/)
- [How to Fix Your Context](https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html)
- [Attentive Reasoning Queries: A Systematic Method for Optimizing Instruction-Following in Large Language Models](https://arxiv.org/abs/2503.03669)
