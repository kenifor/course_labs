<div align="center">
<h1><a id="intro">Лабораторная работа №3</a><br></h1>
<a href="https://docs.github.com/en"><img src="https://img.shields.io/static/v1?logo=github&logoColor=fff&label=&message=Docs&color=36393f&style=flat" alt="GitHub Docs"></a>
<a href="https://daringfireball.net/projects/markdown"><img src="https://img.shields.io/static/v1?logo=markdown&logoColor=fff&label=&message=Markdown&color=36393f&style=flat" alt="Markdown"></a> 
<a href="https://symbl.cc/en/unicode-table"><img src="https://img.shields.io/static/v1?logo=unicode&logoColor=fff&label=&message=Unicode&color=36393f&style=flat" alt="Unicode"></a> 
<a href="https://shields.io"><img src="https://img.shields.io/static/v1?logo=shieldsdotio&logoColor=fff&label=&message=Shields&color=36393f&style=flat" alt="Shields"></a>
<a href="https://img.shields.io/badge/Risk_Analyze-2448a2"><img src="https://img.shields.io/badge/Course-Risk_Analysis-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/AppSec-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/Contributor-Балашов_Д.В.-8b9aff" alt="Contributor Badge"></a></div>

***

Данная лабораторная работа посвещена изучению `nmap` и как с ним работать. Эта лабораторная работа послужит подпоркой для старта в выявлении и определении уязвимостей на уровне сканера портов, что бы освоить базовые методы сканирования. 

***

## Задание

- [ ] 1. Опишите используемые методы по их назначению, как они функционируют и какие результаты могут дать для оценки. Используйте сноску из материалов выше по флагам команд.
- [ ] 2. Выведите на терминале и проанализируйте следующие команды консоли

