import pandas as pd
import numpy as np
import sqlite3 as sql

df_1 = pd.read_csv("only_wood_customer_us_1.csv")

genders = {'0': 'Male', '1': 'Female', 'F': 'Female', 'M': 'Male'}
df_1['Gender'] = df_1['Gender'].replace(genders)

df_1['FirstName'] = df_1['FirstName'].str.replace('\W', '')
df_1['FirstName'] = df_1['FirstName'].str.title()

df_1['LastName'] = df_1['LastName'].str.replace('\W', '')
df_1['LastName'] = df_1['LastName'].str.title()

df_1['Email'] = df_1['Email'].str.lower()

df_1['City'] = df_1['City'].str.replace('_', '-')
df_1['City'] = df_1['City'].str.title()

df_1['Country'] = 'USA'

df_2 = pd.read_csv("only_wood_customer_us_2.csv", sep=';', header=None, 
            names = ['age', 'city', 'gender', 'name', 'email'])
            
df_2.age = df_2.age.str.replace('\D', '')
df_2.name = df_2.name.str.replace('\W', ' ')

df_2.city = df_2.city.str.replace('_', '-')
df_2.city = df_2.city.str.title()

df_2.email = df_2.email.str.lower()

name_df = df_2.name.str.split(expand=True)
df_2['first_name'], df_2['last_name'] = name_df[0], name_df[1]
df_2.drop('name', axis=1, inplace=True)
df_2.first_name = df_2.first_name.str.title()
df_2.last_name = df_2.last_name.str.title()
df_2.gender = df_2.gender.replace(genders)

df_2['country'] = 'USA'

df_3 = pd.read_csv("only_wood_customer_us_3.csv", sep='\t', skiprows=1,
            names = ['gender', 'name', 'email', 'age', 'city', 'country'])
            
df_3.gender = df_3.gender.replace({'string_Male': 'Male', 'string_Female': 'Female', 
                                        'boolean_1': 'Female', 'boolean_0': 'Male', 'character_M': 'Male', 'character_F': 'Female'})

df_3.name = df_3.name.str.replace('string_', '')
df_3.name = df_3.name.str.replace('\W', ' ')
name_df = df_3.name.str.split(expand=True)
df_3['first_name'], df_3['last_name'] = name_df[0], name_df[1]
df_3.drop('name', axis=1, inplace=True)
df_3.first_name = df_3.first_name.str.title()
df_3.last_name = df_3.last_name.str.title()

df_3.email = df_3.email.str.replace('string_', '')

df_3.age = df_3.age.str.replace('\D', '')
df_3.age = df_3.age.astype(int)

df_3.city = df_3.city.str.replace('string_', '')
df_3.city = df_3.city.str.replace('_', '-')
df_3.city = df_3.city.str.title()

df_3.country = 'USA'

df_1.columns = ['gender', 'first_name', 'last_name', 'user_name', 'email', 'age', 'city', 'country']

df = pd.concat([df_1, df_2, df_3], ignore_index=True)
df.drop('user_name', axis=1, inplace=True)

conn = sql.connect('wood.db')
c = conn.cursor()

c.execute("drop table if exists wood")
c.execute('''
            create table wood 
            (gender text,
            first_name text,
            last_name text,
            email text,
            age int,
            city text,
            country text,
            created_at text,
            referral text
            )
            ''')

for index,rows in df.iterrows():
    c.execute('insert into wood values (?, ?, ?, ?, ?, ?, ?, ?, ?)', (rows['gender'], rows['first_name'], 
                    rows['last_name'], rows['email'], rows['age'], rows['city'], rows['country'], '', ''))

for i, row in enumerate(c.execute("select * from wood")):
    print(row)
    if i == 10:
        break
    

c.close()