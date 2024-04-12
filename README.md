# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Solution

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> In AMMs like Uniswap, slippage refers to the difference between the expected price of a trade and the actual executed price. This difference occurs because when traders trade many times, the market price will change each time. As a result, larger trades can cause the price to move against the trader due to the depletion or increase of liquidity in the pool.
Uniswap V2 addresses the slippage issue through the introduction of the x * y = k formula, where x and y represent the quantities of two tokens in a liquidity pool, and k is a constant value. This formula is also known as the constant product invariant.

>The below function implements the constant-product method V2 address uses: 

>def constant_product(x_init, y_init, x_in, k):
    /*Args:
        x (float): Quantity of token X in the liquidity pool.
        y (float): Quantity of token Y in the liquidity pool.
        k (float): x_init * y_init.
    
    Returns:
        float: The new value of y.*/

    solve k = x_init * y_init = (x_init + x_in) * (y_init - y_out) 
    return y_out

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> By imposing a minimum liquidity requirement, the protocol can avoid "dust" transactions, which are extremely small liquidity positions that could clutter the liquidity pool without providing significant benefits. These dust transactions could potentially lead to inefficiencies in the system, such as increased gas costs for processing and maintaining these tiny positions.


## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> When depositing tokens into the liquidity pool, the specific formula ensures that the new liquidity provided conforms to the constant product invariant. By using this formula, the protocol maintains the integrity and efficiency of the liquidity pool by:

Preserving Price Equilibrium: The constant product formula ensures that the ratio of token balances in the pool remains unchanged, preserving the price equilibrium between the tokens. This helps prevent price manipulation and maintains fair and accurate pricing for traders.

Preventing Arbitrary Changes: Without adhering to the constant product invariant, arbitrary changes to the token balances could disrupt the pricing mechanism of the liquidity pool, leading to inaccuracies and potential exploitation by traders.

Promoting Stability and Efficiency: By enforcing the constant product invariant during liquidity provision, the protocol promotes stability and efficiency within the Uniswap ecosystem. Liquidity providers can be confident that their contributions are aligned with the protocol's pricing mechanism, enhancing overall market integrity.

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> A sandwich attack is a type of front-running attack commonly seen in decentralized finance platforms like DEXs such as Uniswap. In a sandwich attack, an attacker exploits the predictable behavior of a liquidity pool's price movement to profit at the expense of other traders. The trader may experience increased slippage, leading to worse execution prices for their trades. In extreme cases, the trader could suffer substantial financial losses if the price manipulation caused by the sandwich attack is severe.

