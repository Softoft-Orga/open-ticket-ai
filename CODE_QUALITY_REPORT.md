# Code Quality Assessment and AI Agent Improvement Report

**Project:** Open Ticket AI  
**Date:** 2026-01-12  
**Assessment Type:** Code Quality & AI Agent Readiness

---

## Executive Summary

Open Ticket AI demonstrates **good to excellent** code quality with a well-structured monorepo architecture using uv workspaces. The project is **moderately well-suited for AI agent collaboration** with some areas for improvement.

**Overall Score: 7.5/10**

### Key Strengths
- ✅ Clear architectural documentation (AGENTS.md, ASTRO.md)
- ✅ Comprehensive agent guidelines for both Python and frontend work
- ✅ Strong typing with modern Python 3.13+ (PEP 695)
- ✅ Well-organized monorepo structure with clear separation
- ✅ Good CI/CD automation with quality gates
- ✅ No code comments (as per guidelines) - clean code approach
- ✅ Excellent test organization structure
- ✅ Modern frontend stack (Astro 5 + Vue 3)
- ✅ Component documentation with Storybook

### Key Areas for Improvement
- ⚠️ Test directory `__init__.py` files violate stated guidelines
- ⚠️ Missing comprehensive CONTRIBUTING.md
- ⚠️ No automated test coverage reporting in CI
- ⚠️ Limited inline documentation for complex logic
- ⚠️ No automated dependency vulnerability scanning
- ⚠️ Frontend lacks TypeScript tests

---

## Detailed Analysis

### 1. Repository Structure & Organization (8/10)

#### Strengths
- **Clear monorepo layout** with uv workspace management
- **Logical separation** between core (`src/`), packages (`packages/`), tests (`tests/`), and docs (`docs/`)
- **Consistent package structure** across all workspace members
- **Well-defined documentation hierarchy** in `/docs`

#### Issues Found
```
Severity: MEDIUM
Issue: Test directories contain __init__.py files
Location: 
  - packages/otai_base/tests/loggers/__init__.py
  - packages/otai_base/tests/template_renderers/__init__.py
  - packages/otai_base/tests/ai_classification_services/__init__.py
  - tests/e2e/test_util/__init__.py
  - tests/e2e/__init__.py
  - tests/__init__.py

Impact: Violates stated guidelines in AGENTS.md
Guidelines state: "NO __init__.py files in test directories"
```

#### Recommendations
1. **Remove all `__init__.py` files from test directories** - This is explicitly forbidden in AGENTS.md and can cause import issues
2. **Add pre-commit hooks** to prevent `__init__.py` files in test directories
3. **Create a STRUCTURE.md** document with an ASCII tree showing the canonical layout
4. **Add automated structure validation** in CI to enforce guidelines

### 2. Code Quality - Python (8.5/10)

#### Metrics
- **Total Python files:** ~150
- **Source code lines:** ~2,986 (src: 1,650 + packages: 1,336)
- **Test code lines:** ~6,059
- **Test-to-code ratio:** ~2.0:1 (Excellent)
- **Type ignore comments:** 1 (Excellent)
- **TODO/FIXME comments:** 0 (Excellent)

#### Strengths
- **Modern Python 3.13+** with PEP 695 type parameters
- **Strong typing** throughout the codebase
- **Pydantic v2** for data validation
- **Dependency Injection** using Injector library
- **Clean code** - no comments as per guidelines
- **Comprehensive linting** with ruff (extensive ruleset)
- **Type checking** with mypy
- **Good separation of concerns** with clear abstractions

#### Code Sample Analysis
From `src/open_ticket_ai/core/dependency_injection/component_registry.py`:
```python
def find[T: Injectable](self, *, by_type: type[T]) -> dict[str, type[T]]:
    return {registry_id: cls for registry_id, cls in self._injectables.items() if issubclass(cls, by_type)}
```
- ✅ Modern PEP 695 generics
- ✅ Clear naming
- ✅ Type safety

#### Issues Found
```
Severity: LOW
Issue: Python version inconsistency
Location: pyproject.toml vs AGENTS.md
Details:
  - pyproject.toml: requires-python = ">=3.14"
  - AGENTS.md: "Python version: **3.13** only"
  - .python-version file may differ

Impact: Confusion for AI agents and developers
```

