# Changelog  
All notable changes to the **FuzzyAttributesV2** QGIS plugin are documented here.  

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project roughly follows Semantic Versioning (SemVer).  

## [Unreleased]

---

## [2.1.0] - 2025-10-04  

### Added
- **New raster modules:**
  - 🟦 **FuzzyRaster** – applies fuzzy membership transformations to single-band raster values.  
  - 🟩 **Raster Aggregation** – performs fuzzy aggregation between two rasters using parameterized fuzzy operators.  
  - 🟨 **Classes → Fuzzy** – reclassifies a categorical raster using a CSV mapping table to produce fuzzy raster outputs.  
- Automatic output raster naming (`fzy_...`) with overwrite or rename-on-conflict handling.  
- Metadata `.fzy` file automatically generated for each fuzzy raster.  
- Full support for **Qt6 / PyQt6 / QGIS ≥ 3.38**.  
- Unified translation system (French, English, Spanish, Portuguese).  

### Changed
- Plugin menu reorganized: **Vector Fuzzy Tools** and **Raster Fuzzy Tools** grouped logically.  
- Unified dialog layouts and execution logic between raster and vector tools.  
- UI modernized with consistent look and field controls across all modules.  

### Fixed
- Display and execution issues related to Qt6 migration.  
- File writing and relative path handling under Windows/Linux.  
- Code cleanup and removal of deprecated imports.  

---

## [2.0.0] - 2025-09-16  

### Added
- Compatibility with **Qt6** and **PyQt6**.  
- Updated PyQt imports for Qt6 syntax.  
- Adjusted code for the Qt6 API (widgets, signals/slots).  

### Changed
- UI updated to follow Qt6 conventions.  

### Fixed
- Minor warnings and deprecation issues removed.  

---

## [1.4.0] - 2025-09-04  

### Added
- Two symbology options for the resulting layer: graduated symbol or color ramp.  
- Added an “above and below” color ramp.  
- Option to define a default symbology (GeoPackage or PostGIS).  

---

## [1.3.1] - 2025-08-31  

### Added
- Fuzzy transformation of text-coded attributes.  

### Fixed
- Minor UI and logic fixes in dialogs.  

---

## [1.2.0] - 2025-08-26  

### Added
- Support for **PostGIS** layers as input data.  
- Validation of numeric parameters for fuzzy membership functions.  
- Automatic graduated symbology for result layers.  

### Changed
- *Cancel* button renamed to *Close* for clarity.  
- Updated translations in **French**, **English**, **Spanish**, and **Portuguese**.  

### Fixed
- Various UI and logical corrections.  

---

## [1.0.5] - 2025-08-27  

### Added
- Default graduated symbology for output layers.  

---

## [1.0.2] - 2025-08-19  

### Added
- Logical consistency check for fuzzy aggregation functions:  
  - Warning message when incompatible combinations are detected.  
  - Option to confirm or cancel processing.  

### Changed
- Improved stability and language compatibility.  
- Updated translations (FR, EN, ES, PT).  

### Fixed
- Fixed missing `self` in `updateFunctionPreview()`.  
- Minor bug fixes in dialog behavior.  

---

## [1.0.1] - 2025-08-13  

### Fixed
- Display of fuzzy function images now works in all languages.  
- Improved mapping consistency with translation system.  

---

## [1.0.0] - 2025-08-10  

### Added
- Initial public release on the QGIS repository.  
- Fuzzy conversion of numeric attributes.  
- Supported membership functions: increasing/decreasing linear, triangular, trapezoidal, sigmoid (S/Z), and Gaussian.  
