# -*- coding: utf-8 -*-
import os, tempfile
import numpy as np
from qgis.core import (QgsCoordinateTransformContext,QgsProcessingUtils, QgsRasterFileWriter, QgsRasterPipe, QgsRasterResampler)
from qgis.core import QgsCoordinateReferenceSystem
import processing
from qgis.core import (QgsProcessingFeedback,QgsProcessing, 
    QgsRectangle, QgsGeometry, QgsFeature, QgsVectorLayer, QgsField)
from qgis.PyQt.QtCore import QVariant
from qgis.core import (QgsRasterBlock, QgsRasterDataProvider, QgsUnitTypes)
from qgis.core import (QgsRasterProjector, QgsRaster)
from qgis.core import (
    QgsColorRampShader, QgsRasterShader,
    QgsSingleBandPseudoColorRenderer
)
from qgis.PyQt.QtGui import QColor
from qgis.core import (
    QgsProject, QgsRasterLayer, 
    )
from qgis.PyQt.QtWidgets import QMessageBox

from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtWidgets import QDialog
from datetime import datetime
from getpass import getuser
import csv
def tr(text, context="FuzzyAttributes"):
    return QCoreApplication.translate(context, text)


def is_geographic(crs):
    """Retourne True si le CRS est géographique (degrés)."""
    return "4326" in crs.authid()

def run_raster_aggregate(self):
    """
    Méthode plugin : ouvre le dialogue et appelle le traitement
    """
    from .fuzzyaggregation_raster_dialog import RasterAggregationDialog


    dlg = RasterAggregationDialog(self.iface.mainWindow())

    # Remplir les combos avec les rasters du projet
    for layer in QgsProject.instance().mapLayers().values():
        if isinstance(layer, QgsRasterLayer):
            dlg.comboRaster1.addItem(layer.name(), layer.id())
            dlg.comboRaster2.addItem(layer.name(), layer.id())

    if dlg.exec():
        config = dlg.get_config()
        try:
            # ⚡ traitement raster
            output_layer = raster_processing.run_raster_aggregation(config)

            # Debug affichage config
            debug_msg = [
                "=== DEBUG Agrégation Raster ===",
                f"Raster1: {config['raster1_name']} (id={config['raster1']})",
                f"Raster2: {config['raster2_name']} (id={config['raster2']})",
                f"CRS: {config['crs']}",
                f"Résolution: {config['resolution']} (X={config['res_x']} Y={config['res_y']})",
                f"Étendue: {config['extent']}",
                f"Resampling: {config['resampling']}",
                f"Function code: {config['function_code']}",
                f"Function obj: {config['function']}",
            ]
            debug_text = "\n".join(debug_msg)

            self.iface.messageBar().pushInfo("Agrégation Raster", debug_text)
            print(debug_text)

            if output_layer:
                QgsProject.instance().addMapLayer(output_layer)

        except Exception as e:
            self.iface.messageBar().pushWarning("Erreur agrégation raster", str(e))
            import traceback
            print("Erreur run_raster_aggregate:", traceback.format_exc())



def is_geographic(crs):
    """Retourne True si le CRS est géographique (unités en degrés)."""
    return crs.mapUnits() == QgsUnitTypes.DistanceUnit.DistanceDegrees

def make_common_grid(r1, r2, extent_mode="intersection", resolution="r1"):
    # --- Étendue commune ---
    if extent_mode == "intersection":
        extent = r1.extent().intersect(r2.extent())
    else:
        extent = QgsRectangle(r1.extent())
        extent.combineExtentWith(r2.extent())

    if extent.isEmpty():
        raise ValueError("⚠️ Intersection vide")

    # --- Résolution ---
    if resolution == "r1":
        res_x, res_y = r1.rasterUnitsPerPixelX(), r1.rasterUnitsPerPixelY()
    else:
        res_x, res_y = r2.rasterUnitsPerPixelX(), r2.rasterUnitsPerPixelY()

    # --- Taille grille ---
    xmin, xmax = extent.xMinimum(), extent.xMaximum()
    ymin, ymax = extent.yMinimum(), extent.yMaximum()

    width  = int(round((xmax - xmin) / res_x))
    height = int(round((ymax - ymin) / res_y))

    return extent, res_x, res_y, width, height


def reproject_and_resample(raster, target_crs, xmin, xmax, ymin, ymax, width, height, name="reproj"):
    feedback = QgsProcessingFeedback()
    out_path = os.path.join(tempfile.gettempdir(), f"{name}.tif")

    params = {
        'INPUT': raster,
        'TARGET_CRS': target_crs.toWkt(),
        'RESAMPLING': 0,  # nearest neighbour
        'OUTPUT': out_path,
        'TARGET_EXTENT': f"{xmin},{xmax},{ymin},{ymax}",
        'WIDTH': width,
        'HEIGHT': height,
    }

    processing.run("gdal:warpreproject", params, feedback=feedback)

    layer = QgsRasterLayer(out_path, name)
    if not layer.isValid():
        raise Exception(f"Échec reprojection de {raster.name()}")
    return layer


