<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="en_US" sourcelanguage="fr_FR">
<context>
    <name></name>
    <message>
        <source>Préparation Agrégation Raster</source>
        <translation type="vanished">Raster Aggregation Preparation</translation>
    </message>
    <message>
        <source>Nom raster de sortie :</source>
        <translation type="vanished">Output raster name:</translation>
    </message>
    <message>
        <source>Aggregation_Result</source>
        <translation type="vanished">Aggregation_Result</translation>
    </message>
    <message>
        <source>Dossier de sortie :</source>
        <translation type="vanished">Output directory:</translation>
    </message>
    <message>
        <source>Parcourir...</source>
        <translation type="vanished">Browse...</translation>
    </message>
    <message>
        <source>Étendue spatiale</source>
        <translation type="vanished">Spatial extent</translation>
    </message>
    <message>
        <source>Intersection (zone commune)</source>
        <translation type="vanished">Intersection (common area)</translation>
    </message>
    <message>
        <source>Union (couvrir toute la zone)</source>
        <translation type="vanished">Union (cover the entire area)</translation>
    </message>
    <message>
        <source>Méthode de rééchantillonnage :</source>
        <translation type="vanished">Resampling method:</translation>
    </message>
    <message>
        <source>Définir la fonction d&apos;agrégation...</source>
        <translation type="vanished">Define the aggregation function...</translation>
    </message>
    <message>
        <source>Aucune fonction définie</source>
        <translation type="vanished">No defined function</translation>
    </message>
    <message>
        <source>Aide</source>
        <translation type="vanished">Help</translation>
    </message>
    <message>
        <source>Annuler</source>
        <translation type="vanished">Exit</translation>
    </message>
    <message>
        <source>Aide - Agrégation raster</source>
        <translation type="vanished">Help - Raster aggregation</translation>
    </message>
    <message>
        <source>Ce module permet d&apos;agréger deux rasters avec une fonction floue.

Étapes :
1. Choisissez Raster 1 et Raster 2.
   Les deux rasters doivent avoir le même CRS et être projetés. 
   Le raster 1 détermine la résolution du résultat.
2. Définissez l&apos;étendue : intersection ou union.
3. Choisissez le dossier et le nom du fichier de sortie.
4. Lancez l&apos;agrégation.

Le résultat est un raster GeoTIFF enregistré dans le dossier choisi.</source>
        <translation type="vanished">This module allows you to aggregate two rasters using a fuzzy function.

Steps:
1. Select Raster 1 and Raster 2.
   Both rasters must have the same CRS and be projected. 
   Raster 1 determines the resolution of the result.
2. Define the extent: intersection or union.
3. Select the folder and name of the output file.
4. Start the aggregation.

The result is a GeoTIFF raster saved in the selected folder.</translation>
    </message>
    <message>
        <source>Choisir dossier de sortie</source>
        <translation type="vanished">Select output folder</translation>
    </message>
    <message>
        <source>Fonction manquante</source>
        <comment>Veuillez définir une fonction d’agrégation avant de continuer.</comment>
        <translatorcomment>Please define an aggregate function before continuing.</translatorcomment>
        <translation type="vanished">Missing function</translation>
    </message>
    <message>
        <source>Vérification de la combinaison</source>
        <comment>La combinaison semble incohérente :

{details}

Voulez-vous continuer ?</comment>
        <translation type="vanished">Verification of the combination</translation>
    </message>
    <message>
        <source>Erreur</source>
        <comment>Impossible de construire la fonction d’agrégation.

{e}</comment>
        <translation type="vanished">Error</translation>
    </message>
</context>
<context>
    <name>AggregationFunctionDialog</name>
    <message>
        <source>Définir la fonction d&apos;agrégation</source>
        <translation type="vanished">Define the aggregation function</translation>
    </message>
    <message>
        <source>Critère 1</source>
        <translation type="vanished">Criterion 1</translation>
    </message>
    <message>
        <source>Très bon</source>
        <translation type="vanished">Very good</translation>
    </message>
    <message>
        <source>Bon</source>
        <translation type="vanished">Good</translation>
    </message>
    <message>
        <source>Moyen</source>
        <translation type="vanished">Average</translation>
    </message>
    <message>
        <source>Médiocre</source>
        <translation type="vanished">Poor</translation>
    </message>
    <message>
        <source>Très mauvais</source>
        <translation type="vanished">Very poor</translation>
    </message>
    <message>
        <source>Critère 2</source>
        <translation type="vanished">Criterion 2</translation>
    </message>
    <message>
        <source>Critère 3</source>
        <translation type="vanished">Criterion 3</translation>
    </message>
    <message>
        <location filename="../aggregation_function_dialog.py" line="88"/>
        <source>Critère 1 : si le critère &apos;{0}&apos; est Très mauvais et le critère &apos;{1}&apos; est Très bon, le résultat doit être :</source>
        <translation>Criterion 1: if criterion ‘{0}’ is Very Bad and criterion ‘{1}’ is Very Good, the result must be :</translation>
    </message>
    <message>
        <location filename="../aggregation_function_dialog.py" line="91"/>
        <source>Critère 2 : si le critère &apos;{0}&apos; est Moyen et le critère &apos;{1}&apos; est Moyen, le résultat doit être :</source>
        <translation>Criterion 2: if criterion ‘{0}’ is Medium and criterion ‘{1}’ is Medium, the result must be :</translation>
    </message>
    <message>
        <location filename="../aggregation_function_dialog.py" line="94"/>
        <source>Critère 3 : si le critère &apos;{0}&apos; est Moyen et le critère &apos;{1}&apos; est Très bon, le résultat doit être :</source>
        <translation>Criterion 3: if criterion ‘{0}’ is Average and criterion ‘{1}’ is Very good, the result must be :</translation>
    </message>
    <message>
        <location filename="../aggregation_function_dialog.py" line="97"/>
        <source>Critère 4 : si le critère &apos;{0}&apos; est Très bon et le critère &apos;{1}&apos; est Très mauvais, le résultat doit être :</source>
        <translation>Criterion 4: if criterion ‘{0}’ is Very Good and criterion ‘{1}’ is Very Bad, the result must be :</translation>
    </message>
    <message>
        <source>Test de symétrie des réponses</source>
        <translation type="vanished">Response symmetry test</translation>
    </message>
    <message>
        <source>Critère 4</source>
        <translation type="vanished">Criterion 4</translation>
    </message>
    <message>
        <source>Vérifier la symétrie</source>
        <translation type="vanished">Check symmetry</translation>
    </message>
</context>
<context>
    <name>Dialog</name>
    <message>
        <source>Dialog</source>
        <translation type="obsolete">Dialog</translation>
    </message>
