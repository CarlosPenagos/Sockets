import mysql.connector
host_a = '34.192.197.58'
user_a = 'carlos'
password_a = 'Ticketsoft2020*'
database_a ='ticketsoft_main'
port_a = 3306

import mysql.connector

def connect_to_database(host, user, password, database, port):
    try:
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database, port=port)
        print("Conexión exitosa a la base de datos")
        return connection
    except Exception as e:
        print("Error al conectarse a la base de datos:", e)
        return None

def fetch_dispensadores(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, codigo_estacion, posicion_dispensador, mac_address, actu_user, actu_vehicle, actu_parameters, actu_data_server, actu_puerto_serial, actu_products, actu_ticket, actu_ventas, actu_resoluciones, actu_db, actu_firmware, actu_descuentos, actu_formas_pago, actu_notification, actu_referencias, ultima_conexion FROM ticketsoft_main.dispensadores")
        dispensadores = cursor.fetchall()
        return dispensadores
    except Exception as e:
        print("Error al recuperar datos de la tabla dispensadores:", e)
        return []

def get_dispensadores():
    connection = connect_to_database(host_a, user_a, password_a, database_a, port_a)
    if connection:
        dispensadores = fetch_dispensadores(connection)
        connection.close()
        return dispensadores
    else:
        return []

