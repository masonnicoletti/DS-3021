# ML Bootcamp Lab
# Mason Nicoletti

'''
Step 1

College Completion Data
Q: What factors are the greatest predictors of a college having a 4-year graduation rate above 90%? 

Job Placement Data
Q: What are the greatest predicting factors for producing graduates with a salary in the top 75th Percentile.
'''

# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# Load in the two datasets
college_data = pd.read_csv("https://raw.githubusercontent.com/masonnicoletti/DS-3021/refs/heads/main/data/cc_institution_details.csv")
job_data = pd.read_csv("https://raw.githubusercontent.com/DG1606/CMS-R-2020/master/Placement_Data_Full_Class.csv")

# %%
# Predicting 4-year graduation rates with college completion data

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

# Convert object variables to categorical
college_data['hbcu'] = (college_data.hbcu.apply(lambda x: True if x == "X" else False)).astype('category')
college_data['flagship'] = (college_data.flagship.apply(lambda x: True if x == "X" else False)).astype('category')

#college_control = ["Public", "Private not-for-profit", "Private for-profit"]
#college_data['control'] = (college_data.control.apply(lambda x: x if x in college_control else "")).astype('category')
college_data['control'] = college_data['control'].astype('category')

# Convert graduation rate to a categorical variable above or below 90%
# college_data.grad_100_percentile = (college_data.grad_100_percentile.apply(lambda x: "above_90%" if x >= 90 else "below_90%")).astype('category')#

# Standardize numeric data
numeric_columns = list(college_data.select_dtypes('number'))
college_data[numeric_columns] = MinMaxScaler().fit_transform(college_data[numeric_columns])

# One-Hot Encoding
grad_categories = list(college_data.select_dtypes('category'))
college_data = pd.get_dummies(college_data, columns = grad_categories)

# Set graduation rate above 90% as the target variable
college_data['grad_rate_90'] = pd.cut(college_data.grad_100_percentile, bins = [-1, 0.90, 1], labels = [0,1])

# Drop the old graduation rate column
college_data = college_data.drop(['grad_100_percentile'], axis = 1)

# Calculate the prevalence of the target variable
prevalence = (college_data.grad_rate_90.value_counts()) / len(college_data.grad_rate_90)
# print(prevalence)

# Partitioning the data
# Create a Training and Testing data set stratified by the target variable
Train, Test = train_test_split(college_data, train_size = 1600, stratify = college_data.grad_rate_90)

# Create a tuning set split from the test data
Tune, Test = train_test_split(Test, train_size = 0.5, stratify = Test.grad_rate_90)

# Check prevalence for all three sets
# print(Train.grad_rate_90.value_counts())
# print(Test.grad_rate_90.value_counts())
# print(Tune.grad_rate_90.value_counts())

# %%
# Build into data preprocessing function
def college_data(url):
    college_data = pd.read_csv(url)
    college_data = college_data.drop(college_data[college_data['level'] != "4-year"].index)
    college_data = college_data.dropna(subset = ["grad_100_percentile"])
    location = [10, 11, 12]
    grad_info = [30, 32, 33, 36, 38, 39] + list(range(40, 57))
    financial = [26, 28, 29, 34, 35] + list(range(14, 20))
    unnecessary = list(range(0, 6)) + [7, 21, 24, 57, 58, 60, 61]
    drop_columns = location + grad_info + financial + unnecessary
    college_data = college_data.drop(columns = college_data.columns[drop_columns], axis = 1)
    college_data['hbcu'] = (college_data.hbcu.apply(lambda x: True if x == "X" else False)).astype('category')
    college_data['flagship'] = (college_data.flagship.apply(lambda x: True if x == "X" else False)).astype('category')
    college_data['control'] = college_data['control'].astype('category')
    numeric_columns = list(college_data.select_dtypes('number'))
    college_data[numeric_columns] = MinMaxScaler().fit_transform(college_data[numeric_columns])
    grad_categories = list(college_data.select_dtypes('category'))
    college_data = pd.get_dummies(college_data, columns = grad_categories)
    college_data['grad_rate_90'] = pd.cut(college_data.grad_100_percentile, bins = [-1, 0.90, 1], labels = [0,1])
    college_data = college_data.drop(['grad_100_percentile'], axis = 1)
    prevalence = (college_data.grad_rate_90.value_counts()) / len(college_data.grad_rate_90)
    Train, Test = train_test_split(college_data, train_size = 1600, stratify = college_data.grad_rate_90)
    Tune, Test = train_test_split(Test, train_size = 0.5, stratify = Test.grad_rate_90)
    Train_prevalence = (Train.grad_rate_90.value_counts()) / len(Train.grad_rate_90)
    Tune_prevalence = (Tune.grad_rate_90.value_counts()) / len(Tune.grad_rate_90)
    Test_prevalence = (Test.grad_rate_90.value_counts()) / len(Test.grad_rate_90)
    return Train_prevalence, Tune_prevalence, Test_prevalence, prevalence

