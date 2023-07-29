#!/bin/bash
cd ../
source venv/bin/activate
cd src
python -m cli  --quantity 5000 --use-dask true  --max-signals 10 --generation-directory ../data_gen/threshold_subsignal/ --threshold true --sub-labels true
python -m cli  --quantity 5000 --use-dask true  --max-signals 20 --generation-directory ../data_gen/threshold_subsignal/ --threshold true --sub-labels true
python -m cli  --quantity 5000 --use-dask true  --max-signals 30 --generation-directory ../data_gen/threshold_subsignal/ --threshold true --sub-labels true
python -m cli  --quantity 5000 --use-dask true  --max-signals 40 --generation-directory ../data_gen/threshold_subsignal/ --threshold true --sub-labels true
python -m cli  --quantity 5000 --use-dask true  --max-signals 50 --generation-directory ../data_gen/threshold_subsignal/ --threshold true --sub-labels true
python -m cli  --quantity 5000 --use-dask true  --max-signals 60 --generation-directory ../data_gen/threshold_subsignal/ --threshold true --sub-labels true

