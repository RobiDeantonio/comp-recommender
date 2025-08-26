import pandas as pd
import re

def load_users(path: str) -> pd.DataFrame:
    users = pd.read_csv(path, sep=",", engine="python")  # tolera tabs o comas
    users['edad'] = pd.to_numeric(users['edad'], errors='coerce')
    for col in ['genero', 'nivel_ingresos', 'nivel_educativo', 'tipo_suscripcion',
                'categoria_cliente', 'ubicacion', 'dispositivo', 'frecuencia_login']:
        if col in users.columns:
            users[col] = users[col].astype(str).str.lower().str.strip()
    users['intereses'] = users['intereses'].fillna("").apply(
        lambda x: [i.strip().lower() for i in str(x).split(",") if i]
    )
    return users


def split_keywords(x):
    if pd.isna(x):
        return []
    return [kw.strip().lower() for kw in re.split('[,;|\t]+', str(x)) if kw.strip()]


def load_products(path: str) -> pd.DataFrame:
    products = pd.read_csv(path, sep=";", engine="python")
    products['category'] = products['category'].astype(str).str.lower().str.strip()
    products['palabras_clave'] = products['palabras_clave'].apply(split_keywords)
    for col in ['precio', 'rating_promedio', 'descuento_aplicado', 'stock_actual']:
        products[col] = pd.to_numeric(products[col], errors='coerce')
    return products


def load_interactions(path: str) -> pd.DataFrame:
    interactions = pd.read_csv(path, sep=",", engine="python")
    interactions['timestamp'] = pd.to_datetime(interactions['timestamp'], errors='coerce')
    interactions['tipo_interaccion'] = interactions['tipo_interaccion'].astype(str).str.lower().str.strip()
    interactions['metodo_pago'] = interactions['metodo_pago'].astype(str).str.lower().str.strip()
    interactions['rating'] = pd.to_numeric(interactions['rating'], errors='coerce')
    return interactions


def load_all(users_path: str, products_path: str, interactions_path: str):
    users = load_users(users_path)
    products = load_products(products_path)
    interactions = load_interactions(interactions_path)
    return users, products, interactions
