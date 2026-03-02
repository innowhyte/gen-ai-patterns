# Structured Output Evaluation

## Problem

When your AI system generates structured outputs, simply checking for an exact match between the actual and expected output using a boolean comparison is not sufficient. During experimentation with different parameters, determining which output is better requires a numerical score.

However, evaluating structured outputs presents challenges, especially when dealing with diverse data types, multiple nesting levels, and arrays (where order may impact accuracy). This pattern outlines an approach to effectively assessing and scoring structured outputs.

\[REPHRASE\]: Allows focusing on examples with low numerical values, allows us to get some patterns, etc.

## Condition

- This pattern applies to any use case involving structured output.

## Use cases

- Invoice details extraction
- Candidates details extraction from a resume
- Citations for a RAG response

## Solution

## 1. Identify the Nature of the Structure

Understanding the structure of the output helps in choosing appropriate evaluation techniques. Common types include:

- **Tabular Data** (e.g., CSV, relational tables)
- **Key-Value Pairs** (e.g., JSON, dictionaries)
- **Nested Structures** (e.g., JSON with hierarchical elements, XML trees)
- **Array-based data** (e.g., lists of items, ordered sequences)

## 2. Identify the Different Data Types Involved

Structured outputs often contain multiple data types, each requiring different comparison methods:

- **Numerical Data** (e.g., integers, floats)
- **Categorical Data** (e.g., labels, classes)
- **Textual Data** (e.g., free-form text, descriptions)
- **Boolean Data** (e.g., true/false values)
- **Structured Objects** (e.g., nested JSON, lists of dictionaries)
- **Datetime Data**

## 3. Identify the Required Accuracy Measures

Accuracy evaluation depends on the goal of the comparison. Common measures include:

- **Structural Accuracy** – Comparing the format and layout of the output.
- **Exact Match** – Checking if values are identical.
- **Approximate Similarity** – Handling minor differences (e.g., floating-point errors, fuzzy matching).
- **Semantic Accuracy** – Comparing meanings rather than literal values.
- **Ordering Accuracy** – Measuring sequence consistency in ordered structures.
- **Statistical Accuracy** – Evaluating distribution similarity for numerical data.

## 4. Define Evaluation Metrics and Compute Similarity

Based on the structure and data types, apply the appropriate evaluation methods.

### A. Numerical Data

- **Mean Squared Error (MSE)** – Measures the average squared difference between numerical values.  
    _Example:_ Comparing predicted vs. actual temperature readings:  

    **Predicted:** `\[32.5, 34.0, 31.8\]`  

    **Actual:** `\[33.0, 35.5, 30.0\]`  

    **MSE:** `( (32.5 - 33.0)² \+ (34.0 - 35.5)² \+ (31.8 - 30.0)² ) / 3`

- **Mean Absolute Error (MAE)** – Computes absolute differences between values.  
    _Example:_ Same as above, but without squaring:  

    **MAE:** `( |32.5 - 33.0| \+ |34.0 - 35.5| \+ |31.8 - 30.0| ) / 3`

- **Pearson Correlation** – Measures linear relationship between numerical outputs.  
    _Example:_ Comparing sales numbers from two different stores over time.

- **Cosine Similarity** – Measures how similar two numerical vectors are.  
    _Example:_ Comparing the purchase behavior of two customers using product spending vectors.

- **Relative Error (RE)** – Expresses error relative to actual values.  
    _Example:_ Comparing sensor readings to expected values.


### B. Categorical Data

- **Exact Match Accuracy** – Percentage of exact matches between expected and predicted categories.  
    _Example:_ Comparing classification results for animal types:  

    **Predicted:** `\["cat", "dog", "bird"\]`  

    **Actual:** `\["cat", "dog", "dog"\]`  

    **Accuracy:** `2/3 = 66.67%`

- **F1 Score** – Balances precision and recall.  
    _Example:_ Evaluating model performance for a spam classifier.

- **Jaccard Similarity** – Measures set overlap.  
    _Example:_ Comparing predicted vs. actual clothing categories:  

    **Predicted:** `\{"jeans", "t-shirt", "hat"\}`  

    **Actual:** `\{"t-shirt", "jacket", "hat"\}`  

    **Jaccard Score:** `|\{"t-shirt", "hat"\}| / |\{"jeans", "t-shirt", "hat", "jacket"\}| = 2/4 = 50%`

- **Hamming Distance** – Counts differences in categorical sequences.  
    _Example:_ Comparing two DNA sequences:  

    **Seq1:** `"AGCT"`  

    **Seq2:** `"ACGT"`  

    **Hamming Distance:** `2` (positions 2 and 3 are different)

- **Mutual Information Score** – Measures information gain between two categorical distributions.  
    _Example:_ Evaluating how well one set of customer labels predicts another.


### C. Textual Data

- **Levenshtein Distance** – Measures how many edits (insertions, deletions, substitutions) are needed.  
    _Example:_  

    **Text1:** `"hello world"`  

    **Text2:** `"helo wrold"`  

    **Levenshtein Distance:** `2` (fix missing "l" and swap "o" and "r")

