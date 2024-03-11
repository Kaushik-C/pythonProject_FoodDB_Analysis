# Conversion of JSON data to
# dictionary


# importing the json module for handling json database
import json
#importing pandas module for working with input data in the form of dataframes
import pandas as pd
#importing matplotlib module to plot horizontal bar chart
import matplotlib.pyplot as plt
#importing numpy module for performing mathematical operations on input data
import numpy as np
#import statsmodels to perform Chi-square test
import scipy.stats as stats


# Opening json file
#with open('food_data.json') as json_file:
 #   input_data = json.load(json_file)

# Reading the input json file using Pandas library
#The read_json method reads JSON file into a data frame.

input_json = pd.read_json('food_data.json')
#print(input_json)

#Q1 Manufacturer sent smallest diff group of foods

data_frame = pd.DataFrame(input_json)
#print("The data frame is:")
#print(data_frame)

####################################################Question_1##########################################################

#Extracting the manufacturer data from input json file
input_manufacturer = data_frame['manufacturer']
#print(input_manufacturer)

#Filtering only foods which has valid manufacturer name and storing it as dictionary
dict_manu_list = dict(input_manufacturer.value_counts())
#print(dict_manu_list)

#Finding the manufacturer who has submitted less food items for the database
smallest_manufacturer = input_manufacturer.value_counts().min()
#print(smallest_manufacturer)

#Iterating through the valid manufacturer list and printing the expected smallest data submitted manufacturer
print("Q1: Manufacturer which has sent the smallest number of different group of foods for analysis:")
for key, value in dict_manu_list.items():
    if smallest_manufacturer == value:
        print(key," - ",value)

####################################################Question_2##########################################################
#Q2 foods with at least 2 different nutrients
input_nutrient = data_frame['nutrient']
#print(input_nutrient)

#The split() method splits a string into a list
def find_substring(input_str,matches):
    str_split = input_str.split(',')
    #result = list(filter(lambda x: sub_str1 in x, str_split))
    if any([x in input_str for x in matches]):
        result = True
    else:
        result = False

    return result

#data_frame['#nutrient'] = data_frame['nutrient'].apply(lambda x: len(x.split(',')))
matches = ["added", "total"]
data_frame['#nutrient'] = data_frame['nutrient'].apply(lambda x: len(x.split(','))-1 if find_substring(x,matches) else len(x.split(',')))
#print(data_frame[['nutrient','#nutrient']])
#Answer for Q2:
answer_Q2 = (len(data_frame[data_frame['#nutrient'] > 1]))
print("Q2: The foods in database that have atleast 2 nutrients is: " + str(answer_Q2))

####################################################Question_3##########################################################

#Extracting the entryById data from input json file
input_entryById = data_frame['entryById']
#print(input_entryById)

#Filtering only foods which has valid manufacturer name and storing it as dictionary
dict_entryById_list = dict(input_entryById.value_counts())
#print(dict_entryById_list)

#Finding the manufacturer who has submitted less food items for the database
highest_entrybyId = input_entryById.value_counts().max()
#print(highest_entrybyId)

print("Q3: Employer who has made the highest number of entries of different group of foods for analysis:")
for key, value in dict_entryById_list.items():
    if highest_entrybyId == value:
        print("Employee ID: ",key," - ",value,"entries")

####################################################Question_4##########################################################

#take a copy of entrybyId dictionary since two keys ' ' and 'None' needed to be replaced with 'Anonymous'

anonymous_entries = data_frame['entryById'].replace('None','Anonymous')
anonymous_entries = anonymous_entries.replace(' ','Anonymous')
#print(anonymous_entries)

dict_anonymous_entries = anonymous_entries.value_counts()
#print("The anonymous entries in dict is: ", str(dict_anonymous_entries['Anonymous']))
#print("The total no.of.entries in dict is: ", str(sum(anonymous_entries.value_counts())))

