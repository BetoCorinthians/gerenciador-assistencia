from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Configuração da conexão com o SQL Server
server = '********'
database = 'assistencia'
username = 'Admin'
password = '***********'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def get_db_connection():
    conn = pyodbc.connect(connection_string)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_assistance', methods=['GET', 'POST'])
def add_assistance():
    if request.method == 'POST':
        description = request.form['description']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO assistencia (description) VALUES (?)", (description,))
        conn.commit()
        conn.close()
        return redirect(url_for('view_assistencia'))
    return render_template('add_assistancia.html')

@app.route('/view_assistencia')
def view_assistances():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, description FROM assistencia")
    assistances = cursor.fetchall()
    conn.close()
    return render_template('view_assistances.html', assistances=assistances)

@app.route('/add_plano', methods=['GET', 'POST'])
def add_plano():
    if request.method == 'POST':
        plan_name = request.form['plan_name']
        description = request.form['description']
        price = request.form['price']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO plano_assistencia (nome_plano, descricao, preco) VALUES (?, ?, ?)",
            (plan_name, description, price)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('view_plans'))
    return render_template('add_plano.html')

@app.route('/view_plano')
def view_plano():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome_plano, descricao, preco FROM plano_assistencia")
    plans = cursor.fetchall()
    conn.close()
    return render_template('view_plano.html', plans=plans)

@app.route('/add_benefit_plan', methods=['GET', 'POST'])
def add_benefit_plan():
    if request.method == 'POST':
        plan_name = request.form['plan_name']
        description = request.form['description']
        coverage = request.form['coverage']
        price = request.form['price']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO plano_beneficio (plan_name, description, coverage, price) VALUES (?, ?, ?, ?)",
            (plan_name, description, coverage, price)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('view_benefit_plans'))
    return render_template('add_benefit_plan.html')

@app.route('/view_benefit_plans')
def view_benefit_plans():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, plan_name, description, coverage, price FROM plano_beneficio")
    benefit_plans = cursor.fetchall()
    conn.close()
    return render_template('view_benefit_plans.html', benefit_plans=benefit_plans)


@app.route('/add_benefit', methods=['GET', 'POST'])
def add_benefit():
    if request.method == 'POST':
        benefit_name = request.form['benefit_name']
        description = request.form['description']
        eligibility_criteria = request.form['eligibility_criteria']
        amount = request.form['amount']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO beneficios (benefit_name, description, eligibility_criteria, amount) VALUES (?, ?, ?, ?)",
            (benefit_name, description, eligibility_criteria, amount)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('view_benefits'))
    return render_template('add_benefit.html')

@app.route('/view_benefits')
def view_benefits():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, benefit_name, description, eligibility_criteria, amount FROM beneficios")
    benefits = cursor.fetchall()
    conn.close()
    return render_template('view_benefits.html', benefits=benefits)

if __name__ == '__main__':
    app.run(debug=True)
