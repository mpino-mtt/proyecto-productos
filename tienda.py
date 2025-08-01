from flask import Flask, render_template
import pymysql
import boto3

app = Flask(__name__)

# Conexión a RDS
connection = pymysql.connect(
    host='database-practica-rds.cbwk86wqieiu.us-east-1.rds.amazonaws.com',
    user='admin',
    password='Admin.1301',
    database='base_de_datos_prueba'
)

# Conexión a S3
s3_bucket = 'bucket-app-web-s3-practica'
s3 = boto3.client('s3', region_name='us-east-1')

@app.route('/')
def productos():
    with connection.cursor() as cursor:
        cursor.execute("SELECT nombre, precio, cantidad FROM productos")
        resultados = cursor.fetchall()

        productos_con_imagen = []
        for nombre, precio, cantidad in resultados:
            
            nombre_archivo = f"{nombre.replace(' ', '_').lower()}.jpg"

            image_url = f"https://{s3_bucket}.s3.us-east-1.amazonaws.com/{nombre_archivo}"

            productos_con_imagen.append({
                'nombre': nombre,
                'precio': precio,
                'cantidad': cantidad,
                'imagen': image_url
            })

        return render_template('productos.html', productos=productos_con_imagen)

@app.route('/health')    
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
