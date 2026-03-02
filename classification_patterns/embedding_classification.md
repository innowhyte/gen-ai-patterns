# Embedding Classification

## Problem

Something has to decide which agent handles each incoming message. You have two obvious options: an LLM (accurate but slow and expensive) or a pile of if/else rules (fast but painful to maintain).

There's a third option. Embed each agent's description into a vector once at startup, embed each user message at runtime, and pick the closest match. No LLM inference per request. No hand-written rules to update every time you add an agent.

## Condition

Use this pattern when you have a known set of routes with clear text descriptions and you need classification to be fast and cheap.

Don't use it when:
- Routes overlap enough that you need actual reasoning to tell them apart. Use LLM classification instead.
- The taxonomy changes mid-session. Re-indexing has overhead.
- You need the system to say "I don't know." Embedding classifiers always return the nearest match, even when the right answer is "none of the above."

Typical fit:
- High-throughput multi-agent routing (support bots, helpdesks, tutoring systems)
- Cost-sensitive deployments where an LLM call per classification isn't viable
- Fast pre-filter before a heavier LLM classifier

## Solution

1. Register route descriptions. One short text per route or agent.
2. Embed all descriptions into vectors with an embedding model.
3. Normalize vectors (L2) and build a similarity index (e.g., FAISS `IndexFlatIP` for cosine similarity).
4. At classification time, embed the user message, normalize it, and find the nearest description vector.
5. Return the matched route and the similarity score as a confidence proxy.
6. Optionally set a confidence threshold. Below it, fall back to a default route.

```text
                       Build Time
                       ─────────────────────────────────────────────
                       ┌──────────────────┐    ┌──────────────────┐
                       │ Route            │    │                  │
                       │ Descriptions     │--->│ Embedding Model  │──> FAISS Index
                       │ (one per agent)  │    │                  │
                       └──────────────────┘    └──────────────────┘

                       Query Time
                       ─────────────────────────────────────────────
┌──────────────┐    ┌──────────────────┐    ┌──────────────┐    ┌──────────────────┐
│ User Message │--->│ Embedding Model  │--->│ FAISS Search │--->│ Route Decision   │
└──────────────┘    └──────────────────┘    │ (nearest     │    │ (agent, score,   │
                                            │  neighbor)   │    │  threshold gate) │
                                            └──────────────┘    └──────────────────┘
```

A few things that matter in practice:

- **L2-normalize all vectors before indexing.** Use inner product (`IndexFlatIP`) on normalized vectors for cosine similarity. Raw L2 distance penalizes magnitude, which isn't what you want here.
- **Confidence scores are geometric, not semantic.** A similarity of 0.35 means "this was the closest vector." It does not mean "35% sure this is the right agent." Treat it as a ranking signal, not a probability.
- **There is no universal "good" threshold.** You have to run labeled test cases against your specific taxonomy and find the threshold that trades off false positives against unnecessary fallbacks. This is empirical work.

## Example

Customer support system with five agents (billing, technical, sales, account, general):

1. Embed each agent's description (e.g., "Handles billing inquiries, payment issues, invoices, charges, refunds, and subscription changes").
2. Build a FAISS index from the five description vectors.
3. User sends: "I was charged twice on my credit card last month."
4. Embed the message, search the index. Nearest match is `billing` with similarity 0.52.
5. 0.52 is above the confidence threshold of 0.25. Route to `billing`.

Now try adversarial input: "asdfjkl;qwerty12345 banana"
- Nearest match is `technical` with similarity 0.17.
- That's below threshold. Fall back to `general`.

The threshold caught the gibberish. But notice: without the threshold, this nonsense string would have been routed to `technical` with full confidence. The classifier doesn't know it's confused.

## Tradeoffs

- Classification cost is basically zero. You pay for one embedding API call. No LLM inference.
- Latency is sub-second, usually dominated by the embedding API round-trip rather than the search itself.
- Results are deterministic. Same input, same route, every time. No temperature, no sampling variance.
- Accuracy drops on ambiguous or multi-intent queries compared to LLM classifiers. The model can't reason about "what does this user actually want?"
- The classifier can't explain its decisions. There's no reasoning, just a distance.
- Catch-all categories get crushed. A `general` agent with a vague description like "handles general inquiries and greetings" will consistently lose to specialist agents whose descriptions share more vocabulary with incoming messages. Off-topic messages end up at a specialist more often than you'd expect.

## Failure Modes

- **No "none of the above."** The index always returns a nearest neighbor. Gibberish, off-topic messages, prompt injections: they all get routed somewhere. Thresholds help. They don't fix it.
- **The catch-all agent under-triggers.** In every benchmark we've run, the `general` agent gets fewer messages than it should, because its description is too vague to win in embedding space. This is structural, not a tuning problem.
- **Description quality is the ceiling.** If two agents have overlapping descriptions, the classifier can't distinguish them no matter how much you tune the threshold. Accuracy is bounded by how well descriptions separate in embedding space.
- **Multi-intent messages split the difference.** "My payment failed and the app crashed" sits between `billing` and `technical`. The classifier picks one. It can't flag ambiguity or route to both.

## Relationship To Other Patterns

- Embedding classification is one way to implement the classifier step in [`routing`](../orchestration_patterns/routing.md).
- When embedding confidence is low, you can hand off to an LLM classifier as a second pass (see `llm_classification`).
- Combining both becomes a cost/accuracy optimization: embeddings handle the easy cases, LLMs handle the hard ones.

## References

- FAISS: A Library for Efficient Similarity Search - https://github.com/facebookresearch/faiss
- OpenAI Embeddings Guide - https://platform.openai.com/docs/guides/embeddings
- Anthropic: Building Effective Agents (routing workflow) - https://www.anthropic.com/engineering/building-effective-agents
- Johnson et al., Billion-scale similarity search with GPUs (FAISS paper), 2017 - https://arxiv.org/abs/1702.08734
