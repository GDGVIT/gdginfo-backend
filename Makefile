.PHONY: dep
dep:
	sudo apt install python3-pip # install python3 pip
	pip3 install -r requirements.txt # install dependancies
	chmod +x app # add file permission to execute


.PHONY: docs
docs: 
	@echo "Generating docs"
	sudo npm i apidoc -g # install apidoc
	apidoc -i routes -o docs # create docs

.PHONY: clean
clean:
	pip3 uninstall -r requirements.txt  # Uninstall dependancies
	find . -name "*pyc" -type f -delete # Delete .pyc files
