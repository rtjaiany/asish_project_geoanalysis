# Asish's Project - Twitter Geoanalysis

This project analyzes Twitter data to forecast and map discussions around gun violence. It specifically focuses on four mass shooting incidents, capturing social media reactions over a 5-day window ($\pm 2$ days) around each event, within the respective geographic bounding boxes.

## Setup Instructions

1. **Environment Setup:**
   Ensure you have Python 3.9+ installed. You can install the required dependencies using:
   ```bash
   pip install -r requirements.txt
   ```

2. **Data Pipeline:**
   The entire data processing pipeline (configuration, bounding box collection, spatial/temporal filtering, and keyword filtering) has been consolidated into a single Jupyter Notebook. Open Jupyter Lab and run:
   ```bash
   jupyter lab notebooks/data_processing_pipeline.ipynb
   ```
   Adjust the `RAW_DATA_DIR` and `OUTPUT_DIR` variables in the first configuration cell to match the structure on your local machine or the Harvard FASRC cluster. Then, run all cells to execute the pipeline.

3. **Analysis:**
   After the pipeline completes, run the descriptive analysis notebook to visualize the filtered data.
