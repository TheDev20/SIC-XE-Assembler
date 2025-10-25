Format1 = { "FIX" : "C4", "FLOAT" : "C0", "HIO" : "F4", "SIO" : "F0", "TIO" : "F8"  ,"NORM" : "C8"}
Format2 =  { "ADDR": "90", "CLEAR":"B4", "COMPR":"A0","DIVR" :"9C" ,"MULR":"98","RMO":"AC","SHIFTL":"A4", "SHIFTR": "A8", "SUBR":"94","SVC":"B0","TIXR":"B8" }
Format3 = { "ADD" :"18", "ADDF":"58", "AND": "40", "COMP":"28", "COMPF":"88","DIV":"24", "DIVF":"64", "J": "3C" , "JEQ" :"30" , "JGT": "34","JLT":"38","JSUB":"48", "LDA":"00","LDB":"68","LDCH":"50","LDF":"70","LDL":"08","LDS":"6C","LDT":"74","LDX":"04", "LPS": "D0", "MUL":"20", "MULF":"60","OR":"44","RD":"D8","RSUB":"4C", "SSK":"EC", "STA":"0C", "STB":"78", "STCH":"54", "STF":"80", "STI":"D4", "STL":"14", "STS":"7C", "STSW":"E8", "STT":"84", "STX":"10", "SUB":"1C", "SUBF":"5C", "TD":"E0", "TIX":"2C", "WD":"DC" }


Format4 = { "+ADD" :"18", "+ADDF":"58", "+AND": "40", "+COMP":"28", "+COMPF":"88","+DIV":"24", "+DIVF":"64", "+J": "3C" , "+JEQ" :"30" , "+JGT": "34","+JLT":"38","+JSUB":"48", "+LDA":"00","+LDB":"68","+LDCH":"50","+LDF":"70","+LDL":"08","+LDS":"6C","+LDT":"74","+LDX":"04", "+LPS": "D0", "+MUL":"20", "+MULF":"60","+OR":"44","+RD":"D8","+RSUB":"4C", "+SSK":"EC", "+STA":"0C", "+STB":"78", "+STCH":"54", "+STF":"80", "+STI":"D4", "+STL":"14", "+STS":"7C", "+STSW":"E8", "+STT":"84", "+STX":"10", "+SUB":"1C", "+SUBF":"5C", "+TD":"E0", "+TIX":"2C", "+WD":"DC" }
Format4f = { "CADD": "BC" , "CSUB":"8C" ,"CLOAD" : "E4" , "CSTORE": "FC" ,"CJUMP":"CC" }

RegisterSyb={ "A":"0", "X":"1","L":"2","B":"3","S":"4","T":"5","F":"6","PC":"8","SW":"9"}


ASCII =  { 'A': '41' , 'B': '42' , 'C': '43' , 'D': '44' , 'E': '45' , 'F': '46' , 'G': '47' , 'H': '48' , 'I': '49'  , 'J': '4A' , 'K': '4B' , 'L': '4C' , 'M': '4D' , 'N': '4E' , 'O': '4F' , 'P': '50' , 'Q': '51' , 'R': '52' , 'S':'53', 'T': '54' , 'U': '55' , 'V': '56' , 'W': '57' , 'X': '58' , 'Y': '59' , 'Z': '5A' }
REG = { "A":"0", "X":"1","L":"2","B":"3","S":"4","T":"5","F":"6","PC":"8","SW":"9"}
FLAGS={ "Z":"0" , "N":"1" , "C":"2" , "V":"3" }

directives = ['START','END','BYTE','RESB','WORD','RESW','BASE','USE','LTORG','EQU']
INSTS = list(Format1.keys())+list(Format2.keys())+list(Format3.keys())+list(Format4.keys())+list(Format4f.keys())+directives