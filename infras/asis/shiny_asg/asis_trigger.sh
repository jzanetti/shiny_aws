#!/bin/sh

echo "asis trigger script ..."
. $CONDA_PREFIX/../../etc/profile.d/conda.sh
which python
conda deactivate
conda activate base
which python
cd /tmp/asis/shiny_asg
cdk deploy --require-approval never
