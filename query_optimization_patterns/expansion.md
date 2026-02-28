# Expansion

# Problem

When a system relies directly on a user’s original query \(as in a basic “naive RAG” setup\), two major issues often arise:

1. **Poorly Formulated Queries**
2. Users might not know how to articulate their questions clearly and succinctly. This results in queries that are overly broad, ambiguous, or missing crucial details needed for accurate retrieval.
3. **Language Ambiguity and Complexity**
4. Specialized vocabulary and abbreviations \(e.g., “LLM” could mean either “Large Language Model” or a “Master of Laws”\) are not always interpreted correctly. Simple keyword matching or straightforward embeddings may miss the nuanced context needed for precision.

Without addressing these challenges, retrieval systems can underperform by:

- Returning irrelevant documents.
- Missing important sub-problems within a complex query.
- Failing to clarify key domain-specific terms, leading to incomplete or incorrect results.

Hence, **Query Expansion** is necessary to ensure higher retrieval accuracy, reduce ambiguity, and preserve essential context.

# Condition

**Best Suited When:**

- **Complex or Multifaceted Queries**
- When the original user query has multiple parts or implicit sub-questions that need to be answered in stages or via different angles of retrieval.
- **Specialized Domains**
- In domains with specialized vocabularies—like medical, legal, or technical fields—expanding the query helps disambiguate specialized terms and synonyms.
- **Unclear or Ambiguous User Input**
- If the query is very short or ambiguously worded, generating multiple expanded variants can help refine the search space.

**Example Use Cases**

1. **Medical Question Answering**: A query about a condition like “effects of drug X on pregnant women” might need expansions \(“drug X contraindications,” “drug X pregnancy guidelines,” “drug X side effects,” etc.\).
2. **Legal Document Retrieval**: A query mentioning “LLM” could be expanded into both “Large Language Model” and “Master of Laws” to see which yields more relevant results in a legal context.
3. **Technical Troubleshooting**: A query like “Why is my code failing?” can be expanded to consider different dimensions: environment setup, syntax errors, library incompatibility, etc.

# Solution

**Core Idea**

Expand the user’s initial query into multiple related queries—either in parallel or via stepwise decomposition—so that the retrieval process covers more ground and resolves ambiguities. This can happen via:

- **Multi-Query Expansion**
- Use prompt engineering to generate multiple, diverse expansions of the user’s query. For example, a user’s single question might be expanded into three or four thematically distinct queries. This ensures broader coverage of possible interpretations.
    - **Weighting the Original Query**: Instruct the system to treat the user’s query as the primary anchor, ensuring expansions do not deviate too far.
- **Sub-Query Decomposition**
- Break down a complex query into smaller sub-queries. For example:
    1. Identify sub-problems or sub-topics within a larger question.
    2. Retrieve information for each sub-problem individually, then combine or re-check the results for coherence \(often via a “Chain-of-Verification” to reduce hallucinations\).

Below is a high-level diagram illustrating how Query Expansion works:

```
\+-------------------\+           \+-------------------\+
|  User's Original  |  Query    |   Multi/ Sub-Query|   Expanded
|      Query        \+---------> |    Generation     \+--------\+
\+-------------------\+           \+-------------------\+        |
                                                             v
                                               \+--------------------------\+
                                               |  Expanded Query \#1       |
                                               \+--------------------------\+
                                               |  Expanded Query \#2       |
                                               \+--------------------------\+
                                               |  Expanded Query \#3       |
                                               \+--------------------------\+
                                                             |
                                                             v
                                               \+--------------------------\+
                                               | Retrieval & Aggregation  |
                                               \+--------------------------\+
                                                             |
                                                             v
                                                   \+----------------\+
                                                   |  Final Answer  |
                                                   \+----------------\+
```
### Important Considerations

1. **Cost and Performance**
    - Generating multiple queries increases the number of LLM calls, potentially raising inference costs and latency.
    - Additional retrieval operations \(e.g., searching the knowledge base multiple times\) also add overhead.
2. **Complexity**
    - Managing many parallel queries requires careful orchestration.
    - Merging or re-ranking the results can be non-trivial, especially when sub-queries overlap.
3. **Evaluation**
    - Need a robust way to evaluate the improved coverage and accuracy versus additional overhead.
    - Metrics like retrieval precision/recall or end-to-end question-answering quality are typically used.
4. **Maintaining User Intent**
    - Over-expansion can dilute the original question or introduce tangential content.
    - Use weighting and verification \(e.g., post-filtering by the original query\) to ensure expansions remain relevant.
5. **Hallucination Reduction**
    - Systems like Chain-of-Verification \(CoVe\) can validate expansions and final answers, reducing the risk of generating spurious content.

### Unique Benefits

- **Broader Coverage**
- By exploring multiple angles, the system is less likely to miss relevant documents or facts.
- **Deeper Context**
- Query expansions capture additional nuances and disambiguate key terms, boosting accuracy in retrieval.
- **Adaptive to Domain Jargon**
- Especially useful when dealing with fields that have specialized terminology, reducing misinterpretation of abbreviations and synonyms.
- **Scalable for Complex Problems**
- Sub-query decomposition enables large problems to be tackled in smaller, more manageable pieces, improving overall clarity and correctness.

By employing **Query Expansion**, retrieval-augmented generation \(RAG\) or any GenAI system can handle ambiguous, complex, or specialized questions more effectively—leading to more relevant, accurate, and context-rich answers.
