import math
import random


def generateOTP() :
    ## storing strings in a list
    digits = [i for i in range(0, 10)]

    ## initializing a string
    OTP = ""
    ## we can generate any lenght of string we want
    for i in range(6):
        ## generating a random index
        index = math.floor(random.random() * 10)
        OTP += str(digits[index])

    ## displaying the random string
    # print(OTP)
    return OTP