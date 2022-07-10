#Tasks
# Which city has the highest total and why?
#     What product line the highest total in that city?
# Month with highest sales

import pandas as pd

df = pd.read_csv('supermarket_sales_uncleansed.csv')
print(df.tail().to_string())
print(f"\nTotal number of rows {len(df)}")

print("\nSo we have 1000 rows but lets see how many rows we have that do not have NaN\n")

def check_if_any_nans(df):
    print(df.isna().sum())
    print( f"\nCount all NaNs, total: {df.isnull().sum().sum()}" )

check_if_any_nans(df)

print("Thankfully not many NaNs, lets remove them and do a check again")
print("Data loaded in fine, although it does look like some cleaning is needed. Can see this from the first row under the column 'Unit price'. \n")
df = df.dropna()
check_if_any_nans(df)


print("\nI do wonder if the data we have is correct. Going to do a group by in columns to see.")

print("Becuase of the task of finding the city with the highest total and why, initally I am interetsed in a few columns which I believe will be significant. Such as the city, gender, product line, Branch and total.\n")


def gby(df, by, num):
    print( df.groupby(by).sum()[num] )
    
gby(df, ['Product line'], 'Total')



gby(df, ['Gender'], 'Total')

print("\nI noticed branch and city are same.\n") 
gby(df, ['Branch', 'City'], 'Total')



print("\nCity and branch looks fine. However gender has a '$f4' and Product line has a 'LL'. I do believe these two to be incorrect. Best to remove them since it's unclear what they are.\n")

test = df.loc[(df['Gender'] == '$f4') | (df['Product line'] == 'LL')]
print(test.to_string())


print("\nOkay found it now, lets filter it out and test to see if the incorrect data has been removed.\n")
df = df.loc[(df['Gender'] != '$f4')]
df = df.loc[(df['Product line'] != 'LL')]

gby(df, ['Gender'], 'Total')
print()
gby(df, ['Product line'], 'Total')


print("\nLooking better now, going to do the same for more columns\n")

gby(df, ['Quantity'], 'Total')

gby(df, ['Customer type'], 'Total')

print("\nCustomer type looks fine. However quantity has a unqiue issue, it's all meant to be numbers by the looks of it but there's a string 'six'. Best if we convert this and put it into the 6 row\n")

print(df.head().to_string())


print( (df.loc[df['Quantity'] == 'six']).to_string() )


df_six = df.loc[df['Quantity'] == 'six']
print(df_six.to_string())


for index in df_six.index:
    if df_six.loc[index,'Quantity']=='six':
        df_six.loc[index,'Quantity'] = '6'

print(df_six.to_string())


print("\nLets add this back into the main df.\n")
data = [df, df_six]
df = pd.concat(data)

gby(df, ['Quantity'], 'Total')


print("\ndata has been concat successfully, lets remove the six row now.\n")


df = df.loc[df['Quantity'] != 'six']
gby(df, ['Quantity'], 'Total')

print(df.head().to_string())


print("Cleaning looks like it's done.\n\n")

print("Data does look fine. We can now answer the questions.")

print("\nWhich city has the highest total and why?\n")


gby(df, ['City'], 'Total')


print("\n Naypyitaw has the highest total but lets see which product line performs best.\n")

gby(df, ['City', 'Product line'], 'Total')


print("\nIn Naypyitaw, Food and beverages is the higest total. \n")


def groupby_get_city_productline(df, column, city, product_line):
    df = df.groupby(column)
    df = df.get_group(city)
    df = df[df['Product line'] == product_line]
    return df


df_Naypyitaw_FoodNbeverages = groupby_get_city_productline(df, 'City', 'Naypyitaw', 'Food and beverages')
print(df_Naypyitaw_FoodNbeverages.head().to_string())


print("\nNow that we got all from Naypyitaw food and beverages. I do have a feeling, gender, customer type and payment may be telling.\n ")

gby(df_Naypyitaw_FoodNbeverages, ['Gender', 'Customer type'], 'Total')
print()
gby(df_Naypyitaw_FoodNbeverages, ['Payment', 'Gender', 'Customer type'], 'Total')
print()
gby(df_Naypyitaw_FoodNbeverages, ['Payment', 'Gender'], 'Total')
print()
gby(df_Naypyitaw_FoodNbeverages, ['Gender'], 'Total')



print("\n It looks like generally the women out spend men significantly in the Food and beverages in Naypyitaw.")

print(" Lets look at the tasks again..")

print("1) Which city has the highest total and why?")
print("2) What product line the highest total in that city?")
print("3) Month with highest sales")

print("We know the city with the highest total is Naypyitaw and the reason why is due to the Food and beverages.") 
print("We know the product line in Naypyitaw that has the highest total is Food and beverages")
print("We can see why this is happening from looking at Gender and Customer type. I do not believe the Payment column is as significant as the other two.")
print("     Although now I am curious to see if this trend holds true in the other two cities.")


print("So Yangon is the only city of the two where men out spend women in Food beverages. Two out of three cities, women spend a sifnifcant amount more then men on food and beverages.")

print("Now let's see if there's any trends for the months and the total\n")

print(df.head(10).to_string())



df['month'] = df['Date'].str[0:2]
print(df.head().to_string())


print("\nNeed to clean up the month column\n")

for index, row in df.iterrows():
    row = row['month']
    if '/' in row:
        row = row[:-1]
        df.loc[index, "month"] = row
    if row[0] == '0':
        row = row[1]
        df.loc[index, "month"] = row
        
print( df.head().to_string() )
        

print("\nmonth column looking good now. Looks like we wokring with only Jan, Feb and March.\n")

df_Naypyitaw_FoodNbeverages = groupby_get_city_productline(df, 'City', 'Naypyitaw', 'Food and beverages')
gby(df_Naypyitaw_FoodNbeverages, ['month', 'Gender', 'Customer type'], 'Total')
print()
gby(df_Naypyitaw_FoodNbeverages, ['month', 'Gender'], 'Total')
print()
gby(df_Naypyitaw_FoodNbeverages, ['month'], 'Total')


print("\nJanuary is the month with the highets sales.") 
print("Now I have answered all the tasks given. Although I am a bit cusious on the data. I want to explore it a bit more.")
print("It does look like regardless of the month, women spend more. Lets see if this holds true for the other two cities\n")


df_Yangon_FoodNbeverages = groupby_get_city_productline(df, 'City', 'Yangon', 'Food and beverages')
df_Mandalay_FoodNbeverages = groupby_get_city_productline(df, 'City', 'Mandalay', 'Food and beverages')

gby(df_Naypyitaw_FoodNbeverages, ['month', 'Gender'], 'Total')
print()
gby(df_Mandalay_FoodNbeverages, ['month', 'Gender'], 'Total')
print()
gby(df_Yangon_FoodNbeverages, ['month', 'Gender'], 'Total')

print("\nThe same trend as before where only in Yangon, men spend more on food and beverages. To be expected.")







