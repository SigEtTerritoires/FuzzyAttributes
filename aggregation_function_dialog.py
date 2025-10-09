from qgis.PyQt.QtWidgets import QDialog
from .aggregation_function_dialog_ui import Ui_AggregationFunctionDialog
from qgis.PyQt.QtCore import QTranslator, QCoreApplication, QLocale 
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import Qt
import os
from qgis.core import QgsApplication

_translator = None
def load_translator():
    global _translator
    locale = QLocale(QgsApplication.instance().locale().name()[0:2])
    path = os.path.join(os.path.dirname(__file__), f"FuzzyAttributes_{locale}.qm")
    if os.path.exists(path):
        _translator = QTranslator()
        if _translator.load(path):
            QCoreApplication.installTranslator(_translator)
class AggregationFunctionDialog(QDialog, Ui_AggregationFunctionDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.checkSymmetry.stateChanged.connect(self.toggle_symmetry_section)
        self.toggle_symmetry_section(self.checkSymmetry.checkState())

 
    def toggle_symmetry_section(self, state):
        visible = state == Qt.CheckState.Checked  # Qt.CheckState.Checked = 2
        self.group4.setVisible(visible)
        self.line.setVisible(visible)
        self.label_symmetry_test.setVisible(visible)

    def get_selected_values(self):
        """
        Retourne un code à 4 chiffres représentant les valeurs sélectionnées.
        - Si le groupe 4 est masqué, le dernier chiffre = premier (symétrie).
        - Si un groupe visible n’a pas de case cochée, affiche un message et retourne None.
        """
        result = ""

        # Vérification des groupes 1 à 3
        for group in [1, 2, 3]:
            selected = False
            for i in range(1, 6):
                radio = getattr(self, f"radio{group}_{i}")
                if radio.isChecked():
                    result += str(i - 1)
                    selected = True
                    break
            if not selected:
                QMessageBox.warning(self, "Erreur", f"Aucune option sélectionnée pour le Critère {group}.")
                return None

        # Groupe 4 (selon visibilité)
        if self.group4.isVisible():
            selected = False
            for i in range(1, 6):
                radio = getattr(self, f"radio4_{i}")
                if radio.isChecked():
                    result += str(i - 1)
                    selected = True
                    break
            if not selected:
                QMessageBox.warning(self, "Erreur", "Aucune option sélectionnée pour le Critère 4.")
                return None
        else:
            result += result[0]  # symétrie : copie du premier

        return result

    def set_selected_values(self, code):
        """
        Initialise les radio buttons selon un code à 4 chiffres (chaîne).
        Ex : "1234" -> coche radio1_2, radio2_3, radio3_4, radio4_5
        """
        if len(code) != 4 or not code.isdigit():
            return  # Code invalide, on ignore

        for group in [1, 2, 3, 4]:
            val = int(code[group - 1])  # Ex : pour "1234", val = 1, 2, 3, 4
            radio = getattr(self, f"radio{group}_{val + 1}", None)
            if radio:
                radio.setChecked(True)

    def set_criteria_labels(self, nom_couche_1, nom_couche_2):
        self.group1.setTitle(
            self.tr("Critère 1 : si le critère '{0}' est Très mauvais et le critère '{1}' est Très bon, le résultat doit être :").format(nom_couche_1, nom_couche_2)
        )
        self.group2.setTitle(
            self.tr("Critère 2 : si le critère '{0}' est Moyen et le critère '{1}' est Moyen, le résultat doit être :").format(nom_couche_1, nom_couche_2)
        )
        self.group3.setTitle(
            self.tr("Critère 3 : si le critère '{0}' est Moyen et le critère '{1}' est Très bon, le résultat doit être :").format(nom_couche_1, nom_couche_2)
        )
        self.group4.setTitle(
            self.tr("Critère 4 : si le critère '{0}' est Très bon et le critère '{1}' est Très mauvais, le résultat doit être :").format(nom_couche_1, nom_couche_2)
        )
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



