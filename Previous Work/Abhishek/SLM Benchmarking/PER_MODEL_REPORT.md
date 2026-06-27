## Updated Agent Scores (Based on all 30 prompts)

### Scoring Definitions
*   **Prompt Coverage**: 30 prompts total.
*   **Tool-required prompts**: 21 prompts (P1-P4, P6-P8, P10, P17-P29).
*   **No-tool prompts**: 9 prompts (P5, P9, P11-P16, P30).
*   **Action Score**: average correctness across the 21 tool-required prompts. Each prompt is scored as:
    *   `1.0` = fully correct tool use or fully correct conditional tool chain
    *   `0.5` = partially correct behavior (for example, one of two expected tools was used correctly, or the tool was invoked with incomplete/incorrect arguments)
    *   `0.0` = wrong tool, missing tool when one was needed, or an inappropriate no-call on a tool-required prompt
*   **Restraint Score**: average correctness across the 9 no-tool prompts. Each prompt is scored as:
    *   `1.0` = correctly abstained from tool use
    *   `0.0` = made a tool call when no tool call was expected
*   **Wrong-Tool-Avoidance**: `(9 - wrong_tool_count) / 9`, where `wrong_tool_count` counts the number of no-tool prompts on which the model made an inappropriate tool call.
*   **Agent Score**: `Action x 0.4 + Restraint x 0.3 + Wrong-Tool-Avoidance x 0.3`.
*   **Reliability**: N/A for this report; it requires repeated runs per prompt.
*   **Multi-Tool Accuracy**: N/A for these native-tools models because Ollama returns only the first tool call in practice.

---

### Model: `qwen2.5:0.5b`
*   **Action Score**: 17.5/21 = `0.83`
*   **Restraint Score**: 7/9 = `0.78`
*   **Wrong-Tool-Avoidance**: 7/9 = `0.78`
*   **Agent Score**: `(0.83 * 0.4) + (0.78 * 0.3) + (0.78 * 0.3)` = `0.33 + 0.23 + 0.23` = `0.80`

---

### Model: `qwen3:0.6b`
*   **Action Score**: 17.5/21 = `0.83`
*   **Restraint Score**: 7/9 = `0.78`
*   **Wrong-Tool-Avoidance**: 7/9 = `0.78`
*   **Agent Score**: `(0.83 * 0.4) + (0.78 * 0.3) + (0.78 * 0.3)` = `0.33 + 0.23 + 0.23` = `0.80`

---

### Model: `qwen3:4b`
*   **Action Score**: 21/21 = `1.00`
*   **Restraint Score**: 7/9 = `0.78`
*   **Wrong-Tool-Avoidance**: 7/9 = `0.78`
*   **Agent Score**: `(1.00 * 0.4) + (0.78 * 0.3) + (0.78 * 0.3)` = `0.40 + 0.23 + 0.23` = `0.87`

---

### Model: `ministral-3:3b`
*   **Action Score**: 7.5/21 = `0.36`
*   **Restraint Score**: 9/9 = `1.00`
*   **Wrong-Tool-Avoidance**: 9/9 = `1.00`
*   **Agent Score**: `(0.36 * 0.4) + (1.00 * 0.3) + (1.00 * 0.3)` = `0.14 + 0.30 + 0.30` = `0.74`

---

### Model: `lfm2.5-thinking:1.2b`
*   **Action Score**: 17.5/21 = `0.83`
*   **Restraint Score**: 7/9 = `0.78`
*   **Wrong-Tool-Avoidance**: 7/9 = `0.78`
*   **Agent Score**: `(0.83 * 0.4) + (0.78 * 0.3) + (0.78 * 0.3)` = `0.33 + 0.23 + 0.23` = `0.80`


### Summary of Model Performance Scores

| Model | Action Score | Restraint Score | Wrong-Tool-Avoidance | Agent Score |
|:---------------------|:-------------|:----------------|:---------------------|:------------|
| `qwen2.5:0.5b`       | 0.83         | 0.78            | 0.78                 | 0.80        |
| `qwen3:0.6b`         | 0.83         | 0.78            | 0.78                 | 0.80        |
| `qwen3:4b`           | 1.00         | 0.78            | 0.78                 | 0.87        |
| `ministral-3:3b`     | 0.36         | 1.00            | 1.00                 | 0.74        |
| `lfm2.5-thinking:1.2b` | 0.83         | 0.78            | 0.78                 | 0.80        |