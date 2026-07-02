# Verification & Code Review Capability Contract

## Core Purpose
Audit code quality, verify security practices, and ensure interface compliance.

## Quality Gates
- **Entry Preconditions**: Completed code patch and successful compile logs
- **Required Context**: Constitution_Security, Constitution_Quality, and requirements brief
- **Execution Instructions**: Trace variable scopes, scan for credentials, and review functional tests
- **Verification Assertions**: Confirm tests cover at least 80% of new code pathways
- **Exit Requirements**: Code review audit markdown with explicit status metrics
