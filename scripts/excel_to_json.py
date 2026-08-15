# -*- coding: utf-8 -*-
"""
Convertit le fichier Excel des mesures de l'Avenir en commun en JSON
exploitable par le site :
  - data/mesures.json  : une entrée par mesure (puce), avec la liste des
    slugs de filtres qui s'y appliquent
  - data/filtres.json  : la liste des filtres disponibles (slug, libellé,
    groupe, description, nombre de mesures concernées)
 
Le script est générique : il lit la liste des filtres directement dans
l'onglet "Filtres" du classeur (colonnes Colonne / Nom du filtre / Groupe /
Description), donc il n'a pas besoin d'être modifié si des filtres sont
ajoutés, supprimés ou renommés dans l'Excel.
 
Usage :
    python scripts/excel_to_json.py chemin/vers/avenir_en_commun_mesures.xlsx
"""
import sys
import json
from pathlib import Path
 
import pandas as pd
 
TRUE_VALUES = {"oui", "yes", "1", "x", "true", "vrai", 1}
 
 
def is_true(value) -> bool:
    if pd.isna(value):
        return False
    if isinstance(value, (int, float)):
        return value == 1
    return str(value).strip().lower() in TRUE_VALUES
 
 
def slugify_column(col_key: str) -> str:
    """'filtre_jeune' -> 'jeune' (le préfixe filtre_ est optionnel dans l'Excel)."""
    return col_key[len("filtre_"):] if col_key.startswith("filtre_") else col_key
 
 
def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/excel_to_json.py chemin/vers/fichier.xlsx")
        sys.exit(1)
 
    xlsx_path = Path(sys.argv[1])
    df_mesures = pd.read_excel(xlsx_path, sheet_name="Mesures")
    df_filtres = pd.read_excel(xlsx_path, sheet_name="Filtres")
 
    # Colonne "Colonne" = nom de la colonne dans l'onglet Mesures (ex: filtre_jeune)
    # Colonne "Nom du filtre (affiché sur le site)" = libellé humain
    # Colonne "Groupe" = regroupement thématique (optionnel, "Autres" par défaut)
    # Colonne "Description / critère d'attribution" = description (optionnel)
    filtres_meta = []
    label_col = next(c for c in df_filtres.columns if "colonne" in c.lower())
    name_col = next(c for c in df_filtres.columns if "libellé" in c.lower() or "affiché" in c.lower() or "nom du filtre" in c.lower())
    group_col = next((c for c in df_filtres.columns if "groupe" in c.lower()), None)
    desc_col = next((c for c in df_filtres.columns if "description" in c.lower() or "critère" in c.lower()), None)
 
    label_to_slug = {}
    for _, row in df_filtres.iterrows():
        col_key = str(row[label_col]).strip()
        label = str(row[name_col]).strip()
        slug = slugify_column(col_key)
        label_to_slug[label] = slug
        filtres_meta.append({
            "slug": slug,
            "label": label,
            "groupe": str(row[group_col]).strip() if group_col and not pd.isna(row[group_col]) else "Autres",
            "description": str(row[desc_col]).strip() if desc_col and not pd.isna(row[desc_col]) else "",
        })
 
    # Colonnes de filtres réellement présentes dans l'onglet Mesures
    filter_columns_present = {label: slug for label, slug in label_to_slug.items() if label in df_mesures.columns}
 
    mesures = []
    counts = {slug: 0 for slug in label_to_slug.values()}
    for _, row in df_mesures.iterrows():
        filtres = [slug for label, slug in filter_columns_present.items() if is_true(row.get(label))]
        for slug in filtres:
            counts[slug] += 1
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
 
    for f in filtres_meta:
        f["nb_mesures"] = counts.get(f["slug"], 0)
 
    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
 
    mesures_path = data_dir / "mesures.json"
    mesures_path.write_text(json.dumps(mesures, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(mesures)} mesures écrites dans {mesures_path}")
 
    filtres_path = data_dir / "filtres.json"
    filtres_path.write_text(json.dumps(filtres_meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(filtres_meta)} filtres écrits dans {filtres_path}")
 
 
if __name__ == "__main__":
    main()