</context>
<context>
    <name>FuzzyAggregateDialog</name>
    <message>
        <source>Fuzzy Aggregate</source>
        <translation type="vanished">Fuzzy Aggregate</translation>
    </message>
    <message>
        <source>Couche 1</source>
        <translation type="vanished">Layer 1</translation>
    </message>
    <message>
        <source>Champ flou 1</source>
        <translation type="vanished">Fuzzy field 1</translation>
    </message>
    <message>
        <source>Couche 2</source>
        <translation type="vanished">Layer 2</translation>
    </message>
    <message>
        <source>Champ flou 2</source>
        <translation type="vanished">Fuzzy field 2</translation>
    </message>
    <message>
        <source>Type d’opération spatiale</source>
        <translation type="vanished">Type of spatial operation</translation>
    </message>
    <message>
        <source>Intersection</source>
        <translation type="vanished">Intersection</translation>
    </message>
    <message>
        <source>Union</source>
        <translation type="vanished">Union</translation>
    </message>
    <message>
        <source>Nom de la couche résultat (ajout de _agg à la fin automatique)</source>
        <translation type="vanished">Name of result layer (_agg automatically added at end)</translation>
    </message>
    <message>
        <source>Symbologie de la couche résultante</source>
        <translation type="vanished">Symbology of the resulting layer</translation>
    </message>
    <message>
        <source>Symbole gradué</source>
        <translation type="vanished">Graduated symbol</translation>
    </message>
    <message>
        <source>Rampe de couleur (moyenne ± écart-type)</source>
        <translation type="vanished">Color ramp (mean ± standard deviation)</translation>
    </message>
    <message>
        <source>Sauvegarder comme symbologie par défaut</source>
        <translation type="vanished">Save as default symbology</translation>
    </message>
    <message>
        <source>Définir la fonction</source>
        <translation type="vanished">Define function</translation>
    </message>
    <message>
        <source>Code : </source>
        <translation type="vanished">Code : </translation>
    </message>
    <message>
        <source>Le chemin GPKG doit se terminer par .gpkg</source>
        <translation type="vanished">The GPKG path must end with .gpkg</translation>
    </message>
    <message>
        <source>Le résultat du traitement est inattendu</source>
        <translation type="vanished">Treatment results are unexpected</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="576"/>
        <source>Aucune couche valide</source>
        <translation>No valid layer</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="579"/>
        <source>Aucune couche vectorielle provenant d’un fichier .gpkg ou d’une base PostGIS n’est chargée dans le projet.
Veuillez en ajouter une pour utiliser ce plugin.</source>
        <translation>No vector layer from a .gpkg file is loaded in the project.
Please add one to use this plugin.</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="784"/>
        <source>La sortie n&apos;est pas une couche vectorielle valide</source>
        <translation>Output is not a valid vector layer</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="822"/>
        <source>Type de sortie non supporté (uniquement GPKG ou PostGIS)</source>
        <translation>Output type not supported (only GPKG or PostGIS)</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="832"/>
        <source>Aucune fonction sélectionnée</source>
        <translation>No function selected</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="833"/>
        <source>Veuillez d&apos;abord sélectionner une fonction d&apos;agrégation floue.</source>
        <translation>Please select a fuzzy aggregation function first.</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="854"/>
        <location filename="../fuzzyaggregate_dialog.py" line="952"/>
        <location filename="../fuzzyaggregate_dialog.py" line="969"/>
        <location filename="../fuzzyaggregate_dialog.py" line="973"/>
        <location filename="../fuzzyaggregate_dialog.py" line="1180"/>
        <location filename="../fuzzyaggregate_dialog.py" line="1684"/>
        <location filename="../fuzzyaggregate_dialog.py" line="1723"/>
        <source>Erreur</source>
        <translation>Error</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="856"/>
        <source>Pour l&apos;instant le plugin ne peut traiter que des couches de même type (deux GPKG ou deux PostGIS).</source>
        <translation>For now, the plugin can only process layers of the same type (two GPKG or two PostGIS).</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="969"/>
        <source>Veuillez sélectionner une opération.</source>
        <translation>Please select an operation.</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="973"/>
        <source>Tous les champs doivent être remplis.</source>
        <translation>All fields must be completed.</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1047"/>
        <location filename="../fuzzyaggregate_dialog.py" line="1251"/>
        <source>0 – 0.125 (mauvais)</source>
        <translation>0 – 0.125 (very poor)</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1048"/>
        <location filename="../fuzzyaggregate_dialog.py" line="1252"/>
        <source>0.125 – 0.375 (médiocre)</source>
        <translation>0.125 – 0.375 (poor)</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1049"/>
        <location filename="../fuzzyaggregate_dialog.py" line="1253"/>
        <source>0.375 – 0.625 (moyen)</source>
        <translation>0.375 – 0.625 (average)</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1050"/>
        <location filename="../fuzzyaggregate_dialog.py" line="1254"/>
        <source>0.625 – 0.875 (bon)</source>
        <translation>0.625 – 0.875 (good)</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1051"/>
        <location filename="../fuzzyaggregate_dialog.py" line="1255"/>
        <source>0.875 – 1.0 (très bon)</source>
        <translation>0.875 – 1.0 (very good)</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1107"/>
        <location filename="../fuzzyaggregate_dialog.py" line="1304"/>
        <source>Légende Above/Below</source>
        <translation>Above/Below Legend</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1180"/>
        <source>Champs introuvables dans la couche résultante.</source>
        <translation>Fields not found in the resulting layer.</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1355"/>
        <source>Succès</source>
        <translation>Success</translation>
    </message>
    <message>
        <source>La table metafuzzy n’a pas pu être chargée.</source>
        <translation type="vanished">The metafuzzy table could not be loaded.</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1684"/>
        <source>Aucune couche sélectionnée.</source>
        <translation>No layer selected.</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1689"/>
        <location filename="../fuzzyaggregate_dialog.py" line="1731"/>
        <source>Info</source>
        <translation>Info</translation>
    </message>
    <message>
        <source>Aucune table &apos;metafuzzy&apos; trouvée dans le GeoPackage.</source>
        <translation type="vanished">No ‘metafuzzy’ table found in GeoPackage.</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1740"/>
        <source>Historique des transformations</source>
        <translation>Transformation history</translation>
    </message>
    <message>
        <source>Ce choix n&apos;est peut-être pas logique (ex. : deux critères faibles → excellent résultat)</source>
        <translation type="obsolete">This choice may not be logical (e.g.: two weak criteria → excellent result).</translation>
    </message>
    <message>
        <source>Aucune couche GeoPackage</source>
        <translation type="vanished">No GeoPackage layer</translation>
    </message>
    <message>
        <source>Aucune couche vectorielle provenant d’un fichier .gpkg n’est chargée dans le projet.
Veuillez en ajouter une pour utiliser ce plugin.</source>
        <translation type="vanished">No vector layer from a .gpkg file is loaded in the project.
Please add one to use this plugin.</translation>
    </message>
    <message>
        <source>Voir l&apos;historique des transformations</source>
        <translation type="vanished">View transformation history</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="922"/>
        <source>Vérification de la combinaison</source>
        <translation>Verification of the combination</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="923"/>
        <source>La combinaison semble incohérente :

{0}

Voulez-vous procéder quand même ?</source>
        <translation>The combination seems inconsistent:

{0}

