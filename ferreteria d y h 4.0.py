from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'ferreteria_dyh_secret_key'

# Base de datos completa de productos
PRODUCTOS = {
    # Material de Construcción
    'c1': {"id": "c1", "nombre": "Ladrillo Rojo Tradicional", "descripcion": "Ladrillo rojo de arcilla cocida, ideal para muros y fachadas resistentes.", "precio": "$4.50 - $6.00 MXN", "categoria": "construccion"},
    'c2': {"id": "c2", "nombre": "Cemento Gris (Saco 50 kg)", "descripcion": "Cemento Portland ordinario de alta resistencia para todo tipo de obra negra.", "precio": "$240.00 - $270.00 MXN", "categoria": "construccion"},
    'c3': {"id": "c3", "nombre": "Cal Hidratada (Saco 25 kg)", "descripcion": "Cal de excelente calidad para mezclas de revoque, aplanados y albañilería.", "precio": "$75.00 - $90.00 MXN", "categoria": "construccion"},
    'c4': {"id": "c4", "nombre": "Mortero / Cemento de Albañilería (50 kg)", "descripcion": "Mortero optimizado para pega de ladrillos, bloques y trabajos de mampostería.", "precio": "$210.00 - $235.00 MXN", "categoria": "construccion"},
    'c5': {"id": "c5", "nombre": "Impercel / Cemento Impermeable 50 kg", "descripcion": "Cemento con aditivo impermeabilizante integrado para cimientos y zonas húmedas.", "precio": "$280.00 - $310.00 MXN", "categoria": "construccion"},
    'c6': {"id": "c6", "nombre": "Pegazulejo (Saco 20 kg)", "descripcion": "Adhesivo en polvo base cemento para colocación de pisos cerámicos y azulejos.", "precio": "$130.00 - $160.00 MXN", "categoria": "construccion"},
    'c7': {"id": "c7", "nombre": "Ladrillo Loseta / Azotea", "descripcion": "Pieza cerámica delgada para aislamiento térmico e impermeabilización de azoteas.", "precio": "$12.00 - $16.00 MXN", "categoria": "construccion"},
    'c8': {"id": "c8", "nombre": "Block de Cemento (12x20x40 cm)", "descripcion": "Block hueco de concreto vibrado de alta durabilidad para muros divisorios o carga.", "precio": "$15.00 - $19.00 MXN", "categoria": "construccion"},
    'c9': {"id": "c9", "nombre": "Adobón", "descripcion": "Pieza de barro de mayor tamaño para construcciones rústicas y tradicionales.", "precio": "$18.00 - $24.00 MXN", "categoria": "construccion"},

    # Aceros
    'ac1': {"id": "ac1", "nombre": "Varilla Corrugada (3/8\", 1/2\", 3/4\")", "descripcion": "Varilla de acero grado 42 para refuerzo estructural en losas, columnas y trabes.", "precio": "$140.00 - $320.00 MXN", "categoria": "aceros"},
    'ac2': {"id": "ac2", "nombre": "Perfil PTR (1\", 2\", 3\")", "descripcion": "Perfil tubular rectangular de acero al carbón para estructuras metálicas y herrería.", "precio": "$280.00 - $750.00 MXN", "categoria": "aceros"},
    'ac3': {"id": "ac3", "nombre": "Perfil Tubular (1\", 2\")", "descripcion": "Tubo industrial de acero redondo o cuadrado para soportes y barandales.", "precio": "$220.00 - $540.00 MXN", "categoria": "aceros"},
    'ac4': {"id": "ac4", "nombre": "Lámina Lisa (Calibre 20 a 28)", "descripcion": "Lámina de acero galvanizado para cubiertas, charolas y trabajos de hojalatería.", "precio": "$350.00 - $900.00 MXN", "categoria": "aceros"},
    'ac5': {"id": "ac5", "nombre": "Malla Ciclónica (Rollo)", "descripcion": "Malla de alambre galvanizado entrelazado para delimitación perimetral de terrenos.", "precio": "$1,200.00 - $2,500.00 MXN", "categoria": "aceros"},

    # Pinturas y Solventes
    'p1': {"id": "p1", "nombre": "Pintura Vinílica Base Agua (Cubeta 19L)", "descripcion": "Pintura vinil-acrílica de alto rendimiento para interiores y exteriores.", "precio": "$850.00 - $1,300.00 MXN", "categoria": "pinturas"},
    'p2': {"id": "p2", "nombre": "Esmalte Alquílico / Sintético (Galón 4L)", "descripcion": "Pintura de brillante acabado protector anticorrosivo para metales y madera.", "precio": "$320.00 - $480.00 MXN", "categoria": "pinturas"},
    'p3': {"id": "p3", "nombre": "Impermeabilizante Acrílico (Cubeta 19L)", "descripcion": "Impermeabilizante fibratado con duración de 3 a 5 años para techos de concreto.", "precio": "$950.00 - $1,600.00 MXN", "categoria": "pinturas"},
    'p4': {"id": "p4", "nombre": "Thinner Estándar / Solvente (Litro / Galón)", "descripcion": "Disolvente de uso general para limpieza de brochas, dilución de esmaltes y primarios.", "precio": "$45.00 - $180.00 MXN", "categoria": "pinturas"},
    'p5': {"id": "p5", "nombre": "Pintura en Aerosol (Varios Colores)", "descripcion": "Pintura acrílica en spray de secado rápido para reparaciones y retoques rápidos.", "precio": "$65.00 - $90.00 MXN", "categoria": "pinturas"},

    # Tornillería y Clavos
    't1': {"id": "t1", "nombre": "Tornillos de Alta Precisión (Grado 5 y 8)", "descripcion": "Tornillería hexagonal y cuerda fina de alta resistencia mecánica para maquinaria.", "precio": "$2.00 - $25.00 MXN c/u", "categoria": "tornilleria"},
    't2': {"id": "t2", "nombre": "Rondanas Planas y de Presión", "descripcion": "Juego de rondanas de acero galvanizado para distribución uniforme de carga.", "precio": "$0.50 - $5.00 MXN c/u", "categoria": "tornilleria"},
    't3': {"id": "t3", "nombre": "Clavos para Concreto (Medidas Varias)", "descripcion": "Clavos de acero templado con estrías para fijación directa en muros de concreto.", "precio": "$45.00 - $65.00 kg", "categoria": "tornilleria"},
    't4': {"id": "t4", "nombre": "Clavos para Madera (Con Cabeza y Sin Cabeza)", "descripcion": "Clavos de alambre pulido para carpintería, tarimas y encofrados.", "precio": "$35.00 - $50.00 kg", "categoria": "tornilleria"},

    # Cerámica y Pisos
    'ce1': {"id": "ce1", "nombre": "Vitropisos y Porcelánicos (Caja m²)", "descripcion": "Losetas cerámicas y porcelanatos rectificados de alta dureza para pisos y muros.", "precio": "$180.00 - $380.00 m²", "categoria": "ceramica"},
    'ce2': {"id": "ce2", "nombre": "Sanitarios de Una y Dos Piezas", "descripcion": "Inodoros ecológicos ahorradores de agua con sistema de descarga dual.", "precio": "$1,800.00 - $3,500.00 MXN", "categoria": "ceramica"},
    'ce3': {"id": "ce3", "nombre": "Lavamanos y Muebles de Baño", "descripcion": "Lavabos de sobreponer, pedestales y gabinetes modernos con diseño compacto.", "precio": "$900.00 - $2,800.00 MXN", "categoria": "ceramica"},
    'ce4': {"id": "ce4", "nombre": "Accesorios de Baño (Juegos Completos)", "descripcion": "Juegos de accesorios cromados incluyendo jabonera, toallero y portarrollos.", "precio": "$350.00 - $950.00 MXN", "categoria": "ceramica"},

    # Tuberías y Conexiones
    'tu1': {"id": "tu1", "nombre": "Tubería Medidas Varias (1/2\" a 1 1/2\")", "descripcion": "Tubos para conducción de agua potable, gas y drenaje de alta resistencia.", "precio": "$60.00 - $350.00 tramo", "categoria": "tuberias"},
    'tu2': {"id": "tu2", "nombre": "Tubo de Cobre (Tipo M y L)", "descripcion": "Tubería rígida y flexible de cobre para instalaciones hidrosanitarias y gas.", "precio": "$150.00 - $650.00 tramo", "categoria": "tuberias"},
    'tu3': {"id": "tu3", "nombre": "TuboPlus / Thermofusión", "descripcion": "Sistema de polipropileno copolímero aleatorio para conducción de agua sin fugas.", "precio": "$90.00 - $420.00 tramo", "categoria": "tuberias"},
    'tu4': {"id": "tu4", "nombre": "Tubo de Acero Galvanizado", "descripcion": "Tubería roscada de acero galvanizado para instalaciones industriales o alta presión.", "precio": "$280.00 - $950.00 tramo", "categoria": "tuberias"},

    # Herramientas y Accesorios
    'h1': {"id": "h1", "nombre": "Herramientas de Mano (Martillos, Llaves, Pinzas)", "descripcion": "Herramientas ergonómicas de acero forjado para uso profesional y doméstico.", "precio": "$80.00 - $450.00 MXN", "categoria": "accesorios"},
    'h2': {"id": "h2", "nombre": "Equipo de Protección (Cascos, Lentes, Guantes)", "descripcion": "Equipo de seguridad industrial certificado para protección en obra y talleres.", "precio": "$40.00 - $250.00 MXN", "categoria": "accesorios"},
    'h3': {"id": "h3", "nombre": "Soldadoras Inversoras y Electrodos", "descripcion": "Máquinas de soldar portátiles de tecnología inverter y consumibles especializados.", "precio": "$120.00 - $3,800.00 MXN", "categoria": "accesorios"},
    'h4': {"id": "h4", "nombre": "Flexómetros y Niveles Láser", "descripcion": "Instrumentos de medición de alta precisión con cinta reforzada y plomada láser.", "precio": "$75.00 - $1,200.00 MXN", "categoria": "accesorios"}
}