#### Recommendations
1. **Align Python version requirements** across all documentation and config files
2. **Add ruff format check to pre-commit hooks** for consistent formatting
3. **Enable stricter mypy settings** - currently `strict = false` in pyproject.toml
4. **Add complexity metrics** (e.g., cyclomatic complexity) to CI
5. **Consider adding docstrings to public APIs** - while code comments are forbidden, API documentation is valuable
6. **Add architectural decision records (ADRs)** for major design choices
7. **Create a DESIGN_PATTERNS.md** documenting common patterns used (DI, composition, etc.)

### 3. Test Infrastructure (7/10)

#### Strengths
- **Well-organized test hierarchy** (unit/integration/e2e)
- **Excellent test-to-code ratio** (~2:1)
- **Package-local tests** in appropriate locations
- **Comprehensive pytest configuration**
- **Good fixture organization** across multiple conftest.py files
- **Test markers** for categorization (unit, integration, e2e, slow)
- **Async test support** configured

#### Metrics
- **Test files:** 44 (26 root + 18 packages)
- **conftest.py files:** 7
- **Coverage target:** 90% (configured but not enforced in CI output)

#### Issues Found
```
Severity: HIGH
Issue: Forbidden __init__.py files in test directories
Location: Multiple test directories (see Section 1)
Impact: 
  - Violates stated architectural rules
  - Can cause pytest import confusion
  - Misleads AI agents about project structure

Severity: MEDIUM
Issue: No visible coverage reporting in CI workflow
Location: .github/workflows/ci-quality-assurance.yml
Details: Coverage is generated but not shown in PR comments
Impact: Developers/AI agents cannot see coverage impact of changes
```

#### Recommendations
1. **Remove all `__init__.py` from test directories immediately**
2. **Add coverage reporting to PR comments** using a GitHub Action
3. **Add coverage badge** to README.md
4. **Create test writing guidelines** documenting fixture naming conventions
5. **Add mutation testing** (e.g., mutmut) to verify test quality
6. **Document existing fixtures** in a central location for discoverability
7. **Add performance benchmarks** for critical paths
8. **Create integration test documentation** explaining what requires integration vs unit tests

### 4. Documentation (7.5/10)

#### Strengths
- **Excellent agent-specific documentation** (AGENTS.md, docs/AGENTS.md)
- **Clear component inventory** (COMPONENTS.md)
- **Content collections documentation** (CONTENT_COLLECTIONS.md)
- **Storybook for UI components** (11 stories)
- **Image usage guidelines** (IMAGE_USAGE_EXAMPLES.md)
- **Good README** with quick start

#### Metrics
- **Markdown files:** 52 total, 39 in docs/
- **Vue components:** 18
- **Storybook stories:** 11
- **Story coverage:** ~61% (11/18 components)

#### Issues Found
```
Severity: MEDIUM
Issue: Missing critical documentation files
Missing:
  - CONTRIBUTING.md (for contributors)
  - ARCHITECTURE.md (system overview)
  - SECURITY.md (security policy)
  - CHANGELOG.md (version history)
  - API.md (public API reference)

Severity: LOW
Issue: Incomplete Storybook coverage
Details: 18 components but only 11 stories (61% coverage)
Impact: AI agents cannot reference examples for all components
```

#### Recommendations
1. **Create CONTRIBUTING.md** with:
   - Development setup instructions
   - Code review process
   - Testing requirements
   - Style guide references
   - How to submit PRs
2. **Create ARCHITECTURE.md** with:
   - System overview diagram
   - Data flow diagrams
   - Plugin architecture explanation
   - Component interaction diagrams
3. **Add SECURITY.md** with vulnerability reporting process
4. **Add CHANGELOG.md** following Keep a Changelog format
5. **Complete Storybook coverage** for all Vue components
6. **Add API reference documentation** for public Python APIs
7. **Create troubleshooting guide** for common issues
8. **Add architecture decision records (ADRs)** directory
9. **Document release process** in detail
10. **Create onboarding guide** for new contributors

### 5. CI/CD & Automation (8/10)

#### Strengths
- **Quality gates** (ruff, mypy, pytest)
- **Automated PR handling** for Copilot bot PRs
- **SonarCloud integration** for code quality analysis
- **uv for fast dependency management**
- **Format checking** in CI
- **Clear workflow triggers** (paths-based)

#### Current Workflows
- `ci-quality-assurance.yml` - Main quality checks
- `release.yml` - Release automation

