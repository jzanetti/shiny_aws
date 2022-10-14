override CONDA_BASE = ~/Programs/miniconda3
override CONDA = $(CONDA_BASE)/bin/conda

env:
	rm -rf $(CONDA_BASE)/envs/shiny_aws
	$(CONDA) env create -f env.yml
	$(CONDA_BASE)/envs/shiny_aws/bin/pip install -r requirements.txt
	$(CONDA_BASE)/envs/shiny_aws/bin/npm install -g aws-cdk --prefix $(CONDA_BASE)/envs/shiny_aws

build:
	$(CONDA) build .

install:
	$(CONDA) install -f $(CONDA_BASE)/conda-bld/linux-64/shiny_aws-0.0.1-py310_0.tar.bz2 -n shiny_aws

all: env build install
