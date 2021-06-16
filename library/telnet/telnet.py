import telnetlib

def user_login(host="10.0.253.2", port="", password="motorola"):
    if not port:
        tn = telnetlib.Telnet(host, timeout=1)
    else:
        tn = telnetlib.Telnet(host, port, timeout=1)

    tn.read_until(b"username: ")
    tn.write('admin'.encode('ascii') + b"\n")
    tn.read_until(b"password: ")
    tn.write(password.encode('ascii') + b"\n")

    return tn

##################
##################
def get_vswr(host="10.0.253.2", port="", password="motorola"):
    tn = user_login(host=host, port=port, password=password)
    tn.write(b"dpm 1 get vswr\n")
    tn.read_until(b"dpm 1 get vswr", timeout=3)
    tn.write(b"exit\n")

    result = tn.read_all().decode('ascii')
    item_list = result.split('\r\n')

    try:
        vswr_ratio = item_list[4].strip().split(' ')[-1]
        dpm_status = item_list[5].strip()

        return vswr_ratio, dpm_status

    except:
        return '',''

def get_vswr_br(host="10.0.253.2", port="18011", password="motorola"):
    tn = user_login(host=host, port=port, password=password)
    tn.write(b"get vswr\n")
    tn.read_until(b"Current VSWR ratio is ", timeout=3)
    tn.write(b"exit\n")

    try:
        return tn.read_all().decode('ascii').split('\r\n')[0]
    except:
        return ''
##################
##################
def get_fwd_power(host="10.0.253.2", port="", password="motorola"):
    tn = user_login(host=host, port=port, password=password)
    tn.write(b"dpm 1 get fwd_power\n")
    tn.read_until(b"dpm 1 get fwd_power", timeout=3)
    tn.write(b"exit\n")

    result = tn.read_all().decode('ascii')
    item_list = result.split('\r\n')


    try:
        output_power = ' '.join(item_list[4].strip().split(' ')[-2:])
        dpm_status = item_list[5].strip()

        return output_power, dpm_status

    except:
        return '',''
##################
##################
def get_rev_power(host="10.0.253.2", port="", password="motorola"):
    tn = user_login(host=host, port=port, password=password)
    tn.write(b"dpm 1 get rev_power\n")
    tn.read_until(b"dpm 1 get rev_power", timeout=3)
    tn.write(b"exit\n")

    result = tn.read_all().decode('ascii')
    item_list = result.split('\r\n')


    try:
        reserve_power = ' '.join(item_list[4].strip().split(' ')[-2:])
        dpm_status = item_list[5].strip()

        return reserve_power, dpm_status

    except:
        return '',''

##################
def get_rssi_br(host="10.0.253.2", port="180011", password="motorola"):
    tn = user_login(host=host, port=port, password=password)
    tn.write(b"rssicnt\n")
    tn.read_until(b"RSSI failure counters values:", timeout=3)
    tn.write(b"exit\n")

    item_list = tn.read_all().decode('ascii').split('\r\n')

    rssi_failure_cnt1 = item_list[1].split(' = ')[1]
    rssi_failure_cnt2 = item_list[2].split(' = ')[1]
    rssi_failure_cnt3 = item_list[3].split(' = ')[1]

    return rssi_failure_cnt1, rssi_failure_cnt2, rssi_failure_cnt3