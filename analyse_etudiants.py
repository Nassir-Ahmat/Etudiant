import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# CONFIGURATION
# =========================================================
st.set_page_config(page_title="Analyse de la charge des étudiants", layout="wide")

plt.rcParams.update({
    "font.size": 7,
    "axes.titlesize": 9,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7
})

# =========================================================
# CHARGEMENT DES DONNÉES
# =========================================================
@st.cache_data
def load_data():
    df = pd.read_csv("student.csv")
    return df

df = load_data()

# =========================================================
# CRÉATION DES VARIABLES DÉRIVÉES
# =========================================================
df["charge_totale"] = (
    df["heures_transport"]
    + df["heures_ecole"]
    + df["heures_certification"]
    + df["heures_recherche_stage"]
    + df["temps_linkedin"]
)

df["temps_hors_repos"] = (
    df["heures_transport"]
    + df["heures_ecole"]
    + df["heures_certification"]
    + df["heures_recherche_stage"]
    + df["temps_linkedin"]
)

df["ratio_recherche_ecole"] = df["heures_recherche_stage"] / (df["heures_ecole"] + 1)
df["ratio_recherche_certification"] = df["heures_recherche_stage"] / (df["heures_certification"] + 1)

df["taux_entretien"] = df["entretiens"] / df["candidatures_envoyees"]

df["candidatures_par_entretien"] = np.where(
    df["entretiens"] > 0,
    df["candidatures_envoyees"] / df["entretiens"],
    df["candidatures_envoyees"]
)

df["part_recherche_dans_charge"] = (
    df["heures_recherche_stage"] / df["temps_hors_repos"]
)

# =========================================================
# SEGMENTATION DES PROFILS
# =========================================================
conditions = [
    (df["candidatures_envoyees"] >= 120) & (df["entretiens"] == 0),
    (df["candidatures_envoyees"] >= 100) & (df["entretiens"] <= 1),
    (df["heures_recherche_stage"] >= 8) & (df["heures_ecole"] <= 2),
    (df["charge_totale"] >= 20)
]

labels = [
    "Très forte pression sans retour",
    "Beaucoup d'efforts, peu de retours",
    "Recherche stage > études",
    "Journée extrêmement chargée"
]

df["profil"] = "Autre"

for cond, label in zip(conditions, labels):
    df.loc[cond, "profil"] = label

# =========================================================
# SIDEBAR - FILTRES
# =========================================================
st.sidebar.title("Filtres")

min_cand = int(df["candidatures_envoyees"].min())
max_cand = int(df["candidatures_envoyees"].max())

cand_range = st.sidebar.slider(
    "Plage de candidatures envoyées",
    min_value=min_cand,
    max_value=max_cand,
    value=(min_cand, max_cand)
)

profil_options = ["Tous"] + sorted(df["profil"].unique().tolist())
profil_selected = st.sidebar.selectbox("Profil étudiant", profil_options)

min_entretien = int(df["entretiens"].min())
max_entretien = int(df["entretiens"].max())

entretien_range = st.sidebar.slider(
    "Plage d'entretiens",
    min_value=min_entretien,
    max_value=max_entretien,
    value=(min_entretien, max_entretien)
)

filtered_df = df[
    (df["candidatures_envoyees"] >= cand_range[0]) &
    (df["candidatures_envoyees"] <= cand_range[1]) &
    (df["entretiens"] >= entretien_range[0]) &
    (df["entretiens"] <= entretien_range[1])
]

if profil_selected != "Tous":
    filtered_df = filtered_df[filtered_df["profil"] == profil_selected]

# =========================================================
# TITRE
# =========================================================
st.title("Analyse de la pression étudiante face à la recherche de stage")
st.markdown(
    """
    Ce dashboard analyse la charge de travail des étudiants en comparant le temps consacré
    aux études, aux certifications et à la recherche de stage ou d'alternance.
    Il met aussi en évidence le déséquilibre entre l'effort fourni et les résultats obtenus.
    """
)

