---
title: "Five config lines against supply-chain attacks (npm + PyPI)"
date: 2026-05-18
draft: false
tags: ["security", "supply-chain", "npm", "pypi", "devops"]
translationKey: "npm-supply-chain-cooldown"
summary: "npm yanks malicious versions within 24-48 hours; PyPI quarantines new uploads within hours. A seven-day cooldown — five config lines — turns that window into your defence."
---

The supply-chain attack pattern is routine by now, on both major
ecosystems. A maintainer account gets compromised (phishing, token
leak, social engineering). The attacker publishes a new patch
version of a popular package with malicious code — typically a
post-install / install-hook script that exfiltrates secrets or
installs a dead-man's switch. Anyone with `^x.y.z` or `~x.y.z` in
their lockfile picks it up on the next `npm install`; anyone with
a loose `>=x.y.z` in `pyproject.toml` does the same on
`pip install` or `uv sync`. Within 24-48 hours
[npm](https://docs.npmjs.com/) detects the version and yanks it;
[PyPI](https://blog.pypi.org/) typically quarantines new
malicious uploads within hours.

The bad news: in that detection window your CI pipeline installs
the malicious version without questions. The [LiteLLM attack on
PyPI](https://blog.pypi.org/posts/2026-04-02-incident-report-litellm-telnyx-supply-chain-attack/)
in March 2026 was live for 2 hours and 32 minutes and pulled in
over 119,000 downloads. The good news: that same handful of hours
is a lever.

### The mechanism

A cooldown refuses to install package versions that are younger
than N days. Five package managers, five config keys, all natively
supported — no agent, no daemon, no extra dependency:

| Manager | File | Key | Unit | Min. version |
|---|---|---|---|---|
| [npm](https://docs.npmjs.com/cli/v11/configuring-npm/npmrc) | `~/.npmrc` | `min-release-age` | days | 11.10+ |
| [pnpm](https://pnpm.io/settings) | `~/.npmrc` | `minimum-release-age` | minutes | 10.16+ |
| [bun](https://bun.sh/docs/runtime/bunfig) | `~/.bunfig.toml` | `[install] minimumReleaseAge` | seconds | 1.3+ |
| [uv](https://docs.astral.sh/uv/reference/settings/) | `~/.config/uv/uv.toml` | `exclude-newer` | duration (`"7 days"`) | 0.9.17+ |
| [pip](https://pip.pypa.io/en/stable/cli/pip_install/) | `~/.config/pip/pip.conf` | `[install] uploaded-prior-to` | ISO 8601 (`P7D`) | 26.1+ |

A seven-day window places you categorically after both registries'
detect-and-yank/quarantine moments. A malicious version only reaches
your lockfile if it stayed undetected for a full seven days — an
order of magnitude rarer than the base case.

### Three scopes: workstation, project, CI

All four user-level files (`~/.npmrc`, `~/.bunfig.toml`,
`~/.config/uv/uv.toml`, `~/.config/pip/pip.conf`) cover your own
interactive use. Not enough for the rest:

- Your workstation, you logged in: active.
- A different user on the same machine: not active.
- A Docker build running as the `node` / `python` user: not active.
- CI runner ([GitHub Actions](https://docs.github.com/en/actions),
  GitLab CI, etc.): not active.

CI is exactly where the attacker wants to land — that's where your
production build runs. User-level doesn't cover it.

**Per-project.** Drop config files in every repo you own. For the
Node ecosystem that's `.npmrc` and `bunfig.toml` — auto-detected by
npm/pnpm/bun. For uv: a `[tool.uv]` block in `pyproject.toml` with
`exclude-newer`. Pip is the exception: pip does NOT auto-discover a
project-level `pip.conf` the way npm reads `.npmrc`, so you must
either set `PIP_CONFIG_FILE=$PWD/pip.conf` in CI or use the env-var
route below. None of these files contain secrets and all belong in
version control.

**CI-only.** For projects where you can't commit a file (shared
codebases where the team doesn't share the opinion), set the
cooldown through environment variables:

```yaml
env:
  # Node ecosystem (npm and pnpm both honor NPM_CONFIG_*)
  NPM_CONFIG_MIN_RELEASE_AGE: 7
  NPM_CONFIG_MINIMUM_RELEASE_AGE: 10080

  # Python ecosystem
  UV_EXCLUDE_NEWER: "7 days"
  PIP_UPLOADED_PRIOR_TO: P7D
```

No file change, no PR discussion — just an env block on the jobs
that run `npm install` / `pip install` / `uv sync`. bun has no
env-var equivalent as of 1.3 — for bun projects, `bunfig.toml` is
the only path.

### Override for urgent CVEs

What if a real security patch lands inside your seven-day window?
A CVE in `lodash` or `pydantic` with yesterday's fix, and your
cooldown is holding it back. Per-install override:

```bash
# Node
NPM_CONFIG_MIN_RELEASE_AGE=0 npm install lodash@4.17.45

# Python
pip install --uploaded-prior-to 2026-06-01T00:00:00Z pydantic==2.11.1
uv add --exclude-newer 'never' pydantic==2.11.1
```

Or, if you want to permanently take the fix, set the value to `0`
(or a date before the fix) in the project-local config, commit
that as a hotfix, and revert when the cooldown would have admitted
the package anyway. The commit itself is the audit trail: evidence
the override was deliberate.

### What it costs

You're seven days behind on patches. Be honest about that. For a
dev machine it's trivial. For production builds where dependency
updates already go through a review flow
([Renovate](https://docs.renovatebot.com/) or
[Dependabot](https://docs.github.com/en/code-security/dependabot)),
it's fine: those bots often wait longer themselves before opening
a PR. For use cases that genuinely need to act on a registry
publish within an hour (CVE response on production), the override
flow is there, or you set that specific project to a shorter window.

### What it isn't

Not a silver bullet. An attack hiding behind an 8+-days-old
package falls outside the window. Same for compromise of the
registries themselves, malicious IDE extensions, or package
managers that don't yet have a cooldown feature — `poetry` and
`pipenv` (Python) have no native equivalent as of mid-2026; for
Docker, pin images on SHA. It's a time filter, not an integrity
check.

### Implementation

[`MWest2020/workstation-security`](https://github.com/MWest2020/workstation-security)
has an installer script that sets all five keys idempotently
([`common/install-pm-cooldown.sh`](https://github.com/MWest2020/workstation-security/blob/main/common/install-pm-cooldown.sh)),
plus per-project and CI templates. User-level, no sudo, preserves
existing content and file mode. Standalone explanation with the
full table is in
[`docs/supply-chain-cooldown.md`](https://github.com/MWest2020/workstation-security/blob/main/docs/supply-chain-cooldown.md).

Five config lines, a week of latency. Seems worth the trade.

### Feedback

Feedback on
[`workstation-security`](https://github.com/MWest2020/workstation-security)
is more than welcome — [open an
issue](https://github.com/MWest2020/workstation-security/issues/new/choose)
for bugs, a missing distro, or a use case the tool doesn't yet
cover. Email works too:
[mark@westerweel.work](mailto:mark@westerweel.work).