- **Jaccard Similarity** – Compares token overlap.  
    _Example:_ Comparing two news headlines.

- **Cosine Similarity (TF-IDF or Embeddings)** – Measures text similarity based on word frequency.  
    _Example:_ Checking similarity between job descriptions.

- **BLEU Score** – Evaluates machine translation.  
    _Example:_  

    **Reference:** `"The cat is on the mat."`  

    **Predicted:** `"The cat sits on a mat."`  

    **BLEU Score:** `high due to overlapping words`

- **ROUGE Score** – Measures recall-oriented similarity for summarization.  
    _Example:_ Comparing AI-generated summaries to human-written summaries.


### D. Boolean Data

- **Exact Match Accuracy** –  
    _Example:_  

    **Predicted:** `\[True, False, True, True\]`  

    **Actual:** `\[True, False, False, True\]`  

    **Accuracy:** `3/4 = 75%`

- **Matthews Correlation Coefficient (MCC)** –  
    _Example:_ Evaluating the accuracy of a model predicting a disease presence.

- **Jaccard Similarity** –  
    _Example:_ Comparing binary feature sets for two users.


### E. Datetime Data

- **Absolute Time Difference (Seconds/Minutes/Hours/Days)** –  
    _Example:_ Comparing timestamps of login events:  

    **Timestamp1:** `2024-01-10 12:30:00`  

    **Timestamp2:** `2024-01-10 12:35:00`  

    **Difference:** `5 minutes`

- **Relative Time Difference (Percentage of Time Span)** –  
    _Example:_ Measuring prediction errors in stock market forecasts.

- **Mean Absolute Time Error (MATE)** –  
    _Example:_ Comparing forecasted vs. actual delivery times.

- **Dynamic Time Warping (DTW)** –  
    _Example:_ Measuring similarity between two heartbeat time series with varying speeds.

- **Seasonal/Pattern-Based Similarity (Fourier Transform, DTW on Features)** –  
    _Example:_ Comparing daily energy consumption patterns.

- **Kendall’s Tau for Temporal Order Consistency** –  
    _Example:_ Checking if two ranked lists of project deadlines match in order.


### F. Structured Objects (Key-Value Pairs, JSON, Dictionaries)

- **Jaccard Similarity on Keys and Values** –  
    _Example:_  

    **JSON1:** `\{"name": "Alice", "age": 30, "city": "New York"\}`  

    **JSON2:** `\{"name": "Alice", "age": 31, "city": "San Francisco"\}`  

    **Jaccard Score:** `2/3 = 66.67%`

- **Cosine Similarity (Flattened Representation)** –  
    _Example:_ Comparing JSON objects by vectorizing their numeric/textual values.

- **Tree Edit Distance (TED)** –  
    _Example:_ Comparing two XML/JSON hierarchical structures.

- **Semantic Similarity (Embedding-Based)** –  
    _Example:_ Comparing product descriptions stored in JSON.


### G. Sequence/Array-Based Data

- **Longest Common Subsequence (LCS)** –  
    _Example:_ Comparing DNA sequences to find common subsequences.

- **Kendall’s Tau** –  
    _Example:_ Comparing ranking of athletes across two competitions.

- **Dynamic Time Warping (DTW)** –  
    _Example:_ Aligning two speech recognition waveforms.

- **Hamming Distance** –  
    _Example:_ Comparing binary sequences:  

    **Seq1:** `\[1, 0, 1, 1, 0\]`  

    **Seq2:** `\[1, 1, 1, 0, 0\]`  

    **Hamming Distance:** `2` (positions 2 and 4 differ)


After computing these similarity scores for each relevant data type, normalize them to a **0-1 range** and aggregate them into a **final single numerical score** using a weighted approach.

## 5. Preprocess Data for Comparison

Before applying evaluation metrics, normalize the structured data:

- **Normalize Keys** – Convert to lowercase, and sort alphabetically.
- **Handle Missing Values** – Impute or ignore based on the use case.
- **Convert Numerical Values** – Standardize (e.g., min-max scaling).
- **Tokenize Textual Data** – Remove stopwords, lemmatize for semantic comparison.

Finally, apply the evaluation metrics to compute the final **accuracy score** for structured output.

## Benefits

- When testing a dataset with numerous examples, assigning a numerical score helps pinpoint low-performing cases, making it easier to identify patterns where the application may be failing. This level of insight wouldn’t be achievable with a simple boolean evaluation.

## Tradeoffs

- More informative than boolean checks, but higher implementation effort.
- Better diagnosis across data types, but requires metric selection discipline.
- Stronger evaluation rigor, but added preprocessing and normalization overhead.

## Failure Modes

- Wrong metric chosen for a field type leads to misleading scores.
- Field weights are arbitrary and hide critical errors.
- Aggregated score looks good while specific critical fields fail.
- Preprocessing changes semantics and masks true output defects.

## Example

For invoice extraction, score each field by type and then aggregate:

- `invoice_total`: MAE with tolerance
- `vendor_name`: text similarity (embedding or token-based)
- `invoice_date`: absolute time difference
- `line_items`: sequence-aware comparison

Use explicit field weights so business-critical fields impact the final score more.