Do you want to proceed anyway?</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="952"/>
        <source>La fonction d’agrégation n’a pas pu être générée.</source>
        <translation>The aggregation function could not be generated.</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1355"/>
        <source>Couche &apos;{output_name}&apos; créée avec succès.</source>
        <translation>Layer ‘{output_name}’ successfully created.</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1518"/>
        <source>Impossible de charger la table &apos;metafuzzy&apos; dans QGIS</source>
        <comment>FuzzyPlugin</comment>
        <translation>Unable to load the ‘metafuzzy’ table in QGIS</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1524"/>
        <source>Source inconnue (ni GPKG ni PostGIS)</source>
        <comment>FuzzyPlugin</comment>
        <translation>Unknown source (neither GPKG nor PostGIS)</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1689"/>
        <source>1393 Impossible de créer ou charger la table &apos;metafuzzy&apos;.</source>
        <translation>1393 Unable to create or load the ‘metafuzzy’ table.</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1724"/>
        <source>Format de source non reconnu (ni GPKG ni PostGIS).</source>
        <translation>Unrecognized source format (neither GPKG nor PostGIS).</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1732"/>
        <source>Aucune table &apos;metafuzzy&apos; trouvée.</source>
        <translation>No ‘metafuzzy’ table found.</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1870"/>
        <source>Règle 1 violée : R3 (A=0,5 ; B=1) doit être &gt;= max(R1, R2).</source>
        <translation>Rule 1 violated: R3 (A=0.5; B=1) must be &gt;= max(R1, R2).</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="1874"/>
        <source>Règle 2 violée : R3 (A=0,5 ; B=1) doit être &gt;= 0,5.</source>
        <translation></translation>
    </message>
</context>
<context>
    <name>FuzzyAttributes</name>
    <message>
        <location filename="../FuzzyAttributes_plugin.py" line="143"/>
        <source>Agrégation floue</source>
        <translation>Fuzzy aggregation</translation>
    </message>
    <message>
        <location filename="../FuzzyAttributes_plugin.py" line="148"/>
        <source>Texte → Flou</source>
        <translation>Text → Fuzzy</translation>
    </message>
    <message>
        <location filename="../FuzzyAttributes_plugin.py" line="158"/>
        <source>FuzzyRaster</source>
        <translation>FuzzyRaster</translation>
    </message>
    <message>
        <location filename="../FuzzyAttributes_plugin.py" line="163"/>
        <source>Agrégation Raster</source>
        <translation>Raster aggregation</translation>
    </message>
    <message>
        <location filename="../FuzzyAttributes_plugin.py" line="168"/>
        <source>Classes → Flou</source>
        <translation>Classes → Fuzzy</translation>
    </message>
    <message>
        <location filename="../FuzzyAttributes_plugin.py" line="138"/>
        <location filename="../FuzzyAttributes_plugin.py" line="217"/>
        <source>Fuzzy Plugin</source>
        <translation>Fuzzy Plugin</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="2083"/>
        <source>0 – 0.125 (mauvais)</source>
        <translation>0 – 0.125 (very poor)</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="2084"/>
        <source>0.125 – 0.375 (médiocre)</source>
        <translation>0.125 – 0.375 (poor)</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="2085"/>
        <source>0.375 – 0.625 (moyen)</source>
        <translation>0.375 – 0.625 (average)</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="2086"/>
        <source>0.625 – 0.875 (bon)</source>
        <translation>0.625 – 0.875 (good)</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregate_dialog.py" line="2087"/>
        <source>0.875 – 1.0 (très bon)</source>
        <translation>0.875 – 1.0 (very good)</translation>
    </message>
</context>
<context>
    <name>FuzzyAttributesDialog</name>
    <message>
        <source>Transformation floue d&apos;attributs</source>
        <translation type="vanished">Fuzzy attribute transformation</translation>
    </message>
    <message>
        <location filename="../fuzzyraster.ui" line="24"/>
        <source>Statistiques</source>
        <translation>Statistics</translation>
    </message>
    <message>
        <source>Afficher les statistiques du champ</source>
        <translation type="vanished">Display field statistics</translation>
    </message>
    <message>
        <location filename="../fuzzyraster.ui" line="14"/>
        <source>Transformation floue d&apos;un raster</source>
        <translation>Fuzzy transformation of a raster</translation>
    </message>
    <message>
        <location filename="../fuzzyraster.ui" line="27"/>
        <source>Afficher les statistiques du raster sélectionné</source>
        <translation>Display statistics for the selected raster</translation>
    </message>
    <message>
        <location filename="../fuzzyraster.ui" line="58"/>
        <source>Paramètres séparés par des virgules</source>
        <translation>Comma-separated parameters</translation>
    </message>
    <message>
        <location filename="../fuzzyraster.ui" line="65"/>
        <source>Afficher l’aide sur les fonctions floues</source>
        <translation>View help on fuzzy functions</translation>
    </message>
    <message>
        <location filename="../fuzzyraster.ui" line="68"/>
        <source>?</source>
        <translation>?</translation>
    </message>
    <message>
        <location filename="../fuzzyraster.ui" line="80"/>
        <source>Exemple : </source>
        <translation>Example : </translation>
    </message>
    <message>
        <location filename="../fuzzyraster.ui" line="87"/>
        <source>Voir l&apos;historique des transformations</source>
        <translation>View transformation history</translation>
    </message>
    <message>
        <source>Aucune couche GeoPackage</source>
        <translation type="vanished">No GeoPackage layer</translation>
    </message>
    <message>
        <source>Aucune couche vectorielle provenant d’un fichier .gpkg n’est chargée dans le projet.
Veuillez en ajouter une pour utiliser ce plugin.</source>
        <translation type="vanished">No vector layer from a .gpkg file is loaded in the project.
Please add one to use this plugin.</translation>
    </message>
    <message>
        <source>Seules les couches provenant de fichiers GeoPackage (.gpkg) sont affichées.</source>
        <translation type="vanished">Only layers from GeoPackage (.gpkg) files are displayed.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="58"/>
        <source>Les couches provenant de fichiers GeoPackage (.gpkg) ou de bases PostGIS sont affichées.</source>
        <translation>Layers from GeoPackage (.gpkg) files or PostGIS databases are displayed.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="70"/>
        <location filename="../fuzzyattributes_dialog.py" line="204"/>
        <source>linéaire croissante</source>
        <translation>increasing linear</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="71"/>
        <location filename="../fuzzyattributes_dialog.py" line="205"/>
        <source>linéaire décroissante</source>
        <translation>linear decreasing</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="72"/>
        <location filename="../fuzzyattributes_dialog.py" line="206"/>
        <source>triangulaire</source>
        <translation>triangular</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="73"/>
        <location filename="../fuzzyattributes_dialog.py" line="207"/>
        <source>trapézoïdale</source>
        <translation>trapezoidal</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="74"/>
        <location filename="../fuzzyattributes_dialog.py" line="208"/>
        <source>sigmoïde croissante (S)</source>
        <translation>increasing sigmoid (S)</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="75"/>
        <location filename="../fuzzyattributes_dialog.py" line="209"/>
        <source>sigmoïde décroissante (Z)</source>
        <translation>decreasing sigmoid (Z)</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="76"/>
        <location filename="../fuzzyattributes_dialog.py" line="210"/>
        <source>gaussienne</source>
        <translation>Gaussian</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="157"/>
        <source>Aucune couche trouvée</source>
        <translation>No layer found</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="160"/>
        <source>Aucune couche GeoPackage (.gpkg) ou PostGIS n’est chargée dans le projet.
