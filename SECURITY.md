# Security Policy

## Supported Versions

| Version | Supported |
| --- | --- |
| 4.2.x | Yes |
| 4.0.x | Security fixes only (please upgrade to 4.2.x) |
| < 4.0.0 | No |

## Reporting a Vulnerability

Do **not** open a public GitHub issue for security vulnerabilities in this repository, the UHBS CLI, schemas, or documentation tooling.

Please report vulnerabilities privately via:

1. **GitHub Security Advisories** — preferred:
   [Private vulnerability reporting](https://github.com/mziqudhd92/uhbs-standard/security/advisories/new)
   on this repository.
2. If advisory reporting is unavailable, contact the maintainer privately via
   [GitHub](https://github.com/mziqudhd92) (profile contact / private message).
   Do **not** open a public issue.

There is no project security email address at this time.

Machine-readable policy: [`docs/.well-known/security.txt`](docs/.well-known/security.txt)
(published at `https://mziqudhd92.github.io/uhbs-standard/mkdocs/.well-known/security.txt`).

Include:

- A clear description of the issue and impact
- Steps to reproduce (PoC limited to the minimum needed to demonstrate the issue)
- Affected component (CLI, schema, docs build, CI)
- Whether you believe the issue affects published scorecards or example profiles

## Response Targets

| Stage | Target |
| --- | --- |
| Initial acknowledgement | Within 3 business days |
| Triage / severity assessment | Within 7 business days |
| Fix or mitigation plan | Communicated after triage |

We follow coordinated disclosure. Please allow reasonable time for a fix before public discussion.

## Scope Notes

- UHBS evaluates honeypots and decoys; **do not** submit exploitation guidance against third-party production systems as “issues.”
- Findings against *other projects’* honeypots should be reported to those projects under their own policies.
- Schema or scoring-logic bugs that could inflate UHQS grades are treated as security-relevant integrity issues.
