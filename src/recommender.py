import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecommenderSystem:
    def __init__(self, users: pd.DataFrame, products: pd.DataFrame, interactions: pd.DataFrame):
        self.users = users
        self.products = products
        self.interactions = interactions
        self.product_profiles = None
        self._build_content_profiles()

    def _build_content_profiles(self):
        """
        Construye representaciones vectoriales de los productos
        usando palabras clave + descripción.
        """
        self.products['text_features'] = self.products.apply(
            lambda row: " ".join(row['palabras_clave']) + " " + str(row['descripcion']),
            axis=1
        )

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(self.products['text_features'])
        self.product_profiles = (vectorizer, tfidf_matrix)

    def recommend_by_popularity(self, top_n=5):
        """
        Ranking de productos más populares (compras + valoraciones altas).
        """
        pop = (
            self.interactions.groupby("product_id")
            .agg(pop_score=("rating", "mean"), n_interacciones=("product_id", "count"))
            .fillna(0)
            .reset_index()
        )
        pop['score'] = pop['pop_score'] * 0.6 + pop['n_interacciones'] * 0.4
        pop = pop.sort_values("score", ascending=False)

        return pd.merge(pop, self.products, on="product_id").head(top_n)

    def recommend_for_user(self, user_id: int, top_n=5):
        if user_id not in self.users['user_id'].values:
            return self.recommend_by_popularity(top_n)

        user = self.users[self.users['user_id'] == user_id].iloc[0]

        # Vector del usuario (intereses como texto)
        user_text = " ".join(user['intereses'])
        vectorizer, tfidf_matrix = self.product_profiles
        user_vec = vectorizer.transform([user_text])

        # Similaridad coseno usuario-productos
        sim_scores = cosine_similarity(user_vec, tfidf_matrix).flatten()
        self.products['sim_score'] = sim_scores

        # Popularidad
        pop = (
            self.interactions.groupby("product_id")
            .agg(pop_score=("rating", "mean"), n_interacciones=("product_id", "count"))
            .fillna(0)
            .reset_index()
        )
        pop['pop_norm'] = (pop['n_interacciones'] - pop['n_interacciones'].min()) / (
            pop['n_interacciones'].max() - pop['n_interacciones'].min() + 1e-9
        )
        merged = pd.merge(self.products, pop, on="product_id", how="left").fillna(0)

        # Score híbrido
        merged['score'] = 0.7 * merged['sim_score'] + 0.3 * merged['pop_norm']

        # 🔹 Seleccionamos productos top-N y nos quedamos solo con IDs y score
        top_recs = merged.sort_values("score", ascending=False).head(top_n)[['product_id','score']]

        

        # 🔹 Recuperamos los nombres REALES desde self.products
        recs = pd.merge(
            top_recs,
            self.products[['product_id','name','category']],
            on='product_id',
            how='left'
        )

        print(recs)

        # Reordenamos columnas
        recs = recs[['product_id','name','category','score']].reset_index(drop=True)

        return recs




if __name__ == "__main__":
    from data_loader import load_all

    users, products, interactions = load_all(
        "../data/users.csv", "../data/products.csv", "../data/interactions.csv"
    )

    '''
    print(users.head(2))
    print('='*60)
    print(products.head(2))
    print('='*60)
    print(interactions.head(2))
    print('='*60)
    '''

    recommender = RecommenderSystem(users, products, interactions)

    # Recomendaciones globales (popularidad)
    print("Top productos populares:")
    print(recommender.recommend_by_popularity(3))

    # Recomendaciones personalizadas
    print("\nRecomendaciones para user_id=1:")
    print(recommender.recommend_for_user(1, 5))
