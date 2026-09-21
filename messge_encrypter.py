import base64
from itertools import cycle

def encrypt_message(plain_text, password):
    """Message ke har character ko password ke sath XOR kar ke base64 string banata hai."""
    xor_bytes = bytes(ord(c) ^ ord(k) for c, k in zip(plain_text, cycle(password)))
    return base64.b64encode(xor_bytes).decode('utf-8')

def decrypt_message(encrypted_string, password):
    """Locked base64 string ko wapas password ke sath XOR kar ke asli text nikalta hai."""
    try:
        xor_bytes = base64.b64decode(encrypted_string.encode('utf-8'))
        plain_bytes = bytes(b ^ ord(k) for b, k in zip(xor_bytes, cycle(password)))
        return plain_bytes.decode('utf-8')
    except Exception:
        return "❌ Error: Invalid code ya galat password!"

# --- MAIN MENU SCREEN ---
if __name__ == "__main__":
    while True:
        print("\n======================================")
        print("    🔒 PURE PYTHON CRYPTO TOOL 🔑    ")
        print("======================================")
        print("1. Message LOCK (Encrypt) karein")
        print("2. Message UNLOCK (Decrypt) karein")
        print("3. Exit (System band karein)")
        
        choice = input("\nApna option select karein (1/2/3): ").strip()
        
        if choice == '1':
            msg = input("📝 Apna Khufiya Message likhein: ")
            pwd = input("🔑 Iska Password set karein: ")
            if not msg or not pwd:
                print("❌ Message aur Password likhna zaroori hai!")
                continue
            locked_text = encrypt_message(msg, pwd)
            print("\n---------------- AAPKA LOCKED CODE ----------------")
            print(locked_text)
            print("---------------------------------------------------")
            print("💡 Tip: Is code ko copy kar ke dosto ko bhej dein.")
            
        elif choice == '2':
            cipher_input = input("🔓 Locked Code paste karein: ").strip()
            pwd = input("🔑 Iska Password enter karein: ")
            original_msg = decrypt_message(cipher_input, pwd)
            print("\n--------------- ORIGINAL MESSAGE ---------------")
            print(original_msg)
            print("------------------------------------------------")
            
        elif choice == '3':
            print("\nSystem closed. Allah Hafiz! 👋")
            break
        else:
            print("\n❌ Ghalat option! Sirf 1, 2 ya 3 select karein.")
