import json
import subprocess
import pkg_resources
import tkinter as tk
import urllib.request
from tkinter import filedialog



root = tk.Tk()
root.withdraw()
choosen_file = filedialog.askopenfilenames()

with open(choosen_file[0],'r') as f:
    data = json.load(f)

#print(data)
package_dict = {}
# This list contain the package name and version
require_package = [] 
for key in data:
    if(key=="Dependencies"):
        for package in data[key]:
            version = data[key][package]
            package_dict[package] = version
            require_package.append(package+":"+version)


installed_package_details = pkg_resources.working_set
installed_package_list = {}
for obj in installed_package_details:
    installed_package_list[obj.key] = obj.version

def check_connection(host='https://www.google.com/'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False


for package in package_dict:
    if package in installed_package_list.keys():
        # if version is not same
        if(package_dict[package] != installed_package_list[package]):
            output = subprocess.run('pip install -Iv '+package+'=='+package_dict[package],capture_output=True)
            if(output.returncode==1 and check_connection()==False):
                print("Error!!! Check Internet Connection...")
            elif(output.returncode==0):
                print(package+" is installed :)")
            elif(output.returncode==1 and check_connection()==True):
                print("Error!!! Check the package name")
        else:
            print("Package ",package," is already installed")
    else:
        output = subprocess.run('pip install '+package+'=='+package_dict[package],capture_output=True)
        if(output.returncode==1 and check_connection()==False):
            print("Error!!! Check Internet Connection...")
        elif(output.returncode==0):
            print(package+" is installed :)")
        elif(output.returncode==1 and check_connection()==True):
            print("Error!!! Check the package name")
    print('\n')



        