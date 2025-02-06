# Pandas Lab
# Mason Nicoletti

'''
Instructions

For this assignment you can use any or all of the datasets I provided (described below) or choose two of your own!  

For each of the two datasets you select, produce four parts: 

1. Question
2. Psuedocode that answers the question
3. Single line transactions using pandas functions
4. Pipe the individual lines together and create a function

You can work with your groups for coding tips/advise or work through similar programming issues, but everyone must have their own set of questions and results. 
'''

import pandas as pd
import os
os.getcwd()

# Data: NFL Field Goals 2008
nfl08_fg = pd.read_csv("http://users.stat.ufl.edu/~winner/data/nfl2008_fga.csv")

'''
Question 1
- What quarter do NFL kickers attempt the most field goals, and what quarter do they make the most field goals?

Pseudocode:
- Make 4 separate data sets for each quarter (1, 2, 3, 4).
- Make a data table to hold the total field goals attempted and made per quarter.
- Append the total field goals made per quarter divided by the total attempted.
- Sum up the total fg attempted and the total fg made.
- Append the proportion of field goals attempted and made for each quarter.
'''

# Single line transactions
# print(nfl08_fg.info)
# print(nfl08_fg.head())

# Make the data sets by quarter
q1_fg = nfl08_fg[nfl08_fg["qtr"] == 1]
q2_fg = nfl08_fg[nfl08_fg["qtr"] == 2]
q3_fg = nfl08_fg[nfl08_fg["qtr"] == 3]
q4_fg = nfl08_fg[nfl08_fg["qtr"] == 4]

# Make a data table with the attempted and made fgs
fg_table = pd.DataFrame({
    'quarter': ['1', '2', '3', '4'],
    'fg_attempted': [q1_fg.shape[0], q2_fg.shape[0], q3_fg.shape[0], q4_fg.shape[0]],
    'fg_made': [q1_fg["GOOD"].sum(), q2_fg["GOOD"].sum(), q3_fg["GOOD"].sum(), q4_fg["GOOD"].sum()]
})

# Calculate the fg percentage by quarter and append to the table
fg_table = fg_table.assign(fg_percentage = lambda x: (x['fg_made'] / x['fg_attempted']))

# Calculate total fg attempted and made
total_fg = nfl08_fg.shape[0]
total_good = nfl08_fg[nfl08_fg["GOOD"] == 1].shape[0]

# Append proportion attempted and proportion made to the table
fg_table = fg_table.assign(prop_attempted = lambda x: (x['fg_attempted'] / total_fg))
fg_table = fg_table.assign(prop_made = lambda x: (x['fg_made'] / total_good))

# Print the final table
# print(fg_table)

# Function
def fg_by_qtr(df):
    q1_fg = nfl08_fg[nfl08_fg["qtr"] == 1]
    q2_fg = nfl08_fg[nfl08_fg["qtr"] == 2]
    q3_fg = nfl08_fg[nfl08_fg["qtr"] == 3]
    q4_fg = nfl08_fg[nfl08_fg["qtr"] == 4]
    total_fg = nfl08_fg.shape[0]
    total_good = nfl08_fg[nfl08_fg["GOOD"] == 1].shape[0]
    fg_table = pd.DataFrame()
    fg_table = fg_table.assign(quarter = ['1', '2', '3', '4'],
                               fg_attempted = [q1_fg.shape[0], q2_fg.shape[0], q3_fg.shape[0], q4_fg.shape[0]],
                               fg_made = [q1_fg["GOOD"].sum(), q2_fg["GOOD"].sum(), q3_fg["GOOD"].sum(), q4_fg["GOOD"].sum()],
                               prop_attempted = lambda x: (x['fg_attempted'] / total_fg),
                               prop_made = lambda x: (x['fg_made'] / total_good))
    return fg_table

print(fg_by_qtr(nfl08_fg))

# NFL Kickers in 2008 attempted and made the most field goals in the 2nd quarter. 
# However, the highest percentage of field goals made occurred in the 1st quarter, closely followed by the 4th quarter.


'''
Question 2
- What NFL team had the highest FG percentage in the 2008 season?

Pseudocode:
- Create a new dataset of the fg data grouped by team.
- Calculate the total made and divide by total attempted.
- Assign fg percentage as a new column to the grouped table.
- Sort the table by field goal percentage to identify the team with the greatest kicking success.
- Remove columns from the product table as to only see necessary fg stats.
'''

# Single line transactions

# Group data by team and sum up the total attributes per team
fg_teams = nfl08_fg.groupby('kickteam').sum()

# Append column for total attempted and percent made
fg_teams = fg_teams.assign(attempted = lambda x: x["GOOD"] + x["Missed"] + x["Blocked"])
fg_teams = fg_teams.assign(fg_percentage = lambda x: x["GOOD"] / x["attempted"])

