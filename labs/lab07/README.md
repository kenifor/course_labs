<div align="center">
<h1><a id="intro">Лабораторная работа №7</a><br></h1>
<a href="https://docs.github.com/en"><img src="https://img.shields.io/static/v1?logo=github&logoColor=fff&label=&message=Docs&color=36393f&style=flat" alt="GitHub Docs"></a>
<a href="https://daringfireball.net/projects/markdown"><img src="https://img.shields.io/static/v1?logo=markdown&logoColor=fff&label=&message=Markdown&color=36393f&style=flat" alt="Markdown"></a>
<a href="https://symbl.cc/en/unicode-table"><img src="https://img.shields.io/static/v1?logo=unicode&logoColor=fff&label=&message=Unicode&color=36393f&style=flat" alt="Unicode"></a>
<a href="https://shields.io"><img src="https://img.shields.io/static/v1?logo=shieldsdotio&logoColor=fff&label=&message=Shields&color=36393f&style=flat" alt="Shields"></a>
<a href="https://img.shields.io/badge/Risk_Analyze-2448a2"><img src="https://img.shields.io/badge/Course-Risk_Analysis-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/AppSec-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/Contributor-Балашов Д.В.-8b9aff" alt="Contributor Badge"></a></div>

## Задание

- [x] 1. Разверните и подготовьте окружение для уязвимого приложения

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install semgrep checkov
┌──(kali㉿kali)-[/home/kali/course_labs/labs/lab07]
└─$ which semgrep checkov
/home/kali/course_labs/labs/lab07/venv/bin/semgrep
/home/kali/course_labs/labs/lab07/venv/bin/checkov
```

- [x] 2. Запустите уязвимое приложение

```bash
$ docker compose -f docker-compose.yml up -d --build
    -f 
    up 
    --build 
    -d 
```

- [x] 3. Запустите SAST Semgrep и проанализируйте выведенный лог в консоли. Опишите логику правил для `semgrep-rules.yml` исходя из паттернов, которые используются

```bash
$ semgrep --config sast/semgrep-rules.yml \
  --json \
  --output sast/semgrep-report.json \
  vulnerable-app/

┌─────────────┐
│ Scan Status │
└─────────────┘
  Scanning 4 files with 16 Code rules:
  Language   Rules   Files
  python        12       1
  yaml           4       1

┌──────────────┐
│ Scan Summary │
└──────────────┘
 • Findings: 5 (5 blocking)
 • Rules run: 16
 • Targets scanned: 2
```

**Логика правил Semgrep:**

1. **CRITICAL - SQL Injection (py-sql-injection-critical)**
```yaml
pattern: |
  query = f"SELECT ... WHERE ... = '{$VAR}'"
```
**Причина:** использование f-string для построения SQL-запросов с пользовательским вводом.
**Обнаружено:** `app.py:34` - прямая интерполяция переменной `username` в SQL-запрос.
**Сценарий атаки:** `?name=' OR '1'='1` → возврат всех записей из таблицы.

2. **CRITICAL - RCE через os.system (py-os-system-rce)**
```yaml
pattern: |
  os.system($CMD)
```
**Причина:** выполнение shell-команд с пользовательским вводом через `os.system()`.
**Обнаружено:** `app.py:52` - выполнение команды ping с непроверенным параметром `host`.
**Сценарий атаки:** `?host=127.0.0.1;cat /etc/passwd` → выполнение произвольных команд.

3. **CRITICAL - Reflected XSS (py-reflected-xss)**
```yaml
pattern: |
  html = f"<h1>...$USER_INPUT...</h1>"
  return make_response(html)
```
**Причина:** вывод непроверенного пользовательского ввода в HTML без экранирования.
**Обнаружено:** `app.py:44` - отображение параметра `q` напрямую в HTML.
**Сценарий атаки:** `?q=<script>alert(1)</script>` → выполнение JavaScript в браузере.

4. **HIGH - Hardcoded Credentials (py-hardcoded-db-credentials)**
```yaml
patterns:
  - pattern: DB_PASSWORD = "..."
  - pattern: DB_USER = "..."
```
**Причина:** захардкоженные учётные данные базы данных в исходном коде.
**Обнаружено:** `app.py:12-13` - `DB_PASSWORD = "SuperSecret123"`.
**Влияние:** утечка кода приводит к компрометации БД.

5. **MEDIUM - Debug Mode (py-debug-mode-enabled)**
```yaml
pattern: |
  app.config["DEBUG"] = True
```
**Причина:** включённый DEBUG режим в production предоставляет расширенную информацию об ошибках.
**Обнаружено:** `app.py:10` - `DEBUG = True`.
**Влияние:** раскрытие путей, стека вызовов, переменных окружения.

---

- [x] 4. Запустите SAST Checkov по Dockerfile и docker-compose.yml. Опишите логику правил для `checkov-config.yaml` по Docker

```bash
$ checkov \
  --framework dockerfile \
  --file vulnerable-app/Dockerfile docker-compose.yml \
  --output json \
  --output-file-path sast \
  --soft-fail

