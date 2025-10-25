
import copy
from SICXEInstructionset import *
from queue import *
from convertHex import *
from ErrorHandler import Exception_OutOfBlockRange
# initializing Literals Table as Queue with infinite size.
directives= ["LTORG","BASE","START","USE"]
LTT = Queue()
# Output code.
output=list()
# Program counters for each Use blocks.
block_num = 1
use_DEFAULT = {"Name":"DEFAULT","blockNumber":0,"Address":Hex(0,2),"Length":0}
use_DEFAULTB = {"Name":"DEFAULTB","blockNumber":0,"Address":Hex(0,2),"Length":0}
use_CDATA = {"Name":"CDATA","blockNumber":0,"Address":Hex(0,2),"Length":0}
use_CBLKS = {"Name":"CBLKS","blockNumber":0,"Address":Hex(0,2),"Length":0}
block = use_DEFAULT
blocks = list(dict())
blocks.append(use_DEFAULT)
symtab = dict()
LLTAB = dict()
# Value is in the queue or not
def contains(value):
    q = Queue()
    #Without using deepcopy, q will be literally same as LTT. they are going to share the same memory addressing, deepcopy will just make variable q as unique queue.
    q.queue= copy.deepcopy(LTT.queue)
    if(q.empty()):
        return False
    while(not(q.empty())):
        if(value == q.get()):
            return True
# Function that checks if there are literals or not and inserts it into the literal table.
def hasLiteral(lit):
    if('=' in lit["Address/Value"] and not(contains(lit["Address/Value"]))): # Not in the literal table
        LTT.put(lit["Address/Value"])
    elif('LTORG' in lit["Instruction"]):
        LTT.put(lit["Instruction"])
# Function that inserts literal into the code. ################UPDATED###############
def insertLiteral(lit):
    output.append(lit)
    value=str()
    if('LTORG' in lit["Instruction"]):
        while(value != "LTORG"):
            #,'Block':int(0)
            tup={'Location':'','Name':'','Instruction':'','Address/Value':'','op':''}
            value = LTT._get()
            if(value != "LTORG"):
                tup["Name"] = '*'
                tup["Instruction"] = "BYTE"
                tup["Address/Value"] = value[1:]
                output.append(tup)
    elif('END' in lit["Instruction"]):
        while(not(LTT.empty())):
            tup={'Location':'','Name':'','Instruction':'','Address/Value':'','op':''}
            value = LTT.get()
            tup["Name"] = '*'
            tup["Instruction"] = "BYTE"
            tup["Address/Value"] = value[1:]
            output.append(tup)
# Function that converts each line of code in the assembly file into dictionary.
def Read_file(inputfile):
    code = list(dict())
    with open(inputfile,'r') as f:
        for line in f:
            key = {"Location":'',"Name":'',"Instruction":'',"Address/Value":'',"op":''}
            lis=[]
            if(';' in line):
                line = line.split(';')[0]
                line += '\n'
            line2 = line.strip()
            line_code = line2.split()
            #key = {"Location":'',"Block":int(0),"Name":'',"Instruction":'',"Address/Value":'',"op":''}
            for row in line_code:
                if('\n' in row):
                    row = row[:-1]
                lis.append(row)
            for i in range(0,len(lis)):
                if(lis[i] in INSTS):
                    break
            if(i == 1):
                key['Instruction'] =lis[i]
                key["Name"] = lis[i-1]
            else:
                key["Instruction"] = lis[i]
            z = len(lis)
            if(len(lis) != i+1):
                key["Address/Value"] = lis[i+1]
            code.append(key)
    return code

# Function that calculate the value of EQU
def calc_equ(value,PC,row):
   global symtab
   if("*" in value):
        return str(Hex(((PC)),2))
   elif(value in symtab.keys()):
        return symtab[value]
   elif('+' in value):
        first = value.split('+')[0]
        second =value.split( '+')[1]
        return str(Hex(int(symtab[first][:4] ,16)+int(symtab[second][:4],16),2))
   elif('-' in value):
        first = value.split('-')[0]
        second = value.split('-')[1]
        return str(Hex(int(symtab[first][:4],16)-int((symtab[second][:4]),16),2))
   else:
       return Hex(int(str(row["Address/Value"])),2)

def calcu_ByteLocation(value):
    i = int()
    if("C'" in value):
        i=(len(value[2:])-1)
    elif("X'" in value):
        i=((len(value[2:]))-1)//2
    else:
        i= int(value)
    return i
