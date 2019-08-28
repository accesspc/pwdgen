.PHONY : install
install : 
	install -m 0755 -v ./pwdgen.py /usr/local/bin/pwdgen
	install -d /usr/local/lib/pwdgen
	cp -r ./character-lists /usr/local/lib/pwdgen
	cp -r ./wordlists /usr/local/lib/pwdgen

.PHONY : uninstall
uninstall :
	rm -f /usr/local/bin/pwdgen
	rm -rf /usr/local/lib/pwdgen

.PHONY : update
update :
	install -m 0755 -v ./pwdgen.py /usr/local/bin/pwdgen
	install -d /usr/local/lib/pwdgen
	cp -r ./character-lists /usr/local/lib/pwdgen
	cp -r ./wordlists /usr/local/lib/pwdgen
