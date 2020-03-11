with open('requirements.txt', 'r') as log:
    loglines = 0
    for line in log:
        loglines += 1
f = open('requirements.txt', 'r')
lib = f.readlines()
for i in range(loglines):
    Lib = lib[i].split("==")
    print(Lib[0])