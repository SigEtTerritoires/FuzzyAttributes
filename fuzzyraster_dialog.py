from qgis.core import (
    Qgis,QgsProject, QgsVectorLayer, QgsField, edit, QgsFeature,
    QgsFields, QgsWkbTypes, QgsCoordinateReferenceSystem,
    QgsVectorFileWriter, QgsApplication
)
from qgis.core import (
    QgsColorRampShader, QgsRasterShader,
    QgsSingleBandPseudoColorRenderer
)
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtCore import QTranslator, QCoreApplication, QLocale
from qgis.PyQt.QtWidgets import QDialog, QMessageBox, QToolTip
from qgis.PyQt.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem
from qgis.PyQt.QtCore import QVariant
from .fuzzyattributes_dialog_base import Ui_FuzzyAttributesDialog
from datetime import datetime
import getpass
import re
from qgis.PyQt.QtGui import QPixmap
from qgis.core import QgsDataSourceUri
from qgis.core import QgsMessageLog, Qgis
from qgis.PyQt.QtCore import QDateTime
from qgis.core import QgsVectorLayer, QgsFeature, QgsDataSourceUri
import csv
from datetime import datetime
from getpass import getuser

from qgis.PyQt import QtCore

from qgis.PyQt.QtWidgets import QDialog, QMessageBox
from qgis.PyQt.QtGui import QPixmap
from qgis.core import QgsProject, QgsRasterLayer, QgsRasterBandStats
import os, math
import numpy as np
from osgeo import gdal
from .fuzzyraster_ui import Ui_FuzzyAttributesDialog  # ton UI généré .py
from qgis.PyQt.QtWidgets import QFileDialog
_translator = None

def load_translator():
    global _translator
    locale = QLocale(QgsApplication.instance().locale().name()[0:2])
    path = os.path.join(os.path.dirname(__file__), f"FuzzyAttributes_{locale}.qm")
    if os.path.exists(path):
        _translator = QTranslator()
        if _translator.load(path):
            QCoreApplication.installTranslator(_translator)




