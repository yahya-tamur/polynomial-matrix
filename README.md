Multiplies matrices of integer polynomials.

This is useful, for example, in finding the rational canonical form
or the Jordan canonical form of a matrix -- the first step is to find
the Smith normal form of $xI - A$.

`pm_i` reads these matrices from a simplified syntax, `pm_mul` multiplies them,
and `pm_print` prints them in a nice format.

The following example is included in main.py and out.txt, and can be generated
by running `python3 main.py > out.txt`.

```
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
```

Outputs:

```
┌───┬────────────┬─────────────────┬─────────┐
│ 1 │            │                 │         │
├───┼────────────┼─────────────────┼─────────┤
│   │ -928   + x │ -30  + 15x      │         │
├───┼────────────┼─────────────────┼─────────┤
│   │   62 - 31x │ 940 - 454x + x² │ -4 + 2x │
├───┼────────────┼─────────────────┼─────────┤
│   │            │ -10   + 5x      │ -2  + x │
└───┴────────────┴─────────────────┴─────────┘
times
┌────┬────┬─────────────────┬────┐
│ -1 │    │                 │    │
├────┼────┼─────────────────┼────┤
│    │ 15 │          - 15x² │    │
├────┼────┼─────────────────┼────┤
│    │ -1 │ -928 + x        │    │
├────┼────┼─────────────────┼────┤
│    │    │                 │ -1 │
└────┴────┴─────────────────┴────┘
is
┌────┬───────────────────┬─────────────────────────────────────┬────────┐
│ -1 │                   │                                     │        │
├────┼───────────────────┼─────────────────────────────────────┼────────┤
│    │ -13890            │   27840  - 13950x + 13935x²  - 15x³ │        │
├────┼───────────────────┼─────────────────────────────────────┼────────┤
│    │    -10 - 11x - x² │ -872320 + 422252x  - 2312x² + 466x³ │ 4 - 2x │
├────┼───────────────────┼─────────────────────────────────────┼────────┤
│    │     10  - 5x      │    9280   - 4650x     + 5x²         │ 2  - x │
└────┴───────────────────┴─────────────────────────────────────┴────────┘
```