#### Issues Found
```
Severity: MEDIUM
Issue: No dependency vulnerability scanning
Impact: Unknown security vulnerabilities in dependencies

Severity: MEDIUM
Issue: No automated security scanning (SAST)
Missing: CodeQL, Bandit, or similar security scanning
Impact: Potential security issues not caught early

Severity: LOW
Issue: No performance regression testing
Impact: Performance degradation may go unnoticed
```

#### Recommendations
1. **Add dependency scanning workflow**:
   ```yaml
   - uses: pyupio/safety@v2
   - uses: aquasecurity/trivy-action@master
   ```
2. **Add CodeQL security scanning**:
   ```yaml
   - uses: github/codeql-action/init@v2
   ```
3. **Add bandit security linting** for Python:
   ```yaml
   - run: uv run bandit -r src packages
   ```
4. **Add pre-commit hooks** with:
   - ruff format
   - ruff check
   - mypy
   - Check for test __init__.py
   - Trailing whitespace removal
   - YAML linting
5. **Add documentation build check** in CI
6. **Add Storybook build check** in CI
7. **Add dependabot** for automated dependency updates
8. **Add license compliance checking**
9. **Add performance benchmarking** workflow
10. **Add automatic changelog generation**

### 6. Frontend Code Quality (7/10)

#### Strengths
- **Modern stack** (Astro 5 + Vue 3)
- **TypeScript** for type safety
- **Tailwind CSS** with design tokens
- **Component-based architecture**
- **ESLint flat config** properly configured
- **Headless UI** for accessibility
- **Storybook** for component development

#### Metrics
- **Vue components:** 18
- **TypeScript/JavaScript/Vue files:** 61
- **Storybook stories:** 11
- **ESLint rules:** Comprehensive (Vue, TypeScript, Astro)

#### Issues Found
```
Severity: MEDIUM
Issue: No TypeScript/JavaScript tests
Location: docs/
Details: No .test.ts or .spec.ts files found
Impact: Frontend logic not tested

Severity: LOW
Issue: No accessibility testing
Impact: A11y issues may not be caught

Severity: LOW
Issue: No visual regression testing
Impact: UI changes may break unexpectedly
```

#### Recommendations
1. **Add Vitest** for frontend unit testing
2. **Add component tests** for Vue components using @vue/test-utils
3. **Add accessibility testing** with @axe-core/playwright
4. **Add visual regression testing** with Percy or Chromatic
5. **Add Playwright E2E tests** for critical user flows
6. **Add bundle size monitoring**
7. **Add Lighthouse CI** for performance monitoring
8. **Add TypeScript strict mode** in docs/tsconfig.json
9. **Document design system tokens** comprehensively
10. **Create frontend testing guidelines**

### 7. AI Agent Friendliness (8/10)

#### Strengths
- **Excellent agent documentation** in AGENTS.md files
- **Clear architectural rules** ("Never do X", "Always do Y")
- **Explicit guidelines** for Python and frontend work
- **Custom agent support** (.github/agents/)
- **Automated PR retry mechanism** for Copilot
- **No ambiguous comments** in code
- **Structured documentation** hierarchy

#### Agent-Specific Features
- Clear workspace rules
- Explicit test layout requirements
- Transition system guidelines for UI
- Component inventory for reference
- Forbidden patterns documented

#### Issues Found
```
Severity: HIGH
Issue: Conflicting information in documentation
Example: Python version 3.13 vs 3.14
Impact: AI agents may make incorrect assumptions

Severity: MEDIUM
Issue: No examples of common tasks
Missing:
  - Adding a new package
  - Adding a new pipe
  - Adding a new Vue component
  - Writing integration tests
Impact: AI agents must infer patterns

Severity: MEDIUM
Issue: No validation scripts
Missing: Tools to verify compliance with guidelines
Impact: AI agents cannot self-validate their work
```

#### Recommendations
1. **Fix all conflicting documentation** (Python version, etc.)
2. **Create EXAMPLES.md** with:
   - Adding a new workspace package
   - Creating a new pipe
   - Adding a new Vue component
   - Writing different types of tests
   - Common refactoring patterns
3. **Add validation scripts** that AI agents can run:
   ```bash
   scripts/validate-structure.sh
   scripts/validate-tests.sh
   scripts/validate-imports.sh
   ```
4. **Create task templates** in .github/agents/ for common tasks
5. **Add quick reference cards** (one-page cheat sheets)
6. **Create troubleshooting decision trees**
7. **Add "common mistakes" documentation**
8. **Create a glossary** of project-specific terms
9. **Add explicit success criteria** for different task types
10. **Create validation checklist templates**