COLORES_PINTURA = [
    "Blanco Ostras", "Blanco Humo", "Marfil Claro", "Gris Perla", "Gris Acero",
    "Gris Oscuro", "Arena del Desierto", "Beige Suave", "Azul Cielo", "Azul Naval",
    "Azul Océano", "Verde Limón", "Verde Musgo", "Verde Jade", "Amarillo Canario",
    "Amarillo Trigo", "Naranja Crepúsculo", "Rojo Terracota", "Rojo Oxido", "Vino Tinto",
    "Rosa Pastel", "Violeta Real", "Café Tabaco", "Chocolate Intenso", "Negro Profundo"
]

@app.before_request
def inicializar_sesion():
    if 'lista_compras' not in session:
        session['lista_compras'] = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/construccion')
def construccion():
    mats = [p for p in PRODUCTOS.values() if p['categoria'] == 'construccion']
    return render_template('construccion.html', materiales=mats)

@app.route('/aceros')
def aceros():
    mats = [p for p in PRODUCTOS.values() if p['categoria'] == 'aceros']
    return render_template('aceros.html', materiales=mats)

@app.route('/pinturas')
def pinturas():
    mats = [p for p in PRODUCTOS.values() if p['categoria'] == 'pinturas']
    return render_template('pinturas.html', materiales=mats, colores=COLORES_PINTURA)

