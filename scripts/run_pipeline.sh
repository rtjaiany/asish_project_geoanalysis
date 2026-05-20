#!/bin/bash
#SBATCH -J gun_violence_twitter_pipeline
#SBATCH -o out_%j.log
#SBATCH -e err_%j.log
#SBATCH -p shared
#SBATCH -n 20
#SBATCH -t 06:00:00
#SBATCH --mem=64G

module purge
module load python/3.10.13-fasrc01

# Collect bounding boxes if not already done
python src/collect_bboxes.py

# Run location and date filter
python src/filter_locations_dates.py

# Run keyword filter
python src/filter_keywords.py

echo "Pipeline finished!"
