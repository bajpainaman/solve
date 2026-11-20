import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: Allocate

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Sum(xs):
        d_0___accumulator_ = 0
        while True:
            with _dafny.label():
                if (len(xs)) == (0):
                    return (0) + (d_0___accumulator_)
                elif True:
                    d_0___accumulator_ = (d_0___accumulator_) + ((xs)[0])
                    in0_ = _dafny.SeqWithoutIsStrInference((xs)[1::])
                    xs = in0_
                    raise _dafny.TailCall()
                break

    @staticmethod
    def Split(total, n):
        parts: _dafny.Seq = _dafny.Seq({})
        d_0_share_: int
        d_0_share_ = _dafny.euclidian_division(total, n)
        d_1_leftover_: int
        d_1_leftover_ = _dafny.euclidian_modulus(total, n)
        parts = _dafny.SeqWithoutIsStrInference([d_0_share_ for d_2___v0_ in range(n)])
        d_3_i_: int
        d_3_i_ = 0
        while (d_3_i_) < (d_1_leftover_):
            parts = (parts).set(d_3_i_, ((parts)[d_3_i_]) + (1))
            d_3_i_ = (d_3_i_) + (1)
        return parts

