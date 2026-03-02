# Assembly

> **Core Question:** What should the model see right now?

## Problem

Every token in the context window influences the model's response. Still, most agent builders assemble context in an ad-hoc, unstructured manner. System instructions, retrieved documents, tool definitions, conversation history, and examples are appended in order without thorough consideration.

Models exhibit the "lost in the middle" phenomenon. They attend most strongly to the beginning and end of their context window. When critical instructions or constraints land in this low-attention zone, the model ignores them.

Research shows, inclusion of low-signal tokens actively degrades response quality. Including a file "just in case" isn't free. It actively competes with the information actually needed.

Only putting the tool description without explicit mention of when to use it or when to avoid it. Poor descriptions cause cascading failures. The model picks the wrong tool, or the right tool with wrong arguments, or misses an opportunity to use a tool entirely.

When you ask a model to produce unstructured text, you get unstructured reasoning. Without a clear target shape, the model doesn't know what matters. Give it a schema and you're not just constraining the format; you're telling it what dimensions to reason along.

## Condition

This pattern is best suited when:

- When an agent is working in policy-heavy or regulated environments.
- Context for the agent is built by using multi-source retrieval systems.
- When the agent has access to more than a handful of tools (APIs, functions, databases) and must select the right one for each step.
- When the agent's output must be programmatically parsed, validated, or consumed by downstream systems.

## Solution

### Layer the Context

Arrange the context window into distinct layers aligned with the model's attention distribution.

- **Top Layer (High Attention):** System prompt, mission framing, identity, behavioral constraints, compliance rules. This is what the model must always remember.
- **Middle Layer (Lower Attention):** Retrieved documents, reference material, conversation history, examples. Supportive content that informs reasoning but doesn't need to dominate.
- **Bottom Layer (High Attention):** The immediate user query, task-specific instructions, output constraints, and the output schema. This is what the model must act on right now.

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

Before inserting any content into the context window, apply a curation step.

- **Relevance:** Is this information needed for the current query?
- **Non-redundancy:** Is this information already present in context elsewhere?
- **Token Budgeting:** How many tokens are allocated for each part of context, such as instructions, retrieved information, tool definition, etc?

### Strong Tool definition

A tool definition has four parts. The last two get the least attention but carry the most weight.

- **Name:** Should clearly convey the tool's purpose. get_user_profile is clear. query_42 is not.
- **Description:** The most important part. Tells the model not just what the tool does, but when to use it and what it doesn't do. This is the context that drives tool selection.
- **Parameters:** The input schema. Well-typed parameters and clear descriptions help the model send correctly structured inputs.
- **Return description:** What comes back and how to interpret it. Often omitted, but it helps the model plan multi-step workflows where one tool's output feeds another.

### Apply Output Schemas

When structured output is needed, include the schema in the bottom layer of context.

- Decide what an ideal output structure should look like.
- Define required fields, their types, and their descriptions.
- Curate a JSON output schema.