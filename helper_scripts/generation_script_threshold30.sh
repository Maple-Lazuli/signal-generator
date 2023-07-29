#!/bin/bash
cd ../
source venv/bin/activate
cd src
python -m cli  --quantity 5000 --use-dask true  --max-signals 30 --generation-directory ../data_gen/threshold_transmission/ --threshold true
