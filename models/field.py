from models.field_polinomial import FieldPolinomial


class Field:

    # 5^3
    GENERATOR_POLINOMIAL = [2, 3, 0, 1]
    MODULUS = 5
    POWER = 3
    
    # 3^2
    #GENERATOR_POLINOMIAL = [2, 2, 1]
    #MODULUS = 3
    #POWER = 2

    # 2^4
    #GENERATOR_POLINOMIAL = [1, 1, 0, 0, 1]
    #MODULUS = 2
    #POWER = 4

    def __init__(self):

        self.polinomial_miltipliers = self.generate_polinomial_miltipliers()
        self.items = []
        alpha = FieldPolinomial(self, [0, 1])
        self.items.append(alpha)

        for i in range(2, (self.MODULUS)**self.POWER):
            previous_item = self.items[i-2]
            item_coeffs = previous_item.coeffs
            item_coeffs.insert(0, 0)
            if len(item_coeffs) > self.POWER and item_coeffs[self.POWER] != 0:
                complimentary = self.get_complimentary_polinomial(item_coeffs)
                for j in range(len(item_coeffs)):
                    item_coeffs[j] = (
                        item_coeffs[j] + complimentary[j]) % self.MODULUS
            item = FieldPolinomial(self, item_coeffs)
            #print(f"aplha^{i} : {item}")
            self.items.append(item)

    def generate_polinomial_miltipliers(self):
        polinomial_miltipliers = {}
        polinomial_miltipliers[self.GENERATOR_POLINOMIAL[-1]
                               ] = self.GENERATOR_POLINOMIAL

        for i in range(2, self.MODULUS):
            multiplier = self.GENERATOR_POLINOMIAL[:]
            for j in range(len(multiplier)):
                multiplier[j] = self.GENERATOR_POLINOMIAL[j]*i % self.MODULUS
            polinomial_miltipliers[multiplier[-1]] = multiplier
        return polinomial_miltipliers

    def power_by_polinomial(self, polinomial):
        for i in range(len(self.items)):
            if self.items[i] == polinomial:
                return (i+1) % (self.MODULUS**self.POWER - 1)

    def polinomial_by_power(self, power):
        return self.items[(power - 1 + self.MODULUS**self.POWER - 1) % (self.MODULUS**self.POWER - 1)]

    def get_complimentary_polinomial(self, coeffs):
        leadig_coeff = coeffs[self.POWER]
        return self.polinomial_miltipliers[self.MODULUS - leadig_coeff]