Veuillez en ajouter une pour utiliser ce plugin.</source>
        <translation>No GeoPackage (.gpkg) or PostGIS layer is loaded in the project.
Please add one to use this plugin.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="171"/>
        <source>Les couches provenant de fichiers GeoPackage (.gpkg) ou de bases PostGIS sont affichées (avec schéma pour PostGIS).</source>
        <translation>Layers from GeoPackage (.gpkg) files or PostGIS databases are displayed (with schema for PostGIS).</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="229"/>
        <source>&lt;b&gt;Types de fonctions floues :&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;b&gt;• Linéaire croissante :&lt;/b&gt; augmente de 0 à 1 entre a et b&lt;br&gt;&lt;b&gt;• Linéaire décroissante :&lt;/b&gt; diminue de 1 à 0 entre a et b&lt;br&gt;&lt;b&gt;• Triangulaire :&lt;/b&gt; forme un pic à b entre a et c&lt;br&gt;&lt;b&gt;• Trapézoïdale :&lt;/b&gt; forme un plateau entre b et c&lt;br&gt;&lt;b&gt;• Sigmoïde (S) :&lt;/b&gt; transition douce croissante centrée en b&lt;br&gt;&lt;b&gt;• Sigmoïde (Z) :&lt;/b&gt; transition douce décroissante centrée en b&lt;br&gt;&lt;b&gt;• Gaussienne :&lt;/b&gt; courbe en cloche centrée en c avec largeur sigma&lt;br&gt;</source>
        <translation>&lt;b&gt;Types of fuzzy functions :&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;b&gt;• Linear increasing :&lt;/b&gt; increases from 0 to 1 between a and b&lt;br&gt;&lt;b&gt;• Linear decreasing : &lt;/b&gt; decreases from 1 to 0 between a and b&lt;br&gt;&lt;b&gt;• Triangular :&lt;/b&gt; forms a peak at b between a and c&lt;br&gt;&lt;b&gt;• Trapezoidal :&lt;/b&gt; orms a plateau between b and c&lt;br&gt;&lt;b&gt;• Sigmoid (S) :&lt;/b&gt; smooth increasing transition centered at b&lt;br&gt;&lt;b&gt;• Sigmoid (Z) :&lt;/b&gt; smooth decreasing transition centered at b&lt;br&gt;&lt;b&gt;• Gaussian :&lt;/b&gt; bell curve centered at c with sigma width&lt;br&gt;</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="230"/>
        <source>Aide sur les fonctions floues</source>
        <translation>Help with fuzzy functions</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="237"/>
        <location filename="../fuzzyattributes_dialog.py" line="367"/>
        <location filename="../fuzzyattributes_dialog.py" line="450"/>
        <location filename="../fuzzyattributes_dialog.py" line="489"/>
        <location filename="../fuzzyattributes_dialog.py" line="576"/>
        <location filename="../fuzzyattributes_dialog.py" line="588"/>
        <location filename="../fuzzyattributes_dialog.py" line="595"/>
        <location filename="../fuzzyattributes_dialog.py" line="686"/>
        <location filename="../fuzzyattributes_dialog.py" line="692"/>
        <location filename="../fuzzyattributes_dialog.py" line="697"/>
        <source>Erreur</source>
        <translation>Error</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="237"/>
        <source>Paramètres invalides. Utilisez des nombres séparés par des virgules.</source>
        <translation>Invalid parameters. Use numbers separated by commas.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="369"/>
        <location filename="../fuzzyattributes_dialog.py" line="490"/>
        <source>Format de source non reconnu (ni GPKG ni PostGIS).</source>
        <translation>Unrecognized source format (neither GPKG nor PostGIS).</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="382"/>
        <location filename="../fuzzyattributes_dialog.py" line="455"/>
        <source>Impossible de créer ou charger la table &apos;metafuzzy&apos;.</source>
        <translation>Unable to create or load the ‘metafuzzy’ table.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="498"/>
        <source>Aucune table &apos;metafuzzy&apos; trouvée.</source>
        <translation>No ‘metafuzzy’ table found.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="557"/>
        <source>Paramètres invalides</source>
        <translation>Invalid settings</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="568"/>
        <source>Champ existant</source>
        <translation>Existing field</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="569"/>
        <source>Le champ &apos;{new_field_name}&apos; existe déjà. Voulez-vous le remplacer ?</source>
        <translation>The field ‘{new_field_name}’ already exists. Do you want to replace it?</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="576"/>
        <source>Impossible de supprimer le champ existant.</source>
        <translation>Unable to delete the existing field.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="750"/>
        <source>Cette fonction nécessite exactement 2 paramètres.</source>
        <translation>This function requires exactly 2 parameters.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="753"/>
        <source>Les deux paramètres ne doivent pas être égaux.</source>
        <translation>The two parameters must not be equal.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="756"/>
        <source>La fonction triangulaire nécessite exactement 3 paramètres.</source>
        <translation>The triangular function requires exactly 3 parameters.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="759"/>
        <source>Les paramètres doivent être dans l&apos;ordre a &lt; b &lt; c.</source>
        <translation>The parameters must be in the order a &lt; b &lt; c.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="762"/>
        <source>La fonction trapézoïdale nécessite exactement 4 paramètres.</source>
        <translation>The trapezoidal function requires exactly 4 parameters.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="765"/>
        <source>Les paramètres doivent être dans l&apos;ordre a &lt; b &lt;= c &lt; d.</source>
        <translation>The parameters must be in the order a &lt; b &lt;= c &lt; d.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="768"/>
        <source>La fonction gaussienne nécessite exactement 2 paramètres (c, sigma).</source>
        <translation>The Gaussian function requires exactly 2 parameters (c, sigma).</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="771"/>
        <source>Le paramètre sigma doit être strictement positif.</source>
        <translation>The sigma parameter must be strictly positive.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="773"/>
        <source>Type de fonction floue inconnu.</source>
        <translation>Unknown fuzzy function type.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="775"/>
        <source>Erreur lors de la validation des paramètres : </source>
        <translation>Error validating parameters: </translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="844"/>
        <source>Champs de la couche GeoPackage sélectionnée</source>
        <translation>Fields of the selected GeoPackage layer</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="846"/>
        <source>Champs de la couche PostGIS sélectionnée</source>
        <translation>Fields of the selected PostGIS layer</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="848"/>
        <source>Champs de la couche vectorielle sélectionnée</source>
        <translation>Fields of the selected vector layer</translation>
    </message>
    <message>
        <source>La table metafuzzy n’a pas pu être chargée.</source>
        <translation type="vanished">The metafuzzy table could not be loaded.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="450"/>
        <source>Aucune couche sélectionnée.</source>
        <translation>No layer selected.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="382"/>
        <location filename="../fuzzyattributes_dialog.py" line="455"/>
        <location filename="../fuzzyattributes_dialog.py" line="497"/>
        <source>Info</source>
        <translation>Info</translation>
    </message>
    <message>
        <source>Aucune table &apos;metafuzzy&apos; trouvée dans le GeoPackage.</source>
        <translation type="vanished">No ‘metafuzzy’ table found in GeoPackage.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="505"/>
        <source>Historique des transformations</source>
        <translation>Transformation history</translation>
    </message>
    <message>
        <source>Les métadonnées ne peuvent être stockées que dans un fichier .gpkg.</source>
        <translation type="vanished">Metadata can only be stored in a .gpkg file.</translation>
    </message>
    <message>
        <source>Impossible de créer la table metafuzzy dans le GeoPackage.</source>
        <translation type="vanished">Unable to create metafuzzy table in GeoPackage.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="588"/>
        <source>Impossible d&apos;ajouter le champ.</source>
        <translation>Unable to add field.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="595"/>
        <source>Problème avec les champs.</source>
        <translation>Problem with the fields.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="672"/>
        <source>Succès</source>
        <translation>Success</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="687"/>
        <source>Impossible de trouver la couche &apos;{}&apos;</source>
        <translation>Unable to find ‘{}’ layer</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="692"/>
        <source>Aucun champ sélectionné.</source>
        <translation>No fields selected.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="697"/>
        <source>Le champ est introuvable.</source>
        <translation>The field cannot be found.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="710"/>
        <source>Aucune donnée</source>
        <translation>No data available</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="712"/>
        <source>Aucune valeur numérique disponible pour ce champ.</source>
        <translation>No numeric value available for this field.</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="729"/>
        <source>Statistiques pour le champ &apos;{field_name}&apos; :

