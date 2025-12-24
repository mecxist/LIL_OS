# Rule IDs (v1.0)

## Canonical Format
[LIL-<DOC>-<CAT>-<NNNN>]

DOC:
MR, GOV, CB, RT, WF, QL, SEC, DATA, API, PERF, CR

CAT:
BOUNDARY, AUTH, PROCESS, SAFETY, SCOPE, FORMAT, BUDGET, LOG, RESET

NNNN:
0001+

## Normative Keywords
Each rule line containing an ID MUST include one of:
MUST, MUST NOT, SHOULD, SHOULD NOT, MAY

## Example
- [LIL-MR-BOUNDARY-0001] The system MUST NOT perform irreversible actions without human confirmation.
  - Because: irreversibility amplifies drift and harm.

## Referencing
See [LIL-MR-BOUNDARY-0001].
