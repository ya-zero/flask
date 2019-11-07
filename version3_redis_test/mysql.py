import MySQLdb

#выполнить подключние к mysql
#return  cursor,db
def sql_connect():
    try:
      sql_connect = MySQLdb.connect(host='localhost',
                              user='root',
                              password='root',
                              charset='utf8mb4',
                              use_unicode=True,
                              db='switchdb')

      cursor=sql_connect.cursor()
      return [cursor,sql_connect]
    except MySQLdb.Error as error:
      return error


