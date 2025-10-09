# -*- coding: utf-8 -*-

from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QRadioButton,
    QButtonGroup, QPushButton, QGroupBox, QLineEdit
)
from qgis.PyQt.QtCore import Qt
from functools import partial
from qgis.core import QgsProject
from qgis.PyQt.QtWidgets import QDialogButtonBox, QMessageBox
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import QFileDialog




class RasterAggregationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Préparation Agrégation Raster"))
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # --- Sélection des couches ---
        self.comboRaster1 = QComboBox()
        self.comboRaster2 = QComboBox()
        layout.addWidget(QLabel("Raster 1 :"))
        layout.addWidget(self.comboRaster1)
        layout.addWidget(QLabel("Raster 2 :"))
        layout.addWidget(self.comboRaster2)


        self.outputNameLabel = QLabel(self.tr("Nom raster de sortie :"), self)
        self.outputNameEdit = QLineEdit(self)
        self.outputNameEdit.setText(self.tr("Aggregation_Result"))  # valeur par défaut

        self.outputDirLabel = QLabel(self.tr("Dossier de sortie :"), self)
        self.outputDirEdit = QLineEdit(self)
        self.outputDirEdit.setText(QgsProject.instance().homePath())  # par défaut le dossier projet
        self.chooseDirButton = QPushButton(self.tr("Parcourir..."), self)

        # layout
        layout_name = QHBoxLayout()
        layout_name.addWidget(self.outputNameLabel)
        layout_name.addWidget(self.outputNameEdit)
        layout.addLayout(layout_name)

        layout_dir = QHBoxLayout()
        layout_dir.addWidget(self.outputDirLabel)
        layout_dir.addWidget(self.outputDirEdit)
        layout_dir.addWidget(self.chooseDirButton)
        layout.addLayout(layout_dir)

        # connecter le bouton
        self.chooseDirButton.clicked.connect(self.choose_output_folder)


        # --- Étendue ---
        extent_group = QGroupBox(self.tr("Étendue spatiale"))
        extent_layout = QVBoxLayout()
        self.extIntersection = QRadioButton(self.tr("Intersection (zone commune)"))
        self.extUnion = QRadioButton(self.tr("Union (couvrir toute la zone)"))
        self.extIntersection.setChecked(True)
        extent_layout.addWidget(self.extIntersection)
        extent_layout.addWidget(self.extUnion)
        extent_group.setLayout(extent_layout)
        layout.addWidget(extent_group)

        # --- Méthode de rééchantillonnage ---
        layout.addWidget(QLabel(self.tr("Méthode de rééchantillonnage :")))
        self.resamplingCombo = QComboBox()
        self.resamplingCombo.addItems([
            "Nearest Neighbor", "Bilinear", "Cubic", "Lanczos"
        ])
        layout.addWidget(self.resamplingCombo)
        # --- Bouton pour définir la fonction d'agrégation ---
        h = QHBoxLayout()
        self.btnDefineFunction = QPushButton(self.tr("Définir la fonction d'agrégation..."))
        self.lblFunctionSummary = QLabel(self.tr("Aucune fonction définie"))
        self.lblFunctionSummary.setStyleSheet("color: gray;")
        h.addWidget(self.btnDefineFunction)
        h.addWidget(self.lblFunctionSummary, 1)
        layout.addLayout(h)
                # Récupérer les noms des couches sélectionnées dans les comboBox
        nom_couche_1 = f"{self.comboRaster1.currentText()}"
        nom_couche_2 = f"{self.comboRaster2.currentText()}"
        

        # ...
        self.btnDefineFunction.clicked.connect(
            partial(self.open_aggregation_function_dialog, self.comboRaster1, self.comboRaster2)
        )

        # --- Boutons ---
        btn_layout = QHBoxLayout()

        self.btnHelp = QPushButton(self.tr("Aide"))
        self.btnHelp.setFixedWidth(90)  # petit bouton carré
        btn_layout.addWidget(self.btnHelp)

        btn_layout.addStretch()  # pousse les autres boutons à droite

        self.btnOk = QPushButton("OK")
        self.btnCancel = QPushButton(self.tr("Annuler"))
        btn_layout.addWidget(self.btnOk)
        btn_layout.addWidget(self.btnCancel)

        layout.addLayout(btn_layout)

        # connexion du bouton aide
        self.btnHelp.clicked.connect(self.show_help)


        self.btnOk.clicked.connect(self.validate_and_accept)
        self.btnCancel.clicked.connect(self.reject)

    def show_help(self):
        QMessageBox.information(
            self,self.tr(
            "Aide - Agrégation raster"),self.tr("Ce module permet d'agréger deux rasters avec une fonction floue.\n\n"
             "Étapes :\n"
             "1. Choisissez Raster 1 et Raster 2.\n"
             "   Les deux rasters doivent avoir le même CRS et être projetés. \n"
             "   Le raster 1 détermine la résolution du résultat.\n" 
             "2. Définissez l'étendue : intersection ou union.\n"
             "3. Choisissez le dossier et le nom du fichier de sortie.\n"
             "4. Lancez l'agrégation.\n\n"
             "Le résultat est un raster GeoTIFF enregistré dans le dossier choisi.")
        )

    # fonction pour choisir le dossier
    def choose_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, self.tr("Choisir dossier de sortie"), self.outputDirEdit.text())
        if folder:
            self.outputDirEdit.setText(folder)
    def get_config(self):
        nomfic="agg_"+self.outputNameEdit.text()
        config = {
            "raster1": self.comboRaster1.currentData(),  # l’ID plutôt que le nom
            "raster2": self.comboRaster2.currentData(),
            "raster1_name": self.comboRaster1.currentText(),
            "raster2_name": self.comboRaster2.currentText(),
            "output_name" : nomfic,
            "output_dir" : self.outputDirEdit.text(),
            "extent": "intersection" if self.extIntersection.isChecked() else "union",
            "resampling": self.resamplingCombo.currentText(),
            "function_code": getattr(self, "aggregation_function_code", None),
            "function": getattr(self, "aggregation_function", None),
        }
        return config

    def open_aggregation_function_dialog(self, combo1, combo2):
        from .aggregation_function_dialog import AggregationFunctionDialog

        # récupérer les noms actuels
        nom_couche_1 = combo1.currentText()
        nom_couche_2 = combo2.currentText()

        dlg = AggregationFunctionDialog()
        dlg.set_criteria_labels(nom_couche_1, nom_couche_2)

        # si tu as déjà une fonction définie
        # Si tu as déjà une fonction définie
        if hasattr(self, "aggregation_function_code") and self.aggregation_function_code:
            dlg.set_selected_values(self.aggregation_function_code)


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

        # Lancement du dialogue
        if dlg.exec():
            result = dlg.get_selected_values()
            self.aggregation_function_code = result
            # ⚠️ ta variable s'appelle self.lblFunctionSummary, pas self.functionLabel
            self.lblFunctionSummary.setText(f"Code sélectionné : {result}")
            self.lblFunctionSummary.setStyleSheet("")  # couleur normale
    def validate_and_accept(self):
        if not self.aggregation_function_code:
            QMessageBox.warning(
                self,self.tr(
                "Fonction manquante"),
                self.tr("Veuillez définir une fonction d’agrégation avant de continuer.")
            )
            return

        # --- Vérification d’incohérence ---
        if not self.is_aggregation_code_consistent(self.aggregation_function_code):
            details = self.explain_inconsistency(self.aggregation_function_code)
            reply = QMessageBox.question(
                self,self.tr(
                "Vérification de la combinaison"),
                self.tr(f"La combinaison semble incohérente :\n\n{details}\n\nVoulez-vous continuer ?"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return

        # --- Construire la fonction ---
        try:
            from .fuzzy_functions import get_aggregation_function
            self.aggregation_function = get_aggregation_function(self.aggregation_function_code)
        except Exception as e:
            QMessageBox.critical(
                self,self.tr(
                "Erreur"),
                self.tr(f"Impossible de construire la fonction d’agrégation.\n\n{e}")
            )
            return

        self.accept()
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
            msgs.append(self.self.tr(
                "Règle 1 violée : R3 (A=0,5 ; B=1) doit être >= max(R1, R2).")
            )
        if R3 < 0.5:
            msgs.append(self.self.tr(
                "Règle 2 violée : R3 (A=0,5 ; B=1) doit être >= 0,5.")
            )
        return "\n".join(msgs)
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
    def _decode_digit(self,d):
        """'0'→1.0, '1'→0.75, '2'→0.5, '3'→0.25, '4'→0.0"""
        mapping = {"0": 1.0, "1": 0.75, "2": 0.5, "3": 0.25, "4": 0.0}
        return mapping.get(d, None)