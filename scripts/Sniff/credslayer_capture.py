import subprocess
import time
import configparser
import datetime


def run_credslayer_capture(utility, duration_seconds):
    try:
        process = subprocess.Popen(utility, shell=True)
        time.sleep(duration_seconds)
        process.terminate()
        process.wait()
    except Exception as e:
        print("[-] CredsLayer error:", e)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('local_config.ini')

    settings = config['settings']
    report_path = config['report_path']

    used_interface = settings.get('used_interface')
    report_folder = report_path.get('sniff_path')

    uniq_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    credslayer_traffic_file = f"credslayer_traffic_{uniq_filename}.pcap"
    credslayer_file = f"credslayer_traffic_{uniq_filename}.txt"

    utility_to_run = (
        f"credslayer -l {used_interface} "
        f"-lo {report_folder}/{credslayer_traffic_file} "
        f"-o {report_folder}/{credslayer_file}"
    )
    duration_seconds = settings.getint('credslayer_traffic_capture_time')

    print('[+] Start CredsLayer traffic sniffing...')
    run_credslayer_capture(utility_to_run, duration_seconds)
    print('[+] CredsLayer traffic sniffing DONE.\n')
