# Motor de Recomendaciones - Compensar

Repositorio oficial del motor de recomendaciones personalizado para la plataforma digital de **Compensar**, desarrollado como parte de la prueba práctica de evaluación.

[Repositorio en GitHub](https://github.com/RobiDeantonio/comp-recommender)

---

## 1️⃣ Metodología utilizada

Este motor combina **filtrado basado en contenido** con **popularidad de productos**, generando recomendaciones personalizadas a partir de:

* **Intereses del usuario**: cada usuario tiene etiquetas de interés (deportes, salud, bienestar, etc.).
* **Atributos del producto**: nombre, categoría, descripción y palabras clave.
* **Popularidad del producto**: basada en la cantidad de interacciones y el rating promedio.

El **score final** de cada producto combina:

```
score_híbrido = 0.7 * similitud_usuario_producto + 0.3 * popularidad_normalizada
```

Se utiliza **TF-IDF** para vectorizar texto de productos y calcular similitud coseno con los intereses del usuario.

---

## 2️⃣ Dataset y procesamiento

Se utilizan tres datasets CSV:

| Archivo            | Tamaño | Contenido                                                                                |
| ------------------ | ------ | ---------------------------------------------------------------------------------------- |
| `users.csv`        | 2.8 MB | Información de usuarios: edad, género, intereses, ubicación, tipo de suscripción, etc.   |
| `products.csv`     | 328 KB | Información de productos: nombre, descripción, categoría, precio, stock, palabras clave. |
| `interactions.csv` | 465 KB | Historial de interacciones: compras, ratings, método de pago, timestamp.                 |

**Procesamiento**:

* Limpieza de datos: conversión de columnas numéricas y categóricas.
* Normalización de texto: minúsculas, eliminación de espacios, separación de palabras clave.
* Conversión de intereses del usuario y palabras clave del producto en vectores para cálculo de similitud.

---

## 3️⃣ Tecnologías y arquitectura

* **Lenguaje:** Python 3.10
* **Framework:** FastAPI para exponer la API REST
* **Machine Learning:** scikit-learn (TF-IDF y similitud coseno)
* **Contenedor:** Docker
* **Despliegue gratuito:** Render (auto-escalable, URL pública)

**Arquitectura**:

```
Cliente → FastAPI (src/api.py) → RecommenderSystem (src/recommender.py) → CSV datasets (data/)
```

* La API expone endpoints `/recommendations` y `/popular`.
* Los datasets se cargan al iniciar la app y se mantienen en memoria para consultas rápidas.

---

## 4️⃣ Estructura del repositorio

```
comp-recommender/
├── data/                     # CSVs de usuarios, productos e interacciones
├── src/
│   ├── __init__.py           # Marca src como paquete
│   ├── api.py                # FastAPI app
│   ├── data_loader.py        # Funciones para cargar y procesar CSVs
│   └── recommender.py        # Lógica del motor de recomendaciones
├── requirements.txt          # Dependencias Python
├── Dockerfile                # Contenedor para Render
└── README.md                 # Este archivo
```

---

## 5️⃣ Cómo ejecutar la API localmente

1. Clona el repositorio:

```bash
git clone https://github.com/RobiDeantonio/comp-recommender.git
cd comp-recommender
```

2. Instala dependencias:

```bash
pip install -r requirements.txt
```

3. Corre la API con Uvicorn:

```bash
uvicorn src.api:app --host 0.0.0.0 --port 8000
```

4. Prueba la documentación interactiva:
   [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 6️⃣ Cómo ejecutar la API en Render

1. Conecta el repositorio en Render.
2. Render detecta el **Dockerfile** y construye la imagen automáticamente.
3. La API se desplegará en la URL pública asignada, por ejemplo:

```
https://comp-recommender.onrender.com
```

---

## 7️⃣ Ejemplos de consultas a la API

### Recomendaciones personalizadas

```
https://comp-recommender.onrender.com/recommendations?user_id=1&top_n=5
```

**Respuesta esperada**:

```json
{
  "user_id": 1,
  "recommendations": [
    {
      "product_id": 1460,
      "name": "Rutina de Ejercicios Personalizada",
      "category": "deportes",
      "score": 0.299999999990625
    },
    {
      "product_id": 305,
      "name": "Entrenador Personal Virtual",
      "category": "bienestar mental",
      "score": 0.290624999990918
    },
    {
      "product_id": 1612,
      "name": "Vitaminas y Suplementos",
      "category": "nutrición",
      "score": 0.281249999991211
    },
    {
      "product_id": 1700,
      "name": "Spa y Masajes",
      "category": "salud",
      "score": 0.281249999991211
    },
    {
      "product_id": 1789,
      "name": "Ropa Deportiva",
      "category": "deportes",
      "score": 0.271874999991504
    }
  ]
}
```

### Productos más populares

```bash
curl "https://comp-recommender.onrender.com/popular?top_n=3"
```

**Respuesta esperada**:

```json
{
  "recommendations": [
    {
      "product_id": 1460,
      "name": "Rutina de Ejercicios Personalizada",
      "category": "deportes",
      "score": 18.525
    },
    {
      "product_id": 305,
      "name": "Entrenador Personal Virtual",
      "category": "bienestar mental",
      "score": 18.15
    },
    {
      "product_id": 1612,
      "name": "Vitaminas y Suplementos",
      "category": "nutrición",
      "score": 17.9714285714286
    }
  ]
}
```

---
