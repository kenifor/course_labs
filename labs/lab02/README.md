<div align="center">
<h1><a id="intro">Лабораторная работа №2</a><br></h1>
<a href="https://docs.github.com/en"><img src="https://img.shields.io/static/v1?logo=github&logoColor=fff&label=&message=Docs&color=36393f&style=flat" alt="GitHub Docs"></a>
<a href="https://daringfireball.net/projects/markdown"><img src="https://img.shields.io/static/v1?logo=markdown&logoColor=fff&label=&message=Markdown&color=36393f&style=flat" alt="Markdown"></a> 
<a href="https://symbl.cc/en/unicode-table"><img src="https://img.shields.io/static/v1?logo=unicode&logoColor=fff&label=&message=Unicode&color=36393f&style=flat" alt="Unicode"></a> 
<a href="https://shields.io"><img src="https://img.shields.io/static/v1?logo=shieldsdotio&logoColor=fff&label=&message=Shields&color=36393f&style=flat" alt="Shields"></a>
<a href="https://img.shields.io/badge/Risk_Analyze-2448a2"><img src="https://img.shields.io/badge/Course-Risk_Analysis-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/AppSec-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/Contributor-Балашов_Д.В.-8b9aff" alt="Contributor Badge"></a></div>

***

Данная лабораторная работа посвещена изучению *nix машин и как они работают, позволяет приобрести навыки для работы с терминалом/ консолью и приобрести знания по работе ОС. В лабоработрной работе описываются материалы по командам, скриптам и подключаемым приложениям.

***
## Задание

- [x] 1. Выведите на терминале и проанализируйте следующие команды консоли
```bash
$ who | wc -l # who показывает активные интерактивные сессии, wc -l считает строки → сколько пользователей "в системе" сейчас
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ who | wc -l
0

$ id # показывает uid/gid текущего пользователя и его группы
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ id
uid=1000(kali) gid=1000(kali) groups=1000(kali),4(adm),20(dialout),24(cdrom),25(floppy),27(sudo),29(audio),30(dip),44(video),46(plugdev),100(users),101(netdev),107(bluetooth),115(scanner),126(lpadmin),134(wireshark),136(kaboxer),137(vboxsf)

$ whoami # выводит имя текущего пользователя
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ whoami 
kali

$ hostnamectl # подробная инфа о хосте: имя, ОС, ядро, архитектура, тип машины
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ hostnamectl 
 Static hostname: kali
       Icon name: computer-vm
         Chassis: vm 🖴
      Machine ID: 22f806e906284626a47f5ed8edf04972
         Boot ID: b09eb61ccdab456eb02eb92040ebc1ca
  Virtualization: oracle
Operating System: Kali GNU/Linux Rolling          
          Kernel: Linux 6.12.13-amd64
    Architecture: x86-64
 Hardware Vendor: innotek GmbH
  Hardware Model: VirtualBox
Firmware Version: VirtualBox
   Firmware Date: Fri 2006-12-01
    Firmware Age: 18y 11month 4w 2d

```
- [x] 2. Выведите утилитой `tree` список вложенности дерева диреторий для каталога своего пользователя. Далее используйте `ls -a` и укажите отличие от `ls -l`.
```bash
┌──(kali㉿kali)-[~]
└─$ tree           
.
├── course_labs
│   ├── APPENDIX.md
│   ├── artifacts
│   │   ├── art_cheatsheet
│   │   │   ├── Docker_Image_Security_Best_Practices.pdf
│   │   │   └── gitscm.jpg
│   │   ├── cheatsheet
│   │   │   ├── CHEATSHEET_DOCKERIGNORE.md
│   │   │   ├── CHEATSHEET_DOCKER.md
│   │   │   ├── CHEATSHEET_GH_CLI.md
│   │   │   ├── CHEATSHEET_GITIGNORE.md
│   │   │   └── CHEATSHEET_GIT.md
│   │   ├── exmpls
│   │   │   ├── Аналитический отчет по уязвимости PrintNightmare.pdf
│   │   │   ├── Пример - Multisignature - Безопасности криптовалютных платежей.pdf
│   │   │   └── Пример_аналитических_отчетов_по_задачам_ИБ.pdf
│   │   ├── owasp
│   │   │   ├── OWASP_Top_10_CICD_Risks.pdf
│   │   │   ├── Авторизация (Authorization).pdf
│   │   │   ├── Атаки на клиентов (Client-side Attacks).pdf
│   │   │   ├── Аутентификация (Authentication).pdf
│   │   │   ├── Выполнение кода (Command Execution).pdf
│   │   │   ├── Логические атаки (Logical Attacks).pdf
│   │   │   └── Разглашение информации (Information Disclosure).pdf
│   │   └── ppt
│   │       └── Лекция_Управление Рисками ИБ_intro.pdf
│   ├── assets
│   │   ├── logotype
│   │   │   ├── logo2.jpg
│   │   │   └── logo.jpg


┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ ls -a
.  ..  exmpl_hello.py  pygamesteel.py  README.md
                                                                                                     
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ ls -l
total 24
-rw-rw-r-- 1 kali kali   414 Nov 27 13:54 exmpl_hello.py
-rw-rw-r-- 1 kali kali   807 Nov 27 13:54 pygamesteel.py
-rw-rw-r-- 1 kali kali 16240 Nov 27 13:54 README.md

#ls -a — показать все файлы/папки, включая скрытые (начинающиеся с точки).
#ls -l — показать подробный список (права, владелец, размер, дата, имя), но скрытые файлы не выводит.
```
- [x] 3. Используйте утилиту `file` и `df` для определения какая файловая система на разделе `/dev/sda1`.
```bash
┌──(root㉿kali)-[/home/kali/course_labs/labs/lab02]
└─# file -s /dev/sda1
/dev/sda1: Linux rev 1.0 ext4 filesystem data, UUID=8ef2cfd5-4f7d-4943-a6c3-825ac3876ec2, volume name "root" (needs journal recovery) (extents) (64bit) (large files) (huge files)
                                                                                                     
┌──(root㉿kali)-[/home/kali/course_labs/labs/lab02]
└─# df -h /dev/sda1 
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        79G   55G   21G  73% /

```
- [x] 4. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ which vi # показывает путь к vi
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ which vi
/usr/bin/vi

