def reset_fichiers(fichier_x, fichier_y):
    try:
        with open(fichier_x, "w") as fx:
            fx.write("")
        with open(fichier_y, "w") as fy:
            fy.write("")
        print(f"Les fichiers {fichier_x} et {fichier_y} ont été réinitialisés.")
    except Exception as e:
        print(f"Erreur lors de la réinitialisation des fichiers : {e}")


base_fic = "trajectoires/"

planets = ["Terre", "Soleil", "Pluton", "Terre2", "Terre3", "Terre4", "Soleil2"]

colors = ["Blue", "Yellow", "Green", "Red", "Brown", "Black", "Orange"]

base_fic_planets = [base_fic + planet + "/" for planet in planets]
fics = [
    [base_fic_planet + "x.txt", base_fic_planet + "y.txt"]
    for base_fic_planet in base_fic_planets
]

for pla in fics:
    reset_fichiers(pla[0], pla[1])
