---
name: python-style
description: Python code style preferences — architecture, types, tooling, and conventions for Python projects
compatibility: opencode, claude-code
---

★ Starred rules are highest priority — always follow these.

## ★ Type annotations

- Use `| None` union syntax (e.g., `str | None`) over `Optional[str]`. Why: PEP 604 native syntax, no typing import needed. Assume Python 3.12+.

  ```python
  # Bad
  from typing import Optional
  def greet(name: Optional[str]) -> Optional[str]: ...

  # Good
  def greet(name: str | None) -> str | None: ...
  ```
- Make fields explicitly nullable rather than providing empty values like `=""` or `=0`. Use `| None` for optional params; meaningful defaults (e.g., `timeout=30`) are fine.

  ```python
  # Bad
  def create_user(name: str = "", age: int = 0): ...
  class Config:
      host: str = ""

  # Good
  def create_user(name: str | None = None): ...
  class Config:
      host: str | None = None

  # Also good: meaningful defaults
  def fetch(timeout: int = 30): ...
  ```

## Code hygiene

- Use `.get("key")` without a default — let `None` propagate naturally. Why: Avoids masking bugs; empty string or 0 can be valid data. Use default only when it's meaningful and `None` is a valid dict value.

  ```python
  # Bad
  count = data.get("count", 0)  # masks that count could be missing

  # Good
  count = data.get("count")  # let None propagate if missing

  # Good: meaningful default when None is valid
  enabled = config.get("enabled", True)
  ```

  Use dataclass for structured data instead of raw dicts when the abstraction is justified.
- Never add imports inside functions — always at the top of the file. Sort: stdlib → third-party → local. Prefer relative imports within the same package.

  ```python
  # Bad
  def process():
      from pathlib import Path
      ...

  # Good
  from pathlib import Path

  def process():
      ...
  ```
- Use custom exception classes for domain errors. Prefer built-in exceptions (ValueError, KeyError, etc.) when they match. Use custom exceptions when no built-in fits.

  ```python
  # Bad
  raise Exception("failed to fetch")
  raise ValueError("invalid token")  # when it's actually a domain error

  # Good
  if not token:
      raise ValueError("token is required")

  class GitHubError(Exception):
      pass

  class GitHubRateLimitError(GitHubError):
      def __init__(self, retry_after: int):
          self.retry_after = retry_after
          super().__init__(f"Rate limited, retry after {retry_after}s")
  ```

## Code conventions

- Paths: Use descriptive constants instead of hardcoded strings. Define at module level.

  ```python
  # Bad
  with open("/home/alex/data/output.json") as f: ...

  # Good
  DATA_DIR = Path(__file__).parent / "data"
  OUTPUT_FILE = DATA_DIR / "output.json"

  with OUTPUT_FILE.open() as f: ...
  ```
- Paths: Prefer methods like `with_stem`, `with_suffix`, `with_name` over string concatenation. Simple f-strings like `f"{name}.json"` are fine.

  ```python
  # Bad
  filename = data["name"] + ".json"
  path = "/data/" + filename

  # Good
  filename = f"{data['name']}.json"  # simple case: OK
  output = input_path.with_suffix(".json")
  output = input_path.with_name("output.json")
  ```
- Duplication: Extract repeated logic into helper functions. Apply Rule of Three: extract after third occurrence. Don't extract trivial or unlikely-to-change duplication.

  ```python
  # Bad
  def process_user():
      data = fetch()
      validated = validate(data)
      save(validated)
  def process_order():
      data = fetch()
      validated = validate(data)
      save(validated)

  # Good: extract to helper
  def process():
      data = fetch()
      validated = validate(data)
      save(validated)
  def process_user(): process()
  def process_order(): process()

  # Also good: don't extract trivial cases
  if user.is_active and user.has_permission: ...
  ```
- Enums/Literal: Use `typing.Literal` instead of magic constants or enums. Works for both user-facing choices and internal state machines.

  ```python
  # Bad
  status = "done"
  if status == "done": ...

  # Good
  Status = Literal["pending", "done", "failed"]

  def process(status: Status) -> None:
      if status == "done": ...
  ```

## Architecture

