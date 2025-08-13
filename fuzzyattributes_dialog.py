from qgis.core import (
    Qgis,QgsProject, QgsVectorLayer, QgsField, edit, QgsFeature,
    QgsFields, QgsWkbTypes, QgsCoordinateReferenceSystem,
    QgsVectorFileWriter, QgsApplication
)

from qgis.PyQt.QtCore import QTranslator, QCoreApplication, QLocale
from PyQt5.QtWidgets import QDialog, QMessageBox, QToolTip
from qgis.PyQt.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QVariant
from .fuzzyattributes_dialog_base import Ui_FuzzyAttributesDialog
import math
import os
from datetime import datetime
import getpass
from qgis.PyQt.QtGui import QPixmap




_translator = None

def load_translator():
    global _translator
    locale = QLocale(QgsApplication.instance().locale().name()[0:2])
    path = os.path.join(os.path.dirname(__file__), f"FuzzyAttributes_{locale}.qm")
    if os.path.exists(path):
        _translator = QTranslator()
        if _translator.load(path):
            QCoreApplication.installTranslator(_translator)

class FuzzyAttributesDialog(QDialog, Ui_FuzzyAttributesDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_translator()  # 🔹 AJOUT ICI
        self.setupUi(self)
        
        # Connecter les boutons
        self.buttonBox.accepted.connect(self.apply_fuzzy_transformation)
        self.buttonBox.rejected.connect(self.reject)
        self.helpButton.clicked.connect(self.show_help)
        self.btnShowStats.clicked.connect(self.show_field_statistics)

        # Remplir la comboBox des couches vectorielles
        # Remplir la comboBox des couches vectorielles GeoPackage uniquement
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
        self.layerComboBox.addItems(layer_names)
        # Initialiser self.current_layer avec la première couche sélectionnée
        if layer_names:
            self.current_layer = self.layer_map.get(layer_names[0])
        # Infobulle explicative
        self.layerComboBox.setToolTip(self.tr("Seules les couches provenant de fichiers GeoPackage (.gpkg) sont affichées."))
        self.btnShowMetadata.clicked.connect(self.show_metadata_table)
        self.layerComboBox.currentIndexChanged.connect(self.on_layer_changed)
        self.layerComboBox.currentTextChanged.connect(self.update_current_layer)


        # Types flous disponibles avec codes internes
        self.fuzzy_types = [
            ("linear_inc", self.tr("linéaire croissante")),
            ("linear_dec", self.tr("linéaire décroissante")),
            ("triangular", self.tr("triangulaire")),
            ("trapezoidal", self.tr("trapézoïdale")),
            ("sigmoid_inc", self.tr("sigmoïde croissante (S)")),
            ("sigmoid_dec", self.tr("sigmoïde décroissante (Z)")),
            ("gaussian", self.tr("gaussienne"))
        ]

        # Ajout à la combo : texte affiché + code interne en data
        for code, label in self.fuzzy_types:
            self.fuzzyTypeComboBox.addItem(label, code)
         

        self.fuzzyTypeComboBox.currentTextChanged.connect(self.updateFunctionPreview)
        # Appel initial
        self.updateFunctionPreview(self.fuzzyTypeComboBox.currentText())

        # Connexions
        self.layerComboBox.currentIndexChanged.connect(self.update_fields)
        self.fuzzyTypeComboBox.currentIndexChanged.connect(self.update_example_parameters)

        self.update_fields()
        self.update_example_parameters()  # Affiche exemple au démarrage

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


    def selected_layer(self):
        name = self.layerComboBox.currentText()
        for layer in QgsProject.instance().mapLayers().values():
            if layer.name() == name:
                return layer
        return None

    def update_fields(self):
        self.fieldComboBox.clear()
        layer = self.selected_layer()
        if not layer:
            return
        numeric_fields = [f.name() for f in layer.fields() if f.type() in (
            QVariant.Int, QVariant.Double, QVariant.LongLong,
            QVariant.UInt, QVariant.ULongLong)]
        self.fieldComboBox.addItems(numeric_fields)

    def update_example_parameters(self):
        type_text = self.fuzzyTypeComboBox.currentText()
        examples = {
            self.tr("linéaire croissante"): "Ex : 10, 50",
            self.tr("linéaire décroissante"): "Ex : 10, 50",
            self.tr("triangulaire"): "Ex : 10, 30, 50",
            self.tr("trapézoïdale"): "Ex : 10, 20, 40, 50",
            self.tr("sigmoïde croissante (S)"): "Ex : 0.2, 30",
            self.tr("sigmoïde décroissante (Z)"): "Ex : 0.2, 30",
            self.tr("gaussienne"): "Ex : 30, 10"
        }
        self.paramExampleLabel.setText(examples.get(type_text, ""))
    def update_current_layer(self, layer_name):
        if hasattr(self, 'layer_map'):
            self.current_layer = self.layer_map.get(layer_name)
        else:
            self.current_layer = None

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

    def append_metadata(self, gpkg_path, field_name, fuzzy_type, params):
        uri = f"{gpkg_path}|layername=metafuzzy"
        layer = QgsVectorLayer(uri, "metafuzzy", "ogr")
        if not layer.isValid():
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("La table metafuzzy n’a pas pu être chargée."))
            return
        
        
      

        new_feature = QgsFeature(layer.fields())
        new_feature.setAttribute("field", field_name)
        new_feature.setAttribute("function", fuzzy_type)
        new_feature.setAttribute("params", ", ".join(map(str, params)))
        new_source = f"{self.layerComboBox.currentText()}/{self.fieldComboBox.currentText()} "
        new_feature.setAttribute("source1", new_source)
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
    def on_layer_changed(self):
        layer_name = self.layerComboBox.currentText()
        layers = QgsProject.instance().mapLayers().values()
        for layer in layers:
            if layer.name() == layer_name:
                self.current_layer = layer
                break
    def open_aggregation_function_dialog(self):
        dlg = AggregationFunctionDialog()
        if dlg.exec_():
            result_code = dlg.get_selected_values()
            self.functionCodeLabel.setText(result_code)  # à adapter selon votre interface
    
    def apply_fuzzy_transformation(self):
        config = self.get_parameters()
        if not config:
            return

        layer = config['layer']
        source_path = layer.source().split('|')[0]
        if not source_path.lower().endswith('.gpkg'):
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Les métadonnées ne peuvent être stockées que dans un fichier .gpkg."))
            return

        if not self.ensure_metadata_table_exists(source_path):
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Impossible de créer la table metafuzzy dans le GeoPackage."))
            return

        field_name = config['field_name']
        fuzzy_type = config['fuzzy_type']
        params = config['params']

        new_field_name = f"{field_name}_fuzzy"
        if not layer.dataProvider().addAttributes([QgsField(new_field_name, QVariant.Double)]):
            QMessageBox.warning(self, self.tr("Erreur"),self.tr( "Impossible d'ajouter le champ."))
            return

        layer.updateFields()
        fuzzy_index = layer.fields().indexFromName(new_field_name)
        field_index = layer.fields().indexFromName(field_name)
        if fuzzy_index == -1 or field_index == -1:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Problème avec les champs."))
            return

        with edit(layer):
            for f in layer.getFeatures():
                x = f[field_index]
                if x is None:
                    f[fuzzy_index] = None
                    continue

                try:
                    if fuzzy_type == "linéaire croissante":
                        a, b = params
                        val = (x - a) / (b - a)
                    elif fuzzy_type == "linéaire décroissante":
                        a, b = params
                        val = (b - x) / (b - a)
                    elif fuzzy_type == "triangulaire":
                        a, b, c = params
                        if x <= a or x >= c:
                            val = 0
                        elif a < x < b:
                            val = (x - a) / (b - a)
                        elif b <= x < c:
                            val = (c - x) / (c - b)
                    elif fuzzy_type == "trapézoïdale":
                        a, b, c, d = params
                        if x <= a or x >= d:
                            val = 0
                        elif a < x < b:
                            val = (x - a) / (b - a)
                        elif b <= x <= c:
                            val = 1
                        elif c < x < d:
                            val = (d - x) / (d - c)
                    elif fuzzy_type == "sigmoïde croissante (S)":
                        a, b = params
                        val = 1 / (1 + math.exp(-a * (x - b)))
                    elif fuzzy_type == "sigmoïde décroissante (Z)":
                        a, b = params
                        val = 1 - (1 / (1 + math.exp(-a * (x - b))))
                    elif fuzzy_type == "gaussienne":
                        c, sigma = params
                        val = math.exp(-((x - c) ** 2) / (2 * sigma ** 2))
                    else:
                        val = None

                    f[fuzzy_index] = max(0, min(1, val)) if val is not None else None
                    layer.updateFeature(f)

                except Exception as e:
                    f[fuzzy_index] = None
        self.append_metadata(source_path, field_name, fuzzy_type, params)

        QMessageBox.information(self, self.tr("Succès"), self.tr("Transformation floue ajoutée dans '{}'").format(new_field_name))
    def show_field_statistics(self):
        layer_name = self.layerComboBox.currentText()
        field_name = self.fieldComboBox.currentText()
    
        # Récupère la couche depuis le nom
        layer = None
        for lyr in QgsProject.instance().mapLayers().values():
            if lyr.name() == layer_name:
                layer = lyr
                break

        if not layer:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Impossible de trouver la couche '{}'").format(layer_name))
            return

        if not field_name:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Aucun champ sélectionné."))
            return

        idx = layer.fields().indexFromName(field_name)
        if idx == -1:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Le champ est introuvable."))
            return

        # Récupère les valeurs numériques valides
        values = []
        for feat in layer.getFeatures():
            val = feat[field_name]
            if isinstance(val, (int, float)):
                values.append(val)

        if not values:
            QMessageBox.information(self, self.tr("Aucune donnée"), self.tr("Aucune valeur numérique disponible pour ce champ."))
            return

        # Calcule les stats
        from statistics import mean, median
        min_val = min(values)
        max_val = max(values)
        mean_val = mean(values)
        median_val = median(values)

        msg = self.tr(
            "Statistiques pour le champ '{field_name}' :\n\n"
            "Nombre de valeurs : {count}\n"
            "Min : {min_val}\n"
            "Max : {max_val}\n"
            "Moyenne : {mean_val:.2f}\n"
            "Médiane : {median_val:.2f}"
        ).format(
            field_name=field_name,
            count=len(values),
            min_val=min_val,
            max_val=max_val,
            mean_val=mean_val,
            median_val=median_val
        )

        QMessageBox.information(self, self.tr("Statistiques du champ"), msg)
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


