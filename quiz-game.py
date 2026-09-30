import random

def run_advanced_quiz(high_score):
    # --- 1️⃣ SECTION 1: World Geography & International Sports ---
    section_1 = [
        {
            "topic": "World Geography",
            "question": "Which is the largest and deepest ocean on Earth?",
            "options": ["A) Indian Ocean", "B) Atlantic Ocean", "C) Pacific Ocean", "D) Arctic Ocean"],
            "correct": "c",
            "hint": "Its name means 'peaceful', separating Asia from the Americas."
        },
        {
            "topic": "International Sports",
            "question": "How many times has Pakistan won the Hockey World Cup?",
            "options": ["A) 2 Times", "B) 3 Times", "C) 4 Times", "D) 5 Times"],
            "correct": "c",
            "hint": "Pakistan holds the world record for the most World Cup titles."
        }
    ]

    # --- 2️⃣ SECTION 2: General Knowledge & Basic Science ---
    section_2 = [
        {
            "topic": "General Knowledge",
            "question": "Which of the following is the national bird of Pakistan?",
            "options": ["A) Shaheen", "B) Parrot", "C) Chakor", "D) Pigeon"],
            "correct": "c",
            "hint": "It is a beautiful mountain bird known for its legendary love for the moon."
        },
        {
            "topic": "Basic Science",
            "question": "What is the chemical formula of water?",
            "options": ["A) CO2", "B) H2O", "C) O2", "D) NaCl"],
            "correct": "b",
            "hint": "It consists of two hydrogen atoms and one oxygen atom."
        },
        {
            "topic": "Basic Science",
            "question": "Which gas do plants absorb from the atmosphere to make their food?",
            "options": ["A) Oxygen", "B) Nitrogen", "C) Hydrogen", "D) Carbon Dioxide"],
            "correct": "d",
            "hint": "This is the gas that humans exhale during breathing."
        }
    ]

    # --- 3️⃣ SECTION 3: Punjabi Culture & Folk History ---
    section_3 = [
        {
            "topic": "Punjab Culture",
            "question": "Which is the most famous and energetic traditional dance of Punjab?",
            "options": ["A) Jhumar", "B) Bhangra", "C) Luddi", "D) Sammi"],
            "correct": "b",
            "hint": "This dance is performed to the beat of the dhol, especially during Vaisakhi festivals."
        },
        {
            "topic": "Punjab History",
            "question": "Who wrote the famous Punjabi romantic folk tale 'Heer Ranjha'?",
            "options": ["A) Bulleh Shah", "B) Mian Muhammad Baksh", "C) Waris Shah", "D) Sultan Bahu"],
            "correct": "ج",  # Maps to 'c' in execution
            "correct": "c",
            "hint": "This legendary poet is often referred to as the Shakespeare of the Punjabi language."
        },
        {
            "topic": "Traditional Sports",
            "question": "Which is the most popular traditional sport played in the villages of Punjab?",
            "options": ["A) Kabaddi", "B) Cricket", "C) Football", "D) Hockey"],
            "correct": "a",
            "hint": "In this sport, a player constantly repeats a specific word while entering the opponent's court."
        }
    ]

    # Randomizing questions *inside* each section to keep it dynamic
    random.shuffle(section_1)
    random.shuffle(section_2)
    random.shuffle(section_3)

    # Combine them in a fixed sequence: Section 1 -> Section 2 -> Section 3
    all_questions = section_1 + section_2 + section_3

    score = 0
    lifeline_available = True
    total_questions = len(all_questions)

    print("====================================================")
    print("   🔥 WELCOME TO THE ULTIMATE ADVANCED QUIZ 🔥    ")
    print("====================================================")
    print(f"📈 Current High Score to Beat: {high_score}")
    print("⚠️ RULES:")
    print("1. Correct Answer = +10 Points | Wrong Answer = -5 Points")
    print("2. Using a Hint gives only +5 Points on correct answer.")
    print("3. Type 'hint' for a clue.")
    print("4. Type '50' to trigger 50:50 Lifeline (Can be used ONCE).")
    print("====================================================\n")

    for i, q in enumerate(all_questions, 1):
        print(f"\n📋 [DASHBOARD] Question: {i}/{total_questions} | Score: {score} | Topic: {q['topic']}")
        print(f"❓ {q['question']}")
        
        for option in q['options']:
            print(option)
            
        used_hint = False
        
        while True:
            user_input = input("\nYour Answer (A/B/C/D): ").strip().lower()
                
            if user_input == 'hint':
                print(f"💡 Hint: {q['hint']}")
                used_hint = True
                continue
                
            if user_input == '50':
                if lifeline_available:
                    lifeline_available = False
                    print("\n⚡ 50:50 Lifeline Activated! Two wrong options removed:")
                    
                    correct_letter = q['correct']
                    filtered_opts = [opt for opt in q['options'] if opt.lower().startswith(correct_letter)]
                    wrongs = [opt for opt in q['options'] if not opt.lower().startswith(correct_letter)]
                    filtered_opts.append(random.choice(wrongs))
                    filtered_opts.sort()
                    
                    for opt in filtered_opts:
                        print(f"👉 {opt}")
                    continue
                else:
                    print("⚠️ Lifeline already used up!")
                    continue
            
            if user_input in ['a', 'b', 'c', 'd']:
                if user_input == q['correct']:
                    reward = 5 if used_hint else 10
                    print(f"✅ Correct! +{reward} Points.")
                    score += reward
                else:
                    print(f"❌ Wrong! The correct answer was ({q['correct'].upper()}). -5 Points.")
                    score -= 5
                break
            else:
                print("⚠️ Invalid choice. Enter A, B, C, D, 'hint', or '50'.")

    print("\n====================================================")
    print("             🏁 GAME OVER RESULTS 🏁                ")
    print("====================================================")
    print(f"🏆 Your Total Points: {score}")
    return score

if __name__ == "__main__":
    global_high_score = 0
    while True:
        final_score = run_advanced_quiz(global_high_score)
        if final_score > global_high_score:
            global_high_score = final_score
            print("👑 NEW HIGH SCORE ESTABLISHED!")
            
        play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            print("\n👋 Goodbye! Thanks for playing the Quiz Game. 🎉")
            break
