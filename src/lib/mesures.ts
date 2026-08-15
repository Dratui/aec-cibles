import mesuresData from "../../data/mesures.json";

export interface Mesure {
  id: string;
  id_mesure_cle: string;
  axe: string;
  sous_theme: string;
  titre: string;
  texte: string;
  page_pdf: number | null;
  filtres: string[];
}

export interface MesureGroupee {
  id_mesure_cle: string;
  axe: string;
  sous_theme: string;
  titre: string;
  textes: string[];
}

export const mesures = mesuresData as Mesure[];

export function getMesuresParFiltre(slug: string): Mesure[] {
  return mesures.filter((m) => m.filtres.includes(slug));
}

// Regroupe les mesures d'un même titre clé (colonne "Titre (mesure clé)") en
// un seul bloc, avec la liste des textes complets qui s'y rattachent.
export function getMesuresGroupeesParFiltre(slug: string): MesureGroupee[] {
  const groupes = new Map<string, MesureGroupee>();

  for (const m of getMesuresParFiltre(slug)) {
    let groupe = groupes.get(m.id_mesure_cle);
    if (!groupe) {
      groupe = {
        id_mesure_cle: m.id_mesure_cle,
        axe: m.axe,
        sous_theme: m.sous_theme,
        titre: m.titre,
        textes: [],
      };
      groupes.set(m.id_mesure_cle, groupe);
    }
    groupe.textes.push(m.texte);
  }

  return Array.from(groupes.values());
}
