import streamlit as st
import datetime
import os

# --- Configuration des missions / notions ---
MISSIONS = [
    {
        "id": 1,
        "title": "Mission 1 – Réseaux locaux industriels (RLI)",
        "emoji": "🏭",
        "summary": "Comprendre le rôle d'un réseau local industriel dans une usine et ses contraintes.",
        "resources": [
            ("Cours RLI – Abdelhamid Djeffal", "http://www.abdelhamid-djeffal.net/web_documents/polycope_rli_10.pdf"),
            ("Cours RLI – TVaira", "http://tvaira.free.fr/bts-sn/reseaux/cours/cours-rli.pdf"),
            ("Introduction aux RLI – Univ. Evry", "http://lsc.univ-evry.fr/~hoppenot/enseignement/cours/rli/introrli.pdf"),
        ],
    },
    {
        "id": 2,
        "title": "Mission 2 – Protocoles Modbus (RTU/TCP)",
        "emoji": "⚙️",
        "summary": "Voir Modbus comme une "langue" simple entre automate, capteurs et actionneurs.",
        "resources": [
            ("RLI & Modbus – Electronique-mixte", "https://www.electronique-mixte.fr/wp-content/uploads/2018/07/Formation-Interface-communication-28.pdf"),
        ],
    },
    {
        "id": 3,
        "title": "Mission 3 – Protocole Bluetooth",
        "emoji": "📡",
        "summary": "Comprendre Bluetooth comme chat sans fil sécurisé entre équipements proches.",
        "resources": [
            ("Cours Bluetooth CNED", "https://github.com/Gabawaru/bts-ciel-sp6-interactif"),
        ],
    },
    {
        "id": 4,
        "title": "Mission 4 – I2C et liaisons séries filaires", "emoji": "🔌",
        "summary": "Relier proprement capteurs et cartes en I2C/UART/SPI.",
        "resources": [
            ("Liaisons séries filaires (UART/I2C/SPI)", "https://example.com/liaisons-uart-i2c-spi"),
        ],
    },
    {
        "id": 5,
        "title": "Mission 5 – Protocoles LPWAN (LoRaWAN / Sigfox)",
        "emoji": "🌐",
        "summary": "Découvrir les réseaux longue portée très basse consommation pour l'IoT.",
        "resources": [
            ("Introduction LPWAN (LoRa & Sigfox) – Adafruit", "https://learn.adafruit.com/alltheiot-transports/lora-sigfox"),
            ("Introduction réseaux LPWA – Disk91", "https://www.disk91.com/wp-content/uploads/2018/11/IntroductionAuxReseauxLowPower-Sigfox.pdf"),
            ("Chapter 3: LPWAN – IoT Book", "https://pressbooks.bccampus.ca/iotbook/chapter/lpwan/"),
        ],
    },
]

PROGRESS_DIR = os.path.expanduser(os.path.join("~", "SP6_progression_web"))
os.makedirs(PROGRESS_DIR, exist_ok=True)

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "media", "audio")
VIDEO_DIR = os.path.join(os.path.dirname(__file__), "media", "video")
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)


def save_progress(username: str, mission_id: int, free_notes: str, answers: dict[str, str]) -> str:
    """Enregistre la séance dans un fichier Markdown dans un dossier dédié."""
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"web_SP6_{username}_mission{mission_id}_{now}.md"
    path = os.path.join(PROGRESS_DIR, filename)

    mission = next(m for m in MISSIONS if m["id"] == mission_id)

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {mission['title']}\n")
        f.write(f"Utilisateur : {username}\n")
        f.write(f"Date : {now}\n\n")

        f.write("## Notes libres\n")
        f.write(free_notes + "\n\n")

        f.write("## Questions guidées\n")
        for label, text in answers.items():
            f.write(f"### {label}\n")
            f.write(text + "\n\n")

    return path


def list_progress_files(username: str) -> list[str]:
    files: list[str] = []
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


def mission_audio_path(mission_id: int) -> str:
    """Construit le chemin attendu pour l'audio d'intro d'une mission."""
    return os.path.join(AUDIO_DIR, f"mission{mission_id}_intro.mp3")


def mission_video_path(mission_id: int) -> str:
    """Construit le chemin attendu pour la vidéo d'intro d'une mission."""
    return os.path.join(VIDEO_DIR, f"mission{mission_id}_intro.mp4")


