# Small-to-Big

## Problem

When building Retrieval-Augmented Generation (RAG) applications, one common challenge is finding the right balance between retrieving enough context to answer a question accurately and ensuring that the retrieval process remains precise.

- **What Problem Does It Solve?**
- In many RAG workflows, larger chunks of text can provide the necessary context for thorough understanding, but they also risk introducing noise and irrelevant data into retrieval. Smaller chunks, while more targeted, can lose the broader context necessary for producing accurate and complete answers. The “Small-to-Big” pattern addresses this tension by enabling both high-precision retrieval and access to richer contextual data.
- **Why Is This Pattern Necessary?**
- Without an approach that distinguishes between “retrieval chunks” and “synthesis chunks,” your system could suffer from:
    1. **Overly Large Chunks** leading to poor search precision (retrieving a lot of irrelevant text).
    2. **Overly Small Chunks** leading to insufficient context at synthesis time, causing incomplete or misleading outputs.
    3. The “Small-to-Big” pattern tackles both issues by combining the best of both worlds.

---
## Condition

- **When to Use It**
    - You need to retrieve highly targeted information from large repositories (e.g., large databases, corpora, or knowledge bases).
    - You want to ensure that your final generative model has access to broader context while still limiting the noise during retrieval.
    - Your application frequently answers detailed questions requiring both precision and expansive background information.
- **Example Use Cases**
    1. **Customer Support Knowledge Base**: Retrieve fine-grained knowledge from individual articles or FAQ entries (small chunks), but reference entire documents or sections when generating a comprehensive answer.
    2. **Academic Research Assistant**: When answering queries about specific facts within a large corpus of scientific papers, retrieve short passages containing the key points, then expand context from the full paper if needed.
    3. **Legal Document Review**: Retrieve specific clauses or paragraphs (small chunks) in contracts but keep entire contract sections (bigger chunks) accessible for deeper analysis.

---
## Solution

The “Small-to-Big” pattern involves splitting your knowledge base into two layers of chunks:

1. **Small / Fine-Grained Chunks**
    - Used primarily for retrieval.
    - Typically consist of short passages, paragraphs, or summarized segments.
    - Maximizes retrieval accuracy because the search engine or vector database can match query embeddings more precisely.
2. **Big / Contextual Chunks**
    - Large sections of text, documents, or entire chapters.
    - Provides sufficient context during the synthesis phase.
    - By referencing the larger parent chunk (or full document), the answer can incorporate necessary background information.

A **high-level workflow** might look like this:

```
 ┌─────────────┐      ┌───────────────────────────────┐
 │ User Query   │      │ Vector DB / Retrieval Service │
 └──────┬───────┘      └───────┬───────────────────────┘
        │                     │
        │ (1) Retrieve        │
        └────────────────────>│  Smaller chunks found
                              │
                              v
                 ┌─────────────────────────┐
                 │ Retrieve Larger Context │  (2) Reference bigger chunks
                 └─────────────────────────┘
                              │
                              v
                ┌──────────────────────────┐
                │  LLM-based Synthesis     │  (3) Generate final answer
                └──────────────────────────┘
```
1. **Retrieval (Small Chunks)**: The user’s query is matched against a database of small, fine-grained chunks. This ensures precision and minimal noise.
2. **Context Lookup (Big Chunks)**: For each retrieved small chunk, identify and pull in the associated larger context from its “parent” document or cluster.
3. **Synthesis**: Pass both the smaller targeted results and necessary big-chunk context to the generative model (LLM). The model then synthesizes a final, coherent answer.

### Important Considerations

- **Indexing Strategy**:
- You may need dual indexes—one for fine-grained chunks (optimized for high-precision search) and another for larger documents or sections.
- **Summarization for Small Chunks**:
- Often, the small chunks are themselves condensed or summarized to reduce noise and focus on the key points.
- **Linking Mechanism**:
- Each small chunk must keep a reference (like an ID or parent pointer) to its larger source text. This relationship is vital when pulling bigger context.
- **Storage vs. Search Cost**:
    - Storing both small and big chunks can increase storage overhead.
    - However, searching on smaller chunks is often faster and more accurate.
    - The subsequent reference to big chunks can happen only for highly relevant content, optimizing overall efficiency.
- **Complexity**:
- Implementing a two-tier system requires additional steps for chunk management and parent-child linking. But the payoff is improved accuracy and completeness.
- **Evaluation**:
    - **Precision** improves because retrieval focuses on narrower, more specific units.
    - **Recall** remains high because the larger context is ultimately accessible.
    - Evaluate both retrieval accuracy (small chunks) and final answer quality (with big context) to confirm the pattern’s effectiveness.

### Unique Benefits

- **Better Query Matching**: Smaller, well-defined chunks reduce ambiguity, yielding more relevant search results.
- **Rich Context**: Larger chunks (or entire documents) are not lost; they come into play when assembling the final response.
- **Flexibility**: You can adjust chunk sizes dynamically based on different domains or application needs.
- **Scalability**: This approach scales well for large document collections, balancing retrieval precision with comprehensive coverage.

By systematically distinguishing the role of smaller chunks for retrieval and bigger chunks for synthesis, the “Small-to-Big” pattern ensures both a high-precision retrieval step and a thorough generative process, leading to answers that are both precise and complete.

## Tradeoffs

- Higher retrieval precision, but extra engineering to maintain two chunk layers.
- Better final context for synthesis, but additional storage and linking overhead.
- More controllable quality, but more moving parts in indexing and retrieval.

## Failure Modes

- Parent-child links between small and big chunks are missing or incorrect.
- Small chunks are over-compressed and lose critical retrieval cues.
- Big chunks are too large for synthesis and reintroduce context noise.
- Teams optimize retrieval precision but skip end-to-end answer quality checks.

## Example

In a legal assistant, retrieve matching clauses as small chunks first, then pull the full section containing each clause before answer generation.
