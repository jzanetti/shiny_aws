override CONDA_BASE = ~/Programs/miniconda3
override CONDA = $(CONDA_BASE)/bin/conda

env:
	rm -rf $(CONDA_BASE)/envs/shiny_aws_bsis
	$(CONDA) env create -f env.yml

build:
	$(CONDA) build .

install:
	$(CONDA) install -f $(CONDA_BASE)/conda-bld/linux-64/shiny_aws_bsis-0.0.1-py310_0.tar.bz2 -n shiny_aws_bsis

bsis: env build install
