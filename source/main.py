import copy

def handle_input(filename):
    with open(filename, "r") as file:
        M = int(file.readline())
        query = [file.readline().strip().split(" OR ") for _ in range(M)]

        N = int(file.readline())
        KB = [file.readline().strip().split(" OR ") for _ in range(N)]

    return query, KB

def handle_output(is_success, clauses):
    if is_success:
        success = "YES"
    else:
        success = "NO"
    # loops_count = [len(clauses[i]) for i in range(len(clauses))]
    path = "../output/"
    filename = input("Enter the output filename: ")
    filename = path + filename
    file = open(filename, 'w')

    for i in range(len(clauses)):
        file.write(str(len(clauses[i])) + "\n")
        for literal in clauses[i]:
            if len(literal) == 1: 
                line = str(literal[0])
            elif len(literal) == 0:
                line = str("{}")
            else:
                string = " OR "
                line = string.join(literal)
            file.write(line + "\n")
    file.write(success)
    file.close()

def negate_literal(clause):
    new_clause = []
    for literal in clause:
        for i in range(len(literal)):
            tmp_literal = literal[i].split()[0]
            if tmp_literal.__contains__('-') == True:
                new_clause.append([str(tmp_literal.strip('-'))])
            else:
                new_clause.append(['-' + str(tmp_literal)])
    return new_clause

# def valid_literal(clause):
#     neg_clause = copy.copy(clause)
#     neg_clause = negate_literal(neg_clause)
#     for literal in clause:
#         for neg_literal in neg_clause:
#             if literal == neg_literal:
#                 return True

def check_negation_literal(l1, l2):
    if len(l1) == len(l2):
        return False
    if l1[-1] == l2[-1]:
        return True
    
def CNF(query, KB):
    neg_query = negate_literal(query)
    # print(neg_query)
    return KB + neg_query

def PL_resolve(c1, c2):
    temp_c1 = copy.deepcopy(c1)
    temp_c2 = copy.deepcopy(c2)
    resolvents = None

    pop_c1, pop_c2 = [], []

    for i in range(len(temp_c1)):
        for j in range(len(temp_c2)):
            if check_negation_literal(temp_c1[i], temp_c2[j]):
                pop_c1.append(temp_c1[i])
                pop_c2.append(temp_c2[j])

    if len(pop_c1) > 1:
        resolvents = None
        return resolvents
    for i in pop_c1:
        temp_c1.remove(i)
    for j in pop_c2:
        temp_c2.remove(j)
        resolvents = temp_c1 + temp_c2

    if resolvents is None:
        return resolvents
    resolvents = sorted(set(resolvents), key = lambda sub : sub[-1])
    return resolvents
    # for lit in temp_c1:
    #     neg_lit = negate_literal([lit])
    #     neg_lit = [neg_lit[i][0] for i in range(len(neg_lit))]
        
    #     resolvent = []
    #     for i in range(len(neg_lit)):
    #         if neg_lit[i] in temp_c2[0]:
    #             temp_c2[0].remove(neg_lit[i])
    #             temp_c1[0].remove(lit[i])
        
    #         resolvent = temp_c1[0] + temp_c2[0]
    #         print(resolvent)
    # return [resolvents]

def PL_resolution(query, KB):
    clauses = CNF(query, KB)
    # print(clauses)
    new_clause = []

    while True:
        temp_new_clause = []        
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                resolvents = PL_resolve(clauses[i], clauses[j])
                # print(clauses[i], clauses[j])
                # print(resolvents)
                # input()
        
                if resolvents == []:
                    temp_new_clause.append(resolvents)
                    new_clause.append(temp_new_clause)
                    # print(new)
                    # print(new_clause)
                    return True, new_clause
                if resolvents != None:
                    if resolvents not in clauses and resolvents not in temp_new_clause:
                        temp_new_clause.append(resolvents)
        if temp_new_clause == []:
            new_clause.append(temp_new_clause)
            return False, new_clause
        new_clause.append(temp_new_clause)
        clauses += temp_new_clause
        
def main():
    path = "../input/"
    filename = input("Enter the filename: ")
    filename = path + filename
    alpha, KB = handle_input(filename)
    is_success, clauses = PL_resolution(alpha, KB)
    handle_output(is_success, clauses)

if __name__ == "__main__":
    main()