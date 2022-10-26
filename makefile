.ONESHELL:

SHELL = /bin/bash

override CONDA = $(CONDA_BASE)/bin/conda
override PKG = shiny_aws
override CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

help:
	@echo "current platform: " $(PLATFORM)
	@echo "current conda_base: $(CONDA_BASE)"
	@echo "current conda: $(CONDA)"
	@echo "- install shiny_aws: make all"
	@echo "- install env: make env"
	@echo "- clean up env: make clear_env"
	@echo "- remove everthing: make clear_all"

clear_env:
	rm -rf $(CONDA_BASE)/envs/$(PKG)
	$(CONDA) index $(CONDA_BASE)/conda-bld

clear_all:
	rm -rf $(CONDA_BASE)/envs/$(PKG)
	rm -rf $(CONDA_BASE)/pkgs/$(PKG)*
	rm -rf $(CONDA_BASE)/conda-bld/linux-64/$(PKG)*
	rm -rf $(CONDA_BASE)/conda-bld/osx-arm64/$(PKG)*
	rm -rf $(CONDA_BASE)/conda-bld/$(PKG)*
	rm -rf $(CONDA_BASE)/conda-bld/linux-64/.cache/paths/$(PKG)*
	rm -rf $(CONDA_BASE)/conda-bld/linux-64/.cache/recipe/$(PKG)*
	rm -rf $(CONDA_BASE)/conda-bld/osx-arm64/.cache/paths/$(PKG)*
	rm -rf $(CONDA_BASE)/conda-bld/osx-arm64/.cache/recipe/$(PKG)*
	$(CONDA) index $(CONDA_BASE)/conda-bld

env: clear_all
	$(CONDA) env create -f env.yml
	$(CONDA_ACTIVATE) $(PKG); $(CONDA_BASE)/envs/$(PKG)/bin/pip3 install -r requirements.txt; $(CONDA_BASE)/envs/$(PKG)/bin/npm install -g aws-cdk --prefix $(CONDA_BASE)/envs/$(PKG)

build:
	$(CONDA) build .


install_awscli:
	rm -rf /tmp/install_awscli
	mkdir -p /tmp/install_awscli
	@if [ "$(PLATFORM)" = "mac" ]; then \
		curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "/tmp/install_awscli/awscliv2.pkg"; \
		cd /tmp/install_awscli; installer -pkg awscliv2.pkg -target $(CONDA_BASE)/envs/$(PKG)/bin; \
	elif [ "$(PLATFORM)" = "linux" ]; then \
		curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/install_awscli/awscliv2.zip"; \
		cd /tmp/install_awscli; unzip /tmp/install_awscli/awscliv2.zip; \
		/tmp/install_awscli/aws/install -i $(CONDA_BASE)/envs/$(PKG)/aws-cli -b $(CONDA_BASE)/envs/$(PKG)/bin; \
	fi
	rm -rf /tmp/install_awscli

install_awscli_linux:
	rm -rf /tmp/install_awscli
	mkdir -p /tmp/install_awscli
	curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/install_awscli/awscliv2.zip"
	cd /tmp/install_awscli; unzip /tmp/install_awscli/awscliv2.zip
	/tmp/install_awscli/aws/install -i $(CONDA_BASE)/envs/$(PKG)/aws-cli -b $(CONDA_BASE)/envs/$(PKG)/bin
	rm -rf /tmp/install_awscli


install:
	$(CONDA_ACTIVATE) $(PKG); $(CONDA) install $(PKG) -c local --yes --prefix $(CONDA_BASE)/envs/$(PKG)

all: env build install install_awscli
