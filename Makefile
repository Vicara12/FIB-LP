CMP := antlr4 -Dlanguage=Python3 -no-listener -visitor Funx.g

all: Funx.g TreeVisitor.py funx.py
	$(CMP)
	@./tests.sh

