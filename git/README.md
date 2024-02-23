# linear-regression-global-warming
A linear regression model made from scratch in python with numpy. Uses gradient descent to fit a line through the yearly average earth temperatures to visualize global warming and predict when the temperature increase will get over 2 degrees.

This is my entry to the coding challenge from Intro to The Math of Intelligence by Siraj Raval on Youtube.
https://github.com/llSourcell/Intro_to_the_Math_of_intelligence

## Usage
To use, just run `linear_regression.csv`. If for some reason the generated files go missing, you can easily remake them by running. `create_csv.py` and playing around with the `go_from_year` value, which is documented below.

## Data
The most important part of machine learning is the data. I am using monthly average global temperatures since 1850 from a kaggle dataset by Berkeley Earth. The dataset can be found [here](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data)

*Note: All temperatures are in Celcius

## Processing the Data
The original CSV `original.csv` contains far more data then I need to train. So `create_csv.py` takes in the original CSV and outputs a CSV file. The edited CSV file has the date starting from 1, which is the the first year, to the end year. The start and end years are included in the top of the CSV file.

The first 100 years are cut out because the data is largely inaccurate because of the technology avaliable at the time and because the data is quite irrelevant because the temperature did not increase. Removing 100 years off data also has the added benefit of making the gradient descent process faster.

```python
go_from_year = 1850
```
By setting this value, you can change how much of the original data is cut off.

The first for loop organizes the data and removes any data not needed. It then moves the temmps into an OrderedDict that is used in the next part.
```python
yearsdata = collections.OrderedDict()
for line in lines[1:]:
    values = line.split(",")
    if(len(values) > 2):
        date = values[0].split("-")
        average_temp = values[1]

        year = date[0]
        month = date[1]
        day = date[2]
        if(int(year) >= go_from_year):
            if not year in yearsdata:
                yearsdata[year] = {}

            yearsdata[year][month] = average_temp
```

The next for loop iterates through the first Dict and creates the final CSV. It takes the monthly temps and creates one yearly average, this is in an effort to speed up the gradient descent by removing un-needed data.
```python
for year in yearsdata.values():
    average_yearly_temp = 0;
    num_months_recorded = 0
    for month in year.values():
        if(len(month)) > 0:
            average_yearly_temp += int(float(month))
            num_months_recorded += 1
    new_csv += str(x_year) + "," + str(average_yearly_temp / num_months_recorded) + "\n"
    x_year += 1
```

## Running Linear Regression using Gradient Descent
Now that all of the data has been processed, I run the linear regression. Most of the action happens from the run() function

The first thing to do is initialize a few parameters
```python
learning_rate = 0.0001
num_iterations = 50000
```
Chances are these two values will have to be changed for different data, but these are the best ones currently. The num_iterations could probably be decreased to about 30,000, but 50,000 gives a bit more of an accurate result.

```python
b, m, cost_h = gradient_descent_runner(points, initial_b, initial_m, learning_rate, num_iterations)
```
This function runs gradient descent for num_iterations and will return the optimal b and m values for the set of points. It also returns a list of every cost from iteration 1 - num_iterations.

I should mention here that the gradient descent function updates b six times as fast as m. This is probably not optimal for most cases, but I found that in this case, it makes gradient descent finish faster.
```python
new_b = b_current - ((learningRate * 6) * b_gradient)
new_m = m_current - (learningRate * m_gradient)
```

The gradient descent function and squared error function are nothing special, so I wont talk about those.

## Results
AFter 50,000 iterations, I can plot the points and the best fit line.
![alt text](https://github.com/Grocode87/linear-regression-global-warming/blob/master/images/1850-2015-gw.png)

The plotted points and best fit line are pretty interesting, you can see that the average temperature has climbed significantly from 1850 to 2015.

After graphing the cost function
![alt text](https://github.com/Grocode87/linear-regression-global-warming/blob/master/images/cost_1.png)

You can see that the learning rate is good.

To see the increase in temperature from 1850 to today more clearly, I can do a little bit of math.
```python
start_temp = (m * 1) + b # Get the temperature in the first year (1850)
end_temp = (m * 166) + b # Get the temperature in the last year (2015) 

temp_increase = end_temp - start_temp # Get the total temperature increase from the first year to the last
yearly_increase = temp_increase / 166 # The total temperature increase by the number of years, to find the yearly temp increase
```
This gives me 0.0084, which means that the yearly temperature increase is 0.0084°C.

## More Results
This is already pretty cool, but there is an issue with it. If you look at the original chart, you can see that the yearly temperature goes up more and more, so a straight line is not the best thing.  A simple fix is to use the temperatures from the last 50 years instead of the last 150 years, this introduces a bit more noise, which could take away from the accuracy, but overall it will give a more relevant, accurate result.

To start I need to make the new data, so I will edit the `create_csv.py` file to give me data from the last 50 years.
```python
go_from_year = 1965
```
Now, after I run that I get a new file called `data-50years.csv`, which I can plug into the linear regression.

The results from this are quite a bit different, the yearly increase went from 0.0084 all the way to 0.0247, Which is a huge increase.

![alt text](https://github.com/Grocode87/linear-regression-global-warming/blob/master/images/50-years-gw.png)

## A Little Predicting
Up until now, I have not done anything past the recorded data, but if I have the mx+b for temperature increase, I may as well see when the temperature increase will get above 2 degrees celcius.

From the original model, the average temperature in 1750 is 7.976C. And the temperature in 2015 is 9.182. So that is a temperature increase of 1.206. Now, I'm going to use the 50 year model to predict how long it'll take to get the remaining 0.794 degrees.

```python
while not two_reached:
        while not two_reached:
        index += 1
        temp = m*(50+index) + b
        total_gained = temp - 7.976;

        if total_gained >= 2:
            two_reached = True
        else:
            year += 1
```

The code above keeps going until the total_gained integer gets above 2 degrees. The current temperature increase from 1880 to 2012 is 0.85 degrees celcius, according to the UN’s Intergovernmental Panel on Climate Change. It is said that by 2100, the temperature increase could be above 2 degrees, some even say it could be above 3 degrees. Which would have devestating effects on our planet.

   `A temperature increase of 2 degress celcius will be reached in the year 2046`
   
The results of my prediction say that we will reach a temperaturee increase of over 2 degrees by the year 2046, which I would say is an exceptable guess. 

