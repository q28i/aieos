# Architecture Constitution

## Metadata
- **System**: AIEOS Core
- **Type**: Constitution Document
- **Status**: Active / Immutable
- **Version**: 1.0.0

## Purpose
Structural rules enforcing modularity, clean interfaces, and DRY principles.

## Immutable Principles
- Subsystems must remain strictly decoupled; communication must happen through abstract interfaces.
- No circular dependencies are permitted under any condition.
- Architectural boundaries must be preserved; utility folders cannot serve as domain logic.
