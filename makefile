update_package:
	pip uninstall fu
	python setup.py install
deploy_doc:
	rsync --progress -r doc/build  me:~/app/MyStatic/fudoc
build-doc:
	cd doc && make html
install:
	python setup.py install
deploy:
	rsync --progress -r ./ me:~/package/fu