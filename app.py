from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ferreteria_dyh_secret_key'

# Base de datos unificada de productos con imágenes PNG organizadas por subcarpeta
PRODUCTOS = {
    # 🧱 MATERIAL DE CONSTRUCCIÓN
    'c1': {
        "id": "c1", "codigo": "101", "nombre": "Ladrillo Rojo Tradicional", "descripcion": "Ladrillo rojo de arcilla cocida, ideal para muros y fachadas resistentes.", "categoria": "construccion",
        "imagen": "images/construccion/c1.png",
        "marcas": [
            {"nombre": "Artesanal Local", "precio_num": 4.50},
            {"nombre": "Tabicón Mexicano", "precio_num": 5.50},
            {"nombre": "Alfarera del Bajío", "precio_num": 6.00}
        ]
    },
    'c2': {
        "id": "c2", "codigo": "102", "nombre": "Cemento Gris (Saco 50 kg)", "descripcion": "Cemento Portland ordinario de alta resistencia para todo tipo de obra negra.", "categoria": "construccion",
        "imagen": "images/construccion/c2.png",
        "marcas": [
            {"nombre": "Cruz Azul", "precio_num": 240.00},
            {"nombre": "Moctezuma", "precio_num": 250.00},
            {"nombre": "Holcim (Apasco)", "precio_num": 260.00},
            {"nombre": "Tolteca", "precio_num": 270.00}
        ]
    },
    'c3': {
        "id": "c3", "codigo": "103", "nombre": "Cal Hidratada (Saco 25 kg)", "descripcion": "Cal de excelente calidad para mezclas de revoque, aplanados y albañilería.", "categoria": "construccion",
        "imagen": "images/construccion/c3.png",
        "marcas": [
            {"nombre": "Calidra", "precio_num": 75.00},
            {"nombre": "Chapultepec", "precio_num": 80.00},
            {"nombre": "White Cal", "precio_num": 90.00}
        ]
    },
    'c4': {
        "id": "c4", "codigo": "104", "nombre": "Mortero / Cemento de Albañilería (50 kg)", "descripcion": "Mortero optimizado para pega de ladrillos, bloques y trabajos de mampostería.", "categoria": "construccion",
        "imagen": "images/construccion/c4.png",
        "marcas": [
            {"nombre": "Cruz Azul", "precio_num": 210.00},
            {"nombre": "Moctezuma", "precio_num": 220.00},
            {"nombre": "Tolteca", "precio_num": 235.00}
        ]
    },
    'c5': {
        "id": "c5", "codigo": "105", "nombre": "Impercel (Cemento Impermeable)", "descripcion": "Cemento con aditivo impermeabilizante integrado para cimientos y zonas húmedas.", "categoria": "construccion",
        "imagen": "images/construccion/c5.png",
        "marcas": [
            {"nombre": "Impercel", "precio_num": 280.00},
            {"nombre": "Crest", "precio_num": 310.00}
        ]
    },
    'c6': {
        "id": "c6", "codigo": "106", "nombre": "Pegazulejo (Saco 20 kg)", "descripcion": "Adhesivo en polvo base cemento para colocación de pisos cerámicos y azulejos.", "categoria": "construccion",
        "imagen": "images/construccion/c6.png",
        "marcas": [
            {"nombre": "Niasa", "precio_num": 130.00},
            {"nombre": "Crest", "precio_num": 145.00},
            {"nombre": "Lamosa", "precio_num": 160.00}
        ]
    },
    'c7': {
        "id": "c7", "codigo": "107", "nombre": "Ladrillo Loseta / Azotea", "descripcion": "Pieza cerámica delgada para aislamiento térmico e impermeabilización de azoteas.", "categoria": "construccion",
        "imagen": "images/construccion/c7.png",
        "marcas": [
            {"nombre": "Cerámica Regia", "precio_num": 12.00},
            {"nombre": "Lamosa", "precio_num": 16.00}
        ]
    },
    'c8': {
        "id": "c8", "codigo": "108", "nombre": "Block de Cemento (12x20x40 cm)", "descripcion": "Block hueco de concreto vibrado de alta durabilidad para muros divisorios o carga.", "categoria": "construccion",
        "imagen": "images/construccion/c8.png",
        "marcas": [
            {"nombre": "Vibroblock", "precio_num": 15.00},
            {"nombre": "Concretos MX", "precio_num": 19.00}
        ]
    },
    'c9': {
        "id": "c9", "codigo": "109", "nombre": "Adobón", "descripcion": "Pieza de barro de mayor tamaño para construcciones rústicas y tradicionales.", "categoria": "construccion",
        "imagen": "images/construccion/c9.png",
        "marcas": [
            {"nombre": "Rústicos del Centro", "precio_num": 18.00},
            {"nombre": "Artesanal", "precio_num": 24.00}
        ]
    },

    # 🏗️ ACEROS
    'ac1': {
        "id": "ac1", "codigo": "201", "nombre": "Varillas de 1/2, 1/4, 3/8", "descripcion": "Varilla corrugada de acero grado 42 para refuerzo estructural en losas y columnas.", "categoria": "aceros",
        "imagen": "images/aceros/ac1.png",
        "marcas": [
            {"nombre": "Deacero", "precio_num": 140.00},
            {"nombre": "Ternium", "precio_num": 150.00},
            {"nombre": "SLC", "precio_num": 160.00}
        ]
    },
    'ac2': {
        "id": "ac2", "codigo": "202", "nombre": "PTR de 1/2, 1/4, 3/8", "descripcion": "Perfil tubular rectangular para herrería y estructuras metálicas.", "categoria": "aceros",
        "imagen": "images/aceros/ac2.png",
        "marcas": [
            {"nombre": "Ternium", "precio_num": 280.00},
            {"nombre": "Deacero", "precio_num": 310.00},
            {"nombre": "Aceros Ocotlán", "precio_num": 350.00}
        ]
    },
    'ac3': {
        "id": "ac3", "codigo": "203", "nombre": "Tubular de 1/2, 1/4, 3/8", "descripcion": "Tubo industrial de acero para soportes, barandales y marcos.", "categoria": "aceros",
        "imagen": "images/aceros/ac3.png",
        "marcas": [
            {"nombre": "Ternium", "precio_num": 230.00},
            {"nombre": "Regiomontana de Perfiles", "precio_num": 260.00}
        ]
    },
    'ac4': {
        "id": "ac4", "codigo": "204", "nombre": "Lámina Lisa", "descripcion": "Lámina de acero para cubiertas, charolas y trabajos de hojalatería.", "categoria": "aceros",
        "imagen": "images/aceros/ac4.png",
        "marcas": [
            {"nombre": "Ternium", "precio_num": 350.00},
            {"nombre": "Galvak", "precio_num": 390.00}
        ]
    },
    'ac5': {
        "id": "ac5", "codigo": "205", "nombre": "Lámina Galvanizada", "descripcion": "Lámina con recubrimiento de zinc altamente resistente a la corrosión.", "categoria": "aceros",
        "imagen": "images/aceros/ac5.png",
        "marcas": [
            {"nombre": "Ternium", "precio_num": 400.00},
            {"nombre": "Galvak", "precio_num": 430.00},
            {"nombre": "Metecno", "precio_num": 450.00}
        ]
    },
    'ac6': {
        "id": "ac6", "codigo": "206", "nombre": "Tubo Cuadrado", "descripcion": "Perfil hueco de sección cuadrada para estructuras y carpintería metálica.", "categoria": "aceros",
        "imagen": "images/aceros/ac6.png",
        "marcas": [
            {"nombre": "Ternium", "precio_num": 310.00},
            {"nombre": "Deacero", "precio_num": 340.00}
        ]
    },
    'ac7': {
        "id": "ac7", "codigo": "207", "nombre": "Tubo Redondo", "descripcion": "Tubo de acero estructural redondo para conducción y soporte.", "categoria": "aceros",
        "imagen": "images/aceros/ac7.png",
        "marcas": [
            {"nombre": "Ternium", "precio_num": 290.00},
            {"nombre": "Aceros Levón", "precio_num": 320.00}
        ]
    },
    'ac8': {
        "id": "ac8", "codigo": "208", "nombre": "Malla Ciclónica", "descripcion": "Malla de alambre galvanizado entrelazado para delimitación perimetral.", "categoria": "aceros",
        "imagen": "images/aceros/ac8.png",
        "marcas": [
            {"nombre": "Deacero", "precio_num": 1200.00},
            {"nombre": "Cercos Mexicanos", "precio_num": 1350.00}
        ]
    },
    'ac9': {
        "id": "ac9", "codigo": "209", "nombre": "Tela Mosquitera", "descripcion": "Malla fina protectora para puertas y ventanas contra insectos.", "categoria": "aceros",
        "imagen": "images/aceros/ac9.png",
        "marcas": [
            {"nombre": "Fiero", "precio_num": 120.00},
            {"nombre": "Tupinambá", "precio_num": 140.00}
        ]
    },
    'ac10': {
        "id": "ac10", "codigo": "210", "nombre": "Ángulos", "descripcion": "Perfil estructural de acero en L para refuerzos y marcos.", "categoria": "aceros",
        "imagen": "images/aceros/ac10.png",
        "marcas": [
            {"nombre": "Ternium", "precio_num": 190.00},
            {"nombre": "Deacero", "precio_num": 215.00}
        ]
    },

    # 🎨 PINTURAS Y SOLVENTES
    'p1': {
        "id": "p1", "codigo": "301", "nombre": "Pintura Vinílica Base Agua (Variedad de Colores)", "descripcion": "Pintura base agua de alto rendimiento para interiores y exteriores.", "categoria": "pinturas",
        "imagen": "images/pinturas/p1.png",
        "marcas": [
            {"nombre": "Comex", "precio_num": 880.00},
            {"nombre": "Berel", "precio_num": 800.00},
            {"nombre": "Sherwin-Williams", "precio_num": 920.00},
            {"nombre": "Osel", "precio_num": 780.00}
        ]
    },
    'p2': {
        "id": "p2", "codigo": "302", "nombre": "Pinturas de Aceite (25 Colores Disponibles)", "descripcion": "Pintura alquílica brillante de gran durabilidad y protección para metales y madera.", "categoria": "pinturas",
        "imagen": "images/pinturas/p2.png",
        "marcas": [
            {"nombre": "Sayer", "precio_num": 320.00},
            {"nombre": "Berelinte", "precio_num": 340.00},
            {"nombre": "Prisa", "precio_num": 360.00}
        ]
    },
    'p3': {
        "id": "p3", "codigo": "303", "nombre": "Pinturas en Aerosol (25 Colores Disponibles)", "descripcion": "Spray acrílico de secado rápido para reparaciones y retoques.", "categoria": "pinturas",
        "imagen": "images/pinturas/p3.png",
        "marcas": [
            {"nombre": "Comex", "precio_num": 75.00},
            {"nombre": "Krylon", "precio_num": 80.00},
            {"nombre": "Dupli-Color", "precio_num": 90.00}
        ]
    },
    'p4': {
        "id": "p4", "codigo": "304", "nombre": "Sellador", "descripcion": "Sellador vinílico concentrado para preparar y sellar porosidad en muros.", "categoria": "pinturas",
        "imagen": "images/pinturas/p4.png",
        "marcas": [
            {"nombre": "Comex", "precio_num": 290.00},
            {"nombre": "Berel", "precio_num": 270.00},
            {"nombre": "Sayer", "precio_num": 300.00}
        ]
    },
    'p5': {
        "id": "p5", "codigo": "305", "nombre": "Primer (Fondo para pintar)", "descripcion": "Base primaria anticorrosiva de excelente adherencia antes del acabado.", "categoria": "pinturas",
        "imagen": "images/pinturas/p5.png",
        "marcas": [
            {"nombre": "Sherwin-Williams", "precio_num": 310.00},
            {"nombre": "Comex", "precio_num": 330.00}
        ]
    },
    'p6': {
        "id": "p6", "codigo": "306", "nombre": "Esmalte", "descripcion": "Esmalte sintético brillante protector contra la intemperie.", "categoria": "pinturas",
        "imagen": "images/pinturas/p6.png",
        "marcas": [
            {"nombre": "Sayerlack", "precio_num": 340.00},
            {"nombre": "Comex 100", "precio_num": 370.00}
        ]
    },
    'p7': {
        "id": "p7", "codigo": "307", "nombre": "Tíner", "descripcion": "Disolvente estándar para dilución de esmaltes y limpieza de herramientas.", "categoria": "pinturas",
        "imagen": "images/pinturas/p7.png",
        "marcas": [
            {"nombre": "Poliformas", "precio_num": 60.00},
            {"nombre": "Maston", "precio_num": 75.00}
        ]
    },

    # 🔩 TORNILLERÍA Y CLAVOS
    't1': {
        "id": "t1", "codigo": "401", "nombre": "Tornillos de rosca fina o milimétrica de toda medida", "descripcion": "Tornillería hexagonal y milimétrica de precisión para maquinaria e industria.", "categoria": "tornilleria",
        "imagen": "images/tornilleria/t1.png",
        "marcas": [
            {"nombre": "Fiero", "precio_num": 12.00},
            {"nombre": "Weston", "precio_num": 15.00},
            {"nombre": "Hermex", "precio_num": 18.00}
        ]
    },
    't2': {
        "id": "t2", "codigo": "402", "nombre": "Rondanas planas o de presión", "descripcion": "Juego de rondanas de acero galvanizado para distribución uniforme de carga.", "categoria": "tornilleria",
        "imagen": "images/tornilleria/t2.png",
        "marcas": [
            {"nombre": "Fiero", "precio_num": 3.00},
            {"nombre": "Hermex", "precio_num": 4.50}
        ]
    },
    't3': {
        "id": "t3", "codigo": "403", "nombre": "Tornillos de presión de toda medida", "descripcion": "Tornillos de alta sujeción a presión para fijaciones firmes.", "categoria": "tornilleria",
        "imagen": "images/tornilleria/t3.png",
        "marcas": [
            {"nombre": "Weston", "precio_num": 20.00},
            {"nombre": "Fiero", "precio_num": 25.00}
        ]
    },
    't4': {
        "id": "t4", "codigo": "404", "nombre": "Clavos de concreto de toda medida", "descripcion": "Clavos de acero templado estrados para fijación en muros de concreto.", "categoria": "tornilleria",
        "imagen": "images/tornilleria/t4.png",
        "marcas": [
            {"nombre": "Fiero", "precio_num": 45.00},
            {"nombre": "Hermex", "precio_num": 55.00}
        ]
    },
    't5': {
        "id": "t5", "codigo": "405", "nombre": "Clavos para madera de toda medida", "descripcion": "Clavos de alambre pulido con o sin cabeza para carpintería.", "categoria": "tornilleria",
        "imagen": "images/tornilleria/t5.png",
        "marcas": [
            {"nombre": "Fiero", "precio_num": 38.00},
            {"nombre": "Nacional", "precio_num": 42.00}
        ]
    },
    't6': {
        "id": "t6", "codigo": "406", "nombre": "Clavo para acero de toda medida", "descripcion": "Clavos especiales de ultra alta resistencia para penetración en láminas y acero.", "categoria": "tornilleria",
        "imagen": "images/tornilleria/t6.png",
        "marcas": [
            {"nombre": "Hilti", "precio_num": 75.00},
            {"nombre": "Fiero", "precio_num": 85.00}
        ]
    },

    # 🚽 CERÁMICA Y PISOS
    'ce1': {
        "id": "ce1", "codigo": "501", "nombre": "Accesorios para baños", "descripcion": "Juegos completos cromados o cerámicos de accesorios de baño.", "categoria": "ceramica",
        "imagen": "images/ceramica/ce1.png",
        "marcas": [
            {"nombre": "Coflex", "precio_num": 380.00},
            {"nombre": "Foset", "precio_num": 420.00}
        ]
    },
    'ce2': {
        "id": "ce2", "codigo": "502", "nombre": "Tazas para el baño", "descripcion": "Inodoros ecológicos ahorradores de agua con descarga eficiente.", "categoria": "ceramica",
        "imagen": "images/ceramica/ce2.png",
        "marcas": [
            {"nombre": "Helvex", "precio_num": 1800.00},
            {"nombre": "Castel", "precio_num": 1950.00},
            {"nombre": "Interceramic", "precio_num": 2200.00}
        ]
    },
    'ce3': {
        "id": "ce3", "codigo": "503", "nombre": "Lavamanos", "descripcion": "Lavabos cerámicos de pedestal y sobreponer.", "categoria": "ceramica",
        "imagen": "images/ceramica/ce3.png",
        "marcas": [
            {"nombre": "Interceramic", "precio_num": 900.00},
            {"nombre": "Helvex", "precio_num": 1100.00}
        ]
    },
    'ce4': {
        "id": "ce4", "codigo": "504", "nombre": "Mingitorios", "descripcion": "Mingitorios de cerámica de bajo consumo de agua.", "categoria": "ceramica",
        "imagen": "images/ceramica/ce4.png",
        "marcas": [
            {"nombre": "Castel", "precio_num": 1150.00},
            {"nombre": "Helvex", "precio_num": 1300.00}
        ]
    },
    'ce5': {
        "id": "ce5", "codigo": "505", "nombre": "Estantes para jabón de cerámica", "descripcion": "Jaboneras y repisas cerámicas para empotrar en muros de baño.", "categoria": "ceramica",
        "imagen": "images/ceramica/ce5.png",
        "marcas": [
            {"nombre": "Coflex", "precio_num": 140.00},
            {"nombre": "Interceramic", "precio_num": 170.00}
        ]
    },
    'ce6': {
        "id": "ce6", "codigo": "506", "nombre": "Vitropiso tipo madera", "descripcion": "Loseta cerámica con acabado y textura realista de madera.", "categoria": "ceramica",
        "imagen": "images/ceramica/ce6.png",
        "marcas": [
            {"nombre": "Lamosa", "precio_num": 200.00},
            {"nombre": "Vitromex", "precio_num": 220.00},
            {"nombre": "Interceramic", "precio_num": 250.00}
        ]
    },
    'ce7': {
        "id": "ce7", "codigo": "507", "nombre": "Vitropiso tipo mármol", "descripcion": "Piso cerámico brillante con vetas estilo mármol elegante.", "categoria": "ceramica",
        "imagen": "images/ceramica/ce7.png",
        "marcas": [
            {"nombre": "Porcelanite", "precio_num": 250.00},
            {"nombre": "Interceramic", "precio_num": 280.00}
        ]
    },
    'ce8': {
        "id": "ce8", "codigo": "508", "nombre": "Vitropiso antiderrapante", "descripcion": "Piso cerámico rugoso ideal para cocheras, patios y áreas húmedas.", "categoria": "ceramica",
        "imagen": "images/ceramica/ce8.png",
        "marcas": [
            {"nombre": "Vitromex", "precio_num": 210.00},
            {"nombre": "Lamosa", "precio_num": 235.00}
        ]
    },
    'ce9': {
        "id": "ce9", "codigo": "509", "nombre": "Vitropiso tradicional o cerámico", "descripcion": "Loseta cerámica estándar de gran resistencia para interiores.", "categoria": "ceramica",
        "imagen": "images/ceramica/ce9.png",
        "marcas": [
            {"nombre": "Lamosa", "precio_num": 170.00},
            {"nombre": "Vitromex", "precio_num": 190.00}
        ]
    },
    'ce10': {
        "id": "ce10", "codigo": "510", "nombre": "Piso porcelanico", "descripcion": "Porcelanato de alta dureza, cero absorción y bordes rectificados.", "categoria": "ceramica",
        "imagen": "images/ceramica/ce10.png",
        "marcas": [
            {"nombre": "Interceramic", "precio_num": 290.00},
            {"nombre": "Porcelanite", "precio_num": 330.00}
        ]
    },

    # 🚰 TUBERÍAS Y CONEXIONES
    'tu2': {
        "id": "tu2", "codigo": "602", "nombre": "Tubería de cobre", "descripcion": "Tubo rígido y flexible de cobre para instalaciones hidrosanitarias y gas.", "categoria": "tuberias",
        "imagen": "images/tuberias/tu2.png",
        "marcas": [
            {"nombre": "Nacobre", "precio_num": 400.00},
            {"nombre": "IUSA", "precio_num": 440.00}
        ]
    },
    'tu3': {
        "id": "tu3", "codigo": "603", "nombre": "Tubo Plus", "descripcion": "Sistema de polipropileno por termofusión garantizado cero fugas.", "categoria": "tuberias",
        "imagen": "images/tuberias/tu3.png",
        "marcas": [
            {"nombre": "Rotoplas", "precio_num": 260.00},
            {"nombre": "Amanco Wavin", "precio_num": 290.00}
        ]
    },
    'tu4': {
        "id": "tu4", "codigo": "604", "nombre": "Tubería de acero", "descripcion": "Tubo de acero galvanizado roscado para instalaciones de alta presión.", "categoria": "tuberias",
        "imagen": "images/tuberias/tu4.png",
        "marcas": [
            {"nombre": "Anáhuac", "precio_num": 620.00},
            {"nombre": "Ternium", "precio_num": 660.00}
        ]
    },
    'tu5': {
        "id": "tu5", "codigo": "605", "nombre": "Tubo PVC", "descripcion": "Tubería plástica para drenajes, bajadas pluviales y desagües.", "categoria": "tuberias",
        "imagen": "images/tuberias/tu5.png",
        "marcas": [
            {"nombre": "Duralón", "precio_num": 80.00},
            {"nombre": "Amanco Wavin", "precio_num": 90.00}
        ]
    },
    'tu6': {
        "id": "tu6", "codigo": "606", "nombre": "Tubo CPVC", "descripcion": "Tubería plástica especial resistente a altas presiones y agua caliente.", "categoria": "tuberias",
        "imagen": "images/tuberias/tu6.png",
        "marcas": [
            {"nombre": "FlowGuard", "precio_num": 105.00},
            {"nombre": "Coflex", "precio_num": 120.00}
        ]
    },

    # 🛠️ ACCESORIOS DE TRABAJO Y HERRAMIENTAS
    'h1': {
        "id": "h1", "codigo": "701", "nombre": "Termofusora", "descripcion": "Equipo eléctrico para fundir y unir conexiones de Tubo Plus.", "categoria": "accesorios",
        "imagen": "images/accesorios/h1.png",
        "marcas": [
            {"nombre": "Pretul", "precio_num": 900.00},
            {"nombre": "Truper", "precio_num": 980.00},
            {"nombre": "Rotoplas", "precio_num": 1050.00}
        ]
    },
    'h2': {
        "id": "h2", "codigo": "702", "nombre": "Silicones", "descripcion": "Cartuchos de silicón transparente y blanco sellador multiusos.", "categoria": "accesorios",
        "imagen": "images/accesorios/h2.png",
        "marcas": [
            {"nombre": "Sista", "precio_num": 60.00},
            {"nombre": "Dowsil", "precio_num": 75.00}
        ]
    },
    'h3': {
        "id": "h3", "codigo": "703", "nombre": "Tijeras", "descripcion": "Tijeras para corte de lámina, PVC y uso general.", "categoria": "accesorios",
        "imagen": "images/accesorios/h3.png",
        "marcas": [
            {"nombre": "Truper", "precio_num": 85.00},
            {"nombre": "Stanley", "precio_num": 100.00}
        ]
    },
    'h4': {
        "id": "h4", "codigo": "704", "nombre": "Palas", "descripcion": "Palas de cuchara redonda y cuadrada con mango de madera/fibra.", "categoria": "accesorios",
        "imagen": "images/accesorios/h4.png",
        "marcas": [
            {"nombre": "Pretul", "precio_num": 170.00},
            {"nombre": "Truper", "precio_num": 195.00}
        ]
    },
    'h5': {
        "id": "h5", "codigo": "705", "nombre": "Talaches", "descripcion": "Herramienta de excavación pesada con hacha y pico.", "categoria": "accesorios",
        "imagen": "images/accesorios/h5.png",
        "marcas": [
            {"nombre": "Truper", "precio_num": 240.00},
            {"nombre": "Surtek", "precio_num": 265.00}
        ]
    },
    'h6': {
        "id": "h6", "codigo": "706", "nombre": "Picos", "descripcion": "Picos de acero forjado para terrenos rocosos.", "categoria": "accesorios",
        "imagen": "images/accesorios/h6.png",
        "marcas": [
            {"nombre": "Truper", "precio_num": 220.00},
            {"nombre": "Pretul", "precio_num": 245.00}
        ]
    },
    'h7': {
        "id": "h7", "codigo": "707", "nombre": "Azadón", "descripcion": "Herramienta para labrado, limpieza y movimiento de tierra.", "categoria": "accesorios",
        "imagen": "images/accesorios/h7.png",
        "marcas": [
            {"nombre": "Truper", "precio_num": 180.00},
            {"nombre": "Surtek", "precio_num": 205.00}
        ]
    },
    'h8': {
        "id": "h8", "codigo": "708", "nombre": "Hachas", "descripcion": "Hachas de acero forjado con mango antiderrapante.", "categoria": "accesorios",
        "imagen": "images/accesorios/h8.png",
        "marcas": [
            {"nombre": "Truper", "precio_num": 270.00},
            {"nombre": "Stanley", "precio_num": 310.00}
        ]
    },
    'h9': {
        "id": "h9", "codigo": "709", "nombre": "Parrillas", "descripcion": "Parrillas de gas y sobreponer reforzadas.", "categoria": "accesorios",
        "imagen": "images/accesorios/h9.png",
        "marcas": [
            {"nombre": "Cinsa", "precio_num": 430.00},
            {"nombre": "Avera", "precio_num": 480.00}
        ]
    },
    'h10': {
        "id": "h10", "codigo": "710", "nombre": "Mangueras de toda medida", "descripcion": "Mangueras reforzadas de niveles y riego agrícola/doméstico.", "categoria": "accesorios",
        "imagen": "images/accesorios/h10.png",
        "marcas": [
            {"nombre": "IUSA", "precio_num": 350.00},
            {"nombre": "Truper", "precio_num": 400.00}
        ]
    },
    'h11': {
        "id": "h11", "codigo": "711", "nombre": "Guantes", "descripcion": "Guantes de carnaza, hilo y maniobra industrial.", "categoria": "accesorios",
        "imagen": "images/accesorios/h11.png",
        "marcas": [
            {"nombre": "DermaCare", "precio_num": 30.00},
            {"nombre": "Truper", "precio_num": 40.00}
        ]
    },
    'h12': {
        "id": "h12", "codigo": "712", "nombre": "Lentes de protección", "descripcion": "Lentes de seguridad transparentes anti-rayaduras.", "categoria": "accesorios",
        "imagen": "images/accesorios/h12.png",
        "marcas": [
            {"nombre": "3M", "precio_num": 40.00},
            {"nombre": "Truper", "precio_num": 50.00}
        ]
    },
    'h13': {
        "id": "h13", "codigo": "713", "nombre": "Arnés de seguridad", "descripcion": "Arnés de cuerpo entero para protección anticaídas.", "categoria": "accesorios",
        "imagen": "images/accesorios/h13.png",
        "marcas": [
            {"nombre": "3M Protecta", "precio_num": 620.00},
            {"nombre": "Surtek", "precio_num": 680.00}
        ]
    },
    'h14': {
        "id": "h14", "codigo": "714", "nombre": "Discos para corte (madera, acero)", "descripcion": "Discos abrasivos y diamantados para sierra y esmeril.", "categoria": "accesorios",
        "imagen": "images/accesorios/h14.png",
        "marcas": [
            {"nombre": "Austromex", "precio_num": 30.00},
            {"nombre": "Norton", "precio_num": 45.00},
            {"nombre": "Bosch", "precio_num": 90.00}
        ]
    },
    'h15': {
        "id": "h15", "codigo": "715", "nombre": "Pinzas", "descripcion": "Pinzas de chofer, presión, corte y electricidad.", "categoria": "accesorios",
        "imagen": "images/accesorios/h15.png",
        "marcas": [
            {"nombre": "Pretul", "precio_num": 95.00},
            {"nombre": "Truper", "precio_num": 120.00},
            {"nombre": "Stanley", "precio_num": 140.00}
        ]
    },
    'h16': {
        "id": "h16", "codigo": "716", "nombre": "Cables", "descripcion": "Cables eléctricos de cobre aislados de varios calibres.", "categoria": "accesorios",
        "imagen": "images/accesorios/h16.png",
        "marcas": [
            {"nombre": "Condumex", "precio_num": 330.00},
            {"nombre": "Viakon", "precio_num": 370.00}
        ]
    },
    'h17': {
        "id": "h17", "codigo": "717", "nombre": "Llaves", "descripcion": "Juegos de llaves combinadas, ajustables (pericas) y Allen.", "categoria": "accesorios",
        "imagen": "images/accesorios/h17.png",
        "marcas": [
            {"nombre": "Truper", "precio_num": 200.00},
            {"nombre": "Craftsman", "precio_num": 250.00}
        ]
    },
    'h18': {
        "id": "h18", "codigo": "718", "nombre": "Pulidoras", "descripcion": "Esmeriladoras angulares eléctricas profesionales.", "categoria": "accesorios",
        "imagen": "images/accesorios/h18.png",
        "marcas": [
            {"nombre": "Dewalt", "precio_num": 950.00},
            {"nombre": "Makita", "precio_num": 1020.00},
            {"nombre": "Bosch", "precio_num": 970.00}
        ]
    },
    'h19': {
        "id": "h19", "codigo": "719", "nombre": "Cortadoras de vitropiso", "descripcion": "Cortadoras manuales de azulejos con rieles de acero.", "categoria": "accesorios",
        "imagen": "images/accesorios/h19.png",
        "marcas": [
            {"nombre": "Truper", "precio_num": 1050.00},
            {"nombre": "Bricard", "precio_num": 1150.00}
        ]
    },
    'h20': {
        "id": "h20", "codigo": "720", "nombre": "Máquina para soldar", "descripcion": "Soldadora inversora ligera y potente para electrodo.", "categoria": "accesorios",
        "imagen": "images/accesorios/h20.png",
        "marcas": [
            {"nombre": "Infra", "precio_num": 2400.00},
            {"nombre": "Truper", "precio_num": 2500.00},
            {"nombre": "Evans", "precio_num": 2700.00}
        ]
    },
    'h21': {
        "id": "h21", "codigo": "721", "nombre": "Electrodos", "descripcion": "Electrodos para soldadura de arco eléctrico 6013.", "categoria": "accesorios",
        "imagen": "images/accesorios/h21.png",
        "marcas": [
            {"nombre": "Infra", "precio_num": 130.00},
            {"nombre": "Eutectic", "precio_num": 155.00}
        ]
    }
}