Nombre de valeurs : {count}
Min : {min_val}
Max : {max_val}
Moyenne : {mean_val:.2f}
Médiane : {median_val:.2f}</source>
        <translation>Statistics for field &apos;{field_name}&apos; :

Number of values : {count}
Min : {min_val}
Max : {max_val}
Mean : {mean_val:.2f}
Median : {median_val:.2f}</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="738"/>
        <source>Statistiques du champ</source>
        <translation>Field statistics</translation>
    </message>
    <message>
        <location filename="../fuzzyattributes_dialog.py" line="673"/>
        <source>Transformation floue ajoutée dans &apos;{}&apos;</source>
        <translation>Fuzzy transformation added in ‘{}’</translation>
    </message>
</context>
<context>
    <name>FuzzyClassDialog</name>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="61"/>
        <source>Enregistrer en CSV</source>
        <translation>Save as CSV</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="62"/>
        <source>Enregistre le mapping actuel dans un fichier CSV</source>
        <translation>Saves the current mapping to a CSV file</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="66"/>
        <source>Charger depuis CSV</source>
        <translation>Load from CSV</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="67"/>
        <source>Charge un mapping depuis un fichier CSV</source>
        <translation>Load a mapping from a CSV file</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="97"/>
        <source>Aucune couche sélectionnée !</source>
        <translation>No layer selected!</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="119"/>
        <location filename="../fuzzyclass_dialog.py" line="130"/>
        <location filename="../fuzzyclass_dialog.py" line="156"/>
        <location filename="../fuzzyclass_dialog.py" line="201"/>
        <location filename="../fuzzyclass_dialog.py" line="207"/>
        <location filename="../fuzzyclass_dialog.py" line="275"/>
        <location filename="../fuzzyclass_dialog.py" line="338"/>
        <location filename="../fuzzyclass_dialog.py" line="380"/>
        <location filename="../fuzzyclass_dialog.py" line="391"/>
        <location filename="../fuzzyclass_dialog.py" line="430"/>
        <source>Erreur</source>
        <translation>Error</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="119"/>
        <source>Aucune couche sélectionnée dans la liste.</source>
        <translation>No layer selected in the list.</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="130"/>
        <location filename="../fuzzyclass_dialog.py" line="391"/>
        <source>La couche sélectionnée n&apos;est pas un raster valide.</source>
        <translation>The selected layer is not a valid raster.</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="156"/>
        <source>Impossible de récupérer les valeurs raster : {e}</source>
        <translation>Unable to retrieve raster values: {e}</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="166"/>
        <source>{len(unique_values)} classes raster uniques ajoutées depuis {layer.name()}.</source>
        <translation>{len(unique_values)} unique raster classes added since {layer.name()}.</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="172"/>
        <source>Sélection vide</source>
        <translation>Empty selection</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="172"/>
        <source>Sélectionnez au moins une ligne dans la table.</source>
        <translation>Select at least one row in the table.</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="178"/>
        <source>Valeur fuzzy</source>
        <translation>Fuzzy value</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="179"/>
        <source>Entrez une valeur fuzzy entre 0 et 1 :</source>
        <translation>Enter a fuzzy value between 0 and 1:</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="192"/>
        <source>Valeur fuzzy {value} appliquée à {sum([r.rowCount() for r in selected_ranges])} lignes.</source>
        <translation>Fuzzy value {value} applied to {sum([r.rowCount() for r in selected_ranges])} rows.</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="201"/>
        <source>Aucune couche sélectionnée.</source>
        <translation>No layer selected.</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="207"/>
        <source>Raster invalide.</source>
        <translation>Invalid raster.</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="243"/>
        <source>Le fichier {base_name}.tif existe déjà dans {out_dir}.</source>
        <translation>The file {base_name}.tif already exists in {out_dir}.</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="244"/>
        <source>Voulez-vous l&apos;écraser ?</source>
        <translation>Do you want to delete it?</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="275"/>
        <source>Échec de la création du raster de sortie</source>
        <translation>Failure to create output raster</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="299"/>
        <location filename="../fuzzyclass_dialog.py" line="427"/>
        <source>Succès</source>
        <translation>Success</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="299"/>
        <source>Raster fuzzy créé : {os.path.basename(out_path)}</source>
        <translation>Fuzzy raster created: {os.path.basename(out_path)}</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="309"/>
        <source>Table vide</source>
        <translation>Empty table</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="309"/>
        <source>Aucune donnée à sauvegarder.</source>
        <translation>No data to save.</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="313"/>
        <source>Enregistrer la table en CSV</source>
        <translation>Save table as CSV</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="338"/>
        <source>Impossible de sauvegarder en CSV : {e}</source>
        <translation>Unable to save as CSV: {e}</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="361"/>
        <source>Charger une table CSV</source>
        <translation>Load a CSV table</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="373"/>
        <source>Attention</source>
        <translation>Caution</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="373"/>
        <source>Le fichier CSV est vide.</source>
        <translation>The CSV file is empty.</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="382"/>
        <source>Le CSV doit contenir les colonnes &apos;Classe raster&apos; et &apos;Fuzzy&apos;.</source>
        <translation>The CSV must contain the columns  &apos;Classe raster&apos; and &apos;Fuzzy&apos;.</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="427"/>
        <source>Table chargée depuis {path}</source>
        <translation>Table loaded from {path}</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.py" line="430"/>
        <source>Impossible de charger le CSV : {e}</source>
        <translation>Unable to load CSV: {e}</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.ui" line="14"/>
        <source>Fuzzy Classes Mapping</source>
        <translation>Fuzzy Classes Mapping</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.ui" line="25"/>
        <source>Charger valeurs uniques</source>
        <translation>Load unique values</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.ui" line="32"/>
        <source>Affecter valeur fuzzy aux lignes sélectionnées</source>
        <translation>Assign fuzzy value to selected rows</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.ui" line="47"/>
        <source>Reclasser le raster</source>
        <translation>Reclassify the raster</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.ui" line="54"/>
        <source>Fermer</source>
        <translation>Close</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.ui" line="63"/>
        <source>color: gray; font-style: italic;</source>
        <translation>color: gray; font-style: italic;</translation>
    </message>
    <message>
        <location filename="../fuzzyclass_dialog.ui" line="66"/>
        <source>Astuce : associez chaque valeur texte du champ sélectionné à une valeur floue comprise entre 0 et 1.</source>
        <translation>Associate each class value with a fuzzy value between 0 and 1.</translation>
    </message>
