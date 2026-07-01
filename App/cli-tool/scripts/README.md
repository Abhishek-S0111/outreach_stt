# Utility Scripts

This directory contains utility scripts for managing and debugging the Outreach Dashboard pipeline.

## Available Scripts

### `utils/inspect_record.py`
Inspect database records for a specific interaction.

**Usage:**
```bash
PYTHONPATH=. python scripts/utils/inspect_record.py <interaction_id>
```

**Example:**
```bash
PYTHONPATH=. python scripts/utils/inspect_record.py 6979fbb468f18e06ffe46303
```

**Output:**
- Metadata (village, sarpanch, date, etc.)
- Participant information
- Narration summary and details
- Key challenges
- Farmer questions
- Terminology mapping
- Conclusion

---

### `utils/regenerate_report.py`
Regenerate reports with updated LLM summary and conclusion for an existing interaction.

**Usage:**
```bash
PYTHONPATH=. venv/bin/python3 scripts/utils/regenerate_report.py
```

**What it does:**
1. Fetches interaction record from database
2. Regenerates summary if it shows "Summary generation failed"
3. Regenerates conclusion using LLM
4. Creates new PDF report with all fixes applied

**Note:** Edit the `IID` variable in the script to specify which interaction to regenerate.

---

## Common Workflows

### Debug a Failed Processing Job
```bash
# 1. Check the logs
tail -f logs/pipeline.log

# 2. Inspect the database record
PYTHONPATH=. python scripts/utils/inspect_record.py <interaction_id>
```

### Regenerate Report After Code Changes
```bash
# After fixing report generation code
PYTHONPATH=. venv/bin/python3 scripts/utils/regenerate_report.py
```
