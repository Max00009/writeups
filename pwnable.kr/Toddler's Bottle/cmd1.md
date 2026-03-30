<blockquote>
<b>Problem:</b><br><br>
  - After seeing the cmd1.c source code i understand that our argument can't contain:"flag","sh","tmp".<br>
  - Also <putenv("PATH=/thankyouverymuch")> sets the environment to absolute PATH in root directory which we don't any access to write.
</blockquote>  
    
---  

<blockquote>
<b>Objective:</b><br><br>
  - what system() actually does is:<br>
		it spawns a shell and run the command which is passed into system().<br>
		for example system(argument) becomes /bin/sh -c "argument".<br>
	- so whatever argv[1] we pass in ./cmd1 will be run into a shell by system.<br>
	- so we could just do this $./cmd1 "cat flag".but it will fail cause:<br>
		1.filter won't allow anything that contains "flag","sh","tmp".<br>
		2.our program sets PATH=/thankyouverymuch. cat,ls etc is not present there.<br>
	- so basically we have to somehow spawn an interactive shell through system(argv[1]) where argv[1] doesn't contain "flag","sh","tmp".<br>
	- after that we can run any command.no need to worrry about filter cause our command is not via argument but directly inside interactive shell.<br>
	- however we need to set the PATH=/bin where cat is located.<br>
</blockquote>  

---  

<blockquote>
<b>Solution:</b><br><br>
  - "/proc/self/exe" is a symlink to the executable of the currently running process.which is /bin/sh cause that's what system() spawns.<br>
	- so by running system(/proc/self/exe) we can re-execute the shell from inside itself.Think of it like spawning a shell from a already existing shell without writting something like "/bin/sh".<br>
	- now we have an interactive shell where we can run "cat flag" but before that we need to set the PATH=/bin where cat is located.<br>
	- so the commands we have to run in sequence to get flags are:<br><br>
  <pre>
		$./cmd1 "/proc/self/exe"
  </pre>

  <pre>
		$PATH=/bin
  </pre>
  
  <pre>
		$cat flag
  </pre>
  - After running theses commands,we get the flag.<br><img width="440" alt="flag" src="https://github.com/user-attachments/assets/b436beca-20fc-4f1e-9b05-c63fed9bce8a" />
</blockquote>
