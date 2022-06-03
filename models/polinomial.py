from copy import deepcopy

from models.field_polinomial import FieldPolinomial


class Polinomial:
    """Обычный многочлен (не из большого поля)"""

    def __init__(self, coeffs):
        self._coeffs = self.reduce_coeffs(deepcopy(coeffs))

    @property
    def coeffs(self):
        return deepcopy(self._coeffs)

    @property
    def degree(self):
        return len(self._coeffs) - 1

    def __add__(self, other):
        if isinstance(other, int):
            other = Polinomial([other])
        result = [0 for _ in range(max(len(self._coeffs), len(other.coeffs)))]
        for index in range(len(result)):
            result[index] = (self.coeffs[index] if len(self.coeffs) > index else 0) + \
                (other.coeffs[index] if len(other.coeffs) > index else 0)
        return Polinomial(result)

    def __mul__(self, other):
        if isinstance(other, int):
            other = Polinomial([other])
        result = []
        for j in range(len(self.coeffs)):
            for k in range(len(other.coeffs)):
                if len(result) <= j+k:
                    result.append(self.coeffs[j]*other.coeffs[k])
                else:
                    result[j+k] = result[j+k] + self.coeffs[j]*other.coeffs[k]
        return Polinomial(result)

    __radd__ = __add__
    __rmul__ = __mul__

    def __neg__(self):
        new_coeffs = self.coeffs
        for i in range(len(new_coeffs)):
            new_coeffs[i] = -new_coeffs[i]
        return Polinomial(new_coeffs)

    def reduce_coeffs(self, coeffs):
        if len(coeffs) == 0:
            return coeffs
        last_coeff = coeffs[-1]

        while len(coeffs) > 0 and ((isinstance(last_coeff, int) and last_coeff == 0) or (isinstance(last_coeff, FieldPolinomial) and last_coeff.coeffs == [])):
            coeffs.pop()
            if len(coeffs) > 0:
                last_coeff = coeffs[-1]
        return coeffs

    def of(self, field, argument):
        """Вычисляет значение многочлена для указанного аргумента"""
        result = FieldPolinomial(field, [0])
        for i in range(len(self.coeffs)):
            result = result + self.coeffs[i]*((argument)**i)
        return result
