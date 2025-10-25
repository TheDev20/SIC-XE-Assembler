dir = directives = ['START','END','BASE','USE','LTORG','EQU']
def generateOutput(outCode,name,keys):
    with open("./outputs/{file}.txt".format(file = name),'w',newline='') as output_file:
        for row in outCode:
            loc = isDirective(row)
            value=loc+'      '+row['Name']

            col = 10-len(row['Name'])
            value=calcu_spaces(value,col)
            value +=row['Instruction']
            col = 10-len(row['Instruction'])
            value=calcu_spaces(value,col)
            value +=row['Address/Value']
            col = 17-len(row['Address/Value'])
            value=calcu_spaces(value,col)
            value +=row['op']+'\n'
            output_file.write(value)

def calcu_spaces(value,col):
    for i in range(0,col):
        value +=" "
    return value

def generateOutputHTME(H,T,M,E):
    with open("./outputs/HTME.txt",'w',newline='') as output_file:
        i = 0
        h = "H" +" "+H['progName']+" "+H['startAddress']+" "+H['length']+'\n'
        e = "E" +" "+E['startAddress']
        t = str()
        m = str()
        for trecord in T:
            if(i!=0):
                t += 'T'+' '+trecord['startAddress']+' '+trecord['length']
                for op in trecord['opCode']:
                    t +=' '+op
                t +='\n'
            i =1
        for maddress in M['Address']:
            m += 'M'+' '+maddress+' '+'05'+'\n'
        
        output_file.write(
            h + t + m + e
        )

def isDirective(inst):
    if( inst['Instruction'] in dir):
        return '    '
    else:
        return inst['Location']