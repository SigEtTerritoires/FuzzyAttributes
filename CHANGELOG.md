# Changelog  
Toutes les modifications notables du plugin **FuzzyAttributes** seront documentées ici.  

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)  
et ce projet suit approximativement le versionnage sémantique (SemVer).  
## [Unreleased]
- Support du format postgis pour les données

---
## [1.0.5] - 2025-08-27 
### Ajouté
- Symbologie graduée par défaut de la couche résultante  

## [1.0.4] - 2025-08-19


### Corrigé
- Bug : Suppression du message QMessageBox pour éviter l'erreur UnboundLocalError
## [1.0.2] - 2025-08-19
### Ajouté
- Vérification de cohérence des fonctions d’agrégation :  
  - Avertissement en cas de combinaison incohérente.  
  - Possibilité de confirmer ou d’annuler le traitement.  

### Modifié
- Amélioration de la stabilité du lancement des agrégations.  
- Meilleure gestion des aperçus de fonctions floues (compatibilité langues).  
- Mise à jour des traductions en **français**, **anglais**, **espagnol**, **portugais**.  

### Corrigé
- Bug d’appel à `updateFunctionPreview()` corrigé.  
- Divers correctifs mineurs dans les dialogues.  

---

## [1.0.1] - 2025-08-13

### Corrigé
- affichage de l'image de la fonction floue dans toutes les langues.
- Amélioration du mapping interne pour compatibilité avec les traductions.
- Mise à jour de la documentation et images dans README.
---

## [1.0.0] - 2025-08-10
### Ajouté
- Première version publiée sur le dépôt QGIS.  
- Conversion d’attributs numériques en nombres flous.  
- Fonctions disponibles : linéaire croissante, linéaire décroissante, triangulaire, trapézoïdale,sigmoïde (S), sigmoïde inversée (Z), gaussienne.  
