# MSSV: 19120454
# Ho va ten: Bui Quang Bao

input_file_name = ['input_1.txt', 'input_2.txt', 'input_3.txt', 'input_4.txt', 'input_5.txt']
output_file_name = ['output_1.txt', 'output_2.txt', 'output_3.txt', 'output_4.txt', 'output_5.txt']

from propositional_logic import *

# Default that the input is in CNF form

# ===========================================================================
# Artificial Intelligence: A Modern Approach, Third Edition, 
# Chapter 7, Image 7.12, func PL-RESOLUTION
#
# function PL-RESOLUTION(KB, α) returns true or false
#      inputs: KB, the knowledge base, a sentence in propositional logic
#              α, the query, a sentence in propositional logic
#      clauses ← the set of clauses in the CNF representation of KB ∧ ¬α
#      new ← { }
#      loop do
#            for each pair of clauses Ci, Cj in clauses do
#                  resolvents ← PL-RESOLVE(Ci, Cj)
#                  if resolvents contains the empty clause then return true
#                  new ← new ∪ resolvents
#            if new ⊆ clauses then return false
#            clauses ← clauses ∪ new
# ===========================================================================
def PL_RESOLUTION(knowledge, query):
    # clauses ← the set of clauses in the CNF representation of KB ∧ ¬α
    clauses = knowledge + [Not(query)]
    # new ← {}
    newList = []
    # For output
    output_clause = []
    output_num = []
    # loop do
    while True:
        print('Current Clauses: ', end='')
        print(clausesPrint(clauses))
        # for each pair of clauses Ci, Cj in clauses do
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(0,n) for j in range(i+1,n)]
        for (ci, cj) in pairs:
            # resolvents ← PL-RESOLVE(Ci, Cj)
            resolvents = PL_RESOLVE(ci, cj, clauses)
            # (this was moved down on purpose) if resolvents contains the empty clause then return true
            # if '{}' in resolvents:
            #     return True
            # new ← new ∪ resolvents
            for e in resolvents:
                if not e in newList:
                    newList.append(e)

        # if new ⊆ clauses then return false
        newIsSubset = True
        for e in newList:
            if not e in clauses:
                newIsSubset = False
        if newIsSubset:
            return [False, output_num, output_clause]

        # clauses ← clauses ∪ new
        count = 0
        for e in newList:
            if not e in clauses:
                clauses.append(e)
                output_clause.append(clausesPrint([e]))
                count += 1
        output_num.append(count)
        print(f'Number of clauses to add: {count}')

        # if clauses contains the empty clause then return true
        if '{}' in clauses:
            return [True, output_num, output_clause]

        print('------------------------------------------------------------------------')

# Apply Resolution Principle
def PL_RESOLVE(ci, cj, PL_RESOLUTION_clauses):
    new_clauses = []
    ciList = ci.listOfLiterals()
    cjList = cj.listOfLiterals()

    # Check if we have empty clause
    if len(ciList) == 1 and len(cjList) == 1:
        if ciList[0] == Not(cjList[0]) or cjList[0] == Not(ciList[0]):
            new_clauses = ['{}']
    # If we haven't had empty clause yet
    else:
        for e_ci in ciList:
            for e_cj in cjList:
                # If exists: X and -X
                if e_ci == Not(e_cj) or Not(e_ci) == e_cj:
                    tempCi = ciList
                    tempCj = cjList
                    tempCi.remove(e_ci)
                    tempCj.remove(e_cj)
                    cur_new_clauses = list(set(tempCi + tempCj))

                    # Apply logic op to clause(s)
                    can_append = False
                    if len(cur_new_clauses) == 1:
                        cur_new_clause = cur_new_clauses[0]
                        can_append = True
                    # This is used to remove clause like: A OR B OR -B
                    elif len(cur_new_clauses) > 1:
                        flag = True
                        for ei in cur_new_clauses:
                            for ej in cur_new_clauses:
                                if ei == Not(ej) or Not(ei) == ej:
                                    flag = False
                        if flag:
                            cur_new_clause = Or(cur_new_clauses)
                            can_append = True

                    # If has new clause, append
                    if can_append:
                        new_clauses.append(cur_new_clause)
    
    # Make sure that we don't return duplicate clauses
    for ei in new_clauses:
        for ej in PL_RESOLUTION_clauses:
            if ei == ej or ei == Not(Not(ej)) or Not(Not(ei)) == ej:
                new_clauses.remove(ei)

    # Print to console for debug
    if len(new_clauses) != 0:
        print(f'> PL_RESOLVE: [{ci.printClause():<12}] and [{cj.printClause():<12}]\t->\t', end='')
        # print(f'> ({ci.printClause()}) hợp giải với ({cj.printClause()})\t->\t', end='')
        print('[' + clausesPrint(new_clauses) + ']')

    # Return PL_RESOLVE
    return new_clauses

