install: uninstall
	pip3 install .

install2: uninstall
	python3 -m build
	pip3 install -r ./requirements.txt
	pip3 install --upgrade dist/*.whl

test1:
	civitdl 123456 '78901,23456' ./test/models/test1 --verbose

test2:
	civitdl ./test/batchtest1.txt ./test/models/test2 --verbose

test3:
	# civitconfig sorter -a test3 ./custom/sort.py
	# civitconfig alias -a @test ./test
	# civitconfig alias -a @test3 @test/models/test3
	civitdl 191977 @test3/default --verbose
	civitdl 123456 @test3/alphabet -s ./custom/sort.py --verbose
	civitdl 78901 @test3/test3 -s test3 --verbose
	civitdl 23456 @test3/tags -s tags --verbose
	civitconfig default --with-prompt
	civitdl 80848 @test3/test-prompt-1 --verbose
	civitconfig default --no-with-prompt
	civitdl 80848 @test3/test-prompt-2 --verbose

test4:
	civitdl 80848 ./test/models/test4/with-prompt --verbose --with-prompt
	civitdl 80848 ./test/models/test4/without-prompt --verbose --no-with-prompt

test5:
	civitdl 123456 ./test/models/test5/500000 --limit-rate 500000 --verbose
	civitdl 123456 ./test/models/test5/500k --limit-rate 500k --verbose
	civitdl 123456 ./test/models/test5/1m --limit-rate 1M --verbose
	civitdl 123456 ./test/models/test5/5m --limit-rate 5m --verbose

errortest1:
	civitdl ./test/errortest1.txt ./test/models/errortest1 --verbose

errortest2:
	civitdl ./test/errortest2.txt ./test/models/errortest2 --verbose

test: install test1 test2 test4 test5

quicktest: install
	civitdl 80848 ./test/models/quicktest --verbose

clean:
	rm -rf **/*.egg-info
	rm -rf dist build
	rm -rf ./test/models

uninstall: clean
	pip3 uninstall civitdl -y
