### Dog breed classifier

ML project for learning to classify dog breeds.

### Setup project:

## Environment setup:
To activate the conda environment with the .yml file (that is hopefully updated and maintained as needed), please refer
to conda docs regarding this topic.

https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file

- Steps: `conda env create -f keras-dog-env.yml` and then `conda activate keras-dog`

## Sourcing data:
Model is trained using data set from "Stanford dogs dataset" which can be found at: http://vision.stanford.edu/aditya86/ImageNetDogs/

- Download the dataset and place the folder on the same level directory as the '/src/' folder (top-level).
- Re-name the dataset folder into 'dog_pics'. Feel free to re-name it something else, but remember to change the 'filepath' variable as needed.

## Pre-processing data and running the CNN model:
You can then pre-process the data by running a script containing the `process_all_images_to_fit()` function.
This is already set-up in the `main.py` file. You can run this in your terminal via: `python3 -B src/main.py`.
Uncomment out the aforementioned function once the data has been pre-processed.

The CNN model is also in the main.py file, and you can use the `run_model()` function to do that too.
