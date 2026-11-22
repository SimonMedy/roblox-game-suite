# Roblox Asset Workflow — copie intégrée v3.2.0

Compétence autonome de la suite pour la **création artistique d'assets Roblox** : Blender, véhicules, UV, skins, raretés, VFX et préparation audio. Les références spécialisées ne sont lues que lorsque la tâche le demande.

Installation depuis la suite :

```bash
npx skills add SimonMedy/roblox-game-suite --skill roblox-asset-workflow
```

Le dépôt autonome d'origine demeure disponible : `npx skills add SimonMedy/roblox-asset-workflow`.

Principes : créativité libre, conservation des parties validées, sauvegardes éditables, inspection du vrai GAME, limites par mesh et tests honnêtes. `EmissiveMaskContent` nécessite les autorisations appropriées ; `EmissiveStrength` et `EmissiveTint` sont scriptables pour un masque fixe. Le guide export applique `PASS / FAIL / UNVERIFIED` ; les tests Studio et mobile non exécutés restent `UNVERIFIED`.

Audits depuis le dossier du skill : `python scripts/validate_skill.py` puis `python -m unittest discover -s tests -v`. Blender et les MCP s'installent séparément.