def recalcular_precios_producto(p_data):
    if "marcas" in p_data and p_data["marcas"]:
        precios = [m["precio_num"] for m in p_data["marcas"]]
        min_p = min(precios)
        max_p = max(precios)
        if min_p != max_p:
            p_data["precio"] = f"${min_p:,.2f} - ${max_p:,.2f} MXN"
        else:
            p_data["precio"] = f"${min_p:,.2f} MXN"
        p_data["precio_num"] = min_p

for p_id, p_data in PRODUCTOS.items():
    recalcular_precios_producto(p_data)

COLORES_PINTURA = [
    "Blanco Ostras", "Blanco Humo", "Marfil Claro", "Gris Perla", "Gris Acero",
    "Gris Oscuro", "Arena del Desierto", "Beige Suave", "Azul Cielo", "Azul Naval",
    "Azul Océano", "Verde Limón", "Verde Musgo", "Verde Jade", "Amarillo Canario",
    "Amarillo Trigo", "Naranja Crepúsculo", "Rojo Terracota", "Rojo Oxido", "Vino Tinto",
    "Rosa Pastel", "Violeta Real", "Café Tabaco", "Chocolate Intenso", "Negro Profundo"
]

def obtener_productos_ordenados(categoria):
    mats = [p for p in PRODUCTOS.values() if p['categoria'] == categoria]
    orden = request.args.get('orden', '')
    if orden == 'desc':
        mats = sorted(mats, key=lambda x: x.get('precio_num', 0), reverse=True)
    elif orden == 'asc':
        mats = sorted(mats, key=lambda x: x.get('precio_num', 0))
    return mats

