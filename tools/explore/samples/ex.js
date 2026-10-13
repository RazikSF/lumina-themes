// Récupère les élèves d'une classe et calcule la moyenne
import { fetchJson } from "./api.js";

export async function moyenne(classe, coeff = 1) {
  const eleves = await fetchJson(`/classes/${classe}`);
  if (!eleves.length) return null;
  const total = eleves.reduce((s, e) => s + e.note * coeff, 0);
  console.log("élèves :", eleves.length, true);
  return Math.round((total / eleves.length) * 100) / 100;
}
