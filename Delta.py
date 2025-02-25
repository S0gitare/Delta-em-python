### Simple root calculator for a quadratic equation
import matplotlib.pyplot as plt
import numpy as np

print ('------------------------')
print ('Simple Root Calculator')
print ('------------------------')

print ('Enter the coefficients:')
a = input('a: ')
b = input('b: ')
c = input('c: ')

while a.isdigit() == False or b.isdigit() == False or c.isdigit() == False:
    print('\n Please enter integers only.')
    a = input('a: ')
    b = input('b: ')
    c = input('c: ')

a = int(a)
b = int(b)
c = int(c)

print ('------------------------')
print ('\n Roots')
print('\n a = ', a ,'\n','b = ', b, '\n', 'c = ', c, '\n')
print ('------------------------')

delta = (b**2) - (4*a*c)
print ('Delta = ', delta)

if delta > 0:
    print('and the roots are real and distinct.')
    x1 = (-b + np.sqrt(delta)) / (2*a)
    x2 = (-b - np.sqrt(delta)) / (2*a)
    print(f'Roots are x1 = {x1:.2f} and x2 = {x1:.2f}')
    x_roots = [x1, x2]
    y_roots = [0, 0]

elif delta == 0:
    print('and the roots are real and equal.')
    x = -b / (2*a)
    print(f'Root is x = {x:.2f}')
    x_roots = [x]
    y_roots = [0]
else:
    print('and has no real roots.')
    x_roots = []
    y_roots = []


x_values = np.linspace(-10, 10, 400)
y_values = a * x_values**2 + b * x_values + c

plt.plot(x_values, y_values, label=f'y = {a}x² + {b}x + {c}')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(color='gray', linestyle='--', linewidth=0.5)

if x_roots:
    plt.scatter(x_roots, y_roots, color='red', zorder=5, label='Roots')

plt.title('Gráfico da Função')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()

#this