```bash

┌──(kali㉿kali)-[~/course_labs/labs]
└─$ nmap localhost # проверка 1000 портов
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 16:41 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0000050s latency).
Other addresses for localhost (not scanned): ::1
All 1000 scanned ports on localhost (127.0.0.1) are in ignored states.
Not shown: 1000 closed tcp ports (reset)

Nmap done: 1 IP address (1 host up) scanned in 0.10 seconds
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs]
└─$ nmap -sC localhost # -sC — запуск стандартных NSE-скриптов (определение сервисов, SSL, HTTP-info, баннеры)
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 16:41 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0000050s latency).
Other addresses for localhost (not scanned): ::1
All 1000 scanned ports on localhost (127.0.0.1) are in ignored states.
Not shown: 1000 closed tcp ports (reset)

Nmap done: 1 IP address (1 host up) scanned in 0.33 seconds
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs]
└─$ 
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs]
└─$ nmap -p localhost # флаг -p позволяет выбрать определенный порт 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 16:41 MSK
Found no matches for the service mask 'localhost' and your specified protocols
QUITTING!
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs]
└─$ nmap -O localhost # -O включает определение ОС устройства
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 16:42 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000047s latency).
Other addresses for localhost (not scanned): ::1
All 1000 scanned ports on localhost (127.0.0.1) are in ignored states.
Not shown: 1000 closed tcp ports (reset)
Too many fingerprints match this host to give specific OS details
Network Distance: 0 hops

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.54 seconds
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs]
└─$ nmap -p 80 localhost # -p 80 сканирует только порт 80
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 16:42 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000068s latency).
Other addresses for localhost (not scanned): ::1

PORT   STATE  SERVICE
80/tcp closed http

Nmap done: 1 IP address (1 host up) scanned in 0.10 seconds
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs]
└─$ nmap -p 443 localhost # -p 443 сканирует только порт 443
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 16:42 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000058s latency).
Other addresses for localhost (not scanned): ::1

PORT    STATE  SERVICE
443/tcp closed https

Nmap done: 1 IP address (1 host up) scanned in 0.08 seconds
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs]
└─$ nmap -p 8443 localhost -p 8443 сканирует альтернативный HTTPS или админ-панель
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 16:42 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000052s latency).
Other addresses for localhost (not scanned): ::1

PORT     STATE  SERVICE
8443/tcp closed https-alt

Nmap done: 1 IP address (1 host up) scanned in 0.11 seconds
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs]
└─$ nmap -p "*" localhost # "*" скан 65535 портов
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 16:42 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0000050s latency).
Other addresses for localhost (not scanned): ::1
All 8377 scanned ports on localhost (127.0.0.1) are in ignored states.
Not shown: 8377 closed tcp ports (reset)

Nmap done: 1 IP address (1 host up) scanned in 0.20 seconds
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs]
└─$ nmap -sV -p 22,8080 localhost # -sV - определение версии сервисов (service version detection), -p 22,8080 — список портов
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 16:42 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000061s latency).
Other addresses for localhost (not scanned): ::1

PORT     STATE  SERVICE    VERSION
22/tcp   closed ssh
8080/tcp closed http-proxy

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.20 seconds
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs]
└─$ nmap -sP 192.168.31.0/24 # проверка активных хостов без сканирования портов
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 16:42 MSK
Nmap scan report for XiaoQiang (192.168.31.1)
Host is up (0.0063s latency).
MAC Address: 9C:9D:7E:8E:5E:23 (Beijing Xiaomi Mobile Software)
Nmap scan report for 192.168.31.60
Host is up (0.055s latency).
MAC Address: FA:AC:6A:8F:23:1B (Unknown)
Nmap scan report for 192.168.31.64
Host is up (0.054s latency).
MAC Address: B2:FC:D2:09:DC:D5 (Unknown)
Nmap scan report for 192.168.31.160
Host is up (0.00017s latency).
MAC Address: 4C:82:A9:B8:98:21 (Cloud Network Technology Singapore PTE.)
Nmap scan report for 192.168.31.41
Host is up.
Nmap done: 256 IP addresses (5 hosts up) scanned in 1.89 seconds
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs]
└─$ nmap --open 192.168.31.1 # фильтрует вывод, скрывая closed / filtered, только открытые порты
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 16:43 MSK
Nmap scan report for XiaoQiang (192.168.31.1)
Host is up (0.0037s latency).
Not shown: 992 closed tcp ports (reset)
PORT     STATE SERVICE
53/tcp   open  domain
80/tcp   open  http
443/tcp  open  https
8192/tcp open  sophos
8193/tcp open  sophos
8383/tcp open  m2mservices
8443/tcp open  https-alt
8899/tcp open  ospf-lite
MAC Address: 9C:9D:7E:8E:5E:23 (Beijing Xiaomi Mobile Software)

Nmap done: 1 IP address (1 host up) scanned in 0.45 seconds
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs]
└─$ nmap --packet-trace 192.168.31.1 # показывает отправленные/полученные пакеты
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 16:43 MSK
SENT (0.0513s) ARP who-has 192.168.31.1 tell 192.168.31.41
RCVD (0.0549s) ARP reply 192.168.31.1 is-at 9C:9D:7E:8E:5E:23
NSOCK INFO [0.1270s] nsock_iod_new2(): nsock_iod_new (IOD #1)
NSOCK INFO [0.1270s] nsock_connect_udp(): UDP connection requested to 192.168.31.1:53 (IOD #1) EID 8
NSOCK INFO [0.1270s] nsock_read(): Read request from IOD #1 [192.168.31.1:53] (timeout: -1ms) EID 18
NSOCK INFO [0.1270s] nsock_write(): Write request for 43 bytes to IOD #1 EID 27 [192.168.31.1:53]

┌──(kali㉿kali)-[~/course_labs/labs]
└─$ nmap --packet-trace scanme.nmap.org # cканирует порт scanme.nmap.org и выводит каждый отправленный/полученный пакет в hex + коротком виде.
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 16:49 MSK
SENT (0.1159s) ICMP [192.168.31.41 > 45.33.32.156 Echo request (type=8/code=0) id=61506 seq=0] IP [ttl=42 id=60232 iplen=28 ]
SENT (0.1162s) TCP 192.168.31.41:40164 > 45.33.32.156:443 S ttl=59 id=40602 iplen=44  seq=1704490746 win=1024 <mss 1460>
SENT (0.1165s) TCP 192.168.31.41:40164 > 45.33.32.156:80 A ttl=54 id=24469 iplen=40  seq=0 win=1024 
SENT (0.1174s) ICMP [192.168.31.41 > 45.33.32.156 Timestamp request (type=13/code=0) id=64954 seq=0 orig=0 recv=0 trans=0] IP [ttl=48 id=30955 iplen=40 ]
RCVD (0.2986s) TCP 45.33.32.156:80 > 192.168.31.41:40164 R ttl=45 id=0 iplen=40  seq=1704490746 win=0 
NSOCK INFO [0.3450s] nsock_iod_new2(): nsock_iod_new (IOD #1)
NSOCK INFO [0.3450s] nsock_connect_udp(): UDP connection requested to 192.168.31.1:53 (IOD #1) EID 8
NSOCK INFO [0.3450s] nsock_read(): Read request from IOD #1 [192.168.31.1:53] (timeout: -1ms) EID 18
NSOCK INFO [0.3450s] nsock_write(): Write request for 43 bytes to IOD #1 EID 27 [192.168.31.1:53]

┌──(kali㉿kali)-[~/course_labs/labs] 
└─$ nmap --iflist # вывод всех интерфейсов и маршрутов
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 16:57 MSK
************************INTERFACES************************
DEV             (SHORT)           IP/MASK                      TYPE     UP MTU   MAC
lo              (lo)              127.0.0.1/8                  loopback up 65536
lo              (lo)              ::1/128                      loopback up 65536
eth0            (eth0)            192.168.31.41/24             ethernet up 1500  08:00:27:BE:7D:82
eth0            (eth0)            fe80::6c01:60ec:a5a9:ed73/64 ethernet up 1500  08:00:27:BE:7D:82
eth1            (eth1)            192.168.100.10/24            ethernet up 1500  08:00:27:75:C5:3E
eth1            (eth1)            fe80::a00:27ff:fe75:c53e/64  ethernet up 1500  08:00:27:75:C5:3E
eth2            (eth2)            10.10.10.2/24                ethernet up 1500  08:00:27:52:82:AB
eth2            (eth2)            fe80::a00:27ff:fe52:82ab/64  ethernet up 1500  08:00:27:52:82:AB
docker0         (docker0)         172.17.0.1/16                ethernet up 1500  16:40:F1:9A:1C:A6
br-97648af44be5 (br-97648af44be5) 172.18.0.1/16                ethernet up 1500  CA:F8:FF:3C:BE:83
br-a9fadc855e8c (br-a9fadc855e8c) 172.21.0.1/16                ethernet up 1500  2A:B7:D2:EF:02:90
br-ad95c370f3af (br-ad95c370f3af) 172.19.0.1/16                ethernet up 1500  86:F4:62:5A:0D:84

**************************ROUTES**************************
DST/MASK                      DEV             METRIC GATEWAY
10.10.10.0/24                 eth2            0
192.168.100.0/24              eth1            0
192.168.31.0/24               eth0            100
172.17.0.0/16                 docker0         0
172.18.0.0/16                 br-97648af44be5 0
172.19.0.0/16                 br-ad95c370f3af 0
172.21.0.0/16                 br-a9fadc855e8c 0
0.0.0.0/0                     eth0            100    192.168.31.1
::1/128                       lo              0
fe80::a00:27ff:fe52:82ab/128  eth2            0
fe80::a00:27ff:fe75:c53e/128  eth1            0
fe80::6c01:60ec:a5a9:ed73/128 eth0            0
fe80::/64                     eth1            256
fe80::/64                     eth2            256
fe80::/64                     eth0            1024
ff00::/8                      eth1            256
ff00::/8                      eth2            256
ff00::/8                      eth0            256

┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ echo "scanme.nmap.org" > test_targets.txt # укажем файл и просканируем
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ nmap -iL test_targets.txt
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 17:03 MSK
Nmap scan report for scanme.nmap.org (45.33.32.156)
Host is up (0.19s latency).
Other addresses for scanme.nmap.org (not scanned): 2600:3c01::f03c:91ff:fe18:bb2f
Not shown: 991 closed tcp ports (reset)
PORT      STATE    SERVICE
22/tcp    open     ssh
80/tcp    open     http
135/tcp   filtered msrpc
139/tcp   filtered netbios-ssn
179/tcp   filtered bgp
445/tcp   filtered microsoft-ds
646/tcp   filtered ldp
9929/tcp  open     nping-echo
31337/tcp open     Elite

Nmap done: 1 IP address (1 host up) scanned in 11.29 seconds

┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ nmap -A -iL test_targets.txt # -A включает ОС + версии сервисов + traceroute + NSE scripts
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 17:03 MSK
Nmap scan report for scanme.nmap.org (45.33.32.156)
Host is up (0.19s latency).
Other addresses for scanme.nmap.org (not scanned): 2600:3c01::f03c:91ff:fe18:bb2f
Not shown: 991 closed tcp ports (reset)
PORT      STATE    SERVICE      VERSION
22/tcp    open     ssh          OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 ac:00:a0:1a:82:ff:cc:55:99:dc:67:2b:34:97:6b:75 (DSA)
|   2048 20:3d:2d:44:62:2a:b0:5a:9d:b5:b3:05:14:c2:a6:b2 (RSA)
|   256 96:02:bb:5e:57:54:1c:4e:45:2f:56:4c:4a:24:b2:57 (ECDSA)
|_  256 33:fa:91:0f:e0:e1:7b:1f:6d:05:a2:b0:f1:54:41:56 (ED25519)
80/tcp    open     http         Apache httpd 2.4.7 ((Ubuntu))
|_http-title: Go ahead and ScanMe!
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-favicon: Nmap Project
135/tcp   filtered msrpc
139/tcp   filtered netbios-ssn
179/tcp   filtered bgp
445/tcp   filtered microsoft-ds
646/tcp   filtered ldp
9929/tcp  open     nping-echo   Nping echo
31337/tcp open     tcpwrapped
Aggressive OS guesses: Linux 5.0 - 5.14 (99%), MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3) (99%), Linux 4.15 - 5.19 (96%), Linux 2.6.32 - 3.13 (95%), Linux 5.0 (94%), OpenWrt 22.03 (Linux 5.10) (94%), Linux 3.10 (94%), Linux 3.10 - 4.11 (94%), Linux 4.15 (93%), Linux 3.2 - 4.14 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 26 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 23/tcp)
HOP RTT       ADDRESS
1   3.68 ms   XiaoQiang (192.168.31.1)
2   3.72 ms   10.185.64.1
3   19.32 ms  213.85.208.250
4   7.69 ms   95.167.38.37
5   7.35 ms   188.128.126.247
6   ... 7
8   47.73 ms  be5484.ccr41.fra05.atlas.cogentco.com (130.117.1.1)
9   52.66 ms  be3343.ccr41.ams03.atlas.cogentco.com (154.54.62.142)
10  148.31 ms be2183.ccr22.lpl01.atlas.cogentco.com (154.54.58.69)
11  148.59 ms be3042.ccr21.ymq01.atlas.cogentco.com (154.54.44.162)
12  150.88 ms be3260.ccr32.yyz02.atlas.cogentco.com (154.54.42.89)
13  ... 14
15  147.92 ms be2718.ccr42.ord01.atlas.cogentco.com (154.54.7.129)
16  154.22 ms be5068.ccr32.oma02.atlas.cogentco.com (154.54.166.73)
17  161.55 ms be3272.ccr21.den01.atlas.cogentco.com (154.54.83.69)
18  175.52 ms be2752.ccr81.slc03.atlas.cogentco.com (154.54.163.246)
19  192.39 ms be3905.ccr21.sfo01.atlas.cogentco.com (154.54.1.210)
20  196.14 ms be3906.ccr22.sfo01.atlas.cogentco.com (154.54.5.154)
21  182.17 ms te0-0-0-18.ccr41.sjc03.atlas.cogentco.com (38.104.138.29)
22  202.00 ms 38.104.138.23
23  ... 25
26  205.56 ms scanme.nmap.org (45.33.32.156)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 31.54 seconds

┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ nmap -sA scanme.nmap.org # -sA - фильтрует ли firewall
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 17:05 MSK
Nmap scan report for scanme.nmap.org (45.33.32.156)
Host is up (0.19s latency).
Other addresses for scanme.nmap.org (not scanned): 2600:3c01::f03c:91ff:fe18:bb2f
Not shown: 995 unfiltered tcp ports (reset)
PORT    STATE    SERVICE
135/tcp filtered msrpc
139/tcp filtered netbios-ssn
179/tcp filtered bgp
445/tcp filtered microsoft-ds
646/tcp filtered ldp

Nmap done: 1 IP address (1 host up) scanned in 14.28 seconds
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ nmap -PN scanme.nmap.org # Сканирует scanme.nmap.org без предварительного ping
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 17:05 MSK
Nmap scan report for scanme.nmap.org (45.33.32.156)
Host is up (0.20s latency).
Other addresses for scanme.nmap.org (not scanned): 2600:3c01::f03c:91ff:fe18:bb2f
Not shown: 991 closed tcp ports (reset)
PORT      STATE    SERVICE
22/tcp    open     ssh
80/tcp    open     http
135/tcp   filtered msrpc
139/tcp   filtered netbios-ssn
179/tcp   filtered bgp
445/tcp   filtered microsoft-ds
646/tcp   filtered ldp
9929/tcp  open     nping-echo
31337/tcp open     Elite

Nmap done: 1 IP address (1 host up) scanned in 11.77 seconds
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ nmap --script=vuln IP_addr -vv # показывает CVE, слабые конфиги, небезопасные сервисы, -vv — подробный вывод
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 17:12 MSK
NSE: Loaded 105 scripts for scanning.
NSE: Script Pre-scanning.
NSE: Starting runlevel 1 (of 2) scan.
Initiating NSE at 17:12
NSE Timing: About 85.71% done; ETC: 17:13 (0:00:05 remaining)
Completed NSE at 17:13, 36.67s elapsed
NSE: Starting runlevel 2 (of 2) scan.
Initiating NSE at 17:13
Completed NSE at 17:13, 0.00s elapsed
Pre-scan script results:
| broadcast-avahi-dos: 
|   Discovered hosts:
|     224.0.0.251
|   After NULL UDP avahi packet DoS (CVE-2011-1002).
|_  Hosts are all up (not vulnerable).
Failed to resolve "IP_addr".
NSE: Script Post-scanning.
NSE: Starting runlevel 1 (of 2) scan.
Initiating NSE at 17:13
Completed NSE at 17:13, 0.00s elapsed
NSE: Starting runlevel 2 (of 2) scan.
Initiating NSE at 17:13
Completed NSE at 17:13, 0.00s elapsed
Read data files from: /usr/share/nmap
WARNING: No targets were specified, so 0 hosts scanned.
Nmap done: 0 IP addresses (0 hosts up) scanned in 36.83 seconds
           Raw packets sent: 0 (0B) | Rcvd: 0 (0B)
          
┌──(kali㉿kali)-[~/course_labs/labs/lab03] # такое количество уяз из-за того что включил sshd и sql
└─$ nmap -sV --script vuln -oN nmapres_new.txt localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-08 20:18 MSK
Pre-scan script results:
| broadcast-avahi-dos: 
|   Discovered hosts:
|     224.0.0.251
|   After NULL UDP avahi packet DoS (CVE-2011-1002).
|_  Hosts are all up (not vulnerable).
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0000050s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 998 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.9p1 Debian 3 (protocol 2.0)
| vulners: 
|   cpe:/a:openbsd:openssh:9.9p1: 
|       PACKETSTORM:189283      6.8     https://vulners.com/packetstorm/PACKETSTORM:189283      *EXPLOIT*
|       CVE-2025-26465  6.8     https://vulners.com/cve/CVE-2025-26465
|       9D8432B9-49EC-5F45-BB96-329B1F2B2254    6.8     https://vulners.com/githubexploit/9D8432B9-49EC-5F45-BB96-329B1F2B2254      *EXPLOIT*
|       85FCDCC6-9A03-597E-AB4F-FA4DAC04F8D0    6.8     https://vulners.com/githubexploit/85FCDCC6-9A03-597E-AB4F-FA4DAC04F8D0      *EXPLOIT*
|       1337DAY-ID-39918        6.8     https://vulners.com/zdt/1337DAY-ID-39918        *EXPLOIT*
|       CVE-2025-26466  5.9     https://vulners.com/cve/CVE-2025-26466
|       OSV:BELL-CVE-2025-32728 4.3     https://vulners.com/osv/OSV:BELL-CVE-2025-32728
|       CVE-2025-32728  4.3     https://vulners.com/cve/CVE-2025-32728
|       OSV:BELL-CVE-2025-61985 3.6     https://vulners.com/osv/OSV:BELL-CVE-2025-61985
|       OSV:BELL-CVE-2025-61984 3.6     https://vulners.com/osv/OSV:BELL-CVE-2025-61984
|       CVE-2025-61985  3.6     https://vulners.com/cve/CVE-2025-61985
|       CVE-2025-61984  3.6     https://vulners.com/cve/CVE-2025-61984
|       B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150    3.6     https://vulners.com/githubexploit/B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150      *EXPLOIT*
|_      4C6E2182-0E99-5626-83F6-1646DD648C57    3.6     https://vulners.com/githubexploit/4C6E2182-0E99-5626-83F6-1646DD648C57      *EXPLOIT*
3306/tcp open  mysql   MariaDB 11.4.5
| ssl-dh-params: 
|   VULNERABLE:
|   Anonymous Diffie-Hellman Key Exchange MitM Vulnerability
|     State: VULNERABLE
|       Transport Layer Security (TLS) services that use anonymous
|       Diffie-Hellman key exchange only provide protection against passive
|       eavesdropping, and are vulnerable to active man-in-the-middle attacks
|       which could completely compromise the confidentiality and integrity
|       of any data exchanged over the resulting session.
|     Check results:
|       ANONYMOUS DH GROUP 1
|             Cipher Suite: TLS_DH_anon_WITH_AES_128_CBC_SHA256
|             Modulus Type: Safe prime
|             Modulus Source: Unknown/Custom-generated
|             Modulus Length: 2048
|             Generator Length: 8
|             Public Key Length: 2048
|     References:
|_      https://www.ietf.org/rfc/rfc2246.txt
| vulners: 
|   cpe:/a:mariadb:mariadb:11.4.5: 
|       OSV:BIT-MARIADB-2025-30722      6.8     https://vulners.com/osv/OSV:BIT-MARIADB-2025-30722
|       OSV:BIT-MARIADB-2025-30693      5.5     https://vulners.com/osv/OSV:BIT-MARIADB-2025-30693
|       OSV:BIT-MARIADB-2023-52971      4.9     https://vulners.com/osv/OSV:BIT-MARIADB-2023-52971
|       OSV:BIT-MARIADB-2023-52970      4.9     https://vulners.com/osv/OSV:BIT-MARIADB-2023-52970
|       OSV:BIT-MARIADB-2023-52969      4.9     https://vulners.com/osv/OSV:BIT-MARIADB-2023-52969
|       CVE-2023-52971  4.9     https://vulners.com/cve/CVE-2023-52971
|_      CVE-2023-52970  4.9     https://vulners.com/cve/CVE-2023-52970
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 45.71 seconds

$ cat > ./nmapres_new.txt # сделать подобный пример файлу exmp_targets.txt

┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ cat nmapres_new.txt    
scanme.nmap.org
192.168.31.0/24
192.168.31.1/24
localhost 

┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ grep "VULNERABLE" nmapres_new.txt # осуществляем поиск по словам в файле
|   VULNERABLE:
|     State: VULNERABLE
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ grep "CVE" nmapres_new.txt
|   After NULL UDP avahi packet DoS (CVE-2011-1002).
|       CVE-2025-26465  6.8     https://vulners.com/cve/CVE-2025-26465
|       CVE-2025-26466  5.9     https://vulners.com/cve/CVE-2025-26466
|       OSV:BELL-CVE-2025-32728 4.3     https://vulners.com/osv/OSV:BELL-CVE-2025-32728
|       CVE-2025-32728  4.3     https://vulners.com/cve/CVE-2025-32728
|       OSV:BELL-CVE-2025-61985 3.6     https://vulners.com/osv/OSV:BELL-CVE-2025-61985
|       OSV:BELL-CVE-2025-61984 3.6     https://vulners.com/osv/OSV:BELL-CVE-2025-61984
|       CVE-2025-61985  3.6     https://vulners.com/cve/CVE-2025-61985
|       CVE-2025-61984  3.6     https://vulners.com/cve/CVE-2025-61984
|       CVE-2023-52971  4.9     https://vulners.com/cve/CVE-2023-52971
|_      CVE-2023-52970  4.9     https://vulners.com/cve/CVE-2023-52970
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ grep "EXPLOIT" nmapres_new.txt
|       PACKETSTORM:189283      6.8     https://vulners.com/packetstorm/PACKETSTORM:189283      *EXPLOIT*
|       9D8432B9-49EC-5F45-BB96-329B1F2B2254    6.8     https://vulners.com/githubexploit/9D8432B9-49EC-5F45-BB96-329B1F2B2254      *EXPLOIT*
|       85FCDCC6-9A03-597E-AB4F-FA4DAC04F8D0    6.8     https://vulners.com/githubexploit/85FCDCC6-9A03-597E-AB4F-FA4DAC04F8D0      *EXPLOIT*
|       1337DAY-ID-39918        6.8     https://vulners.com/zdt/1337DAY-ID-39918        *EXPLOIT*
|       B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150    3.6     https://vulners.com/githubexploit/B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150      *EXPLOIT*
|_      4C6E2182-0E99-5626-83F6-1646DD648C57    3.6     https://vulners.com/githubexploit/4C6E2182-0E99-5626-83F6-1646DD648C57      *EXPLOIT*

$ mkdir -p ~/project/reports 

┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ nmap -sV --script vuln --open -oN ~/project/reports/nmapres_new.txt -oX ~/project/reports/nmapres_new.xml localhost # сканируем все порты, так как на 8080 ничего особо нет уязвимого у меня, -oN — сохранить текстовый отчёт, -oX — сохранить XML отчёт, -sV — определение версий сервисов, --script vuln — запуск vuln-скриптов
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-08 21:11 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0000050s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 998 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.9p1 Debian 3 (protocol 2.0)
| vulners: 
|   cpe:/a:openbsd:openssh:9.9p1: 
|       PACKETSTORM:189283      6.8     https://vulners.com/packetstorm/PACKETSTORM:189283      *EXPLOIT*
|       CVE-2025-26465  6.8     https://vulners.com/cve/CVE-2025-26465
|       9D8432B9-49EC-5F45-BB96-329B1F2B2254    6.8     https://vulners.com/githubexploit/9D8432B9-49EC-5F45-BB96-329B1F2B2254      *EXPLOIT*
|       85FCDCC6-9A03-597E-AB4F-FA4DAC04F8D0    6.8     https://vulners.com/githubexploit/85FCDCC6-9A03-597E-AB4F-FA4DAC04F8D0      *EXPLOIT*
|       1337DAY-ID-39918        6.8     https://vulners.com/zdt/1337DAY-ID-39918        *EXPLOIT*
|       CVE-2025-26466  5.9     https://vulners.com/cve/CVE-2025-26466
|       OSV:BELL-CVE-2025-32728 4.3     https://vulners.com/osv/OSV:BELL-CVE-2025-32728
|       CVE-2025-32728  4.3     https://vulners.com/cve/CVE-2025-32728
|       OSV:BELL-CVE-2025-61985 3.6     https://vulners.com/osv/OSV:BELL-CVE-2025-61985
|       OSV:BELL-CVE-2025-61984 3.6     https://vulners.com/osv/OSV:BELL-CVE-2025-61984
|       CVE-2025-61985  3.6     https://vulners.com/cve/CVE-2025-61985
|       CVE-2025-61984  3.6     https://vulners.com/cve/CVE-2025-61984
|       B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150    3.6     https://vulners.com/githubexploit/B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150      *EXPLOIT*
|_      4C6E2182-0E99-5626-83F6-1646DD648C57    3.6     https://vulners.com/githubexploit/4C6E2182-0E99-5626-83F6-1646DD648C57      *EXPLOIT*
3306/tcp open  mysql   MariaDB 11.4.5
| vulners: 
|   cpe:/a:mariadb:mariadb:11.4.5: 
|       OSV:BIT-MARIADB-2025-30722      6.8     https://vulners.com/osv/OSV:BIT-MARIADB-2025-30722
|       OSV:BIT-MARIADB-2025-30693      5.5     https://vulners.com/osv/OSV:BIT-MARIADB-2025-30693
|       OSV:BIT-MARIADB-2023-52971      4.9     https://vulners.com/osv/OSV:BIT-MARIADB-2023-52971
|       OSV:BIT-MARIADB-2023-52970      4.9     https://vulners.com/osv/OSV:BIT-MARIADB-2023-52970
|       OSV:BIT-MARIADB-2023-52969      4.9     https://vulners.com/osv/OSV:BIT-MARIADB-2023-52969
|       CVE-2023-52971  4.9     https://vulners.com/cve/CVE-2023-52971
|_      CVE-2023-52970  4.9     https://vulners.com/cve/CVE-2023-52970
| ssl-dh-params: 
|   VULNERABLE:
|   Anonymous Diffie-Hellman Key Exchange MitM Vulnerability
|     State: VULNERABLE
|       Transport Layer Security (TLS) services that use anonymous
|       Diffie-Hellman key exchange only provide protection against passive
|       eavesdropping, and are vulnerable to active man-in-the-middle attacks
|       which could completely compromise the confidentiality and integrity
|       of any data exchanged over the resulting session.
|     Check results:
|       ANONYMOUS DH GROUP 1
|             Cipher Suite: TLS_DH_anon_WITH_CAMELLIA_128_CBC_SHA
|             Modulus Type: Safe prime
|             Modulus Source: Unknown/Custom-generated
|             Modulus Length: 2048
|             Generator Length: 8
|             Public Key Length: 2048
|     References:
|_      https://www.ietf.org/rfc/rfc2246.txt
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.42 seconds

┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ xsltproc ~/project/reports/nmapres_new.xml -o ~/project/reports/nmapres_new.html # xsltproc — XSLT процессор, делает web-страницу из XML отчёта
 ```
 - [x] 3. Используйте команду `tree` и выведите все вложенные файлы по директориям.
