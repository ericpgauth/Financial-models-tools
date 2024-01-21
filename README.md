# Financial-models
Repository for snipits of python code on finance theories and models in order to develop both finance and coding skills. Incorporating study notes based on CFA Level I material.
Models, charts, and other content are not for applied use. All products herein are to be considered incomplete, unaudited works in progress. 
# Formulas
WIP collection of CFA L1 formulas on:
        Quantitative Methods 1/19/24
        Economics 1/19/24
        Financial Statement Analysis (TBC)
        Corporate Issuers (TBC)
        Equity (TBC)
        Portfolio Management (TBC)
        Fixed Income (TBC)
        Derivatives (TBC)
        Alernative Investments (TBC)
        
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
    
# Portfolio Value at Risk (VAR)
Value at Risk (VaR) is a statistical measure used in finance to estimate the potential loss that an investment portfolio, trading position, or financial asset may experience over a specific time horizon at a certain level of confidence. In essence, VaR provides an estimate of the worst-case loss under normal market conditions. Here's an explanation of how VaR for a portfolio based on historical data works:

    Time Horizon: VaR calculations are typically done for a specific time horizon, such as one day, one week, or one month. The time horizon represents the period over which the potential loss is estimated.

    Confidence Level: The confidence level is a critical parameter in VaR calculations. It represents the level of confidence that the calculated VaR value will not be exceeded. For example, if you calculate VaR at a 95% confidence level, you are saying that you are 95% confident that the portfolio's loss will not exceed the VaR estimate over the chosen time horizon.

    Historical Data: To calculate VaR, historical data of the portfolio's returns (or changes in value) are needed. These returns are usually expressed as percentages. The historical data provide a basis for assessing how the portfolio has performed in the past.

    Sorting Returns: The historical returns are sorted in ascending order from worst to best performance. This sorted list allows you to determine the loss levels at various percentiles. For example, the loss at the 5th percentile represents the VaR at a 95% confidence level.

    VaR Calculation: The VaR calculation involves finding the return value at the specified confidence level. This value is often referred to as the "critical value" or "cut-off point." It represents the maximum potential loss at the chosen confidence level.

If you calculate VaR using historical data, you simply identify the return at the appropriate percentile. This becomes your VaR value.

        For example, if you calculate VaR at a 95% confidence level and the return at the 5th percentile is -2%, it means you are 95% confident that the portfolio's daily loss will not exceed 2% over the chosen time horizon.

    Interpretation: Once you have the VaR value, it is expressed as a percentage of the portfolio's initial value. This percentage represents the potential loss. In the example above, a 2% VaR at a 95% confidence level means that, under normal market conditions, you can expect a maximum loss of 2% in the portfolio over the specified time frame with a 95% confidence.

    Risk Management: VaR is a valuable tool for risk management. It helps investors and financial institutions assess and manage their exposure to potential losses. It provides a clear picture of the downside risk associated with a portfolio, allowing for better decision-making regarding risk tolerance, hedging strategies, and asset allocation.

It's important to note that VaR has its limitations, especially when dealing with extreme events or non-normal market conditions. It assumes that past market behavior is a reliable indicator of future performance, which may not always be the case. As a result, VaR is often used in conjunction with other risk measures and stress tests to provide a more comprehensive view of portfolio risk.
