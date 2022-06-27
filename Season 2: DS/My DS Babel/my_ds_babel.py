import sqlite3 as sql
import csv

class convert:
    def sql_to_csv(name_file_sql, name_file_csv):
        #connect to sql
        connection = sql.connect(name_file_sql)
        cursor = connection.cursor()

        #find table name
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        table_name = cursor.fetchone()[0]

        #find header
        cursor.execute("SELECT * FROM "+table_name)
        header = []
        for i in cursor.description:
            header.append(i[0])
        
        #write to csv file
        with open(name_file_csv, 'w') as file_csv:
            writer = csv.writer(file_csv)
            writer.writerow(header)
            for i in cursor:
                writer.writerow(i)
    
    def csv_to_sql(name_file_sql, name_file_csv):
        #connect to sql
        connection = sql.connect(name_file_sql)
        cursor = connection.cursor()

        #prepare table data
        with open(name_file_csv, 'r') as file_csv:
            reader = csv.reader(file_csv)
            col_names = next(reader)
            #ignore insufficient rows
            to_db = to_db = [tuple(row) for row in reader if len(row)==len(col_names)]
        
        #create table
        cursor.execute("create table if not exists Volcanos " + str(tuple(col_names)) + " ;")

        #insert values
        cursor.executemany("insert into Volcanos " + " values (?, ?, ?, ?, ?, ?);", to_db)

        connection.commit()
        connection.close()

#name of submit files
submit_file_csv = 'all_fault_lines.csv'
submit_file_sql = 'list_volcanos.db'

#name of source files
name_file_sql = 'all_fault_line.db'
name_file_csv = 'list_volcano.csv'

#start convert functions
convert.sql_to_csv(name_file_sql, submit_file_csv)

convert.csv_to_sql(submit_file_sql, name_file_csv)