import pkga.ta
from bdpyconsts import bdpyconsts

# read
print(bdpyconsts.A)

# read not exists
print(bdpyconsts.C)

# write exists
bdpyconsts.A = 2222

# not all caps
bdpyconsts.f = 111