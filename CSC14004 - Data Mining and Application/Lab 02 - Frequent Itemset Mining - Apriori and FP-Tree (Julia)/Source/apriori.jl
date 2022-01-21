# Bui Quang Bao
# 19120454

# Data Mining - Lab02 - Frequent Itemset Mining

# How to use:
# 1. Change some settings below
# 2. Open command line, cd to directory has "apriori.jl"
# 3. Run: julia apriori.jl

# Settings ===================================
input_file_name = "data/test.txt"             # Input file
min_support_count = 3                         # Minimum support count for Apriori Algorithm
min_confidence = 0.8                          # Only choose rules have confidence >= min_confidence
                                              # To print all Association Rules: min_confidence = 0
# ============================================

# Just un-comment 1 group of codes below for quick settings:

# input_file_name = "data/mushrooms.txt"
# min_support_count = 4000
# min_confidence = 0.97

# input_file_name = "data/chess.txt"
# min_support_count = 3000
# min_confidence = 0.98

# input_file_name = "data/foodmartFIM.txt"      # Not recommended, take time to finish
# min_support_count = 15
# min_confidence = 0

# input_file_name = "data/retail.txt"           # Not recommended, take A LOT OF time to finish
# min_support_count = 10000
# min_confidence = 0.5

# ============================================

# Return True if set 1 is a subset of set 2, False if not
function isSubSet(l1, l2)
    for i in l1
        if !(i in l2)
            return false
        end
    end
    return true  
end

# Return True if set 1 is equal to set 2, False if not
function isEqualSet(l1, l2)
    if length(l1) != length(l2)
        return false
    end
    for i in l1
        if !(i in l2)
            return false
        end
    end
    return true  
end

# Sub-function for Apriori Algorithm
# Input: data list
# Return: L1
function apriori_data_to_L1(data, min_supp)
    items_list = []
    # Get all items and count
    for t in data
        for item in t
            existed = false
            for e in items_list
                if item == e[1][1]
                    existed = true
                    e[2] += 1
                end
            end
            if !existed
                push!(items_list, [[item], 1])
            end
        end
    end
    # Only accept items with count >= min_supp
    result_list = []
    for e in items_list
        if e[2] >= min_supp
            push!(result_list, e)
        end
    end
    return result_list
end
# Sub-function for Apriori Algorithm
# Input: L[k-1]
# Return: Items of C[k]
function apriori_L_to_C_items(L)
    print("L -> C's items")
    items_list = []
    result_list = []
    # Create an unique items list
    for e in L
        for i in e[1]
            if !(i in items_list)
                push!(items_list, i)
            end
        end
    end
    # Create combined list
    for e in L
        for i in items_list
            temp = []
            if !(i in e[1])
                for j in e[1]
                    push!(temp, j)
                end
                push!(temp, i)
                # temp.sort()
                sort!(temp)
                if !(temp in result_list)
                    push!(result_list, temp)
                end
            end
        end
    end
    return result_list
end
# Sub-function for Apriori Algorithm
# Input: Items of C[k]
# Return: C[k]
function apriori_C_items_to_C(data, C_items)
    print(" | C's items -> C")
    C = [[e, 0] for e in C_items]
    # Start counting
    for t in data
        for c in C
            if isSubSet(c[1],t)
                c[2] += 1
            end
        end
    end
    return C
end
# Sub-function for Apriori Algorithm
# Input: C[k]
# Return: L[k]
function apriori_C_to_L(C, min_supp)
    println(" | C -> L")
    L = []
    for c in C
        if c[2] >= min_supp
            push!(L, c)
        end
    end
    return L
end
# Sub-function for Apriori Algorithm
# Just print the apriori result to the console
function apriori_print(L)
    println("============================ Result ===============================")
    println("Itemset -> Support Count")
    for l in L
        for e in l
            ls_print(e[1])
            print(" -> ")
            println(e[2])
        end
    end
    println("===================================================================")
end