```bash
┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ tree # показываем дерево каталогов и файлов текущей директории рекурсивно
.
├── exmp_targets.txt
├── nmapres_new.txt
├── README.md
└── test_targets.txt

1 directory, 4 files
```
- [x] 4.Найдите IP сетевой карты `Ethernet`, которая соответствует вашей виртуальной машине используя `ifconfig` и выполните команду

```bash
┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ ifconfig # показывает список сетевых интерфейсов, их IP, маски, MAC и т.д.
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.31.41  netmask 255.255.255.0  broadcast 192.168.31.255
        inet6 fe80::6c01:60ec:a5a9:ed73  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:be:7d:82  txqueuelen 1000  (Ethernet)
        RX packets 359553  bytes 423031981 (403.4 MiB)
        RX errors 14442  dropped 0  overruns 0  frame 14442
        TX packets 63360  bytes 4821971 (4.5 MiB)
        TX errors 0  dropped 11 overruns 0  carrier 0  collisions 0\
        
┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ nmap -sP 192.168.31.41       
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-08 21:36 MSK
Nmap scan report for 192.168.31.41
Host is up.
Nmap done: 1 IP address (1 host up) scanned in 0.01 seconds
```

- [x] 5. Определите ОС, данные ssh, telnet  с помощью `nmap` и выведитео них информацию.
```bash
┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ nmap -O 192.168.31.41
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-08 21:17 MSK
Nmap scan report for 192.168.31.41
Host is up (0.000045s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
Device type: general purpose
Running: Linux 2.6.X|5.X
OS CPE: cpe:/o:linux:linux_kernel:2.6.32 cpe:/o:linux:linux_kernel:5 cpe:/o:linux:linux_kernel:6
OS details: Linux 2.6.32, Linux 5.0 - 6.2
Network Distance: 0 hops

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.46 seconds
                                                                                                                   
┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ nmap -sV -p 23 192.168.31.41
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-08 21:20 MSK
Nmap scan report for 192.168.31.41
Host is up (0.000072s latency).

PORT   STATE  SERVICE VERSION
23/tcp closed telnet

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.17 seconds
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ nmap -sV -p 22 192.168.31.41
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-08 21:20 MSK
Nmap scan report for 192.168.31.41
Host is up (0.000082s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.9p1 Debian 3 (protocol 2.0)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.20 seconds
```
- [x] 6. Результаты из `nmapres_new.txt` надо перенести в `nmapres.txt` и оставить оба файла рядом в локальном репозитории. Желательно использовать `cp` в консоли через редактор.
```bash
┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ cp nmapres_new.txt nmapres.txt
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ cp nmapres_new.txt ../lab02/nmapres.txt
                                                                                                                    
┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ ls -l
total 28
-rw-rw-r-- 1 kali kali    65 Dec  8 20:33 exmp_targets.txt
-rw-rw-r-- 1 kali kali  3639 Dec  8 20:19 nmapres_new.txt
-rw-rw-r-- 1 kali kali  3639 Dec  8 21:20 nmapres.txt
-rw-rw-r-- 1 kali kali 10714 Nov 27 13:54 README.md
-rw-rw-r-- 1 kali kali    16 Dec  7 17:02 test_targets.txt

┌──(kali㉿kali)-[~/course_labs/labs/lab03]
└─$ ls -l ../lab02
total 40
-rw-rw-r-- 1 kali kali        414 Nov 27 13:54 exmpl_hello.py
-rw-rw-r-- 1 kali kali       3639 Dec  8 21:21 nmapres.txt
-rw-rw-r-- 1 kali kali        807 Nov 27 13:54 pygamesteel.py
-rw-rw-r-- 1 kali kali      20985 Nov 30 19:42 README.md
-rw-r----- 1 kali readgroup   674 Nov 30 18:18 screen.py
```
- [x] 7. Оформить `README.md` по аналогии и использовать `shield`, etc.
- [x] 8. Составить `gist` отчет и отправить ссылку личным сообщением

***
Copyright (c) 2025 Balashov Denis aka kenifor
