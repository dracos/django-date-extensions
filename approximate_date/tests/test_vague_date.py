from datetime import date

from pytest import mark, raises

from approximate_date import VagueDate


def test_comparison():
    y_past = VagueDate(year=2000)
    y_future = VagueDate(year=2100)

    assert y_past == y_past
    assert y_future == y_future

    assert not (y_past != y_past)
    assert not (y_future != y_future)

    assert y_past != y_future
    assert y_future != y_past

    assert y_future > y_past
    assert y_future >= y_past
    assert not (y_past > y_future)
    assert not (y_past >= y_future)

    assert y_past < y_future
    assert y_past <= y_future
    assert not (y_future < y_past)
    assert not (y_future <= y_past)

    # TODO test other operands
    assert VagueDate(2008, 9, 3) == date(2008, 9, 3)
    assert VagueDate(2008, 9, 3) < date(2009, 9, 3)
    assert VagueDate(2007) < date(2007, 9, 3)


@mark.parametrize(
    ("input", "format", "expected"),
    (
        ("9.5.1945", "%d.%m.%Y", {"year": 1945, "month": 5, "day": 9}),
        ("5.1945", "%m.%Y", {"year": 1945, "month": 5}),
        ("1945", "%Y", {"year": 1945}),
    ),
)
def test_from_string(input, format, expected):
    result = VagueDate.from_string(input, format)
    assert result.year == expected["year"]
    assert result.month == expected.get("month", 0)
    assert result.day == expected.get("day", 0)


def test_from_isoesque_string():
    assert VagueDate.from_string("1984") == VagueDate(year=1984)
    assert VagueDate.from_string("1984-03") == VagueDate(year=1984, month=3)
    assert VagueDate.from_string("1984-03-16") == VagueDate(year=1984, month=3, day=16)


def test_invalid_from_string():
    with raises(ValueError):
        VagueDate.from_string("9.5.1945", "%d.%Y")


def test_format():
    assert "*{:%m}*".format(VagueDate(year=1945, month=5)) == "*05*"


@mark.parametrize(
    ("value", "expected"),
    (
        (VagueDate(year=1945), "1945"),
        (VagueDate(year=1945, month=5), "1945-05"),
        (VagueDate(year=1945, month=5, day=9), "1945-05-09"),
    ),
)
def test_string(value, expected):
    assert str(value) == expected


def test_repr():
    assert repr(VagueDate(year=1945)) == "VagueDate(1945)"
