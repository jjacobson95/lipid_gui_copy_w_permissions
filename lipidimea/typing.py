"""
lipidimea/typing.py

Dylan Ross (dylan.ross@pnnl.gov)

    type annotations for use across this package
"""


from typing import Union, Tuple, Optional
import sqlite3

import numpy as np
import numpy.typing as npt
from mzapy.dda import MsmsReaderDda, MsmsReaderDdaCachedMs1
<<<<<<< HEAD

=======
>>>>>>> 4dae6eb847eafffa6f03ccbed2ce80569b9e7180

# TODO (Dylan Ross): add some descriptions for all of these

type MzaFilePath = str

type ResultsDbPath = str
type ResultsDbConnection = sqlite3.Connection
type ResultsDbCursor = sqlite3.Cursor

type YamlFilePath = str

type Xic = Tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]
type Atd = Tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]
type Ms1 = Tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]
type Ms2 = Tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]
type Spec = Union[Ms1, Ms2]
type SpecStr = str

<<<<<<< HEAD
type DdaReader = Union[MsmsReaderDda, MsmsReaderDdaCachedMs1] 
type DdaChromFeat = Tuple[float, float, float, float, float]
type DdaFeature = Tuple[None, MzaFilePath, float, float, float, float, float, int, Optional[int], Optional[str]]
=======
type MzaFileId = int
# (, , , , , , , ,)
type DdaPrecursor = Tuple[None, MzaFileId, float, float, float, float, float, int, Optional[int]]
>>>>>>> 4dae6eb847eafffa6f03ccbed2ce80569b9e7180

type DdaReader = Union[MsmsReaderDda, MsmsReaderDdaCachedMs1]
# (, , , ,)
type DdaChromFeat = Tuple[float, float, float, float, float]

# (, , , ,)
type DiaDeconFragment = Tuple[float, Xic, float, Atd, float]

# (LMID_prefix, lipid_name, sum_c, sum_u, n_chains, adduct, mz)
type ScdbLipidId = Tuple[str, str, int, int, int, str, float]
