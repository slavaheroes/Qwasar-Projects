'''
    Simple command line app to manage sql commands
    Note: after "from" keyword specify the name of csv file,
    because I assume table_name == input_file_name
'''

from my_sqlite_request import MySqliteRequest


def main():
    sql_command = ""

    while not (";" in sql_command):
        cmd_line = input("> ")
        sql_command += cmd_line + " "

    tokens = sql_command.lower().split()

    req = MySqliteRequest()

    if tokens[0] == 'select':
        # 1. Find selected attributes
        attrs = []
        
        select_str = sql_command.lower().split('select')[-1].\
            split('from')[0].split(";")[0].split(',')  
        attrs = [each.strip() for each in select_str]
        

        
        if len(attrs) == 0:
            raise SyntaxError("Select attributes")
        

        # 2. File name
        if 'from' not in sql_command.lower():
            raise SyntaxError("Check SQL Syntax")

        file_name = sql_command.lower().split('from')[-1].split()[0].replace("'", "")

        # 3. Parse where clause if it's there
        if "where" in sql_command or "WHERE" in sql_command:
            if "where" in sql_command:
                where_clause = sql_command.split("where")[-1]
            else:
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

    elif tokens[0] == 'insert':
        raise NotImplemented
    elif tokens[0] == 'update':
        raise NotImplemented
    elif tokens[0] == 'delete':
        raise NotImplemented
    else:
        raise SyntaxError("Check SQL Syntax")

    return 0








if __name__ == "__main__":
    main()