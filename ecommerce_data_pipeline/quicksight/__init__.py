python
import os

# Create directory if it doesn't exist
if not os.path.exists('ecommerce_data_pipeline/quicksight'):
    os.makedirs('ecommerce_data_pipeline/quicksight')

# Create an empty __init__.py file
open('ecommerce_data_pipeline/quicksight/__init__.py', 'a').close()
