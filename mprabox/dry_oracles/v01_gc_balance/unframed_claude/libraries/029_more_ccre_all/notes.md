# 029_more_ccre_all

028 recipe but shift 5k from chr fraction to cCRE_all (now 15k cCRE_all).

## Result
eval_01: 0.6935 — slight drop from 028's 0.6940
GC mean=0.485 std=0.112

## Interpretation
Reducing chr/WG below ~50% costs slightly. 028's 50% chr + 20% cCRE_all
+ 30% high-GC+pELS appears to be a robust local optimum.

## Next
- 030: final — add 5k cCRE dELS,CTCF-bound (compound regulatory) on top
  of 028 by reducing cCRE_all 10k -> 5k.
