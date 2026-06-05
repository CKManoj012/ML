from agents.coordinator import coordinator_agent


ticker = input("Ticker: ")

result = coordinator_agent(ticker)

print(result)