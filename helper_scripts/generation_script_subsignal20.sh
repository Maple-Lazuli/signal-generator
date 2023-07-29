#!/bin/bash
cd ../
source venv/bin/activate
cd src
python -m cli  --quantity 5000 --use-dask true  --max-signals 20 --generation-directory  ../data_gen/non_threshold_subsignals/ --sub-labels true
