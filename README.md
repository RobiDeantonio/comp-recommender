# Motor de Recomendaciones - Compensar

Repositorio oficial del motor de recomendaciones personalizado para la plataforma digital de **Compensar**, desarrollado como parte de la prueba práctica de evaluación.

[Repositorio en GitHub](https://github.com/RobiDeantonio/comp-recommender)

---
## 1️⃣ Metodología y estrategias de recomendación

El motor implementa un enfoque **híbrido**, combinando:

1. **Filtrado Basado en Contenido**:

   * Se extraen **palabras clave** y la **descripción del producto**.
   * Se utiliza **TF-IDF** para vectorizar los textos de los productos.
   * Cada usuario tiene un vector de intereses basado en sus etiquetas (`intereses`), que se transforma también a un vector TF-IDF.
   * Se calcula la **similitud coseno** entre el vector de intereses del usuario y cada producto, obteniendo un `sim_score` que refleja qué tan relevante es cada producto para ese usuario.

2. **Popularidad de Productos**:

   * Se evalúa la popularidad basada en el **rating promedio** y el **número de interacciones** de cada producto.
   * Se normaliza la popularidad (`pop_norm`) para que pueda combinarse con la similitud de contenido.

3. **Score Híbrido**:

   * Combinación ponderada de similitud y popularidad:

```python
score_hibrido = 0.7 * sim_score + 0.3 * pop_norm
```

* Esta estrategia permite que los productos recomendados no solo sean relevantes para los intereses del usuario, sino también populares dentro de la plataforma.

4. **Recomendaciones Globales (Fallback)**:

   * Si el usuario no tiene intereses registrados o no existe, se devuelven los productos más populares, evitando mostrar recomendaciones irrelevantes.

**Resumen del flujo de recomendación para un usuario:**

```
Usuarios -> Extraer intereses -> Vectorizar -> Calcular similitud con productos -> Calcular score híbrido -> Ordenar top-N -> Devolver recomendaciones
```
---

## 2️⃣ Dataset y procesamiento

Se utilizan tres datasets CSV:

| Archivo            | Tamaño | Contenido                                                                                |
| ------------------ | ------ | ---------------------------------------------------------------------------------------- |
| `users.csv`        | 465 kB | Información de usuarios: edad, género, intereses, ubicación, tipo de suscripción, etc.   |
| `products.csv`     | 328 KB | Información de productos: nombre, descripción, categoría, precio, stock, palabras clave. |
| `interactions.csv` | 2.8 MB | Historial de interacciones: compras, ratings, método de pago, timestamp.                 |

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

**Recomendaciones**
```
http://0.0.0.0:8000/recommendations?user_id=1&top_n=5
```

**Popularidad**
```
http://0.0.0.0:8000/popular?top_n=3
```
---

## 6️⃣ Cómo ejecutar la API en Render

**Render** es una plataforma de **despliegue en la nube** que permite publicar aplicaciones web, APIs, bases de datos y servicios de forma sencilla, sin necesidad de administrar servidores directamente.

Para este caso el repositorio de **GitHub** se conecta con Render, de está manera se puede publicar tu API de recomendaciones en línea, dándote una URL pública (https://comp-recommender.onrender.com/) que cualquiera puede usar para hacer consultas a tu motor de recomendaciones.

**Proceso de conexión***

1. Conecta el repositorio en Render.
2. Render detecta el **Dockerfile** y construye la imagen **(Docker)** usando automáticamente.
3. La API se desplegará en la URL pública asignada, por ejemplo:

```
https://comp-recommender.onrender.com
```

---

## 7️⃣ Ejemplos de consultas a la API

### Recomendaciones personalizadas


[Probar recomendaciones](https://comp-recommender.onrender.com/recommendations?user_id=1&top_n=5)
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


[Probar más Populares](https://comp-recommender.onrender.com/popular?top_n=3)

```
https://comp-recommender.onrender.com/popular?top_n=3
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