# Make clause printing easier to read
def clausesPrint(ls):
    res_str = ''
    try:
        for e in ls:
            res_str += e.printClause() + '; '
        res_str = res_str[:-2]
    except:
        res_str = ls[0]
    return res_str







# Split a text into symbols
def splitSymbolsByOr(s_text):
    symbols = []
    s = s_text
    def countOr(s):
        return s.count('OR')
    for i in range(countOr(s)):
        idx = s.find('OR') - 1
        cur_symbol = s[:idx]
        symbols.append(cur_symbol)
        s = s[idx+4:]
    symbols.append(s)
    return symbols

# symbols_string
def extractSymbols(lines):
    symbols = []
    for i, line in enumerate(lines):
        if i != 1:
            for symbol in splitSymbolsByOr(line):
                if symbol[0] == '-':
                    if not symbol[1:] in symbols:
                        symbols.append(symbol[1:])
                else:
                    if not symbol in symbols:
                        symbols.append(symbol)
    return symbols

# clauses_string
def extractLines(lines):
    lns = []
    for line in lines:
        lns.append(line)
    return lns

# Return logical symbol from text symbol
def symStrToLogical(sym_string, symbols_string, symbols_logical):
    if sym_string[0] != '-':
        idx = symbols_string.index(sym_string)
        return symbols_logical[idx]
    else:
        idx = symbols_string.index(sym_string[1:])
        return Not(symbols_logical[idx])

# Return logical clause from text clause
def clauseStrToLogical(clause_string, symbols_string, symbols_logical):
    clause_logical = None

    syms_string_temp = splitSymbolsByOr(clause_string)
    if len(syms_string_temp) == 1:
        sym_string = syms_string_temp[0]
        clause_logical = symStrToLogical(sym_string, symbols_string, symbols_logical)
    else:
        temp_clause_list = []
        for sym_string in syms_string_temp:
            temp_clause_list.append(symStrToLogical(sym_string, symbols_string, symbols_logical))
        clause_logical = Or(temp_clause_list)

    return clause_logical



for i in range(len(input_file_name)):
    # Read file and call PL_RESOLUTION
    read_file_successfully = False
    with open(input_file_name[i], 'r') as f_input:
        lines = [line.rstrip() for line in f_input.readlines()]
        symbols_string = extractSymbols(lines)
        symbols_logical = []
        clauses_string = extractLines(lines)
        clauses_logical = []
        # Create logical symbols
        for sym in symbols_string:
            symbols_logical.append(Symbol(sym))

        n_kb = int(clauses_string[1])
        clauses_string.remove(clauses_string[1])
        
        # Return logical clauses from text clauses
        for clause_string in clauses_string:
            clause_logical = clauseStrToLogical(clause_string, symbols_string, symbols_logical)
            clauses_logical.append(clause_logical)

        query = clauses_logical[0]
        knowledge = clauses_logical[1:]

        # print(f'symbols_string : {symbols_string}')
        # print(f'symbols_logical: {clausesPrint(symbols_logical)}')
        # print(f'clauses_string : {clauses_string}')
        # print(f'clauses_logical: {clausesPrint(clauses_logical)}')
        print('========================================================================')
        print(f"{'Knowledge:':<12}{clausesPrint(knowledge)}")
        print(f"{'Query:':<12}{clausesPrint([query])}")
        print('========================================================================')
        pl_res = PL_RESOLUTION(knowledge, query)
        print(f'\n>> Entailment: {pl_res[0]}')
        # print(f'output_num = {pl_res[1]}')
        # print(f'output_clause = {pl_res[2]}')
        print('========================================================================')

        # Write output to file
        write_file_successfully = False
        with open(output_file_name[i], 'w') as f_output:
            j = 0
            for count in pl_res[1]:
                f_output.write(f'{count}\n')
                for i in range(count):
                    f_output.write(f'{pl_res[2][j]}\n')
                    j += 1
            if pl_res[0] == True:
                f_output.write(f'YES')
            else:
                f_output.write(f'0\nNO')
            write_file_successfully = True
            f_output.close()
        
        if not write_file_successfully:
            print('> Failed to write file!')

        read_file_successfully = True
        f_input.close()

    if not read_file_successfully:
        print('> Failed to read file!')