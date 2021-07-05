string = ''
period = 7
frequency = 3.1415926535 / ( period / 2 )

for i in range(30):
    string += f'sin({i*period}x)+'

print(string + '\n' + str(frequency))