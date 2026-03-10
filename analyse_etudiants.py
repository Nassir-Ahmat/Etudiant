import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analyse des étudiants", layout="wide")

st.title("Analyse de la charge des étudiants")
st.write("Cette application analyse le temps consacré aux études, aux certifications et à la recherche de stage.")

# Charger le dataset
df = pd.read_csv("student.csv")

st.subheader("Aperçu du dataset")
st.dataframe(df.head())

# Création métrique
df["charge_totale"] = (
    df["heures_transport"]
    + df["heures_ecole"]
    + df["heures_certification"]
    + df["heures_recherche_stage"]
    + df["temps_linkedin"]
)

# 1. Temps moyen par activité
st.subheader("Temps moyen par activité")
activities = [
    "heures_sommeil",
    "heures_transport",
    "heures_ecole",
    "heures_certification",
    "heures_recherche_stage",
    "temps_linkedin"
]

avg_values = df[activities].mean()

fig1, ax1 = plt.subplots()
avg_values.plot(kind="bar", ax=ax1)
ax1.set_title("Temps moyen par activité")
ax1.set_ylabel("Heures moyennes")
ax1.set_xlabel("Activités")
plt.xticks(rotation=45)
st.pyplot(fig1)

# 2. Distribution des candidatures
st.subheader("Distribution des candidatures envoyées")
fig2, ax2 = plt.subplots()
ax2.hist(df["candidatures_envoyees"], bins=20)
ax2.set_title("Distribution des candidatures envoyées")
ax2.set_xlabel("Nombre de candidatures")
ax2.set_ylabel("Fréquence")
st.pyplot(fig2)

# 3. Candidatures vs entretiens
st.subheader("Candidatures envoyées vs entretiens obtenus")
fig3, ax3 = plt.subplots()
ax3.scatter(df["candidatures_envoyees"], df["entretiens"])
ax3.set_title("Candidatures vs Entretiens")
ax3.set_xlabel("Candidatures envoyées")
ax3.set_ylabel("Entretiens obtenus")
st.pyplot(fig3)

# 4. Top 10 étudiants les plus débordés
st.subheader("Top 10 étudiants les plus débordés")
top10 = df.sort_values("charge_totale", ascending=False).head(10)

fig4, ax4 = plt.subplots()
ax4.bar(top10["etudiant"], top10["charge_totale"])
ax4.set_title("Top 10 étudiants les plus débordés")
ax4.set_xlabel("Étudiants")
ax4.set_ylabel("Charge totale")
plt.xticks(rotation=45)
st.pyplot(fig4)

# 5. Répartition des entretiens
st.subheader("Répartition des entretiens")
interviews = df["entretiens"].value_counts().sort_index()

fig5, ax5 = plt.subplots()
ax5.pie(interviews, labels=interviews.index, autopct="%1.1f%%")
ax5.set_title("Répartition des entretiens")
st.pyplot(fig5)

# 6. Comparaison recherche stage / école / certification
st.subheader("Comparaison du temps moyen")
compare_cols = [
    "heures_recherche_stage",
    "heures_ecole",
    "heures_certification"
]

compare_means = df[compare_cols].mean()

fig6, ax6 = plt.subplots()
compare_means.plot(kind="bar", ax=ax6)
ax6.set_title("Comparaison temps moyen")
ax6.set_ylabel("Heures")
ax6.set_xlabel("Activités")
plt.xticks(rotation=0)
st.pyplot(fig6)