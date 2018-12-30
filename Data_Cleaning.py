# Job Application Fillings
import pandas as pd
df = pd.read_csv('https://assets.datacamp.com/production/course_2023/datasets/dob_job_application_filings_subset.csv')
df.head()
df.tail()
df.shape
df.columns
df.info()

# Regular Expression to remove $ Sign
df['Initial Cost'] = df['Initial Cost'].replace({'\$':''},regex = True)
df['Total Est. Fee'] = df['Total Est. Fee'].replace({'\$':''},regex = True)

# Convert Series String -> Numeric
df['Initial Cost'] = pd.to_numeric(df['Initial Cost'])
df['Total Est. Fee'] = pd.to_numeric(df['Total Est. Fee'])

# Exploratory Data Analysis
df.describe()
print(df['Borough'].value_counts(dropna=False))
print(df['State'].value_counts(dropna=False))
print(df['Site Fill'].value_counts(dropna=False))

# Visual Exploratory Data Analysis
import matplotlib.pyplot as plt
df['Existing Zoning Sqft'].describe()
df['Existing Zoning Sqft'].plot(kind='hist',rot=70,logx=True,logy=True)
plt.show()

# Boxplot
df.boxplot(column='Initial Cost', by='Borough', rot=90)

# Scatter Plot
df.plot(kind='scatter', x='Initial Cost', y='Total Est. Fee', rot=70)

#--- Tidying Data for Analysis ---#
#-- Air Quality --#
# Melt the Data
import pandas as pd
import numpy as np
airquality = pd.read_csv('https://assets.datacamp.com/production/course_2023/datasets/airquality.csv')
airquality.head()
airquality_melt = pd.melt(frame=airquality, id_vars=['Month','Day'])
airquality_melt.head()

# Change variable & value column names
airquality_melt = pd.melt(airquality, id_vars=['Month', 'Day'], var_name='measurement', value_name='reading')
airquality_melt.head()

# Pivoting Data
airquality_melt.head()
airquality_pivot = airquality_melt.pivot_table(index=['Month','Day'], columns='measurement', values='reading')
airquality_pivot.tail()

# Resetting Data
airquality_pivot.index
airquality_pivot_reset = airquality_pivot.reset_index()
airquality_pivot_reset.index
airquality_pivot_reset.head() # Similar format as airquality

# Pivoting Duplicate Values (By Default, aggfunc = np.mean)
airquality_pivot = airquality.pivot_table(index=['Month','Day'], columns='measurement', values='reading', aggfunc=np.mean)
airquality_pivot.head()
airquality_pivot = airquality_pivot.reset_index()
airquality_pivot.head() # Reset the index

# Tubercolosis (Cases of Tubercolosis by Country)
tb = pd.read_csv('https://assets.datacamp.com/production/course_2023/datasets/tb.csv')
tb.head()
tb_melt = pd.melt(frame=tb, id_vars=['country','year'])
tb_melt['gender'] = tb_melt.variable.str[0]
tb_melt['age_group'] = tb_melt.variable.str[1:]
tb_melt.head()

# Ebola (Cases and Death Counts by Countries and States)
ebola = pd.read_csv('https://assets.datacamp.com/production/course_2023/datasets/ebola.csv')
ebola_melt = pd.melt(frame=ebola, id_vars=['Date','Day'], var_name='type_country', value_name='counts')
ebola_melt.head()

ebola_melt['str_split'] = ebola_melt.type_country.str.split('_')  # Split Underscored Strings
ebola_melt['type'] = ebola_melt.str_split.str.get(0)  # Type of Ebola
ebola_melt['country'] = ebola_melt.str_split.str.get(1)  # Country that had Ebola
ebola_melt.head()

#-- Combining Data ---#
# Sample NYC Uber Data (April-June 2014)
uber = pd.read_csv('https://assets.datacamp.com/production/course_2023/datasets/nyc_uber_2014.csv')
uber.shape
uber = uber.drop('Unnamed: 0',1)
uber.head()
uber = uber.rename(columns={'Date/Time' : 'Date_Time'})

# Separate into three uber dataframe (April, May, June)
import fnmatch
pattern = '4/1/2014*'
matching = fnmatch.filter(uber['Date_Time'], pattern)
uber1 = uber.query('Date_Time in @matching')

pattern = '5/1/2014*'
matching = fnmatch.filter(uber['Date_Time'], pattern)
uber2 = uber.query('Date_Time in @matching')

pattern = '6/1/2014*'
matching = fnmatch.filter(uber['Date_Time'], pattern)
uber3 = uber.query('Date_Time in @matching')


# If Concatentation was needed:
row_concat = pd.concat([uber1, uber2, uber3]) # uber1 (April), uber2 (May), uber3 (June)
row_concat.shape # <=> uber.shape

# Back to Ebola Data but Tidying Ebola
status_country = ebola_melt.loc[:, 'type':'country']
status_country.head()
ebola_tidy = pd.concat([ebola_melt, status_country], axis=1)
ebola_tidy.shape
ebola_tidy.head()

