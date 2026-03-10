import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.pyplot as plt

# ------------------------------
# 1. Charger le dataset
# ------------------------------

df = pd.read_csv("student.csv")

print("Dataset chargé")
print("Nombre de lignes :", df.shape[0])
print("Nombre de colonnes :", df.shape[1])

# ------------------------------
# 2. Création de nouvelles métriques
# ------------------------------

df["charge_totale"] = (
    df["heures_transport"]
    + df["heures_ecole"]
    + df["heures_certification"]
    + df["heures_recherche_stage"]
    + df["temps_linkedin"]
)

df["taux_entretien"] = df["entretiens"] / df["candidatures_envoyees"]

df["candidatures_par_entretien"] = df["candidatures_envoyees"] / (df["entretiens"] + 1)

# ------------------------------
# 3. Statistiques générales
# ------------------------------

print("\nSTATISTIQUES")
print(df.describe())

print("\nTemps moyen recherche stage :", round(df["heures_recherche_stage"].mean(),2))
print("Temps moyen école :", round(df["heures_ecole"].mean(),2))
print("Temps moyen certification :", round(df["heures_certification"].mean(),2))

print("Candidatures moyennes :", round(df["candidatures_envoyees"].mean(),2))
print("Entretiens moyens :", round(df["entretiens"].mean(),2))

# ------------------------------
# 4. Création dossier graphiques
# ------------------------------

if not os.path.exists("graphiques"):
    os.makedirs("graphiques")

# ------------------------------
# 5. Bar chart : temps moyen par activité
# ------------------------------

activities = [
    "heures_sommeil",
    "heures_transport",
    "heures_ecole",
    "heures_certification",
    "heures_recherche_stage",
    "temps_linkedin"
]

avg_values = df[activities].mean()

plt.figure(figsize=(10,6))
avg_values.plot(kind="bar")
plt.title("Temps moyen par activité")
plt.ylabel("Heures moyennes")
plt.xticks(rotation=45)

plt.savefig("graphiques/temps_moyen_activites.png")
plt.close()

# ------------------------------
# 6. Histogramme candidatures
# ------------------------------

plt.figure(figsize=(10,6))
plt.hist(df["candidatures_envoyees"], bins=20)
plt.title("Distribution des candidatures envoyées")
plt.xlabel("Nombre de candidatures")
plt.ylabel("Fréquence")

plt.savefig("graphiques/distribution_candidatures.png")
plt.close()

# ------------------------------
# 7. Scatter plot candidatures vs entretiens
# ------------------------------

plt.figure(figsize=(10,6))
plt.scatter(df["candidatures_envoyees"], df["entretiens"])

plt.title("Candidatures vs Entretiens")
plt.xlabel("Candidatures envoyées")
plt.ylabel("Entretiens obtenus")

plt.savefig("graphiques/candidatures_vs_entretiens.png")
plt.close()

# ------------------------------
# 8. Top 10 étudiants débordés
# ------------------------------

top10 = df.sort_values("charge_totale", ascending=False).head(10)

plt.figure(figsize=(10,6))
plt.bar(top10["etudiant"], top10["charge_totale"])

plt.title("Top 10 étudiants les plus débordés")
plt.xlabel("Etudiants")
plt.ylabel("Heures")

plt.xticks(rotation=45)

plt.savefig("graphiques/top10_etudiants_debordes.png")
plt.close()

# ------------------------------
# 9. Pie chart entretiens
# ------------------------------

interviews = df["entretiens"].value_counts()

plt.figure(figsize=(8,8))
plt.pie(interviews, labels=interviews.index, autopct="%1.1f%%")

plt.title("Répartition des entretiens")

plt.savefig("graphiques/repartition_entretiens.png")
plt.close()

# ------------------------------
# 10. Comparaison recherche stage / école / certification
# ------------------------------

compare_cols = [
    "heures_recherche_stage",
    "heures_ecole",
    "heures_certification"
]

compare_means = df[compare_cols].mean()

plt.figure(figsize=(8,6))
compare_means.plot(kind="bar")

plt.title("Comparaison temps moyen")
plt.ylabel("Heures")

plt.savefig("graphiques/comparaison_temps.png")
plt.close()

# ------------------------------
# 11. Sauvegarde dataset enrichi
# ------------------------------

df.to_csv("dataset_analyse.csv", index=False)

print("\nAnalyse terminée")
print("Les graphiques sont dans le dossier : graphiques/")