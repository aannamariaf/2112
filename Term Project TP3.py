from cmu_112_graphics import *
import math
import random
import time

# card images: https://commons.wikimedia.org/wiki/File:English_pattern_playing_cards_deck.svg
# suit images: http://www.clipartbest.com/suits-deck-of-cardsHave 
# table image: https://pharaohusa.com/catalog/tables/games/blackjack-tables/nile-blackjack/ 
# back of card image: https://www.fadedspade.com/ 
# Working with text files: https://stackoverflow.com/questions/17140886/how-to-search-and-replace-text-in-a-file 
# Understanding Monte Carlo: https://towardsdatascience.com/learning-to-win-blackjack-with-monte-carlo-methods-61c90a52d53e 

###############################################################################
# Main Screen
###############################################################################

def mainScreenMode_redrawAll(app,canvas):

    canvas.create_rectangle(0,0,app.width,app.height,fill="black")

    canvas.create_text(app.width/2, app.height*(4/10), 
                        text = "21|12", 
                        fill = "darkred", font = "courier 70")

    canvas.create_rectangle(app.width*(7/20), app.height*(11.2/20),
                            app.width*(13/20), app.height*(12.8/20),
                            fill = "black", outline = "white", width = 1)

    canvas.create_text(app.width/2, app.height*(12/20), 
                        text = "Enter Your Username To Begin.", 
                        fill = "white", font = "courier 15")
    
def mainScreenMode_mousePressed(app,event):
    (x, y) = (event.x, event.y)
    (boxx1, boxx2) = (int(app.width*(7/20)), int(app.width*(13/20)))
    (boxy1, boxy2) = (int(app.height*(11.2/20)), int(app.height*(12.8/20)))

    if x in range(boxx1, boxx2) and y in range(boxy1, boxy2):
        app.username = app.getUserInput('Username')
        app.mode = "homeScreenMode"
            
###############################################################################
# Home Screen
###############################################################################

def homeScreenMode_redrawAll(app,canvas):

    canvas.create_rectangle(0,0,app.width,app.height,fill="black")
    canvas.create_text(80, app.height-30, text = "<- Backspace", 
                        fill = "darkred", font = "courier 15 bold")

    canvas.create_text(app.width/2, app.height*(1/10),
                        text = f"Welcome {app.username}.",
                        fill = "darkred", font = "courier 30 bold")
   
    canvas.create_text(app.width/2, app.height*(2/10),
                         text = "Click on a Suit to Choose a Mode.", 
                         fill = "darkred", font = "courier 30")
    
    canvas.create_image(app.width/4, app.height/2+app.height/15, 
                        image = ImageTk.PhotoImage(app.heart))

    canvas.create_text(app.width/4, app.height/2+app.height/22, 
                        text = "COUNTING\n CARDS", 
                        fill = "black", font = "courier 20 bold")
    
    canvas.create_image(app.width*(3/4), app.height/2+app.height/15,
                        image = ImageTk.PhotoImage(app.diamond)) 
    
    canvas.create_text(app.width*(3/4), app.height/2+app.height/15,
                        text = "BLACKJACK",
                        fill = "black", font = "courier 15 bold")

def homeScreenMode_keyPressed(app,event):
    if event.key == "Left":
        app.mode = "countCardsMode"
    elif event.key == "Right":
        app.mode = "blackjackMode"
    elif event.key == "Backspace":
        app.mode = "mainScreenMode"