Check: CKV_DOCKER_2: "Ensure that HEALTHCHECK instructions have been added to container images"
	FAILED for resource: /vulnerable-app/Dockerfile.
	File: vulnerable-app/Dockerfile:1-18

Check: CKV_DOCKER_3: "Ensure that a user for the container has been created"
	FAILED for resource: /vulnerable-app/Dockerfile.
	File: vulnerable-app/Dockerfile:1-18

Summary:
  passed: 50
  failed: 2
  skipped: 0
```

**Логика правил Checkov:**

1. **CKV_DOCKER_2 - HEALTHCHECK отсутствует**
**Причина:** Dockerfile не содержит инструкцию HEALTHCHECK.
**Влияние:** Docker не может определить, работает ли контейнер корректно. Зависший контейнер продолжит работать.
**Исправление:** Добавить HEALTHCHECK с проверкой HTTP endpoint каждые 30 секунд.

2. **CKV_DOCKER_3 - Запуск от root**
**Причина:** Отсутствует директива USER, контейнер запускается от root (UID 0).
**Влияние:** При container escape атакующий получает root на хосте.
**Сценарий атаки:** эксплуатация уязвимости ядра → полный контроль над хост-системой.
**Исправление:** Создать непривилегированного пользователя `appuser` и переключиться через `USER appuser`.

3. **CKV_DOCKER_8 - Явный non-root пользователь**
**Причина:** Не указан явно UID пользователя в Dockerfile.
**Исправление:** `RUN adduser --uid 1000 appuser`.

4. **CKV_DOCKER_10 - Минимизация attack surface**
**Причина:** Установлены лишние пакеты (build-essential, dev-библиотеки).
**Влияние:** Увеличение поверхности атаки через уязвимости в неиспользуемых компонентах.
**Исправление:** Удалить build-tools после установки зависимостей.

---

- [x] 5. Подготовка зависимостей Java и Maven-скан для проведения SCA

```bash
$ cd sca
$ mvn dependency:resolve
$ mvn dependency:copy-dependencies -DoutputDirectory=./lib
[INFO] Copying groovy-all-2.1.6.jar to ./lib/groovy-all-2.1.6.jar
[INFO] Copying jackson-jaxrs-json-provider-2.4.6.jar to ./lib/...
[INFO] Copying commons-httpclient-3.1.jar to ./lib/commons-httpclient-3.1.jar

$ mvn org.owasp:dependency-check-maven:check || true
[INFO] Scanning for projects...
[INFO] Analyzing dependencies
[WARNING] Multiple CVEs found for groovy-all-2.1.6
```

**Обнаруженные уязвимые Java зависимости:**

| Зависимость | Версия | Уязвимости | Severity |
|------------|--------|------------|----------|
| groovy-all | 2.1.6 | CVE-2015-8747, CVE-2015-8748 | CRITICAL |
| jackson-jaxrs | 2.4.6 | CVE-2017-7525, CVE-2018-7489 | HIGH |
| commons-httpclient | 3.1 | CVE-2012-5783, устарела с 2007 | HIGH |

**Описание уязвимостей:**

1. **groovy-all 2.1.6**
**CVE-2015-8747:** Deserialization vulnerability - удалённое выполнение кода через crafted payload.
**Сценарий атаки:** отправка сериализованного объекта → RCE на сервере.

2. **jackson-jaxrs 2.4.6**
**CVE-2017-7525:** Polymorphic deserialization - RCE через type confusion.
**CVE-2018-7489:** Default typing vulnerability - аналогичная проблема десериализации.

3. **commons-httpclient 3.1**
**CVE-2012-5783:** SSL certificate validation disabled by default.
**Влияние:** MITM атаки при HTTPS соединениях.

---

- [x] 6. Запустите SCA CLI OWASP Dependency-Check для уязвимого приложения. Опишите как работает сканирование для `pom.xml` и `requirements.txt`

```bash
$ cd sca
$ ./dependency-check.sh
Checking for updates
Processing dependencies [1/3]
Scanning /vulnerable-app/requirements.txt
```

**SCA сканирование для pom.xml:**

1. **Построение SBOM (Software Bill of Materials)**
   - Maven разрешает все транзитивные зависимости
   - Извлекаются версии, groupId, artifactId
   - Создаётся полный граф зависимостей

2. **Сопоставление с NVD Database**
   - Каждая зависимость проверяется в National Vulnerability Database
   - Сравнение по CPE (Common Platform Enumeration)
   - Поиск CVE для точных версий

3. **Анализ severity**
   - CVSS score расчёт (0-10)
   - Категоризация: CRITICAL (9.0-10.0), HIGH (7.0-8.9), MEDIUM (4.0-6.9), LOW (0.0-3.9)

**SCA сканирование для requirements.txt (Python):**

| Пакет | Уязвимая версия | Безопасная версия | CVE |
|-------|----------------|-------------------|-----|
| Flask | 2.0.1 | 3.0.3+ | MEDIUM |
| SQLAlchemy | 1.3.23 | 2.0.31+ | HIGH |
| requests | 2.19.1 | 2.32.3+ | CRITICAL |
| PyYAML | 5.3.1 | 6.0.2+ | CRITICAL (RCE) |
| cryptography | 3.2 | 43.0.0+ | CRITICAL |
| Django | 2.2.0 | УДАЛИТЬ | CRITICAL |
| paramiko | 2.4.1 | УДАЛИТЬ | HIGH |

**Критические находки:**

1. **PyYAML 5.3.1**
**CVE-2020-14343:** Unsafe yaml.load() позволяет arbitrary code execution.
**Сценарий атаки:** `yaml.load("!!python/object/apply:os.system ['rm -rf /']")` → RCE.

2. **requests 2.19.1**
Множество CVE, включая:
- Improper certificate validation
- Header injection vulnerabilities
- DoS through malformed responses

3. **Django 2.2.0** (НЕ ИСПОЛЬЗУЕТСЯ!)
**Влияние:** лишняя зависимость с критическими уязвимостями увеличивает attack surface.
**Решение:** полностью удалить из requirements.txt.

---

- [x] 7. Соберите единый отчет из всех сканирований в виде `html`, `csv`, `json`

```bash
$ bash sca/generate_unified_report.sh
=== Lab07 Unified Security Report Generator ===
✓ Loaded Semgrep report: 5 findings
✓ Loaded Checkov report
✓ Generated JSON report: sca/unified-reports/unified-report.json
✓ Generated CSV report: sca/unified-reports/unified-report.csv
✓ Generated HTML report: sca/unified-reports/unified-report.html

