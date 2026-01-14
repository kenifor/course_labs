<div align="center">
<h1><a id="intro">Лабораторная работа №8</a><br></h1>
<a href="https://docs.github.com/en"><img src="https://img.shields.io/static/v1?logo=github&logoColor=fff&label=&message=Docs&color=36393f&style=flat" alt="GitHub Docs"></a>
<a href="https://daringfireball.net/projects/markdown"><img src="https://img.shields.io/static/v1?logo=markdown&logoColor=fff&label=&message=Markdown&color=36393f&style=flat" alt="Markdown"></a>
<a href="https://symbl.cc/en/unicode-table"><img src="https://img.shields.io/static/v1?logo=unicode&logoColor=fff&label=&message=Unicode&color=36393f&style=flat" alt="Unicode"></a>
<a href="https://shields.io"><img src="https://img.shields.io/static/v1?logo=shieldsdotio&logoColor=fff&label=&message=Shields&color=36393f&style=flat" alt="Shields"></a>
<a href="https://img.shields.io/badge/Risk_Analyze-2448a2"><img src="https://img.shields.io/badge/Course-Risk_Analysis-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/AppSec-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/Contributor-Шмаков_И._С.-8b9aff" alt="Contributor Badge"></a></div>

***

Салют :wave:,<br>
Данная лабораторная работа посвящена динамическому анализу безопасности web‑приложений DAST с использованием OWASP ZAP. Вы развернёте уязвимое приложение в Docker, проведете ручное тестирование по инструкции для понимания принципа и логики работы, далее выполните автоматическое сканирование, проанализируете отчёт и опишете уязвимости как и каким образом они реализуются. Аналогично вы проанализируете риски ИБ и предложите меры защиты, внесете необходимые исправления.

Для сдачи данной работы также будет требоваться ответить на дополнительыне вопросы по описанным темам.

***

## Структура репозитория лабораторной работы

```bash
lab08
├── dast
│   ├── convert_reports.py
│   ├── zap_scan.sh
│   └── zap-baseline.conf
├── docker-compose.yml
├── README.md
├── requirements.txt
└── vulnerable-app
    ├── app.py
    ├── Dockerfile
    ├── files
    │   ├── secret.txt
    │   ├── passwords.txt
    │   └── config.json
    └── requirements.txt
```

***

## Материал

- DAST Dynamic Application Security Testing обеспечивает тестирование «чёрного ящика», когда сканер не знает исходного кода и взаимодействует с приложением как внешний клиент:
    -  Отправляет `HTTP`‑запросы
    -  Анализирует ответы
    -  Пытается воспроизвести реальные атаки `XSS`, `SQLi`, уязвимости в заголовках, слабую авторизацию и т.д.

> В отличие от `SAST`/ `SCA`, здесь обязательно нужно живое, запущенное приложение (стенд), к которому есть сетевой доступ и разрешить доступ сканеру
> Инструмент ведёт себя как автоматизированный атакующий: обходит страницы, подставляет полезные нагрузки payloads и фиксирует подозрительные ответы

### OWASP ZAP

Особенности:
- Чёрный ящик: анализ идёт по внешнему интерфейсу `HTTP`/`HTTPS`
- Фокус на эксплуатацию: `SQLi`, `XSS`, `LFI`/ `RFI`, небезопасные заголовки, слабые cookies, открытые админки и т.д. Сканировать как простыми профилями baseline scan, так и агрессивными активными проверками

    > - Автоматически обходить сайт `spider`/ `crawler` и находить новые эндпоинты (входные точки)
    > - Выполнять пассивный анализ - заголовки, `cookies`, версии серверов, утечки данных и активные атаки `XSS`, `SQLi` и др.

- Формировать отчёты в форматах `HTML`, `JSON`, `XML` для дальнейшего анализа и интеграции в `CI/CD`

### Ремарка

Мы используем `owasp/zap2docker-stable` и CLI‑скрипт `zap_scan.sh` для сканирования по URL `http://localhost:8080/` уязвимого приложения Flask. Скрипт запускает `baseline‑скан`, сохраняет отчёты и передаёт JSON на генерацию `ODT/XLSX`.

***

## Задание

