import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Ultimate Quiz Game API")

# یہ کوئز کا پورا ڈیٹا (Questions Base) ہے جو آپ کے کوڈ سے لیا گیا ہے
QUIZ_DATA = {
    "section_1": [
        {
            "id": 1,
            "topic": "World Geography",
            "question": "Which is the largest and deepest ocean on Earth?",
            "options": ["A) Indian Ocean", "B) Atlantic Ocean", "C) Pacific Ocean", "D) Arctic Ocean"],
            "correct": "c",
            "hint": "Its name means 'peaceful', separating Asia from the Americas."
        },
        {
            "id": 2,
            "topic": "International Sports",
            "question": "How many times has Pakistan won the Hockey World Cup?",
            "options": ["A) 2 Times", "B) 3 Times", "C) 4 Times", "D) 5 Times"],
            "correct": "c",
            "hint": "Pakistan holds the world record for the most World Cup titles."
        }
    ],
    "section_2": [
        {
            "id": 3,
            "topic": "General Knowledge",
            "question": "Which of the following is the national bird of Pakistan?",
            "options": ["A) Shaheen", "B) Parrot", "C) Chakor", "D) Pigeon"],
            "correct": "c",
            "hint": "It is a beautiful mountain bird known for its legendary love for the moon."
        },
        {
            "id": 4,
            "topic": "Basic Science",
            "question": "What is the chemical formula of water?",
            "options": ["A) CO2", "B) H2O", "C) O2", "D) NaCl"],
            "correct": "b",
            "hint": "It consists of two hydrogen atoms and one oxygen atom."
        },
        {
            "id": 5,
            "topic": "Basic Science",
            "question": "Which gas do plants absorb from the atmosphere to make their food?",
            "options": ["A) Oxygen", "B) Nitrogen", "C) Hydrogen", "D) Carbon Dioxide"],
            "correct": "d",
            "hint": "This is the gas that humans exhale during breathing."
        }
    ],
    "section_3": [
        {
            "id": 6,
            "topic": "Punjab Culture",
            "question": "Which is the most famous and energetic traditional dance of Punjab?",
            "options": ["A) Jhumar", "B) Bhangra", "C) Luddi", "D) Sammi"],
            "correct": "b",
            "hint": "This dance is performed to the beat of the dhol, especially during Vaisakhi festivals."
        },
        {
            "id": 7,
            "topic": "Punjab History",
            "question": "Who wrote the famous Punjabi romantic folk tale 'Heer Ranjha'?",
            "options": ["A) Bulleh Shah", "B) Mian Muhammad Baksh", "C) Waris Shah", "D) Sultan Bahu"],
            "correct": "c",
            "hint": "This legendary poet is often referred to as the Shakespeare of the Punjabi language."
        },
        {
            "id": 8,
            "topic": "Traditional Sports",
            "question": "Which is the most popular traditional sport played in the villages of Punjab?",
            "options": ["A) Kabaddi", "B) Cricket", "C) Football", "D) Hockey"],
            "correct": "a",
            "hint": "In this sport, a player constantly repeats a specific word while entering the opponent's court."
        }
    ]
}

# یوزر کا جواب چیک کرنے کے لیے ایک ڈیٹا فارمیٹ (Model)
class AnswerSubmission(BaseModel):
    question_id: int
    user_answer: str
    used_hint: bool = False

# 🛑 ENDPOINT 1: تمام سوالات کو ترتیب اور شفل (Shuffle) کر کے حاصل کرنے کا لنک
@app.get("/quiz/questions")
def get_quiz_questions():
    s1 = list(QUIZ_DATA["section_1"])
    s2 = list(QUIZ_DATA["section_2"])
    s3 = list(QUIZ_DATA["section_3"])
    
    # آپ کے کوڈ کے مطابق ہر سیکشن کے اندر شفلنگ کرنا
    random.shuffle(s1)
    random.shuffle(s2)
    random.shuffle(s3)
    
    all_questions = s1 + s2 + s3
    
    # سیکیورٹی کے لیے فرنٹ اینڈ کو جواب (correct option) نہیں بھیجیں گے
    questions_for_user = []
    for q in all_questions:
        questions_for_user.append({
            "id": q["id"],
            "topic": q["topic"],
            "question": q["question"],
            "options": q["options"],
            "hint": q["hint"]
        })
        
    return {"total_questions": len(questions_for_user), "questions": questions_for_user}

# 🛑 ENDPOINT 2: یوزر کے جواب کو چیک کر کے نمبر (Points) دینے کا لنک
@app.post("/quiz/submit-answer")
def submit_answer(submission: AnswerSubmission):
    # تمام سیکشنز میں سے وہ سوال ڈھونڈنا جس کا یوزر نے جواب دیا ہے
    all_questions = QUIZ_DATA["section_1"] + QUIZ_DATA["section_2"] + QUIZ_DATA["section_3"]
    target_question = next((q for q in all_questions if q["id"] == submission.question_id), None)
    
    if not target_question:
        raise HTTPException(status_code=404, detail="سوال نہیں ملا!")
        
    is_correct = submission.user_answer.strip().lower() == target_question["correct"]
    
    if is_correct:
        # اگر ہنٹ استعمال کی ہو تو 5 نمبر، ورنہ 10 نمبر
        points = 5 if submission.used_hint else 10
        return {
            "status": "correct",
            "message": f"✅ Correct Answer! You earned +{points} points.",
            "points": points,
            "correct_option": target_question["correct"]
        }
    else:
        return {
            "status": "wrong",
            "message": f"❌ Wrong Answer! -5 points.",
            "points": -5,
            "correct_option": target_question["correct"]
        }

# 🛑 ENDPOINT 3: 50:50 لائف لائن کو سنبھالنے کا لنک
@app.get("/quiz/lifeline-50/{question_id}")
def trigger_50_50(question_id: int):
    all_questions = QUIZ_DATA["section_1"] + QUIZ_DATA["section_2"] + QUIZ_DATA["section_3"]
    q = next((q for q in all_questions if q["id"] == question_id), None)
    
    if not q:
        raise HTTPException(status_code=404, detail="سوال نہیں ملا!")
        
    correct_letter = q['correct']
    filtered_opts = [opt for opt in q['options'] if opt.lower().startswith(correct_letter)]
    wrongs = [opt for opt in q['options'] if not opt.lower().startswith(correct_letter)]
    
    # ایک غلط آپشن رینڈم چننا
    filtered_opts.append(random.choice(wrongs))
    filtered_opts.sort()
    
    return {
        "question_id": question_id,
        "remaining_options": filtered_opts
    }
