import os
import time
import subprocess
import configparser


def get_local_ip(interface='eth0'):
    cmd = f"ip addr show {interface} | grep 'inet ' | awk '{{print $2}}'"
    output = os.popen(cmd).read().strip()
    return output.split('/')[0]


def check_ip_address(interface):
    while True:
        result = subprocess.run(["ip", "addr", "show", "dev", interface], capture_output=True, text=True)
        output = result.stdout

        if "inet " in output:
            break

        time.sleep(5)
        subprocess.run("pkexec dhclient", shell=True, capture_output=True, text=True)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('local_config.ini')

    report_base_path = config.get('report_path', 'base_path')
    os.system(f'chmod 777 {report_base_path}/*')

    interface = config.get('settings', 'used_interface')
    check_ip_address(interface)
    local_ip = get_local_ip(interface)

    os.system('python ./scripts/Information_Gathering/scan.py')

    if config.getboolean('settings', 'protocols_parsing'):
        os.system('python ./scripts/Information_Gathering/packet_parsing.py')

    if config.getboolean('settings', 'tshark_traffic_sniffing'):
        os.system('python ./scripts/Sniff/traffic_capture.py')

    if config.getboolean('settings', 'credslayer_traffic_sniffing'):
        os.system(f"python ./scripts/Sniff/credslayer_capture.py")

    if config.getboolean('settings', 'send_report_to_ssh_server'):
        os.system('python ./send_report.py')
