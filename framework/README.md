# Framework Files

This directory is the generic, product-neutral version of the Nine-Dimension Summary Framework.

Use these files with any human workflow, AI assistant, agent runtime, writing pipeline, or custom application.

## Recommended Loading Order

1. Choose language:
   - Chinese: `standard.zh.md`
   - English: `standard.en.md`
2. Choose mode with `material-routing.md`.
3. Shape output with `output-contract.md`.
4. Score with `scoring-rubric.md`.
5. Run `completion-checklist.md` before finalizing.

## Default Workflow

```text
source text or transcript
-> choose material type and mode
-> restore content before evaluation
-> analyze form, evidence, critique, limits, and implications
-> produce Markdown summary
-> run completion checklist
```

Codex-compatible skill packages live in `../skills/`, but they are optional adapters.
