import os.path
import sys
from passOneAssembler import *
from generateOutput import *
from passTwoAssembler import generatePass2
# ############ MAIN ##########
file= f'./inputs/{sys.argv[1]}'
if(not(os.path.isfile(file))):
     raise Exception(f'File {sys.argv[1]} does not exist.')
inCode= Read_file(file)
outCode= generateLocation_1(inCode)
generateOutput(outCode,'pass1',outCode[0].keys())
display_symbol_table()
generatePass2(outCode,symtab,LLTAB,blocks)