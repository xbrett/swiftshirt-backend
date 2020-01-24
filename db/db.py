import psycopg2

class Db:
  conn = None

  def __init__(self, pg_config):
    self.conn = psycopg2.connect(
      host = pg_config["host"], 
      port = pg_config["port"], 
      database = pg_config["database"], 
      user = pg_config["user"], 
      password = pg_config["password"])

  
  def get_workout(self, id):
    cur = self.conn.cursor()

    # A sample query of all data from the "vendors" table in the "suppliers" database
    cur.execute("""SELECT * FROM workouts WHERE id = {}""", id)
    query_results = cur.fetchall()

    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    conn.close()

    return query_results