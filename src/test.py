def sum_odds(home_odds, away_odds):
    home_win = 0.0
    draw = 0.0
    away_win = 0.0

    for x in range(len(home_odds)):
        for y in range(len(away_odds)):
            if x > y:
                home_win += (home_odds[x] * away_odds[y])
            elif x == y:
                draw += (home_odds[x] * away_odds[y])
            else:
                away_win += (home_odds[x] * away_odds[y])

    return (home_win, draw, away_win)

def print_odds(odds):
    print("----------------------------------------")
    print("Home Win: {}%".format(odds[0] * 100))
    print("Draw: {}%".format(odds[1] * 100))
    print("Away Win: {}%".format(odds[2] * 100))

home_odds = []
away_odds = []

for _ in range(6):
    x = input("Home team to score {}: ".format(_))
    home_odds.append(float(x))

for _ in range(6):
    x = input("Away team to score {}: ".format(_))
    away_odds.append(float(x))

print(home_odds, away_odds)
odds = sum_odds(home_odds, away_odds)
print_odds(odds)