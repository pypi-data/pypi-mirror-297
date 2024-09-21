# mlstac

A Common Language for EO Machine Learning Data

Low-level API

```python
import mlstac

# Read the data online
path = "https://huggingface.co/datasets/JulioContrerasH/prueba1/resolve/main/images_2000.mlstac"
metadata = mlstac.core.load_metadata(path)
data = mlstac.core.load_data(metadata[0:4])
data.shape

# Read the data locally
path = "/home/cesar/Downloads/images_2000.mlstac"
dataset = mlstac.core.load_metadata(path)
data = mlstac.core.load_data(dataset[0:4])

# From mlstac to GEOTIFF
import rasterio as rio
path = "https://huggingface.co/datasets/JulioContrerasH/prueba1/resolve/main/images_2000.mlstac"
metadata = mlstac.core.load_metadata(path)
data, metadata = mlstac.core.load_data(metadata[0:1], save_metadata_datapoint=True)[0]
with rio.open("data.tif", "w", **metadata) as dst:
    dst.write(data)
```

High-level API:

```python
import pathlib
import mlstac

## Streaming read support

# Load the ML-STAC collection
ds = mlstac.load(snippet="isp-uv-es/CloudSEN12Plus")
subset = ds.metadata[(ds.metadata["split"] == "test") & (ds.metadata["label_type"] == "high") & (ds.metadata["proj_shape"] == 509)][10:14]

# Load the data
datacube = mlstac.get_data(dataset=subset)

## Local read support

OUTPATH = pathlib.Path("/media/cesar/0790BB3D255A0B7F/CloudSEN12plus/")

# Download the entire dataset
mlstac.download(snippet="isp-uv-es/CloudSEN12Plus", path=OUTPATH)

# Load the ML-STAC collection
ds = mlstac.load(snippet=OUTPATH / "main.json", force=False)
subset = ds.metadata[(ds.metadata["split"] == "test") & (ds.metadata["label_type"] == "high") & (ds.metadata["proj_shape"] == 509)][100:110]

# Load the data
datacube = mlstac.get_data(dataset=subset)
```

Create a MLSTAC Collection object