#print("Anonymous entries of different group of foods for analysis: ",str(Cdict['Anonymous']))
percentage_of_anonymous_entries = str((dict_anonymous_entries['Anonymous'] / (sum(anonymous_entries.value_counts()))) * 100)
print("Q4: Percentage of Anonymous entries of different group of foods for analysis: ",percentage_of_anonymous_entries,"%")

####################################################Question_5##########################################################

# i. Find the fgroup which has most anonymous entries
# ii. Find the fgroup which has least anonymous entries

#Update the existing dataframe with new entrybyId (where 'None' and ' ' replaced by 'Anonymous')
data_frame['#Entry_anonymous'] = anonymous_entries
#print(data_frame[['fgroup','#Entry_anonymous']])

#filter the entries which only have #Entry_anonymous column value as 'Anonymous'
filtered_anonymous_dataframe = data_frame.loc[data_frame['#Entry_anonymous'] == 'Anonymous']
#print("filtered_anonymous_dataframe", filtered_anonymous_dataframe)

#Convert the filtered columns to DataFrame to count the fgroup
df_anonym_entries_fgroup = pd.DataFrame(filtered_anonymous_dataframe['fgroup']).value_counts()

df_fgroup_entryanonymous = data_frame[['fgroup','#Entry_anonymous']]

df_anonym_entries_fgroup_name = df_fgroup_entryanonymous.loc[df_fgroup_entryanonymous['#Entry_anonymous'] == 'Anonymous', 'fgroup']
#print("df_anonym_entries_fgroup_name",pd.DataFrame(df_anonym_entries_fgroup_name).value_counts())
df_anonym_entries_fgroup_name_unique = pd.DataFrame(df_anonym_entries_fgroup_name).drop_duplicates()
#print("df_anonym_entries_fgroup_name_unique",df_anonym_entries_fgroup_name_unique)

keys_fgroup_has_anonym_entries = list(df_anonym_entries_fgroup_name_unique.fgroup.values)
#print("keys_fgroup_has_anonym_entries",keys_fgroup_has_anonym_entries)

anonym_fgroup = data_frame[data_frame['fgroup'].isin(keys_fgroup_has_anonym_entries)]
df_anonym_fgroup_total_entries = pd.DataFrame(anonym_fgroup['fgroup']).value_counts()
print("df_anonym_fgroup_total_entries", df_anonym_fgroup_total_entries)

observed = df_anonym_entries_fgroup
print("The observed values are:", observed)

anonym_fgroup_total_entries_ratio = df_anonym_fgroup_total_entries/len(df_anonym_fgroup_total_entries)
expected = anonym_fgroup_total_entries_ratio * len(df_anonym_entries_fgroup)
print("The expected values are: ", expected)

print("len(df_anonym_entries_fgroup)", len(df_anonym_entries_fgroup))

chi_square_stat = (((observed - expected)**2) / expected).sum()
print("chi_square_stat", chi_square_stat)

critical_value = stats.chi2.ppf(q=0.95,df=len(df_anonym_entries_fgroup))
print("critical_value:", critical_value)
pvalue = 1 - stats.chi2.cdf(x=chi_square_stat,df=len(df_anonym_entries_fgroup))
print("pvalue:", pvalue)

stats.chi2_contingency(observed=observed)

#stats.chisquare(f_obs=observed,f_exp=expected)

fgroup_min_anonymous_entries = df_anonym_entries_fgroup.min()
fgroup_max_anonymous_entries = df_anonym_entries_fgroup.max()

dict_anonym_entries_fgroup = dict(df_anonym_entries_fgroup)
#print("The dict anonymous entries is: ", dict_anonym_entries_fgroup)

print("The fgroup having minimum anonymous entries are: ")
#fgroup with min anonymous entries
for key, value in dict_anonym_entries_fgroup.items():
    if fgroup_min_anonymous_entries == value:
        print(key," - ",value)

print("The fgroup having maximum anonymous entries are: ")
#fgroup with max anonymous entries
for key, value in dict_anonym_entries_fgroup.items():
    if fgroup_max_anonymous_entries == value:
        print(key," - ",value)


####################################################Question_6##########################################################

