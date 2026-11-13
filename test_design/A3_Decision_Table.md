# A3 – Decision Table Testing

| Rule | Dues > 0 | Already Registered | Prerequisites Missing | Credit Limit Exceeded | Course Full | Expected Status |
|---|---|---|---|---|---|---|
| R1 | Yes | - | - | - | - | DUES_BLOCK |
| R2 | No | Yes | - | - | - | ALREADY_REGISTERED |
| R3 | No | No | Yes | - | - | PREREQUISITES_MISSING |
| R4 | No | No | No | Yes | - | CREDIT_LIMIT |
| R5 | No | No | No | No | Yes | WAITLISTED |
| R6 | No | No | No | No | No | REGISTERED |

## Explanation

The system evaluates conditions in the following priority order:

1. Outstanding dues
2. Already registered
3. Missing prerequisites
4. Credit limit
5. Course availability

Only the first applicable outcome is returned.