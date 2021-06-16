import telnetlib
from library.telnet.telnet import *

print("===============================================")



##################
##################
tn = user_login(host=host, port=port, password=password)
tn.write(b"get vswr\n")
tn.read_until(b"get vswr", timeout=5)
tn.write(b"exit\n")

result = tn.read_all().decode('ascii')
item_list = result.split('\r\n')



print(item_list)