@app.route('/tornilleria')
def tornilleria():
    mats = [p for p in PRODUCTOS.values() if p['categoria'] == 'tornilleria']
    return render_template('tornilleria.html', materiales=mats)

@app.route('/ceramica')
def ceramica():
    mats = [p for p in PRODUCTOS.values() if p['categoria'] == 'ceramica']
    return render_template('ceramica.html', materiales=mats)

@app.route('/tuberias')
def tuberias():
    mats = [p for p in PRODUCTOS.values() if p['categoria'] == 'tuberias']
    return render_template('tuberias.html', materiales=mats)

@app.route('/accesorios')
def accesorios():
    mats = [p for p in PRODUCTOS.values() if p['categoria'] == 'accesorios']
    return render_template('accesorios.html', materiales=mats)

@app.route('/agregar/<prod_id>')
def agregar(prod_id):
    if prod_id in PRODUCTOS:
        prod = PRODUCTOS[prod_id]
        lista = session.get('lista_compras', [])
        if prod not in lista:
            lista.append(prod)
            session['lista_compras'] = lista
    return redirect(request.referrer or url_for('index'))

@app.route('/quitar_item/<int:index>')
def quitar_item(index):
    lista = session.get('lista_compras', [])
    if 0 <= index < len(lista):
        lista.pop(index)
        session['lista_compras'] = lista
    return redirect(request.referrer or url_for('index'))

@app.route('/agregar_producto_nuevo/<categoria>', methods=['POST'])
def agregar_producto_nuevo(categoria):
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    
    if nombre and descripcion and precio:
        nuevo_id = f"custom_{len(PRODUCTOS) + 1}"
        PRODUCTOS[nuevo_id] = {
            "id": nuevo_id,
            "nombre": nombre,
            "descripcion": descripcion,
            "precio": f"${precio} MXN",
            "categoria": categoria
        }
    return redirect(url_for(categoria))

@app.route('/eliminar_producto/<prod_id>/<categoria>')
def eliminar_producto(prod_id, categoria):
    if prod_id in PRODUCTOS:
        del PRODUCTOS[prod_id]
    return redirect(url_for(categoria))

@app.route('/enviar_pedido')
def enviar_pedido():
    session['lista_compras'] = []
    return render_template('pedido_enviado.html')

if __name__ == '__main__':
    app.run(debug=True)