$ locate hello.py # ищет hello.py в locate
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ locate hello.py
/home/kali/hello.py
/home/kali/course_labs/labs/lab01/hello.py
/home/kali/course_labs/labs/lab02/exmpl_hello.py
/home/kali/course_labs/labs/lab05/source/hello.py
/home/kali/gpg-test/hello.py
/home/kali/lab_01_risk/hello.py
/usr/lib/python3/dist-packages/mitmproxy/contrib/kaitaistruct/dtls_client_hello.py
/usr/lib/python3/dist-packages/mitmproxy/contrib/kaitaistruct/tls_client_hello.py

$ sudo updatedb # обновляет базу locate
$ locate hello # ищет все файлы/пути где встречается hello
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ locate hello   
/boot/grub/i386-pc/hello.mod
/home/kali/hello.py
/home/kali/course_labs/labs/lab01/hello.py
/home/kali/course_labs/labs/lab02/exmpl_hello.py
/home/kali/course_labs/labs/lab05/source/hello.py
/home/kali/gpg-test/hello.py
/home/kali/lab_01_risk/hello.py
/home/linuxbrew/.linuxbrew/Homebrew/Library/Homebrew/test/support/fixtures/elf/hello
/home/linuxbrew/.linuxbrew/Homebrew/Library/Homebrew/test/support/fixtures/elf/hello_with_rpath
/home/linuxbrew/.linuxbrew/Homebrew/Library/Homebrew/test/support/fixtures/elf/libhello.so.0
/snap/core18/2940/usr/lib/python3.6/__phello__.foo.py
/snap/core18/2940/usr/lib/python3.6/__pycache__/__phello__.foo.cpython-36.pyc
/snap/core18/2952/usr/lib/python3.6/__phello__.foo.py
/snap/core18/2952/usr/lib/python3.6/__pycache__/__phello__.foo.cpython-36.pyc
/snap/core22/2111/usr/lib/python3.10/__phello__.foo.py
/snap/core22/2111/usr/lib/python3.10/__pycache__/__phello__.foo.cpython-310.pyc
/snap/core22/2133/usr/lib/python3.10/__phello__.foo.py
/snap/core22/2133/usr/lib/python3.10/__pycache__/__phello__.foo.cpython-310.pyc
/usr/lib/grub/i386-pc/hello.mod

