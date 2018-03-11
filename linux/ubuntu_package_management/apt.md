apt - Advanced Packaging Tool
---------------
### Determine what files a online package contains
This is possibly impossible via local apt interface, for store the info about the content of each package is not necessary, maintaining the content list does not help any aspects about solving the dependencies or installing the package

### apt-cache
apt-cache depends PACKAGE_NAME		show all the dependencies of PACKAGE_NAME
apt-cache rdepends PACKAGE_NAME		show all packages that depends on PACKAGE_NAME
apt-cache showpkg PACKAGE_NAME		show all the available version of PACKAGE_NAME from official repo	// apt show -a PACKAGE_NAME can also do this
apt-cache unmet [-i]

### TODO: determine which remote package provides specific file (esp. executable)
Why bash know which pacakge to be prompt for you to install when you type a command that does not exist on local machine yet provided by a package in the online repo?

### Downgrade
sudo apt-get install <package-name>=<specific-version-number>


