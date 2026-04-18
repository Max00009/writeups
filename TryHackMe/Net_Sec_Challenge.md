<blockquote>
<b>NET SEC CHALLENGE</b><br><br>
  - First i did a extensive port scanning to answer most of the questions.<br>
  <pre>
    $ sudo nmap -sV -sC  -p- 10.48.134.245
  </pre>
  <img width="1097" alt="image" src="https://github.com/user-attachments/assets/342a6baa-c37b-41d3-9807-b303584c1236" /><br>
  - Then i start hydra to crack password of two given username for ftp service with the command:<br>
  <pre>
    $ hydra -L Username.txt -P /usr/share/wordlists/rockyou.txt -s 10021 ftp://10.48.134.245 
  </pre>
    (I did a mistake here by not adding the port number which we have to cause the ftp server is running on non-standard port).<br>
<img width="1102" alt="image" src="https://github.com/user-attachments/assets/fe760f67-4fd4-47a4-aae2-8d03aab8f09b" /><br>
  - Then i connected to ftp to both user and found the flag in quinn account.I transferred the file via:<br>
  <pre>
    $ get ftp_flag.txt'
  </pre>
  and then cat to get the flag.<br>
  <img width="430" alt="image" src="https://github.com/user-attachments/assets/e3b365ec-bb14-41d5-9fd3-f34f3f3da25f" /><br>
  - after that i visit http://10.48.134.245:8080 to see the challenge.The challenge is to scan the 10.48.134.245 machine without being detected.i.e. we have to be as stealthy as possible.So i ran the scan with:<br>
  <pre>
    $  nmap -sN -T3 -D RND:30 10.48.134.245
  </pre>
  which gave me the flag.
<img width="720" alt="image" src="https://github.com/user-attachments/assets/4b7b0642-861c-43da-a9fb-c0348e695226" />

