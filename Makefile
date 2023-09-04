dev:
	python3 -m build
	pip3 install --upgrade dist/*.whl


clean:
	rm -rf **/*.egg-info
	rm -rf dist
	pip3 uninstall civitai-batch-download
