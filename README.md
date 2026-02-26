# Gen-AI Patterns

A practical collection of patterns for building GenAI systems.

This repo is meant to be useful, not academic.  
Each pattern focuses on when to use it, how to apply it, and what to watch out for.

## Current pattern groups

- Chunking
  - [Metadata Attachment](chunking_patterns/metadata_attachment.md)
  - [Sliding Window](chunking_patterns/sliding_window.md)
  - [Small-to-Big](chunking_patterns/small_to_big.md)
- Evaluation
  - [Human as Judge](evaluation_patterns/human_as_a_judge.md)
  - [Model as Judge](evaluation_patterns/model_as_a_judge.md)
  - [Structured Output Evaluation](evaluation_patterns/structured_output_evaluation.md)
  - [User as Judge](evaluation_patterns/user_as_a_judge.md)
- Extraction
  - [Long Document Structured Extraction](extraction_patterns/long_document_structured_extraction.md)

## How to use this repo

1. Start with the problem you are trying to solve.
2. Pick a pattern that matches your constraints.
3. Adapt it to your use case.
4. Document what worked and what failed.

## Contributing

Contributions are welcome, especially:
- new patterns with real-world examples
- improvements to existing patterns
- clear tradeoffs and failure cases

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a PR.

## Ground rule

Clarity over hype.  
If a pattern looks good in theory but fails in practice, document that.
