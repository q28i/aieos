# Asynchronous Event Bus

## Metadata
- **System**: AIEOS Core
- **Type**: Core Service
- **Status**: Core / Immutable
- **Version**: 1.0.0

## Purpose
Decouples system communications using publish/subscribe event topics.

## Subsystems & Components
- Event Topic Router
- Subscriber Registry Broker
- Historical Execution Log Auditor

## Operational Loop Workflow
- Ingest event payloads containing ID, sender, and topic details.
- Dispatch event models to registered subscribers.
- Write audit telemetry logs to measure process delay metrics.
