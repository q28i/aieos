# Knowledge Graph Memory Service

## Metadata
- **System**: AIEOS Core
- **Type**: Core Service
- **Status**: Core / Immutable
- **Version**: 1.0.0

## Purpose
Stores Goals, Vision, Relationships, Reasons, Decisions, Evidence, Concepts, Preferences, and active Assumption Registry.

## Subsystems & Components
- Concept Node Indexer
- Relationship Matrix Resolver
- Assumption Registry Tracker (Priority, Status, Last Validated)
- Experience Loop Repository (Experience -> Lessons -> Patterns -> Judgment)

## Operational Loop Workflow
- Index concepts, reasons, and decisions as node parameters rather than raw chats.
- Track active assumptions in a registry: score by Priority, Owner, Status, and validation history.
- Record Experience Loop parameters: catalog *why* past decisions worked to extract lessons and patterns.
