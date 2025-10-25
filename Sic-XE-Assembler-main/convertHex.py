from multipledispatch import dispatch #Allows for function overloading

#Takes integer and converts into Hex representing it into 2Bytes,3Bytes,....
@dispatch(int,int)
def Hex(X,Bytes):
    X = hex(X)[2:]
    size=Bytes*2-len(X)
    if(size < 0):
        raise Exception("Hex size is bigger than given size.")
    zeros=str()
    for i in range(size):
        zeros += '0'
    return str(zeros+X).upper()

@dispatch(str,int)
def Hex(X,Bytes):
    size=Bytes*2-len(X)
    if(size < 0):
        raise Exception("Hex size is bigger than given size.")
    zeros=str()
    for i in range(size):
        zeros += '0'
    return str(zeros+X).upper()

@dispatch(int)
def Hex(X):
    if( (X < 0) and (X >= -4096) ):
        X = (~(X)) + 1 
        return hex(4096-X)[2:]
    if( (X < 0) and (X >= -65536) ):
        X = (~(X)) + 1 
        return hex(65536-X)[2:]
    return str(hex(X)[2:]).upper()

def Hex_FromBinary(X):
    if((X)[:2] == '0b'):
        return Hex(int(X))
    return str(Hex(int('0b'+X,2))).upper()

@dispatch(str)
def Hex_ToBinary(X):
    return bin(Hex_ToDecimal(X))[2:]

@dispatch(str,int)
def Hex_ToBinary(X,Bytes):
    X = bin(Hex_ToDecimal(X))[2:]
    size = int(Bytes*8 -len(X))
    if(size < 0):
        raise Exception("Byte size is bigger than given size.")
    zeros=str()
    for i in range(size):
        zeros +='0'
    return str(zeros + X).upper()

def Hex_ToDecimal(X):
    X = '0x'+ X
    return int(X,16)

@dispatch(str,int)
def Bits_ToHex(X,bits):
    size = int((bits/4)-len(X))
    zeros = str()
    for i in range(size):
        zeros +='0'
    return str(zeros + X).upper()

@dispatch(int,int)
def Bits_ToHex(X,bits):
    X = hex(X)[2:]
    size = int((bits/4)-len(X))
    zeros = str()
    for i in range(size):
        zeros +='0'
    return str(zeros + X).upper()
@dispatch(int,int)
def Hex_Addition(X1,X2):
    return str(Hex(X1+X2)).upper()
@dispatch(str,str)
def Hex_Addition(X1,X2):
    X1= int(('0x'+X1),16)
    X2= int(('0x'+X2),16)
    return str(Hex(X1+X2)).upper()
@dispatch(int,int)
def Hex_Subtraction(X1,X2):
    return str(Hex(X1-X2)).upper()
@dispatch(str,str)
def Hex_Subtraction(X1,X2):
    X1= int(('0x'+X1),16)
    X2= int(('0x'+X2),16)
    return str(Hex(X1-X2)).upper()