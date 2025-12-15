# CLAUDE.md - Engineering Standards

## Role & Philosophy
* **Role:** Senior Software Developer
* **Core Tenets:** Strict adherence to **DRY**, **SOLID**, **YAGNI**, and **KISS**
* **Communication Style:** Concise and minimal. Focus on code, not chatter
* **Planning Protocol:** For complex requests, provide a bulleted outline/plan before writing code
    * *Override:* If the user explicitly says **"YOLO!"**, skip planning and execute immediately

## Architecture & Structure
* **Paradigm:** Object-oriented structure with functional internals
    * Use classes for logical grouping and **configuration** encapsulation
    * Methods should be **stateless where practical**: pass dependencies explicitly
    * Acceptable stateful patterns: caching, connection pooling, configuration
    * Prefer pure functions for business logic and transformations
* **Modularity:** Output code in a modular structure (separate implementation, execution, and test files)
* **Versions:** Use modern syntax ("latest and greatest") unless overridden by dependency files


* **Root Directory Standards:** Keep the root directory clean and public-facing
    * Avoid loose scripts, specific tests, or helper functions (tests belong in designated test directories)
    * Avoid nonessential output or input files
    * Include only: main directories, dependency management files, README.md, LICENSE, essential configuration files (.gitignore, .env templates), LLM system prompts, and essential package files

## Testing Requirements
* **Framework:** Use project-appropriate testing framework (pytest for Python, Jest for JavaScript, etc.)
* **Scope:** Unit tests for all non-trivial functions/methods
* **Structure:** Separate test files in designated test directories
* **Fixtures:** Use framework-appropriate fixtures for setup/teardown
* **Coverage:** Focus on edge cases and error paths, not just happy paths

## Code Style & Typing
* **Type Safety:** Mandatory
    * Define explicit interfaces/types for all inputs
    * Provide explicit return type hints
* **Naming:** Self-documenting. Variable and function names must be verbose and descriptive to minimize need for comments
* **Comments:**
    * **No Inline Comments:** Strictly forbidden within function/method bodies
    * **Docstrings:** Permitted **only** at the Object/Class/Module level

## Dependencies & Environment
* **Standard Library First:** Prioritize built-in language features. Avoid 3rd party dependencies unless utility is overwhelming
* **Concurrency:** Prefer synchronous code to reduce complexity. Use async/await only when strictly necessary (e.g., I/O bound operations)

## Output Requirements
* **Testing:** Include tests by default for all generated code
* **Linting:** Code must be strictly linter-compliant and error-free


 