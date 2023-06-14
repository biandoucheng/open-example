import pkga.ta
from bdpyconsts import bdpyconsts

# read
print(bdpyconsts.A)

# read not exists
print(bdpyconsts.C)

# write exists
try:
    bdpyconsts.A = 2222
except Exception as e:
    print("value changed error: ",str(e))

# not all caps
try:
    bdpyconsts.f = 111
except Exception as e:
    print("alpha lower error: ",str(e))


# changed if lock release allow
if not bdpyconsts.lock:
    bdpyconsts.A = 2222
else:
    print("value not changed cause the lock not allow")

# changed by release the lock
bdpyconsts.unlock()
bdpyconsts.A = 2222
bdpyconsts.locked()
print("value changed by release the lock")