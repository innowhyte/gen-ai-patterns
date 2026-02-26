---
name: pattern-thought-refiner
description: Refine a user's raw pattern idea into the repository's pattern template using a strict, no-hallucination interview process. Use when the user has incomplete notes, brainstorms, or rough thoughts about a GenAI pattern and needs a high-quality, challenge-tested draft. Enforce required sections, ask targeted follow-up questions, challenge vague claims, and require evidence or explicit uncertainty labels instead of filling gaps. Also use when the user wants claim verification, external validation, or stress-testing of whether the pattern is actually tested in practice.
---

# Pattern Thought Refiner

Execute this workflow in order.

## 1) Collect the Raw Input

1. Ask for the user's raw notes, statements, and any supporting links.
2. Ask where the final pattern should be written.
3. If the user does not provide a path, propose one in the appropriate pattern group folder.

## 2) Load Repository Constraints

1. Read `pattern-template.md` from the repository root.
2. Read `references/pattern_quality_checklist.md` from this skill.
3. Use these constraints as hard gates for quality and completeness.

## 3) Run Coverage Check

1. Run `scripts/check_pattern_sections.py <candidate-file-or-text-file>` if a draft exists.
2. If no draft exists, use `assets/pattern-draft-template.md` as the starting point.
3. Do not write final prose for sections that are missing user evidence.

## 4) Interview Before Writing

1. Ask only the highest-leverage missing questions first.
2. Use `references/challenge_questions.md` to pick focused questions.
3. Require concrete answers for:
   - Problem scope and failure symptom
   - Trigger conditions and explicit non-conditions
   - Step-by-step solution mechanics
   - One implementation-grade example
4. If the user gives a generic answer, ask for measurable details.

## 5) Enforce No-Hallucination Drafting

1. Convert only confirmed user statements into the pattern draft.
2. When information is unknown, keep explicit placeholders like `[NEEDS USER INPUT: ...]`.
3. Never invent benchmarks, incidents, citations, or outcomes.
4. Keep language specific and implementation-oriented.

## 6) Claim Audit and Verification Plan

1. Run `scripts/claim_audit.py <draft-file>` to detect claims that need proof.
2. For each flagged claim, ask the user for one of:
   - Internal evidence (metric, experiment, incident)
   - Public source (paper, docs, benchmark)
   - Rewording to a bounded, uncertain claim
3. If browsing tools are available, verify cited external claims before finalizing.
4. If a claim cannot be verified, mark it as unverified in the draft.

## 7) Final Quality Gate

1. Validate required template sections are present and non-empty.
2. Confirm `Condition` includes both when-to-use and when-not-to-use.
3. Confirm `Solution` is procedural, not conceptual marketing text.
4. Confirm `Example` is specific enough to implement.
5. Confirm optional sections are included only when concrete.

## 8) Deliver Output

1. Write or update the final markdown file.
2. Provide a short list of unresolved questions, if any.
3. Summarize which claims were verified, unverified, or softened.
