
#Initial Hash values required
initialHashvalueu=['6a09e667'
,'bb67ae85'
,'3c6ef372',
'a54ff53a',
'510e527f',
'9b05688c',
'1f83d9ab',
'5be0cd19']

#The 64 SHA 256 constants 32-bits each
SHA256Constants=[
'428a2f98','71374491','b5c0fbcf','e9b5dba5',
'3956c25b','59f111f1','923f82a4','ab1c5ed5',
'd807aa98','12835b01','243185be','550c7dc3',
'72be5d74','80deb1fe','9bdc06a7','c19bf174',
'e49b69c1','efbe4786','0fc19dc6','240ca1cc',
'2de92c6f','4a7484aa','5cb0a9dc','76f988da',
'983e5152','a831c66d','b00327c8','bf597fc7',
'c6e00bf3','d5a79147','06ca6351','14292967',
'27b70a85','2e1b2138','4d2c6dfc','53380d13',
'650a7354','766a0abb','81c2c92e','92722c85',
'a2bfe8a1','a81a664b','c24b8b70','c76c51a3',
'd192e819','d6990624','f40e3585','106aa070',
'19a4c116','1e376c08','2748774c','34b0bcb5',
'391c0cb3','4ed8aa4a','5b9cca4f','682e6ff3',
'748f82ee','78a5636f','84c87814','8cc70208',
'90befffa','a4506ceb','bef9a3f7','c67178f2'
]

def binReturn(dec):
    return(str(format(dec,'b')))

def bin8Bit(dec):
    return(str(format(dec,'08b')))

def bin32Bit(dec):
    return(str(format(dec,'032b')))

def bin64Bit(dec):
    return(str(format(dec,'064b')))

def hexReturn(dec):
    return(str(format(dec,'x')))

def decReturnBin(bin_string):
    return(int(bin_string,2))

def decReturnHex(hex_string):
    return(int(hex_string,16))


def LP(Sett,n):
    toReturn=[]
    i=0
    k=n
    while k<len(Sett)+1:
        toReturn.append(Sett[i:k])
        i=k
        k+=n 
    return(toReturn)


def SL(bitString):
    bitList=[]
    for i in range(len(bitString)):
        bitList.append(bitString[i])
    return(bitList)

def LS(bitList):
    bitString=''
    for i in range(len(bitList)):
        bitString+=bitList[i]
    return(bitString)

def rotateRight(bitString,n):
    bitList = SL(bitString)
    counter=0
    while counter <= n-1:
        listMain=list(bitList)
        var_0=listMain.pop(-1)
        listMain=list([var_0]+listMain)
        bitList=list(listMain)
        counter+=1
    return(LS(listMain))

def shiftRight(bitString,n):
    bitList=SL(bitString)
    counter=0
    while counter <= n-1:
        bitList.pop(-1)
        counter+=1
    frontAppend=['0']*n
    return(LS(frontAppend+bitList))

def mod32Addition(inputSet):
    valueu=0
    for i in range(len(inputSet)):
        valueu+=inputSet[i]
    mod32 = 4294967296
    return(valueu%mod32)

def xorToStr(bitString1,bitString2):
    xorList=[]
    for i in range(len(bitString1)):
        if bitString1[i]=='0' and bitString2[i]=='0':
            xorList.append('0')
        if bitString1[i]=='1' and bitString2[i]=='1':
            xorList.append('0')
        if bitString1[i]=='0' and bitString2[i]=='1':
            xorList.append('1')
        if bitString1[i]=='1' and bitString2[i]=='0':
            xorList.append('1')
    return(LS(xorList))

def andToStr(bitString1,bitString2):
    andList=[]
    for i in range(len(bitString1)):
        if bitString1[i]=='1' and bitString2[i]=='1':
            andList.append('1')
        else:
            andList.append('0')

    return(LS(andList))



def notStr(bitString):
    notList=[]
    for i in range(len(bitString)):
        if bitString[i]=='0':
            notList.append('1')
        else:
            notList.append('0')
    return(LS(notList))

'''
Six Functions Required by SHA:
'''

def ShaFunc1(x1,y1,z1):
    return(xorToStr(andToStr(x1,y1),andToStr(notStr(x1),z1)))

def ShaFunc2(x1,y1,z1):
    return(xorToStr(xorToStr(andToStr(x1,y1),andToStr(x1,z1)),andToStr(y1,z1)))

def ShaFunc3(x1):
    return(xorToStr(xorToStr(rotateRight(x1,2),rotateRight(x1,13)),rotateRight(x1,22)))

