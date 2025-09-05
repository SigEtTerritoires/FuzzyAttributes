from PyQt5 import uic
from PyQt5.QtWidgets import QDialog,QMessageBox
from qgis.core import QgsProject,QgsVectorLayer, QgsProcessingFeedback,   QgsProcessingFeatureSourceDefinition
from qgis.core import QgsField,QgsFields,QgsWkbTypes,QgsFeature,edit
from qgis.core import QgsDataSourceUri, QgsProviderRegistry, Qgis,QgsApplication
from qgis.core import QgsVectorLayerExporter, QgsCoordinateTransformContext
from qgis.core import QgsGraduatedSymbolRenderer, QgsSymbol
from PyQt5.QtCore import QVariant
import os
import processing
from qgis.core import QgsProcessingOutputLayerDefinition, QgsMessageLog,QgsProcessing,QgsVectorFileWriter
import sys
import re
from qgis.PyQt.QtCore import QFileInfo
import math
from datetime import datetime
from qgis.PyQt.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem
import getpass
from qgis.PyQt.QtCore import QTranslator, QCoreApplication, QLocale ,NULL,QDateTime
import psycopg2
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from qgis.PyQt.QtGui import QColor
from qgis.core import QgsProperty, QgsSymbolLayer, QgsSingleSymbolRenderer
from qgis.core import (
    QgsRendererRange,
    QgsFillSymbol, QgsMapLayerStyle)
from PyQt5.QtCore import QVariant
import tempfile
from qgis.core import QgsStyle

            
_translator = None
def load_translator():
    global _translator
    locale = QLocale(QgsApplication.instance().locale().name()[0:2])
    path = os.path.join(os.path.dirname(__file__), f"FuzzyAttributes_{locale}.qm")
    if os.path.exists(path):
        _translator = QTranslator()
        if _translator.load(path):
            QCoreApplication.installTranslator(_translator)
 
FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'fuzzyaggregate.ui')
)

from .aggregation_function_dialog_ui import Ui_AggregationFunctionDialog


def fuzzy_442(x, y):
    val = (x + y) - 1
    return max(0, val)
def fuzzy_441(x, y):
    val = (x + y) - 1
    val = max(0, val)
    return math.sqrt(val)
def fuzzy_440(x, y):
    val = 2 * ((x + y) - 1)
    val = max(0, min(1, val))
    return val
def fuzzy_432(x, y):
    # Val = x * y
    Val = x * y
    return Val

def fuzzy_431(x, y):
    # Val = sqrt(x*y) - ((1-x)*(1-y))
    # Si Val < 0 alors Val = 0
    import math
    Val = math.sqrt(x * y) - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_430(x, y):
    # Sigma = (x*y) / (1 - x - y + 2*x*y) sauf si x=0 ou y=0 alors Sigma=0
    # Val = Sigma - ((1-x)*(1-y))
    # Si Val < 0 alors Val=0
    if x == 0 or y == 0:
        Sigma = 0
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_422(x, y):
    # Val = min(x, y)
    Val = x if x <= y else y
    return Val


def fuzzy_421(x, y):
    # Val = sqrt(x * y)
    Val = math.sqrt(x * y)
    return Val

def fuzzy_420(x, y):
    # Sigma = (x*y) / (1 - x - y + 2*x*y) sauf si x=0 ou y=0 alors Sigma=0
    if x == 0 or y == 0:
        Sigma = 0
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma
    return Val

def fuzzy_411(x, y):
    # Hypothèse : x et y >= 0
    sqrt_x = math.sqrt(x)
    sqrt_y = math.sqrt(y)
    return min(sqrt_x, sqrt_y)


def fuzzy_410(x, y):
    # Val = sqrt(2 * x * y)
    # Si Val > 1 alors Val = 1
    Val = math.sqrt(2 * x * y)
    if Val > 1:
        Val = 1
    return Val
def fuzzy_400(x, y):
    V = abs(x - y)
    Val = x + y - V
    if Val > 1:
        Val = 1
    return Val

def fuzzy_342(x, y):
    V = x + y - 1
    if V < 0.25:
        V = 0.25
    Val = V - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_341(x, y):
    V = x + y - 0.75
    if V > 1:
        V = 1
    Val = V - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_340(x, y):
    if x == 0 or y == 0:
        Sigma = 0.25
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma - (2 * ((1 - x) * (1 - y)))
    if Val < 0:
        Val = 0
    return Val
def fuzzy_332(x, y):
    Val = x + y - 1
    if Val < 0.25:
        Val = 0.25
    return Val

def fuzzy_331(x, y):
    Val = x + y - 0.75
    if Val > 1:
        Val = 1
    if Val < 0:
        Val = 0
    return Val

def fuzzy_330(x, y):
    if x == 0 or y == 0:
        Sigma = 0.25
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_322(x, y):
    if x >= y and x >= 0.25:
        if y >= 0.25:
            Val = y
        else:
            Val = 0.25
    else:
        if y >= x and y >= 0.25:
            if x >= 0.25:
                Val = x
            else:
                Val = 0.25
        else:
            if x >= y:
                Val = x
            else:
                Val = y
    return Val


def fuzzy_321(x, y):
    x2 = x ** 2
    y2 = y ** 2
    if x2 >= y2 and x2 >= 0.25:
        if y2 >= 0.25:
            Val = y2
        else:
            Val = 0.25
    else:
        if y2 >= x2 and y2 >= 0.25:
            if x2 >= 0.25:
                Val = x2
            else:
                Val = 0.25
        else:
            if x2 >= y2:
                Val = x2
            else:
                Val = y2
    Val = Val - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_320(x, y):
    if x == 0 or y == 0:
        Sigma = 0.25
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma
    return Val

def fuzzy_311(x, y):
    x2 = x ** 2
    y2 = y ** 2
    if x2 >= y2 and x2 >= 0.25:
        if y2 >= 0.25:
            Val = y2
        else:
            Val = 0.25
    else:
        if y2 >= x2 and y2 >= 0.25:
            if x2 >= 0.25:
                Val = x2
            else:
                Val = 0.25
        else:
            if x2 >= y2:
                Val = x2
            else:
                Val = y2
    return Val
def fuzzy_310(x, y):
    if x == 0 or y == 0:
        Sigma = 0.25
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma + ((1 - x) * (1 - y))
    return Val

def fuzzy_300(x, y):
    if x == 0 or y == 0:
        Sigma = 0.25
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma + 2 * ((1 - x) * (1 - y))
    if Val > 1:
        Val = 1
    return Val

def fuzzy_242(x, y):
    if x >= y and x >= 0.5:
        if y >= 0.5:
            Val = y
        else:
            Val = 0.5
    else:
        if y >= x and y >= 0.5:
            if x >= 0.5:
                Val = x
            else:
                Val = 0.5
        else:
            if x >= y:
                Val = x
            else:
                Val = y
    Val = Val - 2 * ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_241(x, y):
    Val = (x * y) + (abs(x - y) / 2)
    Val = Val - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val
def fuzzy_240(x, y):
    if x == 0 or y == 0:
        Sigma = 0.25
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma - 2 * ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_232(x, y):
    if x >= y and x >= 0.5:
        if y >= 0.5:
            Val = y
        else:
            Val = 0.5
    else:
        if y >= x and y >= 0.5:
            if x >= 0.5:
                Val = x
            else:
                Val = 0.5
        else:
            if x >= y:
                Val = x
            else:
                Val = y
    Val = Val - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_231(x, y):
    Val = (x * y) + (abs(x - y) / 2)
    return Val

def fuzzy_230(x, y):
    if x == 0 or y == 0:
        Sigma = 0.5
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val
def fuzzy_222(x, y):
    if x >= y and x >= 0.5:
        if y >= 0.5:
            Val = y
        else:
            Val = 0.5
    else:
        if y >= x and y >= 0.5:
            if x >= 0.5:
                Val = x
            else:
                Val = 0.5
        else:
            if x >= y:
                Val = x
            else:
                Val = y
    # La ligne commentée en VBA est ignorée car non active
    # Val = Val - 2 * ((1 - x) * (1 - y))
    return Val

def fuzzy_221(x, y):
    Val = (x + y) / 2
    return Val

def fuzzy_220(x, y):
    if x == 0 or y == 0:
        Sigma = 0.5
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma
    return Val

def fuzzy_211(x, y):
    x2 = x**2
    y2 = y**2
    if x2 >= y2 and x2 >= 0.5:
        if y2 >= 0.5:
            Val = y2
        else:
            Val = 0.5
    else:
        if y2 >= x2 and y2 >= 0.5:
            if x2 >= 0.5:
                Val = x2
            else:
                Val = 0.5
        else:
            if x2 >= y2:
                Val = x2
            else:
                Val = y2
    return Val
def fuzzy_210(x, y):
    if x == 0 or y == 0:
        Sigma = 0.5
    else:
        denom = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denom if denom != 0 else 0
    Val = Sigma + ((1 - x) * (1 - y))
    if Val > 1:
        Val = 1
    return Val

def fuzzy_200(x, y):
    if x == 0 or y == 0:
        Sigma = 0.5
    else:
        denom = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denom if denom != 0 else 0
    Val = Sigma + 2 * ((1 - x) * (1 - y))
    if Val > 1:
        Val = 1
    return Val

