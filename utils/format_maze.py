llist = list()
i=" "
while i:
    i=input("Line: ")
    llist.append(i)

for i in llist:
    i = i.replace("+", "█")
    i = i.replace("-", "█")
    i = i.replace("|", "█")
    print(i)
print("""██                █████ Press any arrow key to move. █████                 ██
█                    ██ ⥉ = Key, ‖ = Gate, ⊙ = Coin  ██                     █""")