# =========================================================
# KPI PRINCIPAUX
# =========================================================
st.subheader("Indicateurs clés")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Étudiants analysés", filtered_df.shape[0])
col2.metric("Recherche stage moyenne", f"{filtered_df['heures_recherche_stage'].mean():.2f} h")
col3.metric("École moyenne", f"{filtered_df['heures_ecole'].mean():.2f} h")
col4.metric("Candidatures moyennes", f"{filtered_df['candidatures_envoyees'].mean():.2f}")
col5.metric("Entretiens moyens", f"{filtered_df['entretiens'].mean():.2f}")

col6, col7, col8, col9 = st.columns(4)

col6.metric("Charge totale moyenne", f"{filtered_df['charge_totale'].mean():.2f} h")
col7.metric("Taux moyen d'entretien", f"{filtered_df['taux_entretien'].mean() * 100:.2f}%")
col8.metric("Cand./entretien moyen", f"{filtered_df.loc[filtered_df['entretiens'] > 0, 'candidatures_par_entretien'].mean():.2f}")
col9.metric("Part recherche dans charge", f"{filtered_df['part_recherche_dans_charge'].mean() * 100:.2f}%")

# =========================================================
# APERÇU DES DONNÉES
# =========================================================
st.subheader("Aperçu des données")
st.dataframe(filtered_df.head(20), use_container_width=True)

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Vue générale",
    "Candidatures & entretiens",
    "Charge étudiante",
    "Profils",
    "Corrélations",
    "Statistiques"
])

# =========================================================
# TAB 1 - VUE GÉNÉRALE
# =========================================================
with tab1:
    st.markdown("### Temps moyen par activité")
    
    activities = [
        "heures_sommeil",
        "heures_transport",
        "heures_ecole",
        "heures_certification",
        "heures_recherche_stage",
        "temps_linkedin"
    ]
    
    fig1, ax1 = plt.subplots(figsize=(4.8, 2.8))
    filtered_df[activities].mean().plot(kind="bar", ax=ax1)
    ax1.set_title("Temps moyen par activité")
    ax1.set_ylabel("Heures")
    plt.xticks(rotation=30)
    plt.tight_layout()
    st.pyplot(fig1)

    st.markdown("### Comparaison recherche stage vs école vs certification")
    compare_cols = ["heures_recherche_stage", "heures_ecole", "heures_certification"]

    fig2, ax2 = plt.subplots(figsize=(4.5, 2.8))
    filtered_df[compare_cols].mean().plot(kind="bar", ax=ax2)
    ax2.set_title("Comparaison des temps moyens")
    ax2.set_ylabel("Heures")
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig2)

    st.markdown("### Lecture")
    st.write(
        f"En moyenne, les étudiants consacrent {filtered_df['heures_recherche_stage'].mean():.2f} heures à la recherche de stage, "
        f"contre {filtered_df['heures_ecole'].mean():.2f} heures pour l'école et "
        f"{filtered_df['heures_certification'].mean():.2f} heures pour les certifications."
    )

# =========================================================
# TAB 2 - CANDIDATURES & ENTRETIENS
# =========================================================
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### Distribution des candidatures")
        fig3, ax3 = plt.subplots(figsize=(4.8, 2.8))
        ax3.hist(filtered_df["candidatures_envoyees"], bins=20)
        ax3.set_title("Distribution des candidatures")
        ax3.set_xlabel("Candidatures envoyées")
        ax3.set_ylabel("Fréquence")
        plt.tight_layout()
        st.pyplot(fig3)

    with col_b:
        st.markdown("### Candidatures vs entretiens")
        fig4, ax4 = plt.subplots(figsize=(4.8, 2.8))
        ax4.scatter(filtered_df["candidatures_envoyees"], filtered_df["entretiens"])
        ax4.set_title("Candidatures vs entretiens")
        ax4.set_xlabel("Candidatures envoyées")
        ax4.set_ylabel("Entretiens")
        plt.tight_layout()
        st.pyplot(fig4)

    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("### Répartition des entretiens")
        interview_counts = filtered_df["entretiens"].value_counts().sort_index()
        fig5, ax5 = plt.subplots(figsize=(3.5, 3.2))
        ax5.pie(interview_counts, labels=interview_counts.index, autopct="%1.1f%%", textprops={"fontsize": 7})
        ax5.set_title("Répartition des entretiens")
        plt.tight_layout()
        st.pyplot(fig5)

    with col_d:
        st.markdown("### Taux d'entretien")
        fig6, ax6 = plt.subplots(figsize=(4.8, 2.8))
        ax6.hist(filtered_df["taux_entretien"], bins=15)
        ax6.set_title("Distribution du taux d'entretien")
        ax6.set_xlabel("Taux d'entretien")
        ax6.set_ylabel("Fréquence")
        plt.tight_layout()
        st.pyplot(fig6)

    st.markdown("### Résultats clés")
    pct_zero_entretien = (filtered_df["entretiens"] == 0).mean() * 100
    pct_plus_100 = (filtered_df["candidatures_envoyees"] > 100).mean() * 100

    st.write(f"- {pct_zero_entretien:.2f}% des étudiants n'obtiennent aucun entretien.")
    st.write(f"- {pct_plus_100:.2f}% des étudiants envoient plus de 100 candidatures.")
    st.write(
        f"- En moyenne, il faut {filtered_df.loc[filtered_df['entretiens'] > 0, 'candidatures_par_entretien'].mean():.2f} candidatures pour obtenir un entretien."
    )

