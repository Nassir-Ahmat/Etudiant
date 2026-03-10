import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# Configuration générale
# ------------------------------
st.set_page_config(page_title="Analyse des étudiants", layout="centered")

plt.rcParams.update({
    "font.size": 6,
    "axes.titlesize": 7,
    "axes.labelsize": 6,
    "xtick.labelsize": 5,
    "ytick.labelsize": 5,
    "legend.fontsize": 5
})

# ------------------------------
# Titre
# ------------------------------
st.title("Analyse de la charge des étudiants")

# ------------------------------
# Charger dataset
# ------------------------------
df = pd.read_csv("student.csv")

# ------------------------------
# Nouvelle métrique
# ------------------------------
df["charge_totale"] = (
    df["heures_transport"]
    + df["heures_ecole"]
    + df["heures_certification"]
    + df["heures_recherche_stage"]
    + df["temps_linkedin"]
)

# ------------------------------
# Aperçu données
# ------------------------------
st.subheader("Dataset")
st.dataframe(df.head())

# ------------------------------
# KPI
# ------------------------------
st.subheader("Indicateurs")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Recherche stage (h)", f"{df['heures_recherche_stage'].mean():.1f}")
c2.metric("Ecole (h)", f"{df['heures_ecole'].mean():.1f}")
c3.metric("Candidatures", f"{df['candidatures_envoyees'].mean():.0f}")
c4.metric("Entretiens", f"{df['entretiens'].mean():.1f}")

# ------------------------------
# 1 Temps moyen activité
# ------------------------------
st.subheader("Temps moyen par activité")

activities = [
    "heures_sommeil",
    "heures_transport",
    "heures_ecole",
    "heures_certification",
    "heures_recherche_stage",
    "temps_linkedin"
]

fig1, ax1 = plt.subplots(figsize=(3,2))
df[activities].mean().plot(kind="bar", ax=ax1)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig1)

# ------------------------------
# 2 Distribution candidatures
# ------------------------------
st.subheader("Distribution candidatures")

fig2, ax2 = plt.subplots(figsize=(3,2))
ax2.hist(df["candidatures_envoyees"], bins=20)
plt.tight_layout()
st.pyplot(fig2)

# ------------------------------
# 3 Scatter candidatures / entretiens
# ------------------------------
st.subheader("Candidatures vs Entretiens")

fig3, ax3 = plt.subplots(figsize=(3,2))
ax3.scatter(df["candidatures_envoyees"], df["entretiens"])
plt.tight_layout()
st.pyplot(fig3)

# ------------------------------
# 4 Top 10 étudiants débordés
# ------------------------------
st.subheader("Top 10 étudiants débordés")

top10 = df.sort_values("charge_totale", ascending=False).head(10)

fig4, ax4 = plt.subplots(figsize=(4,2))
ax4.bar(top10["etudiant"], top10["charge_totale"])
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig4)

# ------------------------------
# 5 Répartition entretiens
# ------------------------------
st.subheader("Répartition entretiens")

fig5, ax5 = plt.subplots(figsize=(2.5,2.5))
df["entretiens"].value_counts().plot.pie(ax=ax5, autopct="%1.1f%%")
plt.tight_layout()
st.pyplot(fig5)

# ------------------------------
# 6 Comparaison temps
# ------------------------------
st.subheader("Comparaison temps")

compare = [
    "heures_recherche_stage",
    "heures_ecole",
    "heures_certification"
]

fig6, ax6 = plt.subplots(figsize=(3,2))
df[compare].mean().plot(kind="bar", ax=ax6)
plt.tight_layout()
st.pyplot(fig6)