- Data classes: Use `dataclass` for simple DTOs with no validation. Use `dataclass` + `msgspec` for fast serialization. Use `pydantic` when you need validation + OpenAPI schema. Use `TypedDict` when integrating with dict-returning code outside your control. Prefer `@dataclass` over `typing.NamedTuple` — dataclass is more flexible (can add methods, defaults, validators) and the syntax is cleaner.

  ```python
  # Bad: NamedTuple - less flexible
  class Point(NamedTuple):
      x: int
      y: int

  # Good: dataclass - can add methods, defaults, validation
  @dataclass
  class Point:
      x: int
      y: int

      def distance_from_origin(self) -> float:
          return math.sqrt(self.x ** 2 + self.y ** 2)
  ```

  ```python
  # dataclass: simple DTO, no validation
  @dataclass
  class User:
      name: str
      email: str

  # msgspec for fast serialization: define with @dataclass, encode/decode with msgspec
  import msgspec

  @dataclass
  class Event:
      id: str
      timestamp: float
      payload: bytes

  def serialize(event: Event) -> bytes:
      return msgspec.encode(event)

  def deserialize(data: bytes) -> Event:
      return msgspec.decode(data, type=Event)

  # pydantic: validation + OpenAPI
  from pydantic import BaseModel

  class Config(BaseModel):
      host: str
      port: int

  # TypedDict: dict-returning external code
  from typing import TypedDict

  class ExternalAPIResponse(TypedDict):
      user_id: str
      data: dict
  ```
- Module structure: Prefer flat over deep. Split when a module exceeds ~300 lines or has 3+ distinct responsibilities.

  ```python
  # Bad (deep)
  src/utils/helpers/formatters/date.py

  # Good (flat)
  src/formatters.py  # split by responsibility, not by type
  ```

  Split triggers: >300 lines or 3+ distinct responsibilities.
- `__init__.py`: Export only what consumers need. Never add placeholder functions. Use `__all__` to define public API. Avoid wildcard imports (`from x import *`).

  ```python
  # Bad
  def stub(): pass
  from utils import *  # unclear what's exposed

  # Good
  from .parser import parse

  __all__ = ["parse"]
  ```

## ★ Testing

- Write tests for correct behavior, not for bugs. Don't assert the buggy result — assert what the code *should* do.

  ```python
  # Bad: exit_code == 0 is the bug (unhandled exception silently exits 0)
  def test_status_outside_git():
      result = runner.invoke(cli, ["status"])
      assert result.exit_code == 0  # only passes because of the bug

  # Good: assert the intended behavior
  def test_status_outside_git():
      with runner.isolated_filesystem():
          result = runner.invoke(cli, ["status"])
      assert result.exit_code != 0
      assert "not a git repository" in result.output
  ```
- Prefer real objects, fakes, fixtures, or DI over mocks. Always isolate from external systems (network, subprocess calls, time) — unmocked externals cause hangs, flakiness, and test pollution. Use `patch()` for true externals; use fakes or fixtures for internal collaborators.

  ```python
  # Bad: over-mocking internal logic
  with mock.patch("myapp.validator.check") as m:
      m.return_value = True
      result = process()

  # Bad: unmocked subprocess may hang CI
  def test_status():
      result = runner.invoke(cli, ["status"])  # runs real git

  # Good: fake for internal collaborators
  class FakeGitHubClient:
      def fetch(self, repo):
          return {"stars": 100}

  # Good: patch true externals (network, subprocess)
  with mock.patch("httpx.Client.get") as mock_get:
      mock_get.return_value = Response(200, json={"id": 1})
      result = api_call()
  ```
- Reuse common setups using fixtures and functions. Extract to fixture only when used in 2+ tests.

  ```python
  # Good: reuse setups with fixtures
  @pytest.fixture
  def sample_user():
      return {"id": 1, "name": "Test", "email": "test@example.com"}

  @pytest.fixture
  def db_connection():
      return create_test_db()

  def test_create_user(db_connection, sample_user):
      result = create_user(db_connection, sample_user)
      assert result["id"] == 1

  def test_user_email(db_connection, sample_user):
      result = create_user(db_connection, sample_user)
      assert result["email"] == "test@example.com"
  ```
