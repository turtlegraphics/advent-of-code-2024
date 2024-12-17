def theprog(init):
    A = init
    B = 0
    C = 0

    while A != 0:
        B = A % 8
        B = B ^ 5
        C = A // pow(2,B)
        B = B ^ 6
        A = A // 3
        B = B ^ C
        print(f"  {B%8:b}")

for i in range(5):
    print('i:',i)
    theprog(i)
