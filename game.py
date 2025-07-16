import random
import json
import os

# -------------------------------
# გლობალური ცვლადები
# -------------------------------

levels = 10
score = 0
high_score = 0
player_data_file = "player_data.json"

attempts_by_level = {
    1: 6, 2: 6,
    3: 5, 4: 5,
    5: 4, 6: 4,
    7: 3, 8: 3,
    9: 2, 10: 1
}

# -------------------------------
# მონაცემების ჩატვირთვა / შენახვა
# -------------------------------

def load_data():
    global high_score
    if os.path.exists(player_data_file):
        with open(player_data_file, "r") as f:
            data = json.load(f)
            high_score = data.get("high_score", 0)

def save_data():
    with open(player_data_file, "w") as f:
        json.dump({"high_score": high_score}, f)

# -------------------------------
# დამხმარე ფუნქციები
# -------------------------------

def get_difficulty():
    print("\nაირჩიე სირთულე:")
    print("1) ადვილი")
    print("2) საშუალო")
    print("3) რთული")
    while True:
        choice = input("შეიყვანე 1, 2 ან 3: ")
        if choice in ["1", "2", "3"]:
            return int(choice)
        else:
            print("⚠️ არასწორი არჩევანი. სცადე თავიდან.")

def get_range_by_difficulty(difficulty, level):
    base = {1: 10, 2: 20, 3: 30}[difficulty]
    return 1, base + (level * 2)

def get_hint(secret, guess):
    if abs(secret - guess) <= 2:
        return "🔥 ძალიან ახლოს ხარ!"
    elif guess < secret:
        return "🔺 ჩემი რიცხვი უფრო დიდია."
    else:
        return "🔻 ჩემი რიცხვი უფრო პატარაა."

# -------------------------------
# თამაშის დაწყება
# -------------------------------

print("🎯 შეგიძლია თუ ვერა... გამოიცნო რიცხვი?")
player_name = input("📛 შეიყვანე შენი სახელი: ")

load_data()
difficulty = get_difficulty()

print(f"\n{name}, დავიწყოთ თამაში! სულ {levels} დონეა.")
print("🎮 წარმატებები!")

for level in range(1, levels + 1):
    min_val, max_val = get_range_by_difficulty(difficulty, level)
    secret = random.randint(min_val, max_val)
    attempts = attempts_by_level.get(level, 3)

    print(f"\n🌟 დონე {level} — გამოიცანი რიცხვი {min_val}-დან {max_val}-მდე")
    print(f"📌 მცდელობები: {attempts}")

    while attempts > 0:
        try:
            guess = int(input("👉 შენი პასუხი: "))
        except ValueError:
            print("⚠️ გთხოვ, შეიყვანე მხოლოდ რიცხვი.")
            continue

        if guess == secret:
            bonus = attempts * 10
            print(f"✅ სწორია! მიიღე ბონუს ქულები: {bonus}")
            score += bonus
            break
        else:
            attempts -= 1
            print("❌ არასწორია.")
            print(get_hint(secret, guess))
            if attempts > 0:
                print(f"🔁 დარჩენილი მცდელობები: {attempts}")

    else:
        print(f"💀 წააგე დონე {level}-ზე. სწორი პასუხი იყო: {secret}")
        break

# -------------------------------
# შედეგების ჩვენება
# -------------------------------

print(f"\n🎉 თამაში დასრულდა! შენმა ქულამ შეადგინა: {score} ქულა")

if score > high_score:
    print(f"🏆 გილოცავ! ახალი რეკორდი: {score} ქულა (ძველი იყო {high_score})")
    high_score = score
    save_data()
else:
    print(f"📊 შენი რეკორდი კვლავ რჩება: {high_score} ქულა")

print("🙏 მადლობა თამაშისთვის!")
