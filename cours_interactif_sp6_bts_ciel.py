#!/usr/bin/env python3

"""
Cours interactif pour la Situation professionnelle 6 du BTS CIEL (Bloc 2).
Indépendant de l'assistant : fonctionne en ligne de commande.

Fonctions principales :
- proposer des "épisodes" (missions) autour des RLI, Modbus, Bluetooth et I2C,
- poser les questions une par une,
- enregistrer les réponses dans un fichier texte/markdown pour révision.

Tu peux modifier le contenu des questions directement dans ce fichier si besoin.
"""

import datetime
import textwrap

MISSIONS = [
    {
        "id": 1,
        "title": "Épisode 1 – Hangar et réseaux locaux industriels (RLI)",
        "description": "Tu conçois le réseau du nouveau hangar et découvres le rôle des réseaux locaux industriels.",
        "levels": [
            {
                "name": "Niveau 1 – Comprendre",
                "questions": [
                    "Dans tes mots : à quoi servent les machines du hangar (production, types de produits, etc.) ?",
                    "Comment imagines-tu la connexion entre l'entreprise et le hangar (distance, type de liaison, câbles) ?",
                    "Explique ce qu'est un réseau local industriel (RLI) et pourquoi on en a besoin dans une usine.",
                ],
            },
            {
                "name": "Niveau 2 – Imaginer",
                "questions": [
                    "Imagine la scène : le directeur te demande d'assurer une connexion fiable entre le hangar et l'entreprise. Qu'est-ce que tu lui promets concrètement ?",
                    "Décris ton RLI comme un "système nerveux" du hangar : quels sont les "nerfs" et quel est le "cerveau" ?",
                ],
            },
            {
                "name": "Niveau 3 – Appliquer",
                "questions": [
                    "Propose un plan d'adressage IP simple pour quelques équipements du hangar (serveur, machines, caméras) sur un même sous-réseau.",
                    "Explique pourquoi tu réserverais certaines adresses pour la passerelle et le DNS dans ce plan.",
                ],
            },
        ],
    },
    {
        "id": 2,
        "title": "Épisode 2 – Modbus, la langue des machines",
        "description": "Tu explores le protocole Modbus RTU/TCP entre automate, variateurs et moteurs.",
        "levels": [
            {
                "name": "Niveau 1 – Comprendre",
                "questions": [
                    "Que représente pour toi Modbus RTU et Modbus TCP ? Donne leurs grands rôles en industriel.",
                    "Explique le principe maître / esclave avec un exemple simple (automate et variateur).",
                    "Dans une trame Modbus, quels types d'informations importantes aimerais-tu repérer (adresse, fonction, données…) ?",
                ],
            },
            {
                "name": "Niveau 2 – Imaginer",
                "questions": [
                    "Raconte une mini-histoire : l'automate est un coach qui surveille la fréquence et le courant du moteur via Modbus.",
                    "Imagine une trame Modbus comme une phrase : quels sont les "mots" (champs) et ce qu'ils disent ?",
                ],
            },
            {
                "name": "Niveau 3 – Appliquer",
                "questions": [
                    "Invente un exemple de trame Modbus (sans détail hexadécimal) et explique en français ce qu'elle ferait sur le moteur.",
                    "Décris en quelques lignes une simulation serveur/client Modbus TCP avec deux machines virtuelles (qui joue quel rôle, et quel est l'intérêt ?).",
                ],
            },
        ],
    },
    {
        "id": 3,
        "title": "Épisode 3 – Chat Bluetooth PC ↔ Raspberry Pi",
        "description": "Tu mets en place une messagerie simple entre un PC et un Raspberry Pi via Bluetooth.",
        "levels": [
            {
                "name": "Niveau 1 – Comprendre",
                "questions": [
                    "À quoi sert selon toi le protocole Bluetooth dans une entreprise ou un projet technique ?",
                    "Explique ce qu'est l'appareillage Bluetooth et pourquoi chaque équipement doit avoir une puce Bluetooth.",
                    "Quelles idées de risques ou de précautions de sécurité t'inspirent le Bluetooth (authentification, visibilité, etc.) ?",
                ],
            },
            {
                "name": "Niveau 2 – Imaginer",
                "questions": [
                    "Imagine que ton PC est un serveur de chat et ton Raspberry Pi un ami distant : décris leur conversation via Bluetooth.",
                    "Décris ce que tu verrais dans un outil d'analyse de trames pendant cet échange (sans détail technique, juste l'idée générale).",
                ],
            },
            {
                "name": "Niveau 3 – Appliquer",
                "questions": [
                    "Liste les grandes étapes pour mettre en place le chat : environnement Python sur PC, sur Pi, connexion Bluetooth, lancement des scripts.",
                    "Propose une organisation de ton projet (dossiers, fichiers) pour ce chat Bluetooth afin de pouvoir le réutiliser plus tard.",
                ],
            },
        ],
    },
    {
        "id": 4,
        "title": "Épisode 4 – I2C, capteur Si7021 et dashboard Node-RED",
        "description": "Tu utilises un capteur I2C pour mesurer température et humidité, et tu affiches les valeurs dans un tableau de bord.",
        "levels": [
            {
                "name": "Niveau 1 – Comprendre",
                "questions": [
                    "Dans tes mots : qu'est-ce qu'une liaison série filaire et pourquoi I2C te semble adaptée à un capteur ?",
                    "Explique ce que représentent SDA et SCL sur un bus I2C.",
                    "Quelles grandeurs physiques un capteur comme le Si7021 peut mesurer et à quoi cela sert dans un local technique ?",
                ],
            },
            {
                "name": "Niveau 2 – Imaginer",
                "questions": [
                    "Raconte une scène : ton Raspberry Pi interroge régulièrement le capteur pour savoir s'il fait bon et sec dans le local.",
                    "Imagine le tableau de bord Node-RED que tu aimerais voir (jauges, couleurs, fréquence de mise à jour…).",
                ],
            },
            {
                "name": "Niveau 3 – Appliquer",
                "questions": [
                    "Liste les étapes pour activer I2C sur le Raspberry Pi et détecter ton capteur sur le bus.",
                    "Décris le flow Node-RED que tu mettrais en place (nodes inject, exec, gauge) pour afficher température et humidité.",
                ],
            },
        ],
    },
]