- Group tests in nested classes matching the code structure. Simple modules don't need deep nesting.

  ```python
  # Good: nested classes match code structure
  class TestGithubClient:
      class TestFetch:
          @staticmethod
          def test_writes_content_to_file(): ...
          @staticmethod
          def test_handles_404(): ...

      class TestCreate:
          @staticmethod
          def test_returns_new_record(): ...

  # Simple modules don't need deep nesting
  def test_parse_valid_json(): ...
  def test_parse_invalid_json_raises(): ...
  ```
- Test naming: Drop redundant prefixes — context comes from nested classes.

  ```python
  # Bad: redundant prefix
  class TestGithubClient:
      def test_github_client_fetch_writes_contents_to_file(self): ...

  # Good: prefix dropped
  class TestGithubClient:
      class TestFetch:
          def test_writes_to_file(): ...
  ```
- Use `@staticmethod` on test methods that don't need `self`.

  ```python
  class TestParser:
      @staticmethod
      def test_parses_valid_json():  # doesn't need self
          result = parse('{"key": "value"}')
          assert result == {"key": "value"}
  ```
- Compare parsed results against fixture files (json/csv/yaml/etc.) rather than many individual assertions. Simple tests don't need fixture files.

  ```python
  # Good: compare against fixture file
  def test_parse_config():
      result = parse_config("fixtures/config.yaml")
      expected = load_fixture("fixtures/config_expected.json")
      assert result == expected

  # Simple tests don't need fixture files
  def test_empty_list():
      result = parse([])
      assert result is None
  ```
- Write multiple focused test functions rather than one large monolithic test. Simple tests can be single functions.

  ```python
  # Bad: monolithic test
  def test_user_crud():
      create_user()
      assert user exists
      update_user()
      assert updated
      delete_user()
      assert deleted

  # Good: focused tests
  def test_create_user(): ...
  def test_update_user(): ...
  def test_delete_user(): ...

  # Simple tests: one function is fine
  def test_parse_empty_returns_none(): ...
  ```

## Common pitfalls

- **Regex matching**: Use `re.search()` when the pattern can appear anywhere in a string. `re.match()` only matches from position 0.

  ```python
  # Bad: match only finds at string start
  url = "git@github.com:owner/repo.git"
  re.match(r"github\.com[:/]", url)  # None

  # Good: search finds anywhere in string
  re.search(r"github\.com[:/]", url)  # Match found
  ```

- **Redundant config**: Don't specify tool config that matches defaults. This adds noise without benefit.

  ```python
  # Bad: redundant defaults
  [tool.pytest.ini_options]
  python_functions = ["test_*"]  # pytest default
  python_classes = ["Test*"]  # pytest default

  # Good: only specify what differs from defaults
  [tool.pytest.ini_options]
  asyncio_mode = "auto"
  ```

- **Local imports in tests**: Always use module-level imports. Local imports inside functions indicate a code smell and slow test collection.

  ```python
  # Bad: local import inside test
  def test_something():
      from rv.module import something  # slow, hides dependency

  # Good: top-level import
  from rv.module import something

  def test_something():
      assert something() == expected
  ```

- **Plain `except`**: Never use bare `except:` or catch generic `Exception`. Catch specific exception types. This masks bugs and makes debugging harder.

  ```python
  # Bad: catches everything including KeyboardInterrupt
  try:
      do_something()
  except Exception:
      pass

  # Good: catch specific exceptions
  import keyring.errors
  try:
      token = keyring.get_password("rv", "github")
  except (keyring.errors.NoKeyringError, keyring.errors.KeyringError):
      pass  # keyring not available, continue to fallback
  ```

## Tooling

- Package manager: `uv`. Use `uv add <package>` for production deps or `uv add --dev <package>` for dev deps. Why: uv manages lockfiles and dependency resolution automatically.
- Testing: `pytest`. Run by `make test` in the project directory.
- Linting/formatting: `make lint` in the project directory. Use `make lint-fix` to reformat automatically. CI should run `make lint` without fix.
- Type checking: `make ty` in the project directory.

---

**Scope**: These rules apply to new code. For existing code, follow "fix on touch" — improve as you work in a file but don't refactor unrelated code.
