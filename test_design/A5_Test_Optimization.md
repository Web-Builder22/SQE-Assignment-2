
# A5 – Test Case Optimization

## 1. Duplicate Test Analysis

The test suite was reviewed to identify duplicate test cases.

| Test Cases | Similarity | Decision |
|---|---|---|
| test_full_course_waitlisted and test_waitlist_adds_student_without_changing_credits | Both test a full course. | Keep both because one checks the decision and the other checks state changes. |
| test_available_seat and test_registration_updates_student_and_course | Both involve available seats. | Keep both because they test different functions. |

## 2. Optimization Strategy

- Remove only exact duplicate test cases.
- Keep tests that verify different requirements.
- Use meaningful test names.
- Reuse pytest fixtures if repeated setup becomes excessive.
- Maintain traceability between requirements and test cases.

## 3. Final Test Suite

- Total test cases: 20
- Exact duplicate test cases identified: 0
- Tests retained: 20

## 4. Conclusion

The test suite contains no exact duplicate test cases. Similar test scenarios were retained because they verify different system behaviors, including registration decisions and state modifications.
