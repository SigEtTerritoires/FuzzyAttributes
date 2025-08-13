
# FuzzyAttributes QGIS Plugin

![version](https://img.shields.io/badge/version-1.0.0-blue)
![QGIS](https://img.shields.io/badge/QGIS-3.28%2B-green)
![license](https://img.shields.io/badge/license-GPL--3.0-blue)
![status](https://img.shields.io/badge/status-active-brightgreen)

## Description

**FR :**  
FuzzyAttributes est un plugin QGIS qui permet de convertir des attributs numériques ou catégoriels en **valeurs floues** (degrés d’appartenance entre 0 et 1) à l’aide de fonctions d’appartenance courantes (linéaire croissante/décroissante, triangulaire, trapézoïdale, sigmoïde S et Z, gaussienne).
  
Il offre également la possibilité d’agréger plusieurs critères flous avec des fonctions personnalisables, tout en intégrant une interface graphique conviviale, des exemples visuels et une aide intégrée multilingue.

**Mode d’emploi complet** : [Guide utilisateur FuzzyAttributes](https://www.sigterritoires.fr/index.php/fuzzyattributes/)

---

**EN :**  
FuzzyAttributes is a QGIS plugin that converts numeric or categorical attributes into **fuzzy values** (membership degrees between 0 and 1) using common membership functions (increasing/decreasing linear, triangular, trapezoidal, sigmoid S and Z, Gaussian).  

It also allows aggregation of multiple fuzzy criteria with customizable functions, featuring a user-friendly interface, visual examples, and built-in multilingual help.

**Complete user guide**: [FuzzyAttributes User Guide](https://www.sigterritoires.fr/index.php/en/fuzzyattributesen/)

---

**ES:**  
FuzzyAttributes es un complemento de QGIS que permite convertir atributos numéricos o categóricos en **valores difusos** (grados de pertenencia entre 0 y 1) utilizando funciones de pertenencia comunes (lineal ascendente/descendente, triangular, trapezoidal, sigmoide S y Z, gaussiana).
  
También ofrece la posibilidad de agregar varios criterios difusos con funciones personalizables, al tiempo que integra una interfaz gráfica fácil de usar, ejemplos visuales y ayuda integrada en varios idiomas.

**Instrucciones completas**: [Guía del usuario de FuzzyAttributes](https://www.sigterritoires.fr/index.php/es/fuzzyattributeses/)

---

**PT:**  
O FuzzyAttributes é um plugin do QGIS que permite converter atributos numéricos ou categóricos em **valores difusos** (graus de pertencimento entre 0 e 1) utilizando funções de pertencimento comuns (linear crescente/decrescente, triangular, trapezoidal, sigmoide S e Z, gaussiana). 
 
Ele também oferece a possibilidade de agregar vários critérios difusos com funções personalizáveis, além de integrar uma interface gráfica amigável, exemplos visuais e ajuda integrada multilíngue.

**Manual de instruções completo**: [Guia do usuário FuzzyAttributes](https://www.sigterritoires.fr/index.php/pt/fuzzyattributespt/)

---

## Features

- **Attribute Fuzzification** – Transform numerical fields into fuzzy membership values using common functions.
- **Visual Guidance** – See example graphs for each membership function type.
- **Spatial Aggregation** – Combine fuzzy layers using intersection or union.
- **Decision-Based Aggregation** – Build or select a custom fuzzy aggregation function through a guided process.
- **Metadata Logging** – Record transformation parameters, sources, and user info in a GeoPackage table.
- **Multilingual Support** – English, French, Spanish, Portuguese (extensible).

---

## Installation

1. **Download or Clone** this repository:
   ```bash
   git clone https://github.com/SigEtTerritoires/FuzzyAttributes.git
````

2. Copy the plugin folder to your QGIS plugin directory:

   * **Windows**: `%APPDATA%/QGIS/QGIS3/profiles/default/python/plugins/`
   * **Linux/macOS**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
3. Restart QGIS.
4. Enable the plugin in the **Plugin Manager**.

---

## Usage

1. **Fuzzy Transformation**
   Menu: **FuzzyAttributes > Transformation floue**

   * Select a layer and a field.
   * Choose a fuzzy function type.
   * Enter parameters and apply.
     ![Fuzzy transformation dialog](https://raw.githubusercontent.com/SigEtTerritoires/FuzzyAttributes/tree/main/resources/images/attributs.jpg)


2. **Fuzzy Aggregation**
   Menu: **FuzzyAttributes > Agrégation floue**

   * Select two fuzzy layers.
   * Choose intersection or union.
   * Define or select an aggregation function.
     ![Fuzzy aggregation dialog](https://raw.githubusercontent.com/SigEtTerritoires/FuzzyAttributes/tree/main/resources/images/aggregation.jpg)


---

### About Fuzzy Aggregation Functions

The plugin includes **50 predefined aggregation functions** covering balanced and symmetrical cases.
For complex situations (criteria with **unequal weights** or **asymmetric judgments**), a generalized function can be generated using projection/interpolation methods to ensure both logical and mathematical consistency.

---

## Plugin Menu Structure

* **FuzzyAttributes** – Fuzzy transformation dialog.
* **Agrégation floue** – Spatial aggregation with fuzzy logic.

---

## Configuration

* Input layers should be from a **GeoPackage** to enable direct writing.
* Translations are stored in `i18n/` (compiled `.qm` files).

---

## Development

UI files (`.ui`) are compiled with:

```bash
pyuic5 -o ui_fuzzyattributes_dialog.py fuzzyattributes_dialog.ui
pyuic5 -o ui_aggregation_function_dialog.py aggregation_function_dialog.ui
```

---

## Metadata Table

All transformations and aggregations are logged in the `metafuzzy` table of the target GeoPackage, including:

* Field name
* Function code & parameters
* Source layers and fields
* Timestamp and user

---

## License

This plugin is released under the [GNU GPL-3.0 License](LICENSE).

---

## Contributing

Issues and pull requests are welcome:
[https://github.com/SigEtTerritoires/FuzzyAttributes](https://github.com/SigEtTerritoires/FuzzyAttributes)