$ touch screen
$ find ~ -name screen  # поиск по файловой системе в ~
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ find ~ -name screen
/home/kali/course_labs/labs/lab02/screen

$ locate screen  # ищет screen в locate

$ sudo updatedb # обновляем базу ещё раз после создания файла
$ locate screen # ищет screen в locate
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ locate screen
/etc/screenrc
/etc/alternatives/desktop-lockscreen.xml
/etc/init.d/screen-cleanup
/etc/pam.d/xfce4-screensaver
/etc/rcS.d/S01screen-cleanup
/etc/tmpfiles.d/screen-cleanup.conf
/etc/xdg/kscreenlockerrc
/etc/xdg/autostart/xfce4-screensaver.desktop
/etc/xdg/menus/xfce4-screensavers.menu
/home/kali/.config/google-chrome/Default/Extensions/ghbmnnjooekpmoecnnnilnnbdlolhkhi/1.98.1_0/offscreendocument.html
/home/kali/.config/google-chrome/Default/Extensions/ghbmnnjooekpmoecnnnilnnbdlolhkhi/1.98.1_0/offscreendocument_main.js
/home/kali/.config/google-chrome/WasmTtsEngine/20251114.1/offscreen.html
/home/kali/.config/google-chrome/WasmTtsEngine/20251114.1/offscreen_compiled.js
/home/kali/.config/xfce4/xfce4-screenshooter
/home/kali/.config/xfce4/desktop/icons.screen0.yaml
/home/kali/Desktop/IoTGoat/OpenWrt/openwrt-18.06.2/target/linux/brcm2708/patches-4.9/950-0062-rpi-ft5406-Add-touchscreen-driver-for-pi-LCD-display.patch
/home/kali/Desktop/venv/lib/python3.13/site-packages/pip/_vendor/rich/screen.py
/home/kali/Desktop/venv/lib/python3.13/site-packages/pip/_vendor/rich/__pycache__/screen.cpython-313.pyc
/home/kali/api_junit_tests/screenshots
/home/kali/api_junit_tests/screenshots/test_passed.png
/home/kali/course_labs/labs/lab02/screen
/home/kali/gpg-test/venv/lib/python3.13/site-packages/pip/_vendor/rich/screen.py
/home/kali/gpg-test/venv/lib/python3.13/site-packages/pip/_vendor/rich/__pycache__/screen.cpython-313.pyc
/home/kali/gpg-test/venv/lib/python3.13/site-packages/rich/screen.py
/home/kali/gpg-test/venv/lib/python3.13/site-packages/rich/__pycache__/screen.cpython-313.pyc
/home/kali/lab_01_risk/venv/lib/python3.13/site-packages/pip/_vendor/rich/screen.py
/home/kali/lab_01_risk/venv/lib/python3.13/site-packages/pip/_vendor/rich/__pycache__/screen.cpython-313.pyc
/home/kali/lab_01_risk/venv/lib/python3.13/site-packages/rich/screen.py
/home/kali/lab_01_risk/venv/lib/python3.13/site-packages/rich/__pycache__/screen.cpython-313.pyc
/home/kali/snap/postman/350/.local/share/glib-2.0/schemas/org.gnome.desktop.screensaver.gschema.xml
/home/kali/snap/postman/351/.local/share/glib-2.0/schemas/org.gnome.desktop.screensaver.gschema.xml
/home/kali/ui_cucumber_tests/screenshots
/home/kali/ui_cucumber_tests/screenshots/test_passed.png
```

- [x]  5. Используйте конструкцию и вставьте ее в созданный файл ранее. Подключите `pygame` - используем исключительно для стилизации окна.

```py
import pygame
pygame.init()

