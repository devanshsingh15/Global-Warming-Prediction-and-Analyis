## Slightly (Very Slightly) edited code based off Siraj Raval's Intro To the math of intelligence
## https://github.com/llSourcell/Intro_to_the_Math_of_intelligence

from numpy import *
import math
import matplotlib.pyplot as plt

# Error Function
def compute_error_for_line_given_points(b, m, points):
    totalError = 0
    for i in range(0, len(points)):
        x = points[i, 0]
        y = points[i, 1]
        totalError += (y - (b + (m*x))) ** 2
    return totalError / float(len(points))

# Gradient Descent Function
def step_gradient(b_current, m_current, points, learningRate):
    b_gradient = 0
    m_gradient = 0
    
    N = len(points)
    for i in range(0, len(points)):
        x = points[i, 0]
        y = points[i, 1]

        b_gradient += -(2/N) * (y - ((m_current * x) + b_current)) # Calculate the b gradient
        m_gradient += -(2/N) * x * (y - ((m_current * x) + b_current)) # Calculate the m gradient

    new_b = b_current - ((learningRate * 6) * b_gradient) # Create the new b value, the learning rate in multiplied by two to train the model faster
    new_m = m_current - (learningRate * m_gradient) # Create the new m value
    return [new_b, new_m]

# Runs gradient descent for N iterations
def gradient_descent_runner(points, starting_b, starting_m, learning_rate, num_iterations):
    b = starting_b
    m = starting_m

    cost_h = []
    for i in range(num_iterations):
        b, m= step_gradient(b, m, array(points), learning_rate) # Run gradient descent once

        cost_h.append(compute_error_for_line_given_points(b, m, points)) # Calculate the cost and add it to a list, used to visualize the cost function later

        # Progress report for training (Log every 1000 iterations)
        if(i % 1000 == 0):
            print("After {0} iterations b = {1}, m = {2}, error = {3}".format(i, b, m, compute_error_for_line_given_points(b, m, points)))
    return b, m, cost_h

#Does the linear regression for the temperature in the past 166 years
def large_scale_regression():
    initial_b = 0
    initial_m = 0
    learning_rate = 0.0001
    num_iterations = 50000

    # Generate the data from the csv file 
    points = genfromtxt("data/data.csv", delimiter=",")

    print("Starting gradient descent at b = {0}, m = {1}, error = {2}".format(initial_b, initial_m,compute_error_for_line_given_points(initial_b, initial_m, points)))
    print("Running...")
    b, m, cost_h = gradient_descent_runner(points, initial_b, initial_m, learning_rate, num_iterations)
    print("Finished gradient descent, final cost:", compute_error_for_line_given_points(b, m, points))

    # Generate X and Y points for the trained m and b values
    x_points = []
    y_points = []
    for i in range(0, len(points)):
        x_points.append(points.item(i, 0))
        y_points.append(b + (m * points.item(i, 0)))
    
    # Plot the values and the best fit line
    plt.figure(1)
    plt.ylabel('Y')
    plt.xlabel('X')
    plt.plot(x_points, y_points, color='r')
    plt.scatter(points[:,0], points[:,1])

    # Plot the cost function over training period
    plt.figure(2) 
    plt.ylabel('Total cost')
    plt.xlabel('Iteration')
    plt.plot(cost_h)

    start_temp = (m * 1) + b # Get the temperature in the first year (1850)
    end_temp = (m * 166) + b # Get the temperature in the last year (2015) 

    temp_increase = end_temp - start_temp # Get the total temperature increase from the first year to the last
    yearly_increase = temp_increase / 166 # The total temperature increase by the number of years, to find the yearly temp increase

    print("Overall Increase:", temp_increase)
    print("Yearly Increase:", yearly_increase)

    print("\nShowing plots, close them to continue")
    plt.show()


# Does the linear regression for the temperature in the past 50 years
def fifty_year_regression():
    # Train the model for the last 50 years, and plot the outcome
    initial_b = 0
    initial_m = 0
    learning_rate = 0.001
    num_iterations = 10000
    points = genfromtxt("data/data-50years.csv", delimiter=",")
    b, m, cost_h = gradient_descent_runner(points, initial_b, initial_m, learning_rate, num_iterations)

     # Generate X and Y points for the trained m and b values
    x_points = []
    y_points = []
    for i in range(0, len(points)):
        x_points.append(points.item(i, 0))
        y_points.append(b + (m * points.item(i, 0)))
    
    # Plot the values and the best fit line
    plt.figure(3)
    plt.ylabel('Y')
    plt.xlabel('X')
    plt.plot(x_points, y_points, color='r')
    plt.scatter(points[:,0], points[:,1])

    # Plot the cost function over training period
    plt.figure(4) 
    plt.ylabel('Total cost')
    plt.xlabel('Iteration')
    plt.plot(cost_h)

    start_temp = (m * 1) + b # Get the temperature in the first year (1850)
    end_temp = (m * 50) + b # Get the temperature in the last year (2015) 
    print(end_temp)
    temp_increase = end_temp - start_temp # Get the total temperature increase from the first year to the last
    yearly_increase = temp_increase / 50 # The total temperature increase by the number of years, to find the yearly temp increase

    print("Overall Increase:", temp_increase)
    print("Yearly Increase:", yearly_increase)

    year = 2015
    index = 0
    two_reached = False

    while not two_reached:
        index += 1
        temp = m*(50+index) + b
        total_gained = temp - 7.976;

        if total_gained >= 2:
            two_reached = True
        else:
            year += 1

    print("A temperature increase of 2 degress celcius will be reached in the year " + str(year))

    plt.show()

# The starting point for the linear regression
def run():
   large_scale_regression()
   fifty_year_regression()
    

if __name__ == '__main__':
    run()