url = "https://raw.githubusercontent.com/masonnicoletti/DS-3021/refs/heads/main/data/cc_institution_details.csv"
Train_p, Tune_p, Test_p, prevalence = college_data(url)

print(Train_p, Tune_p, Test_p, prevalence)

# %%
# Finding predictors of highest salaries with job placement data
'''
Turn to category (1H):
- gender
- ssc_b
- hsc_b
- degree_t
- workex
- specialisation

Target: salary >= .75
'''

# Load in the jobs data set
job_data = pd.read_csv("https://raw.githubusercontent.com/DG1606/CMS-R-2020/master/Placement_Data_Full_Class.csv")

# Remove rows with null salary data
job_data = job_data.dropna(subset = ["salary"])

# Drop unnecessary columns
drop_columns = [0, 13]
job_data = job_data.drop(job_data.columns[drop_columns], axis =1)

# One hot encoding for object type variables
object_list = list(job_data.select_dtypes('object'))
job_data = pd.get_dummies(job_data, columns = object_list)

# Normalize continuous variables
numeric_list = list(job_data.select_dtypes("number"))
job_data[numeric_list] = MinMaxScaler().fit_transform(job_data[numeric_list])

# Create target variable based on salary above the 75th percentile
#print(job_data.salary.describe())
job_data['salary'] = pd.cut(job_data.salary, bins = [-1, 0.135, 1], labels = [0,1])

# Calculate the prevalence of the target variable
prevalence = job_data.salary.value_counts()/len(job_data.salary)
# print(prevalence)

# Create data partitions
Train, Test = train_test_split(job_data, train_size = 118, stratify = job_data.salary)
Tune, Test = train_test_split(Test, train_size = 0.5, stratify = Test.salary)

#print(Train.shape)
#print(Test.shape)
#print(Tune.shape)

#print(job_data.info())

# %%
# Build into data preprocessing function
def job_data(url):
    job_data = pd.read_csv(url)
    job_data = job_data.dropna(subset = ["salary"])
    drop_columns = [0, 13]
    job_data = job_data.drop(job_data.columns[drop_columns], axis =1)
    object_list = list(job_data.select_dtypes('object'))
    job_data = pd.get_dummies(job_data, columns = object_list)
    numeric_list = list(job_data.select_dtypes("number"))
    job_data[numeric_list] = MinMaxScaler().fit_transform(job_data[numeric_list])
    job_data['salary'] = pd.cut(job_data.salary, bins = [-1, 0.135, 1], labels = [0,1])
    prevalence = job_data.salary.value_counts()/len(job_data.salary)
    Train, Test = train_test_split(job_data, train_size = 118, stratify = job_data.salary)
    Tune, Test = train_test_split(Test, train_size = 0.5, stratify = Test.salary)
    Train_prevalence = Train.salary.value_counts()/len(Train.salary)
    Tune_prevalence = Tune.salary.value_counts()/len(Tune.salary)
    Test_prevalence = Test.salary.value_counts()/len(Test.salary)
    return Train_prevalence, Tune_prevalence, Test_prevalence, prevalence

url = "https://raw.githubusercontent.com/DG1606/CMS-R-2020/master/Placement_Data_Full_Class.csv"
Train_p, Tune_p, Test_p, prevalence = job_data(url)

print(Train_p, Tune_p, Test_p, prevalence)


'''
Step 3
What do your instincts tell you about the data. Can it address your problem, what areas/items are you worried about?

College Completion Data
- When I first tried to make sense of this data set, I was overwhelmed by the amount of content in it.
- My data instincts told me that a lot of the columns were unnecessary: features such as location strings, details about grants and awards, additional graduation data aside from 4 year graduation rate, and more.
- Because of how my question was set up, I also realized I had to drop all the rows that didn't deal with 4-year universities.
- I believe that features such as student population, aid provided, student retention, carnegie count, etc. would provide useful insights to 4-yr graduation rate.
- The chosen target variable dealt with 4-year graduation rates, specifically colleges with grad rates above 90%. However, I noticed a large portion of the data had a 0% graduation rate, which may poorly impact the model.

Job Placement Data
- The first thing I noticed about this dataset is that there are far less features than the college completion data, but there is a greater proportion of object features to numeric features.
- I was uncertain about the meaning of several of the columns such as "ssc" and "hsc," however, I noticed that these options exist as both object and number data types.
- I was also curious as to where this sample of data came from. I found it interesting that the minimum salary in this dataset is $200,000. The highest salary in this data set is just shy of 1 million.
- Despite these ridiculously high salaries, I still thought it would be interesting to look at what factors may predict the highest salaries of the bunch.
'''