# Gun Violence Twitter Forecasting

This project analyzes Twitter data to forecast and map discussions around gun violence. It specifically focuses on four mass shooting incidents, capturing social media reactions over a 5-day window ($\pm 2$ days) around each event, within the respective geographic bounding boxes.

## Setup Instructions

1. **Environment Setup:**
   Ensure you have Python 3.9+ installed. You can install the required dependencies using:
   ```bash
   pip install -r requirements.txt
   ```

2. **Bounding Boxes Collection:**
   Run the `collect_bboxes.py` script to fetch the bounding boxes for the target cities using OpenStreetMap's Nominatim API. This will generate a `bboxes.json` file in the `data/` directory.
   ```bash
   python src/collect_bboxes.py
   ```

3. **Data Configuration:**
   Review `src/config.py` and adjust the `RAW_DATA_DIR` and `OUTPUT_DIR` paths to match the structure on your local machine or the Harvard FASRC cluster.

4. **Running the Pipeline (Harvard HPC):**
   A sample SLURM script is provided in `scripts/run_pipeline.sh`. To submit the pipeline to the cluster:
   ```bash
   sbatch scripts/run_pipeline.sh
   ```

5. **Analysis:**
   After the pipeline completes, run the Jupyter Notebook in `notebooks/01_descriptive_analysis.ipynb` to visualize the filtered data.