- [ ] 1. Разверните и подготовьте окружение для уязвимого приложения

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt -r vulnerable-app/requirements.txt
```

- [ ] 2. Запустите уязвимое приложение

```bash
┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ docker compose up -d --build  # http://localhost:8080
WARN[0000] /home/kali/course_labs/labs/lab08/docker-compose.yml: the attribute `version` is obsolete
[+] Building 30.3s (12/12) FINISHED
 => [vulnerable-app 1/6] FROM docker.io/library/python:3.11-slim             16.7s
 => [vulnerable-app 2/6] WORKDIR /app                                          0.3s
 => [vulnerable-app 3/6] COPY requirements.txt .                               0.1s
 => [vulnerable-app 4/6] RUN pip install --no-cache-dir -r requirements.txt    9.0s
 => [vulnerable-app 5/6] COPY app.py .                                         0.1s
 => [vulnerable-app 6/6] COPY files/ ./files/                                  0.1s
 => [vulnerable-app] exporting to image                                        0.2s
[+] Running 3/3
 ✔ Network lab08-net               Created
 ✔ Container lab08-vulnerable-app  Started
```

- [ ] 3. Проверьте доступность приложения

```bash
┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ curl -i http://localhost:8080
HTTP/1.1 200 OK
Server: Werkzeug/2.2.3 Python/3.11.14
Date: Wed, 14 Jan 2026 12:32:49 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 625
Set-Cookie: session=guest-session-id; Path=/
Connection: close


    <h1>Vulnerable DAST Demo App</h1>
    <p>Пример уязвимого приложения для лабораторной по DAST.</p>
    <ul>
      <li><a href="/echo?msg=Hello">Reflected XSS / echo</a></li>
      <li><a href="/search?username=admin">SQL Injection / search</a></li>
      <li><a href="/login">Небезопасный логин</a></li>
      <li><a href="/profile">Профиль (зависит от cookie)</a></li>
      <li><a href="/admin">«Админка» без нормальной авторизации</a></li>
      <li><a href="/files/">Directory listing</a></li>
    </ul>
```

- [ ] 4. Проведите ручное исследование уязвимостей и опишите почему такое происходит, каким образом реализуются уязвимости и дайте им определение
- [ ] 4.1. `/echo` - проверить отражение параметра  `msg`  в `HTML` и использовать `payload` вида  `<script>alert('XSS')</script>` зафиксировав его поведение

```bash
┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ curl --url-query "msg=<script>alert('hack with XSS')</script>" http://localhost:8080/echo
    <h2>Echo</h2>
    <p>Сообщение: <script>alert('hack with XSS')</script></p>
    <p>Попробуйте передать что-нибудь вроде: <code>&lt;script&gt;alert('XSS')&lt;/script&gt;</code></p>
    <a href="/">Назад</a>
```

**Анализ XSS уязвимости:**

**Определение:** Reflected XSS (отражённый межсайтовый скриптинг) — уязвимость, при которой вредоносный скрипт внедряется через параметры запроса и немедленно отражается в ответе без фильтрации.

**Причина:** В `app.py:68` используется `.format(msg=msg)` с `render_template_string()`. Пользовательский ввод напрямую вставляется в HTML без экранирования специальных символов.

**Механизм эксплуатации:**
1. Атакующий отправляет URL с вредоносным JavaScript кодом в параметре `msg`
2. Сервер вставляет код напрямую в HTML-страницу
3. Браузер жертвы выполняет JavaScript код

**Последствия:** Кража cookies, перехват сессии, фишинг, кейлоггинг, редирект на вредоносные сайты.

**Риск:** ВЫСОКИЙ — выполнение произвольного JavaScript кода в контексте приложения.

- [ ] 4.2. `/search` - проверить обычный запрос  `?username=admin` и использовать строку  `?username=admin' OR '1'='1` зафиксировав его поведение описав признак SQLi

```bash
┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ curl --url-query "username=admin" http://localhost:8080/search
    <h2>Поиск пользователя</h2>
    <p>Запрос: <code>SELECT id, username, role FROM users WHERE username = &#39;admin&#39;</code></p>

      <ul>
        <li>3 – admin (admin)</li>
      </ul>

┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ curl --url-query "username=admin' OR '1'='1" http://localhost:8080/search
    <h2>Поиск пользователя</h2>
    <p>Запрос: <code>SELECT id, username, role FROM users WHERE username = &#39;admin&#39; OR &#39;1&#39;=&#39;1&#39;</code></p>

      <ul>
        <li>3 – admin (admin)</li>
        <li>4 – user (user)</li>
      </ul>
```

**Анализ SQL Injection:**

**Определение:** SQL Injection — внедрение вредоносного SQL кода через пользовательский ввод для манипуляции базой данных.

**Причина:** В `app.py:77, 130` используется f-string конкатенация: `f"SELECT ... WHERE username = '{username}'"`. Отсутствует параметризация запросов.

**Механизм:** Payload `admin' OR '1'='1` замыкает кавычку и добавляет условие, всегда истинное (`'1'='1'`), возвращая все записи.

**Риск:** КРИТИЧЕСКИЙ — извлечение всех данных БД, модификация/удаление данных, обход аутентификации, выполнение системных команд.

- [ ] 4.3. `/login` - войти под  `admin`  и  `user` проверив логику на открытые пароли и простые SQL‑запросы

```bash
┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ curl -X POST -d "username=admin&password=admin123" http://localhost:8080/login
<h2>Добро пожаловать, admin (admin)!</h2><a href='/'>На главную</a>

┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ curl -X POST -d "username=user&password=user123" http://localhost:8080/login
<h2>Добро пожаловать, user (user)!</h2><a href='/'>На главную</a>
```

**Анализ Login уязвимостей:**

**Проблемы:**
1. **Hardcoded credentials** — пароли захардкожены в коде (`app.py:32-36`)
2. **Plaintext passwords** — пароли хранятся в открытом виде в БД
3. **SQL Injection** — аналогичная уязвимость через f-string (`app.py:130`)
4. **No rate limiting** — отсутствует защита от brute-force

**Риск:** КРИТИЧЕСКИЙ — полный компромисс системы аутентификации.

- [ ] 4.4. `/profile` - изменить `cookie  role`  на  `admin`  через `DevTools` → `Application` → `Cookies` и обновить  `/profile` (возможно создать `cookie`)

```bash
┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ curl -b "role=guest" http://localhost:8080/profile
    <h2>Профиль пользователя</h2>
    <p>Имя: guest</p>
    <p>Роль: guest</p>

┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ curl -b "role=admin" http://localhost:8080/profile
    <h2>Профиль пользователя</h2>
    <p>Имя: guest</p>
    <p>Роль: admin</p>
```

**Анализ Cookie Manipulation:**

**Определение:** Insecure Cookie — уязвимость, позволяющая клиенту подделывать cookies без серверной валидации.

**Причина:** В `app.py:140-141` cookies устанавливаются без подписи/шифрования. Сервер доверяет значениям из `request.cookies.get()` (`app.py:151-152, 166`).

**Риск:** ВЫСОКИЙ — privilege escalation, обход авторизации, персонализация от имени других пользователей.

- [ ] 4.5. `/admin` -  проверить, что доступ запрещён без `cookie  role=admin` и далее подделать `cookie`, что «админка» открывается путем изменения через `DevTools`. **Подсказка:** доступ завязан на значение cookie, без подписи/ токена/ серверной проверки.

```bash
┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ curl http://localhost:8080/admin
<h2>Доступ запрещён: вы не admin</h2><p>Попробуйте изменить cookie 'role'.</p><a href='/'>Назад</a>

┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ curl -b "role=admin" http://localhost:8080/admin
    <h2>Admin panel</h2>
    <p>Секретные настройки приложения (демо).</p>
    <ul>
      <li>DEBUG: true</li>
      <li>FEATURE_FLAG: experimental_mode</li>
    </ul>
