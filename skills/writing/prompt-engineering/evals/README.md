# Prompt Engineering Pattern Evaluations

Systematic testing and validation framework for prompt engineering patterns. Each eval case isolates a single pattern, defines clear inputs and expected outputs, and applies scoring criteria to measure effectiveness.

## Purpose

Prompt patterns are only useful if they reliably produce better results. This evaluation framework:

- **Validates patterns** — confirms each technique (CoT, few-shot, role-playing, etc.) delivers measurable improvement over naive prompting
- **Catches regressions** — detects when model updates or prompt changes degrade output quality
- **Benchmarks alternatives** — compares variants of the same pattern (e.g., 3-shot vs 5-shot) with consistent inputs
- **Documents expectations** — serves as living documentation of what each pattern should achieve

## Eval Structure

Each evaluation case in `eval_cases.json` tests **one pattern** with this structure:

| Field                      | Type       | Description                                              |
| -------------------------- | ---------- | -------------------------------------------------------- |
| `id`                       | `string`   | Unique identifier (`pattern-name-NN`)                    |
| `pattern`                  | `string`   | Pattern being tested                                     |
| `description`              | `string`   | What this case validates                                  |
| `input`                    | `string`   | The full prompt sent to the model                        |
| `expected_output_contains` | `string[]` | Substrings or phrases the output must include            |
| `criteria`                 | `string[]` | Human-readable quality criteria for pass/fail judgement   |
| `difficulty`               | `string`   | `easy`, `medium`, or `hard`                              |

### Example

```json
{
  "id": "chain-of-thought-01",
  "pattern": "chain-of-thought",
  "description": "Test CoT prompting for multi-step math reasoning",
  "input": "Let's think step by step. What is 15% of 240?",
  "expected_output_contains": ["step", "36"],
  "criteria": ["shows intermediate reasoning", "arrives at correct answer"],
  "difficulty": "easy"
}
```

## Running Evals

### Manual Execution

1. Load `eval_cases.json` and iterate over each case.
2. Send the `input` to the target model.
3. Check the response against `expected_output_contains` (substring match, case-insensitive).
4. Evaluate `criteria` with human review or an LLM-as-judge pass.

```bash
# Example: run with a simple Python script
python scripts/run_evals.py --cases evals/eval_cases.json --model gpt-4

# Run a single pattern
python scripts/run_evals.py --cases evals/eval_cases.json --pattern chain-of-thought

# Run by difficulty
python scripts/run_evals.py --cases evals/eval_cases.json --difficulty easy
```

### CI Integration

Add to your CI pipeline to catch prompt regressions:

```yaml
# .github/workflows/prompt-evals.yml
- name: Run prompt pattern evals
  run: python scripts/run_evals.py --cases evals/eval_cases.json --fail-threshold 0.8
```

Set `--fail-threshold` to the minimum pass rate (0.0–1.0). The pipeline fails if the overall score drops below it.

## Adding New Evals

Use this template when adding a new evaluation case:

```json
{
  "id": "<pattern>-<NN>",
  "pattern": "<pattern-name>",
  "description": "<what this case specifically validates>",
  "input": "<the exact prompt to send>",
  "expected_output_contains": ["<required substring 1>", "<required substring 2>"],
  "criteria": ["<quality check 1>", "<quality check 2>"],
  "difficulty": "easy | medium | hard"
}
```

**Guidelines for new cases:**

1. **One pattern per case** — don't mix CoT with few-shot in a single eval
2. **Specific expectations** — `expected_output_contains` should be concrete, not vague
3. **Reproducible inputs** — the `input` field should be self-contained (no external dependencies)
4. **Graduated difficulty** — include easy, medium, and hard variants for each pattern
5. **Distinct from existing cases** — check current cases to avoid redundancy

## Scoring

Each eval case produces one of three results:

| Result      | Meaning                                                        | Score |
| ----------- | -------------------------------------------------------------- | ----- |
| **Pass**    | All `expected_output_contains` found AND all `criteria` met    | 1.0   |
| **Partial** | Some `expected_output_contains` found OR some `criteria` met   | 0.5   |
| **Fail**    | No expected outputs found AND no criteria met                  | 0.0   |

### Aggregation

- **Per-pattern score** = average of all cases for that pattern
- **Overall score** = average of all per-pattern scores (equally weighted)
- **Pass threshold** = configurable, default 0.8 (80%)

### Interpreting Results

- **Score < 0.5** — pattern is unreliable; review prompt construction or switch models
- **Score 0.5–0.8** — pattern works inconsistently; consider refining the prompt or adding constraints
- **Score > 0.8** — pattern is production-ready for the tested scenarios
