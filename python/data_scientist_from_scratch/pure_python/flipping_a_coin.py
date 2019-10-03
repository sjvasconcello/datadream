# Flipping a coin - Hypothesis and Inference - Chapter 7

import math
import random
from typing import Tuple

SQRT_TWO_PI = math.sqrt(2 * math.pi)


def normal_cdf(x, mu=0, sigma=1):
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2


def inverse_normal_cdf(p, mu=0, sigma=1, tolerance=0.00001):
    """find approximate inverse using binary search"""

    # if not standard, compute standard and rescale
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)

    low_z, low_p = -10.0, 0            # normal_cdf(-10) is (very close to) 0
    hi_z,  hi_p = 10.0, 1            # normal_cdf(10)  is (very close to) 1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2     # consider the midpoint
        mid_p = normal_cdf(mid_z)      # and the cdf's value there
        if mid_p < p:
            # midpoint is still too low, search above it
            low_z, low_p = mid_z, mid_p
        elif mid_p > p:
            # midpoint is still too high, search below it
            hi_z, hi_p = mid_z, mid_p
        else:
            break

    return mid_z


def normal_approximation_to_binomial(n: int, p: float) -> Tuple[float, float]:
    # Retorna mu y sigma correspondiente a Binomina(n,p)
    mu = p * n
    sigma = math.sqrt(p * (1 - p) * n)
    return mu, sigma


# Usamos funcion de distribucion cuando la probabilidad de que la
# variable esté por debajo de un umbral
normal_probability_below = normal_cdf

# Cuando está por encima del umbral si no está por debajo del umbral


def normal_probability_above(lo: float,
                             hi: float,
                             mu: float = 0,
                             sigma: float = 1) -> float:
    """ La probabilidad que un N(mu, sigma) es mayor que lo """
    return 1 - normal_cdf(lo, mu, sigma)

# Cuando está por bajo del hi pero no menos que lo


def normal_probability_between(lo: float,
                               hi: float,
                               mu: float = 0,
                               sigma: float = 1) -> float:
    """ La probabilidad que un N(mu, sigma) esta en medio de lo y hi """
    return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)

# Cuando está por encima y no entre medio


def normal_probability_outside(lo: float,
                               hi: float,
                               mu: float = 0,
                               sigma: float = 1) -> float:
    """ La probabilidad que un N(mu, sigma) es mayor que lo """
    return 1 - normal_probability_between(lo, hi, mu, sigma)


def normal_upper_bound(probability: float,
                       mu: float = 0,
                       sigma: float = 1) -> float:
    """ Retorna devolver la z para la cual P(z <= z) = probability"""
    return inverse_normal_cdf(probability, mu, sigma)


def normal_lower_bound(probability: float,
                       mu: float = 0,
                       sigma: float = 1) -> float:
    return inverse_normal_cdf(1 - probability, mu, sigma)


def normal_two_sided_bounds(probability: float,
                            mu: float = 0,
                            sigma: float = 1) -> Tuple[float, float]:
    tail_probability = (1 - probability) / 2

    upper_bound = normal_lower_bound(tail_probability, mu, sigma)

    lower_bound = normal_upper_bound(tail_probability, mu, sigma)

    return lower_bound, upper_bound

# 3


mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)

# Lanzamos los 1000 veces, si nuestra hipotesis es correcta
# Con promedio 500 y su desviacion estadar es 15.8

print(mu_0, "Mu_0")
print(sigma_0, "Sigma_0")
print("--------------------------------------------")

lower_bound, upper_bound = normal_two_sided_bounds(0.95, mu_0, sigma_0)

print(lower_bound, "Lower Bound")
print(upper_bound, "Upper Bound")
print("--------------------------------------------")


# p-Values


def two_sided_p_value(x, mu=0, sigma=1):
    if x >= mu:
        # if x is greater than the mean, the tail is above x
        return 2 * normal_probability_above(x, mu, sigma)
    else:
        # if x is less than the mean, the tail is below x
        return 2 * normal_probability_below(x, mu, sigma)


print("--------------------------------------------")
print("p-Values ")

p_values = two_sided_p_value(529.5, 500, 15.811)

print(p_values)

extreme_value_count = 0
for _ in range(1000):
    num_heads = sum(1 if random.random() < 0.5 else 0 for _ in range(1000))
    if num_heads >= 530 or num_heads <= 470:
        extreme_value_count += 1


print("--------------------------------------------")
print("1000 flips, p-Values ")
print(extreme_value_count)
