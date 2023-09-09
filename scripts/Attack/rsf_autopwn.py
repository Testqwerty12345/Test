from routersploit.modules.scanners.autopwn import Exploit

# Створення об'єкта експлоіту
exploit = Exploit()
exploit.target = "192.168.0.1"
# Запуск експлоіту
result = exploit.run()

if result:
    print("Вразливість була успішно експлуатована!")

    # Виведення інформації про підтверджені вразливості
    for confirmed_vulnerability in exploit.confirmed_vulnerabilities:
        print("Підтверджена вразливість:", confirmed_vulnerability)

else:
    print("Не вдалося експлуатувати вразливість.")