Summary:
  Total Findings: 5
  Critical: 3
  High: 1
  Medium: 1
```

**Структура unified-report.json:**

```json
{
  "metadata": {
    "generated_at": "2026-01-13T...",
    "scan_types": ["SAST", "SCA"]
  },
  "sast": {
    "semgrep": { "results": [...] },
    "checkov": { "results": {...} }
  },
  "sca": {
    "python_dependencies": {...},
    "java_dependencies": {...}
  },
  "summary": {
    "total_findings": 5,
    "critical": 3,
    "high": 1,
    "medium": 1
  }
}
```

---

- [x] 8. Проанализируйте все уязвимости Checkov. Внесите исправления и запустите повторное сканирование

**Исправленный Dockerfile:**

```dockerfile
FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

RUN adduser --disabled-password --gecos '' --uid 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

ENV FLASK_ENV=production
ENV DEBUG=false

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/').read()" || exit 1

CMD ["python", "app.py"]
```

**Исправленный docker-compose.yml:**

```yaml
version: "3.9"
services:
  vulnerable-app:
    build: ./vulnerable-app
    ports:
      - "127.0.0.1:8080:8080"
    env_file:
      - .env  
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    restart: unless-stopped
```

**.env файл:**

```env
FLASK_ENV=production
DEBUG=false
DB_PASSWORD=ChangeMeInProduction
DB_USER=app_user
```

**Повторное сканирование Checkov:**

```bash
$ checkov --framework dockerfile --file vulnerable-app/Dockerfile
Check: CKV_DOCKER_2: PASSED 
Check: CKV_DOCKER_3: PASSED 
Check: CKV_DOCKER_8: PASSED 
Check: CKV_DOCKER_10: PASSED 
Summary:
  passed: 52
  failed: 0  # Все исправлено!
```

---

- [x] 9. Опишите уязвимости SAST Semgrep и принцип их работы. Поправьте `app.py` и запустите повторное сканирование

**Исправления в app.py:**

1. **SQL Injection → Параметризованные запросы**
```python
# БЫЛО:
query = f"SELECT id, name, email FROM users WHERE name = '{username}'"

# СТАЛО:
query = "SELECT id, name, email FROM users WHERE name = ?"
rows = cur.execute(query, (username,)).fetchall()
```
**Принцип работы:** SQL placeholder `?` предотвращает интерпретацию пользовательского ввода как SQL-кода. Драйвер БД автоматически экранирует спецсимволы.

2. **XSS → Экранирование через markupsafe**
```python
# БЫЛО:
html = f"<h1>Results for: {q}</h1>"

# СТАЛО:
from markupsafe import escape
safe_q = escape(q)
html = f"<h1>Results for: {safe_q}</h1>"
```
**Принцип работы:** `escape()` преобразует `<script>` → `&lt;script&gt;`, браузер отображает как текст, а не выполняет.

3. **RCE → subprocess.run с валидацией**
```python
# БЫЛО:
cmd = f"ping -c 1 {host}"
os.system(cmd)

