# Hierarchical Index Pattern

## Problem

Flat chunk indexing can return either fragmented snippets or overly broad passages. In retrieval pipelines this often creates two failure symptoms:

- Broad questions return low-level chunks without enough context.
- Specific questions return large, noisy chunks that dilute the answer signal.

This pattern targets document sets where one query interface must support both summary-level and detail-level retrieval over the same corpus.

## Condition

Use this pattern when:

- Documents have natural hierarchy (document -> section -> paragraph).
- Users ask both high-level and highly specific questions.
- Retrieval latency or cost is impacted by searching all fine-grained chunks for every query.

Do not use this pattern when:

- Corpus is small enough that flat retrieval already meets latency and quality targets.
- Source data has weak structure (for example short independent notes with no section tree).

## Solution

1. Build hierarchical units during ingestion.
- Create document-level records (title, summary, global metadata).
- Create section-level chunks tied to parent document IDs.
- Create paragraph- or sentence-level chunks tied to parent section IDs.
2. Store each level with explicit parent-child links.
- Keep IDs that allow downward traversal (document -> section -> fine chunk).
- Keep metadata filters shared across levels (tenant, product, date, language).
3. Index each level for retrieval.
- Keep vector index for semantic matching.
- Keep metadata index for filtering and routing.
4. Execute top-down retrieval.
- Step A: retrieve candidate documents/sections for the query.
- Step B: decide whether detail is needed (for example based on query specificity, answer confidence, or missing entities).
- Step C: drill down only inside selected parents to fetch fine-grained chunks.
5. Compose context for generation.
- Merge selected chunks with lineage metadata (document ID, section heading, offsets).
- Enforce max token budget with deterministic truncation rules.

## Example

- Legal document search: a query starts with case-level summaries, then drills into the specific clause and precedent paragraphs only within the selected case.
- Enterprise knowledge base support bot: broad troubleshooting questions return section-level playbooks first, while error-code questions drill into fine-grained chunks for exact remediation steps.
- Technical API documentation: retrieval begins at module-level descriptions and then narrows to endpoint-level chunks (parameters, limits, error codes) when the query asks for implementation details.
- Multi-product developer portal: for "How do rate limits work for refund endpoints?", retrieval narrows from `payments-api-v2` -> `rate-limits` and `refunds` sections -> endpoint chunks, then returns only those scoped chunks for generation.

## Tradeoffs

- Gain: better control over context granularity per query.
- Gain: reduced search scope for detail retrieval after top-level narrowing.
- Cost: higher ingestion and storage overhead due to multi-level embeddings.
- Cost: more complex retrieval orchestration and testing.

## Failure Modes

- Incorrect parent-child links cause drill-down to wrong sections.
- Stop/drill-down decision logic is unstable, causing inconsistent answer quality.
- Hierarchy becomes stale when documents are restructured without full re-indexing.
