import re
from convertHex import *
from SICXEInstructionset import *
from generateOutput import generateOutput,generateOutputHTME
from ErrorHandler import *
# htme records
Mr=list()
Tr = list()
Hrecord ={"progName": "", "startAddress": "0000", "length": ""}
Trecord = list(dict())
Mrecord = {"M": "M", "Address":Mr}
Erecord = {"E":"E", "startAddress": ""}
T={"startAddress": "0000", "length": "00", "opCode": Tr}
length =0
breakFlag = True
Base = Hex(0,2)
blocks = list()
block =dict()
symtab = list()
LLTAB = list()
# with open('./outputs/output.txt', 'r') as file:
#     csv_reader = csv.DictReader(file, delimiter='\t')
#     code = [row for row in csv_reader]

def isBlock(name):
    if(name == ''):
        block = blocks[0]
        return block
    else:
        for b in blocks:
            if(b['Name'] == name):
                block = b
                return block
def calcu_Base(row,PC):
    global Base
    if(row["Address/Value"] == '*'):
         Base = PC
    elif(row['Address/Value'][0] == '#'):
         Base = Hex(int(row['Address/Value'][1:]),2)
    else:
         Base = symtab[row['Address/Value']]
def directivebehaviour(row):
     row ["op"] = ""
def wordbehaviour(row):
     row["op"] = Hex(int(row["Address/Value"]),3)
def bytebehaviour(row):
     if(row["Address/Value"][0] == 'X' or row["Address/Value"][0] == 'x' ):
          row["op"] = row["Address/Value"][2:-1]
     elif(row["Address/Value"][0] == 'C' or row["Address/Value"][0] == 'c' ):
          word = row["Address/Value"][2:-1]
          for char in word:
               row["op"] = row["op"] + ASCII[char]
def format1behaviour(row):
     row["op"] = Format1[row["Instruction"]]
def format2behaviour(row):
     row["op"] = Format2[row["Instruction"]]
     register1 = row["Address/Value"][0]
     if(row["Instruction"] in["CLEAR"  ,"TIXR" , "SVR"]):
               row["op"] = row["op"] + REG[register1] + "0"
     else:
          register2 = '0'
          if(len(row["Address/Value"]) > 1):
               register2 = REG[row["Address/Value"][2]]
          row["op"] = row["op"] + REG[register1] + register2               
                   
def PC_relative(TA,PC):
     disp = Hex(Hex_ToDecimal(Hex_Subtraction(TA,PC)))
     return disp
def Base_relative(TA,bits):
     disp= Hex_ToDecimal(Hex_Subtraction(Hex_ToDecimal(TA),Hex_ToDecimal(Base)))
     return Bits_ToHex(disp,bits)
def AddressingMode(TA,PC,bits):
     disp_PC = PC_relative(TA,PC)
     disp_Base = Base_relative(TA,bits)
     if(not(len(disp_PC) >= 4)):
          return '2'+Bits_ToHex(disp_PC,bits)
     elif ( (Hex_ToDecimal(disp_Base) >= 0) and (Hex_ToDecimal(disp_Base) <= 4095) ):
          return '4'+disp_Base