</context>
<context>
    <name>FuzzyRasterDialog</name>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="121"/>
        <source>Statistiques du raster</source>
        <translation>Raster statistics</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="167"/>
        <source>&lt;b&gt;Types de fonctions floues :&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;b&gt;• Linéaire croissante :&lt;/b&gt; augmente de 0 à 1 entre a et b&lt;br&gt;&lt;b&gt;• Linéaire décroissante :&lt;/b&gt; diminue de 1 à 0 entre a et b&lt;br&gt;&lt;b&gt;• Triangulaire :&lt;/b&gt; forme un pic à b entre a et c&lt;br&gt;&lt;b&gt;• Trapézoïdale :&lt;/b&gt; forme un plateau entre b et c&lt;br&gt;&lt;b&gt;• Sigmoïde (S) :&lt;/b&gt; transition douce croissante centrée en b&lt;br&gt;&lt;b&gt;• Sigmoïde (Z) :&lt;/b&gt; transition douce décroissante centrée en b&lt;br&gt;&lt;b&gt;• Gaussienne :&lt;/b&gt; courbe en cloche centrée en c avec largeur sigma&lt;br&gt;</source>
        <translation>&lt;b&gt;Types of fuzzy functions :&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;b&gt;• Linear increasing :&lt;/b&gt; increases from 0 to 1 between a and b&lt;br&gt;&lt;b&gt;• Linear decreasing : &lt;/b&gt; decreases from 1 to 0 between a and b&lt;br&gt;&lt;b&gt;• Triangular :&lt;/b&gt; forms a peak at b between a and c&lt;br&gt;&lt;b&gt;• Trapezoidal :&lt;/b&gt; orms a plateau between b and c&lt;br&gt;&lt;b&gt;• Sigmoid (S) :&lt;/b&gt; smooth increasing transition centered at b&lt;br&gt;&lt;b&gt;• Sigmoid (Z) :&lt;/b&gt; smooth decreasing transition centered at b&lt;br&gt;&lt;b&gt;• Gaussian :&lt;/b&gt; bell curve centered at c with sigma width&lt;br&gt;</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="168"/>
        <source>Aide sur les fonctions floues</source>
        <translation>Help with fuzzy functions</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="105"/>
        <location filename="../fuzzyraster_dialog.py" line="110"/>
        <location filename="../fuzzyraster_dialog.py" line="115"/>
        <location filename="../fuzzyraster_dialog.py" line="175"/>
        <location filename="../fuzzyraster_dialog.py" line="216"/>
        <location filename="../fuzzyraster_dialog.py" line="238"/>
        <location filename="../fuzzyraster_dialog.py" line="245"/>
        <location filename="../fuzzyraster_dialog.py" line="285"/>
        <location filename="../fuzzyraster_dialog.py" line="330"/>
        <location filename="../fuzzyraster_dialog.py" line="429"/>
        <location filename="../fuzzyraster_dialog.py" line="531"/>
        <location filename="../fuzzyraster_dialog.py" line="536"/>
        <source>Erreur</source>
        <translation>Error</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="73"/>
        <source>linéaire croissante</source>
        <translation>increasing linear</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="74"/>
        <source>linéaire décroissante</source>
        <translation>linear decreasing</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="75"/>
        <source>triangulaire</source>
        <translation>triangular</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="76"/>
        <source>trapézoïdale</source>
        <translation>trapezoidal</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="77"/>
        <source>sigmoïde croissante (S)</source>
        <translation>increasing sigmoid (S)</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="78"/>
        <source>sigmoïde décroissante (Z)</source>
        <translation>decreasing sigmoid (Z)</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="79"/>
        <source>gaussienne</source>
        <translation>Gaussian</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="105"/>
        <location filename="../fuzzyraster_dialog.py" line="531"/>
        <source>Aucune couche sélectionnée</source>
        <translation>No layer selected</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="110"/>
        <location filename="../fuzzyraster_dialog.py" line="536"/>
        <source>Impossible de trouver la couche {name}</source>
        <translation>Unable to find {name} layer</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="115"/>
        <source>La couche {name} n’est pas un raster</source>
        <translation>The {name} layer is not a raster</translation>
    </message>
    <message>
        <source>Moyenne : {stats.mean}
</source>
        <translation type="vanished">Mean : {stats.mean}\n</translation>
    </message>
    <message>
        <source>Écart-type : {stats.stdDev}</source>
        <translation type="vanished">Standard deviation : {stats.stdDev}</translation>
    </message>
    <message numerus="yes">
        <source>linear_incExemple : a=200, b=1500</source>
        <comment>linear_decExemple : a=1500, b=200</comment>
        <translation type="vanished">
            <numerusform>linear_incExemple : a=200, b=1500</numerusform>
            <numerusform></numerusform>
        </translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="175"/>
        <location filename="../fuzzyraster_dialog.py" line="429"/>
        <source>Paramètres invalides. Utilisez des nombres séparés par des virgules.</source>
        <translation>Invalid parameters. Use numbers separated by commas.</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="216"/>
        <source>Aucun raster sélectionné</source>
        <translation>No raster selected</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="230"/>
        <location filename="../fuzzyraster_dialog.py" line="245"/>
        <source>Paramètres invalides</source>
        <translation>Invalid settings</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="238"/>
        <source>La couche sélectionnée n’est pas un raster</source>
        <translation>The selected layer is not a raster</translation>
    </message>
    <message>
        <source>Fichier existant</source>
        <comment>Le fichier {out_path} existe déjà.

Voulez-vous l’écraser ?</comment>
        <translatorcomment>The file {out_path} already exists. Do you want to overwrite it?</translatorcomment>
        <translation type="vanished">Existing file</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="258"/>
        <source>Fichier existant</source>
        <translation>Existing file</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="259"/>
        <source>Le fichier {out_path} existe déjà.

Voulez-vous l’écraser ?</source>
        <translation>The file {out_path} already exists.

