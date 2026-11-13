"""Shows your Aiven tables and saves each one as a CSV file in the 'exports' folder.
Run:  python ExportData.py
"""
import csv
from datetime import datetime
from pathlib import Path

from database import connect

OUT = Path(__file__).resolve().parent / "exports"

QUERIES = {
    "users": "SELECT id, full_name, email, phone, country, created_at FROM users ORDER BY id",
    "enquiries": "SELECT * FROM enquiries ORDER BY id",
    # service enquiries joined with the customer's details so the file is readable
    "service_enquiries": """
        SELECT se.id, u.full_name, u.email, u.phone, u.country,
               se.service_slug, se.responses_json, se.created_at
        FROM service_enquiries se
        LEFT JOIN users u ON u.id = se.user_id
        ORDER BY se.id
    """,
}


def main():
    OUT.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    conn = connect()
    try:
        with conn.cursor() as cur:
            for table, sql in QUERIES.items():
                cur.execute(sql)
                rows = cur.fetchall()
                print(f"\n{table}: {len(rows)} row(s)")
                for row in rows[:5]:
                    print("  ", row)
                if rows:
                    path = OUT / f"{table}_{stamp}.csv"
                    with open(path, "w", newline="", encoding="utf-8-sig") as f:
                        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                        writer.writeheader()
                        writer.writerows(rows)
                    print("   saved ->", path)
    finally:
        conn.close()


if __name__ == "__main__":
    main()