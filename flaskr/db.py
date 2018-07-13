import psycopg2


""" This Module contains an important class of handling postgresql database
which is use by this web applications
"""


class Database:
    """ Class that contains basic functions to handle a postgresql database """
    
    def __init__ (self, db_name, db_user, db_password, host):
        
        try:
            connection = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=host)
            cursor = connection.cursor()
            self.cursor = cursor
            self.connection = connection
        except Exception as e:
            print("Unable to connect to the database")
            print(e)

    
    def insert(self, table, dictionary_of_columns_and_values):
        
        """ Function takes two arguments:
                table: str,
                dictionary_of_columns_and_values: dictionary
        Adds data to a database depending on dictionary's contents, and returns its ID on success.
        
        Example of usage: insert (table, {"name": "John Doe", "email": "example@example.com"})

        """ 

        table_columns = [*dictionary_of_columns_and_values] # Unpack dictionary keys into a list
        table_values = tuple(dictionary_of_columns_and_values.values())
        try:
            sql_string = "INSERT INTO {} ({}) VALUES ({}) RETURNING id".format(table, ", ".join(table_columns), ("%s,"*len(table_columns))[:-1])
            self.cursor.execute(sql_string, table_values)
            self.connection.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.connection.rollback()
            print(e)
        
    
    def update(self, table, dictionary_of_columns_and_values, condition):
        
        """Function takes three arguments:
                table: str,
                dictionary_of_columns_and_values: dictionary,
                condition: str
                
        Updates records of a given table, depending on dict contents, returns id of the changed column on success.
        
        Example of usage: update(table, {"root": "/usr/tests"}; "id=13")
        It updates the column "root" of the table "table" with the data "/usr/tests" where the id=13
        """
        
        table_columns = [*dictionary_of_columns_and_values]
        table_values = tuple(dictionary_of_columns_and_values.values())     
        try:
            sql_string = "UPDATE {} SET {} WHERE {} RETURNING id".format(table, " = %s, ".join(table_columns) + " = %s", condition)
            self.cursor.execute(sql_string, table_values)
            self.connection.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.connection.rollback()
            print(e)


    def select(self, table, list_of_columns, condition=""):

        """ Function takes three arguments:
                table: str,
                list_of_columns: list,
                condition: str

        Selects a list of columns from a table where a condition is met.

        Example of usage: select("users", ["username", "email"], "id=13")

        It returns an array of records where the conditions are met
        If no record with the conditions exist, it returns an empty list

        """

        try:
            if bool(condition.strip()) == False: #condition is empty
                sql_string = "SELECT {} FROM {}".format(", ".join(list_of_columns), table)
            else:
                sql_string = "SELECT {} FROM {} WHERE {}".format(", ".join(list_of_columns), table, condition)
            self.cursor.execute(sql_string)
            self.connection.commit()
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            self.connection.rollback()
            print(e)

    def execute(self, sql_query):
        try:
            self.cursor.execute(sql_query)
            self.connection.commit()
            return self.cursor
        except Exception as e:
            self.connection.rollback()
            print(e)

    def close(self):
        self.cursor.close()
        self.connection.close()
