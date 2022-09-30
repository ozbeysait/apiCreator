import pyodbc

def main():
    conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=DESKTOP-AK2LDL5;"
        "Database=HR;"
        "UID=sa;"
        "PWD=1234;"
    )

    conn = pyodbc.connect(conn_str)


    cursor1 = conn.cursor()
    cursor1.execute('select * from INFORMATION_SCHEMA.TABLES')
    for i in cursor1:
        print(i)
    conn.close()

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'dependents'")
    conn.close()


if __name__ == '__main__':
    main()