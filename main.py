######################################################
#   Estrazione coordinate in base alla popolazione   #
######################################################

# Numero minimo di abitanti per Km^2
THRESHOLD = 200

# Dimensione Cella
CELLSIZE = 0.008333333333333333

# Numero del quadrante
QUADRANTE = 3

# Numero parallelo di partenza (In alto a sinistra del quadrante)
START_QUADRANTE_X = 0

# Numero meridiano di partenza (In alto rispetto al quadrante, a sinistra)
START_QUADRANTE_Y = 90

# Calcola e mostra immagine
IMMAGINE = True

######################################################

FILE = './popolazione/gpw_v4_population_density_rev11_2020_30_sec_' + str(QUADRANTE) + '.asc'
from PIL import Image
img = Image.new('RGB', (10800, 10800), (200, 210, 220))
output = open('output-' +  str(QUADRANTE) + '.txt', mode='a')

with open(FILE) as fileobj:
    line_number = -6
    for line in fileobj:

        if line_number < 0:
            line_number += 1
            continue

        line = line.split()
        if line:
            for i in range(len(line)):
                if line[i] != '-9999':
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

                    if IMMAGINE == True:
                        img.putpixel((i, line_number), (255, g, b))

        line_number += 1
        if line_number % 100 == 0:
            print('Progresso: ' + str(int((line_number/10800)*100)) + "%", end='\r')

if IMMAGINE == True:
    img.show()
    
output.close()

