# QGIS Stratified Random Sampling

A Python script for QGIS that performs **stratified random sampling** on point vector layers.

The script allows users to define sampling quotas for different categories (e.g., primary forest, secondary forest, degraded forest) and automatically creates a new layer containing randomly selected points while preserving all original attributes.

---

## Features

- Stratified random sampling
- User-defined sample quotas
- Preserves the complete attribute table
- Handles missing geometries safely
- Warns when requested samples exceed available features
- Creates a new QGIS memory layer

---

## Typical Applications

This tool is useful for:

- Forest inventory plot selection
- Carbon monitoring projects
- Biodiversity surveys
- Ecological sampling
- Remote sensing validation
- Environmental monitoring

---

## Requirements

- QGIS 3.x
- Python 3

---

## Configuration

Before running the script, edit the following variables:

```python
LAYER_NAME
CLASS_COLUMN
TARGET_SAMPLE
RANDOM_SEED
```

Example:

```python
TARGET_SAMPLE = {
    "Primary Forest": 5,
    "Secondary Forest": 5
}

# Optional: use an integer to reproduce the same random sequence.
RANDOM_SEED = 42
```

---

## Output

The script creates a new QGIS memory layer called:

```
Selected_Points
```

The output preserves all original attributes and geometries. If a category has fewer features than requested, all available features in that category are selected. Set `RANDOM_SEED` to an integer to make the random selection repeatable for the same input data and feature ordering; use `None` for a different random sequence each run.

---

## Author

**Sebastian Frisancho**

Biologist specializing in Remote Sensing, LiDAR and Forest Ecology.

- **GitHub:** [@sebastianfrisancho](https://github.com/sebastianfrisancho)
- **LinkedIn:** [Sebastian Frisancho](https://www.linkedin.com/in/sebastianfrisancho/)

Remote Sensing | LiDAR | Forest Ecology | GIS | Python

---

## License

MIT License