# Just to print array beautifully
function ls_print(ls)
    print("[")
    first_ele = true
    for e in ls
        if first_ele
            print("$e")
        else
            print(", $e")
        end
        first_ele = false
    end
    print("]")
end

# ======================== Apriori Algorithm =========================
function apriori(data, min_support_count)
    L = []
    # Initialize L with L1
    push!(L, apriori_data_to_L1(data, min_support_count))
    k = 2
    # Find all L[k] from L[k-1] until L[k-1] is empty
    while !isempty(L[k-1])
        print("> Processing: L[$(k-1)] to L[$(k)]: ")
        # Find L[k] from L[k-1]
        # Use all the sub-function for Apriori
        Lk = apriori_C_to_L(
            apriori_C_items_to_C(
                data, apriori_L_to_C_items(L[k-1])
            ), min_support_count
        )
        # Add L[k] to L
        push!(L, Lk)
        k += 1
    end
    # Just remove the last is an empty list
    pop!(L)
    # Just print the apriori result to the console
    apriori_print(L)
    return L
end
# ====================================================================

# Return the confidence of a rule: KB -> alpha
function apriori_confidence(apriori_result, KB, alpha)
    itemset = []
    for e in KB
        push!(itemset, e)
    end
    for e in alpha
        if !(e in itemset)
            push!(itemset, e)
        end
    end

    sup_count_itemset = 0
    sup_count_KB = -1

    for l in apriori_result
        for i in l
            if isEqualSet(itemset, i[1])
                sup_count_itemset = i[2]
            end
            if isEqualSet(KB, i[1])
                sup_count_KB = i[2]
            end
        end
    end

    # print("Confidence($KB => $alpha) = ")
    # print(sup_count_itemset/sup_count_KB)
    # println(" - $sup_count_itemset / $sup_count_KB")
    # println("===================================================================")

    return sup_count_itemset/sup_count_KB
end

# Return powerset of a set
# Example: [1, 2, 3]
# Return: [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]
function powerset(x::Vector{T}) where T
    result = Vector{T}[[]]
    for e in x, j in eachindex(result)
        push!(result, [result[j] ; e])
    end
    return result
end

# Association Rules Generation
# Print all rules (from an itemset) with confidence >= min_confidence
function rules_gen(apriori_result, itemset, min_confidence)
    if length(itemset) != 0
        n = length(itemset)
        rules_right = []
        rules_left = []
        for powerset in powerset(itemset)
            if (length(powerset) != n) && (length(powerset) != 0)
                push!(rules_left, powerset)
            end
        end
        for e in rules_left
            push!(rules_right,symdiff(itemset, e))
        end
        # Print to console
        for i = 1:length(rules_left)
            conf = apriori_confidence(apriori_result, rules_left[i], rules_right[i])
            if conf >= min_confidence
                # print("Confidence($(rules_left[i]) => $(rules_right[i])) = ")
                print("Confidence(")
                ls_print(rules_left[i])
                print(" => ")
                ls_print(rules_right[i])
                print(") = ")
                println(round(conf; digits = 2))
            end
        end
    end
end

# Just apply rules_gen for all frequent itemset
function rules_gen_for_all_itemset(apriori_result, min_confidence)
    println("All Association Rules with confidence >= $min_confidence:")
    for i = 2:length(apriori_result)
        for e in apriori_result[i]
            rules_gen(apriori_result, e[1], min_confidence)
        end
    end
end

# Main
open(input_file_name) do f_input
    println("====================== Apriori Processing =========================")
    lines = []
    temp = []
    data = []
    # Read input file
    while ! eof(f_input)    
       s = rstrip(readline(f_input))
       push!(lines, s)
    end
    println("> Read file successfully")
    # Turn data into data list
    for line in lines
        push!(temp, split(line, " "))
    end
    for t in temp
        push!(data, [parse(Int, x) for x in t])
    end
    println("> Turn data into proper format successfully")
    # ===========================================================================
    # Apriori
    apriori_result = apriori(data, min_support_count)
    # Rule Generation
    rules_gen_for_all_itemset(apriori_result, min_confidence)
    println("===================================================================")
end