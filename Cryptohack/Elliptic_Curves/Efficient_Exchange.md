<blockquote>
<b>Problem:</b><br><br>
  - we have been given:<br>
  an eliptic curve equation: E:Y^2=X^3+497X+1768mod9739,<br>
  G:(1804,5368),<br>
  x(QA)=4726,<br>
  nB=6534,<br>
  {'iv': 'cd9da9f1c60925922377ea952afc212c', <br>
  'encrypted_flag': 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'}<br>
  and a decrypt.py file that we have to use to decrypt the encrypted_flag.

</blockquote>  
    
---  

<blockquote>
<b>Objective:</b><br><br>
  - to use the decrypt() function we need the x coordinate of shared secret.<br>
	- to get the shared secret we have to do=nB*QA.<br>
	- but we don't have y coordinate of QA.<br>
	- to get y coordinate we can put the value of x in the eliptic equation.<br>
	- that way we will get:y^2= something mod p.<br>
	- as the question says that p≡3mod4 so we can calculate y by the formula y=r^((p+1)/4) mod p where r=value of y^2.no need of Toneli Shank Algorithm.<br>
	- now there are two possible values of y which are (y and p-y).<br>
	- but in this case,it doesn't matter which value of y we take cause only x coordinate is used to decrypt.<br>
	- so finally we have both x and y coordinate of QA.<br>
	- we multiply QA with nB.<br>
	- get the shared key.<br>
	- pass the x coordinate in decrypt() function.<br>
	- get the flag.
  
</blockquote>  

---  

<blockquote>
<b>Solution</b><br><br>
<details>
<summary><b>Click to see solution.py</b></summary>

```python
	from Crypto.Cipher import AES
	from Crypto.Util.Padding import pad, unpad
	import hashlib
	from dataclasses import dataclass

	def is_pkcs7_padded(message):
	    padding = message[-message[-1]:]
	    return all(padding[i] == len(padding) for i in range(0, len(padding)))
	def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
	    # Derive AES key from shared secret
	    sha1 = hashlib.sha1()
	    sha1.update(str(shared_secret).encode('ascii'))
	    key = sha1.digest()[:16]
	    # Decrypt flag
	    ciphertext = bytes.fromhex(ciphertext)
	    iv = bytes.fromhex(iv)
	    cipher = AES.new(key, AES.MODE_CBC, iv)
	    plaintext = cipher.decrypt(ciphertext)

	    if is_pkcs7_padded(plaintext):
	        return unpad(plaintext, 16).decode('ascii')
	    else:
	        return plaintext.decode('ascii')


	x_QA=4726
	nB=6534
	ax=497
	p=9739
	@dataclass
	class Point:
	    x:int
	    y:int
	y_QA_square=(x_QA**3+ax*x_QA+1768)%p
	y_QA1=pow(y_QA_square,((p+1)//4),p)
	y_QA2=p-y_QA1
	print(f"y_QA1={y_QA1}")
	print(f"y_QA2={y_QA2}")
	P=Point(x_QA,y_QA1)

	def multiplication(n:int,P:Point):
	    Q=P
	    R=None
	    while n>0:
	        if (n%2)==1:
	            if R==None:
	                R=Q
	            else:
	                R=add(R,Q)
	        n=n//2
	        Q=add(Q,Q)
	    return R
	def add(a:Point,b:Point):
	    x1=a.x
	    x2=b.x
	    y1=a.y
	    y2=b.y
	    if (a!=b):
	        num=(y2-y1)%p
	        den=(x2-x1)%p
	    else:
	        num=(3*x1*x1+ax)%p
	        den=(2*y1)%p
	    lam=(num*(pow(den,-1,p)))%p
	    x3=((lam*lam)-x1-x2)%p
	    y3=(lam*(x1-x3)-y1)%p
	    c=Point(x3,y3)
	    return c
	result=multiplication(nB,P)
	print(f'x:{result.x},y:{result.y}')

	shared_secret = result.x
	iv = 'cd9da9f1c60925922377ea952afc212c'
	ciphertext = 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'


	print(decrypt_flag(shared_secret, iv, ciphertext))

```
</details>
  - After running the program we get the flag:<br><img width="777" alt="flag" src="https://github.com/user-attachments/assets/9669d9cd-6007-4d69-b3c1-1770ea23fc50" />

</blockquote>
