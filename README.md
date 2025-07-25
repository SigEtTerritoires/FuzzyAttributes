# FuzzyAttributes QGIS Plugin

## Description

`FuzzyAttributes` is a QGIS plugin for applying fuzzy logic transformations and aggregations to attribute data. It allows you to define fuzzy membership functions, combine fuzzy criteria spatially (intersection or union), and customize aggregation functions based on decision-maker preferences.

## Features

* **Attribute Fuzzification**: Transform numerical fields into fuzzy membership values using common fuzzy functions (linear, triangular, trapezoidal, sigmoidal, Gaussian).
* **Spatial Aggregation**: Combine two fuzzy attribute layers using intersection or union operations.
* **Decision-Based Aggregation**: Guide users through a three-question process to select or generate a custom fuzzy aggregation function.
* **Metadata Logging**: Automatically record transformation parameters, sources, and user information in a GeoPackage metadata table.
* **Multilingual**: Supports English, French, Spanish, Portuguese (additional translations can be added).

## Installation

1. **Clone or Download** this repository:

   ```bash
   git clone https://github.com/SigEtTerritoires/FuzzyAttributes.git
   ```
2. **Zip the plugin folder** if required by the QGIS plugin installer, or copy the folder directly to your QGIS plugin directory:

   * **Windows**: `%APPDATA%/QGIS/QGIS3/profiles/default/python/plugins/`
   * **Linux/MacOS**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
3. **Restart QGIS**.
4. **Enable the plugin** in the QGIS Plugin Manager.

## Usage

1. **Fuzzy Transformation**: Under menu **FuzzyAttributes > Transformation floue**, select a layer, a field, and a fuzzy function type. Enter parameters and apply.
![Fuzzy transformation dialog](resources/images/attributs.jpg)

2. **Fuzzy Aggregation**: Under menu **FuzzyAttributes > Agrégation floue**, choose two fuzzy layers, select intersection or union, define or select an aggregation function, and run. The result is saved in the same GeoPackage and added to the project.
![Fuzzy aggregation dialog](resources/images/aggregation.jpg)

### Fuzzy aggregation function

The plugin offers a flexible and intuitive method for constructing a **fuzzy aggregation function** from a combination of qualitative criteria. The user expresses his evaluation by means of classic linguistic judgments - *Very good, Good, Average, Mediocre, Very bad* - on 3 or 4 criteria. Each combination of “natural” responses, i.e. balanced and symmetrical, corresponds directly to one of the plugin's **50 predefined functions**.

However, in more complex situations - such as when criteria have **unequal weight**, or responses are **asymmetrical or atypical** - it becomes necessary to go beyond the 50 basic functions. The plugin then offers a **generalization based on an underlying mathematical model**: a projection or interpolation method is used to build a customized aggregation function, close to the behavior expected by the user, while remaining consistent within the framework of fuzzy analysis.

This approach makes it possible to integrate nuanced, non-standard human judgments into a fuzzy analysis process, while ensuring logical continuity and mathematical validity of the aggregation function used.
## Plugin Menus

* **FuzzyAttributes**: Main fuzzy transformation dialog.
* **Agrégation floue**: Spatial aggregation with fuzzy logic.

## Configuration

* Ensure your input layers are from a GeoPackage to support direct output writing.
* Translations are stored in the `i18n` folder. Place compiled `.qm` files there for additional languages.

## Development

* UI files (`.ui`) are located in the root. Use `pyuic5` to compile:

  ```bash
  pyuic5 -o ui_fuzzyattributes_dialog.py fuzzyattributes_dialog.ui
  pyuic5 -o ui_aggregation_function_dialog.py aggregation_function_dialog.ui
  ```
* Python logic resides in `fuzzyattributes_dialog.py` and `fuzzyaggregate_dialog.py`.

## Metadata

Transformation and aggregation metadata is logged in the `metafuzzy` table inside the target GeoPackage. It includes:

* Field name
* Function code
* Function parameters
* Source layers and fields
* Timestamp and user

## License

This plugin is released under the [MIT License](LICENSE).

## Contributing

Contributions welcome! Please submit issues or pull requests on the GitHub repository.