def ShaFunc4(x1):
    return(xorToStr(xorToStr(rotateRight(x1,6),rotateRight(x1,11)),rotateRight(x1,25)))

def ShaFunc5(x1):
    return(xorToStr(xorToStr(rotateRight(x1,7),rotateRight(x1,18)),shiftRight(x1,3)))

def ShaFunc6(x1):
    return(xorToStr(xorToStr(rotateRight(x1,17),rotateRight(x1,19)),shiftRight(x1,10)))

def messagePad(bitList):
    padOne = bitList + '1'
    padLen = len(padOne)
    k=0
    while ((padLen+k)-448)%512 != 0:
        k+=1
    backAppend0 = '0'*k
    backAppend1 = bin64Bit(len(bitList))
    return(padOne+backAppend0+backAppend1)

def messageBitReturn(stringInput):
    bitList=[]
    for i in range(len(stringInput)):
        bitList.append(bin8Bit(ord(stringInput[i])))
    return(LS(bitList))

def messagePrePro(inputString):
    bit_main = messageBitReturn(inputString)
    return(messagePad(bit_main))

def messageParsing(inputString):
    return(LP(messagePrePro(inputString),32))

def messageSchedule(index,wT):
    newWord = bin32Bit(mod32Addition([int(ShaFunc6(wT[index-2]),2),int(wT[index-7],2),int(ShaFunc5(wT[index-15]),2),int(wT[index-16],2)]))
    return(newWord)

'''
Input: Any String
Output: The 256-bit hash string.
'''

def SHA256(inputString):
    wT=messageParsing(inputString)
    a=bin32Bit(decReturnHex(initialHashvalueu[0]))
    b=bin32Bit(decReturnHex(initialHashvalueu[1]))
    c=bin32Bit(decReturnHex(initialHashvalueu[2]))
    d=bin32Bit(decReturnHex(initialHashvalueu[3]))
    e=bin32Bit(decReturnHex(initialHashvalueu[4]))
    f=bin32Bit(decReturnHex(initialHashvalueu[5]))
    g=bin32Bit(decReturnHex(initialHashvalueu[6]))
    h=bin32Bit(decReturnHex(initialHashvalueu[7]))
    for i in range(0,64):
        if i <= 15: 
            t1=mod32Addition([int(h,2),int(ShaFunc4(e),2),int(ShaFunc1(e,f,g),2),int(SHA256Constants[i],16),int(wT[i],2)])
            t2=mod32Addition([int(ShaFunc3(a),2),int(ShaFunc2(a,b,c),2)])
            h=g
            g=f
            f=e
            e=mod32Addition([int(d,2),t1])
            d=c
            c=b
            b=a 
            a=mod32Addition([t1,t2])
            a=bin32Bit(a)
            e=bin32Bit(e)
        if i > 15:
            wT.append(messageSchedule(i,wT))
            t1=mod32Addition([int(h,2),int(ShaFunc4(e),2),int(ShaFunc1(e,f,g),2),int(SHA256Constants[i],16),int(wT[i],2)])
            t2=mod32Addition([int(ShaFunc3(a),2),int(ShaFunc2(a,b,c),2)])
            h=g
            g=f
            f=e
            e=mod32Addition([int(d,2),t1])
            d=c
            c=b
            b=a 
            a=mod32Addition([t1,t2])
            a=bin32Bit(a)
            e=bin32Bit(e)
    hash0 = mod32Addition([decReturnHex(initialHashvalueu[0]),int(a,2)])
    hash1 = mod32Addition([decReturnHex(initialHashvalueu[1]),int(b,2)])
    hash2 = mod32Addition([decReturnHex(initialHashvalueu[2]),int(c,2)])
    hash3 = mod32Addition([decReturnHex(initialHashvalueu[3]),int(d,2)])
    hash4 = mod32Addition([decReturnHex(initialHashvalueu[4]),int(e,2)])
    hash5 = mod32Addition([decReturnHex(initialHashvalueu[5]),int(f,2)])
    hash6 = mod32Addition([decReturnHex(initialHashvalueu[6]),int(g,2)])
    hash7 = mod32Addition([decReturnHex(initialHashvalueu[7]),int(h,2)])
    final_hash = (hexReturn(hash0),
                  hexReturn(hash1),
                  hexReturn(hash2),
                  hexReturn(hash3),
                  hexReturn(hash4),
                  hexReturn(hash5),
                  hexReturn(hash6),
                  hexReturn(hash7))

    final_hash_string = ''
    for h in final_hash:
        final_hash_string+=str(h)


    return final_hash


# print(SHA256('Suhas, Bharath, KokaSiva and Krishna Chaitanya'))