@app.before_request
def inicializar_sesion():
    if 'lista_compras' not in session:
        session['lista_compras'] = []

@app.context_processor
def utility_processor():
    def calcular_total_lista():
        lista = session.get('lista_compras', [])
        total = sum(item.get('precio_item', item.get('precio_num', 0)) * item.get('cantidad', 1) for item in lista)
        return f"${total:,.2f} MXN"
    return dict(calcular_total_lista=calcular_total_lista)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/construccion')
def construccion():
    mats = obtener_productos_ordenados('construccion')
    return render_template('construccion.html', materiales=mats)

@app.route('/aceros')
def aceros():
    mats = obtener_productos_ordenados('aceros')
    return render_template('aceros.html', materiales=mats)

@app.route('/pinturas')
def pinturas():
    mats = obtener_productos_ordenados('pinturas')
    return render_template('pinturas.html', materiales=mats, colores=COLORES_PINTURA)

@app.route('/tornilleria')
def tornilleria():
    mats = obtener_productos_ordenados('tornilleria')
    return render_template('tornilleria.html', materiales=mats)

@app.route('/ceramica')
def ceramica():
    mats = obtener_productos_ordenados('ceramica')
    return render_template('ceramica.html', materiales=mats)

@app.route('/tuberias')
def tuberias():
    mats = obtener_productos_ordenados('tuberias')
    return render_template('tuberias.html', materiales=mats)