### 8. Dependency Management (8.5/10)

#### Strengths
- **uv workspace** for efficient dependency management
- **Version pinning** with ~= for stability
- **Clear workspace member** definition
- **Lock file committed** (uv.lock)
- **Development dependencies** separated

#### Configuration
- Root dependencies: 28
- Workspace members: 4 (otai_base, otai_hf_local, otai_otobo_znuny, otai_zammad)

#### Issues Found
```
Severity: LOW
Issue: No automated dependency updates
Impact: Dependencies may become stale

Severity: LOW
Issue: No dependency license scanning
Impact: License compliance risks
```

#### Recommendations
1. **Add dependabot configuration**
2. **Add license compliance checking** (e.g., pip-licenses)
3. **Document dependency update policy**
4. **Add dependency vulnerability scanning** (see CI/CD section)
5. **Create dependency upgrade guidelines**

### 9. Security (6.5/10)

#### Strengths
- **No secrets in code** (0 found)
- **Environment variable usage** (.env support)
- **Security rules in ruff** (S category enabled)
- **LGPL-2.1 license** clearly stated

#### Issues Found
```
Severity: HIGH
Issue: No security scanning in CI
Missing: CodeQL, Bandit, or security linters
Impact: Security vulnerabilities may be introduced

Severity: MEDIUM
Issue: No SECURITY.md
Impact: No clear vulnerability reporting process

Severity: MEDIUM
Issue: No security audit trail
Impact: Cannot track security-related changes

Severity: LOW
Issue: No dependency vulnerability scanning
Impact: Vulnerable dependencies may be used
```

#### Recommendations
1. **Add SECURITY.md** with:
   - Vulnerability reporting process
   - Supported versions
   - Security update policy
2. **Add CodeQL workflow**
3. **Add Bandit security linting**
4. **Add dependency scanning** (Safety, Trivy)
5. **Add secret scanning** prevention (git-secrets, detect-secrets)
6. **Document security best practices** for contributors
7. **Add security audit schedule**
8. **Enable GitHub security features**:
   - Dependabot alerts
   - Code scanning
   - Secret scanning
9. **Add security testing** to test suite
10. **Create security incident response plan**

### 10. Developer Experience (7.5/10)

#### Strengths
- **Clear setup instructions** in README
- **EditorConfig** for consistent formatting
- **Fast tooling** (uv, ruff)
- **Good error messages** in code
- **Well-structured logging**

#### Issues Found
```
Severity: MEDIUM
Issue: No development environment setup automation
Missing: make/just commands, dev containers
Impact: Manual setup required

Severity: LOW
Issue: No development troubleshooting guide
Impact: Common issues require investigation
```

#### Recommendations
1. **Add Makefile or Justfile** with common commands:
   ```makefile
   install: uv sync
   test: uv run -m pytest
   lint: uv run ruff check .
   format: uv run ruff format .
   check: lint test
   ```
2. **Add .devcontainer** configuration for GitHub Codespaces
3. **Add VS Code settings** recommendations
4. **Create troubleshooting guide**
5. **Add development environment verification script**
6. **Document IDE setup** (PyCharm, VS Code)
7. **Add debugging guide**
8. **Create development best practices** document

---

## Priority Recommendations

### High Priority (Fix Immediately)

1. **Remove `__init__.py` from all test directories** ⚠️
   - Violates stated guidelines
   - Can cause import issues
   - Misleads AI agents

2. **Fix Python version inconsistencies** ⚠️
   - Align pyproject.toml, AGENTS.md, .python-version
   - Update all documentation

3. **Add security scanning to CI** ⚠️
   - CodeQL
   - Bandit
   - Dependency scanning

4. **Create CONTRIBUTING.md** ⚠️
   - Essential for new contributors
   - Critical for AI agent guidance

### Medium Priority (Next Sprint)

5. **Add comprehensive documentation**
   - ARCHITECTURE.md
   - SECURITY.md
   - EXAMPLES.md
   - CHANGELOG.md

6. **Complete Storybook coverage**
   - Add stories for all 18 components
   - Document component props

7. **Add frontend testing**
   - Vitest for unit tests
   - Playwright for E2E
   - Accessibility testing

8. **Add coverage reporting**
   - PR comment integration
   - Coverage badges