# Import Multiple Files
import glob
import pandas as pd
pattern = '*.csv'
csv_files = glob.glob(pattern)
csv2 = pd.read_csv(csv_files[1])

# Import multiple files with Iteration (Assume csv files contain three uber data)
frames = []
for csv in csv_files:
    df = pd.read_csv(csv)
    frames.append(df)
uber = pd.concat(frames)
uber.head()

#--- Merging Data ---#
# Import Database Survey and Test
import sqlite3 as lite
connection = lite.connect('survey.db')
cursor = connection.cursor()
cursor.execute("SELECT Site.lat, Site.long FROM Site;")
results = cursor.fetchall()
for r in results:
    print(r)
cursor.close()
connection.close()

# Create a function for a faster process
import pandas as pd
def lite_query(query, db):
    con = lite.connect(db)
    crs = con.cursor()
    crs.execute(query)
    results = crs.fetchall()
    crs.close()
    con.close()
    return results

# Fix Columns and Dataframes
import pandas as pd
site = pd.DataFrame(lite_query('SELECT * FROM Site;','survey.db'))
visited = pd.DataFrame(lite_query('SELECT * FROM Visited;','survey.db'))
site.columns = ['name','lat','long']
visited.columns = ['id','site','dated']
site
visited

# Merge Data
o2o = pd.merge(left=site, right=visited, left_index=True, right_index=True)
# o2o = site.join(visited, how='inner')

o2o = pd.merge(left=site,right=visited, left_on = 'name', right_on='site')
# Major Difference: Merge Function takes account of duplicate values!!!

#--- Tips Data ---#
# Change Objects to Category
tips = pd.read_csv('https://assets.datacamp.com/production/course_2023/datasets/tips.csv')
tips.info()
tips.sex = tips.sex.astype('category')
tips.smoker = tips.smoker.astype('category')
tips.info()

# Change Objects to Numeric while converting string missing values to NaN
tips.total_bill = pd.to_numeric(tips.total_bill, errors='coerce')
tips.tip = pd.to_numeric(tips.tip, errors='coerce')
tips.info()

#--- Regular Expression Practice ---#
import re
prog = re.compile('\d{3}\-\d{3}\-\d{4}')
result = prog.match('123-456-7890')
bool(result)  # True
result = prog.match('1123-456-7890')
bool(result)  # False

# Extracting numbers from strings
matches = re.findall('\d+', 'the recipe calls for 10 strawberries and 1 banana')
matches  # 10 and 1

# More Practices
pattern1 = bool(re.match(pattern='\d{3}\-\d{3}\-\d{4}', string='123-456-7890'))
pattern1  # True

pattern2 = bool(re.match(pattern='\$\d*\.\d*', string='$123.45'))
print(pattern2)

pattern3 = bool(re.match(pattern='[A-Z]\w*', string='Australia'))
print(pattern3)

#--- Apply Functions ---#
# Recall Tips
tips.head()
def recode_gender(gender):
    if gender == 'Female':
        return 0
    elif gender == 'Male':
        return 1
    else:
        return np.nan
# Apply Method
tips['recode'] = tips.sex.apply(recode_gender)

# Replace Method
dollar = []
for d in tips.total_dollar:
    dollar.append('${:,.2f}'.format(d))
tips['total_dollar'] = pd.DataFrame(dollar)

# Using Lambda Replace
tips['total_dollar_replace'] = tips.total_dollar.apply(lambda x: x.replace('$',''))

# Using Regular Expression
tips['total_dollar_re'] = tips.total_dollar.apply(lambda x: re.findall('\d+\.\d+', x)[0])

tips.head()

#--- Drop Duplicates ---#
tips = pd.read_csv('https://assets.datacamp.com/production/course_2023/datasets/tips.csv')
tips_test = tips
tips_test.info()
tips_test = tips_test.drop_duplicates()  # drop_duplicates from pandas
tips_test.info()  # One duplicate value dropped from 244 to 243

# Use Airquality to drop duplicates and handle missing data
airquality.info()
oz_mean = airquality.Ozone.mean()  # Create Mean of Ozone
airquality['Ozone'] = airquality.fillna(oz_mean)  # Replace NA with mean of Ozone
airquality.info()  # Missing values from Ozone has been filled

# Ebola Non-missing Value Check
assert ebola.notnull().all().all()  # Returns that there's Missing Value (Assertion Error)
assert (ebola >= 0).all().all()  # Returns that there's Missing Value (Assertion Error)
ebola.info()
# Method 1: Drop Missing Values
ebola_1 = ebola.dropna()
ebola_1.info()  # Bad Idea; Only one value remains
# Method 2: Change all NA's to 0
ebola_2 = ebola.fillna(0)
ebola_2.info()  # Viable. But make sure to note that this option may not always work
assert ebola_2.notnull().all().all()  # Passed the Assertion Test
assert (ebola_2 >= 0).all().all()  # Passed the Assertion Test

