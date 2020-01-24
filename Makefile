.PHONY: dep
dep:
	apt-get install libcurl4-gnutls-dev python-setuptools -y
	wget -O gitinspector.deb https://github.com/ejwa/gitinspector/releases/download/v0.4.3/gitinspector_0.4.3-1_all.deb && dpkg -i gitinspector.deb
	pip3 install -r requirements.txt # install dependancies
	chmod +x app # add file permission to execute

.PHONY: dev
dev:
	sudo apt install python3-pip # install python3 pip
	pip install --upgrade autopep8
	pip3 install -r requirements.txt # install dependancies
	chmod +x app # add file permission to execute

.PHONY: docs
docs: 
	@echo "Generating docs"
	sudo npm i apidoc -g # install apidoc
	apidoc -i routes -o docs # create docs

.PHONY: build
build:
	docker image build -t angadsharma1016/dscinfo-backend .

.PHONY: heroku-release
heroku-release:
	heroku container:push web
	heroku container:release web

.PHONY: clean
clean:
	pip3 uninstall -r requirements.txt  # Uninstall dependancies
	find . -name "*pyc" -type f -delete # Delete .pyc files

.PHONY: lint
lint:
	autopep8 --in-place --aggressive --aggressive app
	autopep8 --in-place --aggressive --aggressive utility/*.py
	autopep8 --in-place --aggressive --aggressive routes/*.py
