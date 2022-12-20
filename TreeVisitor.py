from FunxParser import FunxParser
from FunxVisitor import FunxVisitor


# iusful: FunxParser.symbolicNames[l[0].getSymbol().type] +


class TreeVisitor(FunxVisitor):
    def __init__(self):
        self.nivell = 0
        self.contexts = [{}]
        # functions is a dictionary where the key is
        # the function name and number of arguments of
        # the function and the value is the argument names
        # and code
        self.functions = {}
        # if the program is executing a function things like
        # conditionals or while loops should return the first
        # thing that return a value that they encounter, whereas
        # in the main code conditionals and loops do not return
        # anything
        self.infunction = False
        self.parsing_functions = True
        self.output_to_buffer = False
        self.output_buffer = []

    def getStatics(self):
        # each item of statics holds a function or a variable
        # in case of a function the format is:
        # "Function", name of function, parameters
        # in case of a variable the format is:
        # "Variable", name of the variable, str(value)
        statics = []
        for key, val in self.functions.items():
            statics.append(("Function", key[0], " ".join(val[0])))

        for name, val in self.contexts[-1].items():
            statics.append(("Variable", name, str(val)))
        return statics

    def setOutputToBuffer(self, output_to_buffer):
        self.output_to_buffer = output_to_buffer

    def writeOutput(self, text):
        if self.output_to_buffer:
            self.output_buffer.append(text)
        else:
            print(text)

    def getOutputBuffer(self):
        return self.output_buffer

    def visitRoot(self, ctx):
        self.output_buffer = []
        childs = list(ctx.getChildren())
        self.parsing_functions = True
        for i in childs:
            self.visit(i)
        self.parsing_functions = False
        for i in childs:
            self.visit(i)

    def visitConditional(self, ctx):
        childs = list(ctx.getChildren())
        # for each if, elseif or else statement
        for condition in childs:
            # if the condition is true, skip the others
            true_cond, value = self.visit(condition)
            if true_cond:
                return value
        return None

    def visitIf(self, ctx):
        childs = list(ctx.getChildren())
        if self.visit(childs[1]):
            for x in childs[3:-1]:
                val = self.visit(x)
                if self.infunction and val is not None:
                    return True, val
            # return true to let the conditional statement
            # know that this condition was met
            return True, None
        return False, None

    def visitElseif(self, ctx):
        childs = list(ctx.getChildren())
        if self.visit(childs[1]):
            for x in childs[3:-1]:
                val = self.visit(x)
                if self.infunction and val is not None:
                    return True, val
            # same as if
            return True, None
        return False, None

    def visitExprFuncall(self, ctx):
        childs = list(ctx.getChildren())
        return self.visit(childs[0])

    def visitFunction(self, ctx):
        # avoid visiting this element if not parsing functions
        # as functions were already parsed at the beginning
        if not self.parsing_functions:
            return
        childs = list(ctx.getChildren())
        fname = childs[0].getText()
        # get list of parameter names and function code
        texts = [x.getText() for x in childs]
        params = []
        code = []
        parsing_params = True
        for elm in childs[1:-1]:
            t = elm.getText()
            if t == '{':
                parsing_params = False
                continue
            if parsing_params:
                params.append(t)
            else:
                code.append(elm)
        # check that all parameters are different
        if len(params) != len(set(params)):
            msg = "ERROR: repeated parameter names at function {}"
            raise Exception(msg.format(fname))

        key = (fname, len(params))
        if key in self.functions.keys():
            msg = "ERROR: a version of the function {} with {}\
 parameters already exists"
            raise Exception(msg.format(fname, len(params)))
        self.functions[key] = (params, code)

    def visitPrint(self, ctx):
        childs = list(ctx.getChildren())
        output = ""
        for item in childs[1:-1]:
            txt = item.getText()
            if txt[0] == '"':
                output += txt[1:-1]
            else:
                res = self.visit(item)
                output += str(res)
        self.writeOutput(output)

    def visitFuncall(self, ctx):
        childs = list(ctx.getChildren())
        fname = childs[0].getText()
        if childs[-1].getText() == ';':
            params = [self.visit(param) for param in childs[1:-1]]
        else:
            params = [self.visit(param) for param in childs[1:]]

        key = (fname, len(params))
        if key not in self.functions.keys():
            msg = "ERROR: function {} with {} parameters not found"
            raise Exception(msg.format(fname, len(params)))

        # generate new context with function variables
        function = self.functions[key]
        new_context = {}
        for i in range(key[1]):
            new_context[function[0][i]] = params[i]
        self.contexts.append(new_context)

        # execute function code until something returns a
        # value that is not none, otherwise return none
        old_inf = self.infunction
        self.infunction = True
        for code_item in function[1]:
            val = self.visit(code_item)
            if val is not None:
                self.contexts.pop(-1)
                self.infunction = old_inf
                return val
        self.infunction = old_inf
        self.contexts.pop(-1)

    def visitElse(self, ctx):
        childs = list(ctx.getChildren())
        for x in childs[2:-1]:
            val = self.visit(x)
            if self.infunction and val is not None:
                return True, val
        return True, None

    def visitStatement(self, ctx):
        # if this is not a function declaration, ignore it
        # when parsing functions
        if self.parsing_functions:
            return
        childs = list(ctx.getChildren())
        if len(childs) > 1:
            raise Exception("LANGUAGE ERROR: non atomic statement")
        res = self.visit(childs[0])
        if not self.infunction and res is not None:
            self.writeOutput("Out: {}".format(res))
        return res

    def visitBVariable(self, ctx):
        childs = list(ctx.getChildren())
        return self.contexts[-1][childs[0].getText()]

    def visitBParentheses(self, ctx):
        childs = list(ctx.getChildren())
        return self.visit(childs[1])

    def visitNot(self, ctx):
        childs = list(ctx.getChildren())
        return not self.visit(childs[0])

    def visitAnd(self, ctx):
        childs = list(ctx.getChildren())
        return self.visit(childs[0]) and self.visit(childs[2])

    def visitOr(self, ctx):
        childs = list(ctx.getChildren())
        return self.visit(childs[0]) or self.visit(childs[2])

    def visitComparison(self, ctx):
        childs = list(ctx.getChildren())

        if childs[1].getText() == '>':
            return self.visit(childs[0]) > self.visit(childs[2])
        elif childs[1].getText() == '>=':
            return self.visit(childs[0]) >= self.visit(childs[2])
        elif childs[1].getText() == '<':
            return self.visit(childs[0]) < self.visit(childs[2])
        elif childs[1].getText() == '<=':
            return self.visit(childs[0]) <= self.visit(childs[2])
        elif childs[1].getText() == '=':
            return self.visit(childs[0]) == self.visit(childs[2])
        elif childs[1].getText() == '!=':
            return self.visit(childs[0]) != self.visit(childs[2])
        else:
            msg = "LANGUAGE ERROR: unknown symbol {}"
            raise Exception(msg.format(childs[1].getText()))

    def visitExprToBool(self, ctx):
        childs = list(ctx.getChildren())
        res = self.visit(childs[0])
        return res != 0

    def visitTrue(self, ctx):
        return True

    def visitFalse(self, ctx):
        return False

    def visitWhile(self, ctx):
        childs = list(ctx.getChildren())
        while self.visit(childs[1]):
            for x in childs[3:-1]:
                res = self.visit(x)
                if self.infunction and res is not None:
                    return res

    def visitVarassig(self, ctx):
        childs = list(ctx.getChildren())
        value = self.visit(childs[2])
        self.contexts[-1][childs[0].getText()] = value

    def visitParentheses(self, ctx):
        childs = list(ctx.getChildren())
        return self.visit(childs[1])

    def visitPower(self, ctx):
        childs = list(ctx.getChildren())
        val_l = self.visit(childs[0])
        val_r = self.visit(childs[2])
        if val_r < 0:
            expr = "".join([x.getText() for x in childs])
            msg = "ERROR: negative powers are undefined in expr {}"
            raise Exception(msg.format(expr))
        return val_l**val_r

    def visitMultDivMod(self, ctx):
        childs = list(ctx.getChildren())
        val_l = self.visit(childs[0])
        val_r = self.visit(childs[2])
        if childs[1].getText() == '*':
            return val_l * val_r
        elif val_r != 0:
            if childs[1].getText() == '/':
                return val_l // val_r
            else:
                return val_l % val_r
        else:
            expr = "".join([x.getText() for x in childs])
            msg = "ERROR: division by zero at expr {}"
            raise Exception(msg.format(expr))

    def visitNegative(self, ctx):
        childs = list(ctx.getChildren())
        return -self.visit(childs[1])

    def visitPlusMinus(self, ctx):
        childs = list(ctx.getChildren())
        val_l = self.visit(childs[0])
        val_r = self.visit(childs[2])
        if childs[1].getText() == '+':
            return val_l + val_r
        else:
            return val_l - val_r

    def visitNumber(self, ctx):
        childs = list(ctx.getChildren())
        return int(childs[0].getText())

    def visitVariable(self, ctx):
        childs = list(ctx.getChildren())
        varname = childs[0].getText()

        if varname not in self.contexts[-1].keys():
            msg = "ERROR: unkwown variable name \"{}\""
            raise Exception(msg.format(varname))
        return self.contexts[-1][varname]
