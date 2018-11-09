from pytest import mark


from approximate_date import VagueDate
from approximate_date.utils import vague_date_as_signed_int, vague_date_from_signed_int


@mark.parametrize(
    "value",
    (
        VagueDate(year=1),
        VagueDate(year=2),
        VagueDate(year=2, month=2),
        VagueDate(year=2, month=2, day=4),
        VagueDate(year=2, month=12),
    ),
)
def test_int_conversion(value):
    as_int = vague_date_as_signed_int(value)
    from_int = vague_date_from_signed_int(as_int)
    assert from_int == value, f"{from_int} ({as_int}) != {value}"
