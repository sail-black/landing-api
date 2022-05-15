python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install psycopg2
flask db upgrade
flask fake users 10
flask fake posts 100
flask run