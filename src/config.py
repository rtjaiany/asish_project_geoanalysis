import os
import re
import json

# ==========================================
# FILE PATHS
# ==========================================
# Set these to the paths on the Harvard HPC
RAW_DATA_DIR = "/n/holylabs/LABS/cga/Lab/data/geo-tweets/cga-sbg-tweets/"
OUTPUT_DIR = "data/processed/"
BBOX_FILE = "data/bboxes.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================================
# INCIDENTS & DATES
# ==========================================
# t0 = incident date
INCIDENTS = {
    "Uvalde, TX": "2022-05-24",
    "Highland Park, IL": "2022-07-04",
    "Monterey Park, CA": "2023-01-21",
    "Nashville, TN": "2023-03-27"
}

# ==========================================
# KEYWORDS & HASHTAGS
# ==========================================
HASHTAGS = [
    "#GunViolence", "#GunControl", "#GunReformNow", "#BanAssaultWeaponsNow", "#Parkland",
    "#SecondAmendment", "#2A", "#2ndAmendment", "#gunsafety", "#GunControlNow", "#ConcealedCarry",
    "#GunRights", "#NeverAgain", "#NRATerrorism", "#ProGun", "#NeverAlone", "#MarchForOurLives",
    "#OpenCarry", "#gunowners", "#GunDebate", "#FloridaShooting", "#massshooting",
    "#MentalHealthAwareness", "#SuicidePrevention", "#EndGunViolence", "#GunSense",
    "#GunSafetyNow", "#DisarmHate", "#StopGunViolence", "#GunViolencePrevention",
    "#SaveOurKids", "#EnoughIsEnough", "#StopTheViolence"
]

KEYWORDS = [
    # Core Keywords
    "gun violence", "mass shooting", "gun control", "gun deaths", "firearm fatalities",
    "shooting incident", "accidental shooting", "gun accident", "firearm ownership",
    "assault weapons", "gun policy", "active shooter", "gun rally", "shotgun", "rifle",
    "handgun", "automatic weapons", "concealed weapon", "mental health crisis",
    "suicide by firearm", "accidental death", "gun reform", "firearm injuries",
    "gun ban", "shooting prevention", "gun legislation", "open carry", "self-defense shooting",
    "background checks",
    # Emotional/Narrative
    "anger", "fear", "pain", "grief", "advocacy", "hate", "sadness", "rage", "blame",
    "cause", "responsibility",
    # Event-specific
    "Parkland shooting", "Sandy Hook", "Las Vegas shooting", "Orlando nightclub shooting",
    "school shooting", "massacre",
    # Socioeconomic (TREO paper)
    "income inequality", "education level", "poverty", "unemployment", "community violence",
    "neighborhood safety", "urban violence", "race and gun violence", "social isolation",
    "gang violence",
    # Predictive/Contextual
    "threat", "warning signs", "premeditated", "manifesto", "violent intentions",
    "planned attack", "threat assessment",
    # Policy and Advocacy
    "legislation", "gun registration", "universal background checks", "red flag laws",
    "gun safety legislation", "gun lobby", "firearm restriction", "buyback program",
    # Law Enforcement
    "law enforcement", "community policing", "violence prevention", "intervention",
    "risk assessment", "emergency response", "public safety", "crisis intervention",
    # Slang
    "strap", "heater", "gat", "piece", "pop off", "clap back", "drill", "spin the block",
    # Misc
    "active shooter drill", "lockdown", "gun show", "ammo shortage", "arms dealer",
    "illegal firearms", "3D-printed gun", "ghost gun"
]

# Compile regex pattern optimized for matching variations
# Lowercase hashtags without '#' for regex to catch both formats if needed
hashtag_words = [h.replace("#", "").lower() for h in HASHTAGS]
all_phrases = [k.lower() for k in KEYWORDS] + hashtag_words

# Remove duplicates
all_phrases = list(set(all_phrases))

# Create regex pattern for exact phrase match (with word boundaries)
escaped_phrases = [re.escape(phrase) for phrase in all_phrases]
REGEX_PATTERN = re.compile(
    r"\b(?:" + "|".join(escaped_phrases) + r")\b",
    flags=re.IGNORECASE
)

# Alternative regex just for hashtags
escaped_hashtags = [re.escape(h) for h in HASHTAGS]
HASHTAG_REGEX = re.compile(
    r"(?:" + "|".join(escaped_hashtags) + r")\b",
    flags=re.IGNORECASE
)
