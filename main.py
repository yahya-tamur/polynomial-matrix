from lib import *

#make polynomial matrix.
a = pm_i(f"""
1 |        |            |
  | -928 1 | -30 15     |
  | 62 -31 | 940 -454 1 | -4 2
  |        | -10 5      | -2 1
""")

#initial and terminal new lines ignored.
#otherwise, successive non-overlapping numbers, |'s and newlines are read.
b = pm_i(f"""
-1 | | |
 | 15 | 0 0 -15 |
 | -1 | -928 1 |
 | | | -1
""")

pm_print(a)
print("times")
pm_print(b)
print("is")
pm_print(pm_mul(a,b))
