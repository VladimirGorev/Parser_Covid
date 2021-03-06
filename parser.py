from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

pd.options.display.max_rows = 1000   # configurable pandas for display in 1000 lines
pd.set_option('display.expand_frame_repr', False)  # (
# since our table does not fit in the window width, disable its automatic wrapping to a new line
#  )

# Create our day in string format #
today = datetime.today()
today_str = today.strftime('%d-%m-%Y')
time_update_info = ""

# Parsing

url = 'https://coronavirusstat.ru/'
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

time_of_updating_information_on_the_site = soup.findAll('strong', class_='')
for elem in range(len(time_of_updating_information_on_the_site)):
    if time_of_updating_information_on_the_site[elem].find('span', class_='timer-span-russia') is not None:
        continue
    time_update_info = time_of_updating_information_on_the_site[elem].text

total_number_of_infections = []  # for clear data about infections
list_total_number_of_infections = []   # our list with infections


total_number_of_infections_raw = soup.findAll('div', class_='p-1 col-4 col-sm-2')  # search div with data infections
for elem in range(len(total_number_of_infections_raw)):  # iterating over the elements row data about infections
    if total_number_of_infections_raw[elem].find('span', class_='dline') is not None:  # (
        # cut off unnecessary found elements containing unnecessary data)
        continue
    total_number_of_infections.append(total_number_of_infections_raw[elem].text)  # add "clear" data

for elem in range(len(total_number_of_infections)):  # (
    # we get some unnecessary data from the required tag, so we cut it off, cut off the excess and glue it)
    string_row = total_number_of_infections[elem]
    string_with_spaces = string_row.split()
    list_total_number_of_infections.append(string_with_spaces[1])  # add our clear number to clear list data


# search span with city name
city_name_raw = soup.findAll('span', class_='small')
city_list = []  # our list city names
for elem in range(len(city_name_raw)):
    if city_name_raw[elem].find('a') is None:  # cut off unnecessary found elements containing
        continue
    city_list.append(city_name_raw[elem].text)  # add to list need city name


# search div with active_patients
active_patients_raw = soup.findAll('div', class_='p-1 col-4 col-sm-3')
active_patients_list = []
for elem in range(len(active_patients_raw)):
    a = active_patients_raw[elem].find('span', class_='dline')
    active_patients_list.append(a.text)


cured_raw = soup.findAll('div', class_='p-1 col-4 col-sm-2')
cured_people_list = []
for elem in range(len(cured_raw)):
    a = cured_raw[elem].find('span', class_='dline')
    if a == None:
        continue
    cured_people_list.append(a.text)
cut_cured_people_list = cured_people_list[:87]  # (
# since the classes are the same with European countries, we cut off the number of Russian regions we need)

dead_people_raw = soup.findAll('div', class_='p-1 col-3 col-sm-2 d-none d-sm-block')
dead_people_list = []
for elem in range(len(dead_people_raw)):
    a = dead_people_raw[elem].find('span', class_='dline')
    if a == None:
        break
    dead_people_list.append(a.text)


print("\n", "\n", "                       Disease statistics have been updated on the website at    ", time_update_info)


# create pandas DataFrame
table = pd.DataFrame({
    'City': city_list,
    'Total infections': list_total_number_of_infections,
    'Active patients': active_patients_list,
    'Cured people': cut_cured_people_list,
    'Dead people': dead_people_list
})
print(table)

table.to_excel("Covid.xlsx")  # create our pandas DataFrame in excel format
table.info()

table["Total infections"] = pd.to_numeric(table["Total infections"])
table["Active patients"] = pd.to_numeric(table["Active patients"])
table["Cured people"] = pd.to_numeric(table["Cured people"])
table["Dead people"] = pd.to_numeric(table["Dead people"])
table.info()

# Sorting out df at Total infections)
total_sorted = table[["City", "Total infections"]].sort_values(by='Total infections', ascending=False)

active_patients_sorted = table[["City", "Active patients"]].sort_values(by='Active patients', ascending=False)
cured_people_sorted = table[["City", "Cured people"]].sort_values(by='Cured people', ascending=False)
dead_people_sorted = table[["City", "Dead people"]].sort_values(by='Dead people', ascending=False)


def draw_total_infections():

    x = total_sorted["City"].head(10)
    y = total_sorted["Total infections"].head(10)
    plt.grid()  # grid display
    plt.bar(x, y)
    plt.title("Top 10 cities with the highest number of cases!", fontsize=20)
    plt.xlabel("Cities", fontsize=20)
    plt.ylabel("Total infections", fontsize=30)
    plt.xticks(x, rotation=10, fontsize=5)
    plt.show()


def draw_diagram(sorted_table, grouping_by_field_from_sorted_table):

    x = sorted_table["City"].head(10)
    y = sorted_table[grouping_by_field_from_sorted_table].head(10)
    plt.grid()  # grid display
    plt.bar(x, y)
    plt.title(f"Top 10 cities with the highest {grouping_by_field_from_sorted_table}", fontsize=20)
    plt.xlabel("Cities", fontsize=20)
    plt.ylabel(grouping_by_field_from_sorted_table, fontsize=30)
    plt.xticks(x, rotation=10, fontsize=5)
    plt.show()


draw_total_infections()

# draw_diagram(active_patients_sorted, "Active patients")
