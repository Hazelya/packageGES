import pandas as pd
import os


def calcul_emission(mode, distance_km):
    """
    Récupère est calcul le carbon émis d'un véhicule en particulier
    :param mode:
    :param distance_km:
    :return:
    """
    try:
        # Récupère le chemin du fichier Excel
        # os.path.dirname(__file__) => "chemin/vers/packageGES"
        file_path = os.path.join(os.path.dirname(__file__), "data", "impactCarbone.xlsx")

        # Lire le fichier Excel
        df = pd.read_excel(file_path)

        # Récupérer les émissions
        emission = df.loc[df['mode_transport'] == mode, 'emission_avec_constrution']
        emission_sans_construction = df.loc[df['mode_transport'] == mode, 'emission_sans_construction']

        if not emission.empty:
            emission_km = int(emission.values[0]) * distance_km
            pourcentage_sans_construction = (int(emission_sans_construction.values[0]) * distance_km) * 100 / emission_km
            return emission_km, pourcentage_sans_construction # divisé par mille pour passer en kg
        else:
            print(f"Erreur pour le mode {mode} : non trouvé dans le fichier.")
            return None
    except Exception as e:
        print(f"Erreur avec le fichier excel : {e}")
        return None




def calcul_prix(distance_km, mode):
    """
    Calcul le prix du trajet
    :param distance_km:
    :param mode:
    :return:
    """
    try:
        # Récupère le chemin du fichier Excel
        # os.path.dirname(__file__) => "chemin/vers/packageGES"
        file_path = os.path.join(os.path.dirname(__file__), "data", "impactCarbone.xlsx")
        # Lire le fichier Excel
        df = pd.read_excel(file_path)

        # Récupérer le prix par km
        prix_km = df.loc[df['mode_transport'] == mode, 'prix']

        if not prix_km.empty: # si on récupère bien un prix
            return float(prix_km.values[0]) * distance_km # * le nombre de km du trajet
        else:
            print(f"Erreur pour le mode {mode} : non trouvé dans le fichier.")
            return None
    except Exception as e:
        print(f"Erreur avec le fichier excel : {e}")
        return None




def calcul_temps(distance_km, mode):
    """
    Calcul le temps de trajet
    :param distance_km:
    :param mode:
    :return:
    """
    try:
        # Récupère le chemin du fichier Excel
        # os.path.dirname(__file__) => "chemin/vers/packageGES"
        file_path = os.path.join(os.path.dirname(__file__), "data", "impactCarbone.xlsx")
        # Lire le fichier Excel
        df = pd.read_excel(file_path)

        # Récupérer la vitesse
        vitesse_km = df.loc[df['mode_transport'] == mode, 'vitesse']

        if not vitesse_km.empty: # si on a une vitesse
            heure_decimal = distance_km / int(vitesse_km.values[0])

            # conversion heure et minutes
            heures = int(heure_decimal)
            minutes = round((heure_decimal - heures) * 60)
            return f"{heures}h{minutes:02d}" # minutes:02d si minutes < 10 on met un zero devant 02 sinon juste 12
        else:
            print(f"Erreur pour le mode {mode} : non trouvé dans le fichier.")
            return None
    except Exception as e:
        print(f"Erreur avec le fichier excel : {e}")
        return None
