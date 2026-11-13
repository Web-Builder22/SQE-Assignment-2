"""Requirements-based black-box tests (expected results come from REQUIREMENTS.md)."""
import pytest

from registration import (
    Course,
    Student,
    check_credit_limit,
    prerequisites_satisfied,
    register_course,
    registration_decision,
    withdraw_course,
)


def make_student(**overrides):
    values = dict(
        student_id="S100",
        completed_courses={"CS101", "MATH101"},
        current_credits=6,
        outstanding_dues=0,
        registered_courses=set(),
    )
    values.update(overrides)
    return Student(**values)


def make_course(**overrides):
    values = dict(
        code="CS201",
        credit_hours=3,
        capacity=30,
        enrolled=10,
        prerequisites={"CS101", "MATH101"},
        waitlist=[],
    )
    values.update(overrides)
    return Course(**values)


# A1: Equivalence-class representatives (FR-01 to FR-09).
@pytest.mark.parametrize(
    "test_id,student_args,course_args,expected",
    [
        ("ECP-01-zero-dues", {"outstanding_dues": 0}, {}, "REGISTERED"),
        ("ECP-02-positive-dues", {"outstanding_dues": 1}, {}, "DUES_BLOCK"),
        ("ECP-03-no-prerequisites", {}, {"prerequisites": set()}, "REGISTERED"),
        ("ECP-04-all-prerequisites", {"completed_courses": {"CS101", "MATH101"}}, {}, "REGISTERED"),
        ("ECP-05-some-prerequisites-missing", {"completed_courses": {"CS101"}}, {}, "PREREQUISITES_MISSING"),
        ("ECP-06-no-prerequisites-completed", {"completed_courses": set()}, {}, "PREREQUISITES_MISSING"),
        ("ECP-07-seat-available", {}, {"capacity": 30, "enrolled": 29}, "REGISTERED"),
        ("ECP-08-course-full", {}, {"capacity": 30, "enrolled": 30}, "WAITLISTED"),
        ("ECP-09-duplicate-registration", {"registered_courses": {"CS201"}}, {}, "ALREADY_REGISTERED"),
        ("ECP-10-credit-over-limit", {"current_credits": 16}, {"credit_hours": 3}, "CREDIT_LIMIT"),
    ],
)
def test_ecp_registration_classes(test_id, student_args, course_args, expected):
    student = make_student(**student_args)
    course = make_course(**course_args)
    assert registration_decision(student, course) == expected, test_id


@pytest.mark.parametrize(
    "test_id,current,new,expected",
    [
        ("ECP-11-valid-min-course-credit", 0, 1, True),
        ("ECP-12-valid-max-course-credit", 14, 4, True),
        ("ECP-13-one-over-credit-limit", 16, 3, False),
    ],
)
def test_ecp_credit_class_representatives(test_id, current, new, expected):
    assert check_credit_limit(current, new) is expected, test_id


# A2: Boundary-value tests.
@pytest.mark.parametrize(
    "test_id,current,new,expected",
    [
        ("BVA-02-current-credit-maximum", 18, 1, False),
        ("BVA-03-total-just-below-limit", 16, 1, True),
        ("BVA-04-total-exactly-18", 15, 3, True),
        ("BVA-06-course-credit-minimum", 4, 1, True),
    ],
)
def test_bva_credit_boundaries(test_id, current, new, expected):
    assert check_credit_limit(current, new) is expected, test_id


@pytest.mark.parametrize(
    "test_id,new_credit,error",
    [
        ("BVA-08-course-credit-below-minimum", 0, "Invalid course credits"),
        ("BVA-09-course-credit-above-maximum", 5, "Invalid course credits"),
    ],
)
def test_bva_course_credit_outside_boundary(test_id, new_credit, error):
    with pytest.raises(ValueError, match=error):
        check_credit_limit(0, new_credit)


@pytest.mark.parametrize(
    "test_id,enrolled,expected",
    [
        ("BVA-10-one-seat-below-capacity", 1, "REGISTERED"),
        ("BVA-11-exact-capacity", 2, "WAITLISTED"),
    ],
)
def test_bva_capacity_boundary(test_id, enrolled, expected):
    assert registration_decision(make_student(), make_course(capacity=2, enrolled=enrolled)) == expected, test_id


def test_bva_capacity_one_over_is_invalid():
    with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
        registration_decision(make_student(), make_course(capacity=2, enrolled=3))



def test_bva_negative_dues_is_invalid():
    with pytest.raises(ValueError, match="Invalid dues"):
        registration_decision(make_student(outstanding_dues=-1), make_course())


