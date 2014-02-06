from __future__ import division
import sys

def get_alignment(align_tuple, ostream):
    s, align, t = align_tuple
    dist = -1
    if align == ' ': 
        #if s == ' ' and t == ' ': dist = 0
        if (s == '_' and t != '_') or (s != '_' and t == '_'): dist = 1
        elif s != t: dist = 2
        else: dist = -1
    elif align == '|': 
        if s == t: dist = 0
        else: dist = -1 
    else: 
        dist = -1
    #if dist == -1:
    #    print >>ostream, "invalid alignment", s, align, t
    return dist

def parse_alignment(lines, ostream, truthfile=False):
    if len(lines) < 1: return -1, 0
    str = lines[0]
    lines = lines[1:]
    str = str.strip()
    pre = 'levenshtein distance = '
    distance = None
    if str.startswith(pre):
        distance = int(str[len(pre):])
    else:
        if truthfile:
            print >>ostream, "something inexplicable wrong with the truth file"
        else:
            print >>ostream, "something inexplicable wrong with the output"
        sys.exit(2)
    difflist = []
    length = None
    #lines = filter(lambda x: x.strip() != '' and x[0] != '#', lines)
    lines = filter(lambda x: x[0] != '#', lines)
    lines = map(lambda x: x.rstrip(), lines)
    for (i, line) in enumerate(lines):
        # pad spaces using length of first line of alignment
        if i % 3 == 0:
            length = len(line)
        else:
            if length and (len(line) < length):
                line = line + (length - len(line)) * ' '
        difflist.append(line)
    if len(difflist) % 3 != 0:
        print >>ostream, "length is not multiple of 3"
        sys.exit(2)
    for i in range(3,len(difflist)+1,3):
        # remove spaces in between characters
        new_difflist = [ [ line[i] for i in range(0, len(line), 2) ] for line in difflist[i-3:i] ]
        results = [get_alignment(x, ostream) for x in zip(*new_difflist)]
        num_errors = sum(1 for i in results if i == -1)
        computed_distance = sum(i for i in results if i != -1)
        if num_errors > 1 and not truthfile:
            print >>ostream, "error: * indicates an error in the alignment"
            print >>ostream, " ".join('*' if r == -1 else ' ' for r in results)
            print >>ostream, "\n".join([ " ".join(i) for i in new_difflist])
            print >>ostream, num_errors, "errors in alignment"
            distance = -1
        if computed_distance != distance:
            print >>ostream, "error: the visual alignment edit distance is:", computed_distance
            distance = -1
    return distance, len(difflist)/3

def view_distance_diff(truth, output, ostream):
    (truth_dist, truth_num) = parse_alignment(truth, ostream, truthfile=True)
    (output_dist, output_num) = parse_alignment(output, ostream)
    if truth_dist != output_dist:
        print >>ostream, "edit distance mismatch: truth=%d output=%d" % (truth_dist, output_dist)
    if truth_num != output_num:
        print >>ostream, "number of alignments does not match: truth=%d output=%d" % (truth_num, output_num)
    if (truth_dist == output_dist) and (truth_num == output_num):
        return True
    else:
        return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print >>sys.stderr, "usage: %s truth output" % (sys.argv[0])
        sys.exit(2)
    truth = open(sys.argv[1])
    output = open(sys.argv[2])
    print view_distance_diff(truth.readlines(), output.readlines(), sys.stdout)