Do you want to overwrite it?</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="267"/>
        <source>Choisir un nom de fichier</source>
        <translation>Choosing a file name</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="272"/>
        <source>Annulé</source>
        <translation>Cancelled</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="272"/>
        <source>Opération annulée par l’utilisateur.</source>
        <translation>Operation canceled by the user.</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="287"/>
        <source>Impossible d’écraser {out_path}
{e}</source>
        <translation>Unable to overwrite {out_path}
{e}</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="330"/>
        <source>Impossible de charger le raster : {out_path}</source>
        <translation>Unable to load raster: {out_path}</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="334"/>
        <source>Succès</source>
        <translation>Success</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="335"/>
        <source>Transformation floue créée dans fzy_&apos;{}&apos;</source>
        <translation>Fuzzy transformation created in fzy_&apos;{}&apos;</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="447"/>
        <source>Cette fonction nécessite exactement 2 paramètres.</source>
        <translation>This function requires exactly 2 parameters.</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="450"/>
        <source>Les deux paramètres ne doivent pas être égaux.</source>
        <translation>The two parameters must not be equal.</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="453"/>
        <source>La fonction triangulaire nécessite exactement 3 paramètres.</source>
        <translation>The triangular function requires exactly 3 parameters.</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="456"/>
        <source>Les paramètres doivent être dans l&apos;ordre a &lt; b &lt; c.</source>
        <translation>The parameters must be in the order a &lt; b &lt; c.</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="459"/>
        <source>La fonction trapézoïdale nécessite exactement 4 paramètres.</source>
        <translation>The trapezoidal function requires exactly 4 parameters.</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="462"/>
        <source>Les paramètres doivent être dans l&apos;ordre a &lt; b &lt;= c &lt; d.</source>
        <translation>The parameters must be in the order a &lt; b &lt;= c &lt; d.</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="465"/>
        <source>La fonction gaussienne nécessite exactement 2 paramètres (c, sigma).</source>
        <translation>The Gaussian function requires exactly 2 parameters (c, sigma).</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="468"/>
        <source>Le paramètre sigma doit être strictement positif.</source>
        <translation>The sigma parameter must be strictly positive.</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="470"/>
        <source>Type de fonction floue inconnu.</source>
        <translation>Unknown fuzzy function type.</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="472"/>
        <source>Erreur lors de la validation des paramètres : </source>
        <translation>Error validating parameters: </translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="546"/>
        <source>Info</source>
        <translation>Info</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="546"/>
        <source>Aucun fichier de métadonnées trouvé pour {base}</source>
        <translation>No metadata file found for {base}</translation>
    </message>
    <message>
        <source>Info</source>
        <comment>Aucun fichier de métadonnées trouvé pour {base}</comment>
        <translatorcomment>No metadata file found for {base}</translatorcomment>
        <translation type="vanished">Info</translation>
    </message>
</context>
<context>
    <name>FuzzyTextDialog</name>
    <message>
        <location filename="../fuzzytext_dialog.py" line="67"/>
        <location filename="../fuzzytext_dialog.py" line="563"/>
        <source>Enregistrer la table</source>
        <translation>Save the table</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="70"/>
        <source>Enregistrer en CSV</source>
        <translation>Save as CSV</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="74"/>
        <source>Enregistrer dans la base de données</source>
        <translation>Save to database</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="84"/>
        <source>Charger une table</source>
        <translation>Load a table</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="87"/>
        <location filename="../fuzzytext_dialog.py" line="589"/>
        <source>Charger depuis CSV</source>
        <translation>Load from CSV</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="91"/>
        <location filename="../fuzzytext_dialog.py" line="593"/>
        <source>Charger depuis la base de données</source>
        <translation>Load from database</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="181"/>
        <source>Aucune couche trouvée</source>
        <translation>No layer found</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="184"/>
        <source>Aucune couche GeoPackage (.gpkg) ou PostGIS n’est chargée dans le projet.
Veuillez en ajouter une pour utiliser ce plugin.</source>
        <translation>No vector layer from a .gpkg file is loaded in the project.
Please add one to use this plugin.</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="299"/>
        <source>Veuillez sélectionner une couche et un champ texte.</source>
        <translation>Please select a layer and a text field.</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="308"/>
        <source>La couche sélectionnée n&apos;est pas une couche vectorielle valide.</source>
        <translation>The selected layer is not a valid vector layer.</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="346"/>
        <source>Impossible de récupérer les valeurs uniques : {e}</source>
        <translation>Unable to retrieve unique values: {e}</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="361"/>
        <source>{len(unique_values)} valeurs uniques ajoutées depuis {layer.name()} ({field_name}).</source>
        <translation>{len(unique_values)} unique values added since {layer.name()} ({field_name}).</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="367"/>
        <source>Sélection vide</source>
        <translation>Empty selection</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="367"/>
        <source>Sélectionnez au moins une ligne dans la table.</source>
        <translation>Select at least one row in the table.</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="373"/>
        <source>Valeur fuzzy</source>
        <translation>Fuzzy value</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="374"/>
        <source>Entrez une valeur fuzzy entre 0 et 1 :</source>
        <translation>Enter a fuzzy value between 0 and 1:</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="389"/>
        <source>Valeur fuzzy {value} appliquée à {total_rows} lignes.</source>
        <translation>Fuzzy value {value} applied to {total_rows} rows.</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="519"/>
        <source>Charger table de correspondance</source>
        <translation>Load correspondence table</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="532"/>
        <source>Erreur de lecture</source>
        <translation>Reading error</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="534"/>
        <source>Impossible de lire le fichier : {e}</source>
        <translation>Unable to read the file: {e}</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="542"/>
        <source>Incohérence détectée</source>
        <translation>Inconsistency detected</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="546"/>
        <source>Le fichier correspond au champ &apos;{data.get(&apos;field&apos;)}&apos;, mais vous avez sélectionné &apos;{field_name}&apos;.

Veuillez sélectionner le bon champ ou un autre fichier.</source>
        <translation>The file corresponds to the field ‘{data.get(&apos;field’)}‘, but you have selected ’{field_name}&apos;.

