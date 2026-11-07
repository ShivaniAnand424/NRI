from database import connect

conn = connect()
with conn.cursor() as cur:
    cur.execute("SELECT id, full_name, email, created_at FROM users")
    rows = cur.fetchall()
print(len(rows), "user(s) in Aiven:")
for row in rows:
    print(row)