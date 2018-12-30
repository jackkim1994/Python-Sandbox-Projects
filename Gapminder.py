# Import Packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import Data: Life Expectancy by Countries and Years
gapminder = pd.read_csv('https://assets.datacamp.com/production/course_2023/datasets/gapminder.csv')

# Filter it into only the 19th Century Data. Also, Remove Duplicate Countries.
gapminder = gapminder.drop('Unnamed: 0', axis=1)
cols = gapminder.columns.tolist()
cols.insert(0, cols.pop(cols.index('Life expectancy')))
g1800s = gapminder.reindex(columns = cols)
g1800s = g1800s.loc[:,'Life expectancy':'1899']
g1800s = g1800s.drop_duplicates(subset=['Life expectancy'], keep='first')

# Check the 19th century data
g1800s.head()

# Check the info
g1800s.info()  # One object, one int64, and the rest float64

# Plot the data
g1800s.plot(kind='scatter', x='1800', y='1899')
plt.xlabel('Life Expectancy by Country in 1800')
plt.ylabel('Life Expectancy by Country in 1899')
plt.xlim(20, 55)
plt.ylim(20, 55)
# 140 of the 260 data did not change at all during 19th century.
# Possibly the result of no access to the data in the past.

# Check the data's validity
def check_null_or_valid(row_data):
    """Function that takes a row of data,
    drops all missing values,
    and checks if all remaining values are greater than or equal to 0
    """
    no_na = row_data.dropna()
    numeric = pd.to_numeric(no_na)
    ge0 = numeric >= 0
    return ge0

assert g1800s.columns[0] == 'Life expectancy'
assert g1800s.iloc[:,1:].apply(check_null_or_valid, axis=1).all().all()
assert g1800s['Life expectancy'].value_counts()[0] == 1

# Melt the Gapminder Data
gapminder_melt = pd.melt(gapminder, id_vars='Life expectancy')
gapminder_melt.head()
gapminder_melt.columns = ['country','year','life_expectancy']
gapminder_melt.head()

# Test the Data Types
# First Convert Year into numerics
assert gapminder.country.dtypes == np.object  # Test True
assert gapminder.year.dtypes == np.int64  # Test True
assert gapminder.life_expectancy.dtypes == np.float64  # Test True

# Check Country Spellings (Regular Expressions)
countries = gapminder_melt['country']
countries = countries.drop_duplicates()
countries.head()
pattern = '^[A-Za-z\.\s]*$'
mask = countries.str.contains(pattern)
mask_inverse = ~mask
invalid_countries = countries.loc[mask_inverse]
invalid_countries
# Some Countries are indeed valid. However, there exists programming error such as
# United Korea (former)\n

# Check missing Values
assert pd.notnull(gapminder_melt.country).all()  # No NaN in country
assert pd.notnull(gapminder_melt.year).all()  # No NaN in year

# Remove Missing Values
gapminder_melt_clean = gapminder_melt.dropna()  # Drop NaN
gapminder_melt_clean.shape  # 43857 rows, 3 columns

# Add Subplots to prepare for two graphs: Histogram and Line Chart
plt.subplot(2, 1, 1)

# Construct Histogram
gapminder_melt_clean.life_expectancy.plot(kind='hist')  # Histogram of life expectancy per year

# Group gapminder
gapminder_melt_clean_agg = gapminder_melt_clean.groupby('year')['life_expectancy'].mean()

# Check head and tail of the aggregated gapminder
gapminder_melt_clean_agg.head()
gapminder_melt_clean_agg.tail()

# Second Subplot
plt.subplot(2, 1, 2)

# Construct Line Chart
gapminder_melt_clean_agg.plot(kind='line')

# Add title and axis
plt.title('Life Expectancy over the years')
plt.xlabel('Year')
plt.ylabel('Life Expectancy')

# Display the plots
plt.tight_layout()

# Save thefiles
gapminder_melt_clean.to_csv('gapminder.csv')
gapminder_melt_clean_agg.to_csv('gapminder_agg.csv')