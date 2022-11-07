sol = {"A": [[]], "B1": [[]], "B2": [[]], "X":[[]]}
sol["A"] = [[1,2],[3]]
sol["B1"] = [[4],[5,6]]
sol["B2"] = [[7,8],[9]]
sol["X"] = [[10,11],[12]]
solution = sol["A"] + sol["B1"] + sol["B2"] + sol["X"]
print(solution)