def raster_to_array(raster):
    """
    Lit un raster aligné en array NumPy 2D.
    """
    provider = raster.dataProvider()
    block = provider.block(1, raster.extent(), raster.width(), raster.height())
    arr = np.zeros((raster.height(), raster.width()), dtype=float)
    for row in range(raster.height()):
        for col in range(raster.width()):
            arr[row, col] = block.value(col, row)
    nodata = provider.sourceNoDataValue(1)
    arr[arr == nodata] = np.nan
    return arr

def pick_resolution_consistent(r1, r2, config):
    """
    Choisit une résolution cohérente si CRS différents (proj vs géo).
    """
    if config["resolution"] == "manual":
        return config["res_x"], config["res_y"]
    elif config["resolution"] == "r1":
        return r1.rasterUnitsPerPixelX(), r1.rasterUnitsPerPixelY()
    elif config["resolution"] == "r2":
        return r2.rasterUnitsPerPixelX(), r2.rasterUnitsPerPixelY()
    else:  # "fine"
        # si un raster en degrés (EPSG:4326) et l'autre projeté → choisir résolution du raster projeté
        if r1.crs().authid() == "EPSG:4326" and r2.crs().authid() != "EPSG:4326":
            return r2.rasterUnitsPerPixelX(), r2.rasterUnitsPerPixelY()
        elif r2.crs().authid() == "EPSG:4326" and r1.crs().authid() != "EPSG:4326":
            return r1.rasterUnitsPerPixelX(), r1.rasterUnitsPerPixelY()
        else:
            return min(r1.rasterUnitsPerPixelX(), r2.rasterUnitsPerPixelX()), \
                   min(r1.rasterUnitsPerPixelY(), r2.rasterUnitsPerPixelY())

import os
import tempfile
from osgeo import gdal

def warp_align_exact(input_path, output_name, extent, width, height, target_srs):
    """
    Reprojette et rééchantillonne un raster pour qu'il ait exactement
    l'étendue et le nombre de pixels souhaités.

    Parameters:
        input_path (str): chemin vers le raster source
        output_name (str): nom du fichier temporaire de sortie
        extent (QgsRectangle): étendue cible
        width (int): nombre de colonnes
        height (int): nombre de lignes
        target_srs (str ou QgsCoordinateReferenceSystem): CRS cible (EPSG:xxx)
    
    Returns:
        output_path (str): chemin du raster aligné
    """
    output_path = os.path.join(tempfile.gettempdir(), output_name)

    # Calculer la résolution
    res_x = (extent.xMaximum() - extent.xMinimum()) / width
    res_y = (extent.yMaximum() - extent.yMinimum()) / height

    # Si target_srs est un QgsCRS, récupérer l'EPSG
    if hasattr(target_srs, 'authid'):
        target_srs = target_srs.authid()  # ex: "EPSG:4326"

    gdal.Warp(
        destNameOrDestDS=output_path,
        srcDSOrSrcDSTab=input_path,
        format='GTiff',
        width=width,
        height=height,
        xRes=res_x,
        yRes=res_y,
        dstSRS=target_srs,
        outputBounds=(extent.xMinimum(), extent.yMinimum(),
                      extent.xMaximum(), extent.yMaximum()),
        resampleAlg=gdal.GRA_NearestNeighbour,
        targetAlignedPixels=True
    )

    if not os.path.exists(output_path):
        raise Exception(f"Échec du warp pour {input_path}")

    return output_path

def raster_to_array_gdal(path):
    ds = gdal.Open(path)
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray().astype(np.float32)
    nodata = band.GetNoDataValue()
    if nodata is not None:
        arr[arr == nodata] = np.nan
    return arr