# =========================================================
# TAB 3 - CHARGE ÉTUDIANTE
# =========================================================
with tab3:
    st.markdown("### Top 10 étudiants les plus débordés")
    top10 = filtered_df.sort_values("charge_totale", ascending=False).head(10)

    fig7, ax7 = plt.subplots(figsize=(6, 2.8))
    ax7.bar(top10["etudiant"], top10["charge_totale"])
    ax7.set_title("Top 10 des étudiants les plus débordés")
    ax7.set_xlabel("Étudiants")
    ax7.set_ylabel("Charge totale")
    plt.xticks(rotation=35)
    plt.tight_layout()
    st.pyplot(fig7)

    st.markdown("### Répartition de la charge totale")
    fig8, ax8 = plt.subplots(figsize=(4.8, 2.8))
    ax8.hist(filtered_df["charge_totale"], bins=15)
    ax8.set_title("Distribution de la charge totale")
    ax8.set_xlabel("Heures de charge totale")
    ax8.set_ylabel("Fréquence")
    plt.tight_layout()
    st.pyplot(fig8)

    st.markdown("### Ratios")
    col_r1, col_r2 = st.columns(2)

    with col_r1:
        fig9, ax9 = plt.subplots(figsize=(4.5, 2.8))
        ax9.hist(filtered_df["ratio_recherche_ecole"], bins=15)
        ax9.set_title("Ratio recherche / école")
        ax9.set_xlabel("Ratio")
        ax9.set_ylabel("Fréquence")
        plt.tight_layout()
        st.pyplot(fig9)

    with col_r2:
        fig10, ax10 = plt.subplots(figsize=(4.5, 2.8))
        ax10.hist(filtered_df["ratio_recherche_certification"], bins=15)
        ax10.set_title("Ratio recherche / certification")
        ax10.set_xlabel("Ratio")
        ax10.set_ylabel("Fréquence")
        plt.tight_layout()
        st.pyplot(fig10)

    pct_recherche_sup_ecole = (filtered_df["heures_recherche_stage"] > filtered_df["heures_ecole"]).mean() * 100
    pct_recherche_sup_certif = (filtered_df["heures_recherche_stage"] > filtered_df["heures_certification"]).mean() * 100

    st.write(f"- {pct_recherche_sup_ecole:.2f}% des étudiants passent plus de temps à chercher un stage qu'à aller à l'école.")
    st.write(f"- {pct_recherche_sup_certif:.2f}% des étudiants passent plus de temps à chercher un stage qu'à préparer des certifications.")

# =========================================================
# TAB 4 - PROFILS
# =========================================================
with tab4:
    st.markdown("### Répartition des profils")
    profil_counts = filtered_df["profil"].value_counts()

    fig11, ax11 = plt.subplots(figsize=(5.2, 2.8))
    profil_counts.plot(kind="bar", ax=ax11)
    ax11.set_title("Répartition des profils étudiants")
    ax11.set_ylabel("Nombre")
    plt.xticks(rotation=20)
    plt.tight_layout()
    st.pyplot(fig11)

    st.markdown("### Tableau des profils critiques")
    profils_critiques = filtered_df[
        filtered_df["profil"].isin([
            "Très forte pression sans retour",
            "Beaucoup d'efforts, peu de retours",
            "Journée extrêmement chargée"
        ])
    ][[
        "etudiant", "candidatures_envoyees", "entretiens",
        "heures_recherche_stage", "heures_ecole",
        "heures_certification", "charge_totale", "profil"
    ]]

    st.dataframe(profils_critiques, use_container_width=True)

