# Decision Readiness Protocol

## Metadata
- **System**: AIEOS Core
- **Type**: Cognitive Protocol
- **Status**: Core / Immutable
- **Version**: 1.0.0

## Purpose
Assesses if the project state has sufficient evidence, constraints, and risk mitigation to proceed, auditing Decision Reversibility.

## Subsystems & Components
- Evidence Completeness Checker
- Constraint Map Verifier
- Decision Reversibility Auditor (One-Way vs Two-Way Doors)

## Operational Loop Workflow
- Audit Decision Reversibility: classify decisions as reversible (proceed quickly) or irreversible (increase evidence threshold).
- Scan project files for unresolved contradictions and Type-1 assumptions.
- Verify the user has explored alternative gold/silver/titanium paths before releasing the lock state.
