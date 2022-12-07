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

    def visitConditional (self, ctx):
        l = list(ctx.getChildren())
        # for each if, elseif or else statement
        for condition in l:
            # if the condition is true, skip the others
            if self.visit(condition):
                return

    def visitIf (self, ctx):
        l = list(ctx.getChildren())
        if self.visit(l[1]):
            for x in l[3:-1]:
                self.visit(x)
            # return true to let the conditional statement
            # know that this condition was met
            return True
        return False

    def visitElseif (self, ctx):
        l = list(ctx.getChildren())
        if self.visit(l[1]):
            for x in l[3:-1]:
                self.visit(x)
            # same as if
            return True
        return False

    def visitElse (self, ctx):
        l = list(ctx.getChildren())
        for x in l[2:-1]:
            self.visit(x)
        return True

    def visitStatement (self, ctx):
        l = list(ctx.getChildren())
        if len(l) > 1:
            print("LANGUAGE ERROR: non atomic statement")
        res = self.visit(l[0])
        if res is not None:
            print(res)

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
            print("LANGUAJE ERROR: unknown symbol {}".format(l[1].getText()))

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
                self.visit(x)

    def visitPrint (self, ctx):
        l = list(ctx.getChildren())
        for item in l[1:-2]:
            print(item.getSymbol().type)

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

