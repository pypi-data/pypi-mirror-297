import importlib.metadata
import logging
import rdkit

__all__ = ['core','ctydata','engine','io','jobs','models','qm','reaction_sampling']
__version__ = importlib.metadata.version('chemtrayzer')

logger = logging.getLogger("rdkit")
logger.propagate = True
# appending RDKit will help the user to distinguish what is coming from RDKit
logger.handlers[0].setFormatter(logging.Formatter('[RDKit]%(message)s'))
logger.setLevel(logging.DEBUG)      # everything will be forwarded by rdkit to the logger, and the logger can filter by setting loglevel
rdkit.rdBase.LogToPythonLogger()