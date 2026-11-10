# A2 – Boundary Value Analysis (BVA)

## 1. Current Credits (0–18)

| Test ID | Current Credits | Expected Result |
|---|---:|---|
| BVA-01 | -1 | ValueError |
| BVA-02 | 0 | Valid |
| BVA-03 | 1 | Valid |
| BVA-04 | 17 | Valid |
| BVA-05 | 18 | Valid |
| BVA-06 | 19 | ValueError |

## 2. Course Credits (1–4)

| Test ID | Course Credits | Expected Result |
|---|---:|---|
| BVA-07 | 0 | ValueError |
| BVA-08 | 1 | Valid |
| BVA-09 | 2 | Valid |
| BVA-10 | 3 | Valid |
| BVA-11 | 4 | Valid |
| BVA-12 | 5 | ValueError |

## 3. Combined Credit Limit (18)

| Test ID | Current Credits | Course Credits | Expected Result |
|---|---:|---:|---|
| BVA-13 | 15 | 3 | True |
| BVA-14 | 16 | 3 | False |
| BVA-15 | 17 | 1 | True |
| BVA-16 | 17 | 2 | False |

## 4. Course Capacity and Enrollment

| Test ID | Capacity | Enrolled | Expected Result |
|---|---:|---:|---|
| BVA-17 | 30 | 29 | REGISTERED |
| BVA-18 | 30 | 30 | WAITLISTED |
| BVA-19 | 1 | 0 | REGISTERED |
| BVA-20 | 1 | 1 | WAITLISTED |

## 5. Outstanding Dues

| Test ID | Dues (PKR) | Expected Result |
|---|---:|---|
| BVA-21 | -1 | ValueError: Invalid dues |
| BVA-22 | 0 | Registration not blocked by dues |
| BVA-23 | 1 | DUES_BLOCK |