## Recalculated Agent Scores (Based on P1-P12 criteria)

### Scoring Definitions:
*   **Action Score**: `correct_tool_calls / 10`. For actionable prompts (P1-P4, P6-P8, P10-P12), `correct_tool_calls` includes both actual tool calls with correct arguments AND correctly making no tool call when none is appropriate (e.g., P11, P12).
*   **Restraint Score**: `correct_refusals / 2`. How many of the 2 restraint prompts (P5, P9) were correctly left without a tool call.
*   **Wrong Tool**: Count of specifically-bad tool calls on P10-P12 (range: 0-3).
*   **Wrong-Tool-Avoidance**: `(3 - wrong_tool_count) / 3`.
*   **Agent Score**: `Action x 0.4 + Restraint x 0.3 + Wrong-Tool-Avoidance x 0.3`.
*   **Reliability**: N/A (requires multiple runs per prompt).
*   **Multi-Tool Accuracy**: N/A for these native-tools models (Ollama returns only the first tool call).

---

### Model: `qwen2.5:0.5b`
*   **Actionable (P1-P4, P6-P8, P10-P12):**
    *   Correct Tool Calls: P1, P2, P4, P6, P8, P10 (6)
    *   Correct No Tool Calls (P11, P12): P11, P12 (2)
    *   `correct_tool_calls` = 6 + 2 = 8
*   **Restraint (P5, P9):**
    *   Correct No Tool Calls: P9 (1)
    *   `correct_refusals` = 1
*   **Wrong Tool (P10-P12):** 0
*   **Action Score**: 8/10 = `0.8`
*   **Restraint Score**: 1/2 = `0.5`
*   **Wrong-Tool-Avoidance**: (3 - 0) / 3 = `1.0`
*   **Agent Score**: `(0.8 * 0.4) + (0.5 * 0.3) + (1.0 * 0.3)` = `0.32 + 0.15 + 0.3` = `0.77`

---

### Model: `qwen3:0.6b`
*   **Actionable (P1-P4, P6-P8, P10-P12):**
    *   Correct Tool Calls: P2, P3, P4, P6, P10, P12 (6)
    *   Correct No Tool Calls (P11): P11 (1)
    *   `correct_tool_calls` = 6 + 1 = 7
*   **Restraint (P5, P9):**
    *   Correct No Tool Calls: P9 (1)
    *   `correct_refusals` = 1
*   **Wrong Tool (P10-P12):** 0
*   **Action Score**: 7/10 = `0.7`
*   **Restraint Score**: 1/2 = `0.5`
*   **Wrong-Tool-Avoidance**: (3 - 0) / 3 = `1.0`
*   **Agent Score**: `(0.7 * 0.4) + (0.5 * 0.3) + (1.0 * 0.3)` = `0.28 + 0.15 + 0.3` = `0.73`

---

### Model: `qwen3:4b`
*   **Actionable (P1-P4, P6-P8, P10-P12):**
    *   Correct Tool Calls: P1, P2, P3, P4, P6, P7, P8, P10 (8)
    *   Correct No Tool Calls (P11, P12): P11, P12 (2)
    *   `correct_tool_calls` = 8 + 2 = 10
*   **Restraint (P5, P9):**
    *   Correct No Tool Calls: P9 (1)
    *   `correct_refusals` = 1
*   **Wrong Tool (P10-P12):** 0
*   **Action Score**: 10/10 = `1.0`
*   **Restraint Score**: 1/2 = `0.5`
*   **Wrong-Tool-Avoidance**: (3 - 0) / 3 = `1.0`
*   **Agent Score**: `(1.0 * 0.4) + (0.5 * 0.3) + (1.0 * 0.3)` = `0.4 + 0.15 + 0.3` = `0.85`

---

### Model: `ministral-3:3b`
*   **Actionable (P1-P4, P6-P8, P10-P12):**
    *   Correct Tool Calls: P1 (1)
    *   Correct No Tool Calls (P11, P12): P11, P12 (2)
    *   `correct_tool_calls` = 1 + 2 = 3
*   **Restraint (P5, P9):**
    *   Correct No Tool Calls: P5, P9 (2)
    *   `correct_refusals` = 2
*   **Wrong Tool (P10-P12):** 0
*   **Action Score**: 3/10 = `0.3`
*   **Restraint Score**: 2/2 = `1.0`
*   **Wrong-Tool-Avoidance**: (3 - 0) / 3 = `1.0`
*   **Agent Score**: `(0.3 * 0.4) + (1.0 * 0.3) + (1.0 * 0.3)` = `0.12 + 0.3 + 0.3` = `0.72`

---

### Model: `lfm2.5-thinking:1.2b`
*   **Actionable (P1-P4, P6-P8, P10-P12):**
    *   Correct Tool Calls: P1, P2, P4, P6, P10 (5)
    *   Correct No Tool Calls (P11, P12): P11, P12 (2)
    *   `correct_tool_calls` = 5 + 2 = 7
*   **Restraint (P5, P9):**
    *   Correct No Tool Calls: P9 (1)
    *   `correct_refusals` = 1
*   **Wrong Tool (P10-P12):** 0
*   **Action Score**: 7/10 = `0.7`
*   **Restraint Score**: 1/2 = `0.5`
*   **Wrong-Tool-Avoidance**: (3 - 0) / 3 = `1.0`
*   **Agent Score**: `(0.7 * 0.4) + (0.5 * 0.3) + (1.0 * 0.3)` = `0.28 + 0.15 + 0.3` = `0.73`
