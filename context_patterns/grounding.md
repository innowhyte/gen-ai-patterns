# Grounding

> **Core Question:** How do I make sure retrieved data beats training data?

## Problem

RAG systems and tool-integrated agents invest significant effort getting the right information into context, through embedding searches, reranking, API calls, and document retrieval. But getting information into context and getting the model to reliably use it are two distinct problems.

Without proper grounding, the model does not treat retrieved content as the authoritative source. Instead it blends it with its own background knowledge, assumptions, and plausible-sounding guesses. This creates four compounding failures.

- **[Not sure if this make sense but kept if for now.] Blending** - The model does not cleanly separate retrieved content from its own background knowledge. It mixes the two in a single response without distinguishing which is which. The output looks coherent but is part retrieved, part generated, with no boundary between them.
- **Silent gap-filling** - When retrieved content is incomplete, the model does not stop and flag what is missing. It fills the gap with a confident, plausible-sounding answer drawn from training data. The response appears grounded. It is not. This is the most common RAG failure because the system looks like it is working correctly while producing wrong outputs.
- **Contradiction** - The model's output can directly disagree with the source it was supposed to use, without acknowledging the conflict. A retrieved document states one figure; the response states another. The model does not flag this. It simply picks one, often unpredictably.
- **Broken traceability** - Without citations anchored to specific retrieved sources, there is no way to verify whether a claim came from the documents or was generated. In enterprise, legal, or medical settings, this is not just a quality problem. It is a compliance and trust problem. A system designed for accuracy becomes one that merely sounds correct.

## Condition

This pattern is best suited when:

- The retrieved information is the authoritative source and the model must refer to it, such as internal documentation, regulatory content, product specifications, or clinical guidelines, rather than relying on training data that may be outdated or incorrect.
- The domain changes often enough that training data is likely stale. New regulations, updated product features, recent research findings. Retrieved context is the current ground truth.
- Responses must be traceable to specific sources for compliance, auditing, or user trust. The model must not only use retrieved content but demonstrate that it did.

## Solution

### Source Tagging

Before the retrieved content enters the context, label it explicitly. Each chunk should carry a clear marker identifying where it came from.

```
[SOURCE: Product Docs v3.2 - Section 4.2: Token Authentication]
Refresh tokens expire after 24 hours of inactivity. Tokens
issued before the inactivity window reset are invalidated
immediately upon refresh.

[SOURCE: Troubleshooting KB - Auth Errors]
A 401 after token refresh typically indicates the previous
token was invalidated before the new one was issued.
```

This does two things. It gives the model an unambiguous signal about what is retrieved versus what is general context. And it makes citation a natural output behavior, the model has the source label right there to reference.

Take this a step further by making citation a required field in the output schema. A soft instruction to cite sources can be ignored. A required sources field in the output structure cannot. If the model cannot populate it, the response fails validation rather than slipping through unchecked.

### Explicit Anchoring Instructions

Add meta-instructions to the system prompt that define the model's relationship with retrieved content. Three instructions matter most.

- **Prioritize retrieved context over general knowledge:** When retrieved documents conflict with what the model knows from training, it should refer to the documents. State this explicitly. Without it, the model blends the two without a defined rule for which takes priority.
- **Cite sources when making specific claims:** Reference the document or section that supports each claim. This is what makes silent gap-filling visible. If the model cannot point to a source, it should not be making the claim.
- **Flag insufficiency explicitly:** If retrieved documents do not contain enough information to answer the question, the model says so rather than filling the gap from memory. It states what the documents cover and what remains unanswered.

Pair every positive instruction with its negative counterpart - "Prioritize retrieved content" should be accompanied by "do not blend retrieved content with general knowledge." "Flag gaps" should be accompanied by "do not fill gaps with plausible-sounding guesses." Negative instructions catch the failure modes that positive ones miss.

## Example

A technical support agent handles a query about why a user's API requests are returning 401 errors after a recent token refresh. The knowledge base covers four product areas across hundreds of pages of documentation.

Without grounding instructions, the model blends its general knowledge of OAuth token flows with the retrieved product docs. The product's token expiry window differs from the OAuth standard the model was trained on. The model fills that gap silently, producing a confident and wrong troubleshooting path with no indication that it deviated from the source.

With grounding in place, the agent starts with the index, identifies the API Reference authentication section and the auth-related troubleshooting entries as relevant, and loads only those two sources.

```
System prompt anchoring instruction:
"Prioritize retrieved documents over general knowledge.
 Cite the specific section supporting each step.
 If the documents do not cover the issue, say so explicitly
 rather than filling the gap from general knowledge."

Agent loads:
├── API Reference: Token Refresh (1.8k tokens)
└── Troubleshooting KB: 401 errors after refresh (0.9k tokens)

Retrieved docs state:
"Refresh tokens expire after 24 hours of inactivity."
(OAuth standard the model knows: 30-day expiry)

Without grounding: model blends both, answers using 30-day
                   figure from training. No contradiction flagged.

With grounding:    model refers to the 24-hour figure from the docs,
                   cites the exact section, and does not blend in
                   the conflicting standard it was trained on.
```

The anchoring instruction does two things here. It resolves the conflict between retrieved content and training knowledge in a predictable, consistent direction. And it forces the model to cite its source, which makes any silent gap-filling or blending visible rather than buried in a fluent, confident response.
