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
import re
from qgis.PyQt.QtGui import QPixmap
from qgis.core import QgsDataSourceUri
from qgis.core import QgsMessageLog, Qgis
from qgis.PyQt.QtCore import QDateTime
from qgis.core import QgsVectorLayer, QgsFeature, QgsDataSourceUri



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


        self.populate_layer_combo()


        # Infobulle explicative
        self.layerComboBox.setToolTip(
            self.tr("Les couches provenant de fichiers GeoPackage (.gpkg) ou de bases PostGIS sont affichées.")
        )

        self.btnShowMetadata.clicked.connect(self.show_metadata_table)
        self.layerComboBox.currentIndexChanged.connect(self.on_layer_changed)
        self.layerComboBox.currentTextChanged.connect(self.update_current_layer)

        # 🔹 Ajout pour mettre à jour la liste des champs quand on change de couche
        self.layerComboBox.currentIndexChanged.connect(self.update_fields)


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
    def showEvent(self, event):
        super().showEvent(event)
        self.populate_layer_combo()
        self.update_fields()

    def vector_layer_names(self):
        """
        Retourne un dict {nom_affiché: QgsVectorLayer}
        pour les couches GeoPackage et PostGIS.
        """
        layer_map = {}

        for layer in QgsProject.instance().mapLayers().values():
            if layer.type() != layer.VectorLayer:
                continue

            provider = layer.dataProvider().name()
            source = layer.source().lower()

            # Cas GeoPackage
            if provider == 'ogr' and (source.endswith('.gpkg') or '.gpkg|' in source):
                layer_map[layer.name()] = layer

            # Cas PostGIS
            elif provider == 'postgres':
                layer_map[layer.name()] = layer

        return layer_map


    def populate_layer_combo(self):
        """Remplit la comboBox avec les couches GeoPackage et PostGIS"""
        self.layerComboBox.clear()
        

        layer_names = []
        self.layer_map = {}

        for layer in QgsProject.instance().mapLayers().values():
            if layer.type() == layer.VectorLayer:
                provider = layer.dataProvider().name()

                # Cas GeoPackage
                if provider == "ogr" and (layer.source().lower().endswith(".gpkg") or ".gpkg|" in layer.source().lower()):
                    display_name = f"[GPKG] {layer.name()}"
                    self.layer_map[display_name] = layer
                    layer_names.append(display_name)

                # Cas PostGIS
                elif provider == "postgres":
                    uri = layer.dataProvider().uri()
                    schema = uri.schema()  # retourne None si pas de schema
                    table = layer.name()   # nom complet de la table

                    display_name = f"[PG] {schema}.{table}" if schema else f"[PG] {table}"

                    self.layer_map[display_name] = layer
                    layer_names.append(display_name)


        if not layer_names:
            QMessageBox.information(
                self,
                self.tr("Aucune couche trouvée"),
                self.tr("Aucune couche GeoPackage (.gpkg) ou PostGIS n’est chargée dans le projet.\n"
                        "Veuillez en ajouter une pour utiliser ce plugin.")
            )

        self.layerComboBox.addItems(layer_names)

        # Initialiser self.current_layer avec la première couche sélectionnée
        if layer_names:
            self.current_layer = self.layer_map.get(layer_names[0])

        # Infobulle explicative
        self.layerComboBox.setToolTip(
            self.tr("Les couches provenant de fichiers GeoPackage (.gpkg) ou de bases PostGIS sont affichées (avec schéma pour PostGIS).")
        )

    def selected_layer(self):
        """Retourne la couche actuellement sélectionnée dans la comboBox"""
        name = self.layerComboBox.currentText()
        return self.layer_map.get(name)

    def update_fields(self):
        """Met à jour la liste des champs numériques de la couche sélectionnée"""
        self.fieldComboBox.clear()
        layer = self.selected_layer()
        if not layer:
            return

        numeric_fields = [
            f.name() for f in layer.fields()
            if f.type() in (
                QVariant.Int,
                QVariant.Double,
                QVariant.LongLong,
                QVariant.UInt,
                QVariant.ULongLong,
            )
        ]
        self.fieldComboBox.addItems(numeric_fields)

        # 🔹 Sélectionner automatiquement le premier champ si disponible
        if numeric_fields:
            self.fieldComboBox.setCurrentIndex(0)

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
    def ensure_metadata_table_exists(self, layer):
        """
        Vérifie (et crée si besoin) la table metafuzzy dans le même GPKG ou schéma PostGIS que la couche donnée.
        Retourne True si la table existe ou a été créée, False sinon.
        """
        try:
            source = layer.source()

            # ---------------------------
            # Cas 1 : GeoPackage
            # ---------------------------
            if source.lower().endswith(".gpkg") or "|layername=" in source:
                gpkg_path = source.split("|")[0]
                uri = f"{gpkg_path}|layername=metafuzzy"
                meta_layer = QgsVectorLayer(uri, "metafuzzy", "ogr")

                if meta_layer.isValid():
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

                # Vérifier si la table existe déjà
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = %s 
                        AND table_name = 'metafuzzy'
                    );
                """, (schema,))
                exists = cur.fetchone()[0]

                if not exists:
                    # Création de la table
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

                    # Accorder tous les droits à l'utilisateur actuel
                    cur.execute(f'GRANT ALL PRIVILEGES ON TABLE {schema}.metafuzzy TO {user};')
                    conn.commit()
                    # ⚡ Important : forcer QGIS à recharger les couches pour qu'il voie la nouvelle table
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
                        "Impossible de charger la table 'metafuzzy' dans QGIS", "FuzzyPlugin", Qgis.Critical
                    )
                    return False

                return True

            else:
                QMessageBox.warning(
                    self, self.tr("Erreur"),
                    self.tr("Format de source non reconnu (ni GPKG ni PostGIS).")
                )
                return False

        except Exception as e:
            QgsMessageLog.logMessage(f"Erreur ensure_metadata_table_exists: {e}", "FuzzyPlugin", Qgis.Critical)
            return False



    def append_metadata(self, gpkg_or_layer, field_name, fuzzy_type, params,
                        source1=None, source2=None, provider="ogr", schema=None):
        # Assure que la table metafuzzy existe
        if not self.ensure_metadata_table_exists(gpkg_or_layer):
            QMessageBox.information(self, self.tr("Info"), self.tr("Impossible de créer ou charger la table 'metafuzzy'."))
            return

        try:
            date_str = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
            user = getpass.getuser()

            # --- Chargement de la table metafuzzy ---
            if provider == "ogr":
                # gpkg_or_layer est un chemin GeoPackage
                gpkg_path = gpkg_or_layer
                uri = f"{gpkg_path}|layername=metafuzzy"
                metafuzzy_layer = QgsVectorLayer(uri, "metafuzzy", "ogr")
                if not metafuzzy_layer.isValid():
                    raise Exception("Table 'metafuzzy' introuvable dans le GeoPackage.")

            elif provider in ["postgres", "postgis"]:
                # gpkg_or_layer est un layer PostGIS
                layer = gpkg_or_layer
                uri = QgsDataSourceUri(layer.source())
                schema = schema or uri.schema() or "public"  # <-- récupère le schéma de la couche
                uri.setDataSource(schema, "metafuzzy", None, "", "")
                metafuzzy_layer = QgsVectorLayer(uri.uri(), "metafuzzy", "postgres")
                if not metafuzzy_layer.isValid():
                    raise Exception(f"Table '{schema}.metafuzzy' introuvable dans PostGIS (URI: {uri.uri()})")

            else:
                raise Exception(f"Provider non supporté : {provider}")

            # --- Création du nouvel enregistrement ---
            f = QgsFeature(metafuzzy_layer.fields())
            f.setAttribute("sourcefield", field_name)
            f.setAttribute("function", fuzzy_type)
            f.setAttribute("params", str(params))
            f.setAttribute("source1", source1 or "")
            f.setAttribute("source2", source2 or "")
            f.setAttribute("datecreated", date_str)
            f.setAttribute("username", user)

            # --- Ajout dépendant du provider ---
            if provider == "ogr":
                metafuzzy_layer.startEditing()
                metafuzzy_layer.addFeature(f)
                metafuzzy_layer.commitChanges()
            else:  # postgres
                metafuzzy_layer.startEditing()
                metafuzzy_layer.addFeature(f)
                if not metafuzzy_layer.commitChanges():
                    raise Exception("Échec commit PostGIS : " + metafuzzy_layer.commitErrors())


        except Exception as e:
            QgsMessageLog.logMessage(f"Erreur append_metadata: {e}", "FuzzyPlugin", Qgis.Critical)
      
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

        # Assure que la table metafuzzy existe
        if not self.ensure_metadata_table_exists(layer):
            QMessageBox.information(self, self.tr("Info"), self.tr("Impossible de créer ou charger la table 'metafuzzy'."))
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
        field_name = config['field_name']
        fuzzy_code = self.fuzzyTypeComboBox.currentData()  # 🔹 Code interne, pas label
        params = config['params']

        # Validation des paramètres
        valid, msg = self.validate_fuzzy_params(fuzzy_code, params)
        if not valid:
            QMessageBox.warning(self, self.tr("Paramètres invalides"), self.tr(msg))
            return

        new_field_name = f"{field_name}_fuzzy"
        provider = layer.dataProvider()
        existing_index = layer.fields().indexFromName(new_field_name)

        # Vérifier si le champ existe déjà
        if existing_index != -1:
            reply = QMessageBox.question(
                self,
                self.tr("Champ existant"),
                self.tr(f"Le champ '{new_field_name}' existe déjà. Voulez-vous le remplacer ?"),
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
            else:
                if not provider.deleteAttributes([existing_index]):
                    QMessageBox.warning(self, self.tr("Erreur"), self.tr("Impossible de supprimer le champ existant."))
                    return
                layer.updateFields()

        # Ajouter le champ
        new_field = QgsField(new_field_name, QVariant.Double)
        if provider.name().lower() in ["postgres", "postgis"]:
            new_field.setTypeName("DOUBLE PRECISION")
        else:
            new_field.setTypeName("REAL")

        if not provider.addAttributes([new_field]):
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Impossible d'ajouter le champ."))
            return
        layer.updateFields()

        fuzzy_index = layer.fields().indexFromName(new_field_name)
        field_index = layer.fields().indexFromName(field_name)
        if fuzzy_index == -1 or field_index == -1:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Problème avec les champs."))
            return

        # Calcul des valeurs floues
        with edit(layer):
            for f in layer.getFeatures():
                x = f[field_index]
                if x is None:
                    f[fuzzy_index] = None
                    continue
                try:
                    if fuzzy_code == "linear_inc":
                        a, b = params
                        val = (x - a) / (b - a)
                    elif fuzzy_code == "linear_dec":
                        a, b = params
                        val = (b - x) / (b - a)
                    elif fuzzy_code == "triangular":
                        a, b, c = params
                        if x <= a or x >= c:
                            val = 0
                        elif a < x < b:
                            val = (x - a) / (b - a)
                        elif b <= x < c:
                            val = (c - x) / (c - b)
                    elif fuzzy_code == "trapezoidal":
                        a, b, c, d = params
                        if x <= a or x >= d:
                            val = 0
                        elif a < x < b:
                            val = (x - a) / (b - a)
                        elif b <= x <= c:
                            val = 1
                        elif c < x < d:
                            val = (d - x) / (d - c)
                    elif fuzzy_code == "sigmoid_inc":
                        a, b = params
                        val = 1 / (1 + math.exp(-a * (x - b)))
                    elif fuzzy_code == "sigmoid_dec":
                        a, b = params
                        val = 1 - (1 / (1 + math.exp(-a * (x - b))))
                    elif fuzzy_code == "gaussian":
                        c, sigma = params
                        val = math.exp(-((x - c) ** 2) / (2 * sigma ** 2))
                    else:
                        val = None

                    f[fuzzy_index] = max(0, min(1, val)) if val is not None else None
                    layer.updateFeature(f)
                except Exception:
                    f[fuzzy_index] = None

         # Ajouter les métadonnées
        if provider.name().lower() in ["postgres", "postgis"]:
            table_name = layer.name()  # nom de la table PostGIS
            self.append_metadata(
                layer,
                field_name,
                fuzzy_code,
                params,
                source1=table_name,
                provider="postgres"
            )
        else:
            gpkg_path = layer.source().split('|')[0]
            table_name = layer.name()  # nom de la couche dans le GeoPackage
            self.append_metadata(
                gpkg_path,
                field_name,
                fuzzy_code,
                params,
                source1=table_name,
                provider="ogr"
            )

        QMessageBox.information(
            self,
            self.tr("Succès"),
            self.tr("Transformation floue ajoutée dans '{}'").format(new_field_name)
        )

    def show_field_statistics(self):
        layer_name = self.layerComboBox.currentText()
        field_name = self.fieldComboBox.currentText()

        # Récupère la couche depuis le dictionnaire self.layer_map
        layer = self.layer_map.get(layer_name)

        if not layer:
            QMessageBox.warning(
                self, 
                self.tr("Erreur"), 
                self.tr("Impossible de trouver la couche '{}'").format(layer_name)
            )
            return

        if not field_name:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Aucun champ sélectionné."))
            return

        idx = layer.fields().indexFromName(field_name)
        if idx == -1:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Le champ est introuvable."))
            return

        # Récupère les valeurs numériques valides
        values = [
            feat[field_name] 
            for feat in layer.getFeatures() 
            if isinstance(feat[field_name], (int, float))
        ]

        if not values:
            QMessageBox.information(
                self, 
                self.tr("Aucune donnée"), 
                self.tr("Aucune valeur numérique disponible pour ce champ.")
            )
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
    def populate_field_combo(self, layer):
        """
        Remplit la comboBox des champs en fonction de la couche sélectionnée.
        Compatible GeoPackage et PostGIS.
        """
        self.fieldComboBox.clear()

        if not isinstance(layer, QgsVectorLayer):
            return

        # Récupération des champs
        for field in layer.fields():
            # On filtre éventuellement par type si nécessaire (ex: seulement numériques)
            if field.typeName().lower() in ["integer", "real", "double precision", "numeric", "float"]:
                self.fieldComboBox.addItem(field.name())
            else:
                # Si tu veux tout afficher, commente ce if/else
                pass

        # Infobulle explicative selon le provider
        provider = layer.dataProvider().name()
        if provider == "ogr":
            self.fieldComboBox.setToolTip(self.tr("Champs de la couche GeoPackage sélectionnée"))
        elif provider == "postgres":
            self.fieldComboBox.setToolTip(self.tr("Champs de la couche PostGIS sélectionnée"))
        else:
            self.fieldComboBox.setToolTip(self.tr("Champs de la couche vectorielle sélectionnée"))


