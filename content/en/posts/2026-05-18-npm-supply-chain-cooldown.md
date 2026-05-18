---
title: "Three config lines against npm supply-chain attacks"
date: 2026-05-18
draft: false
tags: ["security", "supply-chain", "npm", "devops"]
translationKey: "npm-supply-chain-cooldown"
summary: "npm typically yanks malicious versions within 24-48 hours. A seven-day cooldown — three config lines — turns that window into your defence."
---

The pattern of npm supply-chain attacks is routine by now. A
maintainer account gets compromised (phishing, token leak, social
engineering). The attacker publishes a new patch version of a
popular package with malicious code — typically a post-install
script that exfiltrates secrets or installs a dead-man's switch.
Anyone with `^x.y.z` or `~x.y.z` in their lockfile picks it up on
the next `npm install`. Within 24-48 hours,
[npm](https://docs.npmjs.com/) detects the version, yanks it, and
publishes an advisory.

The bad news: in that one-or-two-day window your CI pipeline
installs the malicious version without questions. The good news:
that same 24-48 hours is a lever.

### The mechanism

A cooldown refuses to install package versions that are younger
than N days. Three package managers, three config keys, all
natively supported — no agent, no daemon, no extra dependency:

| Manager | File | Key | Unit | Min. version |
|---|---|---|---|---|
| [npm](https://docs.npmjs.com/cli/v11/configuring-npm/npmrc) | `~/.npmrc` | `min-release-age` | days | 11.10+ |
| [pnpm](https://pnpm.io/settings) | `~/.npmrc` | `minimum-release-age` | minutes | 10.16+ |
| [bun](https://bun.sh/docs/runtime/bunfig) | `~/.bunfig.toml` | `[install] minimumReleaseAge` | seconds | 1.3+ |

A seven-day window places you categorically after npm's
detect-and-yank moment. A malicious version only reaches your
lockfile if that version stayed undetected for a full seven days —
an order of magnitude rarer than the base case.

### Three scopes: workstation, project, CI

`~/.npmrc` and `~/.bunfig.toml` are user-level. Good for your own
interactive use, not enough on its own:

- Your workstation, you logged in: active.
- A different user on the same machine: not active.
- A Docker build running as the `node` user: not active.
- CI runner ([GitHub Actions](https://docs.github.com/en/actions),
  GitLab CI, etc.): not active.

CI is exactly where the attacker wants to land — that's where your
production build runs. User-level doesn't cover it.

**Per-project.** Drop an `.npmrc` and `bunfig.toml` in every repo
you own, with the cooldown keys set. Neither file contains secrets,
and both belong in version control. A CI runner that checks out
your project reads them automatically.

**CI-only.** For projects where you can't commit a file (shared
codebases where the team doesn't share the opinion), set the
cooldown through environment variables:

```yaml
env:
  NPM_CONFIG_MIN_RELEASE_AGE: 7
  NPM_CONFIG_MINIMUM_RELEASE_AGE: 10080
```

No file change, no PR discussion — just an env block on the jobs
that run `npm install`.

### Override for urgent CVEs

What if a real security patch lands inside your seven-day window?
A CVE in `lodash` with yesterday's fix, and your cooldown is
holding it back. Two options:

```bash
# Temporary override, just for this install command:
NPM_CONFIG_MIN_RELEASE_AGE=0 npm install lodash@4.17.45
```

Or, if you want to permanently take the fix, set the value to `0`
in the project-local `.npmrc`, commit that as a hotfix, and revert
when the cooldown would have admitted the package anyway. The
commit itself is the audit trail: evidence the override was
deliberate.

### What it costs

You're seven days behind on patches. Be honest about that. For a
dev machine it's trivial. For production builds where dependency
updates already go through a review flow
([Renovate](https://docs.renovatebot.com/) or
[Dependabot](https://docs.github.com/en/code-security/dependabot)),
it's fine: those bots often wait longer themselves before opening
a PR. For use cases that genuinely need to act on an `npm publish`
within an hour (CVE response on production), the override flow is
there, or you set that specific project to a shorter window.

### What it isn't

Not a silver bullet. An attack hiding behind an 8+-days-old
package falls outside the window. Same for compromise of the
npm registry itself, malicious IDE extensions, or
npm-independent ecosystems — [PyPI](https://pypi.org/) has no
equivalent of `min-release-age`; for Docker, pin images on SHA.
It's a time filter, not an integrity check.

### Implementation

[`MWest2020/workstation-security`](https://github.com/MWest2020/workstation-security)
has an installer script that sets all three keys idempotently
([`common/install-pm-cooldown.sh`](https://github.com/MWest2020/workstation-security/blob/main/common/install-pm-cooldown.sh)),
plus per-project and CI templates. User-level, no sudo, preserves
existing content and file mode. Standalone explanation with the
full table is in
[`docs/supply-chain-cooldown.md`](https://github.com/MWest2020/workstation-security/blob/main/docs/supply-chain-cooldown.md).

Three config lines, two days of latency. Seems worth the trade.
