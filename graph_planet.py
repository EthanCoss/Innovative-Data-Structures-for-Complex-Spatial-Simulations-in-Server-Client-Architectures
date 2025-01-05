import matplotlib.pyplot as plt


# Fonction pour lire les données à partir d'un fichier texte
def lire_donnees(fichier):
    try:
        with open(fichier, "r") as f:
            # Convertir les lignes en une liste de nombres flottants
            return [float(ligne.strip()) for ligne in f]
    except FileNotFoundError:
        raise FileNotFoundError(f"Erreur : Le fichier {fichier} est introuvable.")
    except ValueError:
        raise ValueError(
            f"Erreur : Le fichier {fichier} contient des données non valides."
        )


def egaliser_listes(liste1, liste2):
    taille_min = min(len(liste1), len(liste2))
    return [liste1[:taille_min], liste2[:taille_min]]


base_fic = "save/trajectoires/"

planets = ["Terre", "Soleil", "Pluton", "Terre2", "Terre3", "Terre4", "Soleil2"]

colors = ["Blue", "Yellow", "Green", "Red", "Brown", "Black", "Orange"]

base_fic_planets = [base_fic + planet + "/" for planet in planets]
fics = [
    [base_fic_planet + "x.txt", base_fic_planet + "y.txt"]
    for base_fic_planet in base_fic_planets
]
data = []

for pla in fics:
    data.append(egaliser_listes(lire_donnees(pla[0]), lire_donnees(pla[1])))

# Vérification de la cohérence des données

# Création du scatter plot


for pla_ind in range(len(data)):
    plt.scatter(data[pla_ind][0], data[pla_ind][1], c=colors[pla_ind], label="Points")


plt.xlabel("Coordonnées X")
plt.ylabel("Coordonnées Y")
plt.title("Diagramme de dispersion des points")
plt.legend()
plt.grid(True)
plt.show()
