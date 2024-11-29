#!/bin/bash

# Source the .env file to load the API key
source .env

# Define the stock symbol
STOCK_SYMBOL=""


get_price() {
    # Fetch the current price from the API
    curl -s -H "X-Finnhub-Token: $FINNHUB_API_KEY" "https://finnhub.io/api/v1/quote?symbol=$symbol" | jq -r '.c'
}

get_data() {
    # Fetch the financial data from the API
    curl -s -H "X-Finnhub-Token: $FINNHUB_API_KEY" "https://finnhub.io/api/v1/stock/metric?metric=all&symbol=$symbol"
}


print_data() {
    local symbol="$1"
    local data=$(get_data "$symbol")
    local price=$(get_price "$symbol")

    # Extract the relevant metrics using jq
    market_cap=$(echo "$data" | jq -r '.metric.marketCapitalization')
    pe_ratio=$(echo "$data" | jq -r '.metric.peAnnual')
    dividend_yield=$(echo "$data" | jq -r '.metric.currentDividendYieldTTM')
    ebitda=$(echo "$data" | jq -r '.metric.ebitdPerShareAnnual')
    revenue=$(echo "$data" | jq -r '.metric.revenuePerShareAnnual')
    net_income=$(echo "$data" | jq -r '.metric.netIncomeEmployeeAnnual')
    debt_to_equity=$(echo "$data" | jq -r '.metric."totalDebt/totalEquityAnnual"')
    profit_margin=$(echo "$data" | jq -r '.metric.netProfitMarginAnnual')

    # Print the data in a table format
    echo "$(echo "$symbol" | tr '[:lower:]' '[:upper:]'): $price"
    echo "----------------------------"
    echo "Market Capitalization          | $market_cap"
    echo "PE Ratio                       | $pe_ratio"
    echo "Dividend Yield YTD             | $dividend_yield"
    echo "EBITDA Annual                  | $ebitda"
    echo "Revenue Per Share Annual       | $revenue"
    echo "Net Income Per Employee Annual | $net_income"
    echo "Debt to Equity Annual          | $debt_to_equity"
    echo "Net Profit Margin Annual       | $profit_margin"
}

# Continuously listen for user input
while true; do
    read -p "Enter a ticker symbol (or 'exit' to quit): " symbol
    if [[ "$symbol" == "exit" ]]; then
        break
    fi
    print_data "$symbol"
    echo
done