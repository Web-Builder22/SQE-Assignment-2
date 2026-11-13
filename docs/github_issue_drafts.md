# GitHub Issue drafts - create these in the real repository

Use `.github/ISSUE_TEMPLATE/bug_report.md`. The records below are issue content drafts; they are not GitHub Issue URLs or already-created issues.

## D-01 - Exact 18-credit registration incorrectly rejected
- **Requirement:** FR-01.
- **Reproduction:** call `check_credit_limit(15, 3)`.
- **Expected:** `True`, because the combined load is exactly 18 credits.
- **Actual on starter:** `False`.
- **Failed test:** BVA-04 (also the boundary case in the workbook).
- **Local status:** corrected by changing the comparison from `< 18` to `<= 18`; regression suite passes.

## D-02 - Partial prerequisite completion incorrectly accepted
- **Requirement:** FR-03 and FR-06.
- **Reproduction:** call `prerequisites_satisfied({"CS101"}, {"CS101", "MATH101"})`.
- **Expected:** `False`; every required course must be completed.
- **Actual on starter:** `True`.
- **Failed test:** ECP-05.
- **Local status:** corrected by checking `required.issubset(completed)`; regression suite passes.

## D-03 - Small positive dues do not block registration
- **Requirement:** FR-04 and FR-09.
- **Reproduction:** use an otherwise eligible student with `outstanding_dues=1`.
- **Expected:** `DUES_BLOCK`.
- **Actual on starter:** `REGISTERED`; in the priority scenario DT-01 it proceeded to `ALREADY_REGISTERED`.
- **Failed tests:** ECP-02 and DT-01.
- **Local status:** corrected to block every value greater than zero; regression suite passes.

## D-04 - A full course is incorrectly treated as available
- **Requirement:** FR-08.
- **Reproduction:** use a valid course with `capacity=30` and `enrolled=30`.
- **Expected:** `WAITLISTED`.
- **Actual on starter:** `REGISTERED`.
- **Failed tests:** ECP-08 and DT-05; waitlist state tests also failed as a consequence.
- **Local status:** corrected to test `enrolled == capacity`; regression suite passes.

## D-05 - Withdrawal does not decrement course enrollment
- **Requirement:** FR-13.
- **Reproduction:** enroll a student in a course with `enrolled=7`, then withdraw the student.
- **Expected:** student credits decrease by course credits and course enrollment becomes 6.
- **Actual on starter:** student credits decreased, but course enrollment stayed 7.
- **Failed test:** `test_withdraw_course_removes_registration_and_updates_both_objects`.
- **Local status:** corrected by decrementing `course.enrolled`; regression suite passes.