# Sort the table by field goal percentage
fg_teams = fg_teams.sort_values(by="fg_percentage", ascending=False)

# Condense the table to field goal stats
fg_teams = fg_teams.loc[:, ["attempted", "GOOD", "Missed", "Blocked", "fg_percentage"]]

# Print the resulting table
# print(fg_teams.head())

# Function
def team_fg_percentage(df):
    fg_teams = df.groupby('kickteam').sum()
    fg_teams = fg_teams.assign(attempted = lambda x: x["GOOD"] + x["Missed"] + x["Blocked"],
                               fg_percentage = lambda x: x["GOOD"] / x["attempted"])
    fg_teams = fg_teams.sort_values(by="fg_percentage", ascending=False)
    fg_teams = fg_teams.loc[:, ["attempted", "GOOD", "Missed", "Blocked", "fg_percentage"]]
    return fg_teams

print(team_fg_percentage(nfl08_fg).head())

# The Detroit Lions had the highest field goal percentage in the 2008 season.


# Data: Red Wine Quality
redwine = pd.read_csv("data/winequality-red-ddl.csv")


'''
Question 3
- Is there a correlation between fixed acidity or pH and the quality of red wine?

Pseudocode:
- Make a new data set grouped by quality of red wine.
- Create a new table sorted by fixed acidity and another table sorted by pH.
- Find the average fixed acidity and pH for quality groupings.
- Append the two groupings together.
'''

# Single line transactions

# Condense important columns into a new data set (get rid of non-numeric columns)
wine_quality = redwine.loc[:,["fixed acidity", "pH", "quality"]]

# Group the data by wine quality
wine_quality = wine_quality.groupby("quality")

# Find the average fixed acidity and pH for each group
acidity_mean = wine_quality['fixed acidity'].mean()
ph_mean = wine_quality['pH'].mean()

# Append the two groupings together
quality_correlation = pd.merge(acidity_mean, ph_mean, on = "quality")

# Print the merged table
# print(quality_correlation)

# Function
def redwine_quality(df):
    quality = df.loc[:, ["fixed acidity", "pH", "quality"]]
    quality = quality.groupby("quality")
    acidity_mean = quality["fixed acidity"].mean()
    ph_mean = quality["pH"].mean()
    quality_correlation = pd.merge(acidity_mean, ph_mean, on = "quality")
    return quality_correlation

print(redwine_quality(redwine))

# There is no apparent correlation between the quality of red wines and their fixed acidity
# There is a positive correlation between redwine acidity (pH) and quality. Higher quality wines have a lower pH on average.


'''
Question 4
- Do wines with a greater alcohol concentration have a lower density?

Pseudocode:
- Create data sets for different ranges of alcohol concentration.
- Compute the average density for each data set.
- Sort the densities in the table to compare averages.
'''

# Single Line Transactions

# Create separate data grouped by alcohol
alcohol_12 = redwine.query('alcohol >= 12')
alcohol_11 = redwine.query('alcohol < 12 and alcohol >= 11')
alcohol_10 = redwine.query('alcohol < 11 and alcohol >= 10')
alcohol_9 = redwine.query('alcohol < 10')

# Calculate the average density for each grouping
density_12 = alcohol_12["density"].mean()
density_11 = alcohol_11["density"].mean()
density_10 = alcohol_10["density"].mean()
density_9 = alcohol_9["density"].mean()

# Create a table to compare densities
density_table = pd.DataFrame({
    'alcohol_concentration': ['+ 12%', '12-11%', '11-10%', '< 10%'],
    'average_density': [density_12, density_11, density_10, density_9]
})

# Sort the table by densities
density_table = density_table.sort_values(by="average_density", ascending=False)

# Return the top row of the data set
# print(density_table.iloc[0]['alcohol_concentration'])

# Function
def wine_densities(df):
    alcohol_12 = df.query('alcohol >= 12')["density"].mean()
    alcohol_11 = df.query('alcohol < 12 and alcohol >= 11')["density"].mean()
    alcohol_10 = df.query('alcohol < 11 and alcohol >= 10')["density"].mean()
    alcohol_9 = df.query('alcohol < 10')["density"].mean()
    density_table = pd.DataFrame({
        'alcohol_concentration': ['+ 12%', '12-11%', '11-10%', '< 10%'],
        'average_density': [alcohol_12, alcohol_11, alcohol_10, alcohol_9]
    })
    density_table = density_table.sort_values(by="average_density", ascending=False)
    highest_density = density_table.iloc[0]['alcohol_concentration']
    print(density_table)
    return(f"The {highest_density} alcohol concentration range has the highest density on average.")

print(wine_densities(redwine))

# Yes, wines with a greater alcohol concentration tend to have a lower density. 
# The grouping of wines with an alcohol concentration less than 10% had the highest average density.