def ask_input(prompt: str) -> str:
    print("\n" + textwrap.fill(prompt, width=80))
    return input("\nTa réponse : ")


def main():
    print("=== Cours interactif – Situation professionnelle 6 (BTS CIEL) ===")
    print("Ce programme est indépendant : il fonctionne en console, sans assistant.")

    student = input("\nTon prénom (par défaut : Gabriel) : ") or "Gabriel"
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"reponses_SP6_{student}_{now}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Cours interactif – Situation professionnelle 6\n")
        f.write(f"Étudiant : {student}\n")
        f.write(f"Date de la séance : {now}\n\n")

        while True:
            print("\n=== Choix de l'épisode ===")
            for mission in MISSIONS:
                print(f"{mission['id']}. {mission['title']}")
            print("0. Quitter")

            try:
                choice = int(input("\nSélectionne un numéro d'épisode : "))
            except ValueError:
                print("Choix invalide.")
                continue

            if choice == 0:
                print("\nFin du cours interactif. Tes réponses sont enregistrées dans :", filename)
                break

            mission = next((m for m in MISSIONS if m["id"] == choice), None)
            if mission is None:
                print("Numéro d'épisode invalide.")
                continue

            print(f"\n=== {mission['title']} ===")
            print(textwrap.fill(mission["description"], width=80))

            f.write(f"\n## {mission['title']}\n")
            f.write(textwrap.fill(mission["description"], width=80) + "\n\n")

            for level in mission["levels"]:
                print(f"\n--- {level['name']} ---")
                f.write(f"### {level['name']}\n")

                for i, q in enumerate(level["questions"], start=1):
                    answer = ask_input(f"[{level['name']}] Question {i} : {q}")
                    f.write(f"- Question {i} : {q}\n")
                    f.write(f"  Réponse : {answer}\n\n")

            print("\nÉpisode terminé. Tu peux choisir un autre épisode ou quitter.")


if __name__ == "__main__":
    main()
