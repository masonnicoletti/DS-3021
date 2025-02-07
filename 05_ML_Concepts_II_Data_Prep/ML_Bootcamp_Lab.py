# ML Bootcamp Lab
# Mason Nicoletti

'''
Step 1

College Completion Data
Q: What factors are the greatest predictors of a college having a 4-year graduation rate above 90%? 

Job Placement Data
Q: What are the greatest predicting factors for producing graduates with a salary over $300,000.
'''
# %%
import pandas as pd

# Load in the two datasets
college_data = pd.read_csv("https://raw.githubusercontent.com/masonnicoletti/DS-3021/refs/heads/main/data/cc_institution_details.csv")
job_data = pd.read_csv("https://raw.githubusercontent.com/DG1606/CMS-R-2020/master/Placement_Data_Full_Class.csv")

#./data/cc_institution_details.csv

# %%
# Predicting 4-year graduation rates

# Prepare the college data
    # Drop all location columns
    # Drop string columns
    # Drop rows that are 2-year university
    # Drop rows with NA grad rates
    # Drop all other grad rate rows
    # Convert target grad_100_percent to above and below .90
print(college_data.info())
print(job_data.info())
# %%
