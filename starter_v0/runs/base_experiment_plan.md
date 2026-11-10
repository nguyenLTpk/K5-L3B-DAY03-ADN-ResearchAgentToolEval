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
