# -*- coding: utf-8 -*-
"""
Convertit le fichier Excel des mesures de l'Avenir en commun en JSON
exploitable par le site (data/mesures.json).

Usage :
    python scripts/excel_to_json.py chemin/vers/avenir_en_commun_mesures.xlsx

Le script lit l'onglet "Mesures" et l'onglet "Filtres", et produit un JSON
avec la liste des mesures et leurs filtres associés (uniquement les filtres
marqués "oui" / "1" / "x" sont conservés dans le tableau `filtres`).
"""
import sys
import json
from pathlib import Path

import pandas as pd

FILTER_COLUMNS = {
    "Je suis jeune": "jeune",
    "Je suis féministe": "feministe",
    "Je suis républicain·e": "republicain",
    "Je soutiens les services publics": "services_publics",
    "Je suis rural·e": "rural",
}

TRUE_VALUES = {"oui", "yes", "1", "x", "true", "vrai"}


def is_true(value) -> bool:
    if pd.isna(value):
        return False
    return str(value).strip().lower() in TRUE_VALUES


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/excel_to_json.py chemin/vers/fichier.xlsx")
        sys.exit(1)

    xlsx_path = Path(sys.argv[1])
    df = pd.read_excel(xlsx_path, sheet_name="Mesures")

    mesures = []
    for _, row in df.iterrows():
        filtres = [slug for label, slug in FILTER_COLUMNS.items() if label in df.columns and is_true(row.get(label))]
        mesures.append({
            "id": row["ID"],
            "id_mesure_cle": row["ID mesure clé"],
            "axe": row["Axe (chapitre)"],
            "sous_theme": row["Sous-thème"],
            "titre": row["Titre (mesure clé)"],
            "texte": row["Texte complet (mesure)"],
            "page_pdf": int(row["Page PDF"]) if not pd.isna(row["Page PDF"]) else None,
            "filtres": filtres,
        })

    out_path = Path(__file__).resolve().parent.parent / "data" / "mesures.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(mesures, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(mesures)} mesures écrites dans {out_path}")


if __name__ == "__main__":
    main()
