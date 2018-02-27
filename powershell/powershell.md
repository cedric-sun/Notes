a.ps1中以相对路径调用b.ps1
=============
`ps_script/a.ps1` calls `ps_script/b.ps1`

a.ps1:
`& "$(split-path $myinvocation.mycommand.path -Parent)\b.ps1"`	# run in standalone scope

`. "$(split-path $myinvocation.mycommand.path -Parent)\b.ps1"`	# run in current scope, just like `source` in linux bash
