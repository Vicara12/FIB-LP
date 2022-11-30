from FunxParser import FunxParser
from FunxVisitor import FunxVisitor


# iusful: FunxParser.symbolicNames[l[0].getSymbol().type] +


class TreeVisitor(FunxVisitor):
    def __init__(self):
        self.nivell = 0

    def visitRoot (self, ctx):
        l = list(ctx.getChildren())
        res = self.visit(l[0])
        print(res)

    def visitParentheses (self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[1])

    def visitPower (self, ctx):
        l = list(ctx.getChildren())
        val_l = self.visit(l[0])
        val_r = self.visit(l[2])
        return val_l**val_r

    def visitMultDiv (self, ctx):
        l = list(ctx.getChildren())
        val_l = self.visit(l[0])
        val_r = self.visit(l[2])
        if l[1].getText() == '*':
            return val_l * val_r
        elif val_r != 0:
            return val_l / val_r
        else:
            expr = "".join([x.getText() for x in l])
            print("ERROR: division by zero at expr {}".format(expr))
            return None

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