def run_raster_aggregation(config):
    """
    Agrège deux rasters avec une fonction floue pixel par pixel.
    Retourne un QgsRasterLayer temporaire.
    """

    import tempfile
    import os
    import numpy as np
    from qgis.core import QgsProject, QgsRasterLayer


    # --- Rasters sources ---
    raster1 = QgsProject.instance().mapLayer(config["raster1"])
    raster2 = QgsProject.instance().mapLayer(config["raster2"])
    func = config["function"]

    if not raster1 or not raster2:
        raise ValueError("Impossible de retrouver les rasters")
    if not func:
        raise ValueError("Pas de fonction d’agrégation définie")

    # --- CRS cible (condition préalable : tous les rasters doivent être dans le même CRS) ---
    target_crs = raster1.crs()

    # --- Étendue cible ---
    if config["extent"] == "intersection":
        extent = raster1.extent().intersect(raster2.extent())
    else:  # union
        extent = QgsRectangle(raster1.extent())
        extent.combineExtentWith(raster2.extent())

    if extent.isEmpty():
        raise ValueError("Les rasters ne se superposent pas (intersection vide).")

    # --- Taille exacte du raster final (en pixels) ---
    # Par exemple : choisir le raster 1 comme référence pour width / height
    width = int(extent.width() / raster1.rasterUnitsPerPixelX())
    height = int(extent.height() / raster1.rasterUnitsPerPixelY())

    # --- Aligner exactement les rasters ---
    r1_path = warp_align_exact(raster1.dataProvider().dataSourceUri(), "r1_aligned.tif",
                               extent, width, height, target_crs)
    r2_path = warp_align_exact(raster2.dataProvider().dataSourceUri(), "r2_aligned.tif",
                               extent, width, height, target_crs)

    # --- Lire les rasters alignés en numpy array ---
    arr1 = raster_to_array_gdal(r1_path)
    arr2 = raster_to_array_gdal(r2_path)

    if arr1.shape != arr2.shape:
        raise ValueError(f"Shapes finales incompatibles: {arr1.shape} vs {arr2.shape}")

    # --- Appliquer la fonction floue pixel par pixel ---
    mask = np.isnan(arr1) | np.isnan(arr2)
    result = np.full_like(arr1, -9999, dtype=float)
    result[~mask] = func(arr1[~mask], arr2[~mask])



    out_dir = config.get("output_dir")  # ici on prend le dossier choisi par l'utilisateur
    if not out_dir:
        out_dir = tempfile.gettempdir()  # fallback si vide ou None

    out_name = config.get("output_name", "Aggregation_Result")
    out_path = os.path.join(out_dir, f"{out_name}.tif")

    # --- Vérification si le fichier existe ---
    if os.path.exists(out_path):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Fichier existant")
        msg.setText(f"Le fichier {out_name}.tif existe déjà dans {out_dir}.")
        msg.setInformativeText("Voulez-vous l'écraser ?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)

        reply = msg.exec()  # Bloque jusqu'à ce que l'utilisateur choisisse

        if reply == QMessageBox.StandardButton.No:
            # Ajouter un suffixe numérique
            base, ext = os.path.splitext(out_name)
            i = 1
            while os.path.exists(os.path.join(out_dir, f"{base}_{i}.tif")):
                i += 1
            out_name = f"{base}_{i}"
            out_path = os.path.join(out_dir, f"{out_name}.tif")
    driver = gdal.GetDriverByName("GTiff")

    # Crée le raster avec les mêmes dimensions et type
    out_raster = driver.Create(out_path, width, height, 1, gdal.GDT_Float32)

    # Géotransform
    out_raster.SetGeoTransform([
        extent.xMinimum(),         # top left x
        extent.width() / width,    # pixel size x
        0,                         # rotation
        extent.yMaximum(),         # top left y
        0,                         # rotation
        -extent.height() / height  # pixel size y (négatif)
    ])

    # Projection
    out_raster.SetProjection(target_crs.toWkt())

    # Écriture des valeurs
    out_band = out_raster.GetRasterBand(1)
    out_band.WriteArray(result)
    out_band.SetNoDataValue(-9999)
    out_raster.FlushCache()
    out_raster = None

    # --- Charger en QgsRasterLayer ---
    output_layer = QgsRasterLayer(out_path, out_name)  # ici on prend le nom final validé
    if not output_layer.isValid():
        raise Exception("Échec de la création du raster de sortie")

    # Ajouter à la légende QGIS
    QgsProject.instance().addMapLayer(output_layer)
    source1 = raster1.dataProvider().dataSourceUri()
    source2 = raster2.dataProvider().dataSourceUri()
    save_raster_metadata(out_path, "", func, "", source1, source2)
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
    renderer = QgsSingleBandPseudoColorRenderer(output_layer.dataProvider(), 1, shader)
    output_layer.setRenderer(renderer)
    output_layer.triggerRepaint()

    # Ajouter à la légende
    if output_layer not in QgsProject.instance().mapLayers().values():
        QgsProject.instance().addMapLayer(output_layer)

    return output_layer

def save_raster_metadata(raster_path, source_field, function_name, params, source1=None, source2=None):
    folder, filename = os.path.split(raster_path)
    meta_path = os.path.join(folder, f"{filename}.fzy")

    # Préparer les données
    data = {
        "sourcefield": raster_path,
        "function": function_name,
        "params": "",
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
        QMessageBox.warning(self, "Erreur", "Aucune couche sélectionnée")
        return

    raster = QgsProject.instance().mapLayersByName(name)
    if not raster:
        QMessageBox.warning(self, "Erreur", f"Impossible de trouver la couche {name}")
        return

    raster = raster[0]  # on prend le premier trouvé
    src_path = raster.dataProvider().dataSourceUri()
    folder, fname = os.path.split(src_path)
    base, _ = os.path.splitext(fname)
    fzy_path = os.path.join(folder, f"fzy_{base}.fzy")

    if not os.path.exists(fzy_path):
        QMessageBox.information(self, "Info", f"Aucun fichier de métadonnées trouvé pour {base}")
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
            QMessageBox.warning(self, "Erreur", f"Fichier métadonnées non trouvé :\n{fzy_path}")
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

