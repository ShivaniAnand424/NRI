"""Checks your project setup. Run it with:  python check_setup.py"""
import importlib
import os
from pathlib import Path

root = Path(__file__).resolve().parent
problems = 0


def ok(message):
    print("  OK       ", message)


def bad(message):
    global problems
    problems += 1
    print("  PROBLEM  ", message)


print("Project folder:", root)
print()

# 1. The .env file
env_file = root / ".env"
if env_file.exists():
    ok(".env file found")
else:
    bad(".env file NOT found in the project folder (next to app.py)")
    if (root / ".env.txt").exists():
        bad("There is a file named .env.txt. Rename it to .env (remove the .txt)")

# 2. Packages
for module, label in (
    ("flask", "Flask"),
    ("pymysql", "PyMySQL"),
    ("cryptography", "cryptography"),
    ("dotenv", "python-dotenv"),
):
    try:
        importlib.import_module(module)
        ok(f"{label} is installed")
    except ImportError:
        bad(f"{label} is not installed. Activate .venv, then run: pip install -r requirements.txt")

# 3. Settings inside .env
try:
    from dotenv import load_dotenv

    load_dotenv(env_file)
except ImportError:
    pass

for key in ("DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME", "DB_SSL_CA", "SECRET_KEY"):
    if os.environ.get(key):
        ok(f"{key} is set")
    else:
        bad(f"{key} is missing or empty in .env")

# 4. Certificate file
ca_setting = os.environ.get("DB_SSL_CA")
if ca_setting:
    ca_path = Path(ca_setting)
    if not ca_path.is_absolute():
        ca_path = root / ca_path
    if ca_path.exists():
        ok(f"Certificate file found: {ca_path.name}")
    else:
        bad(f"Certificate file not found at {ca_path}")

# 5. .gitignore protects the secrets
gitignore = root / ".gitignore"
lines = []
if gitignore.exists():
    lines = [line.strip() for line in gitignore.read_text(encoding="utf-8", errors="ignore").splitlines()]
if ".env" in lines:
    ok(".gitignore lists .env, so it will not be uploaded to GitHub")
else:
    bad("Add a line with  .env  to .gitignore so your passwords are not uploaded")

# 6. Real connection test (only if everything above passed)
print()
if problems == 0:
    try:
        from database import connect

        connection = connect()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION() AS version")
                version = cursor.fetchone()["version"]
        ok(f"Connected to MySQL (version {version})")
    except Exception as error:
        bad(f"Could not connect to MySQL: {error}")
else:
    print("  Fix the problems above first, then run this again.")

print()
print("All good." if problems == 0 else f"{problems} problem(s) found.")