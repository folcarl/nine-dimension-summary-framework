---
name: nine-dimension-summary
description: Produce structured, critical, high-signal summaries from text, transcripts, articles, interviews, lectures, podcasts, research reports, notes, and user-provided video-derived content using the nine-dimension summary framework. Use for Chinese or English summarization, analysis, critique, material review, transcript cleanup review, and full or lightweight summary writing.
---

# Nine-Dimension Summary

Use this Codex-compatible adapter to apply the generic framework in `../../framework/` to source material. It turns source material into a clear Markdown summary that restores the material first, then analyzes its deeper problem, form, evidence, limits, implications, and quality.

## Workflow

1. Identify the input: pasted text, transcript, article, interview, lecture, report, research notes, or user-provided video-derived content.
2. Determine the output language from the user's request; if unspecified, match the source language.
3. Choose execution mode:
   - Use **full mode** for long interviews, dense lectures, political/history/economic/investment material, research reports, complex documentaries, major public events, long podcasts, batch tasks, or ambiguous cases.
   - Use **lightweight mode** only for short, low-density, low-complexity, low-stakes material.
4. Read only the references needed for the task:
   - If material type or mode is unclear, read `references/material-routing.md`.
   - For Chinese output, read `references/standard.zh.md`.
   - For English output, read `references/standard.en.md`.
   - Before shaping sections, read `references/output-contract.md`.
   - Before scoring, read `references/scoring-rubric.md`.
   - Before finalizing, read `references/completion-checklist.md`.
5. Write the summary in Markdown.
6. Run the completion checklist silently and revise before presenting the final answer or saving the output.

## Required Behavior

- Start with content restoration before evaluation.
- Do not turn the nine dimensions into a visible mechanical form unless the user asks for that.
- Preserve a readable essay-like flow while ensuring every required function is covered.
- Separate source claims, reasonable inferences, and externally unverified claims.
- Mark likely transcription errors, missing charts, unclear data口径, and claims requiring external verification.
- Do not claim external verification unless you actually performed it.
- For investment or economic material, frame implications as judgment support, not investment advice.
- When the input contains multiple materials, summarize each independently before writing any cross-material synthesis.

## Output Defaults

Use Markdown. Full mode normally includes core content, the real problem, form/viewing logic, evidence chain, critique and limits, verification boundary, implications, follow-up observations, and scored evaluation. Lightweight mode compresses this while keeping the core functions.
