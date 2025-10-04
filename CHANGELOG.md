# Changelog  
Toutes les modifications notables du plugin **FuzzyAttributesV2** sont documentées ici.  

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)  
et ce projet suit approximativement le versionnage sémantique (SemVer).  

## [Unreleased]

---

## [2.1.0] - 2025-10-04  

### Ajouté
- **Nouveaux modules raster :**
  - 🟦 **FuzzyRaster** : applique une transformation floue sur les valeurs d’un raster monobande.
  - 🟩 **Raster Aggregation** : réalise l’agrégation floue de deux rasters avec fonctions d’agrégation paramétrables.
  - 🟨 **Classes → Fuzzy** : reclassifie un raster catégoriel selon une table de correspondance (CSV) pour obtenir un raster flou.  
- Génération automatique du nom de raster de sortie (`fzy_...`) avec gestion des conflits (écrasement ou renommage automatique).  
- Enregistrement des **métadonnées .fzy** associées aux rasters créés.  
- Support complet **Qt6 / PyQt6 / QGIS ≥ 3.38**.  
- Unification du système de traduction (FR, EN, ES, PT).  

### Modifié
- Menus réorganisés pour regrouper les outils flous **Vecteur** et **Raster**.  
- Harmonisation des dialogues et de la logique d’exécution des traitements raster/vecteur.  
- Interface utilisateur modernisée avec des contrôles cohérents entre les trois modules.  

### Corrigé
- Problèmes d’affichage liés à l’adaptation Qt6.  
- Gestion correcte des fichiers en écriture et des chemins relatifs sous Windows/Linux.  
- Nettoyage du code et suppression d’imports obsolètes.  

---

## [2.0.0] - 2025-09-16  

### Ajouté
- Compatibilité avec **Qt6** et **PyQt6**.  
- Mise à jour des imports PyQt pour Qt6.  
- Ajustements pour l’API Qt6 (widgets, signaux/slots).  

### Modifié
- Interface adaptée aux nouvelles conventions Qt6.  

### Corrigé
- Ajustements mineurs pour éviter les avertissements de dépréciation.  

---

## [1.4.0] - 2025-09-04  

### Ajouté
- Deux symbologies possibles pour la couche résultante : symbole gradué ou rampe de couleur.  
- Ajout d'une rampe “above and below”.  
- Option pour définir une symbologie par défaut (GeoPackage ou PostGIS).  

---

## [1.3.1] - 2025-08-31  

### Ajouté
- Transformation floue des attributs texte codés.  

### Corrigé
- Divers correctifs mineurs dans les dialogues.  

---

## [1.2.0] - 2025-08-26  

### Ajouté
- Gestion des données **PostGIS** comme fichiers source.  
- Validation des paramètres numériques des fonctions floues.  
- Affichage de la couche résultat avec une symbologie graduée.  

### Modifié
- Bouton *Annuler* remplacé par *Fermer* dans les dialogues.  
- Traductions mises à jour (FR, EN, ES, PT).  

### Corrigé
- Divers correctifs d’affichage et de logique interne.  

---

## [1.0.5] - 2025-08-27  

### Ajouté
- Symbologie graduée par défaut pour la couche résultante.  

---

## [1.0.2] - 2025-08-19  

### Ajouté
- Vérification de cohérence des fonctions d’agrégation floue :  
  - Avertissement en cas de combinaison incohérente.  
  - Possibilité de confirmer ou d’annuler le traitement.  

### Modifié
- Amélioration de la stabilité et de la compatibilité linguistique.  
- Mise à jour des traductions (FR, EN, ES, PT).  

### Corrigé
- Bug d’appel à `updateFunctionPreview()` corrigé.  

---

## [1.0.1] - 2025-08-13  

### Corrigé
- Affichage correct des images de fonctions floues dans toutes les langues.  
- Amélioration du mapping interne pour compatibilité avec les traductions.  

---

## [1.0.0] - 2025-08-10  

### Ajouté
- Première version publiée sur le dépôt QGIS.  
- Conversion d’attributs numériques en valeurs floues.  
- Fonctions d’appartenance : linéaire croissante, linéaire décroissante, triangulaire, trapézoïdale, sigmoïde (S/Z), gaussienne.  
