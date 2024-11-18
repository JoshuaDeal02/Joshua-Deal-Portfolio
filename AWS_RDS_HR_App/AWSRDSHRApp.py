import mysql.connector as mc

class Database:
    
    def __init__(self):
        self.admin_block = False
        self.admin_password = 'password'
        self.db = self.connect_db()
        self.admin = self.admin_login()

    def admin_login(self):
        if not self.admin_block:
            attempts = 3
            entry = input("Are you an admin? \n(y/n): ")
            while entry == 'y':
                entry = input("Enter the admin password: ")
                if entry == self.admin_password:
                    self.admin = True
                    print("\nLogged in as an admin\n")
                    return True
                else:
                    attempts -= 1
                    if attempts <= 0:
                        self.admin_block = True
                        print("No tried remaining, admin login locked")
                        return False
                    entry = input(f"Incorrect password, {attempts} attemps remaining, try again? \n(y/n): ")
                    if entry != 'y' and attempts < 3:
                        self.admin_block = True
                        print("Admin login locked\n")
        
        return False
        
    def check_admin(self):
        if self.admin != True:
            print("You are not logged in as an admin")
            return self.admin_login()

    def connect_db(self):
        try:
            db = mc.connect(
                host="employeedb.cfgoe2ycsrr3.us-east-2.rds.amazonaws.com",
                user="admin",
                password=self.admin_password
                )
            self.db = db
            self.cursor = self.db.cursor()
            self.cursor.execute("USE EmployeeDB")
            self.set_up_db()
            db.database = 'EmployeeDB'

        except mc.Error as e:
            print(f"Error {e} ")
            exit()

        return db
    
    def set_up_db(self):
        try:
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables 
                WHERE table_schema = 'EmployeeDB' 
                AND table_name = 'Employees'
            """)
            result = self.cursor.fetchone()
            

            if result[0] == 0:  
                print("Database is not set up, creating now")
                self.create_tables()
                self.db.commit()
                
            else:
                print("The database is already set up")
        
        except mc.Error as e:
            print(f"Error while checking or creating database: {e}")
            exit()
    
    def print_menu(self):
        print("\nMENU\n1 - Enter Employee Record\n2 - Update Employee Record\n3 - Delete Employee Record\n4 - Fetch Employee Record\n5 - Fetch Entire Table\n6 - Manual Query (Admin Only)\n7 - Purge Database Records (Admin Only)\n8 - Restart Entire Database (Admin Only)\n0 - Close Application")
        
    def core_loop(self):
        entry = 1

        while entry != 0:
            self.print_menu()
            entry = int(input("\n\nEntry: "))
            match entry:
                case 1:
                    self.enter_employee_record()
                case 2:
                    self.update_employee_record()
                case 3:
                    self.delete_employee_record()
                case 4:
                    self.fetch_employee_record()
                case 5:
                    self.fetch_entire_table()
                case 6:
                    self.manual_query()
                case 7:
                    self.purge_records()
                case 8:
                    self.restart_database()
                case 0:
                    self.close_app()
                case _:
                    print("Entry must be 0-8")

    def fetch_entire_table(self):
        try:
            table_name = input("Enter the table name to be fetched: ")
            self.cursor.execute(f"""
                SELECT * FROM {table_name}
            """)
            self.print_results()
        except mc.Error as e:
            print(f"Error {e} when retrieving data from {table_name}")

    def create_tables(self):
        self.cursor.execute("""
                CREATE TABLE Departments (
                department_id INT PRIMARY KEY AUTO_INCREMENT,
                department_name VARCHAR(50) UNIQUE NOT NULL,
                department_branch_location VARCHAR(50)
                );
            """)
        self.cursor.execute("""
                CREATE TABLE Jobs (
                job_id INT PRIMARY KEY AUTO_INCREMENT,
                job_name VARCHAR(50) UNIQUE NOT NULL
                );
            """)
        self.cursor.execute("""
                CREATE TABLE Employees (
                employee_id INT PRIMARY KEY AUTO_INCREMENT,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone_number VARCHAR(15),
                job_id VARCHAR(10) NOT NULL,
                hire_date DATE NOT NULL,
                salary DECIMAL(10, 2) DEFAULT 0.00,
                department_id INT,
                manager_id INT
                );
            """)
        
    def manual_query(self):
        if self.check_admin() == False:
            return
        print("\nWARNING: \nDropping core tables (Employees, Departments, Jobs) from the database\nwill cause performance issues until a full database restart is performed\n")
        query = input("Enter your query in proper SQL syntax:\n")
        safe_query = f"""{query}"""
        try:
            self.cursor.execute(safe_query)
            self.print_results()
        except mc.Error as e:
            print(f"An error arose when executing your sql code: {e}")
    
    def print_results(self):
        print("\n")
        try:
            result = self.cursor.fetchall()
            if result:
                # Get the column names and calculate the maximum width for each column
                column_names = [desc[0] for desc in self.cursor.description]
                column_widths = [len(name) for name in column_names]

                # Find the maximum width for each column (including data in the rows)
                for row in result:
                    for i, item in enumerate(row):
                        column_widths[i] = max(column_widths[i], len(str(item)))

                # Print column names with padding for alignment
                print(" | ".join(name.ljust(width) for name, width in zip(column_names, column_widths)))

                # Print separator line (converted sum of widths to string)
                print("-" * (sum(column_widths) + (len(column_widths) - 1) * 3))

                # Print each row with proper column width formatting
                for row in result:
                    print(" | ".join(str(item).ljust(width) for item, width in zip(row, column_widths)))
            else:
                print(f"No output to display")
        except mc.Error as e:
            print(f"Error {e} when retrieving data")

    def close_app(self):
        entry = input("Would you like to commit the changes made? \n(y/n): ")
        while entry != 'y' and entry != 'n':
            entry = input("Entry must be either 'y' or 'n': ")
        if entry == 'y':
            self.db.commit()
        exit()
    
    def purge_records(self):
        if self.check_admin() == False:
            return
        entry = input("WARNING: Entering 'y' will purge all records in the database. \nContinue (y/n): ")
        if entry != 'y':
            return
        try:
            tables = self.get_table_names()
            for table in tables:
                table_name = table[0]
                self.cursor.execute(f"""
                DELETE FROM {table_name}
                """)
                print(f"{table_name} successfully purged")
        except:
            print("There was an error when purging the database")
        
    def get_table_names(self):
        try:
            self.cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'EmployeeDB'
            """)
            result = self.cursor.fetchall() #this information should be cached to increase efficiency if the database is large
            if result:
                return result
            else:
                print("No tables were found")
        except mc.Error as e:
            print(f"There was an error when fetching table names: {e}")
        return 0
    
    def get_column_names(self):
        try:
            self.cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'EmployeeDB' AND table_name = 'Employees'
            """)
            result = self.cursor.fetchall() #this information should be cached to increase efficiency if the database is large
            if result:
                return [column[0] for column in result]
            else:
                print("No columns were found")
        except mc.Error as e:
            print(f"There was an error when fetching column names: {e}")
        return 0

    def fetch_employee_record(self):
        id = input("Enter the ID of the employee record: ")
        self.fetch_employee_record_helper(id)

    def enter_employee_record(self):
        try:
            print("Employee Information Collection: \n")
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            email = input("Email Address: ")
            phone_number = input("Phone Number: ")
            job_id = int(input("Job ID: "))
            hire_date = input("Hire Date (YYYY-MM-DD)")
            salary = input("Salary: ")
            department_id = int(input("Deptartment ID: "))
            manager_id = int(input("Manager ID: "))
        except:
            print("There was an error when collecting information. Check table schema for proper data types")
            return
        try:
            query = ("""
            INSERT INTO Employees (first_name, last_name, email, phone_number, job_id, hire_date, salary, department_id, manager_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """)
            self.cursor.execute(query, (first_name, last_name, email, phone_number, job_id, hire_date, salary, department_id, manager_id))

            query = ("""
            SELECT employee_id FROM Employees WHERE first_name=%s AND last_name=%s AND email=%s AND phone_number=%s
            """)
            self.cursor.execute(query, (first_name, last_name, email, phone_number))
            employee_id = self.cursor.fetchone()
            print(f"{first_name} {last_name} successfully entered, Employee ID: {employee_id[0]}")
        except mc.Error as e:
            print(f"There was an error entering the new employee: {e}")

    def delete_employee_record(self):
        id = int(input("Enter the Employee ID of the record to be deleted: "))
        entry = input("Enter 'delete' to delete this record: ")
        if entry == 'delete':
            try:
                self.cursor.execute(f"""
                DELETE FROM Employees WHERE employee_id={id}
                """)
                print(f"Employee {id} deleted")
            except mc.Error() as e:
                print(f"There was an error when deleting the employee record: {e}")

    def update_employee_record(self):
        id = input("Enter the employee ID for the record to be altered: ")
        print("Is this the record you would like to alter?")
        self.fetch_employee_record_helper(id)
        entry = input("(y/n): ")
        if entry == 'y':
            print("Which field would you like to change? (note that employee ID cannot be changed)")
            columns = self.get_column_names()
            for column in columns:
                print(column)
            entry = input("Entry: ")
            while entry not in columns and entry != 'employee_id':
                entry = input("The entered columm could not be found, check the list of columns or enter '0' to quit")
                if entry == '0':
                    return
            value = input(f"Enter the new value for {entry}: ")
            try:
                query = (f"""
                UPDATE Employees SET {entry} = %s WHERE employee_id=%s
                """)
                self.cursor.execute(query, (value, id))
                print(f"{entry} has been set to {value} for employee {id}")
            except mc.Error() as e:
                print(f"There was an error when updating the column: {e}")

    def restart_database(self):
        if self.check_admin() == False:
            return
        entry = input("WARNING: Entering 'y' will completely restart the database the database. \nContinue (y/n): ")
        if entry != 'y':
            return
        try:
            tables = self.get_table_names()
            for table in tables:
                table_name = table[0]
                self.cursor.execute(f"""
                DROP TABLE {table_name};
                """)
            print("Database deleted, setting up tables...")
            self.create_tables()

        except:
            print("There was an error when purging the database")

    def fetch_employee_record_helper(self, entry):
        try:
            self.cursor.execute(f"""
            SELECT * FROM Employees WHERE employee_id={entry}
            """)
            self.print_results()
        except mc.Error() as e:
            print(f"No record could be found with employee ID {entry}. Error: {e}") #This code should not be reached (backup failsafe)



database = Database()
database.core_loop()