def format3behavior(row,PC):
     disp = Hex(0)
     op = '00'
     flagBits=0
     Exception_NotInSymbolTable(row['Address/Value'],symtab,LLTAB)
     if(row['Instruction'] == 'RSUB'):
          return '4F0000'
     elif(row['Address/Value'][0] == '#'):
         TA = row['Address/Value'][1:]
         op = Hex_Addition(Hex_ToDecimal(Format3[row["Instruction"]]),1)
         if(TA in symtab.keys()):
              TA = symtab[TA]
              num = AddressingMode(TA,PC,12)
              flagBits += int(num[0])
              disp = num[1:]
         else:
              disp =Bits_ToHex(int(TA),12)
     elif(row['Address/Value'][0] == '@'):
         TA = row['Address/Value'][1:]
         op = Hex_Addition(Hex_ToDecimal(Format3[row["Instruction"]]),2)
         TA = symtab[TA]
         num = AddressingMode(TA,PC,12)
         flagBits += int(num[0])
         disp = num[1:]
     else:
         value = str(row['Address/Value']).split(',')
         TA = value[0]
         if(TA[1:] in LLTAB.keys()):
              TA = LLTAB[TA[1:]]
         else:
              TA = symtab[TA]
         if(len(value)>1):
              flagBits +=8
         op = Hex_Addition(Hex_ToDecimal(Format3[row["Instruction"]]),3)
         num = AddressingMode(TA,PC,12)
         flagBits += int(num[0])
         disp = num[1:]
     return Bits_ToHex(op+Bits_ToHex(flagBits,4)+disp,24)

def format4behavior(row):
     disp = Hex(0)
     op = '00'
     flagBits=1
     Exception_NotInSymbolTable(row['Address/Value'],symtab,LLTAB)
     if(row['Instruction'] == '+RSUB'):
          return '4F000000'
     elif(row['Address/Value'][0] == '#'):
         TA = row['Address/Value'][1:]
         op = Hex_Addition(Hex_ToDecimal(Format4[row["Instruction"]]),1)
         if(TA in symtab.keys()):
              TA = symtab[TA]
              disp = Bits_ToHex(TA,20)
         else:
              disp = Bits_ToHex(TA,20)
     elif(row['Address/Value'][0] == '@'):
         TA = row['Address/Value'][1:]
         op = Hex_Addition(Hex_ToDecimal(Format4[row["Instruction"]]),2)
         TA = symtab[TA]
         disp = Bits_ToHex(TA,20)
     else:
          value = str(row['Address/Value']).split(',')
          TA = value[0]
          if(TA in symtab.keys()):
               TA = symtab[TA]
               disp = Bits_ToHex(TA,20)
          else:
               disp = Bits_ToHex(TA,20)
          op = Hex(Hex_Addition(Hex_ToDecimal(Format4[row["Instruction"]]),3),1)
     return Bits_ToHex(op+Bits_ToHex(flagBits,4)+disp,30)
def format4Fbehavior(row):
     op = Format4f[row['Instruction']]
     REG_MEM_FLAG=str(row['Address/Value']).split(',')
     if(row['Instruction'] == 'CJUMP'):
          Exception_NotInSymbolTable(REG_MEM_FLAG[0],symtab,LLTAB)
          reg='0'
          mem=symtab[REG_MEM_FLAG[0]]
          flag = FLAGS[REG_MEM_FLAG[1]]
          reg = Hex_FromBinary(Hex_ToBinary(reg)+'00') 
          reg = Hex_Addition(Hex_ToDecimal(reg) , Hex_ToDecimal(flag))
     else:
          Exception_NotInSymbolTable(REG_MEM_FLAG[1],symtab,LLTAB)
          reg=REG[REG_MEM_FLAG[0]]
          mem=symtab[REG_MEM_FLAG[1]]
          flag=FLAGS[REG_MEM_FLAG[2]]
          op = Hex_Addition(Hex_ToDecimal(op), int(Hex_ToDecimal((reg))/4))
          reg = Hex(Hex_ToDecimal(reg)&3)
          reg = Hex_FromBinary(Hex_ToBinary(reg)+'00') 
          reg = Hex_Addition(Hex_ToDecimal(reg) , Hex_ToDecimal(flag))
     return op+reg+Bits_ToHex(mem,20)
