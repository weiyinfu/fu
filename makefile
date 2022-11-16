update_package:
	pip uninstall fu
	python setup.py install
deploy_doc:
	rsync --progress -r doc/build  me:/home/ubuntu/app/fu
build-doc:
	cd doc && make html
install:
	python setup.py install