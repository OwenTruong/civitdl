dev: clean
	python3 -m build
	pip3 install --upgrade dist/*.whl

test: dev
	civitdl batchstr '123456,78901,23456' ./test/models/test1
	civitdl batchfile ./test/batchtest1.txt ./test/models/test2


clean:
	rm -rf **/*.egg-info
	rm -rf dist
	rm -rf ./test/models
	pip3 uninstall civitai-batch-download -y
