# A1 – Equivalence Class Partitioning (ECP)

## 1. Credit Limit

| Test ID | Input | Expected Result |
|---|---|---|
| ECP-01 | Current credits = 10, New credits = 3 | True |
| ECP-02 | Current credits = 16, New credits = 3 | False |
| ECP-03 | Current credits = -1 | ValueError: Invalid current credits |
| ECP-04 | New credits = 0 | ValueError: Invalid course credits |

## 2. Prerequisites

| Test ID | Input | Expected Result |
|---|---|---|
| ECP-05 | No prerequisites required | True |
| ECP-06 | All prerequisites completed | True |
| ECP-07 | Only some prerequisites completed | False |

## 3. Registration Conditions

| Test ID | Input | Expected Result |
|---|---|---|
| ECP-08 | Outstanding dues = 1 | DUES_BLOCK |
| ECP-09 | Student already registered | ALREADY_REGISTERED |
| ECP-10 | Required prerequisites missing | PREREQUISITES_MISSING |
| ECP-11 | Adding course exceeds 18 credits | CREDIT_LIMIT |
| ECP-12 | Eligible student, seats available | REGISTERED |
| ECP-13 | Eligible student, course full | WAITLISTED |
| ECP-14 | Outstanding dues = -1 | ValueError: Invalid dues |