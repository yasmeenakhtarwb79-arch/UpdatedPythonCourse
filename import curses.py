import curses

# اسکرین سیٹ اپ
screen = curses.initscr()
curses.curs_set(0)
sh, sw = screen.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(50)  # گیم کی اسپیڈ

# پیڈلز اور بال کی پوزیشنز
pad1_y, pad2_y = sh//2, sh//2
ball_x, ball_y = sw//2, sh//2
ball_dx, ball_dy = 1, 1

score1, score2 = 0, 0

# گیم کا مین لوپ
while True:
    w.clear()
    
    # محفوظ اسکور بورڈ (اگر اسکرین بہت چھوٹی ہو تو یہ کریش نہیں کرے گا)
    try:
        w.addstr(0, max(2, sw//2 - 25), f"=== CYBER X PONG === | PLAYER 1: {score1} | PLAYER 2: {score2} ===", curses.A_BOLD)
    except curses.error:
        pass
    
    # اوپر اور نیچے کی دیواریں (Borders کو 1 ہندسہ اندر کر دیا تاکہ ERR نہ آئے)
    for x in range(0, sw - 1):
        try:
            w.addch(1, x, '-')
            w.addch(sh - 2, x, '-')  # یہاں sh-1 کی جگہ sh-2 کیا ہے تاکہ ایرر نہ آئے
        except curses.error:
            pass
        
    # پیڈلز بنانا (سائز: 3 بلاکس)
    for i in range(-1, 2):
        try:
            if 1 < pad1_y + i < sh - 2: w.addch(pad1_y + i, 2, curses.ACS_CKBOARD)
            if 1 < pad2_y + i < sw - 4: w.addch(pad2_y + i, sw - 4, curses.ACS_CKBOARD)
        except curses.error:
            pass
        
    # گیند (Ball) بنانا
    try:
        w.addch(ball_y, ball_x, curses.ACS_LANTERN)
    except curses.error:
        pass
    
    # کی بورڈ ان پٹ (Player 1: W/S اور Player 2: Up/Down Arrows)
    key = w.getch()
    if key == ord('w') and pad1_y > 3: pad1_y -= 1
    if key == ord('s') and pad1_y < sh - 4: pad1_y += 1
    if key == curses.KEY_UP and pad2_y > 3: pad2_y -= 1
    if key == curses.KEY_DOWN and pad2_y < sh - 4: pad2_y += 1
    
    # گیند کی موومنٹ
    ball_x += ball_dx
    ball_y += ball_dy
    
    # اوپر اور نیچے کی دیواروں سے ٹکراؤ
    if ball_y <= 2 or ball_y >= sh - 3:
        ball_dy *= -1
        
    # پیڈل 1 (لیفٹ سائیڈ) سے ٹکراؤ
    if ball_x == 3 and pad1_y - 1 <= ball_y <= pad1_y + 1:
        ball_dx *= -1
        
    # پیڈل 2 (رائٹ سائیڈ) سے ٹکراؤ
    if ball_x == sw - 5 and pad2_y - 1 <= ball_y <= pad2_y + 1:
        ball_dx *= -1
        
    # اگر گیند مس ہو جائے (اسکور ہونا)
    if ball_x < 1:
        score2 += 1
        ball_x, ball_y = sw//2, sh//2
        ball_dx *= -1
    elif ball_x > sw - 3:
        score1 += 1
        ball_x, ball_y = sw//2, sh//2
        ball_dx *= -1
        
    # گیم اوور کی شرط (اگر کوئی بھی 5 اسکور کر لے)
    if score1 == 5 or score2 == 5:
        curses.endwin()
        winner = "PLAYER 1" if score1 == 5 else "PLAYER 2"
        print("\n" + "="*40)
        print(f" SYSTEM OVERRIDE: GAME OVER!\n WINNER: {winner}\n FINAL SCORE: {score1} - {score2}\n PROJECT BY: CYBER X")
        print("="*40 + "\n")
        quit()