#To create a horizontal bar chart that shows the frequency distribution for entryDate by month of database.
#By month means there should be only 12 bars, each representing a month from January to December

#Note:the input data is not filtered from 2002 to 2022 since the inputdata itself contains data only for 2002 to 2022

#Extracting the entryDate in yyyy-dd-mm format from input json file
data_frame['entry_by_date'] = pd.to_datetime(data_frame['entryDate'], unit='ms',origin='unix')
entry_by_date = data_frame['entry_by_date']
#print(entry_by_date)

#Extracting 'month' from the entry_by_date dataframe using pandas datetime library
data_frame['entry_by_month'] = pd.DatetimeIndex(data_frame['entry_by_date']).month
entry_by_month = data_frame['entry_by_month']
#print(entry_by_month)

#Get month name from month number using pandas datetime library
data_frame['entry_by_month_name'] = pd.to_datetime(data_frame['entry_by_date']).dt.month_name(locale = 'English')
entry_by_month_name = data_frame['entry_by_month_name']
#print(entry_by_month_name)

#count the month values (i.e., no.of.entries per month from 2002 to 2022) and store the result in a variable
df_entry_by_month_name_counts = entry_by_month_name.value_counts()

#sort the dataframe based on month values (i.e., no.of.entries per month from 2002 to 2022)
sorted_df_entry_by_month_name_counts = df_entry_by_month_name_counts.sort_values(axis=0,ascending=True)
#print(sorted_df_entry_by_month_name_counts)


#The prerequsite data for plotting horizontal bar chart is available now
#The horizontal bar chart (barh) is plotted using pandas and mathplotlib libraries

plot_barh = sorted_df_entry_by_month_name_counts.plot.barh(color='b',title='US Department of Agriculture (USDA) - Frequency distribution of food entries from 2002 to 2022')

#Give names for axes
plt.ylabel('Month')
plt.xlabel('Number of entries in USDA food database')

#bar_label method used to show values in the horizontal bar chart
plot_barh.bar_label(plot_barh.containers[0])

#Show the calculated horizontal bar chart which is the answer for Question: 6
plt.show()


####################################################Question_7##########################################################

#Create a look-up function to find out which food has the most given nutrient

def is_nutrient_found_in_food_database(dataframe):
    isFound = False
    filtered_nutrient_matches = dataframe['is_nutrient_in_food']
    isfound = dataframe['is_nutrient_in_food'].isin([True]).any()
    #print("Is found: ", str(isfound))
    return isfound

def find_food_has_more_lookup_nutrient(lookup_nutrient, dataframe):
    df_matched_food = dataframe.loc[dataframe['is_nutrient_in_food'] == True]['value']
    #print(df_matched_food)

    food_id_with_max_lookup_nutrient = df_matched_food.max()
    #print(food_id_with_max_lookup_nutrient)

    food_name_with_max_lookup_nutrient = dataframe.loc[dataframe['value'] == food_id_with_max_lookup_nutrient]['food']

    dict_food_name_with_max_lookup_nutrient = dict(food_name_with_max_lookup_nutrient)
    #print(dict_food_name_with_max_lookup_nutrient)

    for key, value in dict_food_name_with_max_lookup_nutrient.items():
        print("Food ID : ", key, "Food name :", value)

    return None


def food_for_nutrient(lookup_nutrient, dataframe):
    dataframe['is_nutrient_in_food'] = dataframe['nutrient'].str.contains(lookup_nutrient)
    is_match_found = is_nutrient_found_in_food_database(dataframe)
    #print(data_frame[['nutrient', 'is_nutrient_in_food']])
    if(bool(is_match_found) == True):
        print("Q7: Food which has more amount of look-up nutrient is: ")
        find_food_has_more_lookup_nutrient(lookup_nutrient, dataframe)
    else:
        print('Q7: No nutrient found')
    return None

#Invoke the food_for_nutrient method to print the search results
food_for_nutrient('Vitamin K',data_frame)

food_for_nutrient('Potassium K',data_frame)