def main() -> None:
    st.set_page_config(
        page_title="Cours SP6 – BTS CIEL",
        page_icon="🎧",
        layout="wide",
    )

    st.sidebar.title("Cours interactif SP6")
    username = st.sidebar.text_input("Ton prénom / pseudo", value="Gabriel")

    mission_labels = {f"{m['emoji']}  {m['title']}": m["id"] for m in MISSIONS}
    choice_label = st.sidebar.selectbox("Choisis une mission", list(mission_labels.keys()))
    mission_id = mission_labels[choice_label]
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

    st.markdown(
        f"<h2 style='margin-bottom:0'>{mission['emoji']}  {mission['title']}</h2>",
        unsafe_allow_html=True,
    )
    st.caption(mission["summary"])

    tab_cours, tab_travail, tab_history = st.tabs([
        "Cours / média",
        "Questions & notes",
        "Historique",
    ])

    # --- Onglet cours / média : audio + vidéo + ressources ---
    with tab_cours:
        st.markdown("### Présentation audio")
        audio_path = mission_audio_path(mission_id)
        if os.path.exists(audio_path):
            st.audio(audio_path, format="audio/mp3")
            st.info(
                "Tu écoutes ici l'introduction audio que tu as enregistrée ou déposée dans "
                f"`media/audio/mission{mission_id}_intro.mp3`."
            )
        else:
            st.warning(
                "Aucun fichier audio trouvé pour cette mission. "
                "Tu peux déposer ton propre MP3 dans le dossier `media/audio` avec le nom "
                f"`mission{mission_id}_intro.mp3`, ou enregistrer un audio via l'outil ci-dessous."
            )

        st.markdown("#### Enregistrer une courte présentation audio")
        audio_rec = st.audio_input("Enregistre ta voix (explication, résumé, story)")
        if audio_rec is not None:
            # Sauvegarde rapide de l'enregistrement pour réutilisation ultérieure
            rec_path = os.path.join(AUDIO_DIR, f"mission{mission_id}_record_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav")
            with open(rec_path, "wb") as f:
                f.write(audio_rec.getvalue())
            st.success(f"Enregistrement sauvegardé dans {rec_path}.")

        st.markdown("### Présentation vidéo (optionnel)")
        video_path = mission_video_path(mission_id)
        if os.path.exists(video_path):
            st.video(video_path, format="video/mp4")
            st.info(
                "Vidéo locale utilisée comme support de cours pour cette mission. "
                "Tu peux remplacer le fichier dans `media/video` pour mettre ta propre vidéo."
            )
        else:
            default_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # placeholder à remplacer
            st.video(default_url)
            st.warning(
                "Aucune vidéo locale n'a été trouvée. Un lien YouTube générique est affiché en exemple. "
                "Tu peux le remplacer dans le code par tes propres liens (tutos, présentations, etc.)."
            )

        st.markdown("### Ressources qui peuvent t'intéresser")
        for title, url in mission["resources"]:
            st.markdown(f"- [{title}]({url})")

    # --- Onglet travail : questions et notes ---
    with tab_travail:
        st.markdown("### Notes libres")
        free_notes = st.text_area(
            "Écris ton résumé, tes images mentales, tes questions, comme si tu racontais la mission à un ami.",
            height=180,
        )

        st.markdown("### Questions pour structurer ton cours")
        answers: dict[str, str] = {}

        if mission_id == 1:
            answers["Contexte du hangar"] = st.text_area(
                "Décris le contexte du hangar (machines, flux, enjeux).", height=120
            )
            answers["Définition RLI"] = st.text_area(
                "Dans tes mots : qu'est-ce qu'un réseau local industriel ?", height=120
            )
            answers["Contraintes industrielles"] = st.text_area(
                "Quelles contraintes particulières doit respecter un RLI (fiabilité, sécurité, robustesse) ?",
                height=120,
            )

        elif mission_id == 2:
            answers["Modbus comme langue"] = st.text_area(
                "Explique Modbus comme une langue simple entre automate et équipements.", height=120
            )
            answers["RTU vs TCP"] = st.text_area(
                "Dans tes mots : différence entre Modbus RTU et Modbus TCP.", height=120
            )
            answers["Trame Modbus"] = st.text_area(
                "Quels champs importants repères-tu dans une trame Modbus ?", height=120
            )

        elif mission_id == 3:
            answers["Bluetooth utilité"] = st.text_area(
                "À quoi sert Bluetooth dans un projet industriel ou perso (exemples concrets) ?", height=120
            )
            answers["Appareillage"] = st.text_area(
                "Explique l'appareillage en Bluetooth (découverte, association).", height=120
            )
            answers["Sécurité Bluetooth"] = st.text_area(
                "Quels risques et protections t'inspirent Bluetooth ?", height=120
            )

        elif mission_id == 4:
            answers["Liaisons séries"] = st.text_area(
                "Explique la différence entre UART, I2C et SPI (dans tes mots).", height=120
            )
            answers["Bus I2C"] = st.text_area(
                "Décris le bus I2C (SDA, SCL, maître/esclave) avec un exemple de capteur.", height=120
            )
            answers["Intégration capteur"] = st.text_area(
                "Comment imagines-tu l'intégration d'un capteur Si7021 dans une maquette Node-RED ?",
                height=120,
            )

        elif mission_id == 5:
            answers["Idée de LPWAN"] = st.text_area(
                "Dans tes mots : à quoi servent les réseaux LPWAN (LoRaWAN, Sigfox) ?", height=120
            )
            answers["Différences LoRaWAN/Sigfox"] = st.text_area(
                "Quelles différences importantes vois-tu entre LoRaWAN et Sigfox ?", height=120
            )
            answers["Cas d'usage"] = st.text_area(
                "Imagine un cas d'usage IoT concret où LPWAN serait pertinent (mesures, traçabilité...).", height=120
            )

        if st.button("💾 Enregistrer cette séance", type="primary"):
            path = save_progress(username, mission_id, free_notes, answers)
            st.success(f"Séance enregistrée dans : {path}")

    # --- Onglet historique ---
    with tab_history:
        st.markdown("### Lecture de tes séances enregistrées")
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
