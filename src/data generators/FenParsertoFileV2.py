pieceDict = {
    'K': 1.0,
    'Q': 0.9,
    'B': 0.4,
    'N': 0.3,
    'R': 0.6,
    'P': 0.1,
    'k': -1.0,
    'q': -0.9,
    'b': -0.4,
    'n': -0.3,
    'r': -0.6,
    'p': -0.1
}

def convertToTrainingData(filename):
    X_data = open("xdata.txt","w")
    Y_data = open("ydata.txt","w")

    count = 0

    dict = splitFenAndEval(filename)
    for fen in dict.keys():    
        count = count + 1   
        for element in convertFenToInput(fen):
            X_data.write(str(element))
            X_data.write(" ")
        X_data.write("\n")

        Y_data.write(str(convertEvaluationToOutput(dict[fen], fen)))    
        Y_data.write("\n")

        if count % 100000 == 0:
            print("Parsing Game No: ",count)

def convertFenToInput(fenString):
    input = []

    # FEN strings are easier to parse when split up like this
    parts = fenString.split(' ')

    # Encode the board
    for char in parts[0]:
        if char != '/':
            if char.isalpha():
                input.append(convertPieceToInputValue(char, parts[1]))

            if char.isnumeric():
                zeroes = [0] * int(char)
                for val in zeroes:
                    input.append(val)

    # Encode the turn player
    input.append(1 if parts[1] == 'w' else -1)

    # Encode castling availability
    castling = [0] * 4
    for char in parts[2]:
        if char == 'K':
            castling[0] = 1
        if char == 'Q':
            castling[1] = 1
        if char == 'k':
            castling[2] = 1
        if char == 'q':
            castling[3] = 1
    for val in castling:
        input.append(val)
    #input.append(castling)

    return input

def convertPieceToInputValue(char, player):
    value = pieceDict[char] if char in pieceDict else 0
    return value

def splitFenAndEval(filename):
    fenDict = {}

    with open(filename) as f:
        for line in f:
            if line.rstrip():
                split = line.rsplit(' ',1)
                fenDict[split[0]] = split[1]

    return fenDict

def convertEvaluationToOutput(eval, fenString):
    fenParts = fenString.split(' ')
    try:
        return sigmoid(float(eval))
    except:
        #print('nonnumeric')
        if eval.strip() == 'MATE':
            return 1 if fenParts[1] == 'b' else -1
        else:
            if eval[2] == '#':
                return 1
            if eval[0] == '#':
                return -1

    return 0

def sigmoid(x):
    return x/(1 + abs(x))


convertToTrainingData("2017FEN.txt")
print("Done")