@app.route('/accesorios')
def accesorios():
    mats = obtener_productos_ordenados('accesorios')
    return render_template('accesorios.html', materiales=mats)

@app.route('/buscar')
def buscar():
    query = request.args.get('q', '').strip().lower()
    orden = request.args.get('orden', '')
    resultados = []
    if query:
        for p in PRODUCTOS.values():
            if query in p['nombre'].lower() or query in p['descripcion'].lower():
                resultados.append(p)
    if orden == 'desc':
        resultados = sorted(resultados, key=lambda x: x.get('precio_num', 0), reverse=True)
    elif orden == 'asc':
        resultados = sorted(resultados, key=lambda x: x.get('precio_num', 0))
    return render_template('buscar.html', resultados=resultados, query=query)

@app.route('/agregar/<prod_id>')
def agregar(prod_id):
    if prod_id in PRODUCTOS:
        prod = PRODUCTOS[prod_id]
        marca = request.args.get('marca', '')
        color = request.args.get('color', '')
        
        # Captura la cantidad seleccionada por el usuario (por defecto 1)
        try:
            cantidad_deseada = int(request.args.get('cantidad', 1))
            if cantidad_deseada < 1:
                cantidad_deseada = 1
        except ValueError:
            cantidad_deseada = 1
        
        precio_item = prod['precio_num']
        if marca and prod.get('marcas'):
            for m in prod['marcas']:
                if m['nombre'] == marca:
                    precio_item = m['precio_num']
                    break
        else:
            if prod.get('marcas') and not marca:
                marca = prod['marcas'][0]['nombre']
                precio_item = prod['marcas'][0]['precio_num']

        nombre_final = prod['nombre']
        if color:
            nombre_final += f" - Color: {color}"

        lista = session.get('lista_compras', [])
        encontrado = False
        for item in lista:
            if item['id'] == prod_id and item.get('marca', '') == marca and item.get('nombre') == nombre_final:
                item['cantidad'] += cantidad_deseada
                encontrado = True
                break
        
        if not encontrado:
            item_nuevo = prod.copy()
            item_nuevo['nombre'] = nombre_final
            item_nuevo['marca'] = marca
            item_nuevo['precio_item'] = precio_item
            item_nuevo['cantidad'] = cantidad_deseada
            lista.append(item_nuevo)
            
        session['lista_compras'] = lista
        session.modified = True
    return redirect(request.referrer or url_for('index'))