# A3: Decision-table outcomes and priority (FR-04 to FR-09).
@pytest.mark.parametrize(
    "test_id,student_args,course_args,expected",
    [
        ("DT-01-dues-over-duplicate", {"outstanding_dues": 1, "registered_courses": {"CS201"}}, {"prerequisites": {"MISSING"}, "capacity": 1, "enrolled": 1}, "DUES_BLOCK"),
        ("DT-02-duplicate-over-prerequisites", {"registered_courses": {"CS201"}}, {"prerequisites": {"MISSING"}, "capacity": 1, "enrolled": 1}, "ALREADY_REGISTERED"),
        ("DT-03-prerequisite-over-credit", {"completed_courses": set(), "current_credits": 18}, {"prerequisites": {"MISSING"}, "capacity": 1, "enrolled": 1}, "PREREQUISITES_MISSING"),
        ("DT-04-credit-over-availability", {"current_credits": 18}, {"prerequisites": set(), "capacity": 1, "enrolled": 1}, "CREDIT_LIMIT"),
        ("DT-05-full-course", {}, {"prerequisites": set(), "capacity": 1, "enrolled": 1}, "WAITLISTED"),
        ("DT-06-seat-available", {}, {"prerequisites": set(), "capacity": 1, "enrolled": 0}, "REGISTERED"),
    ],
)
def test_decision_table_priority(test_id, student_args, course_args, expected):
    student = make_student(**student_args)
    course = make_course(**course_args)
    before = (student.current_credits, set(student.registered_courses), course.enrolled, list(course.waitlist))
    assert registration_decision(student, course) == expected, test_id
    after = (student.current_credits, set(student.registered_courses), course.enrolled, list(course.waitlist))
    assert after == before, f"{test_id}: decision function must not mutate state (FR-10)"


# Registration and withdrawal state behavior (FR-10 to FR-14).
def test_register_course_updates_all_success_state():
    student = make_student(current_credits=6)
    course = make_course(capacity=30, enrolled=10)
    assert register_course(student, course) == "REGISTERED"
    assert student.registered_courses == {"CS201"}
    assert student.current_credits == 9
    assert course.enrolled == 11


def test_register_course_waitlists_without_changing_enrollment_state():
    student = make_student()
    course = make_course(capacity=1, enrolled=1)
    assert register_course(student, course) == "WAITLISTED"
    assert course.waitlist == ["S100"]
    assert student.current_credits == 6
    assert student.registered_courses == set()
    assert course.enrolled == 1


def test_register_course_does_not_duplicate_waitlist_entry():
    student = make_student()
    course = make_course(capacity=1, enrolled=1, waitlist=["S100"])
    assert register_course(student, course) == "WAITLISTED"
    assert course.waitlist == ["S100"]


@pytest.mark.parametrize(
    "student_args,course_args,expected",
    [
        ({"outstanding_dues": 1}, {}, "DUES_BLOCK"),
        ({"registered_courses": {"CS201"}}, {}, "ALREADY_REGISTERED"),
        ({"completed_courses": set()}, {}, "PREREQUISITES_MISSING"),
        ({"current_credits": 18}, {"prerequisites": set()}, "CREDIT_LIMIT"),
    ],
)
def test_unsuccessful_registration_leaves_state_unchanged(student_args, course_args, expected):
    student = make_student(**student_args)
    course = make_course(**course_args)
    before = (student.current_credits, set(student.registered_courses), course.enrolled, list(course.waitlist))
    assert register_course(student, course) == expected
    after = (student.current_credits, set(student.registered_courses), course.enrolled, list(course.waitlist))
    assert after == before


def test_withdraw_course_removes_registration_and_updates_both_objects():
    student = make_student(current_credits=9, registered_courses={"CS201"})
    course = make_course(credit_hours=3, enrolled=7)
    assert withdraw_course(student, course) is True
    assert student.registered_courses == set()
    assert student.current_credits == 6
    assert course.enrolled == 6


def test_withdraw_course_when_not_registered_changes_nothing():
    student = make_student(current_credits=9)
    course = make_course(enrolled=7)
    before = (student.current_credits, set(student.registered_courses), course.enrolled)
    assert withdraw_course(student, course) is False
    assert (student.current_credits, set(student.registered_courses), course.enrolled) == before


# Explicit validation order from FR-02 and FR-15.
def test_current_credit_validation_precedes_course_credit_validation():
    with pytest.raises(ValueError, match="Invalid current credits"):
        check_credit_limit(-1, 0)


def test_negative_dues_validation_precedes_capacity_validation():
    with pytest.raises(ValueError, match="Invalid dues"):
        registration_decision(make_student(outstanding_dues=-1), make_course(capacity=0, enrolled=0))
