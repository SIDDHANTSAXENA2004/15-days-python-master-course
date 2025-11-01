import psycopg2

try:
    conn=psycopg2.connect(
        host="localhost",
        database="comapany_db",
        user="postgres",
        password="mummy"
    )
    print("connection successful...")
    cur=conn.cursor()

    cur.execute('''
                CREATE TABLE if not exists departments(
                 dept_id SERIAL PRIMARY KEY,
                 dept_name TEXT NOT NULL);
                ''')
    
    cur.execute('''
         CREATE TABLE if not exists employees(
             emp_id SERIAL PRIMARY KEY,
             emp_name TEXT NOT NULL ,
             salary int,
             age int,
             dept_id INT REFERENCES departments(dept_id));
            ''')
    
    cur.execute(
        '''
     INSERT INTO departments (dept_name) values('HR'),('IT'),('FINANCE');
    '''
    )
    conn.commit()
    cur.execute("SELECT * from departments")
    rows=cur.fetchall()
    for r in rows:
        print(r)
    name=input("enter name")
    salary=int(input("enter salary"))
    dept_id=int(input("enter dept_id"))
    age=int(input("enter age"))
    cur.execute('''
        INSERT INTO employees (emp_name ,salary,dept_id,age) VALUES
           (%s,%s,%s,%s);
            ''',(name,salary,dept_id,age))
    
    conn.commit()

    cur.execute("SELECT * from employees")
    rows=cur.fetchall()
    for r in rows:
        print(r)
    
    
    
except  Exception as e:
    print("error: ",e)
finally:
    cur.close()
    conn.close()