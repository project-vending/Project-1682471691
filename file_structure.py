
import os

# Create the main project directory
if not os.path.exists('ecommerce_data_pipeline'):
    os.makedirs('ecommerce_data_pipeline')

# Create sub-directories for different stages of the data pipeline
directories = ['glue', 'athena', 'quicksight', 'streamlit']

for directory in directories:
    path = os.path.join('ecommerce_data_pipeline', directory)
    if not os.path.exists(path):
        os.makedirs(path)
        
        # Create empty files for each sub-directory
        open(os.path.join(path, '__init__.py'), 'a').close()
        open(os.path.join(path, f'{directory}.py'), 'a').close()
