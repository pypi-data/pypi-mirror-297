try:
    from wmi import WMI
except ImportError:
    pass
import socket
import subprocess
from sys import platform as splatform
import os
import platform

if platform.system() != "Windows":
    import lsb_release_ex
import uuid


# 获取计算机名
def getname():
    return socket.gethostname()


def get_disk_serial_number():
    c = WMI()
    for disk in c.Win32_DiskDrive():
        return disk.SerialNumber.strip()


def get_windows_uuid():
    c = WMI()
    for os in c.Win32_OperatingSystem():
        return os.UUID.strip()


def get_mac_serial_number():
    cmd = ["/usr/sbin/system_profiler", "SPHardwareDataType"]
    sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out_str = sp.communicate()[0].decode("utf-8")
    for line in out_str.split("\n"):
        if "Serial Number" in line:
            return line.split(":")[1].strip()


def get_device_uuid():
    if splatform == "linux" or splatform == "linux2":
        # pass
        # linux
        u = uuid.uuid1()
        return str(u).split("-")[-1]
    elif splatform == "darwin":
        # OS X
        my_system = platform.uname()
        return f"{my_system.system}-{get_mac_serial_number()}"
    elif splatform == "win32":
        a = WMI().Win32_ComputerSystemProduct()[0]
        b = WMI().Win32_OperatingSystem()[0]
        return f"{b.Caption}-{get_disk_serial_number()}"


def get_device_name():
    if splatform == "linux" or splatform == "linux2":
        my_system = platform.uname()
        distinfo = lsb_release_ex.get_distro_information()
        return "{}-{}".format(getname(), distinfo.get("DESCRIPTION"))
    elif splatform == "darwin":
        my_system = platform.uname()
        return "{}-{}".format(my_system.system, my_system.node)
    elif splatform == "win32":
        a = WMI().Win32_ComputerSystemProduct()[0]
        return "{}-{}".format(a.Vendor, a.Name)


if __name__ == '__main__':
    a = get_device_uuid()
    print(a)