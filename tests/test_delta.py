import pytest
from src.delta.calculator import (
    calculate_roots,
    parse_coefficient,
    display_results,
    _format_complex,
    _x_range,
)


class TestParseCoefficient:
    def test_integer(self):
        assert parse_coefficient('3') == 3.0

    def test_negative(self):
        assert parse_coefficient('-2') == -2.0

    def test_float(self):
        assert parse_coefficient('1.5') == 1.5

    def test_invalid(self):
        with pytest.raises(ValueError):
            parse_coefficient('abc')

    def test_empty(self):
        with pytest.raises(ValueError):
            parse_coefficient('')


class TestCalculateRoots:
    def test_positive_delta_two_roots(self):
        result = calculate_roots(1, -5, 6)
        assert result.root_type == 'real_distinct'
        assert result.delta == 1.0
        roots = sorted(result.roots)
        assert abs(roots[0] - 2.0) < 1e-9
        assert abs(roots[1] - 3.0) < 1e-9

    def test_zero_delta_one_root(self):
        result = calculate_roots(1, -2, 1)
        assert result.root_type == 'real_equal'
        assert result.delta == 0.0
        assert abs(result.roots[0] - 1.0) < 1e-9

    def test_negative_delta_complex_roots(self):
        result = calculate_roots(1, 0, 1)
        assert result.root_type == 'complex'
        assert result.delta == -4.0
        assert len(result.roots) == 2
        assert all(isinstance(r, complex) for r in result.roots)

    def test_complex_root_values(self):
        result = calculate_roots(1, 0, 1)
        x1, x2 = result.roots
        assert abs(x1.real) < 1e-9
        assert abs(x1.imag - 1.0) < 1e-9
        assert abs(x2.real) < 1e-9
        assert abs(x2.imag + 1.0) < 1e-9

    def test_negative_leading_coefficient(self):
        result = calculate_roots(-1, 0, 4)
        assert result.root_type == 'real_distinct'
        roots = sorted(result.roots)
        assert abs(roots[0] - (-2.0)) < 1e-9
        assert abs(roots[1] - 2.0) < 1e-9

    def test_float_coefficients(self):
        result = calculate_roots(0.5, -1.0, 0.5)
        assert result.root_type == 'real_equal'
        assert abs(result.roots[0] - 1.0) < 1e-9

    def test_delta_stored_on_result(self):
        result = calculate_roots(2, 4, 2)
        assert result.delta == 0.0
        assert result.a == 2
        assert result.b == 4
        assert result.c == 2

    def test_large_coefficients_vieta(self):
        result = calculate_roots(1, -1000, 1)
        assert result.root_type == 'real_distinct'
        x1, x2 = sorted(result.roots)
        assert abs(x1 * x2 - 1.0) < 1e-6
        assert abs(x1 + x2 - 1000.0) < 1e-6


class TestFormatComplex:
    def test_positive_imaginary(self):
        assert _format_complex(complex(1, 2)) == '1.0000 + 2.0000i'

    def test_negative_imaginary(self):
        assert _format_complex(complex(0, -1)) == '0.0000 - 1.0000i'

    def test_zero_real(self):
        assert _format_complex(complex(0, 3)) == '0.0000 + 3.0000i'


class TestXRange:
    def test_real_distinct_centered(self):
        result = calculate_roots(1, -5, 6)  # roots at 2 and 3
        x_min, x_max = _x_range(result)
        assert x_min < 2
        assert x_max > 3

    def test_real_equal_centered(self):
        result = calculate_roots(1, -2, 1)  # root at 1
        x_min, x_max = _x_range(result)
        assert x_min < 1
        assert x_max > 1

    def test_complex_uses_default_span(self):
        result = calculate_roots(1, 0, 1)  # no real roots
        x_min, x_max = _x_range(result)
        assert x_max - x_min == pytest.approx(5.0 * 3.2)


class TestDisplayResults:
    def test_real_distinct_output(self, capsys):
        result = calculate_roots(1, -5, 6)
        display_results(result)
        out = capsys.readouterr().out
        assert 'Two distinct real roots' in out
        assert 'x1' in out
        assert 'x2' in out

    def test_real_equal_output(self, capsys):
        result = calculate_roots(1, -2, 1)
        display_results(result)
        out = capsys.readouterr().out
        assert 'One repeated real root' in out

    def test_complex_output(self, capsys):
        result = calculate_roots(1, 0, 1)
        display_results(result)
        out = capsys.readouterr().out
        assert 'complex' in out.lower()
        assert 'i' in out
