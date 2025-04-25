from flask import Flask, request, render_template
import requests
import psycopg2

app = Flask(__name__)

API_KEY = '8b99e00ece0d46e94d7a9cc8322b0901'

# RDS Connection config

DB_HOST = "weatherapp-db.cqvmq642qvn0.us-east-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "Chiranth1999"


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/weather')
def weather():
    city = request.args.get('city')
    if not city:
        return render_template("home.html", error="Please enter a city name.")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url).json()

    if res.get("cod") != 200:
        return render_template("home.html", error=f"City '{city}' not found.")

    temp = res["main"]["temp"]
    desc = res["weather"][0]["description"]

    # Insert into DB
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO weather_history (city, temperature, description) VALUES (%s, %s, %s)",
                (city, temp, desc))
    conn.commit()
    cur.close()
    conn.close()

    return render_template("result.html", city=city, temp=temp, desc=desc)


@app.route('/history')
def history():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT city, temperature, description, timestamp FROM weather_history ORDER BY timestamp DESC LIMIT 10")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("history.html", records=rows)

if __name__=='__main__':
        app.run(host='0.0.0.0',port=8080)