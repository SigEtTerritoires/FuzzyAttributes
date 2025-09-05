from qgis.PyQt.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog, QLineEdit
)
from qgis.PyQt.QtCore import QVariant, Qt
from qgis.PyQt.QtGui import QDoubleValidator
from qgis.core import QgsField, QgsProject, edit
import csv
from qgis.PyQt.QtWidgets import QMessageBox
import sqlite3
from qgis.core import QgsExpression, QgsFeatureRequest, QgsField, QgsVectorLayer,QgsApplication
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtCore import QDateTime
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QLineEdit
from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.PyQt.QtCore import Qt
from qgis.PyQt import uic
from PyQt5.QtCore import QTranslator, QCoreApplication, QLocale
import os
import getpass
import json
from qgis.PyQt.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QToolButton, QMenu, QAction, QFileDialog, QMessageBox
from qgis.core import QgsVectorLayer, QgsProject
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
import psycopg2
from qgis.core import QgsMessageLog, Qgis
from qgis.core import QgsVectorLayer, QgsFeature, QgsDataSourceUri
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'fuzzytext_dialog.ui'
))


class FuzzyTextDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, layer=None, parent=None, plugin_dir=None):
        super(FuzzyTextDialog, self).__init__(parent)
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
        # Bouton Enregistrer avec menu CSV / Couche
        # -----------------------------
        self.btnSave = QPushButton(self.tr("Enregistrer la table"))
        menu_save = QMenu(self)
        self.btnShowMetadata.clicked.connect(self.show_metadata_table) 
        action_csv = QAction(self.tr("Enregistrer en CSV"), self)
        action_csv.triggered.connect(self.save_mapping_to_csv)
        menu_save.addAction(action_csv)

        action_db = QAction(self.tr("Enregistrer dans la base de données"), self)
        action_db.triggered.connect(self.save_mapping_to_layer)
        menu_save.addAction(action_db)

        self.btnSave.setMenu(menu_save)
        self.horizontalLayoutBottom.addWidget(self.btnSave)

        # -----------------------------
        # Bouton Charger avec menu CSV / Base
        # -----------------------------
        self.btnLoad = QPushButton(self.tr("Charger une table"))
        menu_load = QMenu(self)

        action_csv_load = QAction(self.tr("Charger depuis CSV"), self)
        action_csv_load.triggered.connect(self.load_mapping_from_csv)
        menu_load.addAction(action_csv_load)

        action_db_load = QAction(self.tr("Charger depuis la base de données"), self)
        action_db_load.triggered.connect(self.load_mapping_from_db)
        menu_load.addAction(action_db_load)

        self.btnLoad.setMenu(menu_load)
        self.horizontalLayoutBottom.addWidget(self.btnLoad)

        # -----------------------------
        # Boutons classiques
        # -----------------------------
        self.btnApply.clicked.connect(self.apply_mapping)
        self.btnClose.clicked.connect(self.close)
        self.btnLoadValues.clicked.connect(self.load_unique_values)

        # -----------------------------
        # Remplissage de la combo layer
        # -----------------------------
        self.populate_layer_combo()

        # Connexion du signal layer → mise à jour combo field
        self.layerComboBox.currentIndexChanged.connect(self.on_layer_changed)

        # Sélection de la couche au lancement
        if layer:
            for key, lyr in self.layer_map.items():
                if lyr == layer:
                    index = self.layerComboBox.findText(key)
                    if index != -1:
                        self.layerComboBox.setCurrentIndex(index)
                    break
        else:
            self.layerComboBox.setCurrentIndex(0)
            self.on_layer_changed()

    # -----------------------------
    # Méthodes pour la mise à jour des champs
    # -----------------------------
    def on_layer_changed(self):
        display_name = self.layerComboBox.currentText()
        self.current_layer = self.layer_map.get(display_name)
        if self.current_layer is None:
            print("Aucune couche sélectionnée !")
            return

        # Mettre à jour combo field
        self.comboBoxTextField.clear()
        for field in self.current_layer.fields():
            if field.type() == QVariant.String:
                self.comboBoxTextField.addItem(field.name())

        self.tableMapping.setRowCount(0)
        self.btnLoadValues.setEnabled(self.comboBoxTextField.count() > 0)

    # -----------------------------
    # Remplissage combo layer
    # -----------------------------
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
                    schema = uri.schema()
                    table = layer.name()
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

    def on_layer_changed(self):
        """Quand l'utilisateur change de couche"""
        display_name = self.layerComboBox.currentText()
        self.current_layer = self.layer_map.get(display_name)
        self.tableMapping.setRowCount(0)
        self.populate_text_fields()

    def populate_text_fields(self):
        """Remplit comboBoxTextField avec les champs texte de la couche courante"""
        self.comboBoxTextField.clear()
        self.tableMapping.setRowCount(0)

        if not self.current_layer:
            self.btnLoadValues.setEnabled(False)
            self.btnApply.setEnabled(False)
            return

        for field in self.current_layer.fields():
            if field.type() == QVariant.String:
                self.comboBoxTextField.addItem(field.name())

        # Activer/désactiver les boutons
        self.btnLoadValues.setEnabled(self.comboBoxTextField.count() > 0)
        self.btnApply.setEnabled(False)




    def load_unique_values(self):
        """Remplit tableMapping avec les valeurs uniques d'un champ texte"""
        if not self.current_layer:
            QMessageBox.warning(self, "Erreur", "Aucune couche sélectionnée.")
            return

        field_name = self.comboBoxTextField.currentText()
        if not field_name:
            QMessageBox.warning(self, "Erreur", "Aucun champ texte sélectionné.")
            return

        # Définir les colonnes
        self.tableMapping.setColumnCount(2)
        self.tableMapping.setHorizontalHeaderLabels([field_name, "Fuzzy"])
        self.tableMapping.setRowCount(0)

        unique_values = set()
        provider = self.current_layer.dataProvider().name().lower()

        try:
            if "postgres" in provider:
                # --- PostGIS via SELECT DISTINCT ---
                from qgis.core import QgsDataSourceUri
                import psycopg2

                uri = QgsDataSourceUri(self.current_layer.source())
                schema = uri.schema()
                table = uri.table()
                conninfo = uri.connectionInfo(True)  # True pour inclure le mot de passe

                conn = psycopg2.connect(conninfo)
                cur = conn.cursor()
                sql = f'SELECT DISTINCT "{field_name}" FROM "{schema}"."{table}" WHERE "{field_name}" IS NOT NULL'
                cur.execute(sql)
                for row in cur.fetchall():
                    unique_values.add(str(row[0]))
                cur.close()
                conn.close()
            else:
                # --- GeoPackage / Shapefile ---
                for feat in self.current_layer.getFeatures():
                    val = feat[field_name]
                    if val is not None:
                        unique_values.add(str(val))

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de récupérer les valeurs : {e}")
            return

        # Remplir la table
        for val in sorted(unique_values):
            row = self.tableMapping.rowCount()
            self.tableMapping.insertRow(row)
            self.tableMapping.setItem(row, 0, QTableWidgetItem(val))
            self.tableMapping.setItem(row, 1, QTableWidgetItem(""))  # colonne Fuzzy vide

        # Activer le bouton Appliquer
        self.btnApply.setEnabled(len(unique_values) > 0)
        print(f"{len(unique_values)} valeurs uniques ajoutées pour le champ {field_name}.")

    def save_table(self):
        """Enregistre le mapping texte/flou dans un fichier CSV"""
        path, _ = QFileDialog.getSaveFileName(self, "Enregistrer la table", "", "CSV (*.csv)")
        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ValeurTexte", "ValeurFloue"])
            for i in range(self.tableMapping.rowCount()):
                text_val = self.tableMapping.item(i, 0).text()
                widget = self.tableMapping.cellWidget(i, 1)
                flou_val = widget.text() if widget else ""
                writer.writerow([text_val, flou_val])

        QMessageBox.information(self, "Enregistré", f"Table sauvegardée dans {path}")

    def load_table_from_file(self):
        """Charge un mapping texte/flou depuis un CSV"""
        path, _ = QFileDialog.getOpenFileName(self, "Charger une table", "", "CSV (*.csv)")
        if not path:
            return

        mapping = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                mapping.append((row["ValeurTexte"], row["ValeurFloue"]))

        self.tableMapping.setRowCount(len(mapping))
        for i, (txt, flou) in enumerate(mapping):
            item_text = QTableWidgetItem(txt)
            item_text.setFlags(item_text.flags() & ~Qt.ItemIsEditable)
            self.tableMapping.setItem(i, 0, item_text)

            editor = QLineEdit()
            validator = QDoubleValidator(0.0, 1.0, 3)
            editor.setValidator(validator)
            editor.setText(flou)
            self.tableMapping.setCellWidget(i, 1, editor)

        self.tableMapping.resizeColumnsToContents()
        self.btnApply.setEnabled(True)

    def apply_mapping(self):
        """Crée ou met à jour l'attribut flou dans le layer courant"""
        if not self.current_layer:
            return

        # Nom de l'attribut source
        field_name = self.comboBoxTextField.currentText()
        if not field_name:
            return

        # Nom de l'attribut flou
        fuzzy_field = f"{field_name}_fuzzy"

        # Vérifier si le champ existe déjà, sinon le créer
        layer_fields = self.current_layer.fields()
        if fuzzy_field not in [f.name() for f in layer_fields]:
            self.current_layer.dataProvider().addAttributes([QgsField(fuzzy_field, QVariant.Double)])
            self.current_layer.updateFields()

        # Créer un dictionnaire valeur → fuzzy
        mapping = {}
        for row in range(self.tableMapping.rowCount()):
            val_item = self.tableMapping.item(row, 0)
            fuzzy_item = self.tableMapping.item(row, 1)
            if val_item and fuzzy_item:
                try:
                    fuzzy_value = float(fuzzy_item.text())
                    # S'assurer que la valeur est entre 0 et 1
                    if 0 <= fuzzy_value <= 1:
                        mapping[val_item.text()] = fuzzy_value
                    else:
                        QMessageBox.warning(
                            self,
                            "Valeur floue incorrecte",
                            f"Valeur floue {fuzzy_item.text()} pour '{val_item.text()}' doit être entre 0 et 1."
                        )
                except ValueError:
                    QMessageBox.warning(
                        self,
                        "Valeur floue incorrecte",
                        f"Valeur floue '{fuzzy_item.text()}' pour '{val_item.text()}' n’est pas un nombre."
                    )

        # Mettre à jour les features du layer
        self.current_layer.startEditing()
        for feat in self.current_layer.getFeatures():
            val = str(feat[field_name])
            if val in mapping:
                feat[fuzzy_field] = mapping[val]
                self.current_layer.updateFeature(feat)
        self.current_layer.commitChanges()
         # Ajouter les métadonnées
        fuzzy_code='text'

        field_name = self.comboBoxTextField.currentText() or "ValeurTexte"

        # On stockera les lignes sous forme de texte
        lines = [f"{field_name};Fuzzy"]

        for row in range(self.tableMapping.rowCount()):
            text_item = self.tableMapping.item(row, 0)
            fuzzy_item = self.tableMapping.item(row, 1)
            line = f"{text_item.text() if text_item else ''};{fuzzy_item.text() if fuzzy_item else ''}"
            lines.append(line)
        provider = self.current_layer.dataProvider()
        # Joindre toutes les lignes avec des retours à la ligne
        params = "\n".join(lines)
        if provider.name().lower() in ["postgres", "postgis"]:
            table_name = self.current_layer.name()  # nom de la table PostGIS
            self.append_metadata(
                self.current_layer,
                fuzzy_field,
                fuzzy_code,
                params,
                source1='[PG]'+table_name,
                provider="postgres"
            )
        else:
            gpkg_path = self.current_layer.source().split('|')[0]
            table_name = self.current_layer.name()  # nom de la couche dans le GeoPackage
            self.append_metadata(
                gpkg_path,
                fuzzy_field,
                fuzzy_code,
                params,
                source1='[GPKG]'+table_name,
                provider="ogr"
            )

        QMessageBox.information(
            self,
            "Fini",
            f"Attribut flou '{fuzzy_field}' mis à jour dans le layer."
        )

        self.btnApply.setEnabled(False)


    def load_mapping(self):
        """Charge une table de correspondance JSON"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Charger table de correspondance"),
            "",
            "JSON (*.json)"
        )
        if not filepath:
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr("Erreur de lecture"),
                self.tr(f"Impossible de lire le fichier : {e}")
            )
            return

        # Vérifier correspondance du champ
        field_name = self.comboBoxTextField.currentText()
        if data.get("field") != field_name:
            QMessageBox.warning(
                self,
                self.tr("Incohérence détectée"),
                self.tr(f"Le fichier correspond au champ '{data.get('field')}', "
                        f"mais vous avez sélectionné '{field_name}'.\n\n"
                        "Veuillez sélectionner le bon champ ou un autre fichier.")
            )
            return

        # Appliquer le mapping dans la table
        mapping = data.get("mapping", {})
        for i in range(self.tableMapping.rowCount()):
            text_item = self.tableMapping.item(i, 0)
            if not text_item:
                continue
            text_val = text_item.text()
            if text_val in mapping:
                self.tableMapping.cellWidget(i, 1).setText(str(mapping[text_val]))


    def setup_save_button(self):
        """Configure le bouton Enregistrer avec menu déroulant"""
        self.btnSave = QToolButton(self)
        self.btnSave.setText(self.tr("Enregistrer la table"))
        self.btnSave.setPopupMode(QToolButton.MenuButtonPopup)

        menu = QMenu(self)

        action_csv = QAction(self.tr("Sauvegarder en CSV"), self)
        action_csv.triggered.connect(self.save_mapping_to_csv)
        menu.addAction(action_csv)

        action_db = QAction(self.tr("Sauvegarder dans la base de données"), self)
        action_db.triggered.connect(self.save_mapping_to_db)
        menu.addAction(action_db)

        self.btnSave.setMenu(menu)
        self.horizontalLayoutBottom.addWidget(self.btnSave)



    def setup_load_button(self):
        """Configure le bouton Charger avec menu déroulant"""
        self.btnLoad = QToolButton(self)
        self.btnLoad.setText(self.tr("Charger la table"))
        self.btnLoad.setPopupMode(QToolButton.MenuButtonPopup)

        menu = QMenu(self)

        action_csv = QAction(self.tr("Charger depuis CSV"), self)
        action_csv.triggered.connect(self.load_mapping_from_csv)
        menu.addAction(action_csv)

        action_db = QAction(self.tr("Charger depuis la base de données"), self)
        action_db.triggered.connect(self.load_mapping_from_layer)
        menu.addAction(action_db)

        self.btnLoad.setMenu(menu)
        self.horizontalLayoutBottom.addWidget(self.btnLoad)

 

    # -------------------------
    # Sauvegarde en CSV
    # -------------------------
    def save_mapping_to_csv(self):
        """Enregistre le mapping texte/flou dans un fichier CSV"""
        path, _ = QFileDialog.getSaveFileName(self, "Enregistrer la table en CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        field_name = self.comboBoxTextField.currentText() or "ValeurTexte"

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
            QMessageBox.critical(self, "Erreur", f"Impossible de sauvegarder en CSV : {e}")

    def get_selected_layer(self):
        index = self.layerComboBox.currentIndex()
        if index >= 0:
            layer = self.layerComboBox.itemData(index)
            return layer
        return None
    def save_mapping_to_layer(self):
        """Sauvegarde le mapping texte/flou dans une table séparée PostGIS ou GeoPackage."""
        if not self.current_layer:
            QMessageBox.warning(self, "Erreur", "Aucune couche sélectionnée.")
            return

        field_name = self.comboBoxTextField.currentText()
        fuzzy_table = f"{field_name}_fuzzy"
        provider = self.current_layer.dataProvider().name()

        # --- Cas GeoPackage ---
        if provider == "ogr" and (self.current_layer.source().lower().endswith(".gpkg") or ".gpkg|" in self.current_layer.source().lower()):
            path = self.current_layer.source().split("|")[0]
            conn = sqlite3.connect(path)
            cur = conn.cursor()
            cur.execute(f'CREATE TABLE IF NOT EXISTS "{fuzzy_table}" (valeur TEXT PRIMARY KEY, fuzzy REAL)')
            cur.execute(f'DELETE FROM "{fuzzy_table}"')

            for row in range(self.tableMapping.rowCount()):
                val_item = self.tableMapping.item(row, 0)
                fuzzy_item = self.tableMapping.item(row, 1)
                val = val_item.text() if val_item else None
                fuzzy = float(fuzzy_item.text()) if fuzzy_item and fuzzy_item.text() else None
                if val is not None:
                    cur.execute(f'INSERT INTO "{fuzzy_table}" (valeur, fuzzy) VALUES (?, ?)', (val, fuzzy))

            conn.commit()
            conn.close()
            QMessageBox.information(self, "Succès", f"Table {fuzzy_table} sauvegardée dans GeoPackage.")
            return

        # --- Cas PostGIS ---
        elif provider == "postgres":
            import psycopg2
            uri = self.current_layer.dataProvider().uri()
            schema = uri.schema()
            conninfo = uri.connectionInfo(True)

            conn = psycopg2.connect(conninfo)
            cur = conn.cursor()

            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS "{schema}"."{fuzzy_table}" (
                    valeur TEXT PRIMARY KEY,
                    fuzzy DOUBLE PRECISION
                )
            """)
            cur.execute(f'DELETE FROM "{schema}"."{fuzzy_table}"')

            for row in range(self.tableMapping.rowCount()):
                val_item = self.tableMapping.item(row, 0)
                fuzzy_item = self.tableMapping.item(row, 1)
                val = val_item.text() if val_item else None
                fuzzy = float(fuzzy_item.text()) if fuzzy_item and fuzzy_item.text() else None
                if val is not None:
                    cur.execute(f'INSERT INTO "{schema}"."{fuzzy_table}" (valeur, fuzzy) VALUES (%s, %s)', (val, fuzzy))

            conn.commit()
            conn.close()
            QMessageBox.information(self, "Succès", f"Table {fuzzy_table} sauvegardée dans PostGIS (schema {schema}).")
            return

        else:
            QMessageBox.warning(self, "Erreur", "Fournisseur de données non supporté.")

        # -------------------------
        # Chargement depuis CSV
        # -------------------------
    def load_mapping_from_csv(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Charger une table CSV", "", "CSV Files (*.csv)"
        )
        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=";")
                rows = list(reader)

            if not rows:
                QMessageBox.warning(self, "Attention", "Le fichier CSV est vide.")
                return

            # Vérifier que le CSV contient bien une colonne Fuzzy
            headers = reader.fieldnames
            if not headers or "Fuzzy" not in headers:
                QMessageBox.critical(self, "Erreur", "Le CSV doit contenir une colonne 'Fuzzy'.")
                return

            # Récupérer le champ dynamique (le premier différent de Fuzzy)
            field_name = [h for h in headers if h != "Fuzzy"][0]

            # Construire le mapping depuis le CSV
            mapping = {row[field_name]: row["Fuzzy"] for row in rows}

            # Récupérer la couche courante
            layer = self.get_selected_layer()
            unique_values = set()
            if layer:
                if field_name in [f.name() for f in layer.fields()]:
                    idx = layer.fields().indexOf(field_name)
                    unique_values = layer.uniqueValues(idx)
                else:
                    QMessageBox.warning(
                        self,
                        "Attention",
                        f"Le champ '{field_name}' trouvé dans le CSV n’existe pas dans la couche sélectionnée.\n"
                        f"Champs disponibles : {', '.join([f.name() for f in layer.fields()])}"
                    )

            # Union : valeurs du CSV + valeurs uniques de la couche
            all_values = set(mapping.keys()) | set(unique_values)

            # Fusion : garder les correspondances existantes si elles existent
            final_rows = [(val, mapping.get(val, "")) for val in sorted(all_values, key=lambda x: str(x))]

            # Remplir le tableau
            self.tableMapping.setColumnCount(2)
            self.tableMapping.setRowCount(0)
            self.tableMapping.setHorizontalHeaderLabels([field_name, "Fuzzy"])

            for val, fuzzy in final_rows:
                row_idx = self.tableMapping.rowCount()
                self.tableMapping.insertRow(row_idx)
                self.tableMapping.setItem(row_idx, 0, QTableWidgetItem(str(val)))
                self.tableMapping.setItem(row_idx, 1, QTableWidgetItem(str(fuzzy) if fuzzy is not None else ""))

            QMessageBox.information(self, "Succès", f"Table chargée depuis {path}")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger le CSV : {e}")

    def load_mapping_from_db(self):
        """Charge le mapping depuis la table séparée PostGIS ou GeoPackage,
           en gardant aussi les valeurs absentes de la couche mais présentes dans la table fuzzy.
        """
        if not self.current_layer:
            QMessageBox.warning(self, "Erreur", "Aucune couche sélectionnée.")
            return

        field_name = self.comboBoxTextField.currentText()
        fuzzy_table = f"{field_name}_fuzzy"
        provider = self.current_layer.dataProvider().name()

        rows = []
        # --- Cas GeoPackage ---
        if provider == "ogr" and (self.current_layer.source().lower().endswith(".gpkg") or ".gpkg|" in self.current_layer.source().lower()):
            path = self.current_layer.source().split("|")[0]
            conn = sqlite3.connect(path)
            cur = conn.cursor()
            try:
                cur.execute(f'SELECT valeur, fuzzy FROM "{fuzzy_table}"')
                rows = cur.fetchall()
            except sqlite3.OperationalError:
                QMessageBox.information(self, "Info", f"Aucune table {fuzzy_table} trouvée.")
            conn.close()

        # --- Cas PostGIS ---
        elif provider == "postgres":
            import psycopg2
            uri = self.current_layer.dataProvider().uri()
            schema = uri.schema()
            conninfo = uri.connectionInfo(True)
            conn = psycopg2.connect(conninfo)
            cur = conn.cursor()
            try:
                cur.execute(f'SELECT valeur, fuzzy FROM "{schema}"."{fuzzy_table}"')
                rows = cur.fetchall()
            except psycopg2.errors.UndefinedTable:
                QMessageBox.information(self, "Info", f"Aucune table {fuzzy_table} trouvée.")
            conn.close()

        else:
            QMessageBox.warning(self, "Erreur", "Fournisseur de données non supporté.")
            return

        # --- Créer un dict pour les correspondances existantes ---
        mapping = {val: fuzzy for val, fuzzy in rows}

        # --- Extraire toutes les valeurs uniques de la couche ---
        unique_values = self.current_layer.uniqueValues(self.current_layer.fields().indexOf(field_name))

        # --- Union : valeurs présentes dans la couche + valeurs présentes dans la table ---
        all_values = set(unique_values) | set(mapping.keys())

        # --- Fusionner : garder les correspondances existantes si elles existent ---
        final_rows = [(val, mapping.get(val, "")) for val in sorted(all_values, key=lambda x: str(x))]

        # --- Remplissage de la tableMapping ---
        self.tableMapping.setColumnCount(2)
        self.tableMapping.setHorizontalHeaderLabels([field_name, "Fuzzy"])
        self.tableMapping.setRowCount(0)

        for val, fuzzy in final_rows:
            row_idx = self.tableMapping.rowCount()
            self.tableMapping.insertRow(row_idx)
            self.tableMapping.setItem(row_idx, 0, QTableWidgetItem(str(val)))
            self.tableMapping.setItem(row_idx, 1, QTableWidgetItem(str(fuzzy) if fuzzy is not None else ""))

        self.btnApply.setEnabled(True)

    # -------------------------
    # Chargement depuis Base
    # -------------------------
    def load_mapping_from_layer(self):
        """Charge les valeurs texte/flou depuis la couche active."""
        if not self.current_layer:
            QMessageBox.warning(self, "Erreur", "Aucune couche sélectionnée.")
            return

        field_name = self.comboBoxTextField.currentText()
        fuzzy_field = f"{field_name}_fuzzy"

        # Vérifier si le champ flou existe
        if fuzzy_field not in [f.name() for f in self.current_layer.fields()]:
            QMessageBox.warning(
                self,
                "Erreur",
                f"Le champ {fuzzy_field} n'existe pas dans la couche."
            )
            return

        # Vider le tableau actuel
        self.tableMapping.setRowCount(0)

        # Charger les valeurs depuis la couche
        unique_vals = set()
        for feat in self.current_layer.getFeatures():
            val = feat[field_name]
            fuzzy_val = feat[fuzzy_field]
            if val not in unique_vals:  # éviter doublons
                row = self.tableMapping.rowCount()
                self.tableMapping.insertRow(row)

                item_val = QTableWidgetItem(str(val))
                item_fuzzy = QTableWidgetItem("" if fuzzy_val is None else str(fuzzy_val))

                self.tableMapping.setItem(row, 0, item_val)
                self.tableMapping.setItem(row, 1, item_fuzzy)

                unique_vals.add(val)

        QMessageBox.information(
            self,
            "Chargement terminé",
            f"{len(unique_vals)} valeurs chargées depuis la couche."
        )


    # -------------------------
    # Fusion avec les valeurs actuelles
    # -------------------------
    def populate_table_with_mapping(self, mapping):
        """Met à jour la table avec les valeurs uniques du champ + fuzzy existants."""
        field_name = self.comboBoxTextField.currentText()
        if not field_name or not self.current_layer:
            return

        unique_values = self.current_layer.uniqueValues(self.current_layer.fields().indexOf(field_name))

        self.tableWidget.setRowCount(len(unique_values))
        for row, val in enumerate(unique_values):
            item_val = QTableWidgetItem(str(val))
            self.tableWidget.setItem(row, 0, item_val)

            if str(val) in mapping:
                fuzzy_val = str(mapping[str(val)])
            else:
                fuzzy_val = ""

            item_fuzzy = QTableWidgetItem(fuzzy_val)
            item_fuzzy.setFlags(item_fuzzy.flags() | Qt.ItemIsEditable)
            self.tableWidget.setItem(row, 1, item_fuzzy)

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

                QgsMessageLog.logMessage(
                    f"[DEBUG fuzzytext] Tentative de chargement URI={meta_uri.uri()}",
                    "FuzzyPlugin",
                    Qgis.Info
                )

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

