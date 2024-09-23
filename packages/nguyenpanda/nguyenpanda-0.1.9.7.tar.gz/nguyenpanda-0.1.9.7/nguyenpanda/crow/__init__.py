"""
`crow` is a utility package designed to streamline the process of working
on Machine Learning (ML) and Deep Learning (DL) projects within Jupyter notebooks.
It provides a set of convenient functions to help manage datasets, directories,
and other common tasks that are essential in a typical ML/DL workflow.
"""

from .dataset import Dataset
from .exception import InvalidKaggleAPI, KaggleAuthenticationFailed
from .google_colab import GoogleColabUtils, gc_utils, gcu
from .jupyter_notebook import NoteBookUtils, nb_utils, nbu
from .plotting import plot_train_test_loss_accuracy

__all__ = [
    'Dataset',
    'InvalidKaggleAPI', 'KaggleAuthenticationFailed',
    'GoogleColabUtils', 'gc_utils', 'gcu',
    'NoteBookUtils', 'nb_utils', 'nbu',
    'plot_train_test_loss_accuracy',
]
