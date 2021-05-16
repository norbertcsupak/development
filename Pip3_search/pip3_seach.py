#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  11 17:40:03 2020

@author: Pietro

"""

import sys
import subprocess
from pypi_simple import PyPISimple

def simple():
    package=input('\npackage to be checked ')
    try:
        with PyPISimple() as client:
            requests_page = client.get_project_page(package)
    except:
        print("\n SOMETHING WENT WRONG !!!!! \n\n",
        "CHECK INTERNET CONNECTION OR DON'T KNOW WHAT HAPPENED !!!\n")
    pkg = requests_page.packages[0]
    
    print(pkg)
    print(type(pkg))
    print('\nPackage_name: ',pkg,'\n')
    print('\nFilename: '+pkg.filename)
    print('\nUrl: '+pkg.url)
    print('\nproject: '+pkg.project)
    print('\nversion: '+pkg.version)
    print('\ntype: '+pkg.package_type)
    
if __name__ == '__main__': 
  #implement  pip as subprocess 
  #subprocess.check_call([sys.executable, '-m', 'pip', 'install','pypi_simple' ])
  simple()
