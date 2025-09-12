import math

def sin(x):
    return math.sin(x)

def PerlinNoise(x):
    return (
        sin(x) +
        1.00 * sin(2 * x) +
        0.75 * sin(4 * x) +
        0.50 * sin(6 * x) +
        0.25 * sin(8 * x)
    )

def Random(seed):
    x = 389856
    y = 690187
    a = 1
    b = 32
    F1 = (x * seed + y) / (2**16)
    F2 = (a + F1) / (b - a + 1)
    result = (F1 + F2)
    return result

number = Random(1)

number_int = int(number * 100000000 + 0.1)
number_str = str(number_int).zfill(8)
digit_list = [int(char) for char in number_str]

print("Sayı:", number)
print("Dizi:", digit_list)
