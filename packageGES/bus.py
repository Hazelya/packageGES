import json
import os

import networkx as nx
from geopy.distance import geodesic
from geopy.geocoders import Nominatim





def bus(adresse_depart, adresse_arrivee, type_script):

    file_path = os.path.join(os.path.dirname(__file__), "data", "Rtwisto.json")
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    graph = nx.Graph()
    infos = {}  # infos arrets
    noms_arrets = {}

    for ligne in data:
        stops = ligne["stops"]
        route_id = ligne["route_id"]
        poids_ligne = 1.0  # on définit un poids en fonction du type de ligne
        if route_id.startswith("T"):
            poids_ligne = 0.3
        elif route_id.isdigit():
            num_ligne = int(route_id)
            if num_ligne > 140:
                continue  # on ignore les lignes supérieures à 140
            elif num_ligne <= 12:
                poids_ligne = 1.0
            elif num_ligne >= 20:
                poids_ligne = 1.3
        else:
            continue  # ligne non reconnue, on ignore

        for i, stop in enumerate(stops):
            stop_id = stop["stop_id"]
            nom = stop["stop_name"]
            coord = (stop["stop_lat"], stop["stop_lon"])
            infos[stop_id] = {"nom": nom, "coord": coord}
            if nom not in noms_arrets:
                noms_arrets[nom] = []
            noms_arrets[nom].append(stop_id)
            if i > 0:
                prev_stop = stops[i - 1]
                prev_coord = (prev_stop["stop_lat"], prev_stop["stop_lon"])
                distance = geodesic(coord, prev_coord).km
                graph.add_edge(prev_stop["stop_id"], stop_id, weight=distance * poids_ligne, ligne=route_id)

    for arrets in noms_arrets.values():  # liens de marche entre arrêts proches
        for i, stop1 in enumerate(arrets):
            for stop2 in arrets[i + 1:]:
                distance_transfert = geodesic(infos[stop1]["coord"],
                                              infos[stop2]["coord"]).km  # distance entre les deux arrêts
                if distance_transfert < 0.5:  # moins de 500 mètres
                    graph.add_edge(stop1, stop2, weight=0.05, ligne="transfer")

    geolocator = Nominatim(user_agent="trajet_twisto")

    loc_depart = geolocator.geocode(adresse_depart, timeout=5)  # conversion  et timeout sinon il est pas content
    loc_arrivee = geolocator.geocode(adresse_arrivee, timeout=5)

    if not loc_depart or not loc_arrivee:
        exit("erreur de géocodage. impossible de trouver l'une des adresses.")
    coord_depart = (loc_depart.latitude, loc_depart.longitude)
    coord_arrivee = (loc_arrivee.latitude, loc_arrivee.longitude)

    # arrêt le plus proche du lieu de départ

    distance_min_dep = float("inf")

    for stop in infos:  # infos arrets
        distance = geodesic(coord_depart,
                            infos[stop]["coord"]).km  # calcul de la distance des donnes saisis de l'utilisateur
        if distance < distance_min_dep:  # on compare avec ce qu'on a dans le json
            distance_min_dep = distance
            stop_depart = stop  # on garde l'arrêt ayant la plus petite distance

    # même chose pour l'arrivé

    distance_min_arr = float("inf")
    for stop in infos:
        distance = geodesic(coord_arrivee,
                            infos[stop]["coord"]).km  # calcul de la distance des donnes saisis de l'utilisateur
        if distance < distance_min_arr:  # on compare avec ce qu'on a dans le json
            distance_min_arr = distance
            stop_arrivee = stop  # on garde l'arrêt ayant la plus petite distance

    try:
        chemin = nx.shortest_path(graph, stop_depart, stop_arrivee, weight="weight")
    except nx.NetworkXNoPath:
        print(f"Aucun chemin en bus trouvé entre {adresse_depart} et {adresse_arrivee}")
        return None
    except nx.NodeNotFound as e:
        print(f"Nœud non trouvé dans le graphe de bus : {e}")
        return None

    distance_totale = 0

    for u, v in zip(chemin, chemin[1:]):  # pour chaque tranche du chemin
        distance_totale += graph[u][v]["weight"]
    lignes = []
    changements = []
    ligne_actuelle = None

    for i in range(len(chemin) - 1):
        u = chemin[i]
        v = chemin[i + 1]  # l'arrêt suivant
        ligne = graph[u][v]["ligne"]  # recup ligne utilisée entre deux arrêts
        if ligne != "transfer":  # on ignore les transferts à pied
            if ligne_actuelle is None:
                ligne_actuelle = ligne  # on associe la ligne
                lignes.append(ligne)  # on enregistre la première ligne
            elif ligne != ligne_actuelle:
                changements.append(f"{infos[u]['nom']} : {ligne_actuelle} → {ligne}")
                ligne_actuelle = ligne  # on met à jour la ligne courante
                if ligne not in lignes:
                    lignes.append(ligne)  # on ajoute la nouvelle ligne


    if type_script == "calcul" :
        distance_bus = distance_totale
        distance_trajet = distance_totale + distance_min_dep + distance_min_arr # bus + à pied

        return distance_bus, distance_trajet, chemin
    else:
        return chemin, infos, coord_depart, coord_arrivee, stop_depart, stop_arrivee


