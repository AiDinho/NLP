#python create_input_fsa.py > input.fsa.txt
#fstcompile --isymbols=binary.voc --osymbols=binary.voc binary.fst.txt > binary.fst
#fstcompile --acceptor --isymbols=binary.voc input.fsa.txt > input.fsa
#fstarcsort --sort_type=ilabel binary.fst | fstcompose input.fsa - | fstproject --project_output > result.fsa
#fstprint --acceptor --isymbols=binary.voc result.fsa | awk '{print $3}' | grep -v '^$' | tr '\n' ' ' | sed

import sys
import subprocess

def write_input_fsa(ostream):
    for line in sys.stdin:
        input = line.split()
        for (i,inp) in enumerate(input):
            print >>ostream, i, i+1, inp
        print >>ostream, len(input)

def run(cmd, ostream, istream=None):
    if istream is None:
        return subprocess.call(cmd.split(), stdout=ostream)
    else:
        return subprocess.Popen(cmd.split(), stdin=istream, stdout=ostream)

def pipe(cmd, istream=None):
    if istream is not None:
        return subprocess.Popen(cmd.split(), stdin=istream, stdout=subprocess.PIPE)
    else:
        return subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

if __name__ == '__main__':
    with open('input.fsa.txt', 'w') as ostream:
        write_input_fsa(ostream)
    with open('binary.fst', 'w') as ostream:
        run('fstcompile --isymbols=binary.voc --osymbols=binary.voc binary.fst.txt', ostream)
    with open('input.fsa', 'w') as ostream:
        run('fstcompile --acceptor --isymbols=binary.voc input.fsa.txt', ostream)
    with open('result.fsa', 'w') as ostream:
        proc1 = pipe('fstarcsort --sort_type=ilabel binary.fst')
        proc2 = pipe('fstcompose input.fsa -', istream=proc1.stdout)
        proc1.stdout.close()
        proc3 = run('fstproject --project_output', ostream, istream=proc2.stdout)
        proc3.wait()
        proc2.stdout.close()
    result_fsa = subprocess.check_output('fstprint --acceptor --isymbols=binary.voc result.fsa'.split())
    output = map(lambda x: x.split()[2], filter(lambda x: len(x.split()) == 3, filter(lambda x: x != '', map(lambda x: x.strip(), result_fsa.split('\n')))))
    print " ".join(output)
