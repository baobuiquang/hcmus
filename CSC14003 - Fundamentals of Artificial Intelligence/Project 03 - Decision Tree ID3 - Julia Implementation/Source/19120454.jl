# =========================================================================
# MSSV: 19120454
# Ho ten: Bui Quang Bao
# =========================================================================
# Bai lam chi su dung cac thu vien ho tro input, tinh toan, random
# Thuat toan cay quyet dinh ID3 hoan toan duoc cai dat thu cong
# =========================================================================
# Data: iris.csv
# Cach su dung (command line): julia 19120454.jl
# =========================================================================
# Vi du console output:
# 
# > Imported: DataFrames, CSV, Random
# > Reading data > Completed
#
# Petal Length <= 1.9
#    Left Node: String15["Iris-setosa"]
#    Right Node: Petal Width <= 1.7
#       Left Node: Petal Length <= 5.1
#             Left Node: String15["Iris-versicolor"]
#             Right Node: String15["Iris-virginica"]
#       Right Node: Petal Length <= 4.8
#          Left Node: String15["Iris-versicolor"]
#          Right Node: String15["Iris-virginica"]
#
# Accuracy: 0.92
# =========================================================================

NCOLS = 5
ATTRIBUTES = ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]


# ============================ Libraries =================================
# using Pkg
# Pkg.add("DataFrames")
# Pkg.add("CSV")
# Pkg.add("Random")
println("=========================================================================")
print("> Imported: ")
using DataFrames
print("DataFrames")
using CSV
print(", CSV")
using Random
println(", Random")

# =========================== Node Struct ==============================
mutable struct Node
    # Decision Nodes
    feature_index
    threshold
    left
    right
    info_gain
    # Leaf Nodes
    value
end

# =========================== Tree Struct ==============================
mutable struct DecisionTree
    root
    min_samples_split
    max_depth
end

# ============================ ID3 Main Functions ===============================
# Split data into train and test
function splitTrainTest(data, train_ratio = 2/3)
    split_point = trunc(Int, length(data) * train_ratio)
    data_train = data[1 : split_point]
    data_test = data[split_point+1 : length(data)]
    return data_train, data_test
end

# Start ID3 and call the function decisionTree recursively
function startBuildDecisionTree(self, X, Y)
    dataset = concatenate(X, Y)
    self.root = decisionTree(self, dataset)
end

# Fit the dataset into a decision tree
function decisionTree(self, dataset, curr_depth = 0)

    # println("==============================================")
    # print("> build_tree > len(dataset) = ")
    # print(length(dataset))
    # print(" > curr_depth = ")
    # println(curr_depth)

    X, Y = lsSliceLast(dataset)
    num_samples, num_features = length(X), length(X[1])

    # Prevent overfitting with threshold
    if (num_samples >= self.min_samples_split) && (curr_depth <= self.max_depth)
        # Find the best split of the dataset
        best_split = bestSplit(self, dataset, num_features)
        # If information gain > 0
        if best_split["info_gain"] > 0
            # Left node
            left_subtree = decisionTree(self, best_split["dataset_left"], curr_depth + 1)
            # Right node
            right_subtree = decisionTree(self, best_split["dataset_right"], curr_depth + 1)
            # Return decision node
            return Node(
                best_split["feature_index"], 
                best_split["threshold"],
                left_subtree, 
                right_subtree, 
                best_split["info_gain"],
                nothing
            )
        end
    end

    # Leaf node
    leaf_value = calculate_leaf_value(Y)
    return Node(nothing, nothing, nothing, nothing, nothing, leaf_value)
end

# Find the best split
function bestSplit(self, dataset, num_features)

    # print("> get_best_split > len(dataset) = ")
    # print(length(dataset))
    # print(" > num_features = ")
    # println(num_features)

    # dictionary to store the best split
    best_split = Dict()
    max_info_gain = -Inf
    # loop over all the features
    for feature_index = 1:num_features
        feature_values = getCol(dataset, feature_index)
        possible_thresholds = unique(feature_values)

        # print("> possible_thresholds (")
        # print(length(possible_thresholds))
        # print("): ")
        # println(possible_thresholds)

        # Loop over the possible thresholds
        for threshold in possible_thresholds
            
            # Split the data
            dataset_left, dataset_right = split_left_right(dataset, feature_index, threshold)

            # print("len(dataset_left) = ")
            # println(length(dataset_left))
            # print("len(dataset_right) = ")
            # println(length(dataset_right))

            # If have child
            if (length(dataset_left) > 0) && (length(dataset_right) > 0)
                y = getCol(dataset, NCOLS)
                left_y = getCol(dataset_left, NCOLS)
                right_y = getCol(dataset_right, NCOLS)

                # Information gain
                curr_info_gain = information_gain(self, y, left_y, right_y)

                # print("> info_gain = ")
                # println(curr_info_gain)

                # If we found a better threshold
                if curr_info_gain > max_info_gain
                    best_split["feature_index"] = feature_index
                    best_split["threshold"] = threshold
                    best_split["dataset_left"] = dataset_left
                    best_split["dataset_right"] = dataset_right
                    best_split["info_gain"] = curr_info_gain
                    max_info_gain = curr_info_gain
                end
            end
        end

    end
    return best_split
end

# Split the current dataset into 2 left and right dataset
function split_left_right(dataset, feature_index, threshold)
    dataset_left = [row for row in dataset if row[feature_index] <= threshold]
    dataset_right = [row for row in dataset if row[feature_index] > threshold]
    return dataset_left, dataset_right
end

