import psycopg2

# Conectar a la base de datos
try:
    conn = psycopg2.connect(
        dbname="postgres",  # base de datos nombre
        user="postgres",    # usuario
        password="dunklow5566",  # contraseña
        host="localhost",
        port="5432"  # puerto
    )
    print("Conexión exitosa a la base de datos.")
except Exception as e:
    print("Error al conectar a la base de datos:", e)
    exit()

# Cursor para ejecutar consultas
cur = conn.cursor()

# Datos a insertar
products = [
    {"id": 1, "name": "G-Mouse", "price": "25", "image": "/images/mouse.jpg", "description": "Mouse ergonómico y preciso para largas horas de uso."},
    {"id": 2, "name": "Gaming Key", "price": "50", "image": "/images/keyboard.jpg", "description": "Teclado mecánico con retroiluminación para jugadores."},
    {"id": 3, "name": "Monitor 24\"", "price": "150", "image": "/images/monitor.jpg", "description": "Pantalla Full HD de 24 pulgadas con colores vibrantes."},
    {"id": 4, "name": "USB-C Hub", "price": "30", "image": "/images/hub.jpg", "description": "Hub USB-C con múltiples puertos para expandir tu conectividad."},
    {"id": 5, "name": "External SSD", "price": "120", "image": "/images/ssd.jpg", "description": "Almacenamiento rápido y portátil con 500GB de capacidad."},
    {"id": 6, "name": "Smart Stand", "price": "15", "image": "/images/stand.jpg", "description": "Soporte ajustable para mantener tu dispositivo a la altura perfecta."},
    {"id": 7, "name": "Speaker", "price": "45", "image": "/images/speaker.jpg", "description": "Altavoz portátil con sonido envolvente y batería de larga duración."},
    {"id": 8, "name": "Webcam", "price": "80", "image": "/images/webcam.jpg", "description": "Cámara web HD para videollamadas claras y nítidas."},
    {"id": 9, "name": "Charger", "price": "35", "image": "/images/charger.jpg", "description": "Cargador rápido para dispositivos electrónicos."},
    {"id": 10, "name": "Headset", "price": "60", "image": "/images/headset.jpg", "description": "Auriculares con cancelación de ruido y sonido premium."},
    {"id": 11, "name": "Tablet", "price": "200", "image": "/images/tablet.jpg", "description": "Tableta de alto rendimiento con pantalla táctil de 10 pulgadas."},
    {"id": 12, "name": "Smartwatch", "price": "180", "image": "/images/watch.jpg", "description": "Reloj inteligente con seguimiento de actividad y notificaciones."}
]

# Insertar datos en la tabla products
try:
    for product in products:
        cur.execute("""
            INSERT INTO public.products (id, name, description, price, image)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (product['id'], product['name'], product['description'], product['price'], product['image']))
    conn.commit()
    print("Datos insertados correctamente en la tabla 'products'.")
except Exception as e:
    print("Error al insertar datos:", e)
    conn.rollback()

# Cerrar cursor y conexión
cur.close()
conn.close()
