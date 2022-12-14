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

    def visitRoot (self, ctx):
        l = list(ctx.getChildren())
        self.parsing_functions = True
        for i in l:
            self.visit(i)
        self.parsing_functions = False
        for i in l:
            self.visit(i)

    def visitConditional (self, ctx):
        l = list(ctx.getChildren())
        # for each if, elseif or else statement
        for condition in l:
            # if the condition is true, skip the others
            true_cond, value = self.visit(condition)
            if true_cond:
                return value
        return None

    def visitIf (self, ctx):
        l = list(ctx.getChildren())
        if self.visit(l[1]):
            for x in l[3:-1]:
                val = self.visit(x)
                if self.infunction and val is not None:
                    return True, val
            # return true to let the conditional statement
            # know that this condition was met
            return True, None
        return False, None

    def visitElseif (self, ctx):
        l = list(ctx.getChildren())
        if self.visit(l[1]):
            for x in l[3:-1]:
                val = self.visit(x)
                if self.infunction and val is not None:
                    return True, val
            # same as if
            return True, None
        return False, None

    def visitExprFuncall (self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0])

    def visitFunction (self, ctx):
        # avoid visiting this element if not parsing functions
        # as functions were already parsed at the beginning
        if not self.parsing_functions:
            return
        l = list(ctx.getChildren())
        fname = l[0].getText()
        # get list of parameter names and function code
        texts = [x.getText() for x in l]
        params = []
        code = []
        parsing_params = True
        for elm in l[1:-1]:
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
            raise Exception("ERROR: repeated parameter names at function {}".format(fname))

        key = (fname, len(params))
        if key in self.functions.keys():
            raise Exception("ERROR: a version of the function {} with {} parameters already exists".format(fname, len(params)))
        self.functions[key] = (params,code)

    def visitPrint (self, ctx):
        l = list(ctx.getChildren())
        for item in l[1:-1]:
            txt = item.getText()
            if txt[0] == '"':
                print(txt[1:-1],end='')
            else:
                res = self.visit(item)
                print(res,end='')
        print()

    def visitFuncall (self, ctx):
        l = list(ctx.getChildren())
        fname = l[0].getText()
        if l[-1].getText() == ';':
            params = [self.visit(param) for param in l[1:-1]]
        else:
            params = [self.visit(param) for param in l[1:]]

        key = (fname, len(params))
        if key not in self.functions.keys():
            raise Exception("ERROR: function {} with {} parameters not found".format(fname, len(params)))

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

    def visitElse (self, ctx):
        l = list(ctx.getChildren())
        for x in l[2:-1]:
            val = self.visit(x)
            if self.infunction and val is not None:
                return True, val
        return True, None

    def visitStatement (self, ctx):
        # if this is not a function declaration, ignore it
        # when parsing functions
        if self.parsing_functions:
            return
        l = list(ctx.getChildren())
        if len(l) > 1:
            raise Exception("LANGUAGE ERROR: non atomic statement")
        res = self.visit(l[0])
        if not self.infunction and res is not None:
            print("Out: {}".format(res))
        return res

    def visitBVariable (self, ctx):
        l = list(ctx.getChildren())
        return self.contexts[-1][l[0].getText()]

    def visitBParentheses (self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[1])

    def visitNot (self, ctx):
        l = list(ctx.getChildren())
        return not self.visit(l[0])

    def visitAnd (self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) and self.visit(l[2])

    def visitOr (self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) or self.visit(l[2])

    def visitComparison (self, ctx):
        l = list(ctx.getChildren())

        if l[1].getText() == '>':
            return self.visit(l[0]) > self.visit(l[2])
        elif l[1].getText() == '>=':
            return self.visit(l[0]) >= self.visit(l[2])
        elif l[1].getText() == '<':
            return self.visit(l[0]) < self.visit(l[2])
        elif l[1].getText() == '<=':
            return self.visit(l[0]) <= self.visit(l[2])
        elif l[1].getText() == '=':
            return self.visit(l[0]) == self.visit(l[2])
        elif l[1].getText() == '!=':
            return self.visit(l[0]) != self.visit(l[2])
        else:
            raise Exception("LANGUAGE ERROR: unknown symbol {}".format(l[1].getText()))

    def visitExprToBool (self, ctx):
        l = list(ctx.getChildren())
        res = self.visit(l[0])
        return res != 0

    def visitTrue (self, ctx):
        return True

    def visitFalse (self, ctx):
        return False

    def visitWhile (self, ctx):
        l = list(ctx.getChildren())
        while self.visit(l[1]):
            for x in l[3:-1]:
                res = self.visit(x)
                if self.infunction and res is not None:
                    return res

    def visitVarassig (self, ctx):
        l = list(ctx.getChildren())
        value = self.visit(l[2])
        self.contexts[-1][l[0].getText()] = value

    def visitParentheses (self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[1])

    def visitPower (self, ctx):
        l = list(ctx.getChildren())
        val_l = self.visit(l[0])
        val_r = self.visit(l[2])
        if val_r < 0:
            expr = "".join([x.getText() for x in l])
            raise Exception("ERROR: negative powers are undefined in expr {}".format(expr))
        return val_l**val_r

    def visitMultDivMod (self, ctx):
        l = list(ctx.getChildren())
        val_l = self.visit(l[0])
        val_r = self.visit(l[2])
        if l[1].getText() == '*':
            return val_l * val_r
        elif val_r != 0:
            if l[1].getText() == '/':
                return val_l // val_r
            else:
                return val_l % val_r
        else:
            expr = "".join([x.getText() for x in l])
            raise Exception("ERROR: division by zero at expr {}".format(expr))

    def visitNegative (self, ctx):
        l = list(ctx.getChildren())
        return -self.visit(l[1])

    def visitPlusMinus (self, ctx):
        l = list(ctx.getChildren())
        val_l = self.visit(l[0])
        val_r = self.visit(l[2])
        if l[1].getText() == '+':
            return val_l + val_r
        else:
            return val_l - val_r

    def visitNumber (self, ctx):
        l = list(ctx.getChildren())
        return int(l[0].getText())

    def visitVariable (self, ctx):
        l = list(ctx.getChildren())
        varname = l[0].getText()

        if varname not in self.contexts[-1].keys():
            raise Exception("ERROR: unkwown variable name \"{}\"".format(varname))
        return self.contexts[-1][varname]

