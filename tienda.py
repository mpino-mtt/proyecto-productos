from flask import Flask, render_template
import pymysql

app = Flask(__name__)

# Conexión a RDS
connection = pymysql.connect(
    host='database-practica-rds.cbwk86wqieiu.us-east-1.rds.amazonaws.com',
    user='admin',
    password='Admin.1301',
    database='base_de_datos_prueba'
)

@app.route('/')
def productos():
    with connection.cursor() as cursor:
        cursor.execute("SELECT nombre, precio, cantidad from productos")
        resultados = cursor.fetchall()
        return render_template('/productos.html', productos=resultados)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
