
# A4 – Initial Black-box Test Execution Results

## Test Execution Summary

- Total tests executed: 20
- Passed: 14
- Failed: 6
- Test framework: pytest
- Python version: 3.13.15

## Failed Tests and Identified Defects

| Test ID | Test Name | Expected Result | Actual Result | Defect |
|---|---|---|---|---|
| 1 | test_credit_limit_exactly_18 | True | False | Exactly 18 credits are incorrectly rejected. |
| 2 | test_only_some_prerequisites_completed | False | True | System accepts incomplete prerequisites. |
| 3 | test_positive_dues_block_registration | DUES_BLOCK | REGISTERED | Positive dues do not block registration. |
| 4 | test_full_course_waitlisted | WAITLISTED | REGISTERED | Full course incorrectly allows registration. |
| 5 | test_waitlist_adds_student_without_changing_credits | WAITLISTED | REGISTERED | Waiting-list operation is not performed. |
| 6 | test_withdrawal_updates_student_and_enrollment | Enrollment decreases by 1 | Enrollment unchanged | Withdrawal does not decrement course enrollment. |

## Conclusion

The initial black-box test execution identified five distinct defects in the reference implementation. Fourteen tests passed and six tests failed.

The implementation was not modified during initial black-box testing. Expected results were derived from REQUIREMENTS.md.
