import logging
import os
import sys

from dotenv import find_dotenv
from dotenv import load_dotenv

from interactions_update.job import run

# 1. Setup Logging
# Format for Google Cloud Logs compatibility (JSON-like or clear text)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


def main():
    """Entry point for the Job."""
    try:
        # 2. Load Environment Variables
        # This will look for a .env file if it exists (useful for local dev)
        env_file = find_dotenv()
        if env_file:
            logger.info(f"Loading environment from {env_file}")
            load_dotenv(env_file)

        logger.info("Starting Interactions Update Job...")

        # 3. Execute the Job
        # We pass the MAX_WORKERS env var into the run function
        workers = int(os.getenv("MAX_WORKERS", "10"))
        run(max_workers=workers)

        logger.info("Job completed successfully.")
        sys.exit(0)

    except Exception as e:
        logger.error(f"Critical failure in main: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
