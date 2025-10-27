---
layout: post
title: "Configuring a Python Development Environment for 2026"
date: 2025-10-27
author: Craig Oda
author_bio: "Craig Oda is a partner at Oppkey and an active contributor to FastOpp"
image: /assets/images/2025_10/time.jpg
excerpt: "uv and ruff replace pip, flake8, isort, black"
---

Python 3.14 came out in October 2025 with official free-threaded support and a whole
list of features. The Python community is changing faster today than at any
point in the last 10 years. As I drove home from fly fishing in California,
I looked at the changing crimson foliage near Stanford University and decided
that today was the day to dump pip, pylance, flake8, isort and Black formatter and
configure my Python tools for a brighter future in 2026.

Two decades ago, I taught my kids Python with Emacs and flake8.
On that beautiful Autumn afternoon, I was using Cursor with a bunch of extensions imported from
VSCode - Pylance for IntelliSense,
Flake8 for linting, isort for imports, Black for formatting,
and pip for dependency management. Cursor kept giving an annoying message to
use Anysphere Python instead of the proven and stable Pylance language server.
Although I believe that Pylance is better than Anysphere Python, I decided
to give it a try.

## From Pylance to Anysphere Python

**Pylance** is Microsoft's language server for Python — the component that powers IntelliSense in VS Code.
It provides:

- autocompletion,
- type inference,
- inline documentation,
- "go to definition" navigation,
- and static type checking (via Pyright under the hood).

Although Pylance is superior to Anysphere Python, I've switched to Anysphere Python.
Anysphere Python replaces Pylance as the language server and integrates directly with Cursor's AI features.
The advantage of Anysphere Python over Pylance are not immediately obvious. However, I'm
hoping it will get better in 2026. In 2025, Pylance is better than Anysphere Python in
most cases. I made the switch because Anysphere Python
may have better context-aware code generating and editing in the future.
As I've started to use the Cursor Plan mode, I'm hoping that Anysphere Python
will help. In Cursor, I uninstalled the [Pylance extension](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance).

---

## 🧠 2. From **Flake8** → **Ruff**

**Flake8** was my linter for over a decade.
It runs static checks (E, F, W codes) to catch style issues, undefined variables, and logical mistakes.
Flake8 could be extended with plugins like `flake8-bugbear`, `flake8-comprehensions`, and `flake8-docstrings`.

The downside?

- Dozens of small Python plugins to install
- Slow runtime on large projects
- No auto-fix

**Ruff**, written in Rust, replaces all of that in one binary.
It implements nearly all Flake8 plugins natively — `B` for bugbear, `C4` for comprehensions, `UP` for pyupgrade, and more.
It’s **100× faster** and can fix issues automatically:

```bash
ruff check . --fix
```

I uninstalled Flake8 and now rely entirely on Ruff for linting.

---

## ⚙️ 3. From **isort** → **Ruff’s built-in import sorter**

**isort** automatically grouped and alphabetized imports:

```python
# before
import sys, os
from requests import get
```

→

```python
# after
import os
import sys

from requests import get
```

Ruff re-implements isort’s logic internally — same rules, same grouping, same configuration style.
By enabling Ruff’s `"I"` rule family (and `[tool.ruff.isort]` in `pyproject.toml`), imports are fixed automatically during linting:

```bash
ruff check . --fix
```

That means no need for a separate `isort` install or pre-commit hook.

---

## 🎨 4. From **Black** → **Ruff Formatter**

**Black** was my code formatter — it enforced consistent indentation, spacing, and line length.
Ruff now includes a **Black-compatible formatter** built in:

```bash
ruff format .
```

It’s fully compatible with Black’s style (the “one true way” of formatting Python) but runs instantly, thanks to Rust.

I removed the Black formatter extension in Cursor and set Ruff as my default formatter in `settings.json`.

---

## 🐍 5. From **pip** → **uv**

**pip** (and later `pipenv` or `poetry`) used to manage my dependencies.
They worked, but installation speed and dependency resolution were slow — especially in large projects.

**uv**, from Astral (the team behind Ruff), replaces pip and virtualenv entirely.
It’s a single Rust binary that can:

- create virtual environments instantly,
- install packages in parallel,
- resolve dependencies deterministically,
- and manage Python versions transparently.

Typical workflow:

```bash
uv init myproject
uv add fastapi
uv run fastapi dev
```

It’s drop-in compatible with pip but 10–100× faster.

---

## 🧱 6. Using a `pyproject.toml` Template

I’ve created a reusable `pyproject.toml` that preloads my Ruff configuration.
Since uv doesn’t yet have a template command, I copy this file manually into new projects.
It defines:

- line length
- rule families (`E`, `F`, `I`, `B`, `UP`, `SIM`, `C4`)
- formatting and import-sorting behavior

Example snippet:

```toml
[tool.ruff]
line-length = 120
select = ["E", "F", "I", "B", "UP", "SIM", "C4"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

Then I just run:

```bash
uv sync --dev
ruff check . --fix
ruff format .
```

---

## ⚙️ 7. Adjusting `settings.json` in Cursor

Finally, I updated my editor configuration (settings.json) to remove old formatters and linters and point to Ruff as the default Python formatter.

I'll include those specific settings in the blog itself, but here’s the key line:

```json
"[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true
}
```

---

## 🚀 Result

After switching:

- No more managing 4+ Python tools
- No redundant dependencies
- Instant linting, formatting, and import cleanup
- uv replaces pip + venv, faster and cleaner
- Cursor’s AI works directly with my Python environment (via Anysphere)

Everything just feels faster — from creating projects to saving files.

---

## ✅ TL;DR

| Old Tool    | Purpose                     | Replacement          | Why                                          |
| ----------- | --------------------------- | -------------------- | -------------------------------------------- |
| **Pylance** | Language server for VS Code | **Anysphere Python** | Faster, AI-integrated, built into Cursor     |
| **Flake8**  | Linting                     | **Ruff**             | 100× faster, auto-fixes, one binary          |
| **isort**   | Import sorting              | **Ruff (built-in)**  | Same behavior, no extra tool                 |
| **Black**   | Code formatting             | **Ruff Formatter**   | Black-compatible, Rust-fast                  |
| **pip**     | Dependency management       | **uv**               | Instant installs, modern environment manager |

---

### 🧠 Reflection

The Python ecosystem has evolved dramatically — the new Rust-based tooling from Astral (Ruff, uv) makes development feel as fast and smooth as Go or Rust itself.
The best part? You can remove almost a dozen Python-only dependencies and simplify your workflow to just **Ruff + uv**.