```

**Анализ Admin Panel Access Control:**

**Определение:** Broken Access Control — отсутствие надёжной проверки прав доступа на серверной стороне.

**Причина:** В `app.py:166-167` проверка роли выполняется только через `request.cookies.get("role")` без криптографической подписи, server-side session или JWT токенов.

**Риск:** КРИТИЧЕСКИЙ — несанкционированный доступ к админ-панели, раскрытие конфиденциальных настроек, возможность управления системой.

- [ ] 4.6. `/files/` - просмотрите `directory listing` и откройте один из файлов убедившись, что оно выводится

```bash
┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ curl http://localhost:8080/files/
        <h2>Files under /files/</h2>
        <ul><li><a href='/files/config.json'>config.json</a></li><li><a href='/files/secret.txt'>secret.txt</a></li><li><a href='/files/passwords.txt'>passwords.txt</a></li></ul>

┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ curl http://localhost:8080/files/secret.txt
<pre>SECRET_TOKEN=123456
</pre>

┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ curl http://localhost:8080/files/passwords.txt
<pre>admin:admin123
user:user123
database_password:superSecretPass2024
api_key:ABC-DEF-GHI-JKL-MNO
</pre>

┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ curl http://localhost:8080/files/config.json
<pre>{
  "database": {
    "host": "localhost",
    "port": 5432,
    "username": "dbadmin",
    "password": "dbpass123"
  },
  "api": {
    "key": "sk_live_51234567890abcdef",
    "secret": "whsec_9876543210fedcba"
  }
}
</pre>
```

**Анализ Directory Listing:**

**Определение:** Directory Listing — уязвимость, позволяющая атакующему просматривать содержимое директорий и скачивать файлы без авторизации.

**Причина:** В `app.py:197` используется `os.listdir()` без ограничений. Все файлы в директории `/files/` доступны для чтения.

**Риск:** КРИТИЧЕСКИЙ — раскрытие конфиденциальной информации: токенов, паролей, ключей API, конфигураций БД.

- [ ] 5. Доработайте по пп 4 лабораторную работу развив их содержимое, которое может выводиться (мин 1 пример)

**Выполнено:** Добавлены файлы `passwords.txt` и `config.json` с примерами конфиденциальных данных для демонстрации серьёзности уязвимости Directory Listing.

- [ ] 6. Поставьте `OWASP ZAP` и стяните образ конкртеной версии для него

```bash
┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ sudo docker pull ghcr.io/zaproxy/zaproxy:stable
stable: Pulling from zaproxy/zaproxy
ae4ce04d0e1c: Pull complete
9cc7b9ca7788: Pull complete
f366d434b6fc: Pull complete
bf2297e7cd8d: Pull complete
87ba3504d442: Pull complete
08eef0be2aa4: Pull complete
4f4fb700ef54: Pull complete
e0a7ecd670cf: Pull complete
5d35d2f8c19f: Pull complete
66e55ea493c9: Pull complete
ff34a238b9c4: Pull complete
a3ce4dd8a0be: Pull complete
eab29e9c387d: Pull complete
a1b9d5c7d548: Pull complete
fb15404aa629: Pull complete
e54ee67029ae: Pull complete
dc5d46bcd90b: Pull complete
9e9c2f9e1f29: Pull complete
108c5836e3c7: Pull complete
de833ed2578d: Pull complete
Digest: sha256:8e79e827afb9e8bdba390c829eb3062062cdb407570559e2ddebd49130c00a59
Status: Downloaded newer image for ghcr.io/zaproxy/zaproxy:stable
ghcr.io/zaproxy/zaproxy:stable
```

- [ ] 7. Задайте переменные окружения для работы скриптов

```bash
┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ export ZAP_IMAGE=ghcr.io/zaproxy/zaproxy:stable
$ export TARGET_URL=http://172.18.0.2:8080  # Container IP in Docker network
$ echo "ZAP_IMAGE=$ZAP_IMAGE"
ZAP_IMAGE=ghcr.io/zaproxy/zaproxy:stable

┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ echo "TARGET_URL=$TARGET_URL"
TARGET_URL=http://172.18.0.2:8080
```

- [ ] 8. Запустите скрипт автоматического сканирования DAST `OWASP ZAP`

```bash
┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ chmod +x dast/zap_scan.sh
$ sudo docker run --rm --network lab08-net -v "$(pwd)/dast/reports:/zap/wrk" ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://172.18.0.2:8080 -r "zap-report-20260114_154633.html" -J "zap-report-20260114_154633.json" -x "zap-report-20260114_154633.xml" -I
[*] Running OWASP ZAP baseline scan against http://172.18.0.2:8080
Using the Automation Framework
Total of 15 URLs

