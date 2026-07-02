# Cognitive Bias Detection Policy

## Metadata
- **System**: AIEOS Core
- **Type**: Learning Policy
- **Status**: Core / Immutable
- **Version**: 1.0.0

## Purpose
Audits human and AI reasoning paths for cognitive biases, flagging potential loops like confirmation bias or planning fallacy.

## Subsystems & Components
- Bias Patterns Scanner
- Planning Fallacy Tracker
- Bias Intervention Proposer

## Operational Loop Workflow
- Scan active inputs and planning logs for bias footprints (Optimism Bias, Sunk Cost, Confirmation Bias).
- Flag detected bias instances clearly to the user.
- Provide balanced counter-arguments to de-bias the active reasoning trace.
