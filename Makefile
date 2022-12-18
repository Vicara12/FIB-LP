CMP := antlr4 -Dlanguage=Python3 -no-listener -visitor Funx.g


all: Funx.g TreeVisitor.py funx.py
	$(CMP)
	@echo
	@echo " ~~~~ CHECKING CODE FORMAT ~~~~"
	pycodestyle TreeVisitor.py
	pycodestyle funx.py
	@./tests.sh

server:
	./funx_interp.py
	export FLASK_APP=funx_interp
	flask run