def generatePass2(code,_symtab,_LLTAB,_blocks):
     global symtab
     global blocks
     global LLTAB
     global PC
     symtab = _symtab
     LLTAB = _LLTAB
     blocks= _blocks
     block = blocks[0]
     end = False
     i = 0
     for r in range(len(code)):
          i +=1
          row = code[r]
          if(row["Instruction"] !="END"):
               location=code[r+1]['Location']
               if((code[r+1]['Instruction'] == 'USE')):
                    location = Hex_Addition(Hex_ToDecimal(code[r]['Location']),Hex_ToDecimal('3'))
          if(row["Instruction"] == 'USE'):
               block=isBlock(row['Address/Value'])
          PC = Hex(Hex_Addition(Hex_ToDecimal(block['Address']),Hex_ToDecimal(location)),2)
          if(row['Instruction'] == 'BASE'):
               calcu_Base(row,PC)
          elif row["Instruction"] == "USE" or row["Instruction"] == "EQU" or row["Instruction"] == "LTORG" or row["Instruction"] == "BASE" or row["Instruction"] == "Start" or row["Instruction"] == "RESW" or row["Instruction"] == "RESB":
               directivebehaviour(row)
          elif (row["Instruction"] == "WORD"):
               wordbehaviour(row)
          elif (row["Instruction"] == "BYTE"):
               bytebehaviour(row)
          elif (row["Instruction"]in Format1):
               format1behaviour(row)
          elif((row["Instruction"]) in Format2.keys()):
               format2behaviour(row)
          elif(row["Instruction"] in Format3.keys()):
               code[r]['op']= format3behavior(row,PC)
          elif(row["Instruction"] in Format4.keys()):
               code[r]['op']= format4behavior(row)
          elif(row["Instruction"] in Format4f.keys()):
               code[r]['op']= format4Fbehavior(row)
          if(i == len(code)):
               end = True
          generateHTME(row,block,end)
     # print_records(Hrecord,Trecord,Mrecord,Erecord)
     generateOutput(code,'pass2',code[0].keys())
     generateOutputHTME(Hrecord,Trecord,Mrecord,Erecord)
     
     

def generateHTME(row,block,end):
     global breakFlag
     global Tr
     global Mr
     global T
     global length
     progLength = '0'
     checkLength= int((length + len(row["op"]))/2)
     if(row["Instruction"] == "START"):
          Hrecord["progName"] = row["Name"]
          for z in range(0,7-len(Hrecord["progName"])):
               Hrecord["progName"]+='X'
          Hrecord["startAddress"] = Hex(row["Location"],3)
          for b in blocks:
               progLength = Hex_Addition(b["Length"],progLength)
          Hrecord["length"] = Hex(progLength,3)
          Erecord["startAddress"] = Hex(Hrecord["startAddress"],3)
     elif(row['Instruction']== 'BASE' or row['Instruction'] == 'LTORG'):
          pass
     elif(row['Instruction']== 'USE' or row['Instruction']== 'RESB' or row['Instruction']== 'RESW' or row['Instruction']== 'EQU'):
          breakFlag = True
     elif(end):
          T["length"] = Hex(int(length/2),1)
          Trecord.append(T)
     else:
          if(checkLength>30):
               breakFlag = True
          if((row['Instruction'] in Format4 )):
               label = row['Address/Value']
               if((row['Address/Value'][0] in '#@') and (row['Address/Value'][1:] in symtab.keys())):
                    label = row['Address/Value'][1:]
               if(label in symtab.keys()):
                    Mr.append(Hex(Hex_Addition(Hex_ToDecimal(Hex_Addition(row['Location'],block['Address'])),1),3))
          if(row['Instruction'] in Format4f):
               Mr.append(Hex(Hex_Addition(Hex_ToDecimal(Hex_Addition(row['Location'],block['Address'])),1),3))
          if(breakFlag):
               T["length"] = Hex(int(length/2),1)
               Trecord.append(T)
               length =0
               Tr =[]
               T={"startAddress":0, "length":0, "opCode": Tr}
               T["startAddress"] = Hex(Hex_Addition(row['Location'],block['Address']),3)
               length += len(row["op"])
               Tr.append(row["op"])
               breakFlag=False
          else:
               Tr.append(row["op"])
               length +=len(row["op"])