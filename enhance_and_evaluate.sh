#!/bin/bash


python recipes/cad1/task1/baseline/enhance.py path.root=$(pwd)/recipes/cad1/cadenza_data_demo/cad1/task1 path.exp_folder=$(pwd)/exp_demucs_baseline
SAMPLIFI=1 python recipes/cad1/task1/baseline/enhance.py path.root=$(pwd)/recipes/cad1/cadenza_data_demo/cad1/task1 path.exp_folder=$(pwd)/exp_demucs_samplifi

python recipes/cad1/task1/baseline/evaluate.py path.root=$(pwd)/recipes/cad1/cadenza_data_demo/cad1/task1 path.exp_folder=$(pwd)/exp_demucs_baseline
SAMPLIFI=1 python recipes/cad1/task1/baseline/evaluate.py path.root=$(pwd)/recipes/cad1/cadenza_data_demo/cad1/task1 path.exp_folder=$(pwd)/exp_demucs_samplifi
