import numpy as np
import scipy.special as spsp

class MathConsts:
    """

    References:
        https://github.com/lattera/glibc/blob/master/math/math.h
    """

    M_E         = 2.7182818284590452354   # e
    M_LOG2E     = 1.4426950408889634074   # log_2 e
    M_LOG10E    = 0.43429448190325182765  # log_10 e
    M_LN2       = 0.69314718055994530942  # log_e 2
    M_LN10      = 2.30258509299404568402  # log_e 10
    M_PI        = 3.14159265358979323846  # pi
    M_PI_2      = 1.57079632679489661923  # pi/2
    M_PI_4      = 0.78539816339744830962  # pi/4
    M_1_PI      = 0.31830988618379067154  # 1/pi
    M_2_PI      = 0.63661977236758134308  # 2/pi
    M_2_SQRTPI  = 1.12837916709551257390  # 2/sqrt(pi)
    M_SQRT2     = 1.41421356237309504880  # sqrt(2)
    M_SQRT1_2   = 0.70710678118654752440  # 1/sqrt(2)

    # values below are from https://keisan.casio.com/calculator
    M_SQRT2PI   = 2.506628274631000502416  # sqrt(2pi)
    M_1_SQRT2PI = 0.3989422804014326779399  # 1/sqrt(2pi)
    M_SQRT_PI_2 = 1.253314137315500251208  # sqrt(pi/2)
    M_LN2PI_2   = 0.9189385332046727417803  # log(sqrt(2pi)) = log(2pi)/2


class MathFuncs:

    @staticmethod
    def mills_ratio(x):
        """
        Mills Ratio: R(x) = N(-x)/n(x) = sqrt(pi/2) erfcx(x/sqrt(2))

        Args:
            x: argument

        Returns:

        """
        return MathConsts.M_SQRT_PI_2 * spsp.erfcx(x * MathConsts.M_SQRT1_2)

    @staticmethod
    def avg_exp(x):
        """
        Integral_0^x exp(x) dx / x = ( exp(x) - 1 ) / x

        Args:
            x: argument

        Returns:
            value
        """

        rv = np.ones_like(x, dtype=float)
        np.divide(np.expm1(x),  x, out=rv, where=(x != 0.0))
        return rv

    @staticmethod
    def avg_inv(x):
        """
        [Integarl 1/x from 1 to 1+x] / x = log(1+x) / x

        Args:
            x: argument

        Returns:

        """
        assert np.all(x > -1.0)

        rv = np.ones_like(x, dtype=float)
        np.divide(np.log1p(x),  x, out=rv, where=(x != 0.0))
        return rv

    @staticmethod
    def avg_pow(x, a):
        """
        (int from 1 to (1+x) t^a dt) / x
            = 1/(1+a) * ((1+x)^(1+a) - 1) / x

        Args:
            x: argument
            a: exponent

        Returns:

        """

        assert np.all(x > -1.0)
        a1p = 1.0 + a
        rv = np.ones(np.broadcast_shapes(np.shape(a1p), np.shape(x)), dtype=float)
        np.divide(np.expm1(a1p * np.log1p(x)),  a1p * x, out=rv, where=(x != 0.0) & (a1p != 0.0))
        np.divide(np.log1p(x),  x, out=rv, where=(x != 0.0) & (a1p == 0.0))

        return rv
