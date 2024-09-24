from spacr.version import version, version_str
import logging
import torch

from . import core
from . import io
from . import utils
from . import settings
from . import plot
from . import measure
from . import sim
from . import sequencing
from . import timelapse
from . import deep_spacr
from . import app_annotate
from . import gui_utils
from . import gui_elements
from . import gui_core
from . import gui
from . import app_make_masks
from . import app_mask
from . import app_measure
from . import app_classify
from . import app_sequencing
from . import app_umap
from . import mediar
from . import logger

__all__ = [
    "core",
    "io",
    "utils",
    "settings",
    "plot",
    "measure",
    "sim",
    "sequencing",
    "timelapse",
    "deep_spacr",
    "app_annotate",
    "gui_utils",
    "gui_elements",
    "gui_core",
    "gui",
    "app_make_masks",
    "app_mask",
    "app_measure",
    "app_classify",
    "app_sequencing",
    "app_umap",
    "mediar",
    "logger"
]

logging.basicConfig(filename='spacr.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')
