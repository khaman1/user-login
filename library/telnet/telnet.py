import telnetlib

def user_login(host="10.0.253.2", password="motorola"):
    tn = telnetlib.Telnet(host, timeout=5)
    tn.read_until(b"username: ")
    tn.write('admin'.encode('ascii') + b"\n")
    tn.read_until(b"password: ")
    tn.write(password.encode('ascii') + b"\n")

    return tn

##################
##################
def get_vswr():
    tn = user_login()
    tn.write(b"dpm 1 get vswr\n")
    tn.read_until(b"dpm 1 get vswr", timeout=5)
    tn.write(b"exit\n")

    result = tn.read_all().decode('ascii')
    item_list = result.split('\r\n')

    try:
        vswr_ratio = item_list[4].strip().split(' ')[-1]
        dpm_status = item_list[5].strip()

        return vswr_ratio, dpm_status

    except:
        return '',''
##################
##################
def get_fwd_power():
    tn = user_login()
    tn.write(b"dpm 1 get fwd_power\n")
    tn.read_until(b"dpm 1 get fwd_power", timeout=5)
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
def get_rev_power():
    tn = user_login()
    tn.write(b"dpm 1 get rev_power\n")
    tn.read_until(b"dpm 1 get rev_power", timeout=5)
    tn.write(b"exit\n")

    result = tn.read_all().decode('ascii')
    item_list = result.split('\r\n')


    try:
        reserve_power = ' '.join(item_list[4].strip().split(' ')[-2:])
        dpm_status = item_list[5].strip()

        return reserve_power, dpm_status

    except:
        return '',''