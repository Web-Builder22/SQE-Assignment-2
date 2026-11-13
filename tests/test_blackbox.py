
import pytest

from registration import (
    Student,
    Course,
    check_credit_limit,
    prerequisites_satisfied,
    registration_decision,
    register_course,
    withdraw_course,
)


# A1: Equivalence Class Partitioning

# Credit limit tests
def test_credit_limit_exactly_18():
    assert check_credit_limit(15, 3) is True


def test_credit_limit_exceeded():
    assert check_credit_limit(16, 3) is False


def test_invalid_current_credits():
    with pytest.raises(ValueError, match="Invalid current credits"):
        check_credit_limit(-1, 3)


def test_invalid_course_credits():
    with pytest.raises(ValueError, match="Invalid course credits"):
        check_credit_limit(10, 0)


# Prerequisite tests
def test_no_prerequisites_required():
    assert prerequisites_satisfied(set(), set()) is True


def test_all_prerequisites_completed():
    assert prerequisites_satisfied(
        {"CS101", "MATH101"},
        {"CS101", "MATH101"}
    ) is True


def test_only_some_prerequisites_completed():
    assert prerequisites_satisfied(
        {"CS101"},
        {"CS101", "MATH101"}
    ) is False


# Registration decision tests
def test_positive_dues_block_registration():
    student = Student("S01", outstanding_dues=1)
    course = Course("CS201", 3, 30)

    assert registration_decision(student, course) == "DUES_BLOCK"


def test_already_registered():
    student = Student("S01", registered_courses={"CS201"})
    course = Course("CS201", 3, 30)

    assert registration_decision(student, course) == "ALREADY_REGISTERED"


def test_missing_prerequisites():
    student = Student("S01")
    course = Course("CS201", 3, 30, prerequisites={"CS101"})

    assert registration_decision(student, course) == "PREREQUISITES_MISSING"


def test_credit_limit_exceeded():
    student = Student("S01", current_credits=16)
    course = Course("CS201", 3, 30)

    assert registration_decision(student, course) == "CREDIT_LIMIT"


def test_available_seat():
    student = Student("S01")
    course = Course("CS201", 3, 30, enrolled=29)

    assert registration_decision(student, course) == "REGISTERED"


def test_full_course_waitlisted():
    student = Student("S01")
    course = Course("CS201", 3, 30, enrolled=30)

    assert registration_decision(student, course) == "WAITLISTED"


# A4: State change tests

def test_registration_updates_student_and_course():
    student = Student("S01", current_credits=6)
    course = Course("CS201", 3, 30, enrolled=10)

    result = register_course(student, course)

    assert result == "REGISTERED"
    assert "CS201" in student.registered_courses
    assert student.current_credits == 9
    assert course.enrolled == 11


def test_waitlist_adds_student_without_changing_credits():
    student = Student("S01", current_credits=6)
    course = Course("CS201", 3, 30, enrolled=30)

    result = register_course(student, course)

    assert result == "WAITLISTED"
    assert "S01" in course.waitlist
    assert student.current_credits == 6
    assert "CS201" not in student.registered_courses
    assert course.enrolled == 30


def test_waitlist_does_not_add_duplicate_student():
    student = Student("S01")
    course = Course("CS201", 3, 30, enrolled=30,
                    waitlist=["S01"])

    register_course(student, course)

    assert course.waitlist.count("S01") == 1


def test_withdrawal_updates_student_and_enrollment():
    student = Student("S01", current_credits=9,
                      registered_courses={"CS201"})
    course = Course("CS201", 3, 30, enrolled=10)

    result = withdraw_course(student, course)

    assert result is True
    assert "CS201" not in student.registered_courses
    assert student.current_credits == 6
    assert course.enrolled == 9


def test_withdraw_unregistered_course_changes_nothing():
    student = Student("S01", current_credits=6)
    course = Course("CS201", 3, 30, enrolled=10)

    result = withdraw_course(student, course)

    assert result is False
    assert student.current_credits == 6
    assert student.registered_courses == set()
    assert course.enrolled == 10


# Validation tests
def test_negative_dues_raise_value_error():
    student = Student("S01", outstanding_dues=-1)
    course = Course("CS201", 3, 30)

    with pytest.raises(ValueError, match="Invalid dues"):
        registration_decision(student, course)


def test_invalid_capacity_raises_value_error():
    student = Student("S01")
    course = Course("CS201", 3, 0)

    with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
        registration_decision(student, course)


# Registration decision must not mutate objects
def test_registration_decision_does_not_change_state():
    student = Student("S01", current_credits=6)
    course = Course("CS201", 3, 30, enrolled=10)

    registration_decision(student, course)

    assert student.current_credits == 6
    assert student.registered_courses == set()
    assert course.enrolled == 10
    assert course.waitlist == []
