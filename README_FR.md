# Roblox Game Suite — Guide français

Suite de **vrais Agent Skills indépendants**, dans un seul dépôt. Chaque agent sélectionne un spécialiste selon sa tâche et charge uniquement ses références utiles.

## Installation

```bash
npx skills add SimonMedy/roblox-game-suite --skill '*'
```

Tu peux aussi sélectionner un seul skill (`--skill roblox-asset-workflow`, par exemple). Node.js et un agent compatible sont nécessaires. Blender/MCP/Roblox Studio s'installent séparément.

## Compétences disponibles

- **`roblox-game-director`** : planifie une première expérience jouable, coordonne les livrables et demande des preuves de qualité.
- **`roblox-asset-workflow`** : reprend l'expertise v3.2.0 du dépôt artistique (Blender, modèles, véhicules, cosmétiques, raretés, UV et audits).
- **`roblox-vfx-audio`** : VFX natifs, sprites et flipbooks, effets de boost, SFX et intégration.

Aucun faux skill gameplay ou UI n'a été créé. Le développement Luau, la sécurité réseau et les tests multijoueurs restent des exigences à traiter avec un outil/agent capable et à valider en jeu. Nous ajouterons les spécialistes correspondants à partir de vrais parcours de développement.

## Règle de production

Ne confonds jamais image conceptuelle, prototype Blender, asset importé et fonctionnalité Roblox finie. Construis **une vertical slice jouable**, mesure dans Studio / sur les clients pertinents et distingue les tests `PASS`, `FAIL`, `UNVERIFIED`. Les contenus artistiques ne doivent pas modifier la physique ou les hitboxes existantes sans autorisation.

## Gestion du dépôt

`develop` est l'unique branche de travail permanente. Les modifications sont revues via PR vers `main` ; une CI valide la structure, les scripts et les tests. La suite contient une copie autonome du skill artistique v3.2.0, avec provenance explicite ; sa synchronisation avec le dépôt original demande un contrôle lors des mises à jour.

```bash
python scripts/validate_suite.py
python -m unittest discover -s tests -v
```

Ce sont des vérifications du package, pas la preuve que le jeu fonctionne en Roblox Studio ou que tous les agents découvrent les skills automatiquement.
