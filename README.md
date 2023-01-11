# Estrazione Coordinate in base alla Popolazione

Questo progetto consente di estrarre le coordinate di una posizione in base alla densità di popolazione.

## Requisiti

Questo progetto richiede Pillow per poter funzionare.

## Utilizzo

Per utilizzare questo progetto, è necessario modificare i seguenti parametri:

    THRESHOLD: numero minimo di abitanti per Km^2
    CELLSIZE: dimensione della cella
    QUADRANTE: numero del quadrante
    START_QUADRANTE_X: numero parallelo di partenza (in alto a sinistra del quadrante)
    START_QUADRANTE_Y: numero meridiano di partenza (in alto rispetto al quadrante, a sinistra)
    IMMAGINE: mostra o meno un'immagine

Inoltre, è necessario specificare il file FILE contenente la densità di popolazione.

Una volta impostati i parametri, esegui il file .py . Il programma creerà un file di testo 'output-{numero quadrante}.txt' contenente le coordinate delle posizioni con densità di popolazione maggiore o uguale al valore di THRESHOLD. Inoltre se si setta IMMAGINE = True, verrà mostrata un'immagine rappresentante le coordinate estratte.

## Note

Si prega di notare che questo progetto è stato scritto per un set di dati specifico e potrebbe non funzionare correttamente con altri set di dati.

Per le istruzioni su come aggiungere il dataset leggere il (README)[https://github.com/emanuele-toma/GeoPopulation/popolazione/README.txt] nella cartella popolazione

Nei file del progetto è presente un'immagine di riferimento per capire quali valori inserire nei campi per la configurazione dei quadranti.