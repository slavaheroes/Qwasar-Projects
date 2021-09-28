'''
    Simple command line app to manage sql commands
    Note: after "from" keyword specify the name of csv file,
    because I assume table_name == input_file_name
'''

from my_sqlite_request import MySqliteRequest


def main():
    
    while True:

        sql_command = ""

        while not (";" in sql_command):
            cmd_line = input("> ")
            if cmd_line.strip() == "quit":
                
                return 0

            sql_command += cmd_line + " "

        
        tokens = sql_command.split()

        req = MySqliteRequest()

        if tokens[0] == 'SELECT':
            # 1. Find selected attributes
            attrs = []
            
            select_str = sql_command.split('SELECT')[-1].\
                split('FROM')[0].split(";")[0].split(',')  
            attrs = [each.strip() for each in select_str]
            

            
            if len(attrs) == 0:
                raise SyntaxError("Select attributes")
            

            # 2. File name
            if 'FROM' not in sql_command:
                raise SyntaxError("Check SQL Syntax")

            file_name = sql_command.split('FROM')[-1].split()[0].replace("'", "")

            # 3. Parse where clause if it's there
            if "WHERE" in sql_command:

                where_clause = sql_command.split("WHERE")[-1]
                where_clause = where_clause.split(';')[0]
                where_clause = where_clause.split('=')
                where_clause = [each.strip() for each in where_clause]
                where_clause = [each.replace("'", "") for each in where_clause]

                # for now we assume only one condition
                if len(where_clause) != 2:
                    raise SyntaxError("Check your SQL syntax")
                
                req = req.new()
                req = req.select(*attrs).from_table(file_name).\
                    where(*where_clause).run()
                print(req)
                
            else:
                req = req.new()
                req = req.select(*attrs).from_table(file_name).run()
                print(req)

        elif tokens[0] == 'INSERT' and tokens[1] == 'INTO' and tokens[3] == 'VALUES':
            file_name = tokens[2].replace("'", "").strip()
            
            values = sql_command.split("VALUES")[-1].split(";")[0].strip()

            values = values.replace("(", "").replace(")", "").split(",")

            req = req.new()
            req = req.insert(file_name).values(*values).run()

        elif tokens[0] == 'UPDATE':
            if "SET" not in sql_command or "WHERE" not in sql_command:
                raise SyntaxError("Check SQL Syntax")
            
            file_name = tokens[1].replace("'","").strip()

            set_attrs = sql_command.split("SET")[-1].split("WHERE")[0].split(",")
            set_attrs = [each.replace("'", "").split("=") for each in set_attrs]
            set_attrs = {each[0].strip() : each[1].strip() for each in set_attrs}

            # Assume only one where condition
            where_clause = sql_command.split("WHERE")[-1]
            where_clause = where_clause.split(';')[0]
            where_clause = where_clause.split('=')
            where_clause = [each.strip() for each in where_clause]
            where_clause = [each.replace("'", "") for each in where_clause]

            # for now we assume only one condition
            if len(where_clause) != 2:
                raise SyntaxError("Check your SQL syntax")
            
            req = req.new()
            req = req.update(file_name)
            
            for key in set_attrs.keys():
                req = req.update_set(key, set_attrs[key])
            
            req = req.where(*where_clause).run()

        elif tokens[0] == 'DELETE' and tokens[1] == "FROM":
            file_name = tokens[2].replace("'", "").strip()

            # Assume only one where condition
            where_clause = sql_command.split("WHERE")[-1]
            where_clause = where_clause.split(';')[0]
            where_clause = where_clause.split('=')
            where_clause = [each.strip() for each in where_clause]
            where_clause = [each.replace("'", "") for each in where_clause]

            # for now we assume only one condition
            if len(where_clause) != 2:
                raise SyntaxError("Check your SQL syntax")

            req = req.new()
            req = req.delete().from_table(file_name).where(*where_clause).run()
        
        else:
            raise SyntaxError("Check SQL Syntax")

    return 0








if __name__ == "__main__":
    main()