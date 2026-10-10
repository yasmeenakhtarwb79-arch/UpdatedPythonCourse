import tkinter as tk
from tkinter import messagebox

# Professional & Corporate Vocabulary Dictionary (A-Z)
word_dictionary = {
    'A': "Accomplished (صلاحیتوں کا حامل / ماہر)",
    'B': "Benevolent (مخلص / خیر خواہ)",
    'C': "Competent (اہل / باصلاحیت)",
    'D': "Driven (پرعزم / باہمت)",
    'E': "Efficient (کام چور نہیں / مستعد)",
    'F': "Focused (توجہ مرکوز رکھنے والا)",
    'G': "Genuine (سچا / کھرا)",
    'H': "Honorable (معزز / قابل احترام)",
    'I': "Innovative (جدت پسند / ذہین)",
    'J': "Judicious (دانشمند / عاقل)",
    'K': "Knowledgeable (علم رکھنے والا)",
    'L': "Loyal (وفادار / مخلص)",
    'M': "Motivated (پرجوش / متحرک)",
    'N': "Noble (شریف / عالی ظرف)",
    'O': "Optimistic (امید پسند / مثبت سوچ)",
    'P': "Punctual (وقت کا پابند)",
    'Q': "Qualified (اہل / سند یافتہ)",
    'R': "Resilient (مستحکم / حالات کا مقابلہ کرنے والا)",
    'S': "Strategic (حکمت عملی بنانے والا / دور اندیش)",
    'T': "Trustworthy (قابل اعتماد)",
    'U': "Unparalleled (بے مثال / بے نظیر)",
    'V': "Visionary (دور اندیش / صاحبِ بصیرت)",
    'W': "Wise (عاقل / دانا)",
    'X': "Xenial (مہمان نواز / خوش اخلاق)",
    'Y': "Yielding (مثبت نتائج دینے والا / لچکدار)",
    'Z': "Zealous (سرگرم / پرجوش)"
}

def generate_acrostic():
    # Get user input and convert to uppercase
    input_name = entry_name.get().upper().strip()
    
    if not input_name:
        messagebox.showwarning("Warning", "Please enter a name!")
        return
    
    result_text = ""
    
    # Process each character of the input name
    for letter in input_name:
        if letter in word_dictionary:
            result_text += f"{letter}  -  {word_dictionary[letter]}\n"
        elif letter.isspace():
            result_text += "\n"  # Handles spaces between names
            
    # Update the display layout with results
    label_result.config(text=result_text)

# Main Application GUI Window Setup
root = tk.Tk()
root.title("Professional Acrostic Profile Generator")
root.geometry("500x600")
root.config(bg="#f4f6f9")  # Clean Professional Light Gray Background

# Professional Header
title_label = tk.Label(root, text="Professional Profile Generator", font=("Helvetica", 18, "bold"), bg="#f4f6f9", fg="#1a202c")
title_label.pack(pady=25)

# Input Field Label
input_label = tk.Label(root, text="Enter Executive Name / Word:", font=("Helvetica", 11), bg="#f4f6f9", fg="#4a5568")
input_label.pack(pady=5)

# Entry Box (User Input)
entry_name = tk.Entry(root, font=("Helvetica", 14), width=28, justify="center", bd=2, relief="groove")
entry_name.pack(pady=5)

# Corporate Style Blue Button
btn_generate = tk.Button(root, text="Generate Profile", font=("Helvetica", 12, "bold"), bg="#1a365d", fg="white", padx=15, pady=8, bd=0, cursor="hand2", command=generate_acrostic)
btn_generate.pack(pady=25)

# Output Section Configuration
label_result = tk.Label(root, text="", font=("Courier New", 14, "bold"), bg="#f4f6f9", fg="#2d3748", justify="left")
label_result.pack(pady=10)

# Execute Application Loop
root.mainloop()