@app.route('/escanear_codigo', methods=['POST'])
def escanear_codigo():
    codigo = request.form.get('codigo', '').strip().lower()
    if codigo:
        producto_encontrado = None
        for p_id, p_data in PRODUCTOS.items():
            if p_id.lower() == codigo or p_data.get('codigo', '').lower() == codigo:
                producto_encontrado = p_data
                break
        
        if producto_encontrado:
            prod = producto_encontrado
            marca = prod['marcas'][0]['nombre'] if prod.get('marcas') else ''
            precio_item = prod['marcas'][0]['precio_num'] if prod.get('marcas') else prod.get('precio_num', 0)
            
            lista = session.get('lista_compras', [])
            encontrado = False
            for item in lista:
                if item['id'] == prod['id'] and item.get('marca', '') == marca:
                    item['cantidad'] += 1
                    encontrado = True
                    break
            if not len(lista) or not encontrado:
                item_nuevo = prod.copy()
                item_nuevo['marca'] = marca
                item_nuevo['precio_item'] = precio_item
                item_nuevo['cantidad'] = 1
                lista.append(item_nuevo)
            session['lista_compras'] = lista
            session.modified = True
    return redirect(request.referrer or url_for('index'))

@app.route('/quitar_item/<int:index>')
def quitar_item(index):
    lista = session.get('lista_compras', [])
    if 0 <= index < len(lista):
        if lista[index]['cantidad'] > 1:
            lista[index]['cantidad'] -= 1
        else:
            lista.pop(index)
        session['lista_compras'] = lista
        session.modified = True
    return redirect(request.referrer or url_for('index'))