Please select the correct field or another file.</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="568"/>
        <source>Sauvegarder en CSV</source>
        <translation>Save as CSV</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="572"/>
        <source>Sauvegarder dans la base de données</source>
        <translation>Save to database</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="584"/>
        <source>Charger la table</source>
        <translation>Load the table</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="299"/>
        <location filename="../fuzzytext_dialog.py" line="308"/>
        <location filename="../fuzzytext_dialog.py" line="346"/>
        <location filename="../fuzzytext_dialog.py" line="1039"/>
        <location filename="../fuzzytext_dialog.py" line="1112"/>
        <location filename="../fuzzytext_dialog.py" line="1151"/>
        <source>Erreur</source>
        <translation>Error</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="1041"/>
        <location filename="../fuzzytext_dialog.py" line="1152"/>
        <source>Format de source non reconnu (ni GPKG ni PostGIS).</source>
        <translation>Unrecognized source format (neither GPKG nor PostGIS).</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="1054"/>
        <location filename="../fuzzytext_dialog.py" line="1117"/>
        <location filename="../fuzzytext_dialog.py" line="1159"/>
        <source>Info</source>
        <translation>Info</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="1054"/>
        <location filename="../fuzzytext_dialog.py" line="1117"/>
        <source>Impossible de créer ou charger la table &apos;metafuzzy&apos;.</source>
        <translation>Unable to create or load the ‘metafuzzy’ table.</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="1112"/>
        <source>Aucune couche sélectionnée.</source>
        <translation>No layer selected.</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="1160"/>
        <source>Aucune table &apos;metafuzzy&apos; trouvée.</source>
        <translation>No ‘metafuzzy’ table found.</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.py" line="1167"/>
        <source>Historique des transformations</source>
        <translation>Transformation history</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.ui" line="6"/>
        <source>Fuzzy Text Mapping</source>
        <translation>Fuzzy Text Mapping</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.ui" line="26"/>
        <source>Charger valeurs uniques</source>
        <translation>Load unique values</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.ui" line="35"/>
        <source>Affecter valeur fuzzy aux lignes sélectionnées</source>
        <translation>Assign fuzzy value to selected rows</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.ui" line="46"/>
        <source>Voir l&apos;historique des transformations</source>
        <translation>View transformation history</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.ui" line="56"/>
        <source>Créer attribut flou</source>
        <translation>Create fuzzy attribute</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.ui" line="63"/>
        <source>Fermer</source>
        <translation>Close</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.ui" line="74"/>
        <source>Astuce : associez chaque valeur texte du champ sélectionné à une valeur floue comprise entre 0 et 1.</source>
        <translation>Associate each text value in the selected field with a fuzzy value between 0 and 1.</translation>
    </message>
    <message>
        <location filename="../fuzzytext_dialog.ui" line="77"/>
        <source>color: gray; font-style: italic;</source>
        <translation>color: gray; font-style: italic;</translation>
    </message>
</context>
<context>
    <name>RasterAggregationDialog</name>
    <message>
        <source>Règle 1 violée : R3 (A=0,5 ; B=1) doit être &gt;= max(R1, R2).</source>
        <translation type="vanished">Rule 1 violated: R3 (A=0.5; B=1) must be &gt;= max(R1, R2).</translation>
    </message>
    <message>
        <source>Règle 2 violée : R3 (A=0,5 ; B=1) doit être &gt;= 0,5.</source>
        <translation type="vanished">Rule 2 violated : R3 (A=0,5 ; B=1)  must be  &gt;= 0,5.</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="20"/>
        <source>Préparation Agrégation Raster</source>
        <translation>Raster Aggregation Preparation</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="34"/>
        <source>Nom raster de sortie :</source>
        <translation>Output raster name:</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="36"/>
        <source>Aggregation_Result</source>
        <translation>Aggregation_Result</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="38"/>
        <source>Dossier de sortie :</source>
        <translation>Output directory:</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="41"/>
        <source>Parcourir...</source>
        <translation>Browse...</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="60"/>
        <source>Étendue spatiale</source>
        <translation>Spatial extent</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="62"/>
        <source>Intersection (zone commune)</source>
        <translation>Intersection (common area)</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="63"/>
        <source>Union (couvrir toute la zone)</source>
        <translation>Union (cover the entire area)</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="71"/>
        <source>Méthode de rééchantillonnage :</source>
        <translation>Resampling method:</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="79"/>
        <source>Définir la fonction d&apos;agrégation...</source>
        <translation>Define the aggregation function...</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="80"/>
        <source>Aucune fonction définie</source>
        <translation>No defined function</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="98"/>
        <source>Aide</source>
        <translation>Help</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="105"/>
        <source>Annuler</source>
        <translation>Exit</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="121"/>
        <source>Aide - Agrégation raster</source>
        <translation>Help - Raster aggregation</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="130"/>
        <source>Ce module permet d&apos;agréger deux rasters avec une fonction floue.

Étapes :
1. Choisissez Raster 1 et Raster 2.
   Les deux rasters doivent avoir le même CRS et être projetés. 
   Le raster 1 détermine la résolution du résultat.
2. Définissez l&apos;étendue : intersection ou union.
3. Choisissez le dossier et le nom du fichier de sortie.
4. Lancez l&apos;agrégation.

Le résultat est un raster GeoTIFF enregistré dans le dossier choisi.</source>
        <translation>This module allows you to aggregate two rasters using a fuzzy function.

Steps:
1. Select Raster 1 and Raster 2.
   Both rasters must have the same CRS and be projected. 
   Raster 1 determines the resolution of the result.
2. Define the extent: intersection or union.
3. Select the folder and name of the output file.
4. Start the aggregation.

The result is a GeoTIFF raster saved in the selected folder.</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="134"/>
        <source>Choisir dossier de sortie</source>
        <translation>Select output folder</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="191"/>
        <source>Fonction manquante</source>
        <translation>Missing function</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="193"/>
        <source>Veuillez définir une fonction d’agrégation avant de continuer.</source>
        <translation>Please define an aggregate function before continuing.</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="201"/>
        <source>Vérification de la combinaison</source>
        <translation>Verification of the combination</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="202"/>
        <source>La combinaison semble incohérente :

{details}

Voulez-vous continuer ?</source>
        <translation>The combination seems inconsistent:

{details}

Do you want to continue?</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="216"/>
        <source>Erreur</source>
        <translation>Error</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="218"/>
        <source>Impossible de construire la fonction d’agrégation.

{e}</source>
        <translation>Unable to build the aggregate function.

{e}</translation>
    </message>
    <message>
        <source>Fonction manquante</source>
        <comment>Veuillez définir une fonction d’agrégation avant de continuer.</comment>
        <translation type="vanished">Missing function</translation>
    </message>
    <message>
        <source>Vérification de la combinaison</source>
        <comment>La combinaison semble incohérente :

{details}

Voulez-vous continuer ?</comment>
        <translation type="vanished">Verification of the combination</translation>
    </message>
    <message>
        <source>Erreur</source>
        <comment>Impossible de construire la fonction d’agrégation.

{e}</comment>
        <translation type="vanished">Error</translation>
    </message>
</context>
<context>
    <name>RasterMetadataDialog</name>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="564"/>
        <source>Erreur</source>
        <translation>Error</translation>
    </message>
    <message>
        <location filename="../fuzzyraster_dialog.py" line="564"/>
        <source>Fichier métadonnées non trouvé :
{fzy_path}</source>
        <translation>Metadata file not found:
{fzy_path}</translation>
    </message>
</context>
<context>
    <name>self.self</name>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="253"/>
        <source>Règle 1 violée : R3 (A=0,5 ; B=1) doit être &gt;= max(R1, R2).</source>
        <translation>Rule 1 violated: R3 (A=0.5; B=1) must be &gt;= max(R1, R2).</translation>
    </message>
    <message>
        <location filename="../fuzzyaggregation_raster_dialog.py" line="257"/>
        <source>Règle 2 violée : R3 (A=0,5 ; B=1) doit être &gt;= 0,5.</source>
        <translation>Rule 2 violated : R3 (A=0,5 ; B=1)  must be  &gt;= 0,5.</translation>
    </message>
</context>
</TS>
