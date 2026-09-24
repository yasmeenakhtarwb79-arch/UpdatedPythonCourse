import random

# Asli Blackjack Deck: Ace (11), King/Queen/Jack (10) aur baqi numbers
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

def calculate_score(cards_list):
    """Cards ka total score calculate karne ka function"""
    # Agar shuru mein hi Ace (11) aur 10 aa jaye toh yeh Blackjack (0) hai
    if sum(cards_list) == 21 and len(cards_list) == 2:
        return 0
    
    # 🃏 ACE RULE: Agar score 21 se upar jaye aur hand mein 11 (Ace) ho, toh use 1 bana do
    while sum(cards_list) > 21 and 11 in cards_list:
        cards_list.remove(11)
        cards_list.append(1)
        
    return sum(cards_list)

def start_game():
    print("\n=============================================")
    print("   🃏 WELCOME TO REAL TERMINAL BLACKJACK 🃏  ")
    print("=============================================")

    # Player aur Dealer ko 2-2 random cards dena
    player_cards = [random.choice(deck), random.choice(deck)]
    dealer_cards = [random.choice(deck), random.choice(deck)]
    
    game_over = False

    # 🔄 Player ki baari (Loop Engine)
    while not game_over:
        player_score = calculate_score(player_cards)
        dealer_score = calculate_score(dealer_cards)
        
        print(f"\nAapke Cards: {player_cards} | Total Score: {player_score}")
        print(f"Dealer ka Pehla Card: [{dealer_cards[0]}]")

        # Agar kisi ka Blackjack ho jaye ya player 21 se upar nikal jaye
        if player_score == 0 or dealer_score == 0 or player_score > 21:
            game_over = True
        else:
            # User se choice lena
            user_choice = input("\nNaya card lene ke liye 'y' dabayein, rukne ke liye 'n' dabayein: ").lower()
            if user_choice == 'y':
                player_cards.append(random.choice(deck))
            elif user_choice == 'n':
                game_over = True
            else:
                print("Ghalat button! Sirf 'y' ya 'n' dabayein.")

    # 🔄 Dealer (Computer) ki baari: Jab tak uska score 17 se kam ho, woh card uthata rahega
    player_score = calculate_score(player_cards)
    dealer_score = calculate_score(dealer_cards)
    
    while dealer_score != 0 and dealer_score < 17 and player_score <= 21:
        dealer_cards.append(random.choice(deck))
        dealer_score = calculate_score(dealer_cards)

    # 📊 Final Result Dashboard
    print("\n=============================================")
    print(f"➔ Aapka Final Hand: {player_cards} | Score: {player_score if player_score != 0 else 21}")
    print(f"➔ Dealer ka Final Hand: {dealer_cards} | Score: {dealer_score if dealer_score != 0 else 21}")
    print("=============================================\n")

    # 🏆 Winner Decision Logic
    if player_score > 21:
        print("❌ Aap 21 se upar nikal gaye! DEALER JEET GAYE!")
    elif dealer_score > 21:
        print("🎉 Dealer 21 se upar nikal gaya! AAP JEET GAYE!")
    elif player_score == dealer_score:
        print("🤝 Match Draw ho gaya (Push)!")
    elif player_score == 0:
        print("🏆 BLACKJACK! Aap pehli hi baari mein JEET GAYE!")
    elif dealer_score == 0:
        print("❌ Dealer ko Blackjack mil gaya! AAP HAAR GAYE!")
    elif player_score > dealer_score:
        print("🎉 Aapka score dealer se zyada hai! AAP JEET GAYE!")
    else:
        print("❌ Dealer ka score zyada hai! AAP HAAR GAYE!")

# Game run karne ka trigger
start_game()
