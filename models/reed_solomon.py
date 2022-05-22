from dataclasses import field
from models.field import Field
from models.field_polinomial import FieldPolinomial
from models.polinomial import Polinomial


class ReedSolomon:
    def __init__(self, field: Field, j0, t):
        self.field = field
        self.j0 = j0
        self.t = t
        self.generator_polinomial = self.create_generator_polinomial()

    def create_generator_polinomial(self):
        pol = [1]
        for i in range(self.j0, self.j0+2*self.t):
            current_alpha = self.field.polinomial_by_power(i)
            min_polimomial = [-current_alpha, 1]
            current_result = []
            for j in range(len(pol)):
                for k in range(len(min_polimomial)):
                    if len(current_result) <= j+k:
                        current_result.append(pol[j]*min_polimomial[k])
                    else:
                        current_result[j+k] = current_result[j +
                                                             k] + pol[j]*min_polimomial[k]
            pol = current_result
        return Polinomial(pol)

    def encode(self, vector):
        return vector * self.generator_polinomial

    def syndromes(self, vector):
        syndromes = []
        for i in range(self.j0, self.j0 + 2*self.t):
            alpha = self.field.polinomial_by_power(i)
            syndrome = vector.of(self.field, alpha)
            #print(syndrome.coeffs)
            syndromes.append(syndrome)
        return syndromes

    def M(self, nu, syndromes):
        matrix = [[FieldPolinomial(self.field, [])
                   for i in range(nu)] for j in range(nu)]
        for i in range(nu):
            for j in range(nu):
                matrix[i][j] = syndromes[i+j]

        if nu == 1:
            return matrix

        if self.determinant(matrix) == FieldPolinomial(self.field, [0]):
            return self.M(nu - 1, syndromes)
        return matrix

    def lambdas(self, inversed_m, syndromes, nu):
        s = [[-syndromes[i]] for i in range(nu, 2*nu)]
        product = self.matmult(inversed_m, s)
        return list(reversed([row[0] for row in product]))

    def locator_polinomial(self, lambdas):
        coeffs = [FieldPolinomial(self.field, [1])] + lambdas
        return Polinomial(coeffs)

    def error_indices(self, locator_polinomial: Polinomial):
        indices = []
        coeffs = []
        for i in range(len(self.field.items)):
            value = locator_polinomial.of(self.field, self.field.items[i])
            if value == FieldPolinomial(self.field, [0]):
                coeffs.append(FieldPolinomial(self.field, [1]) / self.field.items[i])
                indices.append(len(self.field.items) - i - 1)
        return coeffs, indices

    def error_values(self, coeffs, syndromes):
        matrix = []
        for i in range(len(coeffs)):
            matrix.append([coeff**(i+self.j0) for coeff in coeffs])
        inverse_m = self.invert_matrix(matrix)
        s  = [[syndromes[i]] for i in range(len(coeffs))]
        product = self.matmult(inverse_m, s)
        return list([row[0] for row in product])
    
    def error_polinomial(self, error_values, error_indices):
        if len(error_indices) == 0:
            return Polinomial([])
        coeffs = [FieldPolinomial(self.field, [0]) for i in range(max(error_indices) + 1)]
        for i in range(len(error_indices)):
            coeffs[error_indices[i]] = error_values[i]
        return Polinomial(coeffs)


    def decode(self, vector):
        syndromes = self.syndromes(vector)
        matrix = self.M(self.t, syndromes)
        inverse = self.invert_matrix(matrix)
        lambdas = self.lambdas(inverse, syndromes, len(inverse))
        locator = self.locator_polinomial(lambdas)
        coeffs, indices = self.error_indices(locator)
        err_values = self.error_values(coeffs, syndromes)
        error_polinomial = self.error_polinomial(err_values, indices)
        #print(error_polinomial)
        return (vector + (-error_polinomial)), error_polinomial
        

    

    def invert_matrix(self, matrix):
        identity_matrix = [[FieldPolinomial(self.field, []) for _ in range(
            len(matrix))] for __ in range(len(matrix))]

        for i in range(len(matrix)):
            identity_matrix[i][i] = FieldPolinomial(self.field, [1])

        for fd in range(len(matrix)):
            fdScaler = FieldPolinomial(self.field, [1]) / matrix[fd][fd]
            for j in range(len(matrix)):
                matrix[fd][j] *= fdScaler
                identity_matrix[fd][j] *= fdScaler
            for i in list(range(len(matrix)))[0:fd] + list(range(len(matrix)))[fd+1:]:
                crScaler = matrix[i][fd]
                for j in range(len(matrix)):
                    matrix[i][j] = matrix[i][j] - crScaler * matrix[fd][j]
                    identity_matrix[i][j] = identity_matrix[i][j] - \
                        crScaler * identity_matrix[fd][j]
        return identity_matrix

    def determinant(self, A):
        total = FieldPolinomial(self.field, [])
        indices = list(range(len(A)))

        if len(A) == 1 and len(A[0]) == 1:
            return A[0][0]

        if len(A) == 2 and len(A[0]) == 2:
            val = A[0][0] * A[1][1] - A[1][0] * A[0][1]
            return val

        for fc in indices:
            As = [[FieldPolinomial(self.field, A[i][j].coeffs)
                   for i in range(len(A))] for j in range(len(A))]
            As = As[1:]
            height = len(As)

            for i in range(height):
                As[i] = As[i][0:fc] + As[i][fc+1:]

            sign = (-1) ** (fc % 2)
            sub_det = self.determinant(As)
            total += sign * A[0][fc] * sub_det

        return total

    def matmult(self, a, b):
        zip_b = zip(*b)
        zip_b = list(zip_b)
        return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b))
                 for col_b in zip_b] for row_a in a]
