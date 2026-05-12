<blockquote>
<b>INCLUDE</b><br>
</blockquote>
<blockquote>
<b>Recon</b><br><br>
  - First i ran a nmap scan with:<br>
  <pre>
    sudo nmap -sC -sV -vv 10.49.171.94
  </pre>
  - We get many open ports:<br>
  <br><img width="1219" alt="image" src="https://github.com/user-attachments/assets/788d5c77-a2a8-4ec4-bfd9-c23301261143" /><br>
  - We can see two http server running on port 4000 and 50000:<br>
  <br><img width="1621" alt="image" src="https://github.com/user-attachments/assets/969e8d08-3c6c-4cba-b368-54160a032507" /><br>
  - Along with ssh on port 22,smtp on port 25,pop3 on port 110,imap on port 143 etc.<br>
  - I visited both websites being hosted on port 4000 and 50000:<br>
  <br><img width="1284" alt="image" src="https://github.com/user-attachments/assets/5b772a2d-7d87-4fe5-a76c-09c5f0d16404" /><br>
  <br><img width="1282" alt="image" src="https://github.com/user-attachments/assets/d85aaccd-f6cb-4fba-9282-9f1e40b1695a" /><br>
  - On the SysMon application we can see a 'Login' button.Upon visiting the Login page we can see we need credentials to Login:<br>
  <br><img width="1284" alt="image" src="https://github.com/user-attachments/assets/731df71c-c6d7-4edd-b0f8-128a9206f04d" /><br>
  <br><img width="1284" alt="image" src="https://github.com/user-attachments/assets/1ff03ab3-e1b4-4336-98a0-413aee371c80" /><br>

</blockquote>
<blockquote>
<b>Logging In To SysMon App via SSRF</b><br><br>
  - First I logged into 'Review App' which is hosted on port 4000 with username:'guest' and password:'guest' as directed.After successfully logging in,We can see the interface like this:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/57ee02eb-654e-4d3c-9f0d-646825dee92c" /><br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/eb59588b-375e-4a46-bfb5-cf57e594824a" /><br>
  - Upon examining the 'View Profile' option I see an interesting part:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/4409bd23-1158-4527-b14f-207309c34bb0" /><br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/018f5a57-c8f1-4ca5-822c-114df7904968" /><br>
  - There is a field for 'Recommand Activity' where we can send a key:value pair.For example I tried to send 'key' as 'Activity Type' and 'value' as 'Activity Name'.Here's the result:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/b6f83eb2-565e-4f13-b53e-666374e5fa97" /><br>
  <br><img width="1469" alt="image" src="https://github.com/user-attachments/assets/85b0d83a-92a2-43ed-86bc-80ebc8c98039" /><br>
  - As we can see the data we just sent is reflected on the profile immediately.Now what if we try to change the value of 'isAdmin' parameter to 'true'.Will that overwrite the initial value which is 'false'?<br>
  - It worked:<br>
  <br><img width="1468" alt="image" src="https://github.com/user-attachments/assets/02fa7d2c-a115-4ae1-b0d0-62ceb470274f" /><br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/9e4ec6c9-8e60-48c2-a966-f603235074e9" /><br>
  - Now 'isAdmin' is set to 'true' and we can see two new options appear 'API' and 'Settings'.<br>
  - Upon visiting 'API' page we see this:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/87071241-c297-46c2-9950-d6ed402e02f2" /><br>
  - This means if we can send GET request to these endpoints we can get the credentials to log into SysMon application.<br>
  - Now one important thing is if we just try to visit 'http://10.49.171.94:5000/getAllAdmins101099991' we get error.Cause these endpoints are internal API.i.e. These can only be accessed when the Review App sends the get request itself.External requests won't be able to connect.<br>
  - So we have to find a way to make the Review App make the request to these internal api endpoints.<br>
  - Upon examining the 'Settings' page I found an interesting thing.We can put an url from which the 'banner image' will be updated.This could potentially be a SSRF(Server Side Request Forgery) vulnerability.<br>
  - Now what if we pass the 'http://127.0.0.1:5000/getAllAdmins101099991' url.Will that make the application to send request to that internal api endpoint and show the credentials for SysMon app?<br>
  <br><img width="803" alt="image" src="https://github.com/user-attachments/assets/f0bd604f-ce5b-442b-8691-fa6f8050c1ae" /><br>
  - A base64 response is returned:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/12a5364d-c8d7-4a36-b431-1e44f55668b1" /><br>
  - Upon decoding the base64 output,we get the credentails for SysMon web-application:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/afe7e5c2-6416-4ae3-a71a-7c5ea91202ee" /><br>
  - Now after going back to SysMon web-application hosted on port 50000 and logging in with theses credentials we get the first flag:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/380d4f18-c7f1-4c7e-b619-cab48c7765be" /><br>

