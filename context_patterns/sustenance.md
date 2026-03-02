# Sustenance

> **Core Question:** How do I keep the context from rotting over time?

## Problem

Agent sessions don't stay short. Customer support conversations span dozens of turns. Research tasks accumulate hundreds of search results. Coding agents iterate through build-test-debug cycles for hours. With each turn, the context window grows, accumulating tool outputs, intermediate reasoning, superseded hypotheses, verbose error messages, and raw retrieval results.

Growing context causes three major failure modes.

- **Context distraction** - Long-running conversations and agent loops accumulate context continuously. Every message, every tool call, every intermediate result stays in the window. Eventually, the context is dominated by history rather than useful information. Attention gets spent re-reading old messages instead of focusing on the current task.
- **Context rot** - Not all information remains relevant over time. A file read in turn 5 may be deleted or changed by turn 40, but it still occupies equal token space. Old hypotheses that were later revised, verbose tool outputs that have been processed, and early small talks in conversation all accumulate without contributing to the current task.
- **Window exhaustion** - When a conversation ends, everything in it is gone. When you hit the window limit, old information gets pushed out. There might be some information that should persist across multiple sessions, such as user preferences, established decisions, learned constraints, etc. Losing it means starting from scratch every session.

## Condition

Use when:

- When agents have long-running sessions.
- When the agent makes frequent tool calls whose outputs (API responses, search results, database records) accumulate in context. Tool outputs are often verbose and redundant once processed.
- When the relevance of information decays over time. Real-time analytics, monitoring systems, and iterative design processes, where yesterday's data or early-session hypotheses may not be relevant or actively mislead current reasoning.
- When the relevance of information stays even after the session ends.
- When cost, latency, or edge deployment constraints make unbounded context growth impractical, even if the model could technically handle it.

Do not use when:

- Sessions are short and naturally remain within a high-signal context window.
- The task requires full verbatim history at all times (for example, legal transcript replay).

## Solution

### Periodic Context Compaction

When context reaches a threshold, stop, summarize what matters, and start a new context with that summary as the foundation.

- **Detect:** Monitor context length. Set a threshold well below the advertised limit (a good starting point is 60-70% of the effective window).
- **Summarize:** Extract the essential state, such as decisions made, current plan, key facts discovered, constraints established, work completed, and work remaining.
- **Restart:** Begin a new context with the summary as the opening, plus any specific artifacts (code, data) needed for the next step.
- **Discard:** The compacted summary replaces the original context. The agent continues from a lean, focused window. The full history can be archived externally if audit trails are required.

### Recency Management

The core intuition is that recency is a strong signal for relevance. What happened in the last five turns is often more relevant than what happened 30 turns ago. Keep the most recent N turns verbatim. Summarize the middle band into key points. Archive the oldest content externally, leaving only a brief reference in the active window.

```
Recent (full detail)  | Older (summarized)  | Oldest (archived externally)
<---------------------+---------------------+----------------------------->
Turn 45-50 verbatim   | Turns 20-44 summary | Turns 1-19 -> external store
                      |                     | Ref: "Initial research phase
                      |                     | concluded X. Full log in ledger."
```

### External Memory Offloading

Some information needs to outlive the session. User preferences, established decisions, learned constraints, and validated facts should not have to be rediscovered every time. Write them out before the session ends.

- **Scratchpad:** A tool the agent writes to and reads during the session. Keep validated facts and active work state outside the live conversation.
- **File-Based State:** For long-horizon tasks, externalize persistent state into files or structured stores. The agent reconstructs its working context from a state snapshot plus a fixed window of recent actions. Task duration is decoupled from context size.
- **Index in Context:** Keep a lightweight ledger in the active context that maps what has been offloaded and where to find it. The agent knows what is available without carrying the full content.
- **Cache Policy:** Cache stable context blocks and define invalidation triggers (document update timestamp, schema version change, or policy revision).

The compaction prompt must be tailored to the domain. A financial analysis agent needs to preserve numbers and sources. A customer support agent needs to preserve commitments and case details. Generic summarization discards exactly what matters.

## Example

A customer support agent handles a billing dispute that runs across 47 conversation turns. The user has changed their plan twice, received a partial refund, and is now asking why their current invoice is still incorrect.

By turn 30, the context window carries the full raw transcript of every exchange, three verbose API responses from the billing system, two failed tool calls with error traces, and an early product FAQ chunk that is no longer relevant to the issue. Token count is at 68% of the effective window and climbing.

At turn 30, the agent hits the compaction threshold. It stops, runs a compaction step with a domain-specific prompt that instructs it to preserve: the user's account ID, the two plan changes and their dates, the refund amount and status, the current open dispute, and any commitments made to the user. It is told to discard: the full transcript, processed billing API responses, failed tool call traces, and the FAQ chunk.

The new context opens with a 2k token summary. The agent continues from turn 31 with full awareness of what matters and none of the noise.

The validated facts (refund confirmed, plan change dates) are written to an external scratchpad. If the session ends and the user calls back the next day, the agent reads the scratchpad on session start rather than asking the user to repeat themselves.

```
Turn 1-30 (raw)
├── Transcript (14k)
├── Billing API responses (8k)
├── Failed tool traces (3k)
└── FAQ chunk (2k)
Total: 27k tokens

Compaction runs at turn 30
Compaction prompt: preserve decisions, commitments, account state. Discard the rest.

Turn 31 onwards (compacted)
├── Session summary (2k)       <- account ID, plan history, refund status, open dispute
└── Current task context (1k)  <- what the user is asking right now
Total: 3k tokens

External scratchpad
├── refund_confirmed: true, $42.00, processed 14 Feb
└── plan_change_dates: 3 Jan (Basic to Pro), 28 Jan (Pro to Business)
```

The key implementation detail is the compaction prompt. "Summarize this conversation" produces a generic paragraph that loses the account specifics. The prompt must name exactly what to extract, field by field, for the domain.

## Tradeoffs

- Better long-run stability, but extra complexity in memory lifecycle management.
- Lower token cost over time, but possible loss of nuance during compaction.
- Faster restarts, but risk of stale cached context if invalidation is weak.

## Failure Modes

- Compaction drops unresolved questions that were still actionable.
- Temporal decay rules remove constraints that are still valid.
- External memory accumulates contradictions without periodic integrity checks.

## References

- [Compress & Restart](https://contextpatterns.com/patterns/compress/)
- [Write Outside the Window](https://contextpatterns.com/patterns/write-outside/)
- [Context Caching](https://contextpatterns.com/patterns/context-caching/)
- [Temporal Decay](https://contextpatterns.com/patterns/temporal-decay/)
- [How to Fix Your Context](https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html)
