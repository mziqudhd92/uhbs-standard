# Security Policy

## Supported Versions

| Version | Supported |
| --- | --- |
| 4.0.x | Yes |
| < 4.0 | No |

## Reporting a Vulnerability

Do **not** open a public GitHub issue for security vulnerabilities in this repository, the UHBS CLI, schemas, or documentation tooling.

Please report vulnerabilities privately via one of:

1. **GitHub Security Advisories** — use [Private vulnerability reporting](https://github.com/mziqudhd92/uhbs-standard/security/advisories/new) on this repository.
2. **Email** — `security@uhbs.dev` (replace with your operational security contact before public launch if different).

Include:

- A clear description of the issue and impact
- Steps to reproduce (PoC limited to the minimum needed to demonstrate the issue)
- Affected component (CLI, schema, docs build, CI)
- Whether you believe the issue affects published scorecards or adopter profiles

## Response Targets

| Stage | Target |
| --- | --- |
| Initial acknowledgement | Within 3 business days |
| Triage / severity assessment | Within 7 business days |
| Fix or mitigation plan | Communicated after triage |

We follow coordinated disclosure. Please allow reasonable time for a fix before public discussion.

## Scope Notes

- UHBS evaluates honeypots and decoys; **do not** submit exploitation guidance against third-party production systems as “issues.”
- Findings against *adopters’* honeypots should be reported to those projects under their own policies.
- Schema or scoring-logic bugs that could inflate UHQS grades are treated as security-relevant integrity issues.