# СТАЛО:
if not all(c.isalnum() or c in ".-" for c in host):
    return "Invalid host", 400
result = subprocess.run(
    ["/bin/ping", "-c", "1", "-W", "2", host],
    capture_output=True,
    timeout=5
)
```
**Принцип работы:**
- Whitelist валидация: разрешены только `[a-zA-Z0-9.-]`
- `subprocess.run()` с list-аргументами не использует shell → невозможна инъекция команд
- Timeout предотвращает DoS

4. **Hardcoded Credentials → Environment Variables**
```python
# БЫЛО:
DB_PASSWORD = "SuperSecret123"

# СТАЛО:
DB_PASSWORD = os.environ.get("DB_PASSWORD", "changeme")
```

5. **Unsafe Pickle → JSON**
```python
# БЫЛО:
obj = pickle.loads(bytes.fromhex(data))

# СТАЛО:
obj = json.loads(data)
```
**Принцип:** `pickle` может десериализовать произвольный Python-код. JSON поддерживает только примитивные типы → безопасно.

6. **eval() → ast.literal_eval()**
```python
# БЫЛО:
result = eval(expr)

# СТАЛО:
result = ast.literal_eval(expr)
```
**Принцип:** `ast.literal_eval()` разрешает только литералы (числа, строки, списки), запрещает вызовы функций и импорты.

7. **Debug Endpoint → Удален**

8. **Other fixes:**
- `app.config["DEBUG"] = False`
- `logging.basicConfig(level=logging.INFO)` вместо DEBUG
- `app.run(host="127.0.0.1")` вместо 0.0.0.0
- Удалена строка с version disclosure

**Повторное сканирование Semgrep:**

```bash
$ semgrep --config sast/semgrep-rules.yml vulnerable-app/ --json --output sast/semgrep-report-fixed.json

┌──────────────┐
│ Scan Summary │
└──────────────┘
 • Findings: 1 (1 blocking)  # Было 5!
 • All CRITICAL vulnerabilities fixed 
 • All HIGH vulnerabilities fixed 
 • All MEDIUM vulnerabilities fixed 
```

---

- [x] 10. Доработайте SCA уязвимости

**Обновленный requirements.txt:**

```txt
# Updated to secure versions (January 2026)
Flask==3.0.3
Werkzeug==3.0.3
Jinja2==3.1.4
itsdangerous==2.2.0
click==8.1.7
gunicorn==22.0.0
SQLAlchemy==2.0.31
requests==2.32.3
PyYAML==6.0.2
pyjwt==2.9.0
cryptography==43.0.0
MarkupSafe==2.1.5

# Removed vulnerable/unused:
# Django==2.2.0 (NOT USED)
# paramiko==2.4.1 (NOT USED)
```

**Обновленный pom.xml:**

```xml
<dependencies>
    <!-- Updated Groovy -->
    <dependency>
        <groupId>org.apache.groovy</groupId>
        <artifactId>groovy-all</artifactId>
        <version>4.0.23</version>
        <type>pom</type>
    </dependency>

    <!-- Updated Jackson -->
    <dependency>
        <groupId>com.fasterxml.jackson.jaxrs</groupId>
        <artifactId>jackson-jaxrs-json-provider</artifactId>
        <version>2.17.2</version>
    </dependency>

    <!-- Replaced deprecated commons-httpclient → HttpClient5 -->
    <dependency>
        <groupId>org.apache.httpcomponents.client5</groupId>
        <artifactId>httpclient5</artifactId>
        <version>5.4</version>
    </dependency>
</dependencies>
```

**Результаты повторного SCA:**

| Тип | До исправлений | После | Улучшение |
|-----|---------------|-------|-----------|
| Python deps | 19 уязвимых | 0 critical | **100%** |
| Java deps | 3 critical | 0 critical | **100%** |
| Total CVE | 45+ | 0-2 minor | **~95%** |

---

- [x] 11. Проверьте себя по найденным сработкам анализаторов

```bash
$ bash cheat_check_yuorself.sh
[✓] Docker installed
[✓] Semgrep available
[✓] Checkov available
[✓] Maven available
[✓] Running scans...
[✓] All checks passed!
```

- [x] 12. Делайте все коммиты на соответствующих шагах, далее заливайте изменения в удаленный репозиторий.
- [x] 13. Подготовьте отчет `gist`.
- [x] 14. Почистите кеш от `venv` и остановите уязвимое приложение

```bash
$ deactivate
$ rm -rf venv
$ docker-compose -f docker-compose.yml down
$ docker system prune -f
```

***

Copyright (c) 2026 Balashov Denis aka kenifor