@app.route('/agregar_producto_nuevo/<categoria>', methods=['POST'])
def agregar_producto_nuevo(categoria):
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    marcas_raw = request.form.get('marcas', '')
    precios_raw = request.form.get('precios', '')
    
    if nombre and descripcion and marcas_raw and precios_raw:
        lista_marcas_txt = [m.strip() for m in marcas_raw.split(',') if m.strip()]
        lista_precios_txt = [p.strip() for p in precios_raw.split(',') if p.strip()]
        
        marcas_estructuradas = []
        for i in range(len(lista_marcas_txt)):
            m_nombre = lista_marcas_txt[i]
            try:
                p_val = float(lista_precios_txt[i].replace('$', '').replace('MXN', '').strip())
            except (IndexError, ValueError):
                p_val = 0.0
            marcas_estructuradas.append({"nombre": m_nombre, "precio_num": p_val})
            
        if marcas_estructuradas:
            nuevo_id = f"custom_{len(PRODUCTOS) + 1}"
            nuevo_codigo = str(800 + len(PRODUCTOS))
            nuevo_prod = {
                "id": nuevo_id,
                "codigo": nuevo_codigo,
                "nombre": nombre,
                "descripcion": descripcion,
                "categoria": categoria,
                "imagen": f"images/{categoria}/default.png",
                "marcas": marcas_estructuradas
            }
            recalcular_precios_producto(nuevo_prod)
            PRODUCTOS[nuevo_id] = nuevo_prod

    return redirect(url_for(categoria))

