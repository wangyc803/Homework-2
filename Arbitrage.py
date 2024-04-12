liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

path = []
tokens = ["tokenA", "tokenB", "tokenC", "tokenD", "tokenE"]

def trade(liquidity, amount, X1, X2):
    amount_X1, amount_X2 = liquidity[X1][X2]
    #print(amount, " ")
    amount_aX2 = amount_X1 * amount_X2 / (amount_X1 + amount)
    liquidity[X1][X2] = (amount_X1 + amount, amount_aX2)
    liquidity[X2][X1] = (amount_aX2, amount_X1 + amount)
    amount = amount_X2 - amount_aX2
    #print(amount, ",")
    return amount

def checkArbitrage(liquidity, tokens, base_Token):
    for i in range(len(tokens) - 1):
        if i == base_Token:
            continue
        for j in range(len(tokens) - 1):
            if j == i or j == base_Token:
                continue
            for k in range(len(tokens) - 1):
                if k == i or k == j or k == base_Token:
                    continue
                R0, R1 = liquidity[base_Token][i]
                R_1, R2 = liquidity[i][j]
                R_2, R3 = liquidity[j][k]
                R_3, R_0 = liquidity[k][base_Token]
                M0 = R0 * R_1 / (R1 * 0.997+ R_1)
                X2 = 0.997 * R1 * R2 / (R1 * 0.997 + R_1)
                M_2 = R2 * R3 / (R3 * 0.997 + R_3)
                M_0 = 0.997 * R3 * R_0 / (R3 * 0.997 + R_3)
                E_before = M0 * M_2 / (M_2 * 0.997 + X2)
                E_after = 0.997 * X2 * M_0 / (M_2 * 0.997 + X2)
                amount = (E_before * E_after * 0.997)**0.5 - E_before
                if E_after > E_before and amount > 1:
                    return (i, j, k, amount)
        if i == base_Token:
            continue
        for j in range(len(tokens) - 1):
            if j == i or j == base_Token:
                continue
            R0, R1 = liquidity[base_Token][i]
            R_1, R2 = liquidity[i][j]
            R_2, R_0 = liquidity[j][base_Token]
            M0 = R0 * R_1 / (R1 * 0.997 + R_1)
            X2 = 0.997 * R1 * R2 / (R1 * 0.997 + R_1)
            E_before = M0 * R_2 / (X2 + R_2 * 0.997)
            E_after = 0.997 * X2 * R_0 / (X2 + R_2 * 0.997)
            amount = (E_before * E_after * 0.997)**0.5 - E_before
            if E_after > E_before and amount > 1:
                return (i, j, amount)
    return (-1, -1)

def arbitrage(liquidity, amount, base_Token, X1, X2, X3):
    amount = trade(liquidity, amount, base_Token, X1)
    amount = trade(liquidity, amount, X1, X2)
    if X3 == -1:
        amount = trade(liquidity, amount, X2, base_Token)
        return amount
    amount = trade(liquidity, amount, X2, X3)
    amount = trade(liquidity, amount, X3, base_Token)
    #print(amount, "haha")
    return amount

def Arbitrage(graph, start):
    # Initialize liquidity pool
    tokens = ["tokenA", "tokenB", "tokenC", "tokenD", "tokenE"]
    initial_token = 5       
    liquidity = [[() for _ in range(len(tokens))] for _ in range(len(tokens))]
    base_Token = tokens.index(start)
    # Fill the 2D array with the tuples from the liquidity dictionary
    for token1, token2, (a_1, a_2) in graph:
        liquidity[tokens.index(token1)][tokens.index(token2)] = (a_1, a_2)
        liquidity[tokens.index(token2)][tokens.index(token1)] = (a_2, a_1)
    # Relax edges repeatedly
    while (initial_token < 20):
        result = checkArbitrage(liquidity, tokens, base_Token)
        if result == (-1, -1):
            return initial_token, path
        if len(result) == 4:
            X1, X2, X3, amount = result
            path.append([X1, X2, X3, amount]) 
            initial_token -= amount
            amount = arbitrage(liquidity, amount, base_Token, X1, X2, X3)
            initial_token += amount
        if len(result) == 3:
            X1, X2, amount = result
            path.append([X1, X2, amount]) 
            amount = min(amount, initial_token)
            initial_token -= amount
            amount = arbitrage(liquidity, amount, base_Token, X1, X2, -1)
            initial_token += amount
        #print(initial_token, "h")
    return initial_token, path
    

# Construct graph
graph = [(token1, token2, liquidity[(token1, token2)]) for (token1, token2) in liquidity]
# Find the desired path starting from tokenB
final_balance, path = Arbitrage(graph, "tokenB")
for i in range(len(path)):
    print("path: tokenB ->", end = " ")
    for j in range(len(path[i]) - 1):
        print(tokens[path[i][j]], end = " ")
        print("->", end = " ")
print(f"tokenB, tokenB balance = {final_balance}")