PASS: Vulnerable JS Library (Powered by Retire.js) [10003]
PASS: In Page Banner Information Leak [10009]
PASS: Cookie Without Secure Flag [10011]
WARN-NEW: Cookie No HttpOnly Flag [10010] x 2
	http://172.18.0.2:8080 (200 OK)
	http://172.18.0.2:8080/ (200 OK)
WARN-NEW: Missing Anti-clickjacking Header [10020] x 4
	http://172.18.0.2:8080 (200 OK)
	http://172.18.0.2:8080/echo?msg=Hello (200 OK)
	http://172.18.0.2:8080/login (200 OK)
	http://172.18.0.2:8080/profile (200 OK)
WARN-NEW: X-Content-Type-Options Header Missing [10021] x 5
	http://172.18.0.2:8080 (200 OK)
	http://172.18.0.2:8080/echo?msg=Hello (200 OK)
	http://172.18.0.2:8080/login (200 OK)
	http://172.18.0.2:8080/profile (200 OK)
	http://172.18.0.2:8080/search?username=admin (200 OK)
WARN-NEW: Information Disclosure - Sensitive Information in URL [10024] x 1
	http://172.18.0.2:8080/search?username=admin (200 OK)
WARN-NEW: Server Leaks Version Information via "Server" HTTP Response Header Field [10036] x 5
	http://172.18.0.2:8080 (200 OK)
	http://172.18.0.2:8080/login (200 OK)
	http://172.18.0.2:8080/profile (200 OK)
	http://172.18.0.2:8080/robots.txt (404 Not Found)
	http://172.18.0.2:8080/sitemap.xml (404 Not Found)
WARN-NEW: Content Security Policy (CSP) Header Not Set [10038] x 3
	http://172.18.0.2:8080 (200 OK)
	http://172.18.0.2:8080/login (200 OK)
	http://172.18.0.2:8080/profile (200 OK)
WARN-NEW: Non-Storable Content [10049] x 6
	http://172.18.0.2:8080/admin (403 Forbidden)
	http://172.18.0.2:8080 (200 OK)
	http://172.18.0.2:8080/login (200 OK)
	http://172.18.0.2:8080/profile (200 OK)
	http://172.18.0.2:8080/robots.txt (404 Not Found)
WARN-NEW: Cookie without SameSite Attribute [10054] x 2
	http://172.18.0.2:8080 (200 OK)
	http://172.18.0.2:8080/ (200 OK)
WARN-NEW: Permissions Policy Header Not Set [10063] x 5
	http://172.18.0.2:8080 (200 OK)
	http://172.18.0.2:8080/login (200 OK)
	http://172.18.0.2:8080/profile (200 OK)
	http://172.18.0.2:8080/robots.txt (404 Not Found)
	http://172.18.0.2:8080/sitemap.xml (404 Not Found)
WARN-NEW: Source Code Disclosure - SQL [10099] x 1
	http://172.18.0.2:8080/search?username=admin (200 OK)
WARN-NEW: Authentication Request Identified [10111] x 1
	http://172.18.0.2:8080/login (200 OK)
WARN-NEW: Session Management Response Identified [10112] x 3
	http://172.18.0.2:8080 (200 OK)
	http://172.18.0.2:8080/ (200 OK)
	http://172.18.0.2:8080/ (200 OK)
WARN-NEW: Insufficient Site Isolation Against Spectre Vulnerability [90004] x 12
	http://172.18.0.2:8080 (200 OK)
	http://172.18.0.2:8080/echo?msg=Hello (200 OK)
	http://172.18.0.2:8080/login (200 OK)
	http://172.18.0.2:8080/profile (200 OK)
	http://172.18.0.2:8080 (200 OK)

FAIL-NEW: 0	FAIL-INPROG: 0	WARN-NEW: 13	WARN-INPROG: 0	INFO: 0	IGNORE: 0	PASS: 54

┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ ls -lh dast/reports/
-rw-r--r-- 1 kali kali 98K Jan 14 15:47 zap-report-20260114_154633.html
-rw-r--r-- 1 kali kali 36K Jan 14 15:47 zap-report-20260114_154633.json
-rw-r--r-- 1 kali kali 43K Jan 14 15:47 zap-report-20260114_154633.xml

┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab08]
└─$ /home/kali/course_labs/labs/lab08/venv/bin/python dast/convert_reports.py 20260114_154633
[*] Parsing ZAP JSON report: zap-report-20260114_154633.json
[i] Found 14 alerts
[+] ODT report saved: odt/zap-report-20260114_154633.odt
[+] XLSX report saved: xlsx/zap-report-20260114_154633.xlsx
[+] Report conversion completed!
```

- [ ] 9. Изучите сгенерированные отчеты в `dast/reports` и опишите риски ИБ для них, без сценариев, так как ранее вы видели часть из их реализации

## Анализ рисков информационной безопасности (DAST отчёт)

### Найденные уязвимости (13 типов):

#### 1. Cookie No HttpOnly Flag (СРЕДНИЙ риск, CWE-1004)
- Cookies устанавливаются без флага `HttpOnly`
- При XSS атаке возможна кража session cookies
- Затронуто: `/`, `/login`

#### 2. Missing Anti-clickjacking Header (СРЕДНИЙ риск, CWE-693)
- Отсутствует `X-Frame-Options` или CSP `frame-ancestors`
- Возможны clickjacking атаки через iframe
- Затронуто: `/`, `/echo`, `/login`, `/profile`

#### 3. X-Content-Type-Options Header Missing (НИЗКИЙ риск, CWE-693)
- Отсутствует заголовок `nosniff`
- Браузер может неправильно интерпретировать MIME-тип
- Затронуто: 5 endpoints

#### 4. Content Security Policy Header Not Set (СРЕДНИЙ риск, CWE-693)
- Отсутствует CSP
- Нет защиты от XSS и data injection атак
- Затронуто: `/`, `/login`, `/profile`

#### 5. Cookie without SameSite Attribute (НИЗКИЙ риск, CWE-1275)
- Cookies без атрибута `SameSite`
- Уязвимость к CSRF атакам
- Затронуто: `/`, `/`

#### 6. Server Leaks Version Information (НИЗКИЙ риск, CWE-200)
- Заголовок `Server` раскрывает: `Werkzeug/2.2.3 Python/3.11.14`
- Облегчает поиск известных уязвимостей
- Затронуто: все страницы

#### 7. Source Code Disclosure - SQL (СРЕДНИЙ риск, CWE-540)
- SQL запросы видны в HTML ответе
- Раскрытие структуры БД
- Затронуто: `/search?username=admin`

#### 8. Information Disclosure in URL (СРЕДНИЙ риск, CWE-200)
- Чувствительная информация в URL параметрах
- Утечка через логи сервера/браузера
- Затронуто: `/search?username=admin`

#### 9. Permissions Policy Header Not Set (НИЗКИЙ риск, CWE-693)
- Отсутствует контроль браузерных API
- Нет ограничения геолокации, камеры, микрофона
- Затронуто: все страницы

#### 10. Insufficient Site Isolation Against Spectre (НИЗКИЙ риск, CWE-1303)
- Отсутствуют заголовки защиты от Spectre
- Теоретическая возможность side-channel атак
- Затронуто: 12 экземпляров

### Сводка по уровням риска:
- **КРИТИЧЕСКИЙ:** 0
- **ВЫСОКИЙ:** 0
- **СРЕДНИЙ:** 5 типов
- **НИЗКИЙ:** 5 типов

**Общий вывод:** В сочетании с XSS и SQL Injection уязвимостями, общий уровень риска оценивается как **ВЫСОКИЙ**.

- [ ] 10. Внесите исправления по данному отчету `DAST` для `vulnerable-app/app.py`

## Внесённые исправления в app.py

### 1. XSS Protection (строки 63-70)
```python
# До: template.format(msg=msg)
# После: render_template_string(template, msg=msg)  # Jinja2 auto-escaping
```

### 2. SQL Injection Protection (строки 78-84, 130-132)
```python
# До: f"SELECT ... WHERE username = '{username}'"
# После: cur.execute("SELECT ... WHERE username = ?", (username,))
```

### 3. Password Hashing (строки 30-59)
```python
# Добавлена функция hash_password() с SHA-256
# Пароли хранятся в хешированном виде
# Добавлена поддержка переменных окружения ADMIN_PASSWORD, USER_PASSWORD
```

### 4. Security Headers Middleware (строки 19-27)
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response
```

