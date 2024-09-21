"""Logger module."""
# Copyright Gemeente Rotterdam - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import logging
import sys

log_format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream=sys.stdout, filemode="w", format=log_format, level=logging.INFO)

logger = logging.getLogger("azure")
logger.setLevel(logging.INFO)
