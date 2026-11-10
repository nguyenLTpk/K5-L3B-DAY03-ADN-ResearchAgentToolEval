# Lê Hải Anh (Role A): base-suite experiment

Scope: existing prompt/tool descriptions, version log v0-v3, base runs and report B1/B2. Tác giả: Lê Hải Anh (Role A).

Fixed setup: OpenRouter, `openai/gpt-4o-mini`, temperature 0, all 20 unchanged base cases, unchanged evaluator/provider/tool implementations. A run is eligible for comparison only when provider_error_cases=0 and measured_cases=total_cases=20.

1. v0: run the original prompt/tools. Save raw JSON and classify every failed case. Preserve the unsuccessful Gemini attempt separately; never combine it with OpenRouter results.
2. v1 (prompt only): eligibility before action. Hypothesis: deciding scope, required information and publication approval before acting removes the out-of-scope, missing-info and confirmation failures. Keep the single-tool restriction for isolation.
3. v2 (existing tool and parameter descriptions only): explicit contracts. Hypothesis: distinguishing tools and separating topic keywords from news/time arguments fixes argument mismatches, including R13, without changing names or schemas.
4. v3 (prompt only): independent-source coverage. Hypothesis: removing the single-tool restriction makes the instructions consistent with requests for multiple independent sources, preserving or improving complete call-set correctness. Baseline R13 already emitted both tools despite the restriction; this is a consistency/regression experiment, not a claim that v0 omitted a source.

Save byte-exact prompt/tools snapshots under `runs/base_artifacts/<version>/`. Record each hypothesis before its run. After each run, inspect routing failures and tool execution errors separately; do not edit outputs or retry merely to obtain a better score. Stop and consult the user for infrastructure errors. Validate tool contracts after declaration changes, verify snapshot hashes, unchanged base cases and absence of secrets before delivery.

Limitations: one run per version, no statistical confidence claim; subset matching of arguments; no_tool does not grade refusal wording; multi-turn history is serialized into one input. The runner makes one model completion and executes emitted calls serially without a model follow-up. Independent calls are not evidence of concurrent execution or complete research-answer quality.

## v3 hypothesis amendment, recorded after v2 and before v3

v1 and v2 both scored 19/20. In both runs R12 called clarify with response_type=text instead of yes_no; no send was attempted. Description changes alone did not resolve the overlapping prompt rules. The v3 experiment therefore replaces the planned independent-source experiment with a prompt-precedence experiment: explicitly route unapproved publication requests to the confirmation rule before applying the general missing-information rule, and limit the text rule to non-publication requests. All other instructions and v2 tool declarations stay unchanged. Hypothesis: removing this overlap fixes the remaining response_type mismatch without regressions.

The single-tool instruction is intentionally not changed in this experiment to avoid a second mechanism. It remains a known limitation for a later experiment even though the base multi-source case currently passes. No claims about a tested multi-source improvement will be made for v3.

## v4 and v5 plan, recorded after v3 and before either run

Context: B merged four new group tools (`wiki`, `hn_search`, `github_search`, `cite`) at the end of `artifacts/tools.yaml`, so the submitted `tools_hash` no longer matches run v3. The run labelled `v0_B_base_openrouter_20261110T180937971787.json` carries v3 hashes (`p04552040eeb2`, `ta01960b8f782`). It is a repeat of v3 under a wrong label and is not used as v0 evidence.

Same fixed setup as above: OpenRouter, `openai/gpt-4o-mini`, temperature 0, 20 unchanged base cases. Snapshots saved before running under `runs/base_artifacts/v4/` and `runs/base_artifacts/v5/`.

5. v4 (tools.yaml only: add the four group tools; existing descriptions and the v3 prompt unchanged). Expected artifact version `v4+p04552040eeb2+ta078bdccfe27`. Hypothesis: adding four tools with explicit when/when-not descriptions does not distract routing on the base suite, so v4 keeps 20/20 without regressions. Run with `--system-prompt runs/base_artifacts/v3/system_prompt.md`, because `artifacts/system_prompt.md` already holds the v5 prompt.
6. v5 (prompt only: replace the forced single-step / single-tool instruction, the remaining deliberate starter instruction). Expected artifact version `v5+pe1ddb4bfa9ee+ta078bdccfe27`. Hypothesis: allowing every needed tool for requests with several independent sources, while forbidding unneeded tools and premature format/cite calls, keeps 20/20 and removes the conflict between the prompt and multi-source requests such as R13, without adding unnecessary calls. Run with default artifact paths.

Comparison: v4 vs v3 (effect of the new tools), v5 vs v4 (effect of the prompt change). If v4 regresses, inspect the failed cases for routing to a new tool before running v5.