### 5. Secure Cookies (строки 56, 143-145)
```python
# Добавлены флаги безопасности
resp.set_cookie("session", "guest-session-id", httponly=True, secure=True, samesite='Lax')
resp.set_cookie("user", uname, httponly=True, secure=True, samesite='Lax')
resp.set_cookie("role", role, httponly=True, secure=True, samesite='Lax')
resp.set_cookie("session_token", session_token, httponly=True, secure=True, samesite='Lax')
```

### 6. Directory Traversal Protection (строки 185-213)
```python
# Добавлена whitelist файлов
ALLOWED_FILES = []  # Полный запрет доступа к файлам

# Проверка path traversal
full_path = os.path.abspath(os.path.join(target_dir, subpath))
if not full_path.startswith(target_dir):
    return "<h2>Доступ запрещён</h2>", 403

# Запрет directory listing
if os.path.isdir(full_path):
    return "<h2>Доступ к директориям запрещён</h2>", 403

# Проверка whitelist
if subpath not in ALLOWED_FILES:
    return "<h2>Доступ к этому файлу запрещён</h2>", 403
```

### 7. Debug Mode Control (строки 216-220)
```python
# debug=True заменён на переменную окружения
debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
app.run(host="0.0.0.0", port=8080, debug=debug_mode)
```

### 8. Session Management (строки 14-15, 138)
```python
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))
session_token = secrets.token_hex(16)  # Server-side session token
```

- [ ] 11. Делайте все необходимые коммиты по шагам и отправляйте изменения в удалённый репозиторий
- [ ] 12. Подготовьте отчет `gist`.
- [ ] 14. Почистите кеш от `venv` и остановите уязвимое приложение

```bash
$ deactivate
$ rm -rf venv
$ docker-compose -f docker-compose.yml down
$ docker system prune -f
```

***

## Рекомендации

- `XSS` на `echo` — отражение входных данных без экранирования
>   Заменить прямую подстановку строки на безопасный рендер с автоматическим экранированием или ручной фильтрацией
- `SQL Injection` на `search` — небезопасная конкатенация строки запроса
>   Перейти на параметризованные запросы `sqlite` и передача параметров отдельным аргументом, включая отказа от конкатенации `SQL`‑строк с пользовательским вводом
- Небезопасные `cookies` (`session`, `user`, `role` ) — без  `Secure`,  `HttpOnly`, `SameSite`
>   Задать флаги  `HttpOnly`,  `Secure` (если `HTTPS`), `SameSite=Lax/ Strict`
- Отсутствие основных `security‑headers` (`X-Frame-Options`, `X-Content-Type-Options`, `Content-Security-Policy` и т.д.)
- Усилить авторизацию на  `admin`  из-за доступа по подделанному cookie
- `Directory listing` на  `files`
> Ограничить список отдаваемых ресурсов, либо скрыть `directory listing`, либо добавить проверки и фильтрацию путей.

***

## Links

- [Docker](https://docs.docker.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [odfpy – OpenDocument API for Python](https://github.com/eea/odfpy)
- [openpyxl – Excel files in Python](https://openpyxl.readthedocs.io/)
- [Markdown](https://stackedit.io)
- [Gist](https://gist.github.com)
- [GitHub CLI](https://cli.github.com)
- [OWASP ZAP](https://www.zaproxy.org/)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP Top 10 Web Application Security Risks](https://owasp.org/www-project-top-ten/)
- [ZAP Docker images](https://www.zaproxy.org/docs/docker/)
- [ZAP Baseline Scan](https://www.zaproxy.org/docs/docker/baseline-scan/)
- [ZAP Automation Framework](https://www.zaproxy.org/docs/desktop/addons/automation-framework/)

Copyright (c) 2025 Elijah S Shmakov

![Logo](../../assets/logotype/logo.jpg)
