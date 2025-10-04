# FuzzyAttributes V2 QGIS Plugin

![version](https://img.shields.io/badge/version-2.1.0-blue)  
![QGIS](https://img.shields.io/badge/QGIS-3.38%2B-green)  
![Qt](https://img.shields.io/badge/Qt-6.x-lightgrey)  
![license](https://img.shields.io/badge/license-GPL--3.0-blue)  
![status](https://img.shields.io/badge/status-active-brightgreen)

---

## 📑 Table of Contents

- [Description](#description)  
- [Features](#-features)  
- [Installation](#-installation)  
- [Usage Overview](#️-usage-overview)  
  - [1️⃣ Fuzzy Transformation (Vector)](#1️⃣-fuzzy-transformation-vector)  
  - [2️⃣ Text → Fuzzy Mapping](#2️⃣-text--fuzzy-mapping)  
  - [3️⃣ Vector Aggregation](#3️⃣-vector-aggregation)  
  - [4️⃣ Raster Fuzzification (New)](#4️⃣-raster-fuzzification-new)  
  - [5️⃣ Raster Aggregation (New)](#5️⃣-raster-aggregation-new)  
  - [6️⃣ Classes → Fuzzy (New)](#6️⃣-classes--fuzzy-new)  
- [About Fuzzy Aggregation Functions](#-about-fuzzy-aggregation-functions)  
- [File Outputs](#-file-outputs)  
- [Translations](#-translations)  
- [Development Notes](#-development-notes)  
- [License](#-license)  
- [Contributing](#-contributing)

---

## Description

**FR :**  
FuzzyAttributes est un plugin QGIS qui permet de convertir des **attributs ou rasters** en **valeurs floues** (degrés d’appartenance entre 0 et 1) à l’aide de fonctions d’appartenance classiques : linéaire croissante/décroissante, triangulaire, trapézoïdale, sigmoïde S et Z, gaussienne.
FuzzyAttributes  ajoute des outils orientés raster pour la fuzzification, l'agrégation et la reclassification des classes.
Nouveaux modules raster :
- 🔹 **Fuzzy Raster** : transformation floue d’un raster numérique monobande.  
- 🔸 **Raster Aggregation** : agrégation floue de deux rasters avec fonctions paramétrables.  
- 🔶 **Classes → Fuzzy Raster** : reclassification d’un raster catégoriel depuis un CSV (mapping classe→valeur floue).

**Mode d’emploi complet** : [Guide utilisateur FuzzyAttributes](https://www.sigterritoires.fr/index.php/fuzzyattributes/)

---
**EN :**  

FuzzyAttributes is a QGIS plugin that converts **attributes or rasters** into **fuzzy values** (membership degrees between 0 and 1) using classic membership functions: linear increasing/decreasing, triangular, trapezoidal, sigmoid S and Z, Gaussian.
FuzzyAttributesV2 adds raster-oriented tools for fuzzification, aggregation and class reclassification.
New raster modules:
- 🔹 **Fuzzy Raster**: fuzzy transformation of a single-band digital raster.
- 🔸 **Raster Aggregation**: fuzzy aggregation of two rasters with configurable functions.  
- 🔶 **Classes → Fuzzy Raster**: reclassification of a categorical raster from a CSV (class→fuzzy value mapping).

**Complete user guide**: [FuzzyAttributes User Guide](https://www.sigterritoires.fr/index.php/en/fuzzyattributesen/)

---
** ES **

FuzzyAttributesV2 es un complemento de QGIS que permite convertir **atributos o rásteres** en **valores difusos** (grados de pertenencia entre 0 y 1) utilizando funciones de pertenencia clásicas: lineal creciente/decreciente, triangular, trapezoidal, sigmoide S y Z, gaussiana.
FuzzyAttributesV2 añade herramientas orientadas al ráster para la difuminación, la agregación y la reclasificación de clases.

Nuevos módulos ráster:
- 🔹 **Fuzzy Raster**: transformación difusa de un ráster digital monobanda.
- 🔸 **Raster Aggregation**: agregación difusa de dos rásteres con funciones configurables.  
- 🔶 **Classes → Fuzzy Raster**: reclasificación de un ráster categórico a partir de un CSV (mapeo clase→valor difuso).

**Instrucciones completas**: [Guía del usuario de FuzzyAttributes](https://www.sigterritoires.fr/index.php/es/fuzzyattributeses/)

---
** PT **

O FuzzyAttributes é um plugin do QGIS que permite converter atributos ou rasters em valores difusos (graus de pertencimento entre 0 e 1) utilizando funções de pertencimento clássicas: linear crescente/decrescente, triangular, trapezoidal, sigmoide S e Z, gaussiana.
O FuzzyAttributes adiciona ferramentas orientadas para raster para a difusão, agregação e reclassificação de classes.
Novos módulos raster:
- 🔹 **Fuzzy Raster**: transformação difusa de um raster digital monobanda.
- 🔸 **Raster Aggregation**: agregação difusa de dois rasters com funções configuráveis.  
- 🔶 **Classes → Fuzzy Raster**: reclassificação de um raster categórico a partir de um CSV (mapeamento classe→valor difuso).

**Manual de instruções completo**: [Guia do usuário FuzzyAttributes](https://www.sigterritoires.fr/index.php/pt/fuzzyattributespt/)

## 🧩 Features

- **Vector**
  - Numeric field fuzzification (lin/tri/trap/sigmoid/gaussian).
  - Text → fuzzy mapping table.
  - Fuzzy aggregation of multiple criteria (vector).

- **Raster**
  - Fuzzy transformation of single-band rasters.
  - Raster aggregation (two rasters) with reprojection/resampling/extent handling.
  - Classes → fuzzy: reclassify categorical raster using CSV.

- **General**
  - Visual function preview, help tooltips.
  - Automatic metadata `.fzy` generation.
  - Output symbology (graduated or color ramp).
  - Multilingual: FR / EN / ES / PT.
  - Compatible Qt5 & Qt6, QGIS ≥ 3.38.

---

## ⚙️ Installation

1. Clone or download:
```bash
git clone https://github.com/SigEtTerritoires/FuzzyAttributes.git
```

2. Copy the plugin folder to your QGIS plugin directory:
- **Windows:** `%APPDATA%/QGIS/QGIS3/profiles/default/python/plugins/`  
- **Linux/macOS:** `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`

3. Restart QGIS and enable *FuzzyAttributesV2* in **Plugins → Manage and Install Plugins**.

---

## 🖱️ Usage Overview

### 1️⃣ Fuzzy Transformation (Vector)
Menu: `FuzzyAttributes > Transformation floue`  
Sélection d’une couche vectorielle et d’un champ numérique → régler la fonction → appliquer.
     ![Fuzzy transformation dialog](https://raw.githubusercontent.com/SigEtTerritoires/FuzzyAttributes/main/resources/images/attributs.jpg)

### 2️⃣ Text → Fuzzy Mapping
Menu: `FuzzyAttributes > Texte vers flou`  
Charger valeurs uniques d’un champ texte, définir mapping `texte → [0..1]`, créer attribut flou.
     ![Fuzzy text mapping dialog](https://raw.githubusercontent.com/SigEtTerritoires/FuzzyAttributes/main/resources/images/text_fuzzy.jpg)


### 3️⃣ Vector Aggregation
Menu: `FuzzyAttributes > Agrégation floue`  
Choisir deux critères, définir la fonction d’agrégation, lancer l’agrégation.
     ![Fuzzy aggregation dialog](https://raw.githubusercontent.com/SigEtTerritoires/FuzzyAttributes/main/resources/images/aggregation.jpg)

     ![Fuzzy aggregation function dialog](https://raw.githubusercontent.com/SigEtTerritoires/FuzzyAttributes/main/resources/images/fzyaggr_fonction.jpg)

   * Sélectionnez un style pour la couche de sortie : dégradé ou  rampe de couleurs.
   * Sélectionnez pour appliquer ou non comme style par défaut  pour la base de données
   * La couche résultante s'affiche avec une symbologie dégradée basée sur l'attribut d'agrégation.
    ![Fuzzy aggregation layer](https://raw.githubusercontent.com/SigEtTerritoires/FuzzyAttributes/main/resources/images/resultat.jpg)

### 4️⃣ Raster Fuzzification (New)
Menu: `FuzzyRaster`  
Sélection d’un raster monobande → appliquer une fonction floue → créer un raster `fzy_<nom>.tif`.

### 5️⃣ Raster Aggregation (New)
Menu: `Raster Aggregation`  
Sélection de deux rasters → choisir CRS cible / résolution / étendue / méthode de rééchantillonnage → définir la fonction d’agrégation → produire raster de sortie.

### 6️⃣ Classes → Fuzzy (New)
Menu: `Classes vers flou`  
Charger mapping CSV `classe;fuzzy` → reclasser raster catégoriel → produire raster flou.

---

## 🧮 About Fuzzy Aggregation Functions

Le plugin inclut de nombreuses fonctions prédéfinies (symétriques et asymétriques) et un générateur pour créer une fonction à partir d’un code (ex. `221`, `4412`, ...). Les fonctions générées sont documentées dans `fuzzy_functions.py`.

---

## 📂 File Outputs

- Fichiers GeoTIFF (`.tif`) pour rasters de sortie.
- Fichiers métadonnées `.fzy` (format CSV/text) accompagnant les rasters générés.
- Si le fichier de sortie existe : dialogue pour écraser ou renommer automatiquement (`_1`, `_2`, ...).

---

## 🈳 Translations

Les sources de traduction (`.ts`) et les fichiers compilés (`.qm`) sont dans le dossier `i18n/`.

Mise à jour des fichiers `.ts` (pile Qt6 recommandée) :
```bash
pylupdate6 *.py *.ui -ts i18n/FuzzyAttributes_fr.ts i18n/FuzzyAttributes_en.ts i18n/FuzzyAttributes_es.ts i18n/FuzzyAttributes_pt.ts
```

Compiler les `.ts` en `.qm` :
```bash
lrelease i18n/FuzzyAttributes_fr.ts -qm i18n/FuzzyAttributes_fr.qm
# répéter pour les autres langues
```

---

## 🧑‍💻 Development Notes

### UI → Python (Qt6)
```bash
pyuic6 -o ui_fuzzyattributes_dialog.py fuzzyattributes_dialog.ui
pyuic6 -o ui_fuzzytext_dialog.py fuzzytext_dialog.ui
pyuic6 -o ui_aggregation_function_dialog.py aggregation_function_dialog.ui
```

### Bonnes pratiques internes
- Centraliser fonctions d’agrégation dans `fuzzy_functions.py`.
- Mettre la gestion raster (reprojection / alignement / lecture-écriture) dans `raster_processing.py`.
- Tester les reprojections avant calcul d’emprise commune (convertir extent de chaque raster dans le CRS cible).

---

## 🪪 License

Ce plugin est sous **GNU GPL v3.0** — voir le fichier `LICENSE`.

---

## 🤝 Contributing

Signaler issues / PRs :  
https://github.com/SigEtTerritoires/FuzzyAttributes/issues
