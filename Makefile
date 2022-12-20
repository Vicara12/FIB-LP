CMP := antlr4 -Dlanguage=Python3 -no-listener -visitor Funx.g


all: Funx.g TreeVisitor.py funx.py
	$(CMP)
	@echo
	@echo " ~~~~ CHECKING CODE FORMAT ~~~~"
	pycodestyle TreeVisitor.py
	pycodestyle funx.py
	pycodestyle app.py
	@./tests.sh

server:
	./app.py
	flask run

