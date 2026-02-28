# Problem

Retrieval-Augmented Generation \(RAG\) systems often rely on the user’s **original** query to fetch relevant documents. However, users’ queries can be:

1. **Poorly worded or ambiguous**, causing retrieval to miss critical information.
2. **Complex**, especially for domain-specific topics or specialized vocabulary \(e.g., “LLM” might mean “Large Language Model” or “Master of Laws”\).
3. **Unstructured** with run-on sentences, extraneous details, or unclear objectives.

Without a strategy to clean, simplify, or reframe queries, these issues can undermine retrieval effectiveness and lead to low-quality or irrelevant results. This not only hampers user satisfaction but can also waste computational resources on fruitless searches.

**Why this pattern is necessary**

- **Improved Accuracy**: By transforming queries into clearer, more domain-aligned forms, you reduce ambiguity and increase the likelihood of retrieving relevant documents.
- **Scalability**: In large-scale RAG or enterprise search scenarios, each query needs to be processed efficiently and effectively to save time and cost.
- **User Experience**: Automating query transformation lowers the burden on users to perfectly formulate their questions, making the system more accessible.

---
# Condition

This pattern is most effective when:

1. **Users submit incomplete or ambiguous queries**. For instance, a question like “What should I do for LLM?” could refer to legal education or advanced AI models.
2. **The domain involves complex or specialized language**. Domain-specific jargon \(e.g., medical, legal, or technical terms\) often confuses general-purpose language models and retrieval systems.
3. **Long-tail or unique queries** are common. When users ask rare, verbose, or unusual questions, naive retrieval pipelines may fail to capture relevant documents.

**Example Use Cases**

- **E-commerce Search**: A user searches “shoes that are comfy and pinkish for running.” A query transformation module could rewrite this as “comfortable pink running shoes” to improve retrieval.
- **Technical Documentation**: A user queries “Set up K8, how?” The system might rewrite “K8” as “Kubernetes” to match the correct documentation.
- **Legal or Academic Research**: A user asks “LLM requirements for my career.” Query transformation can clarify whether the user is referring to a Master of Laws or Large Language Model courses, pulling in the correct references.

---
# Solution

**Core Idea**

Instead of sending the user’s original query directly into a retrieval system, a dedicated “Query Transformation” step rewrites, restructures, or synthesizes the query into multiple forms. These rewritten queries can better align with the indexing structures of the knowledge base or the embedding space, leading to higher-quality retrieval.

```
   \+---------------\+     Original Query
   |  User Input   |----------------------\+
   \+---------------\+                      |
                                          v
                                \+---------------------\+
                                |  Query Transformation|
                                \+---------------------\+
                                          |
                                          v
                           \+-----------------------------\+
                           |    Enhanced / Rewritten     |
                           |          Query\(ies\)         |
                           \+-----------------------------\+
                                          |
                                          v
                               \+-------------------\+
                               |  Retrieval Layer  |
                               \+-------------------\+
                                          |
                                          v
                               \+-------------------\+
                               |    Documents      |
                               \+-------------------\+
                                          |
                                          v
                              \+---------------------\+
                              |  LLM / RAG Response |
                              \+---------------------\+
```
1. **Rewrite**
    - The system prompts a language model \(or a specialized smaller model\) to rewrite the user query. It can simplify syntax, standardize terminology, and remove extraneous details.
    - **Example**: Taobao’s query rewrite method, which improved recall for long-tail queries.
2. **HyDE \(Hypothetical Document Embeddings\)**
    - Instead of embedding the raw query, the system first generates a hypothetical answer or “document” that might address the user’s query. It then encodes that hypothetical answer for retrieval.
    - **Benefit**: This focuses on answer-to-answer similarity, bridging semantic gaps that might exist between how a question is phrased and how an answer is typically described.
    - **Reverse HyDE**: Alternatively, generate hypothetical queries from each retrieved chunk, refining or clarifying them for improved matching.
3. **Step-back Prompting**
    - Abstract the original query into a “higher-level” concept query \(a step-back question\) and retrieve with both the original and the step-back queries.
    - Combine the results for a more comprehensive final answer. This technique helps cast a wider net, especially if the user’s original question was overly detailed or narrow.

## Important Considerations

1. **Cost**
    - Extra prompting to transform queries or generate hypothetical documents can increase token usage and inference time.
    - Balancing the added cost with the improvement in retrieval quality is crucial.
2. **Complexity**
    - Introducing multiple passes—such as rewriting or generating hypothetical documents—can complicate the system design.
    - A simpler approach \(like a single rewrite\) may suffice in some applications, whereas HyDE or step-back prompting introduces additional steps.
3. **Evaluation**
    - A/B testing transformed queries vs. direct queries helps assess improvements in retrieval recall and precision.
    - Tracking user satisfaction metrics \(click-through rates, time on page, etc.\) offers more holistic feedback.
4. **Domain-Specific Vocabulary**
    - Custom dictionaries or domain heuristics can further refine the rewriting process.
    - For highly specialized fields \(e.g., medical\), smaller domain-specific models might handle rewriting tasks more accurately than a general LLM.
5. **Security and Privacy**
    - Be mindful of transforming queries in domains with sensitive or regulated data. The rewriting process must not inadvertently expose private information or alter the user’s intent in a way that violates policy.

## Unique Benefits

- **Enhanced Retrieval**: By clarifying ambiguous language, systems achieve higher recall and precision.
- **Robustness to Variety**: Users can pose questions in multiple ways, yet the system remains consistently accurate.
- **Reduced User Burden**: Less reliance on perfect query formulation; the system handles linguistic nuances.
- **Scalable Adaptation**: Once the transformation pipeline is in place, it can easily adapt to new domains or specialized vocabularies with minimal user effort.

By applying Query Transformation, RAG and Gen AI systems become more resilient to the vast range of how humans actually ask questions. This pattern helps bridge the gap between human language and machine retrieval, ultimately delivering more accurate, context-rich responses.
