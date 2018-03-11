PACKAGE NOTES
==============
1. No pacakge depends on ubuntu-minimal
2. dpkg itself has no knowledge of what "dependency" is. And its output of dpkg -l is somewhat confusing: Desired is called "selection state" elsewhere, althrough this field usually represent the intent of the user about "what do you want to do with this package". So even some package is installed as a dependency (i.e. not because the user explicitly specify it as the argument of apt-get), dpkg will mark the "desired" field of the dependency as "install"
3. !!! vim-common=2:7.4.1689-3ubuntu1.2 disappeared in `apt-cache` after downgrade to 2:7.4.1689-3ubuntu1
4. 
5. `sslocal` binary provided by obsolete package "shadowsocks" is unable to support encryption method "chacha20-ietf-poly1305". The old "shadowsocks" package in official repo (at least in xenial) is implemented using python, and might now be in the state of no-longer-maintained. Use package "shadowsocks-libev" instead.

TODO
==============
1. How does dpkg understand dependencies?
```	
	dpkg: error processing package sogoupinyin (--install):
	 dependency problems - leaving unconfigured
```
