# Financial-models
Repository for snipits of python code on finance theories and models as part and beyond the CFA Level I material.

# Sharpe Optimization 
A commonly used measure in finance to evaluate the performance of an 
investment relative to its risk. Also used to measure the performance of investment managers.

    Risk-Adjusted Returns: The Sharpe Ratio provides a way to understand an investment's return relative 
    to its risk. Higher returns might be less impressive if they come with much higher risk. 
    The Sharpe Ratio helps to put returns into perspective by considering the volatility or risk associated with those returns.

    Comparing Investments: It allows investors to compare different investments on a level playing field. 
    Two investments could have the same return, but if one has lower risk, 
    it will have a higher Sharpe Ratio, indicating it may be the better choice.

    Optimizing Portfolios: For portfolio management, the Sharpe Ratio is crucial in optimization. 
    It helps in constructing a portfolio that offers the highest possible returns for a given 
    level of risk or the lowest risk for a given level of expected returns.

    Sharpe Ratio is defined as (Rp-Rf)/σp 
    where Rp is the return of the portfolio, Rf is the risk free rate, and σp is the standard deviation of the portfolio's excess return.
    Excess return defined as returns earned by an investment above a benchmark return, typically the S&P500 or Risk free rate/10 Yr US Treasury.
    
# Risk Parity Strategy
Risk parity strategies became particularly popular after the 2008 financial crisis, as they aim to address 
some of the shortcomings of traditional asset allocation models, like the 60/40 stock/bond split, which can
be heavily influenced by the performance of a single asset class. However, it's important to note that 
while risk parity aims for a more stable performance, it is not without its own risks and complexities, 
especially regarding the use of leverage and the assumption that historical correlations and volatilities will continue into the future.

Equalizing Risk Contribution: In a risk parity portfolio, assets are weighted not by their market value but by their contribution
to the portfolio's overall risk. The aim is to ensure that each asset or asset class contributes equally to the portfolio's total risk.

Focus on Volatility and Correlation: Risk parity strategies typically use metrics like volatility and correlation to assess the risk of assets. 
The idea is to balance the portfolio in such a way that assets with higher volatility have a lower weight, and assets with lower volatility have a higher weight.
The primary objective of risk parity is not necessarily to maximize returns, but to achieve a more stable, 
risk-adjusted performance over time. By doing so, the strategy aims to avoid the extremes of market cycles and provide smoother investment returns.
Risk parity portfolios are usually rebalanced regularly to maintain an equal risk contribution from each asset class. 
This rebalancing can help the portfolio adapt to changing market conditions and maintain its risk-balanced stance.
Risk parity portfolios often include a broad range of asset classes, such as stocks, bonds, commodities, and real estate. 
This diversification is based on the understanding that different asset classes react differently to various economic conditions.
