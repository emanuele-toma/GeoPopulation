######################################################
#   Estrazione coordinate in base alla popolazione   #
######################################################

# Numero minimo di abitanti per Km^2
THRESHOLD = 50

# Numero del quadrante
QUADRANTE = 8

# Calcola e mostra immagine
CALCOLA_IMMAGINE = True
MOSTRA_IMMAGINE = True
SALVA_IMMAGINE = False

######################################################
#       Non modificare nulla sotto questa riga       #
######################################################

# Valore cella vuota
NO_DATA_VALUE = -9999

# Dimensione griglia
GRIDSIZE = 10800

# Linee di intestazione
HEADERLINES = 6

# Dimensione Cella
CELLSIZE = 0.008333333333333333

# Numero parallelo di partenza (In alto a sinistra del quadrante)
START_QUADRANTE_X = 0

# Numero meridiano di partenza (In alto rispetto al quadrante, a sinistra)
START_QUADRANTE_Y = 0

# Calcolo coordinate di partenza
if QUADRANTE >= 1 and QUADRANTE <= 4:
    START_QUADRANTE_Y = 90

if QUADRANTE >= 5 and QUADRANTE <= 8:
    START_QUADRANTE_Y = 0

if QUADRANTE == 1 or QUADRANTE == 5:
    START_QUADRANTE_X = -180

if QUADRANTE == 2 or QUADRANTE == 6:
    START_QUADRANTE_X = -90

if QUADRANTE == 3 or QUADRANTE == 7:
    START_QUADRANTE_X = 0

if QUADRANTE == 4 or QUADRANTE == 8:
    START_QUADRANTE_X = 90

# File da leggere
FILE = './popolazione/gpw_v4_population_density_rev11_2020_30_sec_' + str(QUADRANTE) + '.asc'

from PIL import Image
img = Image.new('RGB', (GRIDSIZE, GRIDSIZE), (180, 210, 250))
output = open('output-' +  str(QUADRANTE) + '.txt', mode='a')

with open(FILE, 'r') as fileobj:
    line_number = -HEADERLINES
    for line in fileobj:

        if line_number < 0:
            line_number += 1
            continue

        line = line.split()
        if line:
            for i in range(len(line)):
                if line[i] == str(NO_DATA_VALUE):
                    continue

                r = int(float(line[i]))
                
                if r >= THRESHOLD:
                    r = 255
                    output.write(
                        str(
                            format(
                                START_QUADRANTE_Y - line_number*CELLSIZE
                            , '.6f')) + ", " + 
                        str(
                            format(
                                START_QUADRANTE_X + i*CELLSIZE
                            , '.6f')) + "\n")
                else:
                    r = 0

                g = 255 - r
                b = 255 - r
            
                if CALCOLA_IMMAGINE == True:
                    img.putpixel((i, line_number), (255, g, b))

        line_number += 1
        if line_number % 100 == 0:
            print('Progresso: ' + str(int((line_number/GRIDSIZE)*100)) + "%", end='\r')

if MOSTRA_IMMAGINE == True:
    img.show()
    
if SALVA_IMMAGINE == True:
    img.save('immagine-' + str(QUADRANTE) + '.png')

output.close()