def homeScreenMode_mousePressed(app,event):
    (x, y) = (event.x, event.y)
    heartWidth, heartHeight = app.heart.size
    diamWidth, diamHeight = app.diamond.size
    (heartCx, heartCy) = (int(app.width//4), app.height//2 + app.height//15)
    (diamCx, diamCy) = (int(app.width*(3/4)), app.height//2 + app.height//15)

    if (y in range((heartCy - (heartHeight//2)), 
                    (heartCy + (heartHeight//2))) and 
        x in range((heartCx - (heartWidth//2)), 
                    (heartCx + (heartWidth//2)))):
        app.mode = "countCardsMode"

    elif (y in range((diamCy - (diamHeight//2)), 
                (diamCy + (diamHeight//2))) and 
        x in range((diamCx - (diamWidth//2)), 
                (diamCx + (diamWidth//2)))):
        app.mode = "blackjackMode"

###############################################################################
# Blackjack
###############################################################################

def startBlackjack(app):
    # images in blackjack
    app.table = app.loadImage("blackjackTable.png")
    (app.tableWidth, app.tableHeight) = app.table.size
    # variables in blackjack
    app.bdecks = 3
    app.bplayers = 6
    app.variant = False
    app.numberOfUsers = 1
    blackjackReset(app)
    
    
def blackjackReset(app):
    
    createCards(app)
    app.showRecs = False
    app.cardBack = app.scaleImage(app.loadImage("cardBack.png"), 1/10)
    app.startGame = False
    app.split = False
    app.splitTurn = 0
    app.storage = []
    app.splitVariant = False
    app.startVariantRound = False
    app.variable = True

    app.buttonsOn = False
    app.playersTurn = 0
    app.turnsLeft = 1
    app.hits = 1

    app.bplayersScores = dict()
    app.bet = dict()
    app.riskLevels = dict()

    for i in range(app.bplayers):
        app.bplayersScores[f"Player {i + 1}"] = 500
        app.bet[f"Player {i + 1}"] = 0
        list = [0.5, 1.0, 1.5]
        app.riskLevels[f"Player {i + 1}"] = random.choice(list)

    app.storeCardsUsed = []
    app.cardsUsed = []
    app.angle = math.pi/(app.bplayers+1)
    app.cardRound = "round1"
    app.dealRound = True
    app.checkedForNaturals = False
    setUpDictionaries(app)

def blackjackNewRound(app):
    app.storeCardsUsed = copy.deepcopy(app.cardsUsed)
    app.cardsUsed = []
    app.cardBack = app.scaleImage(app.loadImage("cardBack.png"), 1/10)
    app.split = False
    app.splitTurn = 0
    app.buttonsOn = False
    app.playersTurn = 0
    app.turnsLeft = 1
    app.hits = 1
    app.startGame = True
    app.angle = math.pi/(app.bplayers+1)
    app.cardRound = "round1"
    app.dealRound = True
    app.checkedForNaturals = False
    app.storage = []
    app.splitVariant = False
    app.startVariantRound = False
    app.variable = True
    setUpDictionaries(app)
    
def setUpDictionaries(app):
    app.playersCards = dict()
    app.playersImages = dict()
    app.cardLoc = []
    app.newCardLoc = dict()
    app.playersCounts = dict()

    app.splitPlayersCounts = dict()
    app.splitPlayersCards = dict()

    for i in range(app.bplayers):
        app.playersCards[f"Player {i + 1}"] = []
        app.playersImages[f"Player {i + 1}"] = []
        app.playersCounts[f"Player {i + 1}"] = 0
        app.newCardLoc[f"Player {i + 1}"] = []

        app.splitPlayersCounts[f"Player {i + 1}"] = 0
        app.splitPlayersCards[f"Player {i + 1}"] = []

    app.playersCounts["Dealer"] = 0
    app.playersCards["Dealer"] = []
    app.playersImages["Dealer"] = []
    app.newCardLoc["Dealer"] = []


def blackjackMode_redrawAll(app,canvas):
    # canvas
    canvas.create_rectangle(0,0,app.width,app.height,fill="black")
    canvas.create_text(80, app.height-30, text = "<- Backspace", 
                        fill = "darkred", font = "courier 15 bold")
    # table
    canvas.create_image(app.width/2, app.height/2, 
                        image = ImageTk.PhotoImage(app.table))

    # Settings box
    canvas.create_rectangle(app.width*(1/20), app.height*(1/10), 
                            app.width*(4/20), app.height*(3/20), 
                            fill = "lightgray")
    canvas.create_text(app.width*(2.5/20), app.height*(2.5/20), 
                    text = "SETTINGS", fill = "black", 
                    font = "courier 15 bold")

    # How to play box
    canvas.create_rectangle(app.width*(1/20), app.height*(1/5), 
                            app.width*(4/20), app.height*(1/4), 
                            fill = "lightgray")
    canvas.create_text(app.width*(2.5/20), app.height*(4.5/20), 
                    text = "HOW TO PLAY", fill = "black", 
                    font = "courier 15 bold")

    # game "buttons"
    canvas.create_oval(app.width*(19/20)-35, app.height*(9/20)-35, 
                        app.width*(19/20)+35, app.height*(9/20)+35, fill = "darkred")
    canvas.create_text(app.width*(19/20), app.height*(9/20), 
                        text = "STAND", fill = "black", font = "courier 15 bold") 
    canvas.create_oval(app.width*(19/20)-35, app.height*(12/20)-35,
                        app.width*(19/20)+35, app.height*(12/20)+35, fill = "darkgreen")
    canvas.create_text(app.width*(19/20), app.height*(12/20), 
                        text = "HIT", fill = "black", font = "courier 15 bold") 
    canvas.create_oval(app.width*(19/20)-35, app.height*(15/20)-35, 
                        app.width*(19/20)+35, app.height*(15/20)+35, fill = "yellow")
    canvas.create_text(app.width*(19/20), app.height*(15/20),
                        text = "SPLIT", fill = "black", font = "courier 15 bold") 
    canvas.create_oval(app.width*(19/20)-35, app.height*(18/20)-35, 
                        app.width*(19/20)+35, app.height*(18/20)+35, fill = "orange")
    canvas.create_text(app.width*(19/20), app.height*(18/20), 
                        text = "DD", fill = "black", font = "courier 15 bold")                  

    if app.startGame == False:
        canvas.create_text(app.width/2, app.height*(3/20), 
                            text = "PRESS ENTER TO BEGIN.",
                            fill = "White", font = "courier 25 bold")
    elif app.startGame == True:
        canvas.create_text(app.width/2, app.height*(2/20),
                            text = "Press r to Reset Game.",
                            fill = "White", font = "courier 20 bold italic")

        drawStartingCards(app, canvas)
        drawNewCards(app,canvas)
        drawPlayerBox(app, canvas)
        if app.playersTurn >= app.bplayers + 2:
            canvas.create_rectangle(app.width/4, app.height*(1/20), 
                                    app.width*(3/4), app.height*(3/20),
                                    fill = "lightgray", outline = "black", width = 1)
            canvas.create_text(app.width/2, app.height*(2/20),
                                text = "PRESS SPACE TO BEGIN A NEW ROUND",
                                fill = "black", font = "courier 20 bold")

        if len(app.cardsHave) <= 25:
            canvas.create_text(app.width*(1/5), app.height*(19/20), text = "RESHUFFLING CARDS",
                                fill = "darkred", font = "courier 20 bold italic")
    
    if app.showRecs == False:
        canvas.create_rectangle(app.width*(16/20), app.height*(1/10),
                                app.width*(19/20), app.height*(3/20),
                                fill = "lightgray")
        canvas.create_text(app.width*(17.5/20), app.height*(2.5/20),
                            text = "BETTING RECS", fill = "darkred",
                            font = "courier 15 bold")
    if app.showRecs == True:
        bcount = calculateBJCardCountWrapper(app)
        trueCount = bcount/app.bdecks
        if (trueCount + 1) * 10 > 10:
            bet = (trueCount + 1) * 10
        else:
            bet = 10
        if (trueCount - 1) * 25 > 10:
            riskyBet = (trueCount - 1) * 25 
        else: 
            riskyBet = 15
        trueCount = str(trueCount)[0:4]
        bet = int(bet)
        riskyBet = int(riskyBet)

        canvas.create_rectangle(app.width*(16/20), app.height*(1/10),
                                app.width*(19/20), app.height*(4/20),
                                fill = "lightgray", outline = "red", width = 2)
        canvas.create_text(app.width*(17.5/20), app.height*(3/20),
                            text = f"Count: {bcount}\nTrue Count: {trueCount}\nBet: {bet}\nBet Opt. 2: {riskyBet}",
                            fill = "darkred", font = "courier 9 bold")

def blackjackMode_timerFired(app):
    if app.startGame == True:
        if len(app.cardsHave) <= 25:
            time.sleep(1.5)
            createCards(app)
            app.cardsUsed = []
            blackjackNewRound(app)

        if app.dealRound == True:
            if app.cardRound == "round1":
                (x, y) = (0, 0)
                dealCards(app,x,y)
            elif app.cardRound == "round2":
                (x, y) = (10, 10)
                dealCards(app,x,y)
        elif app.variant == False:
            
            if app.checkedForNaturals == False:
                assignPlayerOrigCards(app)
                assignPlayerCounts(app)
                checkForNaturals(app)

            else:
                beginRound(app)
        
        elif app.variant == True:
            if (app.checkedForNaturals == False and app.playersTurn == 0 and 
                app.splitVariant == False and app.startVariantRound == False):
                assignPlayerOrigCards(app)
                assignPlayerCounts(app)
                app.splitVariant = True
                app.checkedForNaturals = True

            if app.playersTurn == app.bplayers and app.splitVariant == True:

                for i in range(app.numberOfUsers):
                    if i == 0:
                        player = app.username
                    else:
                        player = f"Guest {i}"
                    switch = app.getUserInput(f"{player}, would you like to switch your bottom two cards? (yes or no)")
                    if switch == "yes":
                        switching(app, i)
                    else: 
                        pass
                app.playersTurn = app.numberOfUsers
                app.splitVariant = False

            if app.playersTurn < app.bplayers and app.splitVariant == True:
                i = app.playersTurn
                split(app, i)
                hit(app, i)
                app.splitTurn = 1
                app.hits = 0
                hit(app, i)
                app.playersTurn = i + 1
                app.splitTurn = 0
                app.hits = 1
            

            if  app.playersTurn < app.bplayers and app.splitVariant == False and app.startVariantRound == False:
                
                time.sleep(0.5)
                i = app.playersTurn
                count1 = app.playersCounts[f"Player {i + 1}"]
                count2 = app.splitPlayersCounts[f"Player {i + 1}"]
                hand1 = (count1, app.dealerUpcard)
                hand2 = (count2, app.dealerUpcard)
                if count1 != 22 and count2 != 22:
                    if app.policy[hand1][0] == "s": j = 0
                    elif app.policy[hand1][0] == "h": j = 1
                    elif app.policy[hand1][1] == "s": j = 0
                    elif app.policy[hand1][1] == "h": j = 1
                    if app.policy[hand2][0] == "s": k = 0
                    elif app.policy[hand2][0] == "h": k = 1
                    elif app.policy[hand2][1] == "s": k = 0
                    elif app.policy[hand2][1] == "h": k = 1                
                    winnings = app.Q[hand1][j] + app.Q[hand2][k]
                else: winnings = -100

                switch = app.playersCards[f"Player {1+i}"][1]
                switch2 = app.splitPlayersCards[f"Player {1+i}"][1]
                app.playersCards[f"Player {1+i}"][1] = switch2
                app.splitPlayersCards[f"Player {1+i}"][1] = switch
                assignPlayerCounts(app)

                potcount1 = app.playersCounts[f"Player {i + 1}"]
                potcount2 = app.splitPlayersCounts[f"Player {i + 1}"]
                pothand1 = (potcount1, app.dealerUpcard)
                pothand2 = (potcount2, app.dealerUpcard)
                if potcount1 != 22 and potcount2 != 22: 
                    if app.policy[pothand1][0] == "s": j = 0
                    elif app.policy[pothand1][0] == "h": j = 1
                    elif app.policy[pothand1][1] == "s": j = 0
                    elif app.policy[pothand1][1] == "h": j = 1
                    if app.policy[pothand2][0] == "s": k = 0
                    elif app.policy[pothand2][0] == "h": k = 1
                    elif app.policy[pothand2][1] == "s": k = 0
                    elif app.policy[pothand2][1] == "h": k = 1 
                    potwinnings = app.Q[pothand1][j] + app.Q[pothand2][k]
                else: potwinnings = -100

                if ((winnings >= potwinnings or hand1[0] == 21 or hand2[0] == 21) 
                    and (pothand1[0] != 21 and pothand2[0] != 21)):

                    switch = app.playersCards[f"Player {1+i}"][1]
                    switch2 = app.splitPlayersCards[f"Player {1+i}"][1]
                    app.playersCards[f"Player {1+i}"][1] = switch2
                    app.splitPlayersCards[f"Player {1+i}"][1] = switch
                    assignPlayerCounts(app)

                elif potwinnings > winnings or pothand1[0] == 21 or pothand2[0] == 21:
                    
                    switch = app.playersCards[f"Player {1+i}"][1]
                    switch2 = app.splitPlayersCards[f"Player {1+i}"][1]
                    app.playersCards[f"Player {1+i}"][1] = switch2
                    app.splitPlayersCards[f"Player {1+i}"][1] = switch
                    assignPlayerCounts(app)
                    switching(app, i)

                app.playersTurn += 1

            if app.playersTurn == app.bplayers and app.splitVariant == False:
                if app.checkedForNaturals == True:
                    for player in range(app.bplayers):

                        if app.playersCounts[f"Player {player + 1}"] == 21:
                            app.newCardLoc[f"Player {player + 1}"][1] = (["21"] 
                            + app.newCardLoc[f"Player {player + 1}"][1])

                        if app.splitPlayersCounts[f"Player {player + 1}"] == 21:
                            app.newCardLoc[f"Player {player + 1}"][0] = (["21"] 
                            + app.newCardLoc[f"Player {player + 1}"][0])

                    for i in app.playersCounts:
                        if app.playersCounts[i] == 22:
                            app.playersCounts[i] -= 10

                    for i in app.splitPlayersCounts:
                        if app.splitPlayersCounts[i] == 22:
                            app.splitPlayersCounts[i] -= 22
                                    
                    insuranceBet = []
                    uc = app.playersCards["Dealer"][0][0]
                    if uc == "A":
                        for i in range(app.numberOfUsers):
                            if i == 0: player = f"{app.username}"
                            else: player = f"Guest {i}"
                            
                            insurance = app.getUserInput(f"Does {player} want to make an Insurance Bet? (yes or no)")
                            if insurance == "yes":
                                insuranceBet += [i]
                                app.bplayersScores[f"Player {i+1}"] -= (app.bet[f"Player {i+1}"]//2)
                            else:
                                pass

                    if app.playersCounts["Dealer"] == 21:

                        for item in insuranceBet:
                            app.bplayersScores[f"Player {1+item}"] += app.bet[f"Player {1+item}"]

                        for i in range(app.bplayers):
                            if app.playersCounts[f"Player {i+1}"] == 21:
                                app.bplayersScores[f"Player {i+1}"] += app.bet[f"Player {i+1}"]
                                app.bet[f"Player {i+1}"] = 0
                            
                            if app.splitPlayersCounts[f"Player {i+1}"] == 21:
                                app.bplayersScores[f"Player {i+1}"] += app.bet[f"Player {i+1}"]
                                app.bet[f"Player {i+1}"] = 0
                                    
                        for i in range(app.numberOfUsers):
                            if i == 0: player = f"{app.username}"
                            else: player = f"Guest {i}"
                            try:
                                app.bet[f"Player {i+1}"] = int(app.getUserInput((f'Betting Amount of {player}')))
                                if app.bet[f"Player {i+1}"] <= 10: app.bet[f"Player {i+1}"] = 10
                            except:
                                app.bet[f"Player {i+1}"] = 10
                            app.bplayersScores[f"Player {i+1}"] -= app.bet[f"Player {i+1}"]

                        for i in range(app.numberOfUsers, app.bplayers):
                            app.bet[f"Player {i + 1}"] = findBet(app,i)
                            app.bplayersScores[f"Player {i + 1}"] -= app.bet[f"Player {i + 1}"]

                        returnTurnOver(app, "Dealer", "21")
                        blackjackNewRound(app)

            
                    else:
                        for i in range(app.bplayers):
                            if app.playersCounts[f"Player {i+1}"] == 21: 
                                app.bplayersScores[f"Player {i+1}"] += app.bet[f"Player {i+1}"]*(2.5)
                                app.bet[f"Player {i+1}"] -= (app.bet[f"Player {i+1}"]/2)

                            if app.splitPlayersCounts[f"Player {i+1}"] == 21: 
                                app.bplayersScores[f"Player {i+1}"] += app.bet[f"Player {i+1}"]*(2.5)
                                app.bet[f"Player {i+1}"] -= (app.bet[f"Player {i+1}"]/2)

                            if app.playersCounts[f"Player {i+1}"] == 22:
                                rest = app.playersCards[f"Player {i + 1}"][0][1:]
                                app.playersCards[f"Player {i + 1}"][0] = "1" + rest
                                app.playersCounts[f"Player {i+1}"] -= 10
                                assignPlayerCounts(app)

                            if app.splitPlayersCounts[f"Player {i+1}"] == 22:
                                rest = app.splitPlayersCards[f"Player {i + 1}"][0][1:]
                                app.splitPlayersCards[f"Player {i + 1}"][0] = "1" + rest
                                app.splitPlayersCounts[f"Player {i+1}"] -= 10
                                assignPlayerCounts(app)

                    app.checkedForNaturals = False
                    app.startVariantRound = True 
                    app.playersTurn = 0

            if app.startVariantRound == True:
                beginRound(app)
            

def switching(app, player):
    switch = app.playersCards[f"Player {1+player}"][1]
    switch2 = app.splitPlayersCards[f"Player {1+player}"][1]
    app.playersCards[f"Player {1+player}"][1] = switch2
    app.splitPlayersCards[f"Player {1+player}"][1] = switch

    image1 = app.playersImages[f"Player {player + 1}"][0]
    image2 = app.playersImages[f"Player {player + 1}"][1]
    app.playersImages[f"Player {player + 1}"][0] = image2
    app.playersImages[f"Player {player + 1}"][1] = image1

    assignPlayerCounts(app)


def drawStartingCards(app, canvas):
    for i in range(len(app.cardLoc)):
        if app.cardLoc[i][0] == "None":
            canvas.create_image(app.cardLoc[i][1], app.cardLoc[i][2], 
                                image = ImageTk.PhotoImage(app.cardsUsed[i][1]))
            canvas.create_rectangle(app.cardLoc[i][1] - 50, app.cardLoc[i][2] - 20, 
                                    app.cardLoc[i][1] + 50, app.cardLoc[i][2] + 20,
                                    fill = "lightgrey", outline = "darkred")

            canvas.create_text(app.cardLoc[i][1], app.cardLoc[i][2], 
                                text = "BUST", fill = "darkred", font = "courier 25 bold")
        elif app.cardLoc[i][0] == "21":
            canvas.create_image(app.cardLoc[i][1], app.cardLoc[i][2], 
                                image = ImageTk.PhotoImage(app.cardsUsed[i][1]))
            canvas.create_rectangle(app.cardLoc[i][1] - 30, app.cardLoc[i][2] - 20, 
                                    app.cardLoc[i][1] + 30, app.cardLoc[i][2] + 20,
                                    fill = "lightgrey", outline = "darkgreen")

            canvas.create_text(app.cardLoc[i][1], app.cardLoc[i][2], 
                                text = "21", fill = "darkgreen", font = "courier 25 bold")
        elif app.cardLoc[i][0] == "FinalCard":
            canvas.create_image(app.cardLoc[i][1], app.cardLoc[i][2], 
                                image = ImageTk.PhotoImage(app.cardBack))
        else:   
            canvas.create_image(app.cardLoc[i][0], app.cardLoc[i][1], 
                                image = ImageTk.PhotoImage(app.cardsUsed[i][1]))

def drawPlayerBox(app, canvas):
    for i in range(app.numberOfUsers):
        if i == 0:
            player = f"{app.username}"
        else:
            player = f"Guest {i}"
        if i == app.playersTurn: size = 18
        else: size = 15
        canvas.create_text(app.width/2 + (app.tableWidth/2)*math.cos(math.pi*(1/(app.bplayers+1))*(i+1)),
                            app.height*(1/20) + (app.tableWidth/2)*math.sin(math.pi*(1/(app.bplayers+1))*(i+1)) + 105,
                            text = f"{player}", 
                            fill = "White", font = f"courier {size} bold")
        money = app.bplayersScores[f"Player {i+1}"]
        canvas.create_text(app.width/2 + (app.tableWidth/2)*math.cos(math.pi*(1/(app.bplayers+1))*(i+1)),
                            app.height*(1/20) + (app.tableWidth/2)*math.sin(math.pi*(1/(app.bplayers+1))*(i+1)) + 125,
                            text = f"Money: ${money}", 
                            fill = "darkred", font = "courier 12 bold")

    for i in range(app.numberOfUsers, app.bplayers):
        player = f"Player {i+1}"
        if i == app.playersTurn: size = 18
        else: size = 15
        canvas.create_text(app.width/2 + (app.tableWidth/2)*math.cos(math.pi*(1/(app.bplayers+1))*(i+1)),
                            app.height*(1/20) + (app.tableWidth/2)*math.sin(math.pi*(1/(app.bplayers+1))*(i+1)) + 105,
                            text = f"{player}", 
                            fill = "White", font = f"courier {size} bold")
        money = app.bplayersScores[f"Player {i+1}"]
        canvas.create_text(app.width/2 + (app.tableWidth/2)*math.cos(math.pi*(1/(app.bplayers+1))*(i+1)),
                            app.height*(1/20) + (app.tableWidth/2)*math.sin(math.pi*(1/(app.bplayers+1))*(i+1)) + 125,
                            text = f"Money: ${money}", 
                            fill = "darkred", font = "courier 12 bold")

def drawNewCards(app, canvas): 
    try:
        for i in app.newCardLoc:
            for j in range(len(app.newCardLoc[i])):
                if app.newCardLoc[i][j][0] == "None":
                    canvas.create_image(app.newCardLoc[i][j][1], app.newCardLoc[i][j][2], 
                                image = ImageTk.PhotoImage(app.playersImages[i][j]))
                    canvas.create_rectangle(app.newCardLoc[i][j][1] - 50, app.newCardLoc[i][j][2] - 20, 
                                            app.newCardLoc[i][j][1] + 50, app.newCardLoc[i][j][2] + 20,
                                            fill = "lightgrey", outline = "darkred")
                    canvas.create_text(app.newCardLoc[i][j][1] , app.newCardLoc[i][j][2], 
                                        text = "BUST", fill = "darkred",
                                        font = "courier 25 bold")
                elif app.newCardLoc[i][j][0] == "21":
                    canvas.create_image(app.newCardLoc[i][j][1], app.newCardLoc[i][j][2], 
                                image = ImageTk.PhotoImage(app.playersImages[i][j]))
                    canvas.create_rectangle(app.newCardLoc[i][j][1] - 30, app.newCardLoc[i][j][2] - 20, 
                                            app.newCardLoc[i][j][1] + 30, app.newCardLoc[i][j][2] + 20,
                                            fill = "lightgrey", outline = "darkgreen")
                    canvas.create_text(app.newCardLoc[i][j][1], app.newCardLoc[i][j][2], 
                                        text = "21", fill = "darkgreen", 
                                        font = "courier 25 bold")
                else:
                    canvas.create_image(app.newCardLoc[i][j][0], app.newCardLoc[i][j][1], 
                                image = ImageTk.PhotoImage(app.playersImages[i][j])) 
    except: pass

def dealCards(app,x,y):
# this function creates the locations of all the images of the cards, removes the cards from the deck, and adds them to a cards used list
    time.sleep(0.1)
    if app.angle < math.pi:
        (cardx, cardy) = (app.width/2 + (app.tableWidth/2)*math.cos(app.angle) + x, 
                        app.height*(1/20) + (app.tableWidth/2)*math.sin(app.angle) + y)
        app.cardLoc.append([cardx,cardy])
        card = (random.choice(app.cardsHave))
        app.cardsHave.remove(card)
        app.cardsUsed.append(card)
        app.angle += math.pi/(app.bplayers+1)

    elif app.angle >= math.pi and app.cardRound == "round1":
        app.cardLoc.append([app.width/2-40, app.height*(5/20)]) 
        card = (random.choice(app.cardsHave))
        app.cardsHave.remove(card)
        app.cardsUsed.append(card)    
        app.cardRound = "round2"  
        app.angle = math.pi/(app.bplayers+1)

    elif app.angle >= math.pi and app.cardRound == "round2":
        app.cardLoc.append(['FinalCard', app.width/2+40, app.height*(5/20)])
        card = (random.choice(app.cardsHave))
        app.cardsHave.remove(card)
        app.cardsUsed.append(card)
        app.dealRound = False

def assignPlayerOrigCards(app):
# After cards are dealt, each player is assigned their cards 
    for i in range(app.bplayers):
        app.playersCards[f"Player {i + 1}"] = []
    app.playersCards["Dealer"] = []

    for i in range(len(app.cardsUsed)):
        player = (i + 1) % (app.bplayers + 1)
        if player == 0:
            app.playersCards["Dealer"] += [app.cardsUsed[i][0]]
        else:
            app.playersCards[f"Player {player}"] += [app.cardsUsed[i][0]]

def assignPlayerCounts(app):
# players counts are kept track of 
    for i in range(app.bplayers):
        app.playersCounts[f"Player {i + 1}"] = 0
        app.splitPlayersCounts[f"Player {i + 1}"] = 0

    app.playersCounts["Dealer"] = 0

    for item in app.splitPlayersCards:
        for i in range(len(app.splitPlayersCards[item])):
            if (app.splitPlayersCards[item][i][0:2] == '10' or 
                            app.splitPlayersCards[item][i][0] == 'J' or 
                            app.splitPlayersCards[item][i][0]== 'Q' or 
                            app.splitPlayersCards[item][i][0] == 'K'): 
                            value = 10
            elif app.splitPlayersCards[item][i][0].isdigit() and app.splitPlayersCards[item][i][0]: 
                value = int(app.splitPlayersCards[item][i][0])
            elif app.splitPlayersCards[item][i][0] == 'A': 
                value = 11
            app.splitPlayersCounts[item] += value

    for item in app.playersCards:
        for i in range(len(app.playersCards[item])):
            if (app.playersCards[item][i][0:2] == '10' or 
                            app.playersCards[item][i][0] == 'J' or 
                            app.playersCards[item][i][0]== 'Q' or 
                            app.playersCards[item][i][0] == 'K'): 
                            value = 10
            elif app.playersCards[item][i][0].isdigit() and app.playersCards[item][i][0]: 
                value = int(app.playersCards[item][i][0])
            elif app.playersCards[item][i][0] == 'A': 
                value = 11
            
            app.playersCounts[item] += value
            if item == "Dealer" and i == 0: 
                app.dealerUpcard = value 

def checkForNaturals(app):

    for i in app.playersCounts:
        if app.playersCounts[i] == 22:
            app.playersCounts[i] -= 10

    insuranceBet = []
    uc = app.playersCards["Dealer"][0][0]
    if uc == "A":
        for i in range(app.numberOfUsers):
            if i == 0: player = f"{app.username}"
            else: player = f"Guest {i}"
            
            insurance = app.getUserInput(f"Does {player} want to make an Insurance Bet? (yes or no)")
            if insurance == "yes":
                insuranceBet += [i]
                app.bplayersScores[f"Player {i+1}"] -= (app.bet[f"Player {i+1}"]//2)
            else:
                pass

    if app.playersCounts["Dealer"] == 21:

        for item in insuranceBet:
            app.bplayersScores[f"Player {1+item}"] += app.bet[f"Player {1+item}"]

        for i in range(app.bplayers):
            if app.playersCounts[f"Player {i+1}"] != 21:
                returnTurnOver(app, i, "None")
            else:
                app.bplayersScores[f"Player {i+1}"] += app.bet[f"Player {i+1}"]
                app.bet[f"Player {i+1}"] = 0

        for i in range(app.numberOfUsers):
            if i == 0: player = f"{app.username}"
            else: player = f"Guest {i}"
            try:
                app.bet[f"Player {i+1}"] = int(app.getUserInput((f'Betting Amount {player}')))
            except:
                app.bet[f"Player {i+1}"] = 10
            app.bplayersScores[f"Player {i+1}"] -= app.bet[f"Player {i+1}"]

        for i in range(app.numberOfUsers, app.bplayers):
            app.bet[f"Player {i + 1}"] = findBet(app,i)
            app.bplayersScores[f"Player {i + 1}"] -= app.bet[f"Player {i + 1}"]

        returnTurnOver(app, "Dealer", "21")
        blackjackNewRound(app)
    else:
        for i in range(app.bplayers):
            if app.playersCounts[f"Player {i+1}"] == 21: 
                app.bplayersScores[f"Player {i+1}"] += app.bet[f"Player {i+1}"]*(2.5)
                app.bet[f"Player {i+1}"] = 0
                returnTurnOver(app, i, "21")


            if app.playersCounts[f"Player {i+1}"] == 22:
                rest = app.playersCards[f"Player {i + 1}"][0][1:]
                app.playersCards[f"Player {i + 1}"][0] = "1" + rest
                app.playersCounts[f"Player {i+1}"] -= 10
                assignPlayerCounts(app)

        app.checkedForNaturals = True

def beginRound(app):
    time.sleep(0.2)
    if app.playersTurn in range(app.numberOfUsers):
            
            i = app.playersTurn

            if app.variant == True and (app.newCardLoc[f"Player {1+i}"][0][0] == "None" or app.newCardLoc[f"Player {1+i}"][0][0] == "21"):
                app.splitTurn = 1

            elif app.variant == True and app.splitTurn == 1 and (app.newCardLoc[f"Player {1+i}"][1][0] == "None" or app.newCardLoc[f"Player {1+i}"][1][0] == "21"):
                app.splitTurn = 0
                app.playersTurn = 1

            elif app.variant == False and (app.cardLoc[i+app.bplayers+1][0] == "None" or app.cardLoc[i+app.bplayers+1][0] == "21"):
                app.playersTurn += 1

            app.buttonsOn = True
            if app.variant == True: 
                app.split = True
            
    else:
        app.buttonsOn = False
    
    if app.playersTurn not in range(app.numberOfUsers) and app.playersTurn < app.bplayers:
        if app.split == True and app.splitTurn == 0:
            count = app.splitPlayersCounts[f"Player {app.playersTurn + 1}"]
        else:
            count = app.playersCounts[f"Player {app.playersTurn + 1}"]
        hand = (count, app.dealerUpcard)
        if hand[0] == 22:
            action = "sp"
        else:
            action = app.policy[hand][0]
        if action == "h": 
            hit(app, app.playersTurn)
        elif action == "s":
            if app.split == True and app.splitTurn == 0 and app.variable == True:
                app.splitTurn = 1
                app.hits = 0
                if app.variant == True: app.hits += 1 
                app.variable = False
            else:
                app.splitTurn = 0
                app.playersTurn += 1
                app.hits = 1
                app.variable = True
                if app.variant == False: 
                    app.split = False
        elif action == "dd":
            if (app.playersCounts[f"Player {app.playersTurn+1}"] >= 9 and 
                app.playersCounts[f"Player {app.playersTurn+1}"] <= 11 and
                len(app.playersCards[f"Player {app.playersTurn+1}"]) == 2):
                dd(app, app.playersTurn)
            else:
                app.storage += [app.policy[hand]]
                app.policy[hand] = [app.policy[hand][1]] + [app.policy[hand][0]]
        elif action == "sp":
            if (len(app.playersCards[f"Player {app.playersTurn+1}"]) == 2 and
                (app.playersCards[f"Player {app.playersTurn+1}"][0][0] == 
                app.playersCards[f"Player {app.playersTurn+1}"][1][0]) and app.variant == False):
                split(app, app.playersTurn)
            else:
                app.storage += [app.policy[hand]]
                app.policy[hand] = [app.policy[hand][1]] + [app.policy[hand][0]]

    elif app.playersTurn == app.bplayers:
        app.hits = 1
        app.playersTurn += 1

    elif app.playersTurn == app.bplayers + 1:
        dealerPlay(app)


def dealerPlay(app):

    for item in app.storage:
        item = [item[1]] + [item[0]]

    image = app.cardsUsed[app.bplayers*2 + 1][1]
    app.cardBack = image

    if app.playersCounts["Dealer"] == 21:
        returnTurnOver(app, "Dealer", "21")
        app.playersTurn += 1

    elif app.playersCounts["Dealer"] > 21:
        for i in range(len(app.playersCards["Dealer"])):
            if app.playersCards["Dealer"][i][0] == "A":
                rest = app.playersCards["Dealer"][i][1:]
                app.playersCards["Dealer"][i] = "1" + rest
                assignPlayerCounts(app)  

    if app.playersCounts["Dealer"] > 21:
        returnTurnOver(app, "Dealer", "None")

        for i in range(app.bplayers):
            if app.playersCounts[f"Player {i+1}"] <= 21:
                app.bplayersScores[f"Player {i+1}"] += app.bet[f"Player {i+1}"]*(2)   

            if app.splitPlayersCounts[f"Player {i+1}"] <= 21 and app.splitPlayersCounts[f"Player {i+1}"] != 0: 
                app.bplayersScores[f"Player {i+1}"] += app.bet[f"Player {i+1}"]*(2)  

        app.playersTurn += 1 

    elif app.playersCounts["Dealer"] >= 17:
            
        for i in range(app.bplayers):
            if (app.playersCounts[f"Player {i+1}"] > app.playersCounts["Dealer"] and
                app.playersCounts[f"Player {i+1}"] <= 21):
                app.bplayersScores[f"Player {i+1}"] += (app.bet[f"Player {i+1}"]*(2))

            if (app.playersCounts[f"Player {i+1}"] == app.playersCounts["Dealer"] and
                app.playersCounts[f"Player {i+1}"] <= 21):
                app.bplayersScores[f"Player {i+1}"] += app.bet[f"Player {i+1}"]

            if (app.splitPlayersCounts[f"Player {i+1}"] > app.playersCounts["Dealer"] and
                app.splitPlayersCounts[f"Player {i+1}"] <= 21 and app.splitPlayersCounts[f"Player {i+1}"] != 0):
                app.bplayersScores[f"Player {i+1}"] += (app.bet[f"Player {i+1}"]*(2))

            if (app.splitPlayersCounts[f"Player {i+1}"] == app.playersCounts["Dealer"] and
                app.splitPlayersCounts[f"Player {i+1}"] <= 21 and app.splitPlayersCounts[f"Player {i+1}"] != 0):
                app.bplayersScores[f"Player {i+1}"] += app.bet[f"Player {i+1}"]

        app.playersTurn += 1 


    else:
        origLoc = app.cardLoc[app.bplayers*2 + 1]
        newLoc = [origLoc[1] + 10*(app.hits), origLoc[2] + 10*(app.hits)]
        app.newCardLoc["Dealer"].append(newLoc)
    
        card = (random.choice(app.cardsHave))
        app.cardsHave.remove(card)
        app.cardsUsed.append(card)
        app.playersImages["Dealer"] += [app.cardsUsed[-1][-1]]
        app.playersCards["Dealer"] += [app.cardsUsed[-1][0]]
        assignPlayerCounts(app)  
        app.hits += 1  

def split(app, player):
    if (len(app.playersCards[f"Player {player+1}"]) == 2 and
        (app.playersCards[f"Player {player+1}"][0][0] == 
        app.playersCards[f"Player {player+1}"][1][0])) or app.variant == True:

            app.split = True 
        
            origLoc = app.cardLoc[player]
            newLoc = (origLoc[0] - 70, origLoc[1] + 10)
            app.cardLoc[player] = newLoc

            app.bplayersScores[f"Player {player+1}"] -= app.bet[f"Player {player+1}"]

            app.splitPlayersCards[f"Player {player+1}"] += [app.playersCards[f"Player {player+1}"].pop(1)] 
            assignPlayerCounts(app)


def dd(app, player):
    if (app.playersCounts[f"Player {player+1}"] >= 9 and 
        app.playersCounts[f"Player {player+1}"] <= 11 and
        len(app.playersCards[f"Player {player+1}"]) == 2):

        app.bplayersScores[f"Player {player+1}"] -= app.bet[f"Player {player+1}"]
        app.bet[f"Player {player + 1}"] *= 2
        
        hit(app, player)
        app.buttonsOn = False
        
        app.playersTurn += 1

        app.hits = 1

def hit(app, player):
    if app.split == True and app.splitTurn == 0:
        i = player + app.bplayers + 1
        j = 0
        if app.variant == True and app.startVariantRound == True: j = 1

    else:
        i = player
        j = 1

    origLoc = app.cardLoc[i]
    newLoc = [origLoc[0] + 10*(app.hits+j), origLoc[1] + 10*(app.hits+j)]
    i = player
    app.newCardLoc[f"Player {i+1}"].append(newLoc)
    

    card = (random.choice(app.cardsHave))
    app.cardsHave.remove(card)
    app.cardsUsed.append(card)

    if app.split == True and app.splitTurn == 0:
        app.splitPlayersCards[f"Player {player + 1}"] += [app.cardsUsed[-1][0]]

    else:
        app.playersCards[f"Player {player + 1}"] += [app.cardsUsed[-1][0]]

    app.playersImages[f"Player {player + 1}"] += [app.cardsUsed[-1][-1]]
    assignPlayerCounts(app)

    if app.split == True and app.splitTurn == 0:
        if app.splitPlayersCounts[f"Player {player + 1}"] > 21:
            # check for aces
            for i in range(len(app.splitPlayersCards[f"Player {player + 1}"])):
                if app.splitPlayersCards[f"Player {player + 1}"][i][0] == "A":
                    rest = app.splitPlayersCards[f"Player {player + 1}"][i][1:]
                    app.splitPlayersCards[f"Player {player + 1}"][i] = "1" + rest
                    assignPlayerCounts(app)  

        if app.splitPlayersCounts[f"Player {player + 1}"] > 21:
                returnTurnOver(app, player, "None")
                app.hits = 0
                if app.variant == True: app.hits += 1
                app.splitTurn += 1

        elif app.splitPlayersCounts[f"Player {player + 1}"] == 21 and app.splitVariant == False:
            returnTurnOver(app, player, "21")
            app.hits = 0
            if app.variant == True: app.hits += 1
            app.splitTurn += 1
        
        else:
            app.hits += 1

    else:    
        if app.playersCounts[f"Player {player + 1}"] > 21:
            # check for aces
            for i in range(len(app.playersCards[f"Player {player + 1}"])):
                if app.playersCards[f"Player {player + 1}"][i][0] == "A":
                    rest = app.playersCards[f"Player {player + 1}"][i][1:]
                    app.playersCards[f"Player {player + 1}"][i] = "1" + rest
                    assignPlayerCounts(app)  

        if app.playersCounts[f"Player {player + 1}"] > 21:
                returnTurnOver(app, player, "None")
                app.buttonsOn = False
                app.hits = 1
                app.playersTurn += 1
                app.splitTurn = 0
                if app.variant == False:
                    app.split = False

        elif app.playersCounts[f"Player {player + 1}"] == 21 and app.splitVariant == False:
            returnTurnOver(app, player, "21")
            app.buttonsOn = False
            app.hits = 1
            app.playersTurn += 1
            app.splitTurn = 0
            if app.variant == False:
                app.split = False
        
        else:
            app.hits += 1

def returnTurnOver(app, player, message):
    if player == "Dealer":
        if len(app.newCardLoc["Dealer"]) == 0:
            app.cardLoc[app.bplayers*2+1] = [message] + app.cardLoc[app.bplayers*2+1]
        else:
            app.newCardLoc["Dealer"][-1] = [message] + app.newCardLoc["Dealer"][-1]
    else:
        if len(app.newCardLoc[f"Player {player + 1}"]) == 0:
            app.cardLoc[player+app.bplayers+1] = [message] + app.cardLoc[player+app.bplayers+1]
        else:
            app.newCardLoc[f"Player {player + 1}"][-1] = [message] + app.newCardLoc[f"Player {player + 1}"][-1]

def findBet(app, i):
    try:
        count = calculateBJCardCountWrapper(app)/app.bdecks
    except: count = 0

    bet = int((count + 1)*
            (app.bplayersScores[f"Player {i + 1}"]//50)*
            (app.riskLevels[f"Player {i + 1}"]))
    if bet < 10:
        bet = 10
    return bet


def blackjackMode_mousePressed(app, event):
    (x, y) = (event.x, event.y)

    (sethowx1, sethowx2) = (int(app.width*(1/20)), int(app.width*(4/20)))
    (sety1, sety2) = (int(app.height*(2/20)), int(app.height*(3/20)))
    (howy1, howy2) = (int(app.height*(1/5)), int(app.height*(1/4)))
    
    (buttonx1, buttonx2) = (int(app.width*(19/20)-35), int(app.width*(19/20)+35))
    (standy1, standy2) = (int(app.height*(9/20)-35), int(app.height*(9/20)+35))
    (hity1, hity2) = (int(app.height*(12/20)-35), int(app.height*(12/20)+35))
    (splity1, splity2) = (int(app.height*(15/20)-35), int(app.height*(15/20)+35))
    (DDy1, DDy2) = (int(app.height*(18/20)-35), int(app.height*(18/20)+35))

    if x in range(sethowx1, sethowx2):
        if y in range(sety1, sety2):
            app.mode = "blackjackSettingsMode"

        elif y in range(howy1, howy2):
            app.mode = "howToBlackjackMode"
    
    elif app.buttonsOn == True and x in range(buttonx1, buttonx2):

        if y in range(standy1, standy2):
            if app.split == True and app.splitTurn == 0 and app.variable == True:
                app.splitTurn = 1
                app.hits = 0
                app.variable = False
                if app.variant == True: 
                    app.hits = 1
            else:
                app.playersTurn += 1
                app.variable = True 
                app.splitTurn = 0
                app.hits = 1
                if app.variant == False: 
                    app.split = False


        elif y in range(hity1, hity2):
            hit(app, app.playersTurn)

        elif y in range(splity1, splity2):
            if app.variant == False:
                split(app, app.playersTurn)

        elif y in range(DDy1, DDy2):
            if app.split == False:       #cannot dd after a split
                dd(app, app.playersTurn)
    
    if x in range(int(app.width*(16/20)), int(app.width*(19/20))):
        if y in range(int(app.height*(1/10)), int(app.height*(3/20))):
            if app.showRecs == True:
                app.showRecs = False
            else:
                app.showRecs = True

def blackjackMode_keyPressed(app,event):
    if event.key == "Enter":
        for i in range(app.numberOfUsers):
            if i == 0: player = f"{app.username}"
            else: player = f"Guest {i}"
            try:
                app.bet[f"Player {i+1}"] = int(app.getUserInput(f'Betting Amount {player}'))
            except:
                app.bet[f"Player {i+1}"] = 10

            if app.bet[f"Player {i+1}"] < 0:
                app.bet[f"Player {i+1}"] = 10
            elif app.bet[f"Player {i+1}"] > app.bplayersScores[f"Player {i+1}"]:
                app.bet[f"Player {i+1}"] = copy.deepcopy(app.bplayersScores[f"Player {i+1}"])
            
            app.bplayersScores[f"Player {i+1}"] -= app.bet[f"Player {i+1}"]

        for i in range(app.numberOfUsers, app.bplayers):
            app.bet[f"Player {i + 1}"] = findBet(app,i)
            app.bplayersScores[f"Player {i + 1}"] -= app.bet[f"Player {i + 1}"]

        app.startGame = True
        
    elif event.key == 'r':
        blackjackReset(app)

    elif event.key == "Backspace":
        app.mode = "homeScreenMode"
        blackjackReset(app)

    elif event.key == "Space":
        if app.startGame == True:
            for i in range(app.numberOfUsers):
                if i == 0: player = f"{app.username}"
                else: player = f"Guest {i}"
                try:
                    app.bet[f"Player {i+1}"] = int(app.getUserInput((f'Betting Amount {player}')))
                except:
                    app.bet[f"Player {i+1}"] = 10

                if app.bet[f"Player {i+1}"] < 0:
                    app.bet[f"Player {i+1}"] = 10
                elif app.bet[f"Player {i+1}"] > app.bplayersScores[f"Player {i+1}"]:
                    app.bet[f"Player {i+1}"] = copy.deepcopy(app.bplayersScores[f"Player {i+1}"])
                app.bplayersScores[f"Player {i+1}"] -= app.bet[f"Player {i+1}"]

            for i in range(app.numberOfUsers, app.bplayers):
                app.bet[f"Player {i + 1}"] = findBet(app,i)
                app.bplayersScores[f"Player {i + 1}"] -= app.bet[f"Player {i + 1}"]  
          

            blackjackNewRound(app)

###############################################################################
# Settings: Blackjack
###############################################################################

def blackjackSettingsMode_redrawAll(app,canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_text(80, app.height-30, text = "<- Backspace", 
                        fill = "darkred", font = "courier 15 bold")
    canvas.create_text(app.width/2, app.height*(3/20),
                        text = "SETTINGS",
                        fill = "white", font = "courier 30")

    canvas.create_text(app.width/2, app.height*(12/40), 
                        text = "Number of Decks: ", 
                        fill = "darkred", font = "courier 20 italic", 
                        anchor = "ne")
    canvas.create_rectangle(app.width*(21/40), app.height*(11/40), 
                        app.width*(23/40), app.height*(15/40),
                        fill = "black", outline = "white", width = 1)
    canvas.create_text(app.width*(11/20), app.height*(13/40),
                        text = f"{app.bdecks}", fill = "darkred",
                        font = "courier 30 bold")
    
    canvas.create_text(app.width/2, app.height*(20/40), 
                        text = "Number of Players: ",
                        fill = "white", font = "courier 20 italic", 
                        anchor = "ne")
    canvas.create_rectangle(app.width*(21/40), app.height*(19/40),
                        app.width*(23/40), app.height*(23/40),
                        fill = "black", outline = "white", width = 1)
    canvas.create_text(app.width*(11/20), app.height*(21/40),
                        text = f"{app.bplayers}", fill = "white",
                        font = "courier 30 bold")

    canvas.create_text(app.width/2, app.height*(28/40),
                        text = "Interesting Variant?: ",
                        fill = "darkred", font = "courier 20 italic",
                        anchor = "ne")
    canvas.create_rectangle(app.width*(20.8/40), app.height*(27/40),
                            app.width*(23.2/40), app.height*(31/40),
                            fill = "black", outline = "white", width = 1)
    if app.variant == False: setting = 'No'
    else: setting = 'Yes'
    canvas.create_text(app.width*(22/40), app.height*(29/40), 
                        text = setting, fill = "darkred",
                        font = "courier 30 bold")
    canvas.create_text(app.width*(34/40), app.height*(1/2),
                        text = "Number of Users: ",
                        fill = "darkred", font = "courier 20 italic",
                        anchor = "ne")
    canvas.create_rectangle(app.width*(35/40), app.height*(19/40),
                            app.width*(37/40), app.height*(23/40),
                            fill = "black", outline = "white", width = 1)
    canvas.create_text(app.width*(36/40), app.height*(21/40),
                        text = f"{app.numberOfUsers}", fill = "darkred",
                        font = "courier 30 bold")
    
def blackjackSettingsMode_keyPressed(app, event):
    if event.key == "Backspace":
        app.mode = "blackjackMode"

def blackjackSettingsMode_mousePressed(app, event):
    (x, y) = (event.x, event.y)
    (x1, x2) = (int(app.width*(21/40)), int(app.width*(24/40)))
    (py1, py2) = (int(app.height*(19/40)), int(app.height*(23/40)))
    (dy1, dy2) = (int(app.height*(11/40)), int(app.height*(15/40)))
    (vy1, vy2) = (int(app.height*(27/40)), int(app.height*(31/40)))

    (ux1, ux2) = (int(app.width*(35/40)), int(app.width*(37/40)))
    (uy1, uy2) = (int(app.height*(19/40)), int(app.height*(23/40)))


    if x in range(ux1, ux2) and y in range(uy1, uy2):
        try:
            app.numberOfUsers = int(app.getUserInput("How many users? (1, 2, 3, 4, or 6)?"))
        except:
            app.numberOfUsers = 1
        if app.numberOfUsers >= 5:
            app.numberOfUsers = 6
        blackjackReset(app)


    elif x in range(x1, x2):

        if y in range(py1, py2):
            try:
                app.bplayers = int(app.getUserInput("How many players (1, 2, 3, 4, or 6)?"))
            except:
                app.bplayers = 2
            if app.bplayers >= 5:
                app.bplayers = 6
            blackjackReset(app)
            
        elif y in range(dy1, dy2):
            try:
                app.bdecks = int(app.getUserInput("How many decks?"))
            except:
                app.bdecks = 5
            blackjackReset(app)

        elif y in range(vy1, vy2):
            answer = app.getUserInput("yes or no")
            if answer == "yes":
                app.variant = True
            else:
                app.variant = False
            blackjackReset(app)

###############################################################################
# How to: blackjack
###############################################################################

def howToBlackjackMode_redrawAll(app,canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "darkgray")
    canvas.create_text(80, app.height-30, text = "<- Backspace", 
                        fill = "darkred", font = "courier 15 bold")
    canvas.create_text(app.width/2, app.height/15, 
                        text = "How To Play Blackjack:", 
                        fill = "black", font = "courier 30 bold")
    with open('Instructions for blackjack game.txt', 'r') as f:
        file = f.read() 
    
    canvas.create_text(app.width/2, app.height/2, text = file, font = "courier 10")

def howToBlackjackMode_keyPressed(app,event):
    if event.key == "Backspace":
        app.mode = "blackjackMode"

###############################################################################
# Counting Cards
###############################################################################
def startCountingCards(app):
    app.cardsPassed = 5
    app.cdecks = 3
    app.speed = 1
    resetCountingCards(app)
    
def resetCountingCards(app):
    app.conRightGuesses = 0
    app.lenList = []
    app.ccount = 0
    app.ccardsUsed = []
    app.startCounting = False
    app.pauseCounting = False    
    app.timerDelay = 0
    app.getGuess = True 
    app.guess = ""
    createCardsCounting(app)

def calculateCardCountWrapper(app):
    L = copy.deepcopy(app.ccardsUsed)
    a = len(app.ccardsUsed) + 1
    return calculateCount(L, a, count = 1)

def calculateBJCardCountWrapper(app):
    L = copy.deepcopy(app.cardsUsed)
    a = len(app.cardsUsed) + 1
    return calculateCount(L, a, count = 1)

def calculateCount(L, a, count = 1):
    if a == count:
        return 0
    else:
        card = L[0][0][0]
        for i in ['1', 'J', 'Q', 'K', 'A']:
            if card == i:
                return -1 + calculateCount(L[1:], a, count + 1)
        for i in ['2', '3', '4', '5', '6']:
            if card == i:
                return 1 + calculateCount(L[1:], a, count + 1)
        return calculateCount(L[1:], a, count + 1)

def countCardsMode_redrawAll(app,canvas):

    canvas.create_rectangle(0,0,app.width,app.height,fill="black")
    canvas.create_text(80, app.height-30, text = "<- Backspace", 
                        fill = "darkred", font = "courier 15 bold")
    canvas.create_rectangle(app.width*(3/4), app.height*(1/10), 
                            app.width*(19/20), app.height*(3/20), 
                            fill = "lightgray")

    canvas.create_text(app.width*(17/20), app.height*(2.5/20), 
                    text = "SETTINGS", fill = "black", 
                    font = "courier 15 bold")

    canvas.create_rectangle(app.width*(3/4), app.height*(1/5), 
                            app.width*(19/20), app.height*(1/4), 
                            fill = "lightgray")
    canvas.create_text(app.width*(17/20), app.height*(4.5/20), 
                    text = "HOW TO COUNT", fill = "black", 
                    font = "courier 15 bold")

    canvas.create_rectangle(app.width*(3/4), app.height*(3/10),
                            app.width*(19/20), app.height*(7/20),
                            fill = "lightgray")
    canvas.create_text(app.width*(17/20), app.height*(6.5/20),
                    text = "PROGRESS", fill = "black",
                    font = "courier 15 bold")


    if app.startCounting == False:
        canvas.create_rectangle(app.width*(1/3), app.height*(1/3),
                                app.width*(2/3), app.height*(2/3),
                                fill = "darkgray", outline = "white", width = 4)
        canvas.create_text(app.width/2-20, app.height/2, 
                            text = "    Press Enter\n to Start Counting",
                            fill = "white", font = "courier 25 bold")

    if app.startCounting == True:
        try:
            cardImage = app.ccardsUsed[-1][-1]
            canvas.create_image(app.width/2, app.height/2, 
                                image = ImageTk.PhotoImage(cardImage))
        except: pass

        if app.pauseCounting == True and app.getGuess == False:
            canvas.create_text(app.width*(17/20), app.height*(9/20),
                                text = f"{app.guess}",
                                fill = "darkred", font = "courier 20 bold")
            canvas.create_text(app.width*(17/20), app.height*(11/20),
                                text = f" Your current\n count is: {app.ccount}.",
                                fill = "white", font = "courier 20 bold")
            canvas.create_text(app.width*(3.5/20), app.height*(8/20),
                                text = " Press the space bar\n to resume your\n current count.",
                                fill = "darkred", font = "courier 20 bold") 
            trueCount = str(app.ccount/app.cdecks)[0:4]
            canvas.create_text(app.width*(3.5/20), app.height*(11/20),
                                text = f"Your TRUE COUNT\nis {trueCount}",
                                fill = "white", font = "courier 20 bold")              

def countCardsMode_timerFired(app):
    keepTrackOfProgress(app)
    if app.startCounting == True and app.pauseCounting == False:
        if (len(app.ccardsUsed) != 0 and len(app.ccardsUsed) not in app.lenList 
            and len(app.ccardsUsed) % app.cardsPassed == 0):
            app.lenList.append(len(app.ccardsUsed))
            app.pauseCounting = True

        else:
            app.timerDelay = 3000//app.speed
            card = random.choice(app.ccardsHave)
            if len(app.ccardsUsed) > 0 and card == app.ccardsUsed[-1]:
                card = random.choice(app.ccardsHave)
            app.ccardsUsed.append(card)
            app.ccardsHave.remove(card)

    if app.pauseCounting == True:
        app.ccount = calculateCardCountWrapper(app)
        if app.getGuess == True:
            try:
                guess = app.getUserInput("What is The Count?")
            except:
                guess = 0
            app.getGuess = False
        if app.getGuess == False:
            try:
                if guess == f"{app.ccount}":
                    app.guess = "You are correct!"
                    app.conRightGuesses += 1
                else:
                    app.guess = "That is incorrect."
                    app.conRightGuesses = 0
            except: pass

def keepTrackOfProgress(app):
    with open('usernameData.txt', 'r') as f:
        file = f.read()

    with open('usernameData.txt', 'r') as g:
        fileData = g.readlines()

    username = app.username   #app.username
    speed = app.speed   #str(app.speed)
    rightGuesses = app.conRightGuesses   #app. consecutive number of right guesses for that speed (will reset everytime the user is wrong)
    cardsPassed = app.cardsPassed     # app.cardsPassed
    newList = []
    app.graph = []      #will be app.graph and will be used to construct a graph when the user clicks for one

    for line in fileData:
        if username in line:
            a = (line.split("-"))
            b = a.index(username)
            a = a[b:b+11]
            orig = str("-".join(a))
            for item in a:
                c = item.split(",")
                if c[0] == str(speed):
                    if int(c[1]) < (rightGuesses*cardsPassed):
                        c[1] = str(rightGuesses*cardsPassed)
                if c[0].isdigit():
                    e = [int(c[0]), int(c[1])]
                    app.graph.append(e)   #will be app.graph
                c = ",".join(c)
                newList.append(c)
            newData = str("-".join(newList))

            with open('usernameData.txt', 'w') as f:
                f.write(file.replace(orig, newData))
        else:
            with open('usernameData.txt', 'a') as f:
                        newData = f"-{username}-1,0-2,0-3,0-4,0-5,0-6,0-7,0-8,0-9,0-10,0"
                        f.write(newData)


def countCardsMode_mousePressed(app, event):
    (x, y) = (event.x, event.y)
    (sethowx1, sethowx2) = (int(app.width*(3/4)), int(app.width*(19/20)))
    (sety1, sety2) = (int(app.height*(2/20)), int(app.height*(3/20)))
    (howy1, howy2) = (int(app.height*(1/5)), int(app.height*(1/4)))
    (py1, py2) = (int(app.height*(6/20)), int(app.height*(7/20)))
    
    if x in range(sethowx1, sethowx2):
        if y in range(sety1, sety2):
            app.mode = "countCardsSettingsMode"
            resetCountingCards(app)
        elif y in range(howy1, howy2):
            app.mode = "howToCountCardsMode"
            resetCountingCards(app)
        elif y in range(py1, py2):
            app.mode = "progressMode"

def countCardsMode_keyPressed(app, event):
    if event.key == "Backspace":
        app.mode = "homeScreenMode"
        startCountingCards(app)
    
    if event.key == "Enter":
        app.startCounting = True

    if event.key == "Space":
        app.pauseCounting = False
        app.getGuess = True
        app.guess = ""

###############################################################################
# Progress
###############################################################################

def progressMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_text(80, app.height-30, text = "<- Backspace", 
                        fill = "darkred", font = "courier 15 bold")
    canvas.create_rectangle(app.width*(3/20), app.height*(2/20),
                            app.width*(17/20), app.height*(18/20),
                            fill = "lightgray")
    canvas.create_line(app.width*(4/20), app.height*(3/20),
                        app.width*(4/20), app.height*(17/20),
                        fill = "black", width = 3)
    canvas.create_line(app.width*(4/20), app.height*(17/20),
                        app.width*(16/20), app.height*(17/20),
                        fill = "black", width = 3)

    canvas.create_rectangle(app.width*(12/40), app.height*(0.5/40),
                            app.width*(28/40), app.height*(3.5/40),
                            fill = "darkgray", outline = "white", width = 2)
    canvas.create_text(app.width*(1/2), app.height*(2/40),
                        text = f"{app.username}'s Counting Progress", fill = "black", 
                        font = "courier 15 bold")

    canvas.create_rectangle(app.width*(15/40), app.height*(36.5/40),
                            app.width*(25/40), app.height*(39.5/40),
                            fill = "darkgray", outline = "white", width = 2)
    canvas.create_text(app.width*(1/2), app.height*(38/40),
                        text = "Speed", fill = "black", font = "courier 20 bold")

    canvas.create_rectangle(app.width*(0.5/40), app.height*(15/40),
                            app.width*(5.5/40), app.height*(25/40),
                            fill = "darkgray", outline = "white", width = 2)
    canvas.create_text(app.width*(3/40), app.height*(1/2),
                        text = "  Highest #\n Consecutive\nRight Guesses\n     x\nCards Passed", 
                        font = "courier 14 bold")

    yaxisStart = list(range(0,50,5))
    yaxisS = list(range(0,52))
    yaxisEnd = list(range(52, 322, 15))
    yaxisE = list(range(52,307))
    y = 17.5
    for item in yaxisStart:
        y -= 0.5
        canvas.create_text(app.width*(3.5/20), app.height*(y/20), 
                            text = f"{item}", fill = "black", 
                            font = "courier 10 bold")
        canvas.create_text(app.width*(4/20), app.height*(y/20), 
                            text = "-", fill = "black", 
                            font = "courier 10 bold")
    for item in yaxisEnd:
        y -= 0.5
        canvas.create_text(app.width*(3.5/20), app.height*(y/20), 
                            text = f"{item}", fill = "black", 
                            font = "courier 10 bold")
        canvas.create_text(app.width*(4/20), app.height*(y/20), 
                            text = "-", fill = "black", 
                            font = "courier 10 bold")

    xaxis = list(range(0,11))
    x = 3
    for item in xaxis:
        x += 1
        canvas.create_text(app.width*(x/20), app.height*(17.5/20),
                            text = f"{item}", fill = "black", 
                            font = "courier 10 bold")
    s = 3.5
    for i in range(len(app.graph)):
        s += 1
        value = int(app.graph[i][1])
        if value in yaxisS:
            y1 = app.height*((17+(-0.5)*(value/5))/20)   
        else:
            y1 = app.height*((12+(-0.5)*((value-52)/15))/20) 

        x1 = app.width*(s/20)
        x2 = app.width*((s+1)/20)
        y2 = app.height*(17/20)
        canvas.create_rectangle(x1, y1, x2, y2, 
            fill = "darkred", outline = "black", width = 2)
    

def progressMode_keyPressed(app, event):
    if event.key == "Backspace":
        app.mode = "countCardsMode"


###############################################################################
# How to: Count Cards
###############################################################################

def howToCountCardsMode_redrawAll(app,canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "darkgray")
    canvas.create_text(80, app.height-30, text = "<- Backspace", 
                        fill = "darkred", font = "courier 15 bold")
    canvas.create_text(app.width/2, app.height/15, 
                        text = "How To Count Cards:", 
                        fill = "black", font = "courier 30 bold")
    
    with open('Instructions for Counting Cards.txt', 'r') as f:
        file = f.read() 
    
    canvas.create_text(app.width/2, app.height/2, text = file, font = "courier 12")

def howToCountCardsMode_keyPressed(app,event):
    if event.key == "Backspace":
        app.mode = "countCardsMode"

###############################################################################
# Settings: Count Cards
###############################################################################
# have user input number of decks, speed, after how many cardsHave to insert an answer

def countCardsSettingsMode_redrawAll(app,canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_text(80, app.height-30, text = "<- Backspace", 
                        fill = "darkred", font = "courier 15 bold")
    canvas.create_text(app.width/2, app.height*(3/20),
                        text = "SETTINGS",
                        fill = "white", font = "courier 30")

    canvas.create_text(app.width/2, app.height*(6/20), 
                        text = "Number of Decks: ", 
                        fill = "darkred", font = "courier 20 italic", 
                        anchor = "ne")

    canvas.create_rectangle(app.width*(21/40), app.height*(11/40), 
                        app.width*(23/40), app.height*(15/40),
                        fill = "black", outline = "white", width = 1)
    canvas.create_text(app.width*(11/20), app.height*(13/40),
                        text = f"{app.cdecks}", fill = "darkred",
                        font = "courier 30 bold")

    canvas.create_text(app.width/2, app.height*(9/20), 
                        text = "Speed of play: ",
                        fill = "white", font = "courier 20 italic", 
                        anchor = "ne")
    canvas.create_rectangle(app.width*(21/40), app.height*(17.5/40),
                        app.width*(23/40), app.height*(21.5/40),
                        fill = "black", outline = "white", width = 1)
    canvas.create_text(app.width*(11/20), app.height*(19.5/40),
                        text = f"{app.speed}", fill = "white",
                        font = "courier 30 bold")
    
    canvas.create_text(app.width/2, app.height*(12/20), 
                        text = "Guess Answer After\n This Many Cards: ",
                        fill = "darkred", font = "courier 20 italic", 
                        anchor = "ne")
    canvas.create_rectangle(app.width*(21/40), app.height*(24/40),
                        app.width*(23/40), app.height*(28/40),
                        fill = "black", outline = "white", width = 1)
    canvas.create_text(app.width*(11/20), app.height*(26/40),
                        text = f"{app.cardsPassed}", fill = "white",
                        font = "courier 30 bold")

def countCardsSettingsMode_keyPressed(app, event):
    if event.key == "Backspace":
        app.mode = "countCardsMode"

def countCardsSettingsMode_mousePressed(app, event):
    (x, y) = (event.x, event.y)
    (x1, x2) = (int(app.width*(21/40)), int(app.width*(23/40)))
    (dy1, dy2) = (int(app.height*(11/40)), int(app.height*(15/40)))
    (sy1, sy2) = (int(app.height*(17.5/40)), int(app.height*(21.5/40)))
    (cy1, cy2) = (int(app.height*(24/40)), int(app.height*(28/40)))

    if x in range(x1, x2):
        if y in range(dy1, dy2):
            try:
                app.cdecks = int(app.getUserInput("How many decks?"))
            except:
                app.cdecks = 1
            resetCountingCards(app)

        elif y in range(sy1, sy2):
            try:
                app.speed = int(app.getUserInput("How fast on a scale of 1 to 10?"))
            except:
                app.speed = 1
            resetCountingCards(app)

        elif y in range(cy1, cy2):
            try:
                app.cardsPassed = int(app.getUserInput("How many cards would you like to pass before guessing?"))
            except:
                app.cardsPassed = 5
            resetCountingCards(app)

###############################################################################
# Main App
###############################################################################

def appStarted(app):

    # Main screen
    app.mode = "mainScreenMode"
    app.username = ""

    # images on home screen
    app.heart = app.scaleImage(app.loadImage("Main Screen Heart.png"),4/5)
    app.diamond = app.scaleImage(app.loadImage("Main Screen Diamond.png"),4/5)

    startBlackjack(app)
    startCountingCards(app)

    gameMonteCarlo(app)


def createCards(app):
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['H', 'D', 'S', 'C']
    app.cardsHave = []
    for value in values:
        for suit in suits:
            app.cardsHave.append((value + suit, (app.scaleImage(app.loadImage(value + suit + '.png'), 1/5))))
    app.cardsHave = app.cardsHave*app.bdecks

def createCardsCounting(app):
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['H', 'D', 'S', 'C']
    app.ccardsHave = []
    for value in values:
        for suit in suits:
            app.ccardsHave.append((value + suit, app.loadImage(value + suit + '.png')))
    app.ccardsHave = app.ccardsHave*app.cdecks

def gameMonteCarlo(app):
    app.Q = dict()
    for count in range(2, 22):
        for upcard in range(2, 12):
            hand = (count, upcard)
            if count == 21:
                app.Q[hand] = [1, 0, 0, 0]
            else:
                app.Q[hand] = [-100, -100, -100, -100] 
                actions = ["s", "h", "dd", "sp"] 
                playGame(app, hand, actions)
    app.policy = returnPolicy(app, actions)     
    return app.policy, app.Q


def mcDealerPlays(app, hand):
    dcard = random.choice(range(2,12))
    dealerHand = hand[1] + dcard
    dlist = [hand[1], dcard]
    moneyWon = 0

    while hand[1] != 11 and dcard != 11 and dealerHand < 17:
        ncard = random.choice(range(2,12))
        dealerHand += ncard
        dlist.append(ncard)

    while dealerHand <= 17 and (hand[1] == 11 or dcard == 11):
        ncard = random.choice(range(2,12))
        dealerHand += ncard
        dlist.append(ncard)

    while dealerHand > 21 and 11 in dlist:
        dealerHand -= 10
        dlist.remove(11)
                
    if dealerHand > 21:   
        moneyWon += 10
    elif hand[0] == 21 and dealerHand != 21:       
        moneyWon += 10
    elif hand[0] != 21 and dealerHand == 21:       
        moneyWon -= 10
    elif dealerHand > hand[0]:    
        moneyWon -= 10
    elif hand[0] > dealerHand:    
        moneyWon += 10
    return moneyWon


def playGame(app, hand, actions):

    if len(actions) == 0:
        return 
    
    else:
        if actions[0] == "s":
            moneyWon = 0
            for x in range(50):
                moneyWon += mcDealerPlays(app, hand)
            moneyWon //= 50
            app.Q[hand][0] = moneyWon
            playGame(app, hand, actions[1:])

        if actions[0] == "h":
            moneyWon = 0
            for x in range(50):
                ncard = random.choice(range(2, 11))
                newHand = [hand[0] + ncard, hand[1]]
                if newHand[0] > 21:    
                    moneyWon -= 10
                elif newHand[0] <= 21:
                    moneyWon += mcDealerPlays(app, newHand)
                moneyWon //= 50
                app.Q[hand][1] = moneyWon
                playGame(app, hand, actions[1:])

        if actions[0] == "dd":
            if hand[0] not in [9, 10, 11]:
                playGame(app, hand, actions[1:])
            else:
                moneyWon = 0
                for x in range(50):
                    ncard = random.choice(range(2, 11))
                    newHand = [hand[0] + ncard, hand[1]]
                    if newHand[0] > 21:    moneyWon -= 10
                    elif newHand[0] <= 21:
                        moneyWon += mcDealerPlays(app, newHand)
                    moneyWon //= 25
                    app.Q[hand][2] = moneyWon
                    playGame(app, hand, actions[1:])

        if actions[0] == "sp":
            if hand[0] % 2 != 0:
                playGame(app, hand, actions[1:])
            else:
                startHand = hand[0] / 2
                moneyWon = 0
                for x in range(50):
                    ncard = random.choice(range(2, 11))
                    n2card = random.choice(range(2, 11))
                    newHand = [startHand + ncard + n2card, hand[1]]
                    if newHand[0] > 21:    moneyWon -= 10
                    elif newHand[0] <= 21:
                        moneyWon += mcDealerPlays(app, newHand)

                    ncard = random.choice(range(2, 11))
                    n2card = random.choice(range(2, 11))
                    newHand = [startHand + ncard + n2card, hand[1]]
                    if newHand[0] > 21:    moneyWon -= 10
                    elif newHand[0] <= 21:
                        moneyWon += mcDealerPlays(app, newHand)
                    moneyWon //= 50
                    app.Q[hand][3] = moneyWon
                    playGame(app, hand, actions[1:])

def returnPolicy(app, actions):
    policy = dict()
    for item in app.Q:
        maxi = 0
        max = -100
        for i in range(0,4):
            if app.Q[item][i] > max:
                secmax = max
                secmaxi = maxi
                max = app.Q[item][i]
                maxi = i
        policy[item] = [actions[maxi]]
        policy[item].append(actions[secmaxi]) 
    return policy

runApp(width = 1280, height = 697)   # HAVE TO RUN IT AT THIS SIZE

