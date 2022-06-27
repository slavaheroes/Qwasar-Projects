import pandas, csv

class MySqliteRequest():

    def __init__(self):
        self.new()
        
    def new(self):
        ## source csv file, assume only one "from" file
        self.files = None

        ## selected cols
        self.selected = None

        ## where dictionary
        self.where_dict = {}

        ## insert
        self.insert_list = None

        ## update dict
        self.update_dict = {}

        self.join_ = None
        self.order_by = None
        # possible command types are "insert, update, delete, get_info, join"
        self.command_type = None

        return self

    def insert(self, file_name):
        self.files = file_name
        return self
    
    def values(self, *args):
        self.insert_list = list(args)
        self.command_type = 'insert'
        return self
    
    def update(self, file_name):
        self.files = file_name
        return self
    
    def update_set(self, col_name, value):
        self.update_dict[col_name] = value
        self.command_type = 'update'
        return self
    
    def delete(self):
        self.command_type = 'delete'
        return self

    ## the function name is changed because python has keyword "from"
    def from_table(self, file_names):
        self.files = file_names
        return self
    
    def select(self, *args):
        self.selected = list(args)
        self.command_type = "get_info"
        return self
    
    def where(self, column_name, criteria):
        self.where_dict[column_name] = criteria
        return self
    
    def join(self, column_on_a, join_filename, column_on_b):
        self.join_ = [column_on_a, join_filename, column_on_b]
        self.command_type = "join"
        return self
    
    def order(self, col_name, desc = False):
        if desc:
            self.order_by = [col_name, desc]
        else:
            self.order_by = [col_name]
        return self
    
    def run(self):
        if self.command_type == "get_info":
            df = pandas.read_csv(self.files)
            ## iterate df to satisfy where conditions
            for key in self.where_dict.keys():
                df = df[df[key].isin([self.where_dict[key]])]
            
            if self.order_by:
                df = df.sort_values(by=[self.order_by[0]], ascending = (len(self.order_by) == 1))

            if self.selected[0] == "*":
                return df
            else:
                return df[self.selected]

        elif self.command_type == "join":
            df_main = pandas.read_csv(self.files)
            df_join = pandas.read_csv(self.join_[1])

            df = pandas.merge(df_main, df_join, left_on = self.join_[0], right_on = self.join_[-1], how="inner")

            ## iterate df to satisfy where conditions
            for key in self.where_dict.keys():
                df = df[df[key].isin([self.where_dict[key]])]
            
            if self.order_by:
                df = df.sort_values(by=[self.order_by[0]], ascending = (len(self.order_by) == 1))

            if self.selected[0] == "*":
                return df
            else:
                return df[self.selected]

        elif self.command_type == "insert":
            df = pandas.read_csv(self.files)
            if len(self.insert_list) != len(df.columns):
                raise "Insertion Error. Check the number of attributes"
            
            df.loc[len(df)] = self.insert_list
            df.to_csv(self.files, index=False)
            return self

        elif self.command_type == "update":
            df = pandas.read_csv(self.files)
            for index,row in df.iterrows():
                for key in self.where_dict.keys():
                    if self.where_dict[key] != row[key]:
                        break
                else:
                    # where clause is satisfied, update this row
                    for key in self.update_dict.keys():
                        df.iloc[index, df.columns.get_loc(key)] = self.update_dict[key]
                        
                        
            
            df.to_csv(self.files, index=False)
            return self

        elif self.command_type == "delete":
            df = pandas.read_csv(self.files)
            del_index = []
            for index, row in df.iterrows():
                for key in self.where_dict.keys():
                    if self.where_dict[key] != row[key]:
                        break
                else:
                    # where clause satisfied, add row index to del_index array
                    del_index.append(index)
                    

            df.drop(df.index[del_index], inplace = True)      
            df.to_csv(self.files, index=False)
            return self




        

    

        
    

        