# Function that Calculate weight of each instruction.
def calcu_InstructionLocation(row):
    inst = row["Instruction"]
    if(inst =="BYTE"):
        return calcu_ByteLocation(row["Address/Value"])
    elif(inst =="WORD"):
        return 3
    elif(inst =="RESW"):
        return int(row["Address/Value"])*3
    elif(inst =="RESB"):
        return int(row["Address/Value"] )
    elif(inst in Format1):
        return 1
    elif(inst in Format2):
        return 2
    elif(inst in Format3):
        return 3
    elif('+' in inst):
        return 4
    elif(inst in Format4f):
        return 4
    else:
        return 0

# Function to Calculate the address of the use blocks.
def calcu_UseBlocksAddress():
    for i in range(len(blocks)):
        blocks[i]["Length"] = Hex(blocks[i]["Length"])
        if(i != 0):
            blocks[i]["Address"] = Hex(Hex_Addition(Hex_ToDecimal(blocks[i-1]["Address"]),Hex_ToDecimal(blocks[i-1]["Length"])),2)

# Function to 
def display_symbol_table():
    global symtab
    with open('./outputs/symbtable.txt','w',newline='') as sym:
        sym.write(
            "SYMBOL  TABLE"+'\n'+'----------------------------------------'+'\n'
        )
        for symbol, location in symtab.items():
            sym.write(f"{symbol}\t{location}\n")
        sym.write(
            '\n'+'----------------------------------------'
        )
        sym.write(
            '\n'+"LITERAL TABLE"+'\n'+'----------------------------------------'+'\n'+'\n'
        )
        for ltt,location in LLTAB.items():
            sym.write(f"{ltt}\t{location}\n")
        sym.write(
            '\n'+'----------------------------------------'
        )
        
def useBlocks_Func(row):
    global block_num
    Exception_OutOfBlockRange(block_num)
    if(row["Address/Value"] == "DEFAULT"):
        if(use_DEFAULTB["blockNumber"] ==0):
            use_DEFAULTB["blockNumber"] = block_num
            block_num = block_num+1
            blocks.append(use_DEFAULTB)
        return use_DEFAULT
    if(row["Address/Value"] == "DEFAULTB"):
        if(use_DEFAULTB["blockNumber"] ==0):
            use_DEFAULTB["blockNumber"] = block_num
            block_num = block_num+1
            blocks.append(use_DEFAULTB)
        return use_DEFAULTB
    elif(row["Address/Value"] == "CDATA"):
        if(use_CDATA["blockNumber"] ==0):
            use_CDATA["blockNumber"] = block_num
            block_num = block_num+1
            blocks.append(use_CDATA)
        return use_CDATA
    elif(row["Address/Value"] == "CBLKS"):
        if(use_CBLKS["blockNumber"] ==0):
            use_CBLKS["blockNumber"] = block_num
            block_num = block_num+1
            blocks.append(use_CBLKS)
        return use_CBLKS
    else:
        return use_DEFAULT


##### updated the function to include EQU and parallels
def setLocation(row):
    global symtab
    global block
    if(row["Instruction"] == "USE"):
        block = useBlocks_Func(row)
    PC = block["Length"]
    #row['Block']=block['blockNumber']
    if(row["Instruction"] == "EQU"):
        row["Location"] =calc_equ(row["Address/Value"],PC,row)
        symtab[row["Name"]] =f'{calc_equ(row["Address/Value"],PC,row)}'
    row["Location"]=Hex((PC),2)
    if(row["Name"] != None and row["Name"] != " " and row["Name"] != "" and symtab.get(row["Name"]) == None and row["Name"] != "*" and row["Instruction"] != "START" and row["Instruction"] != "EQU"):
        symtab[row["Name"]]=f'{Hex(PC,2)}+{block["Name"]}'
    if(row['Name'] == '*'):
        LLTAB[row["Address/Value"]] = f'{Hex(PC,2)}+{block["Name"]}'
    PC=PC+calcu_InstructionLocation(row)
    block["Length"] = PC


def blockAddress(name):
    for block in blocks:
        if(block['Name'] ==name):
            return block['Address']
def generateSymbTable():
    for i in symtab:
        if('+' in symtab[i]):
            address = blockAddress(symtab[i][5:])
            symtab[i]=Hex(Hex_Addition(Hex_ToDecimal(symtab[i][:4]),Hex_ToDecimal(address)),2)
def generateLiteralTable():
    for i in LLTAB:
        blockName=str(LLTAB[i]).split('+')
        address = blockAddress(blockName[1])
        LLTAB[i]=Hex(Hex_Addition(Hex_ToDecimal(blockName[0]),Hex_ToDecimal(address)),2)
def generateLocation_1(code):
    global PC
    global Base
    for row in code:
        hasLiteral(row)
    for row in code:
        insertLiteral(row)
    for row in output:
         setLocation(row)
    calcu_UseBlocksAddress()
    generateSymbTable()
    generateLiteralTable()
    return output