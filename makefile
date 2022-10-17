# override CONDA_BASE = ~/Programs/miniconda3
# override CONDA_BASE = ${CONDA_BASE}
override CONDA = $(CONDA_BASE)/bin/conda

help:
	echo $(CONDA_BASE)

env:
	rm -rf $(CONDA_BASE)/envs/shiny_aws
	$(CONDA) env create -f env.yml
	$(CONDA_BASE)/envs/shiny_aws/bin/pip install -r requirements.txt
	$(CONDA_BASE)/envs/shiny_aws/bin/npm install -g aws-cdk --prefix $(CONDA_BASE)/envs/shiny_aws

build:
	$(CONDA) build .

install_awscli:
	rm -rf /tmp/install_awscli
	mkdir -p /tmp/install_awscli
	curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/install_awscli/awscliv2.zip"
	cd /tmp/install_awscli; unzip /tmp/install_awscli/awscliv2.zip
	/tmp/install_awscli/aws/install -i $(CONDA_BASE)/envs/shiny_aws/aws-cli -b $(CONDA_BASE)/envs/shiny_aws/bin
	rm -rf /tmp/install_awscli


install:
	$(CONDA) install -f $(CONDA_BASE)/conda-bld/linux-64/shiny_aws-0.0.1-py310_0.tar.bz2 -n shiny_aws

all: env build install install_awscli