9. **Add dependency management automation**
   - Dependabot
   - License scanning

10. **Add validation scripts**
    - Structure validation
    - Import validation
    - Test directory validation

### Low Priority (Backlog)

11. Add mutation testing
12. Add performance benchmarking
13. Add visual regression testing
14. Create ADR directory
15. Add bundle size monitoring
16. Create glossary
17. Add development containers
18. Create troubleshooting guide
19. Add Makefile/Justfile
20. Document IDE setup

---

## AI Agent Specific Improvements

### For Better AI Agent Collaboration

1. **Add Explicit Examples**
   ```markdown
   # EXAMPLES.md
   
   ## Adding a New Workspace Package
   
   1. Create directory: packages/otai_new_package/
   2. Create pyproject.toml with template...
   3. Add to workspace members in root pyproject.toml
   4. Create src/otai_new_package/__init__.py
   5. Create tests/ directory (NO __init__.py!)
   ```

2. **Add Validation Scripts**
   ```bash
   #!/bin/bash
   # scripts/validate-structure.sh
   
   # Check for forbidden __init__.py in tests
   if find tests packages/*/tests -name "__init__.py" | grep -q .; then
     echo "ERROR: Found __init__.py in test directories"
     exit 1
   fi
   ```

3. **Add Task Templates**
   ```markdown
   # .github/agents/python-dev-task.md
   
   ## Checklist for Python Development
   
   - [ ] Code follows PEP 695 type syntax
   - [ ] No __init__.py in test directories
   - [ ] Tests added under correct hierarchy
   - [ ] ruff check passes
   - [ ] mypy passes
   - [ ] pytest passes
   ```

4. **Add Quick Reference**
   ```markdown
   # QUICK_REFERENCE.md
   
   ## Common Commands
   - Install: `uv sync`
   - Test: `uv run -m pytest`
   - Lint: `uv run ruff check .`
   - Format: `uv run ruff format .`
   
   ## Package Locations
   - Core: src/open_ticket_ai/
   - Plugins: packages/otai_*/
   - Tests: tests/ or packages/*/tests/
   - Docs: docs/
   ```

---

## Metrics Summary

| Category | Score | Notes |
|----------|-------|-------|
| Repository Structure | 8/10 | Well-organized, __init__.py issue |
| Python Code Quality | 8.5/10 | Excellent typing, clean code |
| Test Infrastructure | 7/10 | Good coverage, structural issues |
| Documentation | 7.5/10 | Good agent docs, missing contrib guide |
| CI/CD | 8/10 | Good automation, missing security scans |
| Frontend Quality | 7/10 | Modern stack, no tests |
| AI Agent Friendliness | 8/10 | Great docs, need examples |
| Dependency Management | 8.5/10 | Excellent with uv |
| Security | 6.5/10 | Basic, needs scanning |
| Developer Experience | 7.5/10 | Good, could be better |
| **Overall** | **7.5/10** | **Good foundation, clear improvements** |

---

## Conclusion

Open Ticket AI is a **well-architected project** with **strong fundamentals** and **good AI agent support**. The codebase demonstrates modern Python practices, clear separation of concerns, and thoughtful documentation.

### Key Takeaways

**What's Working Well:**
- Modern Python 3.13+ with PEP 695
- Excellent monorepo structure
- Strong typing throughout
- Good test coverage (~2:1 ratio)
- Clear agent guidelines
- Modern frontend stack

**Critical Issues to Address:**
1. Remove `__init__.py` from test directories (violates guidelines)
2. Fix Python version inconsistencies
3. Add security scanning to CI
4. Create CONTRIBUTING.md

**For AI Agents:**
The project is **moderately AI-agent-friendly**. The excellent agent documentation (AGENTS.md) provides clear guidelines, but AI agents would benefit from:
- Explicit examples of common tasks
- Validation scripts for self-checking
- Consistent information across all documentation
- Task templates for standard operations

### Recommended Action Plan

**Week 1:**
- Remove test `__init__.py` files
- Fix Python version docs
- Add CONTRIBUTING.md
- Add security scanning

**Week 2:**
- Create ARCHITECTURE.md
- Complete Storybook coverage
- Add validation scripts
- Add coverage reporting

**Week 3:**
- Add frontend tests
- Create EXAMPLES.md
- Add dependency scanning
- Document common patterns

**Ongoing:**
- Maintain documentation
- Update examples
- Monitor metrics
- Iterate on AI agent feedback

