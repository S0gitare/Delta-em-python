import pytest
from src.delta.cli import build_parser


class TestBuildParser:
    def test_no_args(self):
        args = build_parser().parse_args([])
        assert args.coefficients == []
        assert args.save is None

    def test_three_coefficients(self):
        args = build_parser().parse_args(['1', '-5', '6'])
        assert args.coefficients == [1.0, -5.0, 6.0]

    def test_negative_coefficient(self):
        args = build_parser().parse_args(['1', '-2', '1'])
        assert args.coefficients == [1.0, -2.0, 1.0]

    def test_float_coefficient(self):
        args = build_parser().parse_args(['0.5', '-1', '0.5'])
        assert args.coefficients == [0.5, -1.0, 0.5]

    def test_save_flag(self):
        args = build_parser().parse_args(['1', '-5', '6', '--save', 'out.png'])
        assert args.save == 'out.png'

    def test_save_flag_without_coefficients(self):
        args = build_parser().parse_args(['--save', 'graph.png'])
        assert args.save == 'graph.png'
        assert args.coefficients == []
