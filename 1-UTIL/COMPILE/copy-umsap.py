#--> Imports
import platform
import shutil
import getpass
import platform

from distutils.dir_util import copy_tree
from pathlib            import Path

#--> VARIABLES 
cwd = Path.cwd()
user = getpass.getuser()
cOS = platform.system()

if cOS == 'Darwin':
	pathF = '/Users/'
	spec = Path(pathF + user + '/Dropbox/UMSAP/CODE/2-RESOURCES/BUNDLE/MAC/UMSAPm.spec')
else:
	pathF = 'C:/Users/'
	spec  = Path(pathF + user + '/Dropbox/UMSAP/CODE/2-RESOURCES/BUNDLE/WIN/UMSAP.spec')
	specH = Path(pathF + user + '/Dropbox/UMSAP/CODE/2-RESOURCES/BUNDLE/WIN/version.txt')

#--> FOLDERS TO COPY
source = Path(pathF + user + '/Dropbox/UMSAP/CODE/0-CODE/')
img    = Path(pathF + user + '/Dropbox/UMSAP/CODE/2-RESOURCES/IMAGES/')
data   = Path(pathF + user + '/Dropbox/UMSAP/LOCAL/DATA/')
dataF  = ['LIMPROT', 'TARPROT', 'PROTPROF']

#--> FILES TO COPY
icon   = Path(pathF + user + '/Dropbox/UMSAP/CODE/2-RESOURCES/ICON/MAC/icon.icns')
icon2  = Path(pathF + user + '/Dropbox/UMSAP/CODE/2-RESOURCES/ICON/WIN/icon2.ico')
manual = Path(pathF + user + '/Dropbox/UMSAP/CODE/2-RESOURCES/MANUAL/manual.pdf')
config = Path(pathF + user + '/Dropbox/UMSAP/CODE/2-RESOURCES/CONFIG/config_def.json')

#--> START RUNNING
##--> ASK IF PLAYGROUND FOLDER CAN BE DELETED
print("The content of folder:")
print(str(cwd))
print("will be deleted")
print("Are you sure about this?")
var = input("Y/N:")

##--> PROCCESS ANSWER
if var == "Y" or var == "y":
 #--> DELETE PLAYGROUND
	print('')
	print('Deleting content of folder: ' + str(cwd))
	for item in cwd.iterdir():
		print('Deleting: ' + str(item)) 
		if item.is_dir():
			shutil.rmtree(item)
		else:
			item.unlink()
 #--> COPY FILES AND FOLDERS
  ##--> CODE
	print('')
	print('Copying UMSAP files')
	copy_tree(str(source), str(cwd))
  ##--> RESOURCE
   ###--> CREATE FOLDER
	res = cwd / 'RESOURCES'
	res.mkdir()
   ###--> IMAGES
	print('')
	print('Copying Resources: IMAGES')
	resI = res / 'IMAGES'
	copy_tree(str(img), str(resI))
   ###--> MANUAL
	print('')
	print('Copying Resources: MANUAL')
	resM = res / 'MANUAL'
	resM.mkdir()
	resM = resM / 'manual.pdf'
	shutil.copyfile(manual, resM)
   ###--> DEFAULT CONFIG FILE
	print('')
	print('Copying Resources: CONFIG')
	resC = res / 'CONFIG'
	resC.mkdir()
	resC = resC / 'config_def.json'
	shutil.copyfile(config, resC)
   ###--> ICON
	print('')
	for i in [icon, icon2]:
		print('Copying Resources: ' + str(i))
		loc = resI / i.name
		shutil.copyfile(i, loc)
   ###--> SPEC
	print('')
	print('Copying Resources: ' + str(spec))		
	loc = cwd / spec.name
	shutil.copyfile(spec, loc)
	if cOS == 'Windows':
		print('Copying Resources: ' + str(specH))		
		loc = cwd / specH.name
		shutil.copyfile(specH, loc)		
	else:
		pass
   ###--> DATA FOLDER
	print('')
	print('Copying PlayDATA folders')
	resD = cwd / 'PlayDATA'
	for f in dataF:
		print('Copying PlayDATA folders: ' + f)
		lf = data / f
		resDf = resD  / f
		copy_tree(str(lf), str(resDf))
   ###--> FINAL PRINT
	print("\nAll Done. Enjoy!!")
else:
 #--> QUIT
	print("You typed: " + var)
	print("Nothing will be done")