# Calculate Information Gain, use Entropy
function information_gain(self, parent, l_child, r_child)

    # print("parent: ")
    # print(parent)
    # print("l_child: ")
    # print(l_child)
    # print("r_child: ")
    # print(r_child)

    weight_l = length(l_child) / length(parent)
    weight_r = length(r_child) / length(parent)
    gain = entropy(self, parent) - (weight_l * entropy(self, l_child) + weight_r * entropy(self, r_child))

    # print("> (")
    # print(weight_l)
    # print(", ")
    # print(weight_r)
    # println(")")

    return gain
end

# Sub-function for entropy
function get_p_cls(y, cls)
    count = 0
    for e in y
        if e == cls
            count += 1
        end
    end
    return count
end

# Calculate Entropy
function entropy(self, y)
    # println("----------------------")
    class_labels = unique(y)
    entropy = 0

    # print("class_labels = ")
    # println(class_labels)

    for cls in class_labels
        p_cls = get_p_cls(y, cls) / length(y)
        entropy += -p_cls * log2(p_cls)

        # print("p_cls = ")
        # println(p_cls)
    end

    # print("entropy = ")
    # println(entropy)

    return entropy
end

# Just find the most common in Y
function calculate_leaf_value(Y)
    # dictionary with occurence
    occurences = Dict{eltype(Y), Int}()
    for val in Y
        if isa(val, Number) && isnan(val)
            continue
        end
        occurences[val] = get(occurences, val, 0) + 1
    end
    # pick the most common item
    result = nothing
    temp_max = 0
    for (key, value) in occurences
        if isnothing(result)
            result = key
            temp_max = value
        else
            if value > temp_max
                result = key
                temp_max = value
            end
        end
    end
    return result
end

# Predict a dataset
function predict(self, X)
    preditions = [makePrediction(self, x, self.root) for x in X]
    return preditions
end

# Sub-function of predict, just to predict 1 row of data
function makePrediction(self, x, tree)
    if !(isnothing(tree.value))
        return tree.value
    end
    feature_val = x[tree.feature_index]
    if feature_val <= tree.threshold
        return makePrediction(self, x, tree.left)
    else
        return makePrediction(self, x, tree.right)
    end
end

# Calculate accuracy
function calAccuracy(Y_test, Y_pred)
    n = length(Y_test)
    match_count = 0
    for i = 1:n
        if Y_test[i] == Y_pred[i]
            match_count += 1
        end
    end
    return match_count / n
end

# =========================== Sub Functions ==============================
# Return a rows-shuffled dataset
function shuffleData(dataset)
    return dataset[shuffle(axes(dataset, 1)), :]
end

# Dataframe to Julia vector array
function dfToVectorArr(data)
    data_array = []
    n = trunc(Int, length(data) / NCOLS)
    for i = 1:n
        push!(data_array, [])
        for j = 1:NCOLS
            push!(data_array[i], data[i, j])
        end
    end
    return data_array
end

# Concatenate 2 matrix horizontally
function concatenate(X, Y)
    result = []
    for i = 1:length(X)
        push!(result, X[i])
        push!(result[i], Y[i][1])
    end
    return result
end

# Just to print the matrix
function lsPrint(data)
    for row in data
        println(row)
    end
end

# Just to slice dataset in to X and Y
function lsSliceLast(data)
    X, Y = [], []
    for row in data
        push!(X, row[1:NCOLS-1])
        push!(Y, [row[end]])
    end
    return X, Y
end

# Just to get a specific column
function getCol(dataset, index)
    result = [row[index] for row in dataset]
    return result
end

# Return an array with unique items
function unique(ls)
    result = []
    for e in ls
        if !(e in result)
            push!(result, e)
        end
    end
    sort!(result)
    return result
end

# Transpose a matrix
function transpose(m)
    n_rows = length(m)
    n_cols = length(m[1])
    return [[m[i][j] for i = 1:n_rows] for j = 1:n_cols]
end

# Just to print a line
function printBreakLine()
    println("=========================================================================")
end

# Print the decision tree
function printDecisionTree(self, tree = nothing, indent = "   ")
    if isnothing(tree)
        tree = self.root
    end
    if !(isnothing(tree.value))
        print(tree.value)
    else
        print(ATTRIBUTES[tree.feature_index])
        print(" <= ")
        println(tree.threshold)
        print(indent)
        print("Left Node: ")
        printDecisionTree(self, tree.left, indent * indent)
        println("")
        print(indent)
        print("Right Node: ")
        printDecisionTree(self, tree.right, indent * "   ")
    end
end



# Main Program

# =========================== Read Dataset ================================
print("> Reading data")
data = DataFrame(CSV.File("iris.csv"; header = true))[:,2:end]
println(" > Completed")
data = shuffleData(data)
# println(data)
data = Matrix(data)
data = dfToVectorArr(data)
# ls_print(data)


# =================== Split data into train and test ======================
data_train, data_test = splitTrainTest(data, 2/3)

X_train, Y_train = lsSliceLast(data_train)
X_test, Y_test = lsSliceLast(data_test)


# ========================= Build Decision Tree ============================
classifier = DecisionTree(nothing, 3, 3)
startBuildDecisionTree(classifier, X_train, Y_train)

printBreakLine()
printDecisionTree(classifier)
println("")

# =================== Predict and calculate accuracy ======================
Y_pred = transpose(predict(classifier, X_test))[1]
Y_test = transpose(Y_test)[1]
printBreakLine()
print("Accuracy: ")
println(calAccuracy(Y_test, Y_pred))
printBreakLine()
