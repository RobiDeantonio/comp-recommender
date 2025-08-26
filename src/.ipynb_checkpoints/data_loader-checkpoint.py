import pandas as pd

def load_users(path: str) -> pd.DataFrame:
    """
    Carga y limpia la información de usuarios.
    """
    users = pd.read_csv(path)
    
    # Normalización de strings
    users['genero'] = users['genero'].str.lower().str.strip()
    users['nivel_ingresos'] = users['nivel_ingresos'].str.lower().str.strip()
    users['nivel_educativo'] = users['nivel_educativo'].str.lower().str.strip()
    
    # Separar intereses en listas
    if 'intereses' in users.columns:
        users['intereses'] = users['intereses'].fillna("").apply(lambda x: [i.strip().lower() for i in str(x).split(",") if i])
    
    return users


def load_products(path: str) -> pd.DataFrame:
    """
    Carga y limpia la información de productos.
    """
    products = pd.read_csv(path)
    
    # Normalización
    products['category'] = products['category'].str.lower().str.strip()
    products['palabras_clave'] = products['palabras_clave'].fillna("").apply(
        lambda x: [p.strip().lower() for p in str(x).split(",") if p]
    )
    
    # Convertir precios y ratings a numéricos
    products['precio'] = pd.to_numeric(products['precio'], errors='coerce')
    products['rating_promedio'] = pd.to_numeric(products['rating_promedio'], errors='coerce')
    
    return products


def load_interactions(path: str) -> pd.DataFrame:
    """
    Carga y limpia la información de interacciones.
    """
    interactions = pd.read_csv(path)
    
    # Convertir timestamp a datetime
    interactions['timestamp'] = pd.to_datetime(interactions['timestamp'], errors='coerce')
    
    # Normalizar strings
    interactions['tipo_interaccion'] = interactions['tipo_interaccion'].str.lower().str.strip()
    interactions['metodo_pago'] = interactions['metodo_pago'].str.lower().str.strip()
    
    # Ratings numéricos
    if 'rating' in interactions.columns:
        interactions['rating'] = pd.to_numeric(interactions['rating'], errors='coerce').fillna(0)
    
    return interactions


def load_all(users_path: str, products_path: str, interactions_path: str):
    """
    Carga los tres datasets principales y los retorna como dataframes.
    """
    users = load_users(users_path)
    products = load_products(products_path)
    interactions = load_interactions(interactions_path)
    
    return users, products, interactions
