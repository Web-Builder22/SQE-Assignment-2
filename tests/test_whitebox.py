"""White-box tests for registration.py (SE3002 Assignment 2, Part B).

Expected values come from REQUIREMENTS.md, not from the code. Tests that fail
against the unmodified implementation expose genuine defects and must not be
edited to pass.

Test ID key
  WB-P*   basis-path tests (CFG of registration_decision, node ids as in docs/cfg.png)
  WB-MC*  MC/DC tests for the line-48 decision
  WB-RC*  tests for the compound decision on line 70 (register_course)
  WB-U*   unit-level branch tests for check_credit_limit / prerequisites_satisfied / withdraw_course

Line-48 decision:  raise if  (NOT (A and B)) or C
  A = 0 <= enrolled      B = enrolled <= capacity      C = capacity < 1
Python short-circuits: A False skips B and C; B False skips C.
"""
import pytest

import registration
from registration import (
    Course,
    Student,
    check_credit_limit,
    prerequisites_satisfied,
    register_course,
    registration_decision,
    withdraw_course,
)


def student(**kw):
    return Student(kw.pop("student_id", "S01"), **kw)


def course(**kw):
    kw.setdefault("code", "CS201")
    kw.setdefault("credit_hours", 3)
    kw.setdefault("capacity", 30)
    return Course(**kw)


# ---------------------------------------------------------------- basis paths
def test_wb_p01_negative_dues_raises():
    """Path P1: N2 True (L46)."""
    with pytest.raises(ValueError, match="Invalid dues"):
        registration_decision(student(outstanding_dues=-1), course())


def test_wb_p05_dues_above_1000_blocks():
    """Path P5: N6 True (L50). Covers line 51. dues=1001 so the path executes
    even with the defective '> 1000' threshold; the SRS case dues=1 is a
    black-box defect test."""
    assert registration_decision(student(outstanding_dues=1001), course()) == "DUES_BLOCK"


def test_wb_p06_already_registered():
    """Path P6: N7 True (L52)."""
    s = student(registered_courses={"CS201"})
    assert registration_decision(s, course()) == "ALREADY_REGISTERED"


def test_wb_p07_prerequisites_missing():
    """Path P7: N8 True (L54)."""
    c = course(prerequisites={"CS101"})
    assert registration_decision(student(), c) == "PREREQUISITES_MISSING"


def test_wb_p08_credit_limit():
    """Path P8: N9 True (L56)."""
    s = student(current_credits=18)
    assert registration_decision(s, course(credit_hours=1)) == "CREDIT_LIMIT"


def test_wb_p09_full_course_waitlisted():
    """Path P9: N10 True (L58). SRS FR-08: enrolled == capacity -> WAITLISTED.
    EXPECTED TO FAIL: the branch is infeasible in the current code because
    line 48 already rejects enrolled > capacity (defect)."""
    assert registration_decision(student(), course(capacity=1, enrolled=1)) == "WAITLISTED"


def test_wb_p10_registered():
    """Path P10: all decisions False -> L60."""
    assert registration_decision(student(), course(capacity=30, enrolled=0)) == "REGISTERED"


# ------------------------------------------- MC/DC for line 48 (A, B, C)
# Truth table (raise = decision True)           A    B    C    raise
#   MC1                                         F    NE   NE   True
#   MC2                                         T    F    NE   True
#   MC3                                         T    T    T    True
#   MC4                                         T    T    F    False
# Independence pairs: A -> (MC1, MC4)  B -> (MC2, MC4)  C -> (MC3, MC4)
def test_wb_mc1_enrolled_negative_A_false():
    """MC/DC A=F (B, C not evaluated). Also path P2."""
    with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
        registration_decision(student(), course(capacity=5, enrolled=-1))


def test_wb_mc2_enrolled_above_capacity_B_false():
    """MC/DC B=F (A=T, C not evaluated). Also path P3."""
    with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
        registration_decision(student(), course(capacity=5, enrolled=6))


