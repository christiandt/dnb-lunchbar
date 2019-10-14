all:
	pip install -r requirements.txt

run:
	python main.py $(update)

gui:
	python gui.py

package:
	python setup.py py2app
