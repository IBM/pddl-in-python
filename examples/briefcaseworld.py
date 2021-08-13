#!/usr/bin/env python3

import sys
sys.path.insert(0, '../')

from pddl_in_python import Domain

# If I use type hint notation e.g. m : location,
# unfortunately, the current python interpreter looks for a class definition in the read-time.

class Briefcaseworld(Domain):
    def move(m = location, l = location):
        if is_at[m]:
            is_at[l] = True
            is_at[m] = False
            for x in all(portable):
                if _in[x]:
                    at[x,l] = True
                    at[x,m] = False

    def take_out(x = portable):
        if _in[x]:
            _in[x] = False

    def put_in(x = portable, l = location):
        if not _in[x] and at[x,l] and is_at[l]:
            _in[x] = True

print(Briefcaseworld())
