from copy import copy


class FieldPolinomial:
    """Многочлен поля"""

    def __init__(self, field, coeffs):
        self.field = field
        self._coeffs = self.reduce_coeffs(copy(coeffs))

    @property
    def coeffs(self):
        return copy(self._coeffs)

    @property
    def degree(self):
        return len(self._coeffs) - 1

    def __add__(self, other):
        if isinstance(other, int):
            other = FieldPolinomial(self.field, [other])
        result = [0 for _ in range(max(len(self._coeffs), len(other.coeffs)))]
        for index in range(len(result)):
            result[index] = (self.coeffs[index] if len(self.coeffs) > index else 0) + \
                (other.coeffs[index] if len(other.coeffs) > index else 0)
        return FieldPolinomial(self.field, result)

    def __mul__(self, other):
        if isinstance(other, int):
            other = FieldPolinomial(self.field, [other])
        if self.coeffs == [] or other.coeffs == []:
            return FieldPolinomial(self.field, [])
        power1 = self.field.power_by_polinomial(self)
        power2 = self.field.power_by_polinomial(other)
        result_power = power1 + power2
        result_polonomial = self.field.polinomial_by_power(result_power)
        return FieldPolinomial(self.field, result_polonomial.coeffs)

    def __truediv__(self, other):
        if isinstance(other, int):
            other = FieldPolinomial(self.field, [other])
        if self.coeffs == [] or other.coeffs == []:
            return FieldPolinomial(self.field, [])
        power1 = self.field.power_by_polinomial(self)
        power2 = self.field.power_by_polinomial(other)
        result_power = power1 - power2
        result_polonomial = self.field.polinomial_by_power(result_power)
        return FieldPolinomial(self.field, result_polonomial.coeffs)

    def __rtruediv__(self, other):
        if isinstance(other, int):
            other = FieldPolinomial(self.field, [other])
        if self.coeffs == [] or other.coeffs == []:
            return FieldPolinomial(self.field, [])
        power2 = self.field.power_by_polinomial(self)
        power1 = self.field.power_by_polinomial(other)
        result_power = power1 - power2
        result_polonomial = self.field.polinomial_by_power(result_power)
        return FieldPolinomial(self.field, result_polonomial.coeffs)

    def __pow__(self, power):
        result = FieldPolinomial(self.field, [1])
        for _ in range(power):
            result = result * self
        return result

    __radd__ = __add__
    __rmul__ = __mul__

    def __repr__(self) -> str:
        st = ""
        if len(self.coeffs) == 0:
            return "0"
            
        for i in range(self.degree, -1, -1):
            if self._coeffs[i] != 0:
                if not len(st) == 0:
                    st += " + "
                if i == 0:
                    st += f"{self._coeffs[i]}"
                elif i == 1:
                    st += f"{'' if self._coeffs[i] == 1  else self._coeffs[i]}x"
                else:
                    st += f"{'' if self._coeffs[i] == 1  else self._coeffs[i]}x^{i}"
        return st

    def __eq__(self, other):
        if self.degree != other.degree:
            return False
        for i in range(len(self._coeffs)):
            if self._coeffs[i] != other.coeffs[i]:
                return False
        return True

    def __neg__(self):
        new_coeffs = self.coeffs
        for i in range(len(new_coeffs)):
            new_coeffs[i] = (-new_coeffs[i] +
                             self.field.MODULUS) % self.field.MODULUS
        return FieldPolinomial(self.field, new_coeffs)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return (-self) + (other)

    def reduce_coeffs(self, coeffs):
        if len(coeffs) == 0:
            return coeffs
        modulus = self.field.MODULUS
        for i in range(len(coeffs)):
            coeffs[i] %= modulus
        last_coeff = coeffs[-1]

        while len(coeffs) > 0 and last_coeff == 0:
            coeffs.pop()
            if len(coeffs) > 0:
                last_coeff = coeffs[-1]
        return coeffs
