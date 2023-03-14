import random

play1 = str(input("Rock, Paper, or Scissors? ")).capitalize()
play2 = random.randint(1,3)

if play2 == 1:
	play2 = "Rock"
elif play2 == 2:
	play2 = "Paper"
elif play2 == 3:
	play2 = "Scissors"

print("Bot: ", play2)

if play1 == play2:
	print("It's a tie!")
elif (play1 == "Rock" and play2 == "Scissors") or (play1 == "Paper" and play2 == "Rock") or (play1 == "Scissors" and play2 == "Paper"):
	print("V for victory!")
else:
	print("Happens to everyone sometime.")