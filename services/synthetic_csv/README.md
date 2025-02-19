# Synthetic E-commerce Dataset Generator

A Python script to generate synthetic e-commerce customer data for testing and development purposes.

## Features

- Generates realistic customer data including:
  - Customer information (ID, name, email)
  - Purchase details
  - Demographics
  - Account information
  - Shopping preferences
- Configurable number of records
- Reproducible data generation with seed option
- CSV output format

## Requirements

```bash
pip install pandas faker
```

```
python generate_data.py
```

```
python generate_data.py --num-rows 10000 --output custom_dataset.csv --seed 42
```
