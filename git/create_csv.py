import collections

with open("data/original.csv", "r") as file:
    data = file.read()

go_from_year = 1850

new_csv = ""
lines = data.split("\n")

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

print(yearsdata)
new_csv = ""
x_year = 1
for year in yearsdata.values():
    average_yearly_temp = 0;
    num_months_recorded = 0
    for month in year.values():
        if(len(month)) > 0:
            average_yearly_temp += int(float(month))
            num_months_recorded += 1
    new_csv += str(x_year) + "," + str(average_yearly_temp / num_months_recorded) + "\n"
    x_year += 1
with open('data/data.csv', 'w') as file:
    file.write(new_csv)