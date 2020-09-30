import random
from winreg import *
import subprocess
import re

# generate random mac address
macVendorList = []
with open('mac-vendor.txt', 'r', encoding='utf-8') as f:
    macVendorList = [i.split('\t')[0] for i in f.readlines() if i.split('\t')[1] != 'Private\n']
macAddress = f'{random.choice(macVendorList)}%02X%02X%02X' % \
             (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


net = r'SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}'  # network reg addr

# find networks
res = subprocess.check_output('wmic nic where netenabled=true get netconnectionID,index')
networkList = [re.split(r'\s{2,}', i)[:-1] for i in res.decode('euc-kr').split('\r\r\n')][1:-2]
for i in range(len(networkList)):
    networkList[i][0] = networkList[i][0].zfill(4)

# select network
print('What network are you going to change?')
for i, v in enumerate(networkList):
    print(f'{i + 1}. {v[1]}')
select = int(input('>>')) - 1

# change or create registry
lanKey = CreateKey(HKEY_LOCAL_MACHINE, net + '\\' + networkList[select][0])
SetValueEx(lanKey, 'NetworkAddress', 0, REG_SZ, macAddress)

# close keys
CloseKey(lanKey)

# mac address change apply
subprocess.run(f'netsh interface set interface name="{networkList[select][1]}" admin="disabled"')
subprocess.run(f'netsh interface set interface name="{networkList[select][1]}" admin="enabled"')
