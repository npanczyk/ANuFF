import numpy as np
import pandas as pd
import random
import yaml
import matplotlib.pyplot as plt
import datetime as dt
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss
from data_fab import get_data
from pytorch_tabular import TabularModel
from pytorch_tabular.models import (
    CategoryEmbeddingModelConfig,
    FTTransformerConfig,
    TabNetModelConfig,
    GatedAdditiveTreeEnsembleConfig,
    TabTransformerConfig,
    AutoIntConfig
)
from pytorch_tabular.config import DataConfig, OptimizerConfig, TrainerConfig, ExperimentConfig
from pytorch_tabular.models.common.heads import LinearHeadConfig

# ADD THE SPECIFIC MODEL RUNS AS FUNCTIONS HERE, THEN FIGURE OUT A WAY TO LET THE USER PICK A MODEL TO RUN (INPUT FILE?)

def CategoryEmbedding():
    model_config = CategoryEmbeddingModelConfig(
    task="classification",
    layers="64-32",  # Number of nodes in each layer
    activation="ReLU", # Activation between each layers
    learning_rate = 1e-3,
    head = "LinearHead", #Linear Head
    head_config = head_config, # Linear Head Config
    )

    tabular_model = TabularModel(
        data_config=data_config,
        model_config=model_config,
        optimizer_config=optimizer_config,
        trainer_config=trainer_config,
    )
    print('CategoryEmbedding Results')
    tabular_model.fit(train=train)
    tabular_model.evaluate(test)
    return 

def GatedAdditiveTree():
    model_config = GatedAdditiveTreeEnsembleConfig(
    task="classification",
    learning_rate = 1e-3,
    head = "LinearHead", #Linear Head
    head_config = head_config, # Linear Head Config
    )

    tabular_model = TabularModel(
        data_config=data_config,
        model_config=model_config,
        optimizer_config=optimizer_config,
        trainer_config=trainer_config,
    )
    print('GatedAdditiveTree Results')
    tabular_model.fit(train=train)
    tabular_model.evaluate(test)
    return 

def FTTransformer():
    model_config = FTTransformerConfig(
    task="classification",
    learning_rate = 1e-3,
    head = "LinearHead", #Linear Head
    head_config = head_config, # Linear Head Config
    )

    tabular_model = TabularModel(
        data_config=data_config,
        model_config=model_config,
        optimizer_config=optimizer_config,
        trainer_config=trainer_config,
    )
    print('FTTransformer Results')
    tabular_model.fit(train=train)
    tabular_model.evaluate(test)
    return 

def TabTransformer():
    model_config = TabTransformerConfig(
    task="classification",
    learning_rate = 1e-3,
    head = "LinearHead", #Linear Head
    head_config = head_config, # Linear Head Config
    )

    tabular_model = TabularModel(
        data_config=data_config,
        model_config=model_config,
        optimizer_config=optimizer_config,
        trainer_config=trainer_config,
    )
    print('TabTransformer Results')
    tabular_model.fit(train=train)
    tabular_model.evaluate(test)
    return 

def AutoInt():
    model_config = AutoIntConfig(
    task="classification",
    learning_rate = 1e-3,
    head = "LinearHead", #Linear Head
    head_config = head_config, # Linear Head Config
    )

    tabular_model = TabularModel(
        data_config=data_config,
        model_config=model_config,
        optimizer_config=optimizer_config,
        trainer_config=trainer_config,
    )
    print('AutoInt Results')
    tabular_model.fit(train=train)
    tabular_model.evaluate(test)
    return 

def TabNetModel():
    model_config = TabNetModelConfig(
    task="classification",
    learning_rate = 1e-3,
    head = "LinearHead", #Linear Head
    head_config = head_config, # Linear Head Config
    )

    tabular_model = TabularModel(
        data_config=data_config,
        model_config=model_config,
        optimizer_config=optimizer_config,
        trainer_config=trainer_config,
    )
    print('TabNetModel Results')
    tabular_model.fit(train=train)
    tabular_model.evaluate(test)
    return 


if __name__=="__main__":
    # read input file stuff
    with open('input.yml', 'r') as f:
        doggo = yaml.full_load(f)
    if doggo.get('cat_cols') == None:
        cat_cols = []
    else:
        cat_cols = doggo.get('cat_cols')
    num_cols = doggo.get('num_cols')
    target_col = doggo.get('target_col')
    models = doggo.get('models')
    data = pd.read_excel(doggo.get('data_file'))
    # list column over which the algorithm will predict outcomes (in our case, whether or not the rod failed)
    target=[target_col]
    train, test = train_test_split(data, stratify=data[target_col], test_size=0.2, random_state=42)
    data_config = DataConfig(
    target=target, #target should always be a list
    continuous_cols=num_cols,
    categorical_cols=cat_cols,
    )
    trainer_config = TrainerConfig(
    #     auto_lr_find=True, # Runs the LRFinder to automatically derive a learning rate
        batch_size=256,
        max_epochs=500,
        early_stopping="valid_loss", # Monitor valid_loss for early stopping
        early_stopping_mode = "min", # Set the mode as min because for val_loss, lower is better
        early_stopping_patience=5, # No. of epochs of degradation training will wait before terminating
        checkpoints="valid_loss", # Save best checkpoint monitoring val_loss
        load_best=True, # After training, load the best checkpoint
    )

    optimizer_config = OptimizerConfig()

    head_config = LinearHeadConfig(
        layers="", # No additional layer in head, just a mapping layer to output_dim
        dropout=0.1,
        initialization="kaiming"
    ).__dict__ # Convert to dict to pass to the model config (OmegaConf doesn't accept objects)
    
    # run the models specified in the input file
    for model in models:
        if model == 'GatedAdditiveTree':
            GatedAdditiveTree()
        elif model == 'FTTransformer':
            FTTransformer()
        elif model == 'TabTransformer':
            TabTransformer()
        elif model == 'AutoInt':
            AutoInt()
        elif model == 'TabNetModel':
            TabNetModel()
        else:
            CategoryEmbedding()




