# Main.py

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

Una volta impostati i parametri, esegui il file .py. 

Il programma creerà un file di testo `output-{numero quadrante}.txt` contenente le coordinate delle posizioni con densità di popolazione maggiore o uguale al valore di THRESHOLD.

Inoltre se si imposta IMMAGINE = True, verrà mostrata un'immagine rappresentante le coordinate estratte.

## Note

Si prega di notare che questo progetto è stato scritto per un set di dati specifico e potrebbe non funzionare correttamente con altri set di dati.

Per le istruzioni su come aggiungere il dataset leggere il [README](https://github.com/emanuele-toma/GeoPopulation/popolazione/README.txt) nella cartella popolazione.

Nei file del progetto è presente un'immagine di riferimento per capire quali valori inserire nei campi per la configurazione dei quadranti.

# Main-API.py

API di generazione mappa

## Requisiti

Per utilizzare questa API è necessario avere i seguenti moduli Python installati:

* PIL
* Flask
* waitress
* hashlib
* os
* threading
* random
* base64
* io
* shutil
* smopy
* geopy

Inoltre l'API utilizza il servizio geocoders di geopy per ottenere informazioni sull'indirizzo a partire dalle coordinate, quindi è necessaria una connessione internet per utilizzare questa funzionalità.

Per installare i moduli necessari è possibile utilizzare il comando `pip install -r requirements-api.txt` o `pip install nome-modulo` per ogni modulo necessario.

## Endpoint:

1. `/api/v1/generate_map/<int:QUADRANTE>/<int:THRESHOLD>`

    * Metodo: GET
    * Parametri:
        * QUADRANTE: intero compreso tra 1 e 8 che rappresenta il quadrante della mappa da generare
        * THRESHOLD: intero maggiore o uguale a 0 che rappresenta la soglia per la generazione della mappa
    * Restituisce:
        * JSON con lo stato della generazione della mappa (0 se in corso, 100 se completato) e l'hash della richiesta
        * Codice di stato HTTP 200 in caso di successo, 400 in caso di parametri non validi

2. `/api/v1/random_map_data/<HASH>`

    * Metodo: GET
    * Parametri:
        * HASH: stringa che rappresenta l'hash della richiesta di generazione della mappa
    * Restituisce:
        * JSON con informazioni su una posizione casuale sulla mappa generata, tra cui latitudine e longitudine, indirizzo, link a Google Maps, immagine della mappa con la posizione segnalata e seed utilizzato per generare la posizione casuale
        * Codice di stato HTTP 200 in caso di successo, 404 in caso di hash non trovato o richiesta di generazione ancora in corso

3. `/api/v1/random_map_data/<HASH>/<int:SEED>`

    * Metodo: GET
    * Parametri:
        * HASH: stringa che rappresenta l'hash della richiesta di generazione della mappa
        * SEED: intero che rappresenta il seed da utilizzare per generare la posizione casuale sulla mappa
    * Restituisce:
        * JSON con informazioni su una posizione sulla mappa generata, tra cui latitudine e longitudine, indirizzo, link a Google Maps, immagine della mappa con la posizione segnalata e seed utilizzato per generare la posizione casuale
        * Codice di stato HTTP 200 in caso di successo, 404 in caso di hash non trovato o richiesta di generazione ancora in corso, 400 in caso di seed non valido

4. `/api/v1/random_map/<HASH>`

    * Metodo: GET
    * Parametri:
        * HASH: stringa che rappresenta l'hash della richiesta di generazione della mappa
    * Restituisce:
        * Immagine che rappresenta un punto casuale del set il cui nome corrisponde al seed di generazione del dato casuale
        * Codice di stato HTTP 200 in caso di successo, 404 in caso di hash non trovato o richiesta di generazione ancora in corso

5. `/api/v1/random_map/<HASH>/<int:SEED>`

    * Metodo: GET
    * Parametri:
        * HASH: stringa che rappresenta l'hash della richiesta di generazione della mappa
        * SEED: intero che rappresenta il seed da utilizzare per generare la posizione casuale sulla mappa
    * Restituisce:
        * Immagine che rappresenta un punto del set il cui nome corrisponde al seed di generazione del dato casuale
        * Codice di stato HTTP 200 in caso di successo, 404 in caso di hash non trovato o richiesta di generazione ancora in corso, 400 in caso di seed non valido.

6. `/api/v1/map/<HASH>`

    * Metodo: GET
    * Parametri
        * HASH: stringa che rappresenta l'hash della richiesta di generazione della mappa
    * Restituisce:
        * Immagine che comprende tutti i segnaposto

## Note:

Per ogni richiesta di generazione mappa, viene creata una cartella specifica nella directory "jobs" con l'hash della richiesta come nome della cartella. 
Questa cartella contiene tutte le informazioni relative alla richiesta, come lo stato della generazione, l'output e le immagini generate.

La funzione che elimina le cartelle è stata progettata per rimuovere la cartella solo quando l'elaborazione è completata e l'output è stato recuperato.
Se la cartella esiste ma non contiene il file "status.txt", la cartella viene eliminata per evitare di occupare spazio inutile.

Si prega di notare che questo progetto è stato scritto per un set di dati specifico e potrebbe non funzionare correttamente con altri set di dati.

Per le istruzioni su come aggiungere il dataset leggere il [README](https://github.com/emanuele-toma/GeoPopulation/popolazione/README.txt) nella cartella popolazione.