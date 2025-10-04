from qgis.PyQt.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog, QLineEdit
)
from qgis.PyQt.QtCore import QVariant, Qt
from qgis.PyQt.QtGui import QDoubleValidator
from qgis.core import QgsField, QgsProject, edit
import csv
import sqlite3
from qgis.core import QgsExpression, QgsFeatureRequest, QgsVectorLayer,QgsApplication
from qgis.PyQt.QtCore import QDateTime
from qgis.PyQt import uic
from qgis.PyQt.QtCore import QTranslator, QCoreApplication, QLocale
import os
import getpass
import json
from qgis.PyQt.QtWidgets import QToolButton, QMenu, QAction
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
import psycopg2
from qgis.core import QgsMessageLog, Qgis
from qgis.core import QgsFeature, QgsDataSourceUri
from qgis.core import QgsRasterLayer
from qgis.core import QgsMapLayer, QgsMapLayerType
from qgis.PyQt.QtWidgets import QInputDialog
from osgeo import gdal
import numpy as np
from datetime import datetime
from getpass import getuser

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'fuzzyclass_dialog.ui'
))


class FuzzyClassDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, layer=None, parent=None, plugin_dir=None):
        super(FuzzyClassDialog, self).__init__(parent)
        self.iface = iface
        self.current_layer = layer
        self.plugin_dir = plugin_dir  # chemin du plugin pour les traductions

        # -----------------------------
        # Traductions
        # -----------------------------
        self.translator = QTranslator()
        locale = QLocale.system().name()  # ex: 'fr_FR'
        if self.plugin_dir:
            qm_path = os.path.join(self.plugin_dir, "i18n", f"fuzzyattributes_{locale}.qm")
            if os.path.exists(qm_path):
                self.translator.load(qm_path)
                QCoreApplication.installTranslator(self.translator)

        # -----------------------------
        # Charge le .ui
        # -----------------------------
        self.setupUi(self)

        # -----------------------------
        # Boutons CSV
        # -----------------------------
        self.btnSave = QPushButton(self.tr("Enregistrer en CSV"))
        self.btnSave.setToolTip(self.tr("Enregistre le mapping actuel dans un fichier CSV"))
        self.btnSave.clicked.connect(self.save_mapping_to_csv)
        self.horizontalLayoutBottom.addWidget(self.btnSave)

        self.btnLoad = QPushButton(self.tr("Charger depuis CSV"))
        self.btnLoad.setToolTip(self.tr("Charge un mapping depuis un fichier CSV"))
        self.btnLoad.clicked.connect(self.load_mapping_from_csv)
        self.horizontalLayoutBottom.addWidget(self.btnLoad)

        # -----------------------------
        # Boutons classiques
        # -----------------------------
        self.btnApply.clicked.connect(self.apply_mapping)
        self.btnClose.clicked.connect(self.close)
        self.btnLoadValues.clicked.connect(self.load_unique_raster_values)
        self.btnAssignFuzzy.clicked.connect(self.assign_fuzzy_to_selection)

        # Configurer la table
        self.tableMapping.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableMapping.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)

        # -----------------------------
        # Combo couche et mise à jour champs
        # -----------------------------
        self.populate_layer_combo()
        self.layerComboBox.currentIndexChanged.connect(self.on_layer_changed)


    # -----------------------------
    # Méthodes pour la mise à jour des champs
    # -----------------------------
    def on_layer_changed(self):
        display_name = self.layerComboBox.currentText()
        self.current_layer = self.layer_map.get(display_name)
        if self.current_layer is None:
            print(self.tr("Aucune couche sélectionnée !"))
            return

        

    # -----------------------------
    # Remplissage combo layer
    # -----------------------------
    def populate_layer_combo(self):
        """Remplit la comboBox avec les couches GeoPackage et PostGIS"""
        self.layerComboBox.clear()
        # Remplir les combos avec les rasters du projet
        for layer in QgsProject.instance().mapLayers().values():
            if isinstance(layer, QgsRasterLayer):
                self.layerComboBox.addItem(layer.name(), layer.id())
        

    def load_unique_raster_values(self):
        """Remplit tableMapping avec les classes uniques du raster sélectionné"""
        # Récupérer l'ID ou le nom choisi dans le combo
        idx = self.layerComboBox.currentIndex()
        if idx < 0:
            QMessageBox.warning(self, self.tr("Erreur"),self.tr( "Aucune couche sélectionnée dans la liste."))
            return

        layer_id = self.layerComboBox.itemData(idx)  # si tu as stocké l'ID comme userData
        if layer_id:
            layer = QgsProject.instance().mapLayer(layer_id)
        else:
            layer_name = self.layerComboBox.currentText()
            layer = next((l for l in QgsProject.instance().mapLayers().values() if l.name() == layer_name), None)

        if not layer or not layer.isValid() or layer.type() != QgsMapLayerType.RasterLayer:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("La couche sélectionnée n'est pas un raster valide."))
            return

        # Définir les colonnes
        self.tableMapping.setColumnCount(2)
        self.tableMapping.setHorizontalHeaderLabels(["Classe raster", "Fuzzy"])
        self.tableMapping.setRowCount(0)

        unique_values = set()

        try:
            from osgeo import gdal
            ds = gdal.Open(layer.dataProvider().dataSourceUri())
            band = ds.GetRasterBand(1)

            arr = band.ReadAsArray()
            nodata = band.GetNoDataValue()

            if nodata is not None:
                unique_values = set([int(v) for v in set(arr.flatten()) if v != nodata])
            else:
                unique_values = set([int(v) for v in set(arr.flatten())])

            ds = None

        except Exception as e:
            QMessageBox.critical(self, self.tr("Erreur"), self.tr(f"Impossible de récupérer les valeurs raster : {e}"))
            return

        for val in sorted(unique_values):
            row = self.tableMapping.rowCount()
            self.tableMapping.insertRow(row)
            self.tableMapping.setItem(row, 0, QTableWidgetItem(str(val)))
            self.tableMapping.setItem(row, 1, QTableWidgetItem(""))

        self.btnApply.setEnabled(len(unique_values) > 0)
        print(self.tr(f"{len(unique_values)} classes raster uniques ajoutées depuis {layer.name()}."))

    def assign_fuzzy_to_selection(self):
        """Assigne une valeur fuzzy à toutes les lignes sélectionnées"""
        selected_ranges = self.tableMapping.selectedRanges()
        if not selected_ranges:
            QMessageBox.warning(self, self.tr("Sélection vide"), self.tr("Sélectionnez au moins une ligne dans la table."))
            return

        # Demander la valeur fuzzy
        value, ok = QInputDialog.getDouble(
            self,
            self.tr("Valeur fuzzy"),
            self.tr("Entrez une valeur fuzzy entre 0 et 1 :"),
            decimals=3,
            min=0.0,
            max=1.0
        )
        if not ok:
            return

        # Affecter à toutes les lignes sélectionnées
        for sel in selected_ranges:
            for row in range(sel.topRow(), sel.bottomRow() + 1):
                self.tableMapping.setItem(row, 1, QTableWidgetItem(str(value)))

        print(self.tr(f"Valeur fuzzy {value} appliquée à {sum([r.rowCount() for r in selected_ranges])} lignes."))



    def apply_mapping(self):
        """Reclasse un raster selon les valeurs fuzzy de tableMapping."""
        # --- Récupérer la couche sélectionnée ---
        idx = self.layerComboBox.currentIndex()
        if idx < 0:
            QMessageBox.warning(self,self.tr( "Erreur"), self.tr("Aucune couche sélectionnée."))
            return

        layer_id = self.layerComboBox.itemData(idx)
        raster = QgsProject.instance().mapLayer(layer_id)
        if not raster or not raster.isValid():
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Raster invalide."))
            return

        # --- Construire le mapping depuis la table ---
        mapping = {}
        for row in range(self.tableMapping.rowCount()):
            key_item = self.tableMapping.item(row, 0)
            val_item = self.tableMapping.item(row, 1)
            if key_item and val_item:
                try:
                    mapping[int(key_item.text())] = float(val_item.text())
                except ValueError:
                    mapping[int(key_item.text())] = np.nan  # pixel non mappé

        # --- Charger le raster en array ---
        ds = gdal.Open(raster.dataProvider().dataSourceUri())
        band = ds.GetRasterBand(1)
        arr = band.ReadAsArray()
        nodata = band.GetNoDataValue()
        ds = None

        # --- Créer le tableau de sortie ---
        result = np.full_like(arr, nodata if nodata is not None else -9999, dtype=np.float32)
        for k, v in mapping.items():
            result[arr == k] = v

        # --- Construire le chemin de sortie ---
        base_name = f"fzy_{raster.name()}"
        out_dir = os.path.dirname(raster.dataProvider().dataSourceUri())
        out_path = os.path.join(out_dir, f"{base_name}.tif")

        # Vérifier si le fichier existe
        if os.path.exists(out_path):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Fichier existant")
            msg.setText(self.tr(f"Le fichier {base_name}.tif existe déjà dans {out_dir}."))
            msg.setInformativeText(self.tr("Voulez-vous l'écraser ?"))
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg.setDefaultButton(QMessageBox.StandardButton.No)
            reply = msg.exec()
            if reply == QMessageBox.StandardButton.No:
                i = 1
                while os.path.exists(os.path.join(out_dir, f"{base_name}_{i}.tif")):
                    i += 1
                out_path = os.path.join(out_dir, f"{base_name}_{i}.tif")

        # --- Créer le raster de sortie ---
        ds_in = gdal.Open(raster.dataProvider().dataSourceUri())
        geo = ds_in.GetGeoTransform()
        proj = ds_in.GetProjection()
        width = ds_in.RasterXSize
        height = ds_in.RasterYSize
        ds_in = None

        driver = gdal.GetDriverByName("GTiff")
        out_raster = driver.Create(out_path, width, height, 1, gdal.GDT_Float32)
        out_raster.SetGeoTransform(geo)
        out_raster.SetProjection(proj)
        out_band = out_raster.GetRasterBand(1)
        out_band.SetNoDataValue(nodata if nodata is not None else -9999)
        out_band.WriteArray(result)
        out_raster.FlushCache()
        out_raster = None

        # --- Charger comme QgsRasterLayer ---
        output_layer = QgsRasterLayer(out_path, base_name)
        if not output_layer.isValid():
            QMessageBox.critical(self, self.tr("Erreur"), self.tr("Échec de la création du raster de sortie"))
            return

        QgsProject.instance().addMapLayer(output_layer)
        
                 # Ajouter les métadonnées
        fuzzy_code='Classes'

        # On stockera les lignes sous forme de texte
        lines = [f"Classe raster;Fuzzy"]

        for row in range(self.tableMapping.rowCount()):
            text_item = self.tableMapping.item(row, 0)
            fuzzy_item = self.tableMapping.item(row, 1)
            line = f"{text_item.text() if text_item else ''};{fuzzy_item.text() if fuzzy_item else ''}"
            lines.append(line)
        
        # Joindre toutes les lignes avec des retours à la ligne
        params = "\n".join(lines)
        
        self.save_raster_metadata(out_path, "", "", params, raster.name(), "")
        
        
        
        QMessageBox.information(self, self.tr("Succès"), self.tr(f"Raster fuzzy créé : {os.path.basename(out_path)}"))



    # -------------------------
    # Sauvegarde en CSV
    # -------------------------
    def save_mapping_to_csv(self):
        """Enregistre le mapping raster/flou dans un fichier CSV"""
        if self.tableMapping.rowCount() == 0:
            QMessageBox.warning(self, self.tr("Table vide"), self.tr("Aucune donnée à sauvegarder."))
            return

        path, _ = QFileDialog.getSaveFileName(
            self, self.tr("Enregistrer la table en CSV"), "", "CSV Files (*.csv)"
        )
        if not path:
            return

        if not path.lower().endswith(".csv"):
            path += ".csv"

        field_name = "Classe raster"  # ✅ fixe pour ton dialog raster

        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow([field_name, "Fuzzy"])
                for row in range(self.tableMapping.rowCount()):
                    text_item = self.tableMapping.item(row, 0)
                    fuzzy_item = self.tableMapping.item(row, 1)
                    writer.writerow([
                        text_item.text() if text_item else "",
                        fuzzy_item.text() if fuzzy_item else ""
                    ])

            QMessageBox.information(self, "Succès", f"Table sauvegardée dans {path}")

        except Exception as e:
            QMessageBox.critical(self, self.tr("Erreur"), self.tr(f"Impossible de sauvegarder en CSV : {e}"))

    def get_selected_layer(self):
        """Retourne la couche raster sélectionnée dans le comboBox."""
        idx = self.layerComboBox.currentIndex()
        if idx < 0:
            return None

        # Essayer de récupérer par ID stocké en userData
        layer_id = self.layerComboBox.itemData(idx)
        if layer_id:
            layer = QgsProject.instance().mapLayer(layer_id)
        else:
            # Sinon récupérer par nom
            layer_name = self.layerComboBox.currentText()
            layer = next((l for l in QgsProject.instance().mapLayers().values() if l.name() == layer_name), None)

        return layer


    def load_mapping_from_csv(self):
        """Charge un mapping classes raster ↔ fuzzy depuis un CSV et complète avec les valeurs uniques du raster"""
        path, _ = QFileDialog.getOpenFileName(
            self, self.tr("Charger une table CSV"), "", "CSV Files (*.csv)"
        )
        if not path:
            return

        try:
            # Lire le CSV
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=";")
                rows = list(reader)

            if not rows:
                QMessageBox.warning(self, self.tr("Attention"), self.tr("Le fichier CSV est vide."))
                return

            headers = reader.fieldnames
            if not headers or "Fuzzy" not in headers or "Classe raster" not in headers:
                QMessageBox.critical(
                    self,
                    self.tr("Erreur"),
                    self.tr("Le CSV doit contenir les colonnes 'Classe raster' et 'Fuzzy'.")
                )
                return

            # Construire le mapping à partir du CSV
            mapping = {row["Classe raster"]: row["Fuzzy"] for row in rows}

            # --- Récupérer les classes uniques du raster sélectionné ---
            layer = self.get_selected_layer()
            if not layer or not layer.isValid() or layer.type() != QgsMapLayerType.RasterLayer:
                QMessageBox.warning(self,self.tr( "Erreur"), self.tr("La couche sélectionnée n'est pas un raster valide."))
                return

            unique_values = set()

            if layer and layer.type() == QgsMapLayer.LayerType.RasterLayer:
                from osgeo import gdal
                ds = gdal.Open(layer.dataProvider().dataSourceUri())
                band = ds.GetRasterBand(1)
                arr = band.ReadAsArray()
                nodata = band.GetNoDataValue()

                if nodata is not None:
                    unique_values = set([int(v) for v in set(arr.flatten()) if v != nodata])
                else:
                    unique_values = set([int(v) for v in set(arr.flatten())])

                ds = None

            # Union CSV + raster
            all_values = set(mapping.keys()) | set(str(v) for v in unique_values)

            # Fusion : valeurs CSV prioritaires
            final_rows = [(val, mapping.get(val, "")) for val in sorted(all_values, key=lambda x: int(x) if x.isdigit() else x)]

            # --- Remplir la table ---
            self.tableMapping.setColumnCount(2)
            self.tableMapping.setRowCount(0)
            self.tableMapping.setHorizontalHeaderLabels(["Classe raster", "Fuzzy"])

            for val, fuzzy in final_rows:
                row_idx = self.tableMapping.rowCount()
                self.tableMapping.insertRow(row_idx)
                self.tableMapping.setItem(row_idx, 0, QTableWidgetItem(str(val)))
                self.tableMapping.setItem(row_idx, 1, QTableWidgetItem(str(fuzzy) if fuzzy is not None else ""))

            QMessageBox.information(self, self.tr("Succès"), self.tr(f"Table chargée depuis {path}"))

        except Exception as e:
            QMessageBox.critical(self, self.tr("Erreur"), self.tr(f"Impossible de charger le CSV : {e}"))

    def save_raster_metadata(self,raster_path, source_field, function_name, params, source1=None, source2=None):
        folder, filename = os.path.split(raster_path)
        meta_path = os.path.join(folder, f"{filename}.fzy")

        # Préparer les données
        data = {
            "sourcefield": raster_path,
            "function": "Classes",
            "params": params,
            "source1": source1 if source1 else "",
            "source2": source2 if source2 else "",
            "datecreated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": getuser()
        }

        # Vérifier si le fichier existe déjà
        file_exists = os.path.isfile(meta_path)

        with open(meta_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

        return meta_path


