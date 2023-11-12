dev: clean
	# echo "Now building dev..."
	python3 -m build
	pip3 install -r ./requirements.txt
	pip3 install --upgrade dist/*.whl
	# echo "Building dev complete."

test1:
	civitdl batchstr '123456,78901,23456' ./test/models/test1

test2:
	civitdl batchfile ./test/batchtest1.txt ./test/models/test2

test: dev test1 test2


clean:
	# echo "Now cleaning..."
	rm -rf **/*.egg-info
	rm -rf dist
	rm -rf ./test/models
	pip3 uninstall civitai-batch-download -y
	# echo "Cleaning complete."
