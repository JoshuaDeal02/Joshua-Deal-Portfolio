SUMMARY:
This application is a HR employee management program aimed to store employee information,
fetch employee information, and perform more advanced querries (admin only). There is basic
administrative control so that general users cannot change the database schema. 

MAIN TECH USED: 
Python, MySQL, SQL, AWS RDS

TABLE SCHEMAS:
Employees: employee_ID (int), first_name(varchar(50)), last_name(varchar(50)), department_ID(int), manager_ID(int), job_ID(varchar(10)), phone_number(varchar(15)), hire_date(date), salary(decimal(10, 2))
Jobs: job_ID(int), job_name(varchar(50))
Departments: department_ID(int), department_name(varchar(50)), department_branch_location(varchar(50))

SECURITY NOTE: 
The database used in this application is NOT secure. 
This application is only meant to demonstrate competency in 
various skills and not for production. This application cannot
be used for other databases besides the example database that
is publically hosted on AWS. Known vulnerabilities include SQL 
injection attacks, password stored in plaintext, and brute force
prone login system (AKA broken authentication). Again this system is a proof of concept, it is
intentionally not a secure application as that is beyond this project's
scope. 