```python
import requests
import mlstac

# Define the descriptor
description = (
    "<img src='cloudsen12.gif' alt='drawing' width='20%'/>\n"
    "CloudSEN12+ is a significant extension of the CloudSEN12 dataset, which"
    " doubles the number of expert-reviewed labels, making it, by a large"
    " margin, the largest cloud detection dataset to date for Sentinel-2."
    " All labels from the previous version have been curated and refined,"
    " enhancing the dataset's trustworthiness. This new release is licensed"
    " under CC0, which puts it in the public domain and allows anyone to use,"
    " modify, and distribute it without permission or attribution.\n\n"
    "##Data Folder order:\n\n"
    " The CloudSEN12+ dataset is organized into `train`, `val`, and `test` splits."
    " The images have been padded from 509x509 to 512x512 and 2000x2000 to"
    " 2048x2048 to ensure that the patches are divisible by 32. The padding"
    " is filled with zeros in the left and bottom sides of the image. For"
    " those who prefer traditional storage formats, GeoTIFF files are"
    " available in our [ScienceDataBank](https://www.scidb.cn/en/detail?dataSetId=2036f4657b094edfbb099053d6024b08&version=V1) repository.\n\n"
    "<center>\n"
    "<img src='https://cdn-uploads.huggingface.co/production/uploads/6402474cfa1acad600659e92/9UA4U3WObVeq7BAcf37-C.png' alt='drawing' width='50%'/>\n"
    "</center>\n"
    "*CloudSEN12+ spatial coverage. The terms p509 and p2000 denote the"
    " patch size 509 × 509 and 2000 × 2000, respectively. `high`, `scribble`,"
    " and `nolabel` refer to the types of expert-labeled annotations*"
)

def get_checksum(file: str):
    return int(requests.head(file).headers["X-Linked-Size"])


# Define the catalog
REPO = "https://huggingface.co/datasets/isp-uv-es/CloudSEN12Plus/resolve/main/"
train_catalog = mlstac.SingleCatalog(
    name = "train",
    metadata = REPO + "train/metadata.parquet",
    data_files = [
        REPO + "train/train_2000_high.mlstac",
        REPO + "train/train_509_high.mlstac",
        REPO + "train/train_509_scribble.mlstac",
        REPO + "train/train_509_nolabel_chunk1.mlstac",
        REPO + "train/train_509_nolabel_chunk2.mlstac"
    ],
    data_descriptions = [
        "The training set contains 687 patches of 2048x2048 pixels with high-quality labels.",
        "The training set contains 8490 patches of 512x512 pixels with high-quality labels.",
        "The training set contains 8785 patches of 512x512 pixels with scribble labels.",
        "The training set contains 14700 patches of 512x512 pixels with no labels (chunk 1).",
        "The training set contains 14700 patches of 512x512 pixels with no labels (chunk 2)."
    ],
    data_checksum = [
        get_checksum(REPO + "train/train_2000_high.mlstac"),
        get_checksum(REPO + "train/train_509_high.mlstac"),
        get_checksum(REPO + "train/train_509_scribble.mlstac"),
        get_checksum(REPO + "train/train_509_nolabel_chunk1.mlstac"),
        get_checksum(REPO + "train/train_509_nolabel_chunk2.mlstac")
    ],
    metadata_file = REPO + "train/metadata.parquet",
    metadata_description = "The metadata of the training set.",
    metadata_checksum = get_checksum(REPO + "train/metadata.parquet")
)

val_catalog = mlstac.SingleCatalog(
    name = "validation",
    metadata = REPO + "validation/metadata.parquet",
    data_files = [
        REPO + "validation/validation_2000_high.mlstac",
        REPO + "validation/validation_509_high.mlstac",
        REPO + "validation/validation_509_scribble.mlstac"
    ],
    data_descriptions = [
        "The validation set contains 77 patches of 2048x2048 pixels with high-quality labels.",
        "The validation set contains 687 patches of 512x512 pixels with high-quality labels.",
        "The validation set contains 85 patches of 512x512 pixels with scribble labels."
    ],
    data_checksum = [
        get_checksum(REPO + "validation/validation_2000_high.mlstac"),
        get_checksum(REPO + "validation/validation_509_high.mlstac"),
        get_checksum(REPO + "validation/validation_509_scribble.mlstac")
    ],
    metadata_file = REPO + "validation/metadata.parquet",
    metadata_description = "The metadata of the validation set.",
    metadata_checksum = get_checksum(REPO + "validation/metadata.parquet")
)

test_catalog = mlstac.SingleCatalog(
    name = "test",
    data_files = [
        REPO + "test/test_2000_high.mlstac",
        REPO + "test/test_509_high.mlstac",
        REPO + "test/test_509_scribble.mlstac"
    ],
    data_descriptions = [
        "The test set contains 85 patches of 2048x2048 pixels with high-quality labels.",
        "The test set contains 975 patches of 512x512 pixels with high-quality labels.",
        "The test set contains 655 patches of 512x512 pixels with scribble labels."
    ],
    data_checksum = [
        get_checksum(REPO + "test/test_2000_high.mlstac"),
        get_checksum(REPO + "test/test_509_high.mlstac"),
        get_checksum(REPO + "test/test_509_scribble.mlstac")
    ],
    metadata_file = REPO + "test/metadata.parquet",
    metadata_description = "The metadata of the test set.",
    metadata_checksum = get_checksum(REPO + "test/metadata.parquet")
)

ml_catalog=mlstac.Catalog(
    train = train_catalog,
    validation = val_catalog,
    test = test_catalog
)

# Define the providers
providers = mlstac.stac.Providers(
    field=[
        mlstac.stac.Provider(
            name="Image & Signal Processing",
            roles=["host"],
            url="https://isp.uv.es/"
        ),
        mlstac.stac.Provider(
            name="ESA",
            roles=["producer"],
            url="https://www.esa.int/"
        )
    ]
)

# Define a simple ML-STAC collection
ml_collection = mlstac.Collection(
    id = "CloudSEN12Plus",
    title = "A global dataset for semantic understanding of cloud and cloud shadow in Sentinel-2",
    description = description,
    license = "cc0-1.0",
    providers = providers,
    keywords = ["clouds", "sentinel-2", "image-segmentation", "deep-learning", "remote-sensing"],
    ml_task = ["image-segmentation"],
    ml_catalog = ml_catalog,
    extent = mlstac.stac.Extent(
        spatial = mlstac.stac.SpatialExtent(bbox=[[-180, -56, 180, 84]]),
        temporal = mlstac.stac.TemporalExtent(interval=[["2015-06-23T00:00:00Z", "2023-06-23T00:00:00Z"]])
    )
)


# Define extensions [Optional]

## Extension --- Define authors

### RSC4Earth
ml_collection.add_author(
    name="David Montero",
    position="PhD",
    organization= "RSC4Earth",
    links=[{
        "href": "https://twitter.com/dmlmont",
        "rel": "group"
    }]
)

### IPL
authors = ["Cesar Aybar", "Gonzalo Mateo-García", "Luis Gómez-Chova"]
webs = ["http://csaybar.github.io/", "https://www.uv.es/gonmagar/", "https://www.uv.es/chovago/"]
for author, web in zip(authors, webs):
    ml_collection.add_author(
        name=author,
        position="PhD",
        organization= "Image & Signal Processing",
        links=[{
            "href": web,
            "rel": "about"
        }]
    )


### UNMSM
authors = [
    "Luis Ysuhuaylas", "Jhomira Loja", "Karen Gonzales",
    "Fernando Herrera", "Lesly Bautista", "Roy Yali",
    "Wendy Espinoza", "Fernando Prudencio", "Lucy A. Flores",
    "Evelin Mamani", "Antonio Limas", "Alejandro Alcantara"
]

for author in authors:
    ml_collection.add_author(
        name=author,
        position="Bachelor student",
        organization= "UNMSM",
        links=[{
            "href": "https://vrip.unmsm.edu.pe/ecohidro/",
            "rel": "group"
        }]
    )

## Agraria La Molina
ml_collection.add_author(
    name="Daryl Ayala",
    position="Bachelor student",
    organization= "U. Agraria La Molina",
    links=[{
        "href": "https://www.lamolina.edu.pe/",
        "rel": "group"
    }]
)

## Villareal
ml_collection.add_author(
    name="Jeanett Valladares",
    position="Bachelor student",
    organization= "U. Villareal",
    links=[{
        "href": "https://www.unfv.edu.pe/",
        "rel": "group"
    }]
)


## Santiago Antunez de Mayolo
ml_collection.add_author(
    name="Maria Quiñonez",
    position="Bachelor student",
    organization= "U. Santiago Antunez de Mayolo",
    links=[{
        "href": "https://www.usam.edu.pe/",
        "rel": "group"
    }]
)

## Agraria de la Selva
ml_collection.add_author(
    name="Rai Fajardo",
    position="Bachelor student",
    organization= "U. Agraia de la Selva",
    links=[{
        "href": "https://www.unas.edu.pe/",
        "rel": "group"
    }]
)

## Cayetano Heredia
authors = [
    "Raul Loayza-Muro",
    "Martin Leyva",
    "Bram Willems",
]
for author in authors:
    ml_collection.add_author(
        name=author,
        position="PhD",
        organization= "U. Cayetano Heredia",
        links=[{
            "href": "https://www.upch.edu.pe/",
            "rel": "group"
        }]
    )

## Extension --- Define curators
ml_collection.add_curator(
    name="Cesar Aybar",
    position="PhD",
    organization= "Image & Signal Processing",
    links=[{
        "href": "http://csaybar.github.io/",
        "rel": "about"
    }]
)

## Extension --- Define labels
ml_collection.add_labels(
    labels={"clear": 0, "thick-cloud": 1, "thin-cloud": 2, "cloud-shadow": 3},
    layers=1
)

## Extension --- Define spectral bands
ml_collection.add_dimension(axis=0, name="C", description="Spectral bands")
ml_collection.add_dimension(axis=1, name="H", description="Height")
ml_collection.add_dimension(axis=2, name="W", description="Width")

## Extension --- Spectral extension
ml_collection.add_sentinel2()

## Extension --- rawdata
ml_collection.add_raw_data_url(url="https://cloudsen12.github.io/")

## Extension --- discussion
ml_collection.add_discussion_url(url="https://huggingface.co/datasets/isp-uv-es/CloudSEN12Plus/discussions")

## Extension --- split strategy
ml_collection.add_split_strategy(split_strategy="stratified")

## Extension --- paper
ml_collection.add_paper(url="https://www.sciencedirect.com/science/article/pii/S2352340924008163")

## Save the results
ml_collection.create_markdown(outfile="README.md")
ml_collection.create_json(outfile="main.json")
```
