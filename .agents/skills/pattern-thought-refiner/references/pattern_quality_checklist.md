# Pattern Quality Checklist

Use this checklist before finalizing any pattern.

## Required Section Quality

- `Problem`: Names one concrete pain point and who experiences it.
- `Condition`: Includes both "use when" and "do not use when" conditions.
- `Solution`: Gives procedural steps with execution detail.
- `Example`: Includes enough specifics (context, steps, outcome) for implementation.

## Precision Rules

- Prefer bounded language over absolutes.
- Replace vague terms (`better`, `faster`, `scalable`) with measurable context.
- Avoid copying generic best-practice text without user-provided evidence.

## Tradeoffs and Failure Modes

Add only when concrete:

- `Tradeoffs`: Must include at least one gain and one cost that are context-specific.
- `Failure Modes`: Must describe realistic break points and early warning signs.

## Evidence Rules

- Every high-confidence claim must map to a source:
  - User-provided experiment/metric
  - Internal postmortem or production signal
  - External source with citation
- If no source exists, mark as unverified or rewrite with uncertainty.
