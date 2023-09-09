import configparser
import subprocess
import datetime


def run_tshark_capture(interface, duration_seconds, report_folder, report_file):
    print('[+] Start Tshark packet parsing...')
    subprocess.run(
        ['tshark', '-i', interface, '-a', f'duration:{duration_seconds}',
         ' -Y "(mndp || lldp || cdp || ospf || vrrp || llmnr)"', '-w', f'{report_folder}/{report_file}'])


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('local_config.ini')

    settings = config['settings']
    report_path = config['report_path']

    interface = settings.get('used_interface')
    duration_seconds = settings.getint('packet_traffic_capture_time')
    report_folder = report_path.get('sniff_path')

    uniq_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    report_file = f"captured_packets_{uniq_filename}.pcapng"

    run_tshark_capture(interface, duration_seconds, report_folder, report_file)
    print('[+] Packet parsing DONE.\n')