</blockquote>

<blockquote>
<b>Identifying LFI</b><br><br>
  - Upon reviewing the page source code of SysMon dashboard,I found an interesting thing:<br>
  <br><img width="1376" alt="image" src="https://github.com/user-attachments/assets/b10d2f5a-236b-49e5-9702-31959cdbbe3d" /><br>
  - The 'profile.php' is taking a filename as the 'img' parameter to fetch the file.<br>
  - This could possibly be a LFI(Local File Inclusion) vulnerability.I tried to put filepaths manually to see if i can find any sensitive information.But it didn't work.Maybe because i couldn't reach the target upper directory where sensitive file is present or maybe some kind of filetering is in action.<br>
  - So I tried to automate the process by fuzzing the filepath using ffuf with the command:
  <pre>
    ffuf -u http://10.49.171.94:50000/profile.php?img=FUZZ -w /usr/share/wordlists/SecLists/Fuzzing/LFI/LFI-Jhaddix.txt -b "PHPSESSID=m0qgsm7kt3srrlc1gsj3q8o8po" -fs 0
  </pre>
    NOTE:Use your own PHPSESSID which you can find in cookies. '-fs 0' is to hide empty results.<br>
  <br><img width="1205" alt="image" src="https://github.com/user-attachments/assets/2cb04848-fdc1-4645-a703-2954632ebc3d" /><br>
  - Let's try the first filepath from the result.And we can see the output:<br>
  <br><img width="1467" alt="image" src="https://github.com/user-attachments/assets/43836a65-3fbf-4559-a8ab-067287b1e29a" /><br>
  - We successfully exploited a LFI vulnerability.<br>
</blockquote>
<blockquote>
<b>Getting RCE via Log Poisoning</b><br><br>
  - Now that we have exploied LFI we can try to poison the log to get RCE.<br>
  - First let's try to see what logs we have access to.In the previous payload that we get from ffuf if we replace '/etc/passwd' with '/var/log/mail.log' and '/var/log/auth.log' we can access the mail logs and ssh logs respectively.<br>
  <br><img width="1287" alt="image" src="https://github.com/user-attachments/assets/b7bdd2ad-84bd-49b9-9e57-d399b2065543" /><br>
  <br><img width="1285" alt="image" src="https://github.com/user-attachments/assets/39696650-c038-4ca6-95e2-3872834b119c" /><br>
  - By poisoning any of these two logs we can get RCE(Remote Code Execution).I will demonstrate the mail logs poisoning.However the ssh logs can be poisoned too using Remmina or other tools.<br>
  - First let's test the RCE with the payload:
  
```php
    <?php system('id'); ?>
```

  - Let's connect to target machine port 25 where smtp service is running.We will connect via netcat:<br>
  <br><img width="1092" alt="image" src="https://github.com/user-attachments/assets/0c3f9f0c-11b6-4ba7-b815-c66171c21073" /><br>
  - Now let's send an email in smtp format but in place of 'RCPT TO' we will inject our payload.The reason we choose 'RCPT TO' is when an email is sent to a non-existent user or a specific recipient, the SMTP server (Postfix) logs that attempt in /var/log/mail.log. By making the recipient name a PHP tag, that tag gets written directly into the log file.<br>
  <br><img width="1097" alt="image" src="https://github.com/user-attachments/assets/e402739b-609d-4646-b0ef-6891c0a885ae" /><br>
  NOTE:we get the 'filepath.lab' name from nmap scan at the beginning where Host name was 'filepath.lab'<br>
  <br><img width="786" alt="image" src="https://github.com/user-attachments/assets/eefbfc47-50c3-47e3-abbf-48b16e0c5447" /><br>
  - After sending the payload when we refresh the '/profile.php?img=....//....//....//....//....//....//....//....//....//....//....//....//....//....//....//....//....//....//....//....//....//var/log/mail.log' page we can see our command was executed:<br>
  <br><img width="1287" alt="image" src="https://github.com/user-attachments/assets/c8a88982-1e05-4cc3-9818-bee5984d0827" /><br>
  - Now that we have RCE we can navigate directories and read the second flag.<br>
  <br><img width="739" alt="image" src="https://github.com/user-attachments/assets/cce5d603-f616-4c70-9a22-fa904a8b11a0" /><br>
  <br><img width="1288" alt="image" src="https://github.com/user-attachments/assets/32f1191b-747d-4bc6-a744-831c5dada224" /><br>

  
</blockquote>


