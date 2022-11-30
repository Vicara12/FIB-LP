CMP := antlr4 -Dlanguage=Python3 -no-listener -visitor Funx.g

bld:
	$(CMP)

all: Funx.g TreeVisitor.py funx.py
	$(CMP)
	@./tests.sh