from qgis.PyQt.QtWidgets import QDialog
from qgis.core import QgsProject, QgsRasterLayer, QgsRasterBandStats
from .fuzzyraster_ui import Ui_FuzzyAttributesDialog
from .fuzzyraster_ui import Ui_FuzzyAttributesDialog as Ui_FuzzyRasterDialog
class FuzzyRasterDialog(QDialog, Ui_FuzzyRasterDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Dictionnaire nom -> layer
        self.layer_map = {}

        # Boutons
        self.btnShowStats.clicked.connect(self.show_raster_statistics)
        self.helpButton.clicked.connect(self.show_help)
        self.buttonBox.accepted.connect(self.apply_fuzzy_transformation)
        self.buttonBox.rejected.connect(self.reject)
        self.btnShowMetadata.clicked.connect(self.show_metadata_table)
        # Types flous
        self.fuzzy_types = [
            ("linear_inc", self.tr("linéaire croissante")),
            ("linear_dec", self.tr("linéaire décroissante")),
            ("triangular", self.tr("triangulaire")),
            ("trapezoidal", self.tr("trapézoïdale")),
            ("sigmoid_inc", self.tr("sigmoïde croissante (S)")),
            ("sigmoid_dec", self.tr("sigmoïde décroissante (Z)")),
            ("gaussian", self.tr("gaussienne"))
        ]
        for code, label in self.fuzzy_types:
            self.fuzzyTypeComboBox.addItem(label, code)
        self.fuzzyTypeComboBox.currentTextChanged.connect(self.updateFunctionPreview)
        self.fuzzyTypeComboBox.currentIndexChanged.connect(self.update_example_parameters)
        self.updateFunctionPreview(self.fuzzyTypeComboBox.currentText())
        self.update_example_parameters()  # Affiche exemple au démarrage
        # Mettre à jour la liste si des couches sont ajoutées/supprimées
        QgsProject.instance().layersAdded.connect(lambda _: self.populate_layer_combo())
        QgsProject.instance().layersRemoved.connect(lambda _: self.populate_layer_combo())

    def populate_layer_combo(self):
        """Affiche uniquement les couches raster dans la combo"""
        self.layerComboBox.clear()
        self.layer_map.clear()
        for layer in QgsProject.instance().mapLayers().values():
            if isinstance(layer, QgsRasterLayer):
                self.layerComboBox.addItem(layer.name())
                self.layer_map[layer.name()] = layer


    def show_raster_statistics(self):
        """Affiche les stats du raster sélectionné"""
        name = self.layerComboBox.currentText()
        if not name:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Aucune couche sélectionnée"))
            return

        layers = QgsProject.instance().mapLayersByName(name)
        if not layers:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr(f"Impossible de trouver la couche {name}"))
            return

        layer = layers[0]
        if not isinstance(layer, QgsRasterLayer):
            QMessageBox.warning(self, self.tr("Erreur"), self.tr(f"La couche {name} n’est pas un raster"))
            return

        stats = layer.dataProvider().bandStatistics(1, QgsRasterBandStats.Stats.All)
        QMessageBox.information(
            self,
            self.tr("Statistiques du raster"),
            f"Min : {stats.minimumValue}\n"
            f"Max : {stats.maximumValue}\n"
            f"Moyenne : {stats.mean}\n"
            f"Écart-type : {stats.stdDev}"
        )

    # ----------------------------
    # Exemple de paramètres
    # ----------------------------
    def update_example_parameters(self):
        code = self.fuzzyTypeComboBox.currentData()
        examples = {
            "linear_inc": "Exemple : a=200, b=1500",
            "linear_dec": "Exemple : a=1500, b=200",
            "triangular": "Exemple : a=200, b=800, c=1500",
            "trapezoidal": "Exemple : a=200, b=500, c=1200, d=1500",
            "sigmoid_inc": "Exemple : c=800, k=0.01",
            "sigmoid_dec": "Exemple : c=800, k=0.01",
            "gaussian": "Exemple : c=800, σ=200"
        }
        self.paramExampleLabel.setText(examples.get(code, "Exemple :"))


    def showEvent(self, event):
        super().showEvent(event)
        self.populate_layer_combo()

    def selected_layer(self):
        """Retourne le raster sélectionné"""
        name = self.layerComboBox.currentText()
        return self.layer_map.get(name)

  


    def show_help(self):
        help_text = (
            self.tr("<b>Types de fonctions floues :</b><br><br>"
            "<b>• Linéaire croissante :</b> augmente de 0 à 1 entre a et b<br>"
            "<b>• Linéaire décroissante :</b> diminue de 1 à 0 entre a et b<br>"
            "<b>• Triangulaire :</b> forme un pic à b entre a et c<br>"
            "<b>• Trapézoïdale :</b> forme un plateau entre b et c<br>"
            "<b>• Sigmoïde (S) :</b> transition douce croissante centrée en b<br>"
            "<b>• Sigmoïde (Z) :</b> transition douce décroissante centrée en b<br>"
            "<b>• Gaussienne :</b> courbe en cloche centrée en c avec largeur sigma<br>")
        )
        QMessageBox.information(self, self.tr("Aide sur les fonctions floues"), help_text)

    def get_parameters(self):
        param_text = self.paramLineEdit.text()
        try:
            params = [float(x.strip()) for x in param_text.split(',')]
        except ValueError:
            QMessageBox.warning(self, self.tr("Erreur"),self.tr( "Paramètres invalides. Utilisez des nombres séparés par des virgules."))
            return None
        return {
            'layer': self.selected_layer(),
            'field_name': self.fieldComboBox.currentText(),
            'fuzzy_type': self.fuzzyTypeComboBox.currentText(),
            'params': params
        }
    def updateFunctionPreview(self, _unused=None):
        mapping = {
            "linear_inc": "linearcroiss.png",
            "linear_dec": "lineardecroiss.png",
            "triangular": "triangulaire.png",
            "trapezoidal": "trapezoidale.png",
            "sigmoid_inc": "sigmocroiss.png",
            "sigmoid_dec": "sigmodecroiss.png",
            "gaussian": "gaussienne.png"
        }
        
        code = self.fuzzyTypeComboBox.currentData()  # Récupère le code interne
        fname = mapping.get(code)
        
        if fname:
            img_path = os.path.join(os.path.dirname(__file__), "resources", "images", fname)
            pix = QPixmap(img_path)
        else:
            pix = QPixmap()  # vide

        self.labelFunctionPreview.setPixmap(pix)

    def on_layer_changed(self):
        layer_name = self.layerComboBox.currentText()
        layers = QgsProject.instance().mapLayers().values()
        for layer in layers:
            if layer.name() == layer_name:
                self.current_layer = layer
                break
    def open_aggregation_function_dialog(self):
        dlg = AggregationFunctionDialog()
        if dlg.exec():
            result_code = dlg.get_selected_values()
            self.functionCodeLabel.setText(result_code)  # à adapter selon votre interface
    


    def apply_fuzzy_transformation(self):
        idx = self.layerComboBox.currentIndex()
        if idx < 0:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Aucun raster sélectionné"))
            return

        config = self.get_parameters()
        if not config:
            return

        layer = config['layer']
        fuzzy_code = self.fuzzyTypeComboBox.currentData()  # 🔹 Code interne, pas label
        params = config['params']

        # Validation des paramètres
        valid, msg = self.validate_fuzzy_params(fuzzy_code, params)
        if not valid:
            QMessageBox.warning(self, self.tr("Paramètres invalides"), self.tr(msg))
            return


        
        # Récupérer la couche raster
        raster = self.selected_layer()
        if not isinstance(raster, QgsRasterLayer):
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("La couche sélectionnée n’est pas un raster"))
            return

        # Récupérer les paramètres
        try:
            params = [float(p.strip()) for p in self.paramLineEdit.text().split(",")]
        except Exception:
            QMessageBox.warning(self,self.tr("Erreur"), self.tr("Paramètres invalides"))
            return

        # Préparer fichier sortie (⚠️ bien en dehors du except)
        src_path = raster.dataProvider().dataSourceUri()
        folder, name = os.path.split(src_path)
        base, _ = os.path.splitext(name)
        out_path = os.path.join(folder, f"fzy_{base}.tif")

        # Vérifier si le fichier existe déjà
        if os.path.exists(out_path):
            reply = QMessageBox.question(
                self,
                self.tr("Fichier existant",
                f"Le fichier {out_path} existe déjà.\n\nVoulez-vous l’écraser ?"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                # Demander un nouveau nom de fichier
                new_path, _ = QFileDialog.getSaveFileName(
                    self,
                    self.tr("Choisir un nom de fichier"),
                    os.path.join(folder, f"fzy_{base}_new.tif"),
                    "GeoTIFF (*.tif)"
                )
                if not new_path:  # utilisateur a annulé
                    QMessageBox.information(self, self.tr("Annulé"), self.tr("Opération annulée par l’utilisateur."))
                    return
                out_path = new_path
            else:
                # ⚠️ fermer les handles avant suppression pour éviter "Permission denied"
                try:
                    band = None
                    ds = None
                    if os.path.exists(out_path):
                        os.remove(out_path)
                except Exception as e:
                    QMessageBox.warning(
                        self,
                        self.tr("Erreur"),
                        self.tr(f"Impossible d’écraser {out_path}\n{e}")
                    )
                    return

        # Lecture du raster en numpy
        ds = gdal.Open(src_path)
        band = ds.GetRasterBand(1)
        arr = band.ReadAsArray().astype(float)

        # Application transformation floue
        fuzzy_arr = self.fuzzy_raster_array(arr, fuzzy_code, params)

        # Lecture de la bande source
        src_band = ds.GetRasterBand(1)
        nodata = src_band.GetNoDataValue()

        # Création du raster de sortie
        driver = gdal.GetDriverByName("GTiff")
        out_ds = driver.Create(out_path, ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Float32)

        # Copier la géoréférence et la projection
        out_ds.SetGeoTransform(ds.GetGeoTransform())
        out_ds.SetProjection(ds.GetProjection())

        # Écriture des données floues
        out_band = out_ds.GetRasterBand(1)
        out_band.WriteArray(fuzzy_arr)



        # Vider le cache et fermer les fichiers
        out_band.FlushCache()
        out_band = None
        out_ds = None
        ds = None


        # Charger dans QGIS
        final_name = os.path.splitext(os.path.basename(out_path))[0]  # extrait le nom du fichier sans extension
        new_layer = QgsRasterLayer(out_path, final_name)

        if new_layer.isValid():
            QgsProject.instance().addMapLayer(new_layer)
        else:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr(f"Impossible de charger le raster : {out_path}"))

        QMessageBox.information(
            self,
            self.tr("Succès"),
            self.tr("Transformation floue créée dans fzy_'{}'").format(base)
        )
        


        # raster_out : QgsRasterLayer déjà créé et ajouté à QGIS
        raster_out = new_layer  # ton raster flou
        folder, filename = os.path.split(out_path) 
        base, ext = os.path.splitext(filename)
        self.save_raster_metadata(src_path,'',fuzzy_code,params,base,'')

        # Shader et rampe
        shader = QgsRasterShader()
        color_ramp = QgsColorRampShader()
        color_ramp.setColorRampType(QgsColorRampShader.Type.Discrete)

        # Définir les classes
        classes = [
            (0.0, 0.125, "#ff0000", "0 – 0.125 (mauvais)"),
            (0.125, 0.375, "#ff7f00", "0.125 – 0.375 (médiocre)"),
            (0.375, 0.625, "#ffff00", "0.375 – 0.625 (moyen)"),
            (0.625, 0.875, "#7fff00", "0.625 – 0.875 (bon)"),
            (0.875, 1.01, "#006400", "0.875 – 1.0 (très bon)")
        ]

        items = []
        for min_val, max_val, color, label in classes:
            items.append(QgsColorRampShader.ColorRampItem(max_val, QColor(color), label))

        color_ramp.setColorRampItemList(items)
        shader.setRasterShaderFunction(color_ramp)

        # Rendu pseudo-coloré
        renderer = QgsSingleBandPseudoColorRenderer(raster_out.dataProvider(), 1, shader)
        raster_out.setRenderer(renderer)
        raster_out.triggerRepaint()

        # Ajouter à la légende
        if raster_out not in QgsProject.instance().mapLayers().values():
            QgsProject.instance().addMapLayer(raster_out)

        
    def fuzzy_raster_array(self, arr, fuzzy_code, params):
        # On commence avec un tableau vide rempli de nan
        result = np.full(arr.shape, np.nan, dtype=np.float32)

        # Masque des pixels valides (non nodata)
        mask = ~np.isnan(arr)

        if fuzzy_code == "linear_inc":
            a, b = params
            result[mask] = (arr[mask] - a) / (b - a)
        elif fuzzy_code == "linear_dec":
            a, b = params
            result[mask] = (b - arr[mask]) / (b - a)
        elif fuzzy_code == "triangular":
            a, b, c = params
            result[mask] = np.where(
                (arr[mask] <= a) | (arr[mask] >= c),
                0,
                np.where(
                    arr[mask] < b,
                    (arr[mask] - a) / (b - a),
                    (c - arr[mask]) / (c - b)
                )
            )
        elif fuzzy_code == "trapezoidal":
            a, b, c, d = params
            res = np.zeros_like(arr[mask])
            res = np.where((arr[mask] <= a) | (arr[mask] >= d), 0, res)
            res = np.where((arr[mask] > a) & (arr[mask] < b), (arr[mask]-a)/(b-a), res)
            res = np.where((arr[mask] >= b) & (arr[mask] <= c), 1, res)
            res = np.where((arr[mask] > c) & (arr[mask] < d), (d-arr[mask])/(d-c), res)
            result[mask] = res
        elif fuzzy_code == "sigmoid_inc":
            a, b = params
            result[mask] = 1 / (1 + np.exp(-a * (arr[mask] - b)))
        elif fuzzy_code == "sigmoid_dec":
            a, b = params
            result[mask] = 1 - (1 / (1 + np.exp(-a * (arr[mask] - b))))
        elif fuzzy_code == "gaussian":
            c, sigma = params
            result[mask] = np.exp(-((arr[mask] - c) ** 2) / (2 * sigma ** 2))

        # Forcer dans [0,1]
        result = np.clip(result, 0, 1)

        return result

    def get_parameters(self):
        param_text = self.paramLineEdit.text()
        try:
            params = [float(x.strip()) for x in param_text.split(',')]
        except ValueError:
            QMessageBox.warning(self, self.tr("Erreur"),self.tr( "Paramètres invalides. Utilisez des nombres séparés par des virgules."))
            return None
        return {
            'layer': self.selected_layer(),
            'fuzzy_type': self.fuzzyTypeComboBox.currentText(),
            'params': params
        }

    def validate_fuzzy_params(self, fuzzy_code, params):
        """
        Vérifie que les paramètres de la fonction floue sont corrects selon le type.
        Utilise les codes internes des fonctions floues.
        Retourne : (bool_valid, message)
        """
        try:
            if fuzzy_code in ["linear_inc", "linear_dec", "sigmoid_inc", "sigmoid_dec"]:
                if len(params) != 2:
                    return False, self.tr("Cette fonction nécessite exactement 2 paramètres.")
                a, b = params
                if a == b:
                    return False, self.tr("Les deux paramètres ne doivent pas être égaux.")
            elif fuzzy_code == "triangular":
                if len(params) != 3:
                    return False, self.tr("La fonction triangulaire nécessite exactement 3 paramètres.")
                a, b, c = params
                if not (a < b < c):
                    return False, self.tr("Les paramètres doivent être dans l'ordre a < b < c.")
            elif fuzzy_code == "trapezoidal":
                if len(params) != 4:
                    return False, self.tr("La fonction trapézoïdale nécessite exactement 4 paramètres.")
                a, b, c, d = params
                if not (a < b <= c < d):
                    return False, self.tr("Les paramètres doivent être dans l'ordre a < b <= c < d.")
            elif fuzzy_code == "gaussian":
                if len(params) != 2:
                    return False, self.tr("La fonction gaussienne nécessite exactement 2 paramètres (c, sigma).")
                c, sigma = params
                if sigma <= 0:
                    return False, self.tr("Le paramètre sigma doit être strictement positif.")
            else:
                return False, self.tr("Type de fonction floue inconnu.")
            return True, ""
        except Exception as e:
            return False, self.tr("Erreur lors de la validation des paramètres : ") + str(e)

    def load_translator(self):
        from qgis.PyQt.QtCore import QTranslator, QLocale, QCoreApplication
        from qgis.core import QgsApplication
        import os

        # Obtenir la langue actuelle de QGIS (ex : 'fr')
        locale_name = QgsApplication.instance().locale()
        locale = QLocale(locale_name).name()[0:2]  # 'fr', 'en', etc.
        from qgis.core import QgsMessageLog, Qgis
        QgsMessageLog.logMessage(f"Langue QGIS détectée : {locale}", "FuzzyAttributes", Qgis.MessageLevel.Info)



        translations_path = os.path.join(os.path.dirname(__file__), 'i18n')
        translation_file = f'FuzzyAttributes_{locale}.qm'
        translation_path = os.path.join(translations_path, translation_file)

        if os.path.exists(translation_path):
            self.translator = QTranslator()
            if self.translator.load(translation_path):
                QCoreApplication.installTranslator(self.translator)
        from qgis.PyQt.QtCore import QCoreApplication

    def _(text):
        return QCoreApplication.translate("FuzzyAttributes", text)



    def save_raster_metadata(self,raster_path, source_field, function_name, params, source1=None, source2=None):
        folder, source2 = os.path.split(raster_path)
        meta_path = os.path.join(folder, f"{source1}.fzy")

        # Préparer les données
        data = {
            "sourcefield": source_field,
            "function": function_name,
            "params": ",".join(map(str, params)),
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

    def show_metadata_table(self):
        name = self.layerComboBox.currentText()
        if not name:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Aucune couche sélectionnée"))
            return

        raster = QgsProject.instance().mapLayersByName(name)
        if not raster:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr(f"Impossible de trouver la couche {name}"))
            return

        raster = raster[0]  # on prend le premier trouvé
        src_path = raster.dataProvider().dataSourceUri()
        folder, fname = os.path.split(src_path)
        base, _ = os.path.splitext(fname)
        fzy_path = os.path.join(folder, f"fzy_{base}.fzy")

        if not os.path.exists(fzy_path):
            QMessageBox.information(self, self.tr("Info", f"Aucun fichier de métadonnées trouvé pour {base}"))
            return

        dlg = RasterMetadataDialog(fzy_path, self)
        dlg.exec()  # ⚠️ exec_ pour afficher la fenêtre modale


class RasterMetadataDialog(QDialog):
    def __init__(self, fzy_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Métadonnées du raster")
        self.resize(700, 400)

        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        layout.addWidget(self.table)

        if not os.path.exists(fzy_path):
            QMessageBox.warning(self, self.tr("Erreur"), self.tr(f"Fichier métadonnées non trouvé :\n{fzy_path}"))
            return

        # Lecture CSV
        with open(fzy_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
            rows = list(reader)

        # Remplir le QTableWidget
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, field in enumerate(headers):
                value = row.get(field, "")
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

