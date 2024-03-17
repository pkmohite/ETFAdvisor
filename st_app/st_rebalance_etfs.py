# file: st_app/st_rebalance_etfs.py
from st_home import fetch_current_price, load_portfolio, save_portfolio, calculate_total_value

#define rebalance_ETFs function
def rebalance_etfs(portfolio, bucket_name, allocation):

    # Calculate the total value of the portfolio
    total_value = calculate_total_value(portfolio)

    # Find the bucket that needs to be rebalanced
    bucket_name = next(b for b in portfolio['buckets'] if b['name'] == bucket_name)

    # Determine bucket value by total_value * allocation
    bucket_value = total_value * bucket_name['allocation'] / 100

    # Emulate buying ETFs based on the new allocations
    for etf in bucket_name['etfs']:
        ticker = etf['ticker']
        new_allocation = allocation[ticker] / 100
        target_amount = bucket_value * new_allocation
        current_price = fetch_current_price(ticker)
        if current_price is not None:
            new_shares = int(target_amount / current_price)  # Round down to the nearest integer
            etf['shares'] = new_shares
            etf['allocation'] = allocation[ticker]

    # Calculate the total value of the ETFs in the portfolio
    total_ETF_value = 0
    for bucket in portfolio['buckets']:
        for etf in bucket['etfs']:
            total_ETF_value += fetch_current_price(etf['ticker']) * etf['shares']

    # Update the cash amount after rebalancing
    portfolio['cash'] = total_value - total_ETF_value

    return portfolio


def rebalance_etfs_old(portfolio, bucket_name, allocation):
    
    bucket = next(b for b in portfolio['buckets'] if b['name'] == bucket_name)

    # Emulate selling all ETFs in the bucket
    total_value = sum(fetch_current_price(etf['ticker']) * etf['shares'] for etf in bucket['etfs'])
    total_value += portfolio['cash']

    # Emulate buying ETFs based on the new allocations
    for etf in bucket['etfs']:
        ticker = etf['ticker']
        new_allocation = allocation[ticker] / 100
        target_amount = total_value * new_allocation
        current_price = fetch_current_price(ticker)
        if current_price is not None:
            new_shares = int(target_amount / current_price)  # Round down to the nearest integer
            etf['shares'] = new_shares
            etf['allocation'] = allocation[ticker]

    # Update the cash amount after rebalancing
    portfolio['cash'] = total_value - sum(fetch_current_price(etf['ticker']) * etf['shares'] for etf in bucket['etfs'])
    
    return portfolio