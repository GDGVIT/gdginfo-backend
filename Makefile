.PHONY: dep
dep:
	sudo apt install python3-pip
	pip3 install -r requirements.txt 
	chmod +x app


.PHONY: docs
docs: 
	@echo "Generating docs"
	sudo npm i apidoc -g
	apidoc -i routes -o docs

.PHONY: clean
clean:
	pip3 uninstall -r requirements.txt 