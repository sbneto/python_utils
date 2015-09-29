__author__ = 'Samuel'

import numpy as np
import json


class NumpyEncoder(json.JSONEncoder):
    """ <cropped for brevity> """
    def default(self, obj):
        if isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
