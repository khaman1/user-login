import telnetlib
from library.telnet.telnet import *

print("===============================================")



##################
##################
vswr_ratio, dpm_status = get_vswr()
output_power, dpm_status = get_fwd_power()
reserve_power, dpm_status = get_rev_power()

print(vswr_ratio)
print(output_power)
print(reserve_power)
print(dpm_status)

