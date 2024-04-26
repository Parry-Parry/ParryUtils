#!/bin/bash

# Function to create a Conda environment and install pandas
create_env() {
    local env_name=$1
    local python_version=$2
    
    # Create the Conda environment
    if [ -z "$python_version" ]; then
        conda create -n $env_name python
    else
        conda create -n $env_name python=$python_version
    fi
    
    # Activate the environment
    source activate $env_name

    conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia || echo "Failed to install pytorch, continuing with other packages..."
    pip install transformers[torch] || echo "Failed to install transformers, continuing with other packages..."
    pip install python-terrier || echo "Failed to install pandas, continuing with other packages..."
    pip install fire || echo "Failed to install fire, continuing with other packages..."
    pip install scipy || echo "Failed to install scipy, continuing with other packages..."
    pip install --upgrade git+https://github.com/Parry-Parry/ParryUtils.git || echo "Failed to install ParryUtils, continuing with other packages..."
    
    # Deactivate the environment
    conda deactivate
}

# Main script
if [ $# -lt 1 ]; then
    echo "Usage: $0 <env_name> [python_version]"
    exit 1
fi

env_name=$1
python_version=$2

create_env $env_name $python_version

echo "Conda environment '$env_name' created and pandas installed."
