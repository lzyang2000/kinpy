from typing import Any, Optional
import numpy as np
import scipy.optimize as sco

from . import transform


def inverse_kinematics(serial_chain: Any, pose: transform.Transform, initial_state: Optional[np.ndarray] = None) -> np.ndarray:
    ndim = len(serial_chain.get_joint_parameter_names())
    if initial_state is None:
        x0 = np.zeros(ndim)
    else:
        x0 = initial_state

    def object_fn(x):
        tf = serial_chain.forward_kinematics(x)
        obj = np.square(np.linalg.lstsq(pose.matrix(), tf.matrix(), rcond=-1)[0] - np.identity(4)).sum()
        return obj

    ret = sco.minimize(object_fn, x0, method='BFGS')
    return ret.x