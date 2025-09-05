
from qgis.core import (
    Qgis,QgsProject, QgsVectorLayer, QgsField, edit, QgsFeature,
    QgsFields, QgsWkbTypes, QgsCoordinateReferenceSystem,
    QgsVectorFileWriter, QgsApplication
)

from qgis.PyQt.QtCore import QTranslator, QCoreApplication, QLocale
from PyQt5.QtWidgets import QDialog, QMessageBox, QToolTip
from qgis.PyQt.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QAction, QDialog
from PyQt5.QtGui import QIcon
from .fuzzyattributes_dialog import FuzzyAttributesDialog
from .fuzzyaggregate_dialog import FuzzyAggregateDialog
import os
from qgis.PyQt.QtCore import QTranslator, QCoreApplication, QLocale 

_translator = None
def load_translator():
    global _translator
    locale = QLocale(QgsApplication.instance().locale().name()[0:2])
    path = os.path.join(os.path.dirname(__file__), f"FuzzyAttributes_{locale}.qm")
    if os.path.exists(path):
        _translator = QTranslator()
        if _translator.load(path):
            QCoreApplication.installTranslator(_translator)
def is_aggregation_code_consistent(code):
    """
    Vérifie si une combinaison est logiquement cohérente :
    - On compare (A=1, B=0) et (A=0, B=1)
    - Si A meilleur que B donne un moins bon score que B meilleur que A → incohérence
    """
    
    if len(code) != 4:
        return True  # Pas de vérification si ce n’est pas un code asymétrique

    try:
        a1b0 = int(code[0])
        a0b1 = int(code[3])
        return a1b0 <= a0b1
    except ValueError:
        return True  # Ne pas bloquer pour code malformé
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

    return fuzzy_func
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

    return fuzzy_func

class FuzzyAttributes:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        
        # Récupérer la locale du système ou de QGIS
        #self.locale = QLocale.system().name()[0:2]  # ex 'fr'
        # ou mieux encore, récupérer la locale de QGIS : iface.locale() ou QgsApplication.locale()
        self.locale = QgsApplication.locale()[:2]  # récupère les 2 premiers caractères, ex: "fr"
        # Charger le fichier de traduction .qm correspondant
        locale_path = os.path.join(self.plugin_dir, 'i18n', f'FuzzyAttributes_{self.locale}.qm')
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)
    
            
        self.action = None
        self.fuzzy_attributes_dialog = None
        self.fuzzy_aggregate_dialog = None
    @staticmethod
    def tr(message):
        return QCoreApplication.translate("FuzzyAttributes", message)

    def initGui(self):
        icon = QIcon(os.path.join(self.plugin_dir, "icon.png"))

        # Nom du menu principal
        menu_name = self.tr("Fuzzy Plugin")

        # Action principale : FuzzyAttributes
        self.main_action = QAction(icon, "FuzzyAttributes", self.iface.mainWindow())
        self.main_action.triggered.connect(self.run)
        self.iface.addPluginToMenu(menu_name, self.main_action)

        # Action : Agrégation floue
        self.aggregate_action = QAction(icon, self.tr("Agrégation floue"), self.iface.mainWindow())
        self.aggregate_action.triggered.connect(self.run_fuzzy_aggregate)
        self.iface.addPluginToMenu(menu_name, self.aggregate_action)

        # ➕ Nouvelle action : Fuzzy Text
        self.text_action = QAction(icon, self.tr("Texte → Flou"), self.iface.mainWindow())
        self.text_action.triggered.connect(self.run_fuzzy_text)
        self.iface.addPluginToMenu(menu_name, self.text_action)



        

    def unload(self):
        menu_name = self.tr("Fuzzy Plugin")
        
        if hasattr(self, 'main_action'):
            self.iface.removePluginMenu(menu_name, self.main_action)

        if hasattr(self, 'aggregate_action'):
            self.iface.removePluginMenu(menu_name, self.aggregate_action)

        if hasattr(self, 'text_action'):   # ➕ suppression de l'action Texte→Flou
            self.iface.removePluginMenu(menu_name, self.text_action)


    def run(self):
        if self.fuzzy_attributes_dialog is None:
            self.fuzzy_attributes_dialog = FuzzyAttributesDialog()
            self.fuzzy_attributes_dialog.finished.connect(self.clear_fuzzy_attributes_dialog)

        self.fuzzy_attributes_dialog.show()
        self.fuzzy_attributes_dialog.raise_()
        self.fuzzy_attributes_dialog.activateWindow()

    def run_fuzzy_aggregate(self):
        if self.fuzzy_aggregate_dialog is None:
            self.fuzzy_aggregate_dialog = FuzzyAggregateDialog()
            self.fuzzy_aggregate_dialog.finished.connect(self.clear_fuzzy_aggregate_dialog)

        self.fuzzy_aggregate_dialog.show()
        self.fuzzy_aggregate_dialog.raise_()
        self.fuzzy_aggregate_dialog.activateWindow()

    def clear_fuzzy_attributes_dialog(self):
        self.fuzzy_attributes_dialog = None
    def clear_fuzzy_aggregate_dialog(self):
        self.fuzzy_aggregate_dialog = None
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
    def run_fuzzy_text(self):
        from .fuzzytext_dialog import FuzzyTextDialog
        layer = self.iface.activeLayer()
        if not layer:
            self.iface.messageBar().pushMessage("Erreur", "Aucune couche active sélectionnée", level=3)
            return

        dlg = FuzzyTextDialog(self.iface, layer)
        dlg.exec_()

