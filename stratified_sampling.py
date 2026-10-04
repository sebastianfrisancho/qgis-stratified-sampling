"""
===============================================================================
QGIS Stratified Random Sampling
===============================================================================

Author:
    Sebastian Frisancho

Version:
    1.0.0

Description:
    Performs stratified random sampling on QGIS point vector layers while
    preserving all original attributes.

    Users define sampling quotas for one or more categories (strata), and the
    script automatically creates a new memory layer containing randomly
    selected features.

Requirements:
    - QGIS 3.x
    - Python 3.x

License:
    MIT License
===============================================================================
"""

__author__ = "Sebastian Frisancho"
__version__ = "1.0.0"

import random

from qgis.core import (
    QgsFeature,
    QgsProject,
    QgsVectorLayer,
    QgsWkbTypes,
)


def stratified_random_sampling():
    """
    Perform stratified random sampling on a QGIS point layer.

    The script groups features according to a categorical attribute,
    randomly selects the requested number of features from each category,
    and creates a new memory layer while preserving all original fields.

    Returns
    -------
    None
    """
    print("\nStarting stratified random sampling...\n")

    # =============================================================================
    # USER CONFIGURATION
    # Modify only this section when adapting the script to a new project.
    # =============================================================================
    LAYER_NAME = "your_layer_name_here"
    CLASS_COLUMN = "your_column_name_here"
    OUTPUT_NAME = "Selected_Points"

    # Example configuration.
    # Replace the class names with the categories in your own dataset.
    TARGET_SAMPLE = {
        "Primary Forest": 5,
        "Secondary Forest": 5,
    }
    # =============================================================================

    print(f"Input layer: {LAYER_NAME}")

    matches = QgsProject.instance().mapLayersByName(LAYER_NAME)
    if not matches:
        print(f"ERROR: Layer '{LAYER_NAME}' not found.")
        return
    layer = matches[0]

    if not layer.isValid():
        print(f"ERROR: Layer '{LAYER_NAME}' is invalid.")
        return
    if layer.geometryType() != QgsWkbTypes.PointGeometry or QgsWkbTypes.isMultiType(layer.wkbType()):
        print("ERROR: Input layer must contain single-part point geometries.")
        return

    # Validate quotas before reading features.
    if not TARGET_SAMPLE:
        print("ERROR: TARGET_SAMPLE must contain at least one category.")
        return
    for category, amount in TARGET_SAMPLE.items():
        if not isinstance(amount, int) or isinstance(amount, bool) or amount < 0:
            print(f"ERROR: Sample size for '{category}' must be a non-negative integer.")
            return

    normalized_targets = [str(key).strip().casefold() for key in TARGET_SAMPLE]
    if len(normalized_targets) != len(set(normalized_targets)):
        print("ERROR: TARGET_SAMPLE contains duplicate categories after case/space normalization.")
        return

    # Check if the class column exists
    if CLASS_COLUMN not in layer.fields().names():
        print(f"ERROR: Column '{CLASS_COLUMN}' does not exist in the layer.")
        return

    print("Reading features and grouping by category...")

    features_by_class = {
        str(key).strip().casefold(): []
        for key in TARGET_SAMPLE.keys()
    }

    for feature in layer.getFeatures():
        if not feature.hasGeometry() or feature.geometry().isEmpty():
            continue

        raw_class = feature[CLASS_COLUMN]
        if raw_class is None:
            continue
        feature_class = str(raw_class).strip().casefold()

        if feature_class in features_by_class:
            features_by_class[feature_class].append(feature)

    print("Performing random sampling...")
    selected_features = []

    for target_class, required_amount in TARGET_SAMPLE.items():
        class_key = str(target_class).strip().casefold()
        candidate_features = features_by_class[class_key]
        total_available = len(candidate_features)

        if total_available == 0:
            print(f"WARNING: No features found for class '{target_class}'.")
            continue

        if total_available < required_amount:
            print(
                f"WARNING: Only {total_available} feature(s) available "
                f"for '{target_class}' (requested {required_amount}). "
                f"Using all available."
            )
            selected_class_features = candidate_features
        else:
            # Randomly select the required number of features.
            selected_class_features = random.sample(
                candidate_features, required_amount
            )

        selected_features.extend(selected_class_features)
        print(
            f"{target_class}: "
            f"{len(selected_class_features)} feature(s) selected."
        )

    if not selected_features:
        print("ERROR: No features were selected. Check your attribute table.")
        return

    print("Creating output layer...")
    layer_crs = layer.crs()
    out_layer = QgsVectorLayer("Point", OUTPUT_NAME, "memory")
    out_layer.setCrs(layer_crs)
    if not out_layer.isValid():
        print("ERROR: Could not create the output memory layer.")
        return
    provider = out_layer.dataProvider()

    provider.addAttributes(layer.fields().toList())
    out_layer.updateFields()

    new_features = []
    for source_feature in selected_features:
        new_feature = QgsFeature()
        new_feature.setGeometry(source_feature.geometry())
        new_feature.setAttributes(list(source_feature.attributes()))
        new_features.append(new_feature)

    # Copy selected features into the output layer.
    success, _ = provider.addFeatures(new_features)
    if not success:
        print("ERROR: QGIS could not add all selected features to the output layer.")
        return
    out_layer.updateExtents()
    QgsProject.instance().addMapLayer(out_layer)

    print(
        f"\nSampling completed successfully.\n"
        f"Total selected features: {len(selected_features)}\n"
        f"Output layer: {OUTPUT_NAME}"
    )


if __name__ == "__main__":
    stratified_random_sampling()