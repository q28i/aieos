# Contributing to AIEOS

We welcome contributions from the community to help make AIEOS a robust Decision Operating System!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/aieos/aieos.git
   cd aieos
   ```

2. Initialize a local workspace:
   ```bash
   python aieos.py init
   ```

3. Run diagnostic audits:
   ```bash
   python aieos.py doctor
   ```

## Commit Guidelines

We enforce the **Conventional Commits** specification for release tagging and changelog updates:
- `feat`: A new feature or command.
- `fix`: A bug fix.
- `docs`: Documentation updates.
- `refactor`: Code restructuring without functional modifications.
- `test`: Adding or upgrading test cases.
