def Exception_NotInSymbolTable(label,symtab,LTTAB):
    if(label == ''):
         return 0
    if(',' in label):
         label = label.split(',')
         label = label[0]
    if(label[0] in '@#='):
        label = label[1:]
    error = f"Label {label} not in symbol table."
    if (label in symtab.keys()) or (label in symtab.keys()) or (label in LTTAB.keys()):
        pass
    else:
            try:
                int(label)
            except:
                raise Exception(error)
    
def Exception_OutOfBlockRange(b):
    if(b > 4):
        raise Exception("Out of block range")
    