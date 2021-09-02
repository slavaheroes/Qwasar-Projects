import numpy as np
import matplotlib.pyplot as plt

## Part 1
def h(x, theta):
    return x.dot(theta)

def mean_squared_error(y_predicted, y_label):
    return (1.0/y_label.size) * np.sum(np.square(y_predicted-y_label))

## Part 2
## Write a class LeastSquareRegression to calculate the θ feature weights and make predictions.

class LeastSquaresRegression():
    def __init__(self,):
        self.theta_ = None  
        
    def fit(self, X, y):
        # Calculates theta that minimizes the MSE and updates self.theta_
        inv = np.linalg.inv(np.dot(X.T, X))
        self.theta_ = np.dot(np.dot(inv, X.T), y)

        
    def predict(self, X):
        # Make predictions for data X, i.e output y = h(X) (See equation in Introduction)
        return h(X, self.theta_)

X = 4 * np.random.rand(100, 1)
y = 10 + 2 * X + np.random.randn(100, 1)

def bias_column(X):
    z = np.ones((X.size, 1))
    return np.append(z, X, axis=1)
    

X_new = bias_column(X)

model = LeastSquaresRegression()
model.fit(X_new, y)

print("Theta my Normal Eq.: " + str(model.theta_))

y_new = model.predict(X_new)

def my_plot(X, y, y_new):
    plt.scatter(X, y)
    plt.plot(X, y_new, color='red')
    plt.show()

my_plot(X, y, y_new)

## Part 3

class GradientDescentOptimizer():

    def __init__(self, f, fprime, start, learning_rate = 0.001):
        self.f_      = f                       # The function
        self.fprime_ = fprime                  # The gradient of f
        self.current_ = start                  # The current point being evaluated
        self.learning_rate_ = learning_rate    # Does this need a comment ?

        # Save history as attributes
        self.history_ = [start]
    
    def step(self):
        # Take a gradient descent step
        # 1. Compute the new value and update selt.current_
        # 2. Append the new value to history
        # Does not return anything
        self.current_ = self.current_ - self.learning_rate_ * self.fprime_(self.current_)
        self.history_.append(self.current_)

    def optimize(self, iterations = 100):
        # Use the gradient descent to get closer to the minimum:
        # For each iteration, take a gradient step
        for i in range(iterations):
            self.step()

            
    def print_result(self):
        print("Best theta found is " + str(self.current_))
        print("Value of f at this theta: f(theta) = " + str(self.f_(self.current_)))
        print("Value of f prime at this theta: f'(theta) = " + str(self.fprime_(self.current_)))

def f(x):
    return 3 + ((x[0]-2)**2)*((x[1]-6)**2)

def fprime(x):
    return 2*np.array([(x[0]-2)*(x[1]-6)*(x[1]-6), (x[0]-2)*(x[0]-2)*(x[1]-6)])

grad = GradientDescentOptimizer(f, fprime, np.random.normal(size=(2,)), 0.001)
grad.optimize()
grad.print_result()

def myplot3D(history):
    x1 = np.arange(-5,5,0.01)
    x2 = np.arange(-5,5,0.01)
    X,Y = np.meshgrid(x1, x2)
    Z = 3 + np.square(X-2)*np.square(Y-6)

    fig = plt.figure(figsize=(10,8))
    x_theta = np.array([x[0] for x in history])
    y_theta = np.array([x[1] for x in history])
    z_theta = 3 + np.multiply(np.square(x_theta-2), np.square(y_theta-6))

    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X,Y,Z, color='b', alpha=0.2)
    ax.plot(x_theta, y_theta, z_theta, color='green')
    ax.scatter(x_theta, y_theta, z_theta, color='red')
    plt.show()


myplot3D(grad.history_)

## Part 4

theta_start = np.random.randn(2,1)
def gradient_descent(X, m, y, theta_start, iterations = 100, learning_rate = 0.1):
    for _ in range(iterations):
        grad = (2/m) * np.matmul(X.T, np.matmul(X, theta_start) - y)
        theta_start = theta_start - learning_rate*grad
    
    return theta_start

    

theta001 = gradient_descent(X_new, 100, y, theta_start, learning_rate=0.01)
theta01 = gradient_descent(X_new, 100, y, theta_start)
theta07 = gradient_descent(X_new, 100, y, theta_start, learning_rate=0.7)

print("Theta at learning rate = 0.01: "+ str(theta001))
print("Theta at learning rate = 0.1: "+ str(theta01))
print("Theta at learning rate = 0.7: "+ str(theta07))

y_predicted001 = h(X_new, theta001)
y_predicted01 = h(X_new, theta01)
y_predicted07 = h(X_new, theta07)

plt.plot(X, y, "b.",label="Data points")
plt.plot(X, y_predicted001, "r-", label = "l_rate = 0.01")
plt.plot(X, y_predicted01, "g-", label="l_rate = 0.1")
plt.grid()
plt.legend()
plt.title("Gradient descent output for diff. learning rates")
plt.show()


plt.plot(X, y, "b.",label="Data points")
plt.plot(X, y_predicted07, "c-", label="l_rate=0.7")
plt.legend()
plt.title("Gradient descent output for diff. learning rates")
plt.show()