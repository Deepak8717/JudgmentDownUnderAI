import pandas as pd
raw_data_path = 'C:\\code\\legal_case_classification_model\\data\\raw_data\\legal_text_classification.csv'
processed_data_path = 'C:\\code\\legal_case_classification_model\\data\\processed\\processed_legal_cases.csv'

try:
    raw_data = pd.read_csv(raw_data_path)
    print("Successfully read in data.")
except Exception as e:
    print(f"Failed to read in data: {e}")
  


try:
    raw_data.to_csv(processed_data_path, index=False)
    print("Successfully wrote to output file.")
except Exception as e:
    print(f"Failed to write to output file: {e}")

    
          

