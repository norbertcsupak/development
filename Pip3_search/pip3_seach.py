import sys
import pip
import subprocess

def install_package(package):
    if hasattr(pip, 'main'):
        pip.main(['install',package])
    else:
        pip._internal.main(['install',package])

def simple():
    package=input('\nPackage to be checked: ')
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
  install_package('pypi_simple')
  from pypi_simple import PyPISimple
  simple()
