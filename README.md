# ANuFF
AI for Nuclear Fuel Failure

## Requirements
This repository requires the use of PyTorch Tabular, an open-source Generative Adversarial Network (GAN) platform for tabular data. The installation instructions are below, along with a list of other required Python libraries. 

### Installation
1. Create a new python environment (default is the latest version of Python=3.12.1)
	
conda create -n gan

2. Activate that python environment

conda activate gan

3. Install pytorch (these instructions are specific to Mac users, but more info can be found at: tps://pytorch-tabular.readthedocs.io/en/latest/gs_installation/)

conda install pytorch torchvision -c pytorch

4. Install Pytorch Tabular to your environment

pip install pytorch_tabular

5. Clone the pytorch_tabular Github repository

git clone https://github.com/manujosephv/pytorch_tabular.git

6. Navigate to the directory of the repository you just cloned

cd pytorch_tabular

7. Ensure all dependencies are installed to your environment

python setup.py install

### Other dependencies
ANuFF requires the use of:
- numpy
- pandas
- matplotlib
- sklearn
- datetime
- yaml

in addition to the software you just installed. Please make sure these are ready to go in your Python environment before getting started. 

## How to Use
Once you've cloned this repo, you can simply run the following files in order in your terminal to demonstrate ANuFF's capabilities:
- data_fab.py
- gan.py
- data_viz.py

If you'd like to manually create an input file (using non-fabricated data), you can copy the template of the data file created by the data_fab.py script, and insert your own data. You can change the models run using the input.yml file.
