import streamlit as st
import datetime
import os
import textwrap

# --- Configuration des episodes ---
MISSIONS = [
    {
        "id": 1,
        "title": "Épisode 1 – Hangar et réseaux locaux industriels (RLI)",
        "short": "Tu conçois le réseau du nouveau hangar et le relie à l'entreprise.",
        "emoji": "🏭",
    },
    {
        "id": 2,
        "title": "Épisode 2 – Modbus, la langue des machines",
        "short": "Tu fais parler automate, variateurs et moteurs en Modbus.",
        "emoji": "⚙️",
    },
    {
        "id": 3,
        "title": "Épisode 3 – Chat Bluetooth PC ↔ Raspberry Pi",
        "short": "Tu mets en place une messagerie simple entre PC et Raspberry.",
        "emoji": "📡",
    },
    {
        "id": 4,
        "title": "Épisode 4 – I2C, capteur Si7021 et dashboard Node-RED",
        "short": "Tu mesures température / humidité et les affiches dans un dashboard.",
        "emoji": "🌡️",
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


def save_progress(username: str, mission_id: int, notes: str, answers: list[str]) -> str:
    """Enregistre la séance dans un fichier Markdown stylé."""
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"web_SP6_{username}_episode{mission_id}_{now}.md"
    path = os.path.join(PROGRESS_DIR, filename)

    mission = next(m for m in MISSIONS if m["id"] == mission_id)

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {mission['title']}\n")
        f.write(f"Utilisateur : {username}\n")
        f.write(f"Date : {now}\n\n")
        f.write("## Notes libres\n")
        f.write(notes + "\n\n")

        f.write("## Questions guidées\n")
        for i, (q, a) in enumerate(zip(QUESTIONS[mission_id], answers), start=1):
            f.write(f"### Question {i}\n")
            f.write(q + "\n\n")
            f.write("Réponse :\n")
            f.write(a + "\n\n")

    return path


def list_progress_files(username: str) -> list[str]:
    files = []
    if not os.path.isdir(PROGRESS_DIR):
        return files
    for name in os.listdir(PROGRESS_DIR):
        if name.lower().startswith(f"web_sp6_{username.lower()}_"):
            files.append(name)
    return sorted(files)


def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return "Impossible de lire ce fichier."


def main() -> None:
    st.set_page_config(
        page_title="Cours SP6 – BTS CIEL",
        page_icon="🛠️",
        layout="wide",
    )

    # --- Barre latérale (profil / navigation) ---
    st.sidebar.title("Cours interactif SP6")
    username = st.sidebar.text_input("Ton prénom / pseudo", value="Gabriel")

    mission_titles = {f"{m['emoji']}  {m['title']}": m["id"] for m in MISSIONS}
    choice_title = st.sidebar.selectbox("Choisis un épisode", list(mission_titles.keys()))
    mission_id = mission_titles[choice_title]
    mission = next(m for m in MISSIONS if m["id"] == mission_id)

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Dossier de progression :**")
    st.sidebar.code(PROGRESS_DIR)

    files = list_progress_files(username)
    if files:
        st.sidebar.markdown("**Séances enregistrées :**")
        for name in files:
            st.sidebar.text(f"• {name}")
    else:
        st.sidebar.text("Aucune séance enregistrée pour l'instant.")

    # --- En-tête stylé ---
    st.markdown(
        f"<h2 style='margin-bottom:0'>{mission['emoji']}  {mission['title']}</h2>",
        unsafe_allow_html=True,
    )
    st.caption(textwrap.fill(mission["short"], width=80))

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### Esprit de l'épisode")
        st.write(
            "Cet écran est ton espace de travail : tu notes tes idées, tu réponds aux questions, "
            "et tu construis ta propre compréhension de la mission."
        )
    with col2:
        st.markdown("### Profil")
        st.write(f"Étudiant : **{username}**")
        st.write(f"Épisode sélectionné : **{mission['emoji']}**")

    # --- Onglets pour organiser la séance ---
    tab_questions, tab_notes, tab_history = st.tabs([
        "Questions guidées",
        "Notes libres",
        "Historique",
    ])

    # --- Onglet Notes libres ---
    with tab_notes:
        st.markdown("#### Zone de réflexion libre")
        default_notes_key = f"notes_episode_{mission_id}"
        notes = st.text_area(
            "Écris ce que tu veux : résumé, schémas en texte, idées de projets, TODO, etc.",
            key=default_notes_key,
            height=200,
        )

    # --- Onglet Questions guidées ---
    answers: list[str] = []
    with tab_questions:
        st.markdown("#### Questions pour structurer ta pensée")
        for i, q in enumerate(QUESTIONS[mission_id], start=1):
            st.markdown(f"**Question {i}**")
            st.write(q)
            default_key = f"answer_{mission_id}_{i}"
            a = st.text_area("Ta réponse", key=default_key, height=140)
            answers.append(a)

        if st.button("💾 Enregistrer cette séance", type="primary"):
            path = save_progress(username, mission_id, notes, answers)
            st.success(f"Séance enregistrée dans : {path}")

    # --- Onglet Historique ---
    with tab_history:
        st.markdown("#### Lecture de tes séances enregistrées")
        files = list_progress_files(username)
        if not files:
            st.info("Tu n'as pas encore enregistré de séance pour cet utilisateur.")
        else:
            selected = st.selectbox("Choisis un fichier à afficher", files)
            full_path = os.path.join(PROGRESS_DIR, selected)
            content = read_file(full_path)
            st.code(content)


if __name__ == "__main__":
    main()
