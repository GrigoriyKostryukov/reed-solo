
import sys
from models.field_polinomial import FieldPolinomial
from models.field import Field
from models.polinomial import Polinomial
from models.reed_solomon import ReedSolomon
field = Field()

reed_solo = ReedSolomon(field, 3, 5)

"""vector = Polinomial([
    FieldPolinomial(field, [0, 0, 0]),
    FieldPolinomial(field, [1, 1, 0]),
]
)
v = Polinomial([
    FieldPolinomial(field, [1, 0, 1]),
    FieldPolinomial(field, [1, 0, 1]),
    FieldPolinomial(field, [1, 0, 0]),
    FieldPolinomial(field, [1, 0, 1])
]
)

reed_solo.decode(v)"""

def to_field_poli(field, sequence):
    coeffs = []
    for chr in sequence:
        coeff = int(chr)
        coeffs.append(coeff)
    return FieldPolinomial(field, list(reversed(coeffs)))

filename = sys.argv[1]

with open(filename, 'r', encoding='UTF-8') as file:
    lines = file.readlines()
    vector = list(reversed(list(lines[1].split())))
    for i in range(len(vector)):
        vector[i] = to_field_poli(field, vector[i])
    if int(lines[0]) == 0:
        pol = reed_solo.encode(Polinomial(vector))
        print(list(reversed(pol.coeffs)))
    else:
        print("ПРИНЯТЫЙ ВЕКТОР:")
        print(list(reversed(vector)))
        pol, error = reed_solo.decode(Polinomial(vector))

        print("ИСПРАВЛЕННЫЙ ВЕКТОР:")
        print(list(reversed(pol.coeffs)))

        print("ОШИБКА:")
        print(list(reversed(error.coeffs)))

    
        

