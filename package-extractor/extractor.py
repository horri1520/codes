r = open('./requirements.txt', 'r')
packages = r.readlines()
for i in packages:
    package = i.split('=')
    print('- {}'.format(package[0]))