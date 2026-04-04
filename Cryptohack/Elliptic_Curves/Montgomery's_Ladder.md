<blockquote>
<b>Problem:</b><br><br>
We have been given:<br>
- An elliptic curve equation E: Y<sup>2</sup> = X<sup>3</sup> + 486662X<sup>2</sup> + X mod 2<sup>255</sup> - 19<br>
- x-coordinate of a generator point G.x = 9<br><br>
<b>Montgomery’s binary algorithm:</b>
<pre>
Input:  P and integer k
Output: [k]P
1. Set (R0, R1) = (P, [2]P)
2. for i = n-2 down to 0:
3.    if k<sub>i</sub> == 0:
4.        (R0, R1) = ([2]R0, R0 + R1)
5.    else:
6.        (R0, R1) = (R0 + R1, [2]R1)
7. return R0
</pre>
We have to find the x-coordinate of Q, where Q = [0x1337c0decafe] G.
</blockquote>

---

<blockquote>
<b>Objective:</b><br><br>
  -First we define necessary add and double function in montgomery ladder.<br>
	-then implement the iteration logic.<br>
	-then calculate the x coordinate of Q.<br>
	-the speciality in Montgomery's ladder is we can compute answer using x coordinate only.No need to find y.<br>
</blockquote>  

---  

<blockquote>
<b>Solution</b><br><br>
<details>
<summary><b>Click to see solution.py</b></summary>

```python
m=(2**255)-19
G_x=9
a=486662
a24=(a+2)*pow(4,-1,m)%m
#n=21130179955454
p=G_x
#functions
def dbl(r):
    x=r[0]
    y=r[1]
    x1=pow((x+y),2,m)*pow((x-y),2,m)%m
    y1=((pow((x+y),2,m)-pow((x-y),2,m))%m)*(pow((x-y),2,m)+(a24)*((pow((x+y),2,m)-pow((x-y),2,m))%m))%m
    return (x1,y1)
def add(r1,r2):
    x2=r1[0]
    z2=r1[1]
    x3=r2[0]
    z3=r2[1]
    A = x2 + z2
    B = x2 - z2
    C = x3 + z3
    D = x3 - z3
    D_A=D*A%m
    C_B=C*B%m
    x5=pow(int(D_A+C_B),2,m)
    y5=pow(int(D_A-C_B),2,m)*p%m
    return x5,y5
#initialization
r_0=(9,1)
r_1=dbl(r_0)
k = int("1337c0decafe", 16)
bits = bin(k)[2:]
for bit in bits[1:]:
    if bit == '0':
        r0_new = dbl(r_0)
        r1_new = add(r_0, r_1)
    else:
        r0_new = add(r_0, r_1)
        r1_new = dbl(r_1)
    r_0, r_1 = r0_new, r1_new
print(f"X={r_0[0]},Z={r_0[1]}")



x = (r_0[0] * pow(r_0[1], -1, m)) % m
print(f"ans={x}")

```
</details>
  - After running the program we get the answer:<br><img width="818" alt="answer" src="https://github.com/user-attachments/assets/720f7d8a-e613-4ba9-aed6-09eb5f9acec8" />

</blockquote>
