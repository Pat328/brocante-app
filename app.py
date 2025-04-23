
import streamlit as st
import pandas as pd
import io

# Titre
st.title("Recherche de réservations - Brocante")

# Chargement automatique du fichier Excel
file_path = "reservations_brocante.xlsx"
try:
    df = pd.read_excel(file_path)
except Exception as e:
    st.error(f"Erreur lors du chargement du fichier : {e}")
    st.stop()

st.success("Fichier chargé avec succès !")

# Affichage du tableau original
st.subheader("Toutes les réservations")
st.dataframe(df)

st.subheader("Filtres de recherche")

# Création des filtres dynamiques pour chaque colonne
filtered_df = df.copy()
for col in df.columns:
    search = st.text_input(f"Rechercher dans '{col}'", "")
    if search:
        try:
            # Tentative de conversion en nombre (int ou float)
            search_num = float(search) if '.' in search else int(search)

            # Si la colonne est numérique, on compare directement
            if pd.api.types.is_numeric_dtype(df[col]):
                filtered_df = filtered_df[filtered_df[col] == search_num]
            else:
                # Sinon on compare les textes (égalité stricte, pas "contient")
                filtered_df = filtered_df[filtered_df[col].astype(str) == search]
        except ValueError:
            # Si la recherche n’est pas un nombre, on fait un .contains classique
            filtered_df = filtered_df[
                filtered_df[col].astype(str).str.contains(search, case=False, na=False)
            ]
# Résultats filtrés
st.subheader("Résultats filtrés")
st.dataframe(filtered_df)

excel_buffer = io.BytesIO()
filtered_df.to_excel(excel_buffer, index=False, engine='openpyxl')
excel_buffer.seek(0)

st.download_button(
    "Télécharger les résultats filtrés en Excel",
    data=excel_buffer,
    file_name="resultats_filtres.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
