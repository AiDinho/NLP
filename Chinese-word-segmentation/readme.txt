
The filenames for each question are given below.  We will grade
only the questions marked with a dagger in the PDF file.  They are
marked with + below.

All text output should be printed to standard output (just use
print).

Programs that take input must read it from standard input (sys.stdin).
The sample program "stdin.py" explains how to do this.  On a Linux
command line run it as: "python stdin.py < readme.txt"

Test your programs by running: "python check-hw1.py". Run without
arguments and it will print out a detailed help text about usage
and grading.

Use svn for your homeworks (more details on course web page).

If you are taking the cross-listed graduate component then replace
CMPT413 with CMPT825 in the following.

$ svn co https://punch.cs.sfu.ca/svn/CMPT413-1141-(your-userid)
$ cd CMPT413-1141-(your-userid)
$ svn mkdir hw1 
$ svn mkdir hw1/answer
$ scp -r fraser.sfu.ca:~anoop/cmpt413/hw1 . 
# in the above command, that last period is important! it is the current directory
$ cd hw1/answer # put all your python programs here
# svn add each file you add to this directory
$ svn commit -m 'commit message'

To continue working at a later date:

$ cd CMPT413-1141-<userid>/hw1/answer
$ svn update
# work on your homework
$ svn commit -m 'commit message'

When you submit HW1 on courses.cs.sfu.ca submit the following URL:

https://punch.cs.sfu.ca/svn/CMPT413-1141-(your-userid)/hw1/answer

For the last two questions, you can get an initial solution by
copying virahanka_stub.py and segment_stub.py to the answer directory
with the filenames below.

%%

q1: devowel.py
q2: noduplicates.py
q3: freq.py
q4: dispersion.py
+q5: virahanka.py # you must start with virahanka_stub.py and only modify the virahanka function
+q6: segment.py

