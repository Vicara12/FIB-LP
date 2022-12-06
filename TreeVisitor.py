from FunxParser import FunxParser
from FunxVisitor import FunxVisitor


# iusful: FunxParser.symbolicNames[l[0].getSymbol().type] +


class TreeVisitor(FunxVisitor):
    def __init__(self):
        self.nivell = 0
        self.contexts = [{}]

    def visitRoot (self, ctx):
        l = list(ctx.getChildren())
        for i in l:
            res = self.visit(i)
            if res is not None:
                print(res)

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
            print("ERROR: division by zero at expr {}".format(expr))
            exit(1)

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
            print("ERROR: unkwown variable name \"{}\"".format(varname))
            exit(1)
        else:
            return self.contexts[-1][varname]