# =========================================================
# TAB 5 - CORRÉLATIONS
# =========================================================
with tab5:
    st.markdown("### Matrice de corrélation")
    corr_cols = [
        "heures_sommeil",
        "heures_transport",
        "heures_ecole",
        "heures_certification",
        "heures_recherche_stage",
        "temps_linkedin",
        "candidatures_envoyees",
        "entretiens",
        "charge_totale"
    ]

    corr_matrix = filtered_df[corr_cols].corr()

    fig12, ax12 = plt.subplots(figsize=(7, 4))
    cax = ax12.matshow(corr_matrix, cmap="coolwarm")
    fig12.colorbar(cax)

    ax12.set_xticks(range(len(corr_cols)))
    ax12.set_yticks(range(len(corr_cols)))
    ax12.set_xticklabels(corr_cols, rotation=90)
    ax12.set_yticklabels(corr_cols)
    ax12.set_title("Matrice de corrélation", pad=20)
    plt.tight_layout()
    st.pyplot(fig12)

    st.markdown("### Corrélations numériques")
    st.dataframe(corr_matrix.round(2), use_container_width=True)

# =========================================================
# TAB 6 - STATISTIQUES
# =========================================================
with tab6:
    st.markdown("### Statistiques descriptives")
    stats_cols = [
        "heures_sommeil",
        "heures_transport",
        "heures_ecole",
        "heures_certification",
        "heures_recherche_stage",
        "temps_linkedin",
        "candidatures_envoyees",
        "entretiens",
        "charge_totale",
        "ratio_recherche_ecole",
        "ratio_recherche_certification",
        "taux_entretien",
        "candidatures_par_entretien"
    ]

    st.dataframe(filtered_df[stats_cols].describe().round(2), use_container_width=True)

    st.markdown("### Tableau récapitulatif")
    resume = pd.DataFrame({
        "indicateur": [
            "Temps moyen de recherche de stage",
            "Temps moyen d'école",
            "Temps moyen de certification",
            "Temps moyen LinkedIn",
            "Candidatures moyennes",
            "Entretiens moyens",
            "Taux moyen d'entretien",
            "Part des étudiants >100 candidatures",
            "Part des étudiants avec 0 entretien",
            "Part des étudiants recherche > école",
            "Part moyenne de la recherche dans la charge"
        ],
        "valeur": [
            round(filtered_df["heures_recherche_stage"].mean(), 2),
            round(filtered_df["heures_ecole"].mean(), 2),
            round(filtered_df["heures_certification"].mean(), 2),
            round(filtered_df["temps_linkedin"].mean(), 2),
            round(filtered_df["candidatures_envoyees"].mean(), 2),
            round(filtered_df["entretiens"].mean(), 2),
            f"{filtered_df['taux_entretien'].mean() * 100:.2f} %",
            f"{(filtered_df['candidatures_envoyees'] > 100).mean() * 100:.2f} %",
            f"{(filtered_df['entretiens'] == 0).mean() * 100:.2f} %",
            f"{(filtered_df['heures_recherche_stage'] > filtered_df['heures_ecole']).mean() * 100:.2f} %",
            f"{filtered_df['part_recherche_dans_charge'].mean() * 100:.2f} %"
        ]
    })

    st.dataframe(resume, use_container_width=True)

# =========================================================
# CONCLUSION
# =========================================================
st.subheader("Conclusion automatique")
st.write(
    f"L'analyse montre que les étudiants consacrent en moyenne {filtered_df['heures_recherche_stage'].mean():.2f} heures "
    f"à la recherche de stage contre {filtered_df['heures_ecole'].mean():.2f} heures à l'école. "
    f"Ils envoient en moyenne {filtered_df['candidatures_envoyees'].mean():.2f} candidatures pour seulement "
    f"{filtered_df['entretiens'].mean():.2f} entretiens. "
    f"Ces résultats mettent en évidence une forte pression liée à l'insertion professionnelle."
)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #5784c8;
    }
    </style>
    """,
    unsafe_allow_html=True
)