update_package:
	pip uninstall fu
	python setup.py install
deploy_doc:
	rsync --progress -r doc/build  tencent:/home/ubuntu/app/fu