bids = {}

while True:
    name = input("Enter your name: ")
    bid = int(input("Enter your bid: "))

    bids[name] = bid

    again = input("Is there another bidder? (yes/no): ")

    if again.lower() == "no":
        break

winner = max(bids, key=bids.get)

print("\nWINNER:", winner)
print("WINNING BID:", bids[winner])