def test_wb_mc3_capacity_zero_C_true():
    """MC/DC C=T (A=T, B=T). Also path P4."""
    with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
        registration_decision(student(), course(capacity=0, enrolled=0))


def test_wb_mc4_valid_capacity_all_false():
    """MC/DC base case A=T, B=T, C=F: no exception."""
    assert registration_decision(student(), course(capacity=5, enrolled=0)) == "REGISTERED"


# ------------------------- compound decision on line 70 (register_course)
# decision == "WAITLISTED" (W)  and  student_id not in waitlist (N)
# registration_decision is stubbed so these tests do not depend on the
# unreachable WAITLISTED path in the real implementation.
@pytest.fixture
def force_waitlisted(monkeypatch):
    monkeypatch.setattr(registration, "registration_decision", lambda s, c: "WAITLISTED")


def test_wb_rc1_waitlisted_new_student_is_appended(force_waitlisted):
    """W=T, N=T -> append (lines 70-71)."""
    s, c = student(current_credits=6), course(enrolled=30)
    assert register_course(s, c) == "WAITLISTED"
    assert c.waitlist == ["S01"]
    assert s.current_credits == 6 and s.registered_courses == set() and c.enrolled == 30


def test_wb_rc2_waitlisted_existing_student_not_duplicated(force_waitlisted):
    """W=T, N=F -> no append. Pair with RC1 shows N's independent effect."""
    c = course(enrolled=30, waitlist=["S01"])
    register_course(student(), c)
    assert c.waitlist == ["S01"]


def test_wb_rc3_non_waitlist_decision_leaves_waitlist_alone():
    """W=F (decision DUES_BLOCK) -> short-circuit, N not evaluated. Pair with RC1 for W."""
    c = course()
    assert register_course(student(outstanding_dues=1001), c) == "DUES_BLOCK"
    assert c.waitlist == []


# ------------------------------------------------ unit-level branch tests
def test_wb_u01_check_credit_limit_current_checked_first():
    """FR-02 order: both arguments invalid -> 'Invalid current credits' first."""
    with pytest.raises(ValueError, match="Invalid current credits"):
        check_credit_limit(19, 0)


def test_wb_u02_check_credit_limit_invalid_new_credits_high():
    """Second guard (L32) True via the upper bound."""
    with pytest.raises(ValueError, match="Invalid course credits"):
        check_credit_limit(0, 5)


def test_wb_u03_check_credit_limit_current_above_18():
    """First guard (L30) True via the upper bound."""
    with pytest.raises(ValueError, match="Invalid current credits"):
        check_credit_limit(19, 1)


def test_wb_u04_total_exactly_18_allowed():
    """FR-01 boundary at the return expression (L34). EXPECTED TO FAIL: '< 18'."""
    assert check_credit_limit(14, 4) is True


def test_wb_u05_prerequisites_none_completed_is_false():
    """L41 with non-empty required and no overlap."""
    assert prerequisites_satisfied(set(), {"CS101"}) is False


def test_wb_u06_prerequisites_partial_is_false():
    """FR-03 requires ALL prerequisites. EXPECTED TO FAIL: code uses any-overlap."""
    assert prerequisites_satisfied({"CS101"}, {"CS101", "MATH101"}) is False


def test_wb_u07_invalid_course_credits_propagate_from_decision():
    """L56 calls check_credit_limit; invalid credit_hours raises through it."""
    with pytest.raises(ValueError, match="Invalid course credits"):
        registration_decision(student(), course(credit_hours=0))


def test_wb_u08_withdraw_decrements_enrollment():
    """withdraw_course True branch (L77-81). FR-13. EXPECTED TO FAIL: enrolled not decremented."""
    s = student(current_credits=3, registered_courses={"CS201"})
    c = course(enrolled=5)
    assert withdraw_course(s, c) is True
    assert s.current_credits == 0 and s.registered_courses == set()
    assert c.enrolled == 4