@app.route('/eliminar_producto/<prod_id>/<categoria>')
def eliminar_producto(prod_id, categoria):
    if prod_id in PRODUCTOS:
        del PRODUCTOS[prod_id]
    return redirect(request.referrer or url_for(categoria))

@app.route('/datos_pedido')
def datos_pedido():
    if not session.get('lista_compras'):
        return redirect(url_for('index'))
    return render_template('datos_pedido.html')

@app.route('/generar_ticket', methods=['POST'])
def generar_ticket():
    nombre_cliente = request.form.get('nombre_cliente', '').strip()
    fecha_recogida = request.form.get('fecha_recogida', '')
    hora_recogida = request.form.get('hora_recogida', '')
    
    lista = session.get('lista_compras', [])
    if not lista or not nombre_cliente:
        return redirect(url_for('index'))
    
    total = sum(item.get('precio_item', item.get('precio_num', 0)) * item.get('cantidad', 1) for item in lista)
    folio = f"DYH-{int(datetime.now().timestamp())}"
    
    datos_ticket = {
        "folio": folio,
        "cliente": nombre_cliente,
        "fecha_recogida": fecha_recogida,
        "hora_recogida": hora_recogida,
        "fecha_emision": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "productos": list(lista),
        "total": f"${total:,.2f} MXN"
    }
    
    session['ticket_actual'] = datos_ticket
    return redirect(url_for('ver_ticket'))

@app.route('/ticket')
def ver_ticket():
    ticket = session.get('ticket_actual')
    if not ticket:
        return redirect(url_for('index'))
    return render_template('ticket.html', ticket=ticket)

@app.route('/finalizar_compra')
def finalizar_compra():
    session['lista_compras'] = []
    session.pop('ticket_actual', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)