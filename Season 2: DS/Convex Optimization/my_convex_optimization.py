## Plot this function to get a feel of what it looks like !
import numpy as np
import matplotlib.pyplot as plt

x_data = np.linspace(-10,10, 1000)
f = lambda x : (x - 1)**4 + x**2
y_data = f(x_data)

plt.plot(x_data, y_data)
plt.show()

## Write a simple dichotomous algorithm (bisection method) to find the zero of a function.
def find_root(f, a, b, method = 'bisection'):
    tol_err = 0.001
    if method == 'bisection':
        if f(a)*f(b) > 0:
            raise Exception("Wrong interval points are provided")
        
        x_zero = 0
        while abs(f(x_zero)) > tol_err:
            x_zero = (a+b)/2

            if f(a)*f(x_zero) < 0:
                b = x_zero
            else:
                a = x_zero
        
        return x_zero
    ## Newton's method
    elif method == 'Newton':
        # Since we want to find zero of f_prime, 
        # we need f'' to use Newton's method
        f_double_prime = lambda x: 12*((x-1)**2) + 2
        x_new = 0
        while abs(f(x_new)) > tol_err:
            x_new = x_new - f(x_new)/f_double_prime(x_new)       
        return x_new


f_prime = lambda x : 4*((x-1)**3) + 2*x
x_min = find_root(f_prime, -1, 1)
print('x_min: %.02f, f(x_min): %.02f, method = %s' % (x_min,f(x_min),"Bisection"))
x_min = find_root(f_prime, -1, 1, method='Newton')
print('x_min: %.02f, f(x_min): %.02f, method = %s' % (x_min,f(x_min),"Newton"))

## Checking result with scipy.optimize
from scipy.optimize import minimize_scalar

res = minimize_scalar(f, method='brent')
print('x_min: %.02f, f(x_min): %.02f, method = Brent' % (res.x, res.fun))

# plot curve
x = np.linspace(res.x - 1, res.x + 1, 100)
y = [f(val) for val in x]
plt.plot(x, y, color='blue', label='f')

# plot optima
plt.scatter(res.x, res.fun, color='red', marker='x', label='Minimum by scipy')
plt.scatter(x_min, f(x_min), color='green', marker='o', label='Minimum by find_root')

plt.grid()
plt.legend(loc = 1)
plt.show()

## Gradient Descent Methods

def gradient_descent(f, f_prime, start, learning_rate = 0.1):
    while abs(f_prime(start)) > 0.001:
        start = start - learning_rate*f_prime(start)
    return start

f = lambda x : (x - 1) ** 4 + x ** 2
f_prime = lambda x : 4*((x-1)**3) + 2*x
start = -1
x_min = gradient_descent(f, f_prime, start, 0.01)
f_min = f(x_min)

print("xmin: %0.2f, f(x_min): %0.2f, method=Gradient Descent" % (x_min, f_min))


## Simplex algorithm
from scipy.optimize import linprog

A = np.array([[2,1], [-4,5], [1, -2]])
b = np.array([10, 8, 3])
c = -1*np.array([1, 2])

def solve_linear_problem(A, b, c):
    res = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)], method='simplex')
    return (res.fun, res.x)

optimal_value, optimal_arg = solve_linear_problem(A, b, c)

print("The optimal value is: ", optimal_value, " and is reached for x = ", optimal_arg)

