import configparser
import subprocess
import datetime


def run_tshark_capture(interface, duration_seconds, report_folder, report_file):
    print('[+] Start Tshark traffic sniffing...')
    subprocess.run(
        ['tshark', '-i', interface, '-a', f'duration:{duration_seconds}', '-w', f'{report_folder}/{report_file}'])


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('local_config.ini')

    settings = config['settings']
    report_path = config['report_path']

    interface = settings.get('used_interface')
    duration_seconds = settings.getint('tshark_traffic_capture_time')
    report_folder = report_path.get('sniff_path')

    uniq_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    report_file = f"captured_traffic_{uniq_filename}.pcapng"

    run_tshark_capture(interface, duration_seconds, report_folder, report_file)
    print('[+] Tshark traffic sniffing DONE.\n')
