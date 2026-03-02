# Routing

## Problem

A single monolithic pipeline is inefficient when queries differ by intent, risk, or domain. Routing (also called conditional routing) selects the most appropriate downstream path for each request.

## Condition

Use this pattern when you have distinct query classes (domain, language, risk level, task type) and specialized modules.
Do not use it when all queries are homogeneous or when classifier overhead outweighs gains.

Typical fit:
- Sensitive vs non-sensitive query handling
- Domain-specific assistants (legal, finance, support)
- Multilingual or tool-selection flows

## Solution

Add a router before heavy processing:
1. Ingest query and metadata.
2. Classify or score candidate routes (rules, model classifier, embeddings, or hybrid).
3. Select one route (or top-n routes, if needed).
4. Execute selected module/pipeline.
5. Log route decision for monitoring and retraining.

```text
┌──────────────┐    ┌────────────────────────────┐
│ User Query   │ -> │ Router (rules/model/hybrid)│
└──────────────┘    └──────────────┬─────────────┘
                                   ├──────────────> ┌───────────────────────────┐
                                   │                │ Route A: Domain Pipeline  │
                                   │                └───────────────────────────┘
                                   ├──────────────> ┌───────────────────────────┐
                                   │                │ Route B: Safety Pipeline  │
                                   │                └───────────────────────────┘
                                   └──────────────> ┌───────────────────────────┐
                                                    │ Route C: General Pipeline │
                                                    └───────────────────────────┘
```

## Example

Enterprise assistant:
1. Detect whether a request is legal, HR, or engineering.
2. Route legal queries to legal index + constrained prompt.
3. Route engineering queries to code/documentation retriever.
4. Return response with route-specific safety policy.

## Tradeoffs

- Gain: better accuracy/cost by matching task to specialist pipeline.
- Cost: route misclassification risk and additional evaluation overhead.

## Failure Modes

- Misrouting sensitive queries into weak-safety pipelines.
- Route drift when taxonomy changes but rules/models are not updated.
- Router confidence too low without fallback behavior.

## References

- Anthropic: Building Effective Agents (routing workflow) - https://www.anthropic.com/engineering/building-effective-agents
- LlamaIndex Router Retriever - https://docs.llamaindex.ai/en/stable/examples/retrievers/router_retriever/
- LangGraph workflows (routing) - https://docs.langchain.com/oss/python/langgraph/workflows-agents
- Haystack documentation: ConditionalRouter - https://docs.haystack.deepset.ai/docs/conditionalrouter
