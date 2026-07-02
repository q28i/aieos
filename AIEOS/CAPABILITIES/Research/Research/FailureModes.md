# Quantitative Research Capability Failure Modes

- If look-ahead bias is detected, immediately halt parameter tuning.
- If database connection times out, retry up to 3 times with exponential backoff.
