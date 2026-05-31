import argparse

from .calculator import get_coefficients, calculate_roots, display_results, plot_parabola


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='delta',
        description='Quadratic equation root calculator  (ax² + bx + c = 0)',
    )
    parser.add_argument(
        'coefficients',
        nargs='*',
        type=float,
        metavar='coef',
        help='Coefficients a, b, c. Omit for interactive mode.',
    )
    parser.add_argument(
        '--save',
        metavar='FILE',
        help='Save graph to file (e.g. graph.png) instead of displaying it.',
    )
    return parser


def _run_once(a: float, b: float, c: float, save_path: str | None = None) -> None:
    result = calculate_roots(a, b, c)
    display_results(result)
    plot_parabola(result, save_path=save_path)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.coefficients:
        if len(args.coefficients) != 3:
            parser.error('Provide exactly 3 coefficients: a b c')
        a, b, c = args.coefficients
        if a == 0:
            parser.error('Coefficient a cannot be zero.')
        _run_once(a, b, c, save_path=args.save)
        return

    while True:
        a, b, c = get_coefficients()
        _run_once(a, b, c, save_path=args.save)
        again = input('Calculate another? (y/n): ').strip().lower()
        if again != 'y':
            break
