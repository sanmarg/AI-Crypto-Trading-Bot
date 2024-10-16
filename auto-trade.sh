#!/bin/bash

while true; do
    # Run collect_data.py
    echo "Running collect_data.py..."
    python3 collect_data.py

    # Run feature_engineering.py
    echo "Running feature_engineering.py..."
    python3 feature_engineering.py

    # Run random_forest_model.py
    echo "Running random_forest_model.py..."
    python3 random_forest_model.py

    # Run gradient_boost_model.py
    echo "Running gradient_boost_model.py..."
    python3 gradient_boost_model.py

    # Run support_vector_model.py
    echo "Running support_vector_model.py..."
    python3 support_vector_model.py

    # Run logistic_regression_model.py
    echo "Running logistic_regression_model.py..."
    python3 logistic_regression_model.py

    # Run aggregator.py
    echo "Running aggregator.py..."
    python3 aggregator.py

    # Wait for 15 minutes (900 seconds)
    echo "Waiting for 15 minutes..."
    sleep 900

    echo "All scripts have been executed."
done
