import difflib

def calculate_score(user_text, original_text):
    user_words = user_text.lower().strip().split()
    original_words = original_text.lower().strip().split()

    
    matcher = difflib.SequenceMatcher(None, original_words, user_words)
    user_analysis = []
    correct_count = 0

    for opcode, i1, i2, j1, j2 in matcher.get_opcodes():
        if opcode == "equal":
            for i in range(i2 - i1):
                user_analysis.append({
                    "word": user_words[j1 + i],
                    "status": "correct"
                })
                correct_count += 1
        elif opcode == "replace":
            for i in range(min(i2 - i1, j2 - j1)):
                user_analysis.append({
                    "word": user_words[j1 + i],
                    "status": "wrong",
                    "expected": original_words[i1 + i]
                })
        elif opcode == "insert":
            for i in range(j1, j2):
                user_analysis.append({
                    "word": user_words[i],
                    "status": "wrong",
                    "expected": None
                })
        elif opcode == "delete":
            for i in range(i1, i2):
                user_analysis.append({
                    "word": original_words[i],
                    "status": "missing"
                })

    score = round((correct_count / len(original_words)) * 100, 2) if original_words else 0.0

    return {
        "score": score,
        "user_text": user_analysis,
        "original_text": original_text
    }