---

## Appendix A: Tool Recommendations

### Python Development
- **uv** - ✅ Already using (excellent choice)
- **ruff** - ✅ Already using (excellent choice)
- **mypy** - ✅ Already using (consider strict mode)
- **pytest** - ✅ Already using
- **pytest-cov** - ✅ Already using
- **bandit** - ⚠️ Add for security scanning
- **safety** - ⚠️ Add for dependency scanning
- **mutmut** - Consider for mutation testing

### Frontend Development
- **Vitest** - ⚠️ Add for unit tests
- **Playwright** - ⚠️ Add for E2E tests
- **@axe-core/playwright** - ⚠️ Add for a11y testing
- **Chromatic/Percy** - Consider for visual regression

### CI/CD
- **CodeQL** - ⚠️ Add for security scanning
- **Dependabot** - ⚠️ Add for dependency updates
- **Trivy** - ⚠️ Add for container/dependency scanning
- **pre-commit** - ⚠️ Add for local quality checks

### Documentation
- **mdx-mermaid** - Consider for diagrams
- **adr-tools** - Consider for ADRs

---

## Appendix B: Example Validation Script

```bash
#!/bin/bash
# scripts/validate-compliance.sh
# Validates project structure compliance with AGENTS.md

set -e

echo "🔍 Validating project structure..."

# Check for forbidden __init__.py in tests
echo "  Checking for __init__.py in test directories..."
if find tests packages/*/tests -name "__init__.py" 2>/dev/null | grep -q .; then
  echo "  ❌ FAIL: Found __init__.py files in test directories:"
  find tests packages/*/tests -name "__init__.py"
  exit 1
fi
echo "  ✅ PASS: No __init__.py in test directories"

# Check Python version consistency
echo "  Checking Python version consistency..."
PYPROJECT_VERSION=$(grep 'requires-python' pyproject.toml | head -1)
PYTHON_VERSION=$(cat .python-version)
echo "  pyproject.toml: $PYPROJECT_VERSION"
echo "  .python-version: $PYTHON_VERSION"

# Check test file naming
echo "  Checking test file naming..."
if find tests packages/*/tests -type f -name "*.py" ! -name "test_*.py" ! -name "conftest.py" ! -name "fixtures_*.py" 2>/dev/null | grep -q .; then
  echo "  ⚠️  WARNING: Found non-standard test file names:"
  find tests packages/*/tests -type f -name "*.py" ! -name "test_*.py" ! -name "conftest.py" ! -name "fixtures_*.py"
fi

# Check for src/tests (forbidden)
echo "  Checking for tests under src/..."
if find src -type d -name "tests" 2>/dev/null | grep -q .; then
  echo "  ❌ FAIL: Found tests under src/"
  find src -type d -name "tests"
  exit 1
fi
echo "  ✅ PASS: No tests under src/"

echo "✅ Validation complete!"
```

---

## Appendix C: Suggested File Templates

### CONTRIBUTING.md Template
```markdown
# Contributing to Open Ticket AI

Thank you for your interest in contributing!

## Development Setup

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/Softoft-Orga/open-ticket-ai.git
   cd open-ticket-ai
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   uv sync
   \`\`\`

3. Run tests:
   \`\`\`bash
   uv run -m pytest
   \`\`\`

## Code Guidelines

- **Python version:** 3.13+ only
- **Type hints:** Required for all functions
- **Comments:** Avoid (clean code approach)
- **Tests:** Required for all changes
- **Linting:** Must pass `uv run ruff check .`
- **Type checking:** Must pass `uv run mypy .`

## Project Structure

See [AGENTS.md](AGENTS.md) for detailed structure guidelines.

**Key rules:**
- ❌ NO `__init__.py` in test directories
- ✅ Tests in `tests/` or `packages/*/tests/`
- ✅ Use Pydantic for data models
- ✅ Use dependency injection

## Testing

- Unit tests: `packages/<name>/tests/unit/`
- Integration tests: `tests/integration/`
- E2E tests: `tests/e2e/`

Run specific test types:
\`\`\`bash
uv run -m pytest -m unit
uv run -m pytest -m integration
uv run -m pytest -m e2e
\`\`\`

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Add/update tests
4. Run quality checks: `uv run ruff check . && uv run mypy . && uv run pytest`
5. Update documentation
6. Submit PR

## Questions?

Open an issue or check our documentation.
```

---

*End of Report*
