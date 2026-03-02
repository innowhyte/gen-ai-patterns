# Compression

# Problem

**Excessive Context and Noise**

When multiple relevant documents are retrieved, the naive approach is to concatenate them all into a single prompt. This can lead to an overly long input, which introduces unnecessary noise for the language model. Instead of focusing on the most critical pieces of information, the model may be distracted by redundant or low-value details. This not only increases the computational costs (in terms of both token usage and inference time) but also can degrade model performance because the “signal” is buried in excessive “noise.”

**Why This Pattern Is Necessary**

Without an effective compression strategy, a RAG system can become:

1. **Costly** due to high token usage, especially when prompts exceed model token limits or approach them.
2. **Less Accurate** as the language model may struggle to identify and apply key details from a sprawling context.
3. **Slower** because processing large prompts invariably takes more time and resources.

---
# Condition

**Best Suitable When**

- The retrieval step produces _numerous or lengthy_ documents, causing input to approach or exceed maximum token limits.
- You see _diminishing returns_ from increasing context size (i.e., adding more text does not significantly improve accuracy or may worsen it).
- There is a need to _reduce inference cost_ and _latency_ by optimizing token usage.

**Example Use Cases**

1. **Knowledge-Base QA**: When a user’s question leads to retrieving multiple articles or lengthy documentation.
2. **Document Summarization**: Where the input is large and you want the language model to focus on the essence of the text rather than every sentence.
3. **Support Ticket Analysis**: Multiple related tickets might be retrieved, but only some paragraphs are truly relevant to the question or classification task.

---
# Solution

### Overview

**Compression** involves transforming or selecting the retrieved text so it remains _semantically informative_ but is _more concise._ Two notable approaches are:

1. **Small-Model-Based Compression** (“Long”LLMLingua approach):
    - A small language model (e.g., GPT-2 Small, LLaMA-7B) is employed to parse through the retrieved context.
    - The small model identifies and removes low-value tokens or phrases, resulting in a compressed representation.
    - This compressed text might look dense or less interpretable to humans but is still meaningful for large language models.
    - **Benefit**: No retraining of the main (large) language model is required. The alignment needed is primarily between the small model’s token-removal strategy and the main model’s understanding.
2. **Selective Context** (“Selective Context Approach”):
    - The system calculates the _self-information_ (or similar relevance metric) of lexical units based on an LLM or base language model.
    - Terms with _high self-information_ (i.e., truly informative or unique) are retained; those that are repetitive or add minimal value are removed.
    - **Benefit**: Often simpler to implement and ensures that only the high-impact tokens remain. However, it can miss important dependencies if the approach doesn’t account for context interactions.

Below is a simple conceptual diagram illustrating how **Compression** fits into a RAG pipeline:

```
        \+-------------------\+
        | User's Question   |
        \+---------\+---------\+
                  |
                  v
        \+-------------------\+
        | Retriever         |
        | (Documents)       |
        \+---------\+---------\+
                  |
                  v
   \+------------------------------\+
   | Compression Module          |
   | (Small Model or Self-Info)  |
   \+--------------\+---------------\+
                  |
                  v
        \+-------------------\+
        | Compressed Prompt |
        | to LLM           |
        \+---------\+---------\+
                  |
                  v
        \+-------------------\+
        | LLM Inference     |
        \+-------------------\+
```
### Important Considerations

1. **Model Alignment**
    - If using a small language model to compress, ensure it aligns well with the main LLM’s understanding. Over-aggressive token removal might confuse the larger model.
2. **Information Loss**
    - Compression always risks removing details that might be crucial for certain queries. Balance compression ratio with the need for completeness.
3. **Computational Cost**
    - While compression reduces the cost of the final prompt to the large model, it _adds a small overhead_ for the compression step itself (e.g., running a small model).
4. **Evaluation Strategy**
    - Track performance metrics (e.g., correctness, factuality) before and after compression to ensure minimal or acceptable degradation.
5. **Complexity**
    - Implementations can range from simple keyword or self-information filtering to more sophisticated token-level classification using a small fine-tuned model.

### Unique Benefits of the Pattern

- **Reduced Token Footprint**: Saves on inference costs in pay-per-token settings (e.g., API-based large language models) and allows for more extended reasoning within the same budget.
- **Focused Context**: Reduces the noise that can mislead or distract the language model’s reasoning process.
- **Better Scalability**: As the number and size of documents grow, compression helps maintain feasible token limits.
- **Improved Performance**: Counterintuitively, _less_ (when carefully selected) can lead to more accurate responses due to improved signal-to-noise ratio in the prompt.

---
By carefully applying **Compression**, RAG-based systems can harness the benefits of broad retrieval (to capture all potentially relevant information) while ensuring the large language model remains focused on the core information it needs to produce high-quality responses.
