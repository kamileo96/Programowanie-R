import re

with open('checkme.txt', 'r', encoding='utf-8') as f:
    txt =str(f.read())
    sr = '[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]*[bpgkhjwtdBPGKHJWTD]ż[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]*'
    xs = re.findall(sr,txt)
    for x in xs:
        print('Czy chcesz zamienić ż na rz w słowie: "'+x+'"')
        ipt = input()
        b = False
        if(ipt=='T'): b = True
        if b:
            txt #unfinished
        
    print(xs)