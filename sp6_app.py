import streamlit as st
import datetime
import os
import textwrap

MISSIONS = [
    {
        "id": 1,
        "title": "Épisode 1 – Hangar et réseaux locaux industriels (RLI)",
        "description": "Tu conçois le réseau du nouveau hangar et découvres le rôle des réseaux locaux industriels.",
    },
    {
        "id": 2,
        "title": "Épisode 2 – Modbus, la langue des machines",
        "description": "Tu explores le protocole Modbus RTU/TCP entre automate, variateurs et moteurs.",
    },
    {
        "id": 3,
        "title": "Épisode 3 – Chat Bluetooth PC ↔ Raspberry Pi",
        "description": "Tu mets en place une messagerie simple entre un PC et un Raspberry Pi via Bluetooth.",
    },
    {
        "id": 4,
        "title": "Épisode 4 – I2C, capteur Si7021 et dashboard Node-RED",
        "description": "Tu utilises un capteur I2C pour mesurer température et humidité, et tu affiches les valeurs dans un tableau de bord.",
    },
]

QUESTIONS = {
    1: [
        "Dans tes mots : à quoi servent les machines du hangar (production, types de produits, etc.) ?",
        "Comment imagines-tu la connexion entre l'entreprise et le hangar (distance, type de liaison, câbles) ?",
        "Explique ce qu'est un réseau local industriel (RLI) et pourquoi on en a besoin dans une usine.",
    ],
    2: [
        "Que représente pour toi Modbus RTU et Modbus TCP ? Donne leurs grands rôles en industriel.",
        "Explique le principe maître / esclave avec un exemple simple (automate et variateur).",
        "Dans une trame Modbus, quels types d'informations importantes aimerais-tu repérer (adresse, fonction, données…) ?",
    ],
    3: [
        "À quoi sert selon toi le protocole Bluetooth dans une entreprise ou un projet technique ?",
        "Explique ce qu'est l'appareillage Bluetooth et pourquoi chaque équipement doit avoir une puce Bluetooth.",
        "Quelles idées de risques ou de précautions de sécurité t'inspirent le Bluetooth (authentification, visibilité, etc.) ?",
    ],
    4: [
        "Dans tes mots : qu'est-ce qu'une liaison série filaire et pourquoi I2C te semble adaptée à un capteur ?",
        "Explique ce que représentent SDA et SCL sur un bus I2C.",
        "Quelles grandeurs physiques un capteur comme le Si7021 peut mesurer et à quoi cela sert dans un local technique ?",
    ],
}

PROGRESS_DIR = os.path.expanduser(os.path.join("~", "SP6_progression_web"))
os.makedirs(PROGRESS_DIR, exist_ok=True)


def save_progress(username: str, mission_id: int, answers: list[str]) -> str:
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"web_SP6_{username}_episode{mission_id}_{now}.md"
    path = os.path.join(PROGRESS_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        mission = next(m for m in MISSIONS if m["id"] == mission_id)
        f.write(f"# {mission['title']}\n")
        f.write(textwrap.fill(mission["description"], width=80) + "\n\n")
        for i, (q, a) in enumerate(zip(QUESTIONS[mission_id], answers), start=1):
            f.write(f"## Question {i}\n")
            f.write(f"{q}\n\n")
            f.write(f"Réponse :\n{a}\n\n")
    return path


def list_progress_files(username: str) -> list[str]:
    files = []
    if not os.path.isdir(PROGRESS_DIR):
        return files
    for name in os.listdir(PROGRESS_DIR):
        if name.lower().startswith(f"web_sp6_{username.lower()}_"):
            files.append(name)
    return sorted(files)


def main():
    st.set_page_config(page_title="Cours interactif SP6 – BTS CIEL", page_icon="🎓", layout="wide")

    st.sidebar.title("Cours interactif SP6")
    username = st.sidebar.text_input("Ton prénom / pseudo", value="Gabriel")
    st.sidebar.write("Tes fichiers de progression seront stockés dans:")
    st.sidebar.code(PROGRESS_DIR)

    mission_titles = {m["title"]: m["id"] for m in MISSIONS}
    choice_title = st.sidebar.selectbox("Choisis un épisode", list(mission_titles.keys()))
    mission_id = mission_titles[choice_title]
    mission = next(m for m in MISSIONS if m["id"] == mission_id)

    st.title(mission["title"])
    st.markdown(textwrap.fill(mission["description"], width=80))

    st.subheader("Questions")
    answers: list[str] = []
    for i, q in enumerate(QUESTIONS[mission_id], start=1):
        st.markdown(f"**Question {i}**")
        st.write(q)
        default_key = f"answer_{mission_id}_{i}"
        a = st.text_area("Ta réponse", key=default_key, height=120)
        answers.append(a)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Enregistrer cet épisode"):
            path = save_progress(username, mission_id, answers)
            st.success(f"Progression enregistrée dans {path}")

    with col2:
        st.write("\n")
        st.write("\n")
        st.write("\n")

    st.sidebar.subheader("Tes épisodes enregistrés")
    files = list_progress_files(username)
    if files:
        for name in files:
            st.sidebar.text(f"- {name}")
    else:
        st.sidebar.text("Aucune progression enregistrée pour l'instant.")


if __name__ == "__main__":
    main()
