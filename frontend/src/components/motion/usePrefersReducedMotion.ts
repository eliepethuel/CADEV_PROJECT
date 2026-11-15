import { useSyncExternalStore } from "react";

const QUERY = "(prefers-reduced-motion: reduce)";

function subscribe(onChange: () => void) {
  const media = window.matchMedia(QUERY);
  media.addEventListener("change", onChange);
  return () => media.removeEventListener("change", onChange);
}

/**
 * Réglage système « réduire les animations ».
 *
 * Vaut `false` côté serveur et pendant l'hydratation, puis se met à jour : le premier rendu
 * du navigateur reste identique au HTML reçu, quel que soit le réglage de l'utilisateur.
 */
export function usePrefersReducedMotion(): boolean {
  return useSyncExternalStore(
    subscribe,
    () => window.matchMedia(QUERY).matches,
    () => false,
  );
}
