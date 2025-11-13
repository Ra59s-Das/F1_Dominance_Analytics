import logging
from helper_functions import load_csv, save_csv, ensure_dir
import subprocess
import os

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# -------------------------
# PATH CONFIG
# -------------------------
DATA_DIR = "data"
OUTPUT_DIR = "output"

TEAM_METRICS_PATH = f"{OUTPUT_DIR}/processed/team_metrics.csv"
TDI_PATH = f"{OUTPUT_DIR}/processed/team_tdi.csv"

# -------------------------
# STEP EXECUTION WRAPPER
# -------------------------

def run_step(script_name):
    logging.info(f"\n🚀 Running {script_name} ...")
    result = subprocess.run(["python", script_name], capture_output=True, text=True)

    if result.returncode == 0:
        logging.info(f"✅ Completed: {script_name}")
    else:
        logging.error(f"❌ Error in {script_name}")
        logging.error(result.stderr)


# -------------------------
# MAIN PIPELINE
# -------------------------
def main():

    logging.info("\n===============================")
    logging.info("      F1 DOMINANCE PIPELINE     ")
    logging.info("===============================\n")

    # Ensure output folders exist
    ensure_dir(f"{OUTPUT_DIR}/processed")
    ensure_dir(f"{OUTPUT_DIR}/visuals")

    # Run sequential scripts
    run_step("01_load_and_clean_data.py")
    run_step("02_compute_team_metrics.py")
    run_step("03_compute_tdi.py")
    run_step("04_visualize_dominance.py")

    logging.info("\n🎉 Pipeline finished successfully!")
    logging.info(f"📁 Metrics saved to: {TEAM_METRICS_PATH}")
    logging.info(f"📁 TDI saved to: {TDI_PATH}")
    logging.info("\nAll visuals stored in /output/visuals")

if __name__ == "__main__":
    main()
