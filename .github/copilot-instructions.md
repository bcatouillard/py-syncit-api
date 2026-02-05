# Copilot instructions

## Project

- This project is located in the following [GitHub Repository](https://github.com/bcatouillard/py-sync-it-api).
- This is a repository hosting a python project. The main branch is `main`.

## Pull requests and commits

- When creating a pull request, ensure the title is descriptive and follows the format `feat: <description>` for new features, `fix: <description>` for bug fixes, or `chore: <description>` for maintenance tasks.
- Please take a look at [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/) specifications for more details about this.
- When committing code, use clear and concise commit messages that follow the same format as pull request titles.
- When creating pull requests, ensure that you follow the [Pull Request Template](https://github.com/bcatouillard/py-sync-it-api/blob/main/.github/PULL_REQUEST_TEMPLATE.md) to provide a clear description of the changes made, the reason for the changes, and any relevant context.
- If the pull request is related to an issue, include a link to the issue in the pull request description in the format `Fixes #<issue_number>` in the section `## Link to the initial request/ticket`. If the Pull Request is not related to an issue, you can remove this section.
- Use the `## What this PR Provides` section to describe the changes made in the pull request, including any new features, bug fixes, or improvements.
- Use the `## Breaking changes (if any)` section to list any breaking changes introduced by the pull request. If there are no breaking changes, use `N/A`.
- Use the `## How to test` section to provide instructions on how to test the changes made in the pull request, including any specific steps or commands that need to be run.

## Coding style

### General

- Always conform to the coding styles defined in `.editorconfig` when you write code.
- Ensure there is no trailing whitespace at the end of lines.
- Ensure files end in a newline and only a newline.

### Markdown files

- Follow the instructions from <https://github.com/github/awesome-copilot/blob/main/instructions/markdown.instructions.md> when writing markdown files.
- Always conform to the coding styles defined in `.markdownlint.yaml` when you write markdown files.

### Python files

- We use `uv` to manage python dependencies and virtual environments.

### General Instructions

- Always prioritize readability and clarity.
- For algorithm-related code, include explanations of the approach used.
- Write code with good maintainability practices, including comments on why certain design decisions were made.
- Handle edge cases and write clear exception handling.
- Use consistent naming conventions and follow language-specific best practices.
- Write concise, efficient, and idiomatic code that is also easily understandable.

### Style guides

- We use [PEP 8](https://www.python.org/dev/peps/pep-0008/) as the coding style for Python files.
- We use [PEP 257](https://www.python.org/dev/peps/pep-0257/) for docstrings in Python files.
- We use one-line docstrings for functions that do not raise exceptions, and multi-line docstrings for function that do raise exceptions.
- Python modules and packages contain a docstring at the top of the file, which describes the module's purpose and functionality
- Python packages contain an explicit `__init__.py` file.
- When writing code, ensure that it is well-structured and follows the principles of clean code.
- When writing code, ensure that it is well-documented comments where necessary.

### Code structure

- All python modules should be placed in the `src/` directory.

### Code quality

- Python public functions and classes should be documented with type hints for parameters and output to comply with Ruff rules:

  - [missing-type-function-argument (ANN001)](https://docs.astral.sh/ruff/rules/missing-type-function-argument/)
  - [missing-return-type-special-method (ANN204)](https://docs.astral.sh/ruff/rules/missing-return-type-special-method/)

- We use f-strings for string formatting except when writing log statements.

### Testing

- Tests are located in the `tests` directory and follow the naming convention `test_*.py`.
- If a function or class is located in a module named `foo.py`, the test file should be named `test_foo.py`.

- When writing tests, use the `pytest` framework and ensure that all tests are passing before submitting a pull request.
- When using `pytest.mark.parametrize`:

- always use a tuple for the parameters, even if there is only one parameter.
- the content of the `argvalues` parameter should be a list of `pytest.param(...)` objects, which allows you to specify additional metadata for each test case, such as `id`, `marks`, and `xfail`.

- When writing code or tests, respect as much as possible the pylint rule `Import outside toplevel (import-outside-toplevel)` and the ruff rule [PLC0415](https://docs.astral.sh/ruff/rules/import-outside-top-level/).

- When writing tests, ensure that you use fixtures to set up the test environment.
- Write custom fixtures in the `conftest.py` file located in the `tests` directory and use the `@pytest.fixture` decorator to define and declare the name of the fixture through the `name` parameter of `@pytest.fixture`
- When using fixtures, ensure that you use the `scope` parameter to specify the scope of the fixture, which can be one of `function`, `class`, `module`, or `session`.

- When writing tests, ensure that you use assertions to check the expected behavior of the code.
- To mock external dependencies in tests, use the `pytest-mock` library.
- When using the `mocker` fixture, always specify the type hint associated which is `MockerFixture`
- When performing assertions on mock objects, use the `assert_called_once_with` or `assert_called_with` methods to check that the mock was called with the expected arguments.
- When using `mocker.patch`, ensure that you specify the full path to the object being patched, including the module name.
- When patching classes, use `mocker.patch.object` to patch a class method or attribute.
- When patching functions, use `mocker.patch` to patch a function in a module.
- When patching an object, ensure that you use the `autospec=True` argument to ensure that the mock behaves like the original object.
- When writing tests, ensure that you use the `pytest.raises` context manager to check for exceptions.
- When using `pytest.raises`, ensure that you specify the exception type and use the `match` parameter to check the exception message.
- When writing tests, ensure that you use the `pytest.mark.asyncio` decorator to mark asynchronous tests.
- When writing asynchronous tests, ensure that you use the `await` keyword to call asynchronous functions.
- When writing asynchronous tests, ensure that you use the `async def` syntax to define asynchronous test functions.
- When writing assertions in tests related to lists or sets, use the `pytest-unordered` plugin to ensure that the order of elements does not matter.
- When writing tests, ensure that you use the `pytest.mark.skip` decorator to skip tests that are not applicable in certain environments or conditions.
- When writing tests, ensure that you use the `pytest.mark.xfail` decorator to mark tests that are expected to fail.
- When writing tests that need a mocked environment, use the `mocker` fixture and the `mocker.patch.dict` pattern.
- When using a MagicMock, generated if from the `mocker` fixture, and ensure that you use the `autospec=True` argument to ensure that the mock behaves like the original object.
- When using inner classes in tests, ensure there is a docstring for the class that describes its purpose and functionality.
- When writing tests that requires a password to be hardcoded, create a fixture that uses [Faker](https://faker.readthedocs.io/en/master/) that returns the password and use it in the test and reuse it in other tests as needed.
- When writing tests related to Http status codes, ensure that you use the `HTTPStatus` enum from the `http` module to represent HTTP status codes.
- When writing tests relying on local files, ensure that you use the fixtures `datadir` or `shared_datadir` from the [pytest-datadir](https://github.com/gabrielcnr/pytest-datadir) plugin to create temporary files and directories for testing purposes.

#### Edge Cases and Testing

- Always include test cases for critical paths of the application.
- Account for common edge cases like empty inputs, invalid data types, and large datasets.
- Include comments for edge cases and the expected behavior in those cases.

### Checking code

- Before submitting a pull request, ensure that you have run the following commands with success to check your code:

  ```bash
  ruff format --check
  ruff check
  ```

- When running these checks in vscode, use `uv run` to execute the commands, as it ensures that the correct virtual environment is used.