# Устанавливаем размеры окна
screen_width = 800
screen_height = 600
window_size = (screen_width, screen_height)
pygame.display.set_mode(window_size) # Создаем окно

# Задаем цвет фона
bg_color = (255, 255, 255)
pygame.draw.rect(screen, bg_color, [0, 0, screen_width, screen_height], 1)

# Выводим текст на экран
font = pygame.font.SysFont(None, 75)
text = font.render("Hello appsec world*", True, (0, 255, 0))
text_rect = text.get_rect()
text_rect.center = (400, 300)
screen.blit(text, text_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
pygame.display.flip() # Обновляем экран
```

- [x] 6. Сделайте `commit` и `push` в свой репозиторий с изменениями в `master branch`. На следующих лабораторных работах мы вернемся к этому файлу.
- [x] 7. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ groups # показывает группы текущего пользователя
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ groups                 
kali adm dialout cdrom floppy sudo audio dip video plugdev users netdev bluetooth scanner lpadmin wireshark kaboxer vboxsf

$ useradd smallman # создаёт пользователя smallman
$ userdel smallman -rf # удаляет пользователя
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ sudo userdel smallman -rf
userdel: smallman mail spool (/var/mail/smallman) not found
userdel: smallman home directory (/home/smallman) not found

$ useradd smallman
$ passwd smallman # задает пароль пользователю
┌──(root㉿kali)-[/home/kali/course_labs/labs/lab02]
└─# passwd smallman
New password: 
Retype new password: 
passwd: password updated successfully

$ usermod smallman -c 'Hach Hachov Hacherovich,239,45-67,499-239-45-33' # записываем GECOS-комментарий
$ passwd smallman
$ id smallman # выводит uid/gid и группы smallman
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ sudo id smallman    
uid=1001(smallman) gid=1001(smallman) groups=1001(smallman)

$ groupadd -g 1500 readgroup # создает группу readgroup с gid=1500
$ usermod -aG readgroup smallman  # добавляет smallman в readgroup
$ chmod 666 screen.py # ставит права rw-rw-rw- (читать/писать всем)
```
- [x] 8. Выведите группу прав для `screen` и измените, что бы файл был доступен только для чтения созданному пользователю и выведите права этого польователя для измененного файла только используя `readgroup`.
```bash
┌──(root㉿kali)-[/home/kali/course_labs/labs/lab02]
└─# ls -l screen.py 
-rw-rw-rw- 1 kali kali 674 Nov 30 18:18 screen.py

┌──(root㉿kali)-[~/course_labs/labs/lab02]
└─$ chgrp readgroup screen.py # меняем группу файла на readgroup

┌──(root㉿kali)-[~/course_labs/labs/lab02]
└─$ sudo chmod 640 screen.py # права: владелец rw, группа r

┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ ls -l screen.py 
-rw-r----- 1 kali readgroup 674 Nov 30 18:18 screen.py

```
- [x] 9. Используйте `POSIX ACL`. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ touch nmapres.txt
$ setfacl -m u:smallman:rw nmapres.txt
$ setfacl -m g:readgroup:r nmapres.txt
$ getfacl nmapres.txt
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ getfacl nmapres.txt
# file: nmapres.txt
# owner: kali
# group: kali
user::rw-
user:smallman:rw-
group::rw-
group:readgroup:r--
mask::rw-
other::r--


```

- [x] 10. Сохраните файл внутри локального репозитория, так как следующая работа будет подразумевать запись в нее данных о nmap.
```bash
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ git add nmapres.txt                       
                                                                                                     
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ git commit -m "for_lab_3"
[develop 989f911] for_lab_3
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 labs/lab02/nmapres.txt
                                                                                                     
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ git push                 
Enumerating objects: 8, done.
Counting objects: 100% (8/8), done.
Delta compression using up to 4 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (5/5), 921 bytes | 921.00 KiB/s, done.
Total 5 (delta 3), reused 1 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
To github.com:kenifor/course_labs.git
   9f776a4..989f911  develop -> develop

```
- [x] 11. Для закрепления выведите все списки групп пользователей на вашей ОС и права на верхнеуровневые каталоги.
```bash
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ ls -ld /* 
lrwxrwxrwx   1 root root          7 Feb 17  2025 /bin -> usr/bin
drwxr-xr-x   3 root root       4096 Sep 20 08:48 /boot
drwxr-xr-x  18 root root       3460 Nov 30 15:38 /dev
drwxr-xr-x 186 root root      12288 Nov 30 18:28 /etc
drwxr-xr-x   4 root root       4096 Nov 17 16:31 /home
lrwxrwxrwx   1 root root         29 Apr 23  2025 /initrd.img -> boot/initrd.img-6.12.13-amd64
lrwxrwxrwx   1 root root         29 Apr 23  2025 /initrd.img.old -> boot/initrd.img-6.12.13-amd64
drwxr-xr-x   3 root root       4096 Jul 20 13:30 /jetbra
lrwxrwxrwx   1 root root          7 Feb 17  2025 /lib -> usr/lib
lrwxrwxrwx   1 root root          9 Apr 23  2025 /lib32 -> usr/lib32
lrwxrwxrwx   1 root root          9 Feb 17  2025 /lib64 -> usr/lib64
drwx------   2 root root      16384 Apr 23  2025 /lost+found
drwxr-xr-x   2 root root       4096 Apr 23  2025 /media

┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ cat /etc/group
root:x:0:
daemon:x:1:
bin:x:2:
sys:x:3:
adm:x:4:kali
tty:x:5:
disk:x:6:

```
- [x] 12. Выведите все права для файлов и директорий локального репозитория которые имеют различные пользователи  (без использования длинных путей)
```bash
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ ls -l     
total 28
-rw-rw-r--  1 kali kali        414 Nov 27 13:54 exmpl_hello.py
-rw-rw-r--+ 1 kali kali          0 Nov 30 18:32 nmapres.txt
-rw-rw-r--  1 kali kali        807 Nov 27 13:54 pygamesteel.py
-rw-rw-r--  1 kali kali      16240 Nov 27 13:54 README.md
-rw-r-----  1 kali readgroup   674 Nov 30 18:18 screen.py

```
- [x] 13. Выведите процессы которые у вас запущены в термине и вне его.
```bash
──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ ps -a
    PID TTY          TIME CMD
  82630 pts/0    00:00:00 ps
                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ ps -x 
    PID TTY      STAT   TIME COMMAND
   1472 ?        Ss     0:00 /usr/lib/systemd/systemd --user
   1474 ?        S      0:00 (sd-pam)
   1492 ?        Ss     0:00 /usr/bin/mpris-proxy
   1493 ?        Ssl    0:00 /usr/bin/pipewire
   1494 ?        Ssl    0:00 /usr/bin/pipewire -c filter-chain.conf
   1496 ?        Ssl    0:00 /usr/bin/wireplumber
   1497 ?        Ssl    0:00 /usr/bin/pipewire-pulse

┌──(kali㉿kali)-[~/course_labs/labs/lab02]
└─$ pstree
systemd─┬─ModemManager───3*[{ModemManager}]
        ├─NetworkManager───3*[{NetworkManager}]
        ├─3*[VBoxClient───VBoxClient───3*[{VBoxClient}]]
        ├─VBoxClient───VBoxClient───4*[{VBoxClient}]
        ├─VBoxService───8*[{VBoxService}]
        ├─accounts-daemon───3*[{accounts-daemon}]
        ├─agetty
        ├─colord───3*[{colord}]
        ├─containerd───8*[{containerd}]
        ├─cron
        ├─dbus-daemon
```
- [x] 14. Оформить `README.md` по аналогии и использовать `shield`, etc.
- [x] 15. Составить `gist` отчет и отправить ссылку личным сообщением
