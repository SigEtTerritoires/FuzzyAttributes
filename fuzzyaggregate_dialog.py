from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from qgis.core import QgsProject,QgsVectorLayer, QgsProcessingFeedback,   QgsProcessingFeatureSourceDefinition
from PyQt5.QtWidgets import QMessageBox
from qgis.core import QgsField,QgsFields,QgsWkbTypes,QgsFeature,edit
from PyQt5.QtCore import QVariant
import os
import processing
from qgis.core import QgsProcessingOutputLayerDefinition
import sys
from qgis.core import QgsMessageLog,QgsProcessing
from qgis.core import Qgis
from qgis.PyQt.QtCore import QFileInfo
from qgis.core import QgsVectorFileWriter
import math
from datetime import datetime
from qgis.PyQt.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem
import getpass
from qgis.PyQt.QtCore import QTranslator, QCoreApplication, QLocale 
from qgis.PyQt.QtCore import NULL
from PyQt5 import QtWidgets
from qgis.core import (
    QgsVectorLayer,
    QgsField,
    QgsSymbol,
    QgsRendererRange,
    QgsGraduatedSymbolRenderer,
    QgsProject
)

from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QMessageBox

# Si tu veux rafraîchir via l’interface QGIS :
from qgis.utils import iface

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
                self.tr("Aucune couche GeoPackage"),
                self.tr("Aucune couche vectorielle provenant d’un fichier .gpkg n’est chargée dans le projet.\n"
                "Veuillez en ajouter une pour utiliser ce plugin.")
            )
        
        # Initialiser self.current_layer avec la première couche sélectionnée
        if layer_names:
            self.current_layer = self.layer_map.get(layer_names[0])
    def vector_layer_names(self):
        layers = QgsProject.instance().mapLayers().values()
        gpkg_layers = []
        for layer in layers:
            if not isinstance(layer, QgsVectorLayer):
                continue
            source = layer.source().split('|')[0]  # enlever la partie "|layername=..."
            if source.lower().endswith('.gpkg'):
                gpkg_layers.append(layer.name())
        return gpkg_layers

    def populate_layer_combos(self):
        self.layerCombo1.clear()
        self.layerCombo2.clear()

        for layer in QgsProject.instance().mapLayers().values():
            if layer.type() == layer.VectorLayer and layer.dataProvider().name() == 'ogr':
                source = layer.source().lower()
                if source.endswith('.gpkg') or '.gpkg|' in source:
                    name = layer.name()
                    self.layerCombo1.addItem(name, layer)  # associe la couche à l’entrée
                    self.layerCombo2.addItem(name, layer)

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


    def run_processing_to_gpkg(self,alg, params, gpkg_path, layer_name, overwrite=False, log_tag="MonPlugin"):
        try:
            if not gpkg_path.lower().endswith(".gpkg"):
                raise ValueError(self.tr("Le chemin GPKG doit se terminer par .gpkg"))

            
            # Forcer sortie temporaire
            params["OUTPUT"] = "TEMPORARY_OUTPUT"
            result = processing.run(alg, params)
            
            # Récupération de la couche de sortie selon le type de retour
            if isinstance(result, dict):
                output_layer = result.get("OUTPUT")
                if output_layer is None:
                    raise Exception("La clé 'OUTPUT' est absente du résultat")
            elif isinstance(result, QgsVectorLayer):
                output_layer = result
            else:
                raise Exception(self.tr("Le résultat du traitement est inattendu"))

            if not isinstance(output_layer, QgsVectorLayer):
                raise Exception(self.tr("La sortie n'est pas une couche vectorielle valide"))
            
            # Nettoyer le champ fid avant d'écrire dans le GPKG
            cleaned_layer = self.reset_fid_field(output_layer, log_tag=log_tag)
            
            # Options d'écriture
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
                gpkg_path,
                QgsProject.instance().transformContext(),
                options
            )[0]
            
            if error != QgsVectorFileWriter.NoError:
                raise Exception(f"Erreur d'écriture dans le GeoPackage : code {error}")

            QgsMessageLog.logMessage(f"✅ Résultat sauvegardé dans {gpkg_path} (couche : {layer_name})", level=Qgis.Success, tag=log_tag)

            return cleaned_layer

        except Exception as e:
            QgsMessageLog.logMessage(f"❌ Erreur : {str(e)}", level=Qgis.Critical, tag=log_tag)
            raise







    def run_aggregation(self):
        function_code = getattr(self, 'aggregation_function_code', None)
        
        if not function_code:
            QMessageBox.warning(self, "Aucune fonction sélectionnée",
                                "Veuillez d'abord sélectionner une fonction d'agrégation floue.")
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
            from qgis.PyQt.QtWidgets import QMessageBox
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
        output_name = self.outputLayerName.text().strip()+ "_agg"
        agg_field_name = output_name  # Nom du champ d'agrégation

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
            algo = 'native:intersection' if operation == 'intersection' else 'native:union'

            # Exemple : récupérer le chemin du GPKG depuis layer1
            gpkg_path = layer1.source().split('|')[0]  # on enlève le suffixe éventuel "|layername=..."
            
            # Nom de la couche résultante donné par l’utilisateur (champ texte)
            layer_name = self.outputLayerName.text().strip()

            # Construction du chemin de sortie dans le GPKG
            
            
            result = self.run_processing_to_gpkg(
                alg=algo,
                params={
                    "INPUT": layer1,
                    "OVERLAY": layer2
                },
                gpkg_path=f"{gpkg_path}",
                layer_name=self.outputLayerName.text().strip()+"_agg",
                overwrite=True
            )


            # Récupération de la couche de sortie selon le type de retour
            if isinstance(result, dict):
                output_layer = result.get("OUTPUT")
                if output_layer is None:
                    raise Exception("La clé 'OUTPUT' est absente du résultat")
            elif isinstance(result, QgsVectorLayer):
                output_layer = result
            else:
                raise Exception(self.tr("Le résultat du traitement est inattendu"))

            if not isinstance(output_layer, QgsVectorLayer):
                raise Exception(self.tr("La sortie n'est pas une couche vectorielle valide"))

            # Construction du chemin de la couche dans le GPKG
            gpkg_layer_path = f"{gpkg_path}|layername={(self.outputLayerName.text().strip() + '_agg')}"


            # Création explicite de la couche depuis le GPKG
            real_layer = QgsVectorLayer(gpkg_layer_path, self.outputLayerName.text().strip()+"_agg", "ogr")

            if not real_layer.isValid():
                raise Exception("Échec du chargement de la couche depuis le GeoPackage")


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

            # Définir les classes (valeur min, valeur max, couleur, étiquette)
            classes = [
                (0.0, 0.125, "#ff0000", self.tr("0 – 0.125 (mauvais)")),          # rouge
                (0.125, 0.375, "#ff7f00", self.tr("0.125 – 0.375 (médiocre)")),   # orange
                (0.375, 0.625, "#ffff00", self.tr("0.375 – 0.625 (moyen)")),    # jaune
                (0.625, 0.875, "#7fff00", self.tr("0.625 – 0.875 (bon)")), # vert clair
                (0.875, 1.0, "#006400", self.tr("0.875 – 1.0 (très bon)"))    # vert foncé
            ]

            ranges = []
            for min_val, max_val, color, label in classes:
                symbol = QgsSymbol.defaultSymbol(real_layer.geometryType())
                symbol.setColor(QColor(color))
                rng = QgsRendererRange(min_val, max_val, symbol, label)
                ranges.append(rng)

            # Créer un renderer gradué basé sur les plages définies
            renderer = QgsGraduatedSymbolRenderer(agg_field_name, ranges)

            # Inutile d’appeler setMode() → les ranges sont déjà explicites
            real_layer.setRenderer(renderer)
            real_layer.triggerRepaint()

            # Ajouter la couche au projet
            QgsProject.instance().addMapLayer(real_layer)

        
            # Message de succès
            QMessageBox.information(self, self.tr("Succès"), f"Couche '{output_name}' créée avec succès.")

            self.ensure_metadata_table_exists(gpkg_path)

            source1 = f"{self.layerCombo1.currentText()}/{self.fieldCombo1.currentText()}"
            source2 = f"{self.layerCombo2.currentText()}/{self.fieldCombo2.currentText()}"
            self.append_metadata(
                gpkg_path=gpkg_path,
                field_name=agg_field_name,
                fuzzy_type=function_id,
                params=fuzzy_params,  # par ex., tu peux adapter
                source1=source1,
                source2=source2
            )

        except Exception as e:
            return
            
    def ensure_metadata_table_exists(self, gpkg_path):
            # Vérifie si la couche 'metafuzzy' existe déjà
            uri = f"{gpkg_path}|layername=metafuzzy"
            existing_layer = QgsVectorLayer(uri, "metafuzzy", "ogr")

            if existing_layer.isValid():
                return True  # La table existe déjà

            # Crée un layer mémoire sans géométrie
            fields = QgsFields()
            fields.append(QgsField("field", QVariant.String))
            fields.append(QgsField("function", QVariant.String))
            fields.append(QgsField("params", QVariant.String))
            fields.append(QgsField("source1", QVariant.String))
            fields.append(QgsField("source2", QVariant.String))
            fields.append(QgsField("date", QVariant.String))
            fields.append(QgsField("user", QVariant.String))

            mem_layer = QgsVectorLayer("None", "metafuzzy", "memory")
            mem_layer.dataProvider().addAttributes(fields)
            mem_layer.updateFields()

            # Enregistre dans le GeoPackage
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.driverName = "GPKG"
            options.layerName = "metafuzzy"
            options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
            options.EditionCapabilities = QgsVectorFileWriter.CanAddNewLayer

            err, _ = QgsVectorFileWriter.writeAsVectorFormatV2(
                layer=mem_layer,
                fileName=gpkg_path,
                transformContext=QgsProject.instance().transformContext(),
                options=options
            )

            return err == QgsVectorFileWriter.NoError
    def append_metadata(self, gpkg_path, field_name, fuzzy_type, params, source1, source2):
        uri = f"{gpkg_path}|layername=metafuzzy"
        layer = QgsVectorLayer(uri, "metafuzzy", "ogr")
        if not layer.isValid():
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("La table metafuzzy n’a pas pu être chargée."))
            return
        # Détermine le type d'opération selon les boutons cochés
        if self.radioIntersection.isChecked():
            operation_type = "inter"
        elif self.radioUnion.isChecked():
            operation_type = "union"
        else:
            operation_type = "none"

        function_value = f"{operation_type}-{fuzzy_type}"
        new_feature = QgsFeature(layer.fields())
        new_feature.setAttribute("field", field_name)
        new_feature.setAttribute("function", function_value)
        new_feature.setAttribute("params", str(params))
        new_feature.setAttribute("source1", source1)
        new_feature.setAttribute("source2", source2)
        new_feature.setAttribute("date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        new_feature.setAttribute("user", getpass.getuser())

        with edit(layer):
            layer.addFeature(new_feature)

    
    def get_layer_path(self, layer):
        """Retourne le chemin du fichier GPKG associé à une couche"""
        source = layer.source()
        if "|layername=" in source:
            return source.split("|layername=")[0]
        else:
            return source

    
    def show_metadata_table(self):
        layer_name = self.layerComboBox.currentText()
        layer = self.layer_map.get(layer_name)
        if not layer:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Aucune couche sélectionnée."))
            return

        gpkg_path = self.get_layer_path(self.current_layer)

        uri = f"{gpkg_path}|layername=metafuzzy"
        metafuzzy_layer = QgsVectorLayer(uri, "metafuzzy", "ogr")

        if not metafuzzy_layer.isValid():
            QMessageBox.information(self, self.tr("Info"),self.tr( "Aucune table 'metafuzzy' trouvée dans le GeoPackage."))
            return

        # Crée une boîte de dialogue pour afficher les données
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
                val = str(feat[field.name()])
                table.setItem(row_idx, col_idx, QTableWidgetItem(val))

        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.resize(600, 300)
        dialog.exec_()
    def show_metadata_table(self):
        layer_name = self.layerCombo1.currentText()
        layer = self.layer_map.get(layer_name)
        if not layer:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Aucune couche sélectionnée."))
            return

        gpkg_path = self.get_layer_path(self.current_layer)

        uri = f"{gpkg_path}|layername=metafuzzy"
        metafuzzy_layer = QgsVectorLayer(uri, "metafuzzy", "ogr")

        if not metafuzzy_layer.isValid():
            QMessageBox.information(self, self.tr("Info"), self.tr("Aucune table 'metafuzzy' trouvée dans le GeoPackage."))
            return

        # Crée une boîte de dialogue pour afficher les données
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
                val = str(feat[field.name()])
                table.setItem(row_idx, col_idx, QTableWidgetItem(val))

        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.resize(600, 300)
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
