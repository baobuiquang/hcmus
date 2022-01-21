# MSSV: 19120454
# Ho va ten: Bui Quang Bao

# Default that the input is in CNF form

class Clause():

    def printClause(self):
        return ""

    def listOfSymbols(self):
        return set()

    def listOfLiterals(self):
        return []

class Symbol(Clause):

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(("symbol", self.name))

    def printClause(self):
        return self.name

    def listOfSymbols(self):
        return {self.name}

    def listOfLiterals(self):
        ls = [Symbol(self.name)]
        return ls

class Not(Clause):
    def __init__(self, operand):
        self.operand = operand

    def __eq__(self, other):
        return isinstance(other, Not) and self.operand == other.operand

    def __hash__(self):
        return hash(("not", hash(self.operand)))

    def printClause(self):
        return "-" + self.operand.printClause()

    def listOfSymbols(self):
        return self.operand.listOfSymbols()

    def listOfLiterals(self):
        ls = [Not(self.operand)]
        return ls

class And(Clause):
    def __init__(self, *args):
        self.args = list(args)

    def __eq__(self, other):
        return isinstance(other, And) and self.args == other.args

    def __hash__(self):
        return hash(("and", tuple(hash(arg) for arg in self.args)))

    def add(self, arg):
        self.args.append(arg)

    def printClause(self):
        if len(self.args) == 1:
            return self.args[0].printClause()
        return " AND ".join([arg.printClause() for arg in self.args])

    def listOfSymbols(self):
        return set.union(*[arg.listOfSymbols() for arg in self.args])

class Or(Clause):
    def __init__(self, *args):
        try:
            for arg in args:
                if not isinstance(arg, Clause):
                    raise Exception('Not logical clause')
            self.args = list(args)
        except:
            if isinstance(args[0], list):
                self.args = args[0]
            else:
                raise Exception('Error at Or operation')

    def __eq__(self, other):
        return isinstance(other, Or) and self.args == other.args

    def __hash__(self):
        return hash(
            ("or", tuple(hash(arg) for arg in self.args))
        )

    def printClause(self):
        if len(self.args) == 1:
            return self.args[0].printClause()
        symbols_list = [arg.printClause() for arg in self.args]
        symbols_list.sort()
        return " OR ".join(symbols_list)

    def listOfSymbols(self):
        return set.union(*[arg.listOfSymbols() for arg in self.args])

    def listOfLiterals(self):
        ls = []
        for arg in self.args:
            ls.append(arg)
        return ls
