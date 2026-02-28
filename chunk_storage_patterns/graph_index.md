# Graph Index Pattern

## Problem

Similarity-only retrieval can miss answers that depend on explicit relationships between chunks. Typical failure symptoms are:

- The system retrieves text that is topically similar but not connected through the needed dependency path.
- Multi-hop questions (for example cause -> mechanism -> mitigation) return partial context.
- Relationship-specific queries (for example "what depends on X?") are hard to answer reliably.

This pattern addresses corpora where relationship traversal is a first-class retrieval requirement.

## Condition

Use this pattern when:

- Knowledge can be modeled as entities/chunks connected by typed edges.
- Users ask path-based or dependency-based questions, not only similarity questions.
- Product requirements include explainable traversal paths in retrieved evidence.

Do not use this pattern when:

- Queries are mostly single-hop FAQ lookup where vector retrieval is sufficient.
- Relationship extraction quality is low and cannot be validated.

## Solution

1. Define graph schema for retrieval use cases.
- Node types (for example `chunk`, `concept`, `entity`).
- Edge types with semantics (for example `depends_on`, `part_of`, `causes`, `mentions`).
- Required properties (source doc ID, confidence score, timestamp).
2. Build graph during ingestion.
- Create chunk nodes from source documents.
- Extract or map relationships and attach typed edges.
- Persist edge lineage metadata to support debugging and review.
3. Add hybrid retrieval hooks.
- Store embeddings on chunk nodes (or side index keyed by node ID).
- Support mixed queries: graph traversal constraints + semantic similarity.
4. Execute retrieval in two phases.
- Phase A: graph constraint step (start nodes, edge types, hop limits).
- Phase B: rank candidate nodes/chunks with semantic similarity and metadata filters.
5. Return evidence with path context.
- Include traversed edges and source chunks so answers can cite "why this chunk was selected."

## Example

- Incident-response knowledge base: from `service A`, traversal over `depends_on` and `mitigated_by` edges identifies at-risk downstream services and returns linked runbook chunks for the same path.
- Legal analysis assistant: traversal over citation and interpretation edges links statutes -> precedents -> commentary chunks so responses include relationship-aware evidence, not just topical similarity matches.
- Pharma research corpus: edges between compounds, mechanisms, trials, and adverse events allow retrieval to follow relationship paths that connect a drug candidate to relevant study-result chunks.

## Tradeoffs

- Gain: supports path-aware retrieval and relationship-specific questions.
- Gain: better explainability via explicit traversal paths.
- Cost: higher ingestion complexity due to schema and edge extraction.
- Cost: graph maintenance overhead (schema evolution, consistency checks, reprocessing).

## Failure Modes

- Incorrect edge extraction introduces false paths and irrelevant evidence.
- Unbounded hop traversal causes noisy retrieval and latency spikes.
- Stale graph state after document updates leads to outdated paths.
