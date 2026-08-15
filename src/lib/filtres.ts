import filtresData from "../../data/filtres.json";

export interface Filtre {
  slug: string;
  label: string;
  groupe: string;
  description: string;
  nb_mesures: number;
}

// Généré par scripts/excel_to_json.py depuis l'onglet "Filtres" de l'Excel —
// ne pas éditer ce fichier à la main, régénérer data/filtres.json à la place.
export const FILTRES = filtresData as Filtre[];

export function getFiltreBySlug(slug: string): Filtre | undefined {
  return FILTRES.find((f) => f.slug === slug);
}
