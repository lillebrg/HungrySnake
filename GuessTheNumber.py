""" Number Guessing Game
----------------------------------------
"""
import random
attempts_list = []
def show_score():
    if len(attempts_list) <= 0:
        print("Der er ingen HighScore, Its up for grabs!")
    else:
        print("HighScoren er lige nu {} forsøg".format(min(attempts_list)))
def start_game():
    random_number = int(random.randint(1, 10))
    print("Whatup BOI. Velkommen til gæt tallet biaaaatch")
    player_name = input("Hvad hedder du? ")
    wanna_play = input("Wassup, {}, vil du spille gæt tallet med mig? (skriv jada/næ) ".format(player_name))
    // Where the show_score function USED to be
    attempts = 0
    show_score()
    while wanna_play.lower() == "jada":
        try:
            guess = input("Vælg et nummer mellem 1 og 10 ")
            if int(guess) < 1 or int(guess) > 10:
                raise ValueError("Cmon, kan du ikke engang finde ud af at vælge et tal imellem 1 og 10? Wow. Prøv igen")
            if int(guess) == random_number:
                print("Nice! You got it!")
                attempts += 1
                attempts_list.append(attempts)
                print("Det tog dig: {} forsøg".format(attempts))
                play_again = input("Skal vi spille endnu en runde?? (skriv jada/næ) ")
                attempts = 0
                show_score()
                random_number = int(random.randint(1, 10))
                if play_again.lower() == "næ":
                    print("Pussy, ses senere håber jeg")
                    break
            elif int(guess) > random_number:
                print("Lavere")
                attempts += 1
            elif int(guess) < random_number:
                print("Højere")
                attempts += 1
        except ValueError as err:
            print("Det giver ikke mening... prøv igen dummy")
            print("({})".format(err))
    else:
        print("Pussy, ses senere håber jeg")
if __name__ == '__main__':
    start_game()