import math

def fuzzy_141(x, y):
    V = (x + y) / 2
    Val = V - 3 * ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    else:
        Val = math.sqrt(Val)
    return Val

def fuzzy_140(x, y):
    Val = x + y - 0.5
    if Val > 1:
        Val = 1
    if Val < 0:
        Val = 0
    Val = math.sqrt(Val) - 3 * ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_131(x, y):
    if x >= y and x >= 0.75:
        if y >= 0.75:
            Val = y
        else:
            Val = 0.75
    else:
        if y >= x and y >= 0.75:
            if x >= 0.75:
                Val = x
            else:
                Val = 0.75
        else:
            if x >= y:
                Val = x
            else:
                Val = y
    Val = Val - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val


def fuzzy_130(x, y):
    Val = x + y - 0.5
    if Val > 1:
        Val = 1
    if Val < 0:
        Val = 0
    Val = math.sqrt(Val) - 2 * ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_121(x, y):
    return sorted([x, y, 0.75])[1]


def fuzzy_120(x, y):
    Val = x + y - 0.5
    if Val > 1:
        Val = 1
    if Val < 0:
        Val = 0
    Val = math.sqrt(Val) - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_111(x, y):
    Val = math.sqrt((x + y) / 2)
    return Val

def fuzzy_110(x, y):
    Val = x + y - 0.5
    if Val > 1:
        Val = 1
    if Val < 0:
        Val = 0
    Val = math.sqrt(Val)
    return Val

def fuzzy_100(x, y):
    Val = x + y - 0.5
    if Val > 1:
        Val = 1
    if Val < 0:
        Val = 0
    Val = math.sqrt(Val) + ((1 - x) * (1 - y))
    return Val

def fuzzy_040(x, y):
    Val = (x * y) + abs(x - y) - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_030(x, y):
    Val = (x * y) + abs(x - y)
    return Val

def fuzzy_020(x, y):
    if x >= y:
        Val = x
    else:
        Val = y
    return Val

def fuzzy_010(x, y):
    Val = x + y - (x * y)
    return Val

def fuzzy_000(x, y):
    Val = x + y
    if Val > 1:
        Val = 1
    return Val


class FuzzyAggregateDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(FuzzyAggregateDialog, self).__init__(parent)
        self.setupUi(self)

        # Initialisation
        self.layerCombo1.currentIndexChanged.connect(self.populate_field_combo1)
        self.layerCombo2.currentIndexChanged.connect(self.populate_field_combo2)

        # Charger les couches GeoPackage uniquement
        self.populate_layer_combos()
        self.populate_field_combo1()
        self.populate_field_combo2()
        self.btnShowMetadata.clicked.connect(self.show_metadata_table)       
        self.defineFunctionButton.clicked.connect(self.open_aggregation_function_dialog)
        self.buttonBox.accepted.connect(self.run_aggregation)
        self.buttonBox.rejected.connect(self.reject)
        layer_names = self.vector_layer_names()
        self.layer_map = {}
        # Construit le dictionnaire couche -> nom
        for layer in QgsProject.instance().mapLayers().values():
            if layer.type() == layer.VectorLayer and layer.dataProvider().name() == 'ogr':
                source = layer.source().lower()
                if source.endswith('.gpkg') or '.gpkg|' in source:
                    self.layer_map[layer.name()] = layer
            if not layer_names:
                QMessageBox.information(
                    self,
                    self.tr("Aucune couche valide"),
                    self.tr("Aucune couche vectorielle provenant d’un fichier .gpkg ou d’une base PostGIS n’est chargée dans le projet.\n"
                            "Veuillez en ajouter une pour utiliser ce plugin.")
                )

        
        # Initialiser self.current_layer avec la première couche sélectionnée
        if layer_names:
            self.current_layer = self.layer_map.get(layer_names[0])
    def showEvent(self, event):
        super().showEvent(event)
        self.populate_layer_combos()
        self.populate_field_combo1()
        self.populate_field_combo2()

    def vector_layer_names(self):
        """
        Retourne la liste des noms de couches formatés pour affichage :
        [GPKG] nom_couche   ou   [PG] schema.table
        """
        names = []
        for layer in QgsProject.instance().mapLayers().values():
            if not isinstance(layer, QgsVectorLayer):
                continue

            provider = layer.dataProvider().name().lower()
            source = layer.source()

            # Cas GeoPackage
            if provider == "ogr" and (source.lower().endswith(".gpkg") or ".gpkg|" in source.lower()):
                names.append(f"[GPKG] {layer.name()}")

            # Cas PostGIS
            elif provider in ["postgres", "postgis"]:
                schema, table = None, None
                parts = source.split(" ")
                for part in parts:
                    if part.startswith("table="):
                        table_full = part.split("=")[1]
                        if "." in table_full:
                            schema, table = table_full.split(".", 1)
                        else:
                            table = table_full
                if schema and table:
                    names.append(f"[PG] {schema}.{table}")
                else:
                    names.append(f"[PG] {layer.name()}")

        return names

    def populate_layer_combos(self):
        self.layerCombo1.clear()
        self.layerCombo2.clear()
        layer_names = []
        self.layer_map = {}

        for layer in QgsProject.instance().mapLayers().values():
            if not isinstance(layer, QgsVectorLayer):
                continue

            provider = layer.dataProvider().name().lower()
            source = layer.source()

            # Cas GeoPackage
            if provider == "ogr" and (source.lower().endswith(".gpkg") or ".gpkg|" in source.lower()):
                display_name = f"[GPKG] {layer.name()}"
                self.layer_map[display_name] = layer
                layer_names.append(display_name)

            # Cas PostGIS
            elif provider in ["postgres", "postgis"]:
                uri = QgsDataSourceUri(source)
                schema = uri.schema() or "public"
                table = uri.table()
                display_name = f"[PG] {schema}.{table}" if table else f"[PG] {layer.name()}"
                self.layer_map[display_name] = layer
                layer_names.append(display_name)

            else:
                # On ignore les autres types de couches
                continue

            # Ajout dans les deux combos, avec l’objet layer en data
            self.layerCombo1.addItem(display_name, layer)
            self.layerCombo2.addItem(display_name, layer)

        # Recharge les champs de la première sélection
        self.populate_field_combo1()
        self.populate_field_combo2()


    def populate_field_combo1(self):
        self.fieldCombo1.clear()
        layer = self.layerCombo1.currentData()
        if layer:
            for field in layer.fields():
                if field.name().endswith('_fuzzy'):
                    self.fieldCombo1.addItem(field.name())



    def populate_field_combo2(self):
        self.fieldCombo2.clear()
        layer = self.layerCombo2.currentData()
        if layer:
            for field in layer.fields():
                if  field.name().endswith('_fuzzy'):
                    self.fieldCombo2.addItem(field.name())

 

    def get_inputs(self):
        return {
            "layer1": self.layer_map.get(self.layerCombo1.currentText()),
            "field1": self.fieldCombo1.currentText(),
            "layer2": self.layer_map.get(self.layerCombo2.currentText()),
            "field2": self.fieldCombo2.currentText(),
            "operation": "intersection" if self.radioIntersection.isChecked() else "union",
            "result_name": self.resultLayerName.text()+ "_agg"
        }
    def open_aggregation_function_dialog(self):
        from .aggregation_function_dialog import AggregationFunctionDialog

        # Récupérer les noms des couches sélectionnées dans les comboBox
        nom_couche_1 = f"{self.layerCombo1.currentText()}/{self.fieldCombo1.currentText()}"
        nom_couche_2 = f"{self.layerCombo2.currentText()}/{self.fieldCombo2.currentText()}"

        dlg = AggregationFunctionDialog()
        dlg.set_criteria_labels(nom_couche_1, nom_couche_2)

        # ➕ Initialiser les radios si un code existe déjà
        if hasattr(self, "aggregation_function_code") and self.aggregation_function_code:
            dlg.set_selected_values(self.aggregation_function_code)

            # ➕ Optionnel : cocher la case "symétrie" si code symétrique
            if self.aggregation_function_code[0] == self.aggregation_function_code[3]:
                dlg.checkSymmetry.setChecked(True)
                dlg.group4.show()
                dlg.line.show()
                dlg.label_symmetry_test.show()
            else:
                dlg.checkSymmetry.setChecked(False)
                dlg.group4.hide()
                dlg.line.hide()
                dlg.label_symmetry_test.hide()

        # ➕ Lancement du dialogue
        if dlg.exec_():
            result = dlg.get_selected_values()
            self.aggregation_function_code = result
            self.functionLabel.setText(f"Code sélectionné : {result}")

            
            
    def reset_fid_field(self,layer: QgsVectorLayer, log_tag: str = "FuzzyPlugin") -> QgsVectorLayer:
        
        # Crée une nouvelle couche mémoire sans champ 'fid'
        fields = layer.fields()
        fields_no_fid = QgsFields()
        for f in fields:
            if f.name().lower() != 'fid':
                fields_no_fid.append(f)
        
        crs = layer.crs()
        geom_type = layer.geometryType()
        
        new_layer = QgsVectorLayer(f"{QgsWkbTypes.displayString(layer.wkbType())}?crs={crs.authid()}", "temp", "memory")
        new_layer.dataProvider().addAttributes(fields_no_fid)
        new_layer.updateFields()
        
        feats = []
        for feat in layer.getFeatures():
            new_feat = QgsFeature()
            new_feat.setGeometry(feat.geometry())
            attr_values = [feat.attributes()[fields.indexFromName(f.name())] for f in fields_no_fid]
            new_feat.setAttributes(attr_values)
            feats.append(new_feat)
        
        new_layer.dataProvider().addFeatures(feats)
        new_layer.updateExtents()

        return new_layer


    def run_processing_to_output(self, alg, params, output_path, layer_name, overwrite=False, log_tag="FuzzyAggregation"):
        """
        Lance un algorithme de traitement et enregistre le résultat
        soit dans un GeoPackage (OGR), soit dans une table PostGIS.
        """

        try:
            provider = None
            if output_path.lower().endswith(".gpkg"):
                provider = "ogr"
            elif "dbname" in output_path and "table=" in output_path:
                provider = "postgres"

            # --- Cas GeoPackage ---
            if provider == "ogr":
                params["OUTPUT"] = "TEMPORARY_OUTPUT"
                result = processing.run(alg, params)

                if isinstance(result, dict):
                    output_layer = result.get("OUTPUT")
                else:
                    output_layer = result

                if not isinstance(output_layer, QgsVectorLayer):
                    raise Exception(self.tr("La sortie n'est pas une couche vectorielle valide"))

                # Nettoyer FIDs
                cleaned_layer = self.reset_fid_field(output_layer, log_tag=log_tag)

                # Options d'écriture dans le GPKG
                options = QgsVectorFileWriter.SaveVectorOptions()
                options.driverName = "GPKG"
                options.layerName = layer_name
                options.fileEncoding = "UTF-8"
                options.actionOnExistingFile = (
                    QgsVectorFileWriter.CreateOrOverwriteLayer if overwrite
                    else QgsVectorFileWriter.CreateOrSkip
                )

                error = QgsVectorFileWriter.writeAsVectorFormatV3(
                    cleaned_layer,
                    output_path,
                    QgsProject.instance().transformContext(),
                    options
                )[0]

                if error != QgsVectorFileWriter.NoError:
                    raise Exception(f"Erreur d'écriture dans le GeoPackage : code {error}")

                QgsMessageLog.logMessage(
                    f"✅ Résultat sauvegardé dans {output_path} (couche : {layer_name})",
                    level=Qgis.Success,
                    tag=log_tag
                )

                return cleaned_layer

            # --- Cas PostGIS ---
            elif provider == "postgres":
                return 

            else:
                raise Exception(self.tr("Type de sortie non supporté (uniquement GPKG ou PostGIS)"))

        except Exception as e:
            QgsMessageLog.logMessage(f"❌ Erreur : {str(e)}", level=Qgis.Critical, tag=log_tag)
            raise

    def run_aggregation(self):
        function_code = getattr(self, 'aggregation_function_code', None)
        
        if not function_code:
            QMessageBox.warning(self, self.tr("Aucune fonction sélectionnée"),
                                self.tr("Veuillez d'abord sélectionner une fonction d'agrégation floue."))
            return

        # Vérification du type des couches
        layer1 = self.layerCombo1.currentData()
        layer2 = self.layerCombo2.currentData()
        if not layer1 or not layer2:
            QMessageBox.critical(self, "Erreur", "Veuillez sélectionner deux couches valides.")
            return

        provider1 = layer1.dataProvider().name().lower()
        provider2 = layer2.dataProvider().name().lower()

        # Autoriser uniquement ogr↔ogr (gpkg) ou postgres/postgis ↔ postgres/postgis
        if (provider1 in ["ogr"] and provider2 in ["ogr"]):
            pass  # ok -> GPKG
        elif (provider1 in ["postgres", "postgis"] and provider2 in ["postgres", "postgis"]):
            pass  # ok -> PostGIS
        else:
            QMessageBox.critical(
                self,
                self.tr("Erreur"),
                self.tr("Pour l'instant le plugin ne peut traiter que des couches de même type (deux GPKG ou deux PostGIS).")
            )
            return

        
        agg_functions = {
                "442": fuzzy_442,
                "441": fuzzy_441,
                "440": fuzzy_440,
                "130": fuzzy_130,
                "121": fuzzy_121,
                "120": fuzzy_120,
                "111": fuzzy_111,
                "110": fuzzy_110,
                "100": fuzzy_100,
                "040": fuzzy_040,
                "030": fuzzy_030,
                "020": fuzzy_020,
                "010": fuzzy_010,
                "000": fuzzy_000,
                "131": fuzzy_131,
                "140": fuzzy_140,
                "141": fuzzy_141,
                "200": fuzzy_200,
                "210": fuzzy_210,
                "211": fuzzy_211,
                "220": fuzzy_220,
                "221": fuzzy_221,
                "222": fuzzy_222,
                "230": fuzzy_230,
                "231": fuzzy_231,
                "232": fuzzy_232,
                "240": fuzzy_240,
                "241": fuzzy_241,
                "242": fuzzy_242,
                "300": fuzzy_300,
                "310": fuzzy_310,
                "311": fuzzy_311,
                "320": fuzzy_320,
                "321": fuzzy_321,
                "322": fuzzy_322,
                "330": fuzzy_330,
                "331": fuzzy_331,
                "332": fuzzy_332,
                "340": fuzzy_340,
                "341": fuzzy_341,
                "342": fuzzy_342,
                "400": fuzzy_400,
                "410": fuzzy_410,
                "411": fuzzy_411,
                "420": fuzzy_420,
                "421": fuzzy_421,
                "422": fuzzy_422,
                "430": fuzzy_430,
                "431": fuzzy_431,
                "432": fuzzy_432
            }
        # Test d’incohérence (pour code à 4 chiffres)
        
        code = self.aggregation_function_code  # 'XYZ' ou 'WXYZ'

        if not self.is_aggregation_code_consistent(function_code):
            details = self.explain_inconsistency(function_code)
            # Affiche un avertissement et demande confirmation
            
            reply = QMessageBox.question(
                self,
                self.tr("Vérification de la combinaison"),
                self.tr("La combinaison semble incohérente :\n\n{0}\n\nVoulez-vous procéder quand même ?").format(details),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return  # annuler le traitement

        
        
        
        # Traitement
        code3 = function_code[:3]
        code4 = function_code

        # Choix de la fonction d’agrégation
        if code4[0] == code4[3]:  # Symétrique
            if code3 in agg_functions:
                func = agg_functions[code3]
                fuzzy_params = None
                function_id = f"fuzzy_{code3}"
            else:
                func, fuzzy_params = generate_fuzzy_function(code3)
                function_id = f"generated_fuzzy_{code3}"
                
        else:  # Asymétrique
            func, fuzzy_params = generate_asymmetric_function(code4)
            function_id = f"asymmetric_{code4}"

        if func is None:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("La fonction d’agrégation n’a pas pu être générée."))
            return

        

        layer1 = self.layerCombo1.currentData()
        layer2 = self.layerCombo2.currentData()
        field1 = self.fieldCombo1.currentText()
        field2 = self.fieldCombo2.currentText()
        output_name = self.outputLayerName.text().strip() + "_agg"
        agg_field_name = output_name

        if self.radioIntersection.isChecked():
            operation = "intersection"
        elif self.radioUnion.isChecked():
            operation = "union"
        else:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Veuillez sélectionner une opération."))
            return

        if not layer1 or not layer2 or not field1 or not field2 or not output_name:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Tous les champs doivent être remplis."))
            return

        try:
            algo = "native:intersection" if operation == "intersection" else "native:union"

            provider1 = layer1.dataProvider().name().lower()
            src = layer1.source()

            # --- Cas GeoPackage ---
            if provider1 == "ogr" and (src.lower().endswith(".gpkg") or "gpkg" in src.lower()):
                gpkg_path = src.split("|")[0]

                result = self.run_processing_to_output(
                    alg=algo,
                    params={
                        "INPUT": layer1,
                        "OVERLAY": layer2
                    },
                    output_path=gpkg_path,
                    layer_name=output_name,
                    overwrite=True
                )

                gpkg_layer_path = f"{gpkg_path}|layername={output_name}"
                real_layer = QgsVectorLayer(gpkg_layer_path, output_name, "ogr")
                # Debug : vérifier les champs disponibles
                all_fields = [f.name() for f in real_layer.fields()]
                print("Champs dans la couche résultante :", all_fields)

                # Trouver les vrais noms de champs résultants
                field1_out = next((f for f in all_fields if field1 in f), None)
                field2_out = next((f for f in all_fields if field2 in f), None)

                if not field1_out or not field2_out:
                    QMessageBox.warning(self, "Erreur", "Champs introuvables dans la couche résultante.")
                    return
                # Ajouter champ d’agrégation
                if agg_field_name not in all_fields:
                    real_layer.dataProvider().addAttributes([QgsField(agg_field_name, QVariant.Double)])
                    real_layer.updateFields()
                # Choix fonction d'agrégation floue
                
                real_layer.startEditing()
                # Initialiser les valeurs manquantes du champ à 0
                idx = real_layer.fields().indexFromName(agg_field_name)
                for f in real_layer.getFeatures():
                    if f[field1_out]in [None, NULL]:
                        f[field1_out] = 0.0
                        real_layer.updateFeature(f)
                for f in real_layer.getFeatures():
                    if f[field2_out]in [None, NULL]:
                        f[field2_out] = 0.0
                        real_layer.updateFeature(f)
                for f in real_layer.getFeatures():
                    try:
                        val1 = f[field1_out]
                        val2 = f[field2_out]
                        val1 = float(val1) if val1 not in [None, NULL] else 0.0
                        val2 = float(val2) if val2 not in [None, NULL] else 0.0
                        agg_val = func(val1, val2)
                        f[agg_field_name] = agg_val if agg_val is not None else 0.0
                        real_layer.updateFeature(f)
                    except Exception as e:
                        print(f"Erreur lors de l’agrégation : {e}")

                # Fin de l’édition
                real_layer.commitChanges()
                real_layer.updateFields()                    

                # --- Choix de la symbologie ---
                if self.radioGraduated.isChecked():
                    # ---- Symbole gradué (code actuel) ----
                    classes = [
                        (0.0, 0.125, "#ff0000", self.tr("0 – 0.125 (mauvais)")),          # rouge
                        (0.125, 0.375, "#ff7f00", self.tr("0.125 – 0.375 (médiocre)")),   # orange
                        (0.375, 0.625, "#ffff00", self.tr("0.375 – 0.625 (moyen)")),      # jaune
                        (0.625, 0.875, "#7fff00", self.tr("0.625 – 0.875 (bon)")),        # vert clair
                        (0.875, 1.0, "#006400", self.tr("0.875 – 1.0 (très bon)"))        # vert foncé
                    ]

                    ranges = []
                    for min_val, max_val, color, label in classes:
                        symbol = QgsSymbol.defaultSymbol(real_layer.geometryType())
                        symbol.setColor(QColor(color))
                        rng = QgsRendererRange(min_val, max_val, symbol, label)
                        ranges.append(rng)

                    renderer = QgsGraduatedSymbolRenderer(agg_field_name, ranges)
                    renderer.setMode(QgsGraduatedSymbolRenderer.Custom)
                    real_layer.setRenderer(renderer)

                elif self.radioRamp.isChecked():
                    # Vérifie si la rampe 'AboveAndBelow' existe dans le style QGIS
                    style = QgsStyle.defaultStyle()
                    ramp = style.colorRamp('AboveAndBelow')

                    if ramp is None:
                        ramp_name = 'Spectral'   # fallback si AboveAndBelow n’existe pas
                    else:
                        ramp_name = 'AboveAndBelow'

                    # ---- Symbole avec rampe de couleur ----
                    expr = f"""
                        ramp_color(
                          '{ramp_name}',
                          scale_linear(
                            "{agg_field_name}",
                            mean("{agg_field_name}") - stdev("{agg_field_name}"),
                            mean("{agg_field_name}") + stdev("{agg_field_name}"),
                            0, 1
                          )
                        )
                    """

                    symbol = QgsSymbol.defaultSymbol(real_layer.geometryType())
                    layer0 = symbol.symbolLayer(0)

                    geom_type = real_layer.geometryType()
                    if geom_type == QgsWkbTypes.PolygonGeometry:
                        layer0.setDataDefinedProperty(QgsSymbolLayer.PropertyFillColor, QgsProperty.fromExpression(expr))
                    elif geom_type == QgsWkbTypes.LineGeometry:
                        layer0.setDataDefinedProperty(QgsSymbolLayer.PropertyStrokeColor, QgsProperty.fromExpression(expr))
                    elif geom_type == QgsWkbTypes.PointGeometry:
                        layer0.setDataDefinedProperty(QgsSymbolLayer.PropertyFillColor, QgsProperty.fromExpression(expr))

                    # Contour en gris transparent pour polygones
                    if geom_type == QgsWkbTypes.PolygonGeometry:
                        layer0.setStrokeColor(QColor(0, 0, 0, 50))

                    real_layer.setRenderer(QgsSingleSymbolRenderer(symbol))
                # Rafraîchir la couche
                real_layer.triggerRepaint()
                QgsProject.instance().addMapLayer(real_layer)

                # Sauvegarder comme style par défaut si demandé
                if self.checkDefaultStyle.isChecked():
                    ok, errMsg = real_layer.saveDefaultStyle()
                    if not ok:
                        QgsMessageLog.logMessage(
                            f"Erreur en sauvegardant le style : {errMsg}",
                            "FuzzyAggregate",
                            Qgis.Warning
                        )

            # --- Cas PostGIS ---
            elif provider1 in ["postgres", "postgis"]:
                # appel direct à notre fonction SQL
                try:
                    real_layer = overlay_postgis(
                        layer1=layer1,
                        layer2=layer2,
                        operation=operation,   # "intersection" ou "union"
                        output_table=output_name.lower()
                    )

                except Exception as e:
                    raise Exception(f"Erreur lors de l'opération PostGIS ({operation}) : {e}")

                # --- Ajout champ d’agrégation et calcul ---
                all_fields = [f.name() for f in real_layer.fields()]
                field1="a_"+ field1
                field2="b_"+ field2
                field1_out = next((f for f in all_fields if f == field1), None)
                field2_out = next((f for f in all_fields if f == field2), None)

                if not field1_out or not field2_out:
                    QMessageBox.warning(self, self.tr("Erreur"), self.tr("Champs introuvables dans la couche résultante."))
                    return
        except Exception as e:
            raise Exception(f"Erreur lors de l'opération spatiale")
        QgsMessageLog.logMessage(f"Début de l’agrégation sur la couche '{output_name}'", tag="FuzzyAggregation", level=Qgis.Info)

        real_layer.startEditing()
        
        

        # --- Nom du champ sécurisé pour PostgreSQL ---
        safe_name = re.sub(r'\W+', '_', agg_field_name.lower())  # minuscules et _ seulement
        safe_name = safe_name[:63]  # PostgreSQL limite les noms à 63 caractères

        # --- Vérifier si le champ existe déjà ---
        all_fields = [f.name() for f in real_layer.fields()]
        if safe_name not in all_fields:
            new_field = QgsField(safe_name, QVariant.Double)
            res = real_layer.dataProvider().addAttributes([new_field])
            real_layer.updateFields()
            if res != [True]:
                raise Exception(f"Erreur PostGIS lors de l'ajout du champ '{safe_name}'")
        else:
            QgsMessageLog.logMessage(f"Le champ '{safe_name}' existe déjà.", "FuzzyAggregation", Qgis.Info)

        # --- Récupérer l'index du champ pour l’agrégation ---
        idx = real_layer.fields().indexFromName(safe_name)
        if idx == -1:
            raise Exception(f"Impossible de récupérer l’index du champ '{safe_name}'")
        
        
        
        
        
        

        # Préparer toutes les modifications en une seule passe
        changes = {}
        for f in real_layer.getFeatures():
            try:
                # sécurisation : si None, alors 0.0
                val1 = f[field1_out]
                val2 = f[field2_out]
                v1 = float(val1) if val1 not in (None, "") else 0.0
                v2 = float(val2) if val2 not in (None, "") else 0.0
                agg_val = func(v1, v2)
                
                # si la fonction renvoie None, forcer à 0.0
                if agg_val is None:
                    agg_val = 0.0

                changes[f.id()] = {idx: agg_val}
            except Exception as e:
                QgsMessageLog.logMessage(
                    f"Erreur lors de l’agrégation (fid={f.id()}) : {e}",
                    tag="FuzzyAggregation",
                    level=Qgis.Warning
                )

        # Appliquer toutes les modifs d’un coup
        if changes:
            real_layer.dataProvider().changeAttributeValues(changes)

        real_layer.commitChanges()
        


# --- Appliquer la symbologie ---
        if self.radioGraduated.isChecked():
            # Symbole gradué
            classes = [
                (0.0, 0.125, "#ff0000", self.tr("0 – 0.125 (mauvais)")),
                (0.125, 0.375, "#ff7f00", self.tr("0.125 – 0.375 (médiocre)")),
                (0.375, 0.625, "#ffff00", self.tr("0.375 – 0.625 (moyen)")),
                (0.625, 0.875, "#7fff00", self.tr("0.625 – 0.875 (bon)")),
                (0.875, 1.0, "#006400", self.tr("0.875 – 1.0 (très bon)"))
            ]
            ranges = []
            for min_val, max_val, color, label in classes:
                symbol = QgsSymbol.defaultSymbol(real_layer.geometryType())
                symbol.setColor(QColor(color))
                rng = QgsRendererRange(min_val, max_val, symbol, label)
                ranges.append(rng)
            renderer = QgsGraduatedSymbolRenderer(agg_field_name, ranges)
            renderer.setMode(QgsGraduatedSymbolRenderer.Custom)
            real_layer.setRenderer(renderer)

        elif self.radioRamp.isChecked():
            # Vérifie si la rampe 'AboveAndBelow' existe dans le style QGIS
            style = QgsStyle.defaultStyle()
            ramp = style.colorRamp('AboveAndBelow')

            if ramp is None:
                ramp_name = 'Spectral'   # fallback si AboveAndBelow n’existe pas
            else:
                ramp_name = 'AboveAndBelow'

            # ---- Symbole avec rampe de couleur ----
            expr = f"""
                ramp_color(
                  '{ramp_name}',
                  scale_linear(
                    "{agg_field_name}",
                    mean("{agg_field_name}") - stdev("{agg_field_name}"),
                    mean("{agg_field_name}") + stdev("{agg_field_name}"),
                    0, 1
                  )
                )
            """

            symbol = QgsSymbol.defaultSymbol(real_layer.geometryType())
            layer0 = symbol.symbolLayer(0)
            geom_type = real_layer.geometryType()

            if geom_type == QgsWkbTypes.PolygonGeometry:
                layer0.setDataDefinedProperty(QgsSymbolLayer.PropertyFillColor, QgsProperty.fromExpression(expr))
                layer0.setStrokeColor(QColor(0,0,0,50))
            elif geom_type == QgsWkbTypes.LineGeometry:
                layer0.setDataDefinedProperty(QgsSymbolLayer.PropertyStrokeColor, QgsProperty.fromExpression(expr))
            elif geom_type == QgsWkbTypes.PointGeometry:
                layer0.setDataDefinedProperty(QgsSymbolLayer.PropertyFillColor, QgsProperty.fromExpression(expr))

            real_layer.setRenderer(QgsSingleSymbolRenderer(symbol))

        # Rafraîchir
        real_layer.triggerRepaint()
        QgsProject.instance().addMapLayer(real_layer)
         
        if self.checkDefaultStyle.isChecked():
            if not save_postgis_default_style_from_layer(real_layer, schema='plugin', style_name='default'):
                QgsMessageLog.logMessage(
                    "Erreur lors de la sauvegarde du style par défaut PostGIS",
                    "FuzzyAggregate",
                    Qgis.Warning
                )
        
        
        QgsProject.instance().addMapLayer(real_layer)

        QgsMessageLog.logMessage(f"Agrégation terminée pour la couche '{output_name}'", tag="FuzzyAggregation", level=Qgis.Info)
        QMessageBox.information(self, self.tr("Succès"), self.tr(f"Couche '{output_name}' créée avec succès."))

        # --- Métadonnées ---
        try:
            source1_str = f"{self.layerCombo1.currentText()}/{field1}"
            source2_str = f"{self.layerCombo2.currentText()}/{field2}"

            if provider1 == "ogr":
                # GeoPackage
                self.ensure_metadata_table_exists(gpkg_path)
                self.append_metadata(
                    gpkg_path=gpkg_path,
                    field_name=agg_field_name,
                    fuzzy_type=function_id,
                    params=fuzzy_params,
                    source1=source1_str,
                    source2=source2_str,
                    provider="ogr"
                )

            elif provider1 in ["postgres", "postgis"]:
                # PostGIS
                layer = layer1  # couche source
                uri = QgsDataSourceUri(layer.source())
                schema = uri.schema() or "public"

                self.append_metadata(
                    field_name=agg_field_name,
                    fuzzy_type=function_id,
                    params=fuzzy_params,
                    source1=source1_str,
                    source2=source2_str,
                    schema=schema,
                    provider="postgres",
                    layer=layer      # <-- AJOUT
                )

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur pendant l'ajout des métadonnées :\n{e}")


    def ensure_metadata_table_exists(self, layer):
        """
        Vérifie (et crée si besoin) la table metafuzzy dans le même GPKG ou schéma PostGIS que la couche donnée.
        Retourne True si la table existe ou a été créée, False sinon.
        """
        try:
            source = layer.source()
            #QgsMessageLog.logMessage(f"[DEBUG] Source de la couche : {source}", "FuzzyPlugin")

            # ---------------------------
            # Cas 1 : GeoPackage
            # ---------------------------
            if source.lower().endswith(".gpkg") or "|layername=" in source:
                gpkg_path = source.split("|")[0]
                #QgsMessageLog.logMessage(f"[DEBUG] Mode GPKG, chemin={gpkg_path}", "FuzzyPlugin")

                uri = f"{gpkg_path}|layername=metafuzzy"
                meta_layer = QgsVectorLayer(uri, "metafuzzy", "ogr")

                if meta_layer.isValid():
                    QgsMessageLog.logMessage("[DEBUG] Table metafuzzy déjà présente dans GPKG", "FuzzyPlugin")
                    return True  # déjà présent

                
                # Crée un layer mémoire sans géométrie
                fields = QgsFields()
                fields.append(QgsField("sourcefield", QVariant.String))
                fields.append(QgsField("function", QVariant.String))
                fields.append(QgsField("params", QVariant.String))
                fields.append(QgsField("source1", QVariant.String))
                fields.append(QgsField("source2", QVariant.String))
                fields.append(QgsField("datecreated", QVariant.String))
                fields.append(QgsField("username", QVariant.String))

                mem_layer = QgsVectorLayer("None", "metafuzzy", "memory")
                mem_layer.dataProvider().addAttributes(fields)
                mem_layer.updateFields()

                options = QgsVectorFileWriter.SaveVectorOptions()
                options.driverName = "GPKG"
                options.layerName = "metafuzzy"
                options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer

                err, _ = QgsVectorFileWriter.writeAsVectorFormatV2(
                    layer=mem_layer,
                    fileName=gpkg_path,
                    transformContext=QgsProject.instance().transformContext(),
                    options=options
                )
                
                return err == QgsVectorFileWriter.NoError

            # ---------------------------
            # Cas 2 : PostGIS
            # ---------------------------
            elif "dbname=" in source:
                

                from qgis.core import QgsDataSourceUri
                import psycopg2

                uri = QgsDataSourceUri(source)
                schema = uri.schema() or "public"
                database = uri.database()
                host = uri.host()
                port = uri.port()
                user = uri.username()
                pwd = uri.password()
                

                conn = psycopg2.connect(
                    dbname=database, user=user, password=pwd,
                    host=host, port=port
                )
                cur = conn.cursor()

                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = %s 
                        AND table_name = 'metafuzzy'
                    );
                """, (schema,))
                exists = cur.fetchone()[0]
                

                if not exists:
                    
                    cur.execute(f"""
                        CREATE TABLE {schema}.metafuzzy (
                            id SERIAL PRIMARY KEY,
                            sourcefield TEXT,
                            function TEXT,
                            params TEXT,
                            source1 TEXT,
                            source2 TEXT,
                            datecreated TIMESTAMP,
                            username TEXT
                        );
                    """)
                    conn.commit()

                    cur.execute(f'GRANT ALL PRIVILEGES ON TABLE {schema}.metafuzzy TO {user};')
                    conn.commit()
                    QgsProject.instance().reloadAllLayers()

                cur.close()
                conn.close()
                QgsApplication.processEvents()

                # Charger la table dans QGIS
                meta_uri = QgsDataSourceUri()
                meta_uri.setConnection(host, str(port), database, user, pwd)
                meta_uri.setDataSource(schema, "metafuzzy", None)  # None = pas de géométrie
                

                metafuzzy_layer = QgsVectorLayer(meta_uri.uri(), "metafuzzy", "postgres")
                

                if not metafuzzy_layer.isValid():
                    QgsMessageLog.logMessage(
                       self.tr( "Impossible de charger la table 'metafuzzy' dans QGIS", "FuzzyPlugin")
                    )
                    return False

                return True

            else:
                QgsMessageLog.logMessage(self.tr("Source inconnue (ni GPKG ni PostGIS)", "FuzzyPlugin"))
                return False

        except Exception as e:
            QgsMessageLog.logMessage(f"[DEBUG] Exception ensure_metadata_table_exists: {e}", "FuzzyPlugin")
            return False


    def append_metadata(self, gpkg_path=None, field_name=None, fuzzy_type=None,
                        params=None, source1=None, source2=None,
                        schema=None, provider="ogr", layer=None):
        """
        Ajoute une ligne dans la table 'metafuzzy'.
        Pour GeoPackage : utilise QgsVectorLayer
        Pour PostGIS : crée la table si nécessaire et insère directement en SQL
        """
        try:
            

            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            user = getpass.getuser()

            if provider == "ogr":
                # --- GeoPackage ---
                uri = f"{gpkg_path}|layername=metafuzzy"
                metafuzzy_layer = QgsVectorLayer(uri, "metafuzzy", "ogr")
                if not metafuzzy_layer.isValid():
                    raise Exception(f"La table 'metafuzzy' est introuvable dans le GeoPackage {gpkg_path}")

                metafuzzy_layer.startEditing()
                f = QgsFeature(metafuzzy_layer.fields())
                f.setAttribute("sourcefield", field_name)
                f.setAttribute("function", fuzzy_type)
                f.setAttribute("params", str(params))
                f.setAttribute("source1", source1 or "")
                f.setAttribute("source2", source2 or "")
                f.setAttribute("datecreated", date_str)
                f.setAttribute("username", user)
                metafuzzy_layer.addFeature(f)
                metafuzzy_layer.commitChanges()

            elif provider in ["postgres", "postgis"]:
                # --- PostGIS ---
                if not layer:
                    raise Exception("Layer PostGIS manquant pour append_metadata")

                uri = QgsDataSourceUri(layer.source())
                schema = schema or uri.schema() or "public"

                # Connexion psycopg2
                conn = psycopg2.connect(
                    dbname=uri.database(),
                    user=uri.username(),
                    password=uri.password(),
                    host=uri.host(),
                    port=uri.port()
                )
                cur = conn.cursor()

                # Crée la table si elle n'existe pas
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {schema}.metafuzzy (
                        id SERIAL PRIMARY KEY,
                        sourcefield TEXT,
                        function TEXT,
                        params TEXT,
                        source1 TEXT,
                        source2 TEXT,
                        datecreated TIMESTAMP,
                        username TEXT
                    )
                """)
                         
                # Insert de la ligne
                cur.execute(f"""
                    INSERT INTO {schema}.metafuzzy
                    (sourcefield, function, params, source1, source2, datecreated, username)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (field_name, fuzzy_type, str(params), source1 or "", source2 or "",
                      date_str, user))

                conn.commit()
                cur.close()
                conn.close()

            else:
                raise Exception(f"Provider non supporté : {provider}")

        except Exception as e:
            QgsMessageLog.logMessage(f"Erreur append_metadata: {e}", "FuzzyPlugin", Qgis.Critical)

    def get_layer_path(self, layer: QgsVectorLayer) -> str:
        """
        Retourne le chemin du fichier GeoPackage associé à la couche.
        """
        source = layer.source()
        if "|layername=" in source:
            return source.split("|")[0]  # garde uniquement le chemin avant le |
        return source


    def get_layer_schema_table(self, layer: QgsVectorLayer) -> tuple:
        """
        Retourne (schema, table) pour une couche PostGIS.
        Si le schema n'est pas défini, renvoie 'public'.
        """
        source = layer.source()
        schema, table = None, None

        for part in source.split(" "):
            if part.startswith("table="):
                table_full = part.split("=")[1].strip('"')  # enlève guillemets éventuels
                if "." in table_full:
                    schema, table = table_full.split(".", 1)
                else:
                    schema, table = "public", table_full
                break

        if not schema or not table:
            raise Exception(f"1348 Impossible de déterminer schema.table pour la couche {layer.name()}")

        return schema, table
    def get_metafuzzy_layer(self, layer: QgsVectorLayer) -> QgsVectorLayer:
        provider = layer.dataProvider().name().lower()

        if provider == "ogr":
            # GeoPackage
            gpkg_path = layer.source().split("|")[0]
            uri = f"{gpkg_path}|layername=metafuzzy"
            return QgsVectorLayer(uri, "metafuzzy", "ogr")

        elif provider in ["postgres", "postgis"]:
            schema, _ = self.get_layer_schema_table(layer)
            geom_field = "geom"

            # On essaie de récupérer le champ géométrique si présent dans la source
            for part in layer.source().split(" "):
                if part.startswith("geometry="):
                    geom_field = part.split("=")[1]

            # Construction de l'URI sécurisé
            source = layer.source()
            # Remplace la partie table=... par table="schema"."metafuzzy"
            uri = re.sub(r'table=[^\s]+', f'table="{schema}"."metafuzzy"', source)
            if 'geometry=' not in uri:
                uri += f" ({geom_field})"

            metafuzzy_layer = QgsVectorLayer(uri, "metafuzzy", "postgres")
            if metafuzzy_layer.isValid():
                return metafuzzy_layer

        return None

    
    def show_metadata_table(self):
        layer_name = self.layerCombo1.currentText()
        
        layer = self.layer_map.get(layer_name)
        if not layer:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Aucune couche sélectionnée."))
            return

        # Assure que la table metafuzzy existe
        if not self.ensure_metadata_table_exists(layer):
            QMessageBox.information(self, self.tr("Info"), self.tr("1393 Impossible de créer ou charger la table 'metafuzzy'."))
            return

        source = layer.source()

        # ---------------------------
        # Cas 1 : GeoPackage
        # ---------------------------
        if source.lower().endswith(".gpkg") or "|layername=" in source:
            gpkg_path = source.split("|")[0]
            uri = f"{gpkg_path}|layername=metafuzzy"
            metafuzzy_layer = QgsVectorLayer(uri, "metafuzzy", "ogr")

        # ---------------------------
        # Cas 2 : PostGIS
        # ---------------------------
        elif "dbname=" in source:
            from qgis.core import QgsDataSourceUri
            uri = QgsDataSourceUri(source)
            schema = uri.schema() or "public"
            database = uri.database()
            host = uri.host()
            port = uri.port()
            user = uri.username()
            pwd = uri.password()

            # Construire URI QGIS pour la table metafuzzy
            meta_uri = QgsDataSourceUri()
            meta_uri.setConnection(host, str(port), database, user, pwd)
            meta_uri.setDataSource(schema, "metafuzzy", None)  # None = pas de géométrie

            metafuzzy_layer = QgsVectorLayer(meta_uri.uri(), "metafuzzy", "postgres")

        else:
            QMessageBox.warning(self, self.tr("Erreur"),
                                self.tr("Format de source non reconnu (ni GPKG ni PostGIS)."))
            return

        # ---------------------------
        # Vérification de validité
        # ---------------------------
        if not metafuzzy_layer.isValid():
            QMessageBox.information(self, self.tr("Info"),
                                    self.tr("Aucune table 'metafuzzy' trouvée."))
            return


        # ---------------------------
        # Création de la boîte de dialogue
        # ---------------------------
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("Historique des transformations"))
        layout = QVBoxLayout()

        table = QTableWidget()
        fields = metafuzzy_layer.fields()
        features = list(metafuzzy_layer.getFeatures())

        table.setColumnCount(len(fields))
        table.setRowCount(len(features))
        table.setHorizontalHeaderLabels([f.name() for f in fields])

        for row_idx, feat in enumerate(features):
            for col_idx, field in enumerate(fields):
                val = feat.attribute(field.name())
                
                # Conversion sécurisée en string
                if isinstance(val, QDateTime):
                    val_str = val.toString("yyyy-MM-dd HH:mm:ss")  # chaîne lisible
                elif hasattr(val, "toPyDateTime"):  
                    # pour PyQt5.QtCore.QDateTime encapsulé
                    val_str = val.toPyDateTime().strftime("%Y-%m-%d %H:%M:%S")
                else:
                    val_str = str(val) if val is not None else ""
                val_str = val_str.replace("PyQt5.QtCore.QDateTime", "")
                table.setItem(row_idx, col_idx, QTableWidgetItem(val_str))
        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.resize(700, 400)
        dialog.exec_()
          
    def load_translator(self):
        from qgis.PyQt.QtCore import QTranslator, QLocale, QCoreApplication
        from qgis.core import QgsApplication
        import os

        # Obtenir la langue actuelle de QGIS (ex : 'fr')
        locale_name = QgsApplication.instance().locale()
        locale = QLocale(locale_name).name()[0:2]  # 'fr', 'en', etc.
        from qgis.core import QgsMessageLog, Qgis
        QgsMessageLog.logMessage(f"Langue QGIS détectée : {locale}", "FuzzyAttributes", Qgis.Info)



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

    def _decode_digit(self,d):
        """'0'→1.0, '1'→0.75, '2'→0.5, '3'→0.25, '4'→0.0"""
        mapping = {"0": 1.0, "1": 0.75, "2": 0.5, "3": 0.25, "4": 0.0}
        return mapping.get(d, None)

    def _extract_Rs(self,code):
        """
        Retourne (R1, R2, R3) selon la logique demandée ou (None, None, None)
        si le code ne doit pas être vérifié (ex: 4 chiffres asymétrique) ou invalide.
        - 3 chiffres (symétrique) : R1=code[0], R2=code[1], R3=code[2]
        - 4 chiffres :
            * asymétrique (code[0] != code[3]) → None (on ne vérifie pas)
            * symétrique (code[0] == code[3]) :
                R1=code[3] (A=0,B=1), R2=code[1] (0.5,0.5), R3=code[2] (0.5,1)
        """
        if not code:
            return (None, None, None)

        code = code.strip()
        if len(code) == 3:
            R1 = self._decode_digit(code[0])
            R2 = self._decode_digit(code[1])
            R3 = self._decode_digit(code[2])
            if None in (R1, R2, R3):
                return (None, None, None)
            return (R1, R2, R3)

        if len(code) == 4:
            # asymétrique → on NE vérifie PAS
            if code[0] != code[3]:
                return (None, None, None)
            # symétrique → mêmes règles que 3 chiffres,
            # mais R1 doit venir du scénario (A=0,B=1) = 4e chiffre
            R1 = self._decode_digit(code[3])
            R2 = self._decode_digit(code[1])
            R3 = self._decode_digit(code[2])
            if None in (R1, R2, R3):
                return (None, None, None)
            return (R1, R2, R3)

        # autres longueurs : on ne vérifie pas
        return (None, None, None)

    def is_aggregation_code_consistent(self,code):
        """
        Renvoie True si le code est « cohérent » au sens des règles demandées,
        False si une règle est violée, et True si le code ne doit pas être vérifié
        (4 chiffres asymétrique) ou malformé (on ne bloque pas).
        Règles :
          1) R3 >= max(R1, R2)
          2) R3 >= 0.5
        """
        R1, R2, R3 = self._extract_Rs(code)
        # Pas de vérification (asym 4 chiffres, longueur inattendue, digits invalides)
        if R1 is None:
            return True
        if R3 < max(R1, R2):
            return False
        if R3 < 0.5:
            return False
        return True

    def explain_inconsistency(self,code):
        """
        Renvoie une chaîne expliquant quelle règle est violée,
        ou '' si tout est cohérent / non vérifiable.
        """
        R1, R2, R3 = self._extract_Rs(code)
        if R1 is None:
            return ""  # pas de vérification => pas de message
        msgs = []
        if R3 < max(R1, R2):
            msgs.append(self.tr(
                "Règle 1 violée : R3 (A=0,5 ; B=1) doit être >= max(R1, R2).")
            )
        if R3 < 0.5:
            msgs.append(self.tr(
                "Règle 2 violée : R3 (A=0,5 ; B=1) doit être >= 0,5.")
            )
        return "\n".join(msgs)




def generate_fuzzy_function(code):
    """
    Génère dynamiquement une fonction floue symétrique à partir d’un code à 3 chiffres
    """
    vals = {
        "0": 1.0,
        "1": 0.75,
        "2": 0.5,
        "3": 0.25,
        "4": 0.0
    }

    v1 = vals[code[0]]
    v2 = vals[code[1]]
    v3 = vals[code[2]]

    def fuzzy_func(x, y):
        if (x == 1 and y == 0) or (x == 0 and y == 1):
            return v1
        elif x == 0.5 and y == 0.5:
            return v2
        elif (x == 0.5 and y == 1) or (x == 1 and y == 0.5):
            return v3
        # Approximation continue entre ces points :
        val = v2 * x * y + v3 * abs(x - y)
        return max(0, min(1, val))
    params = {
        "type": "symétrique générée",
        "code": code,
        "points_clés": {
            "(1,0)/(0,1)": v1,
            "(0.5,0.5)": v2,
            "(0.5,1)/(1,0.5)": v3
        },
        "approximation": "v2 * x * y + v3 * |x - y|"
    }

    return fuzzy_func, params
    
def generate_asymmetric_function(code):
    vals = {
        "0": 1.0,
        "1": 0.75,
        "2": 0.5,
        "3": 0.25,
        "4": 0.0
    }

    vA1B0 = vals[code[0]]
    vA05B05 = vals[code[1]]
    vA05B1 = vals[code[2]]
    vA0B1 = vals[code[3]]

    def fuzzy_func(x, y):
        if x == 1 and y == 0:
            return vA1B0
        elif x == 0.5 and y == 0.5:
            return vA05B05
        elif x == 0.5 and y == 1:
            return vA05B1
        elif x == 0 and y == 1:
            return vA0B1
        # Interpolation générique
        val = vA05B05 * x * y + vA05B1 * x * abs(x - y) + vA0B1 * (1 - x) * y
        return max(0, min(1, val))
    params = {
        "type": "asymétrique générée",
        "code": code,
        "points_clés": {
            "(1,0)": vA1B0,
            "(0.5,0.5)": vA05B05,
            "(0.5,1)": vA05B1,
            "(0,1)": vA0B1
        },
        "approximation": "vA05B05 * x * y + vA05B1 * x * |x - y| + vA0B1 * (1 - x) * y"
    }

    return fuzzy_func, params
import re
from qgis.core import QgsVectorLayer, QgsProject
import psycopg2
from PyQt5.QtCore import QCoreApplication
_ = QCoreApplication.translate
def overlay_postgis(layer1, layer2, output_table, operation="intersection"):
    """
    Effectue une opération spatiale (intersection ou union) entre deux couches PostGIS
    et écrit le résultat dans une table PostGIS. Retourne la couche chargée dans QGIS.

    :param layer1: QgsVectorLayer PostGIS
    :param layer2: QgsVectorLayer PostGIS
    :param output_table: nom de la table résultat (ex: "inter1_agg")
    :param operation: "intersection" ou "union"
    """
    from qgis.core import QgsVectorLayer, QgsProject, QgsDataSourceUri, QgsField
    from PyQt5.QtCore import QVariant
    import psycopg2

    if layer1.providerType() not in ["postgres", "postgis"] or layer2.providerType() not in ["postgres", "postgis"]:
        raise Exception("Les deux couches doivent être PostGIS")

    uri1 = QgsDataSourceUri(layer1.source())
    schema = uri1.schema() or "public"
    conninfo = uri1.connectionInfo()
    table = output_table.lower()
    agg_field = table  # champ d’agrégation automatique

    # Récupération des noms de géométrie
    geom1 = layer1.dataProvider().geometryColumnName()
    geom2 = layer2.dataProvider().geometryColumnName()

    # Fonction pour créer des noms de champs valides pour SQL
    def sql_safe(field_name):
        safe_name = "".join([c if c.isalnum() or c=="_" else "_" for c in field_name])
        if safe_name[0].isdigit():
            safe_name = "_" + safe_name
        return safe_name

    # Récupération des champs et création liste SQL avec préfixes a_ et b_
    fields1 = [f.name() for f in layer1.fields() if f.name() != geom1]
    fields2 = [f.name() for f in layer2.fields() if f.name() != geom2]
    select_fields1 = ", ".join([f'a."{f}" AS a_{sql_safe(f)}' for f in fields1])
    select_fields2 = ", ".join([f'b."{f}" AS b_{sql_safe(f)}' for f in fields2])
    # Vérification que les deux couches ont le même SRID
    srid_a = layer1.crs().postgisSrid()
    srid_b = layer2.crs().postgisSrid()

    if srid_a != srid_b:
        # Deux choix possibles : soit bloquer, soit transformer
        # --- OPTION 1 : bloquer avec un message clair ---
        raise Exception(f"Les couches doivent avoir le même SRID (a={srid_a}, b={srid_b}). "
                        f"Veuillez reprojeter une couche avant de relancer.")

        # --- OPTION 2 : transformer automatiquement b vers le SRID de a ---
        # (à décommenter si tu veux l’appliquer automatiquement)
        # QMessageBox.warning(None, "SRID différent",
        #                     f"La couche B (SRID {srid_b}) a été reprojetée vers {srid_a}.")
        # srid_b = srid_a

    # Construction du SQL selon l'opération
    if operation == "intersection":
        geom_sql = f'ST_Intersection(a."{geom1}", b."{geom2}") AS geom'
        join_clause = f'FROM "{schema}"."{layer1.name()}" a JOIN "{schema}"."{layer2.name()}" b ON ST_Intersects(a."{geom1}", b."{geom2}")'
        sql = f"""
        CREATE TABLE "{schema}"."{table}" AS
        SELECT
            ROW_NUMBER() OVER () AS gid,
            {select_fields1},
            {select_fields2},
            {geom_sql}
        {join_clause};
        """
    elif operation == "union":
        sql = build_union_sql(layer1, layer2, schema, table, geom1, geom2,srid_a)
    else:
        raise Exception("Opération non supportée : choisir 'intersection' ou 'union'")

    # Connexion à Postgres
    conn = psycopg2.connect(conninfo)
    cur = conn.cursor()

    # Supprimer la table si elle existe
    cur.execute(f'DROP TABLE IF EXISTS "{schema}"."{table}" CASCADE;')
    conn.commit()

    # Création de la table résultat
    try:
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Erreur SQL PostGIS ({operation}) : {e}")

    # Ajouter le champ d’agrégation nommé comme la table
    try:
        cur.execute(f"""
            ALTER TABLE "{schema}"."{table}"
            ADD COLUMN IF NOT EXISTS "{table}" double precision;
        """)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Erreur création champ d’agrégation : {e}")
    finally:
        cur.close()
        conn.close()

    # Charger la couche dans QGIS
    uri_out = f"dbname='{uri1.database()}' host={uri1.host()} port={uri1.port()} user={uri1.username()} password={uri1.password()} schema={schema} table={table} (geom)"
    new_layer = QgsVectorLayer(uri_out, table, "postgres")
    if not new_layer.isValid():
        raise Exception("Impossible de charger la couche résultante")

    # --- Ajout du champ d'agrégation ---
    agg_field = output_table  # nom identique à la table
    provider = new_layer.dataProvider()
    if agg_field not in [f.name() for f in provider.fields()]:
        provider.addAttributes([QgsField(agg_field, QVariant.Double)])
        new_layer.updateFields()

    QgsProject.instance().addMapLayer(new_layer)

    # Définir la symbologie floue
    classes = [
        (0.0, 0.125, "#ff0000", QCoreApplication.translate("FuzzyAttributes", "0 – 0.125 (mauvais)")),
        (0.125, 0.375, "#ff7f00", QCoreApplication.translate("FuzzyAttributes", "0.125 – 0.375 (médiocre)")),
        (0.375, 0.625, "#ffff00", QCoreApplication.translate("FuzzyAttributes", "0.375 – 0.625 (moyen)")),
        (0.625, 0.875, "#7fff00", QCoreApplication.translate("FuzzyAttributes", "0.625 – 0.875 (bon)")),
        (0.875, 1.0, "#006400", QCoreApplication.translate("FuzzyAttributes", "0.875 – 1.0 (très bon)")),
    ]
    ranges = []
    for min_val, max_val, color, label in classes:
        symbol = QgsSymbol.defaultSymbol(new_layer.geometryType())
        symbol.setColor(QColor(color))
        rng = QgsRendererRange(min_val, max_val, symbol, label)
        ranges.append(rng)

    renderer = QgsGraduatedSymbolRenderer(agg_field, ranges)
    renderer.setMode(QgsGraduatedSymbolRenderer.Custom)

    new_layer.setRenderer(renderer)
    new_layer.triggerRepaint()
    return new_layer

def build_union_sql(layer1, layer2, schema, table, geom1, geom2, srid):
    """
    Construit une requête SQL pour une union spatiale complète entre deux couches PostGIS,
    en convertissant tous les attributs en TEXT pour homogénéiser les types.
    Forçage du type en MultiPolygon.
    """
    def sql_safe(name):
        safe = "".join(c if c.isalnum() or c == "_" else "_" for c in name)
        if safe and safe[0].isdigit():
            safe = "_" + safe
        return safe or "field"

    # Champs hors géométrie
    fields1 = [f.name() for f in layer1.fields() if f.name() != geom1]
    fields2 = [f.name() for f in layer2.fields() if f.name() != geom2]

    # Tous les champs de a en TEXT
    a_cols = [f'CAST(a."{f}" AS text) AS a_{sql_safe(f)}' for f in fields1]
    # Tous les champs de b en TEXT
    b_cols = [f'CAST(b."{f}" AS text) AS b_{sql_safe(f)}' for f in fields2]

    # Colonnes NULL aussi en TEXT
    a_nulls = [f'NULL::text AS a_{sql_safe(f)}' for f in fields1]
    b_nulls = [f'NULL::text AS b_{sql_safe(f)}' for f in fields2]

    sql = f"""
    CREATE TABLE "{schema}"."{table}" AS
    WITH inter AS (
        SELECT
            {", ".join(a_cols + b_cols)},
            ST_SetSRID(
                ST_Multi(ST_CollectionExtract(ST_Intersection(a."{geom1}", b."{geom2}"), 3)),
                {srid}
            ) AS geom
        FROM "{schema}"."{layer1.name()}" a
        JOIN "{schema}"."{layer2.name()}" b
        ON ST_Intersects(a."{geom1}", b."{geom2}")
        WHERE NOT ST_IsEmpty(ST_Intersection(a."{geom1}", b."{geom2}"))
    ),
    aonly AS (
        SELECT
            {", ".join(a_cols + b_nulls)},
            ST_SetSRID(
                ST_Multi(ST_CollectionExtract(
                    ST_Difference(
                        a."{geom1}",
                        (
                            SELECT ST_Union(ST_Intersection(a2."{geom1}", b2."{geom2}"))
                            FROM "{schema}"."{layer1.name()}" a2
                            JOIN "{schema}"."{layer2.name()}" b2
                            ON ST_Intersects(a2."{geom1}", b2."{geom2}")
                        )
                    ), 3
                )),
                {srid}
            ) AS geom
        FROM "{schema}"."{layer1.name()}" a
        WHERE NOT ST_IsEmpty(ST_Difference(a."{geom1}", (
                SELECT ST_Union(ST_Intersection(a2."{geom1}", b2."{geom2}"))
                FROM "{schema}"."{layer1.name()}" a2
                JOIN "{schema}"."{layer2.name()}" b2
                ON ST_Intersects(a2."{geom1}", b2."{geom2}")
        )))
    ),
    bonly AS (
        SELECT
            {", ".join(a_nulls + b_cols)},
            ST_SetSRID(
                ST_Multi(ST_CollectionExtract(
                    ST_Difference(
                        b."{geom2}",
                        (
                            SELECT ST_Union(ST_Intersection(a2."{geom1}", b2."{geom2}"))
                            FROM "{schema}"."{layer1.name()}" a2
                            JOIN "{schema}"."{layer2.name()}" b2
                            ON ST_Intersects(a2."{geom1}", b2."{geom2}")
                        )
                    ), 3
                )),
                {srid}
            ) AS geom
        FROM "{schema}"."{layer2.name()}" b
        WHERE NOT ST_IsEmpty(ST_Difference(b."{geom2}", (
                SELECT ST_Union(ST_Intersection(a2."{geom1}", b2."{geom2}"))
                FROM "{schema}"."{layer1.name()}" a2
                JOIN "{schema}"."{layer2.name()}" b2
                ON ST_Intersects(a2."{geom1}", b2."{geom2}")
        )))
    )
    SELECT ROW_NUMBER() OVER () AS gid, *
    FROM (
        SELECT * FROM inter
        UNION ALL
        SELECT * FROM aonly
        UNION ALL
        SELECT * FROM bonly
    ) AS all_union;
    """

    return sql



def save_postgis_default_style_from_layer(layer, schema=None, style_name="default"):
    """
    Sauvegarde le style courant de `layer` dans layer_styles (PostGIS).
    Normalise le type en Polygon/LineString/Point (évite MultiSurface etc).
    """
    try:
        if layer.providerType().lower() not in ("postgres", "postgis"):
            QgsMessageLog.logMessage("La couche n'est pas PostGIS.", "FuzzyAggregate", Qgis.Warning)
            return False

        # --- Connexion / infos table ---
        uri = QgsDataSourceUri(layer.dataProvider().dataSourceUri())
        dbname = uri.database()
        host = uri.host()
        port = uri.port() or 5432
        user = uri.username()
        password = uri.password()
        tbl_schema = schema or (uri.schema() or "public")
        tbl_name = uri.table()
        geom_col = uri.geometryColumn() or "geom"

        # --- Récupérer QML du style courant (tentative "fiable") ---
        qml_str = ""
        try:
            style_obj = QgsMapLayerStyle()
            style_obj.readFromLayer(layer)
            qml_str = style_obj.xmlData() or ""
        except Exception:
            qml_str = ""

        # fallback : demander à QGIS d'écrire un QML temporaire si xmlData vide
        if not qml_str.strip():
            try:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".qml")
                tmp.close()
                # saveNamedStyle prend un chemin et écrit le qml
                layer.saveNamedStyle(tmp.name)
                with open(tmp.name, "r", encoding="utf-8") as f:
                    qml_str = f.read()
                os.unlink(tmp.name)
            except Exception as ex:
                QgsMessageLog.logMessage(f"Impossible d'exporter le style QML (fallback) : {ex}", "FuzzyAggregate", Qgis.Warning)
                qml_str = ""

        # --- Normaliser le type géométrique en valeurs canoniques ---
        geom_type_txt = "Polygon"  # choix conservateur

        # si style_name est 'default' ou vide, on met le nom de la table (plus parlant)
        style_name_eff = tbl_name if (style_name in (None, "", "default")) else style_name

        # --- Connexion Postgres et insertion ---
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()

        # créer table layer_styles si nécessaire (ne modifie pas si déjà existante)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS layer_styles (
                id serial primary key,
                f_table_catalog text,
                f_table_schema text,
                f_table_name text,
                f_geometry_column text,
                stylename text,
                styleqml text,
                stylesld text,
                useasdefault boolean,
                description text,
                owner text,
                ui text,
                update_time timestamp DEFAULT now(),
                type text
            );
        """)

        # vérifier colonnes existantes
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = 'layer_styles'
        """)
        existing_cols = {r[0] for r in cur.fetchall()}

        # purge du style existant (même schema/table/stylename)
        if {"f_table_schema", "f_table_name", "stylename"} <= existing_cols:
            cur.execute("""
                DELETE FROM layer_styles
                WHERE f_table_schema = %s AND f_table_name = %s AND stylename = %s
            """, (tbl_schema, tbl_name, style_name_eff))

        # préparer la ligne à insérer (seulement colonnes existantes)
        row = {
            "f_table_catalog": dbname,
            "f_table_schema": tbl_schema,
            "f_table_name":   tbl_name,
            "f_geometry_column": geom_col,
            "stylename":      style_name_eff,
            "styleqml":       qml_str,
            "stylesld":       "",
            "useasdefault":   True,
            "description":    "Style par défaut enregistré via plugin FuzzyAttributes",
            "owner":          user or "",
            "ui":             "",
            "type":           geom_type_txt,
        }

        cols = [c for c in row.keys() if c in existing_cols]
        vals = [row[c] for c in cols]

        placeholders = ", ".join(["%s"] * len(cols))
        col_list = ", ".join(cols)
        sql = f"INSERT INTO layer_styles ({col_list}) VALUES ({placeholders})"
        cur.execute(sql, vals)

        conn.commit()
        cur.close()
        conn.close()

        QgsMessageLog.logMessage(f"Style par défaut enregistré pour {tbl_schema}.{tbl_name} (type={geom_type_txt})", "FuzzyAggregate", Qgis.Info)
        return True

    except Exception as e:
        QgsMessageLog.logMessage(f"Erreur lors de la sauvegarde du style PostGIS : {e}", "FuzzyAggregate", Qgis.Warning)
        return False

