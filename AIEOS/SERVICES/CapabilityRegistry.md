# Capability Registry Service

## Metadata
- **System**: AIEOS Core
- **Type**: Core Service
- **Status**: Core / Immutable
- **Version**: 1.0.0

## Purpose
Exposes and indexes active capabilities based on tag metadata, maturity ratings, and historical confidence metrics.

## Subsystems & Components
- Capability Catalog Indexer
- Maturity Resolver Checker
- Performance Rating Scorer

## Operational Loop Workflow
- Register newly loaded capability directories and parse manifests.
- Answer Kernel capability queries with matching, validated contracts.
- Update capability confidence metrics based on verification histories.
