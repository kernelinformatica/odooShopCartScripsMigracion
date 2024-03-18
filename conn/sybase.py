import pyodbc

serv = "coope-marga"
usr = "dba"
passwd = "sql"
db = "caja1"
prt = ""
conn = pyodbc.connect('DSN='+serv+';Database='+db+';UID='+usr+';PWD='+passwd+'', autocommit=True)
conn.setdecoding(pyodbc.SQL_CHAR, encoding='latin1')
conn.setencoding('latin1')
#cursor = conn.cursor()
#cursor.execute("SELECT * FROM fac_articulos")
#for row in cursor.fetchall():
 #   print (row)