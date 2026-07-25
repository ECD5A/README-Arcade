# Security Policy

## Supported Version

Security fixes are applied to the current `main` branch. README Arcade does not
currently maintain older release branches.

## Reporting a Vulnerability

Do not open a public issue for a suspected vulnerability.

Use GitHub's private vulnerability reporting:

https://github.com/ECD5A/README-Arcade/security/advisories/new

Include:

- the affected file or workflow;
- a minimal reproduction;
- the expected and actual behavior;
- the security impact;
- a suggested fix, if available.

Reports involving path traversal, unsafe SVG content, GitHub Actions token
exposure, workflow injection, or unintended disclosure of contribution data
are especially useful.

You should receive an acknowledgement within seven days. Valid reports will be
handled through a private GitHub security advisory until a fix is available.

## Scope

README Arcade only requests the GitHub token supplied to its Actions workflow
and uses it to read the configured user's contribution calendar. The project
does not require users to paste personal access tokens into configuration
files. Reports that depend on publishing a token in the repository are outside
the intended setup, but accidental token exposure should still be reported
privately.
