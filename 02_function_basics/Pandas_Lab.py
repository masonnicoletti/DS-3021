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


### Data

Any dataset in the class repo works or:

nf2008_fg: http://users.stat.ufl.edu/~winner/data/nfl2008_fga.csv

red_wine_quality: https://data.world/uci/wine-quality
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

# Group the data set by quarter
q_fg = nfl08_fg.groupby("qtr")
# [Unused]

# Calculate the fg attempted and made in each quarter
fg_attempted = q_fg.size()
fg_made = q_fg["GOOD"].sum()
# [Unused]

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
- 
'''