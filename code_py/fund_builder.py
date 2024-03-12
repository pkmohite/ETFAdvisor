import pandas as pd
import numpy as np

def create_portfolio():
    portfolio = {}

    # Assets in portfolio
    portfolio['assets'] = {}
    num_assets = int(input("Enter the number of assets in the portfolio: "))
    for i in range(num_assets):
        ticker = input(f"Enter the ticker for asset {i+1}: ")
        quantity = int(input(f"Enter the quantity for asset {i+1}: "))
        portfolio['assets'][ticker] = quantity

    # Cash in portfolio
    portfolio['cash'] = {}
    num_currencies = int(input("Enter the number of different currencies in the portfolio: "))
    for i in range(num_currencies):
        currency = input(f"Enter the currency type for cash {i+1}: ")
        amount = float(input(f"Enter the amount for cash {i+1}: "))
        portfolio['cash'][currency] = amount

    return portfolio

portfolio = create_portfolio()

