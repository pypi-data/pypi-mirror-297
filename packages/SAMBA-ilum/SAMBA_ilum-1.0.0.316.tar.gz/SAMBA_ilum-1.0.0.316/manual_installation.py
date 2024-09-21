# SAMBA_ilum Copyright (C) 2024 - Closed source


import os
import sys
import site
import shutil
import subprocess

#---------------------------------------------------
# Instalation directory ----------------------------
#---------------------------------------------------

code_name = 'samba_ilum'

dir_inst = site.USER_SITE + '/' + code_name

#----------------------------------------------------------------------
# Copying samba_ilum folder to the main directory ---------------------
#----------------------------------------------------------------------

if os.path.isdir(dir_inst):
   shutil.rmtree(dir_inst)
else:
   0 == 0

shutil.copytree(code_name, dir_inst)

print("")
print("##########################################################")
print("#################  Installation started  #################")
print("##########################################################")
print("")
print("==========================================================")
print("Instructions to execute:                                  ")
print("                                                          ")
print(">>  Go to a directory containing the DFT outpout files    ")
print("                                                          ")
print(">>  Type the following comand:                            ")
print("                                                          ")
print(f'    python -m {code_name}                                ') 
print("    or                                                    ")
print(f'    python3 -m {code_name}                               ')
print("    or                                                    ")
print(f'    python3.x -m {code_name}                             ')
print("                                                          ")
print("*** RUN IT WITH YOUR PYTHON VERSION OR WITH ***           ")
print("*** THE VERSION OF YOUR INSTALLATION DIRECTORY ***        ")
print("--------------------------------------------------        ")
print(f'Installation Directory: {dir_inst}                       ')
print("==========================================================")
print("")
      
print("##########################################################")
print("# Manual software installation is recommended:           #")
print("# ====================================================== #")
print("# VESTA: http://jp-minerals.org/vesta/en/download.html   #")
print("# ------------------------------------------------------ #")
print("# 3D Visualization of the Crystalline lattice (CONTCAR), #")
print("# charge density (CHGCAR) and Potential (LOCPOT)         #")
print("# ====================================================== #")
print("##########################################################")
print(" ")

print("===================================================================")
print(" Installation / Updating the necessary modules --------------------")
print("===================================================================")
print(" Would you like to update and install all necessary dependencies?  ")
print(" modules: numpy|requests|pyfiglet|vasprocar                        ")
print(" ----------------------------------------------------------------- ")
print(" [0] NO                                                            ")
print(" [1] YES                                                           ")
print("===================================================================")
modulos = input(" "); modulos = int(modulos)
print(" ")

if (modulos == 1):

   # ---------------------------------------------------------
   # package_list_to_instal ----------------------------------
   # ---------------------------------------------------------
   
   packages = [
   'numpy', 
   'requests',
   'pyfiglet',
   'vasprocar'
   ]

   for i in range(len(packages)):
       subprocess.run(["pip", "install", "--upgrade", packages[i]])
       print("[OK] " + packages[i])

   print(" ")
   print("##########################################################")
   print("########## SAMBA_ilum installation is complete. ##########")
   print("##########################################################")
   print(" ")

   stop = input( )
