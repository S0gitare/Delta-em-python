import cmath
import math
from dataclasses import dataclass, field

import numpy as np
import matplotlib.pyplot as plt


@dataclass
class QuadraticResult:
    a: float
    b: float
    c: float
    delta: float
    root_type: str  # 'real_distinct' | 'real_equal' | 'complex'
    roots: list = field(default_factory=list)


def parse_coefficient(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"'{value}' is not a valid number.")


def get_coefficients() -> tuple[float, float, float]:
    print('------------------------')
    print('  Simple Root Calculator')
    print('------------------------')
    print('Equation: ax² + bx + c = 0\n')

    while True:
        try:
            a = parse_coefficient(input('a: '))
            if a == 0:
                print('  a cannot be zero (equation would not be quadratic).\n')
                continue
            b = parse_coefficient(input('b: '))
            c = parse_coefficient(input('c: '))
            return a, b, c
        except ValueError as e:
            print(f'  Invalid input: {e} Please try again.\n')


def calculate_roots(a: float, b: float, c: float) -> QuadraticResult:
    delta = b ** 2 - 4 * a * c

    if delta > 0:
        sqrt_d = math.sqrt(delta)
        x1 = (-b + sqrt_d) / (2 * a)
        x2 = (-b - sqrt_d) / (2 * a)
        return QuadraticResult(a, b, c, delta, 'real_distinct', [x1, x2])

    if delta == 0:
        x = -b / (2 * a)
        return QuadraticResult(a, b, c, delta, 'real_equal', [x])

    sqrt_d = cmath.sqrt(delta)
    x1 = (-b + sqrt_d) / (2 * a)
    x2 = (-b - sqrt_d) / (2 * a)
    return QuadraticResult(a, b, c, delta, 'complex', [x1, x2])


def _format_complex(z: complex) -> str:
    sign = '+' if z.imag >= 0 else '-'
    return f'{z.real:.4f} {sign} {abs(z.imag):.4f}i'


def display_results(result: QuadraticResult) -> None:
    print('\n------------------------')
    print(f'  a = {result.a},  b = {result.b},  c = {result.c}')
    print(f'  Delta = {result.delta}')
    print('------------------------')

    if result.root_type == 'real_distinct':
        x1, x2 = result.roots
        print('  Two distinct real roots:')
        print(f'    x1 = {x1:.4f}')
        print(f'    x2 = {x2:.4f}')

    elif result.root_type == 'real_equal':
        print('  One repeated real root:')
        print(f'    x = {result.roots[0]:.4f}')

    else:
        x1, x2 = result.roots
        print('  Two complex roots (no real solutions):')
        print(f'    x1 = {_format_complex(x1)}')
        print(f'    x2 = {_format_complex(x2)}')

    print()


def _x_range(result: QuadraticResult) -> tuple[float, float]:
    vertex_x = -result.b / (2 * result.a)

    if result.root_type in ('real_distinct', 'real_equal'):
        real_roots = [float(r) for r in result.roots]
        span = max(abs(vertex_x - r) for r in real_roots)
        span = max(span, 3.0)
    else:
        span = 5.0

    return vertex_x - span * 1.6, vertex_x + span * 1.6


def plot_parabola(result: QuadraticResult, save_path: str | None = None) -> None:
    x_min, x_max = _x_range(result)
    x_values = np.linspace(x_min, x_max, 600)
    y_values = result.a * x_values ** 2 + result.b * x_values + result.c

    fig, ax = plt.subplots(figsize=(9, 5))

    coeff_str = f'{result.a}x²'
    if result.b != 0:
        coeff_str += f' {"+" if result.b > 0 else "-"} {abs(result.b)}x'
    if result.c != 0:
        coeff_str += f' {"+" if result.c > 0 else "-"} {abs(result.c)}'
    ax.plot(x_values, y_values, label=f'y = {coeff_str}', linewidth=2, color='steelblue')

    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.grid(color='gray', linestyle='--', linewidth=0.4, alpha=0.6)

    if result.root_type in ('real_distinct', 'real_equal'):
        real_roots = [float(r) for r in result.roots]
        ax.scatter(real_roots, [0] * len(real_roots), color='crimson', zorder=5, label='Roots')
        for x in real_roots:
            ax.annotate(
                f'({x:.2f}, 0)',
                xy=(x, 0),
                xytext=(0, 14),
                textcoords='offset points',
                ha='center',
                fontsize=9,
                color='crimson',
            )
    else:
        x1, x2 = result.roots
        msg = f'Complex roots: {_format_complex(x1)},  {_format_complex(x2)}'
        ax.text(0.5, 0.05, msg, transform=ax.transAxes,
                fontsize=9, ha='center', color='gray',
                bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.7))

    ax.set_title(f'Quadratic Function  (Δ = {result.delta:.4f})', fontsize=12)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f'  Graph saved to {save_path}')
    else:
        plt.show()
