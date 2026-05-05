## Development Workflow & Conventions

### Setup
*   **Dependencies:** Use `poetry install` to install dependencies listed in `pyproject.toml`.
*   **Virtual Environment:** The project uses a Poetry-managed environment.

### Quality Gates (Must run in order)
1.  **Formatting:** Run `black` first to ensure code style compliance across the repository.
2.  **Linting:** Run `flake8` to catch stylistic and pattern violations not covered by type checking.
3.  **Type Checking:** Run `mypy` to verify type correctness across the codebase.
4.  **Testing:** Run `pytest` with coverage to ensure functional correctness and measure test coverage.

### Developer Commands Summary
*   **Format Code:**
    \`black src\`
*   **Run Full Checks (Recommended):** Combine linting, typing, and testing in one sequence.
    \`black src && flake8 src && mypy src && pytest --cov=src --cov-report=term-missing --cov-report=html tests\`
*   **Test Execution:** By default, tests are expected to be run from the `tests/` directory using `pytest`.

### Architecture Notes
*   **Entry Point:** The primary execution script appears to be `run_game.py`.
*   **Directory Ownership:**
    *   `src/`: Contains the core application source code.
    *   `tests/`: Contains all unit and integration tests.
    *   `assets/`, `docs/`: Contain non-code resources.

**Notes:**
*   Do not assume that running `pytest` alone is sufficient; always use the full sequence of steps above for comprehensive validation.
*   The `pyproject.toml` configures `pytest` to check coverage specifically in the `src/` directory.
