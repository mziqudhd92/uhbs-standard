# Versioning Policy

UHBS uses [Semantic Versioning](https://semver.org/) for the **specification** and
the **Python package** (`uhbs` / `uhbs_core`), which share version **4.5.1** until
a future split is RFCd.

| Change type | Version bump | Examples |
| --- | --- | --- |
| Breaking normative change | MAJOR | UHQS formula change; remove profile class; weaken δ_C |
| Backward-compatible normative add | MINOR | New optional TPS field; new protocol plugin API |
| Clarifications, fixtures, docs, bugfixes | PATCH | Typo, schema description, harness bug that restores documented behavior |

## Rules

1. Spec docs, schemas, and `uhbs_core` math **MUST** ship in the same tagged release.
2. Accepted RFCs that change normative text **MUST** bump the version accordingly.
3. GitHub Releases **SHOULD** list normative vs informative changes separately.
4. Signed tags (`git tag -s`) are **RECOMMENDED** for MAJOR/MINOR cuts.
