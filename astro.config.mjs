import { defineConfig } from "astro/config";

// Sur GitHub Actions, GITHUB_REPOSITORY vaut "proprietaire/nom-du-depot" :
// on en déduit automatiquement le "base" nécessaire pour un site de projet
// (https://proprietaire.github.io/nom-du-depot/), quel que soit le nom
// choisi pour le dépôt.
const isCI = process.env.GITHUB_ACTIONS === "true";
const owner = process.env.GITHUB_REPOSITORY_OWNER;
const repo = process.env.GITHUB_REPOSITORY?.split("/")[1];

export default defineConfig({
  site: isCI && owner && repo ? `https://${owner}.github.io/${repo}` : undefined,
  base: isCI && repo ? `/${repo}` : "/",
});
