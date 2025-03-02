import pandas as pd

# Load in the college data
college_data = pd.read_csv("https://raw.githubusercontent.com/masonnicoletti/DS-3021/refs/heads/main/data/cc_institution_details.csv")

'''
Prepare the college data
    Drop all location columns
    Drop string columns
    Drop rows that are 2-year university (in level)
    Drop rows with NA grad rates
    Drop all other grad rate rows
    Convert target grad_100_percent to above and below .90
    1 hot encoding hbcu and flagship
    Standardize numeric columns
    Find prevalence
    Make Test, Train, and Tune sets
'''

# Drop entries that are not 4-year universities
college_data = college_data.drop(college_data[college_data['level'] != "4-year"].index)

# Drop entries with NA grad_100_percentile
college_data = college_data.dropna(subset = ["grad_100_percentile"])

# Create list of columns to drop
location = [10, 11, 12]
grad_info = [30, 32, 33, 36, 38, 39] + list(range(40, 57))
financial = [26, 28, 29, 34, 35] + list(range(14, 20))
unnecessary = list(range(0, 6)) + [7, 21, 24, 57, 58, 60, 61]

drop_columns = location + grad_info + financial + unnecessary

# Drop unnecessary columns
college_data = college_data.drop(columns = college_data.columns[drop_columns], axis = 1)


college_data.info()