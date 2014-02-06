"""
Here each group tests single python program which must be named with the group name plus a .py suffix. These programs are executed with the same python interpreter used to run the check program.
"""

import check
import os
import difflib
import re
from view_distance_diff import view_distance_diff

def edgews_normalize(*parts):
    def filter(x):
        x = [l.strip() for l in x]
        return [l + '\n' for l in x if l != '']
    return [filter(x) for x in parts]

def diff_almost_exact(a, b, output):
    a, b = edgews_normalize(a, b)
    if a != b:
            output.write("Diff in output:\n")
            output.writelines(difflib.unified_diff(a, b))
            return False
    return True

def diff_almost_exact_uniq(a, b, output):
    return diff_almost_exact(set(a), set(b), output)

def diff_unordered(a, b, output):
    a, b = edgews_normalize(a, b)
    a, b = sorted(a), sorted(b)
    if a != b:
            output.write("Diff in sorted output:\n")
            output.writelines(difflib.unified_diff(a, b))
            return False
    return True

checks = {
    "cmudict_entries": { 'stdout': diff_unordered },
    "fst_recognize": { 'stdout': diff_almost_exact },
    "fst_compose": { 'stdout': diff_almost_exact_uniq },
    "view_distance": { 'stdout': view_distance_diff },
    "viewall_distance": { 'stdout': view_distance_diff },
    "transliterate": { 'stdout': diff_almost_exact },
    "korean_numbers": { 'stdout': diff_almost_exact },
}

check.check_all(checks, extra_usage=__doc__.rstrip('\n\r'))
