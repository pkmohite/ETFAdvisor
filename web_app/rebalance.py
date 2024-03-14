from home import fetch_current_price

def rebalance_portfolio(portfolio, selected_bucket, new_allocations):
    bucket = next(b for b in portfolio['buckets'] if b['name'] == selected_bucket)

    # Emulate selling all ETFs in the bucket
    total_value = sum(fetch_current_price(etf['ticker']) * etf['shares'] for etf in bucket['etfs'])
    total_value += portfolio['cash']

    # Emulate buying ETFs based on the new allocations
    for etf in bucket['etfs']:
        ticker = etf['ticker']
        new_allocation = new_allocations[ticker] / 100
        target_amount = total_value * new_allocation
        current_price = fetch_current_price(ticker)
        if current_price is not None:
            new_shares = int(target_amount / current_price)  # Round down to the nearest integer
            etf['shares'] = new_shares
            etf['allocation'] = new_allocations[ticker]

    # Update the cash amount after rebalancing
    portfolio['cash'] = total_value - sum(fetch_current_price(etf['ticker']) * etf['shares'] for etf in bucket['etfs'])

    return portfolio