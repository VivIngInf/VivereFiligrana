![GitHub repo size](https://img.shields.io/github/repo-size/VivIngInf/VivereFiligrana)
![GitHub License](https://img.shields.io/github/license/VivIngInf/VivereFiligrana)

# Vivere Filigrana - Utility per la Conversione e la Filigrana di Documenti 🔏

## Lingue disponibili

[🇮🇹 Italiano](#) | [🇬🇧 English](../../README.md)

## Introduzione

Benvenuti in **Vivere Filigrana**, lo strumento di conversione documenti e apposizione filigrana di Vivere Ateneo!

Questo sito web permette agli utenti di convertire file `.docx` in `.pdf` e applicare una filigrana con il logo di Vivere Ateneo e le sue sotto-associazioni.

Inoltre, gli utenti possono caricare direttamente file `.pdf`, e lo strumento applicherà automaticamente la filigrana.

## Struttura del Progetto

Ecco la struttura delle directory del progetto:

```MD
┌── resources 🌍
│   ├── images 🖼️               # Contiene le risorse immagine utilizzate nei readme
│   └── docs 📚                 # Memorizza i file README o documentazione
├── source ⚙️
│   ├── static 🌐
│   │   ├── css 🎨              # File CSS per lo styling
│   │   ├── fonts 🅰️            # File di font utilizzati nel sito web
│   │   ├── images 🖼️           # Immagini statiche utilizzate nel sito web
│   │   ├── uploads 📤          # Cartella per i file caricati
│   │   └── watermarks 🌊       # Cartella per i template di filigrana
│   ├── templates 🧩
│   │   └── index.html 🖥️       # Template HTML principale
│   ├── .env 🗃️                 # File delle variabili di ambiente
│   ├── app.py 🐍               # Il principale script dell'applicazione Flask
│   ├── package-lock.json 🔒    # File di blocco per le dipendenze npm (solo per lo sviluppo)
│   ├── package.json 📄         # File di configurazione npm (solo per lo sviluppo)
│   └── requirements.txt 📑     # Lista delle dipendenze Python
├── LICENSE 🏅                  # Licenza AGPL v3
└── README.md ℹ️           	    # Il file che stai leggendo ora
```

## Requisiti

Prima di eseguire questo progetto, è necessario installare i seguenti strumenti:

- **LibreOffice (headless)**: Richiesto per convertire i file `.docx` in file `.pdf`. 

Per installare LibreOffice su Ubuntu, usa il seguente comando:
    
``` shell
sudo apt install libreoffice
```

- **Python environment**:

1. Crea un virtual environment (venv) nella directory source:

``` shell
    python -m venv venv
```
    
2. Installa le dipendenze:
    
``` shell
    pip install -r requirements.txt
```

- **npm (development only)**: npm è utilizzato solo durante lo sviluppo per buildare gli stili css e non è richiesto per il deployment.

``` shell
    npm run watch
```

## Avviare l'applicazione

Una volta installate tutte le dipendenze e settato l'enviroment, puoi avviare l'applicazione usando il comando: 

``` shell
    python app.py
```

Questo avvierà il server Flask localmente. Apri il browser e naviga in `http://127.0.0.1:5000` per accedere al sito.

## Buildare e servire l'applicazione

Per buildare il progetto come Python wheel, prima bisogna installare i tools di building:

```shell
    pipx install hatch
    pip install build
```

Quindi, dalla root del progetto, buildare il wheel:

```shell
	python -m build --wheel
```

Il file .whl risultante sarà piazzato nella directory dist/ e può essere installato con pip:

```shell
    pip install dist/<package-name>.whl.
```

Quindi si potrà usare qualcosa come gunicorn per esporlo all'Internet:

```shell
	#!/usr/bin/bash
	gunicorn vivere_filigrana:app --bind 0.0.0.0:8000
```

## 👥 Made By

Vivere Filigrana è stato sviluppato da:

<table>
    <tr>
        <th>Daniele Orazio Susino</th>      
    </tr>
    <tr>
        <td><img src="../images/Daniele Orazio Susino.jpg" alt="Daniele Orazio Susino" width="150"></td>     
    </tr>
    <tr>
        <td>
            <a href="https://www.instagram.com/daniele.susino/">Instagram 📸</a><br>
            <a href="https://www.linkedin.com/in/susinodaniele/">LinkedIn 👔</a><br>
            <a href="mailto:susino.daniele@outlook.com">Email 📨</a>
        </td>
    </tr>
</table>


Ma originariamente era stato sviluppato da:

- [GanciDev](https://www.linkedin.com/in/giuseppe-g/)
- [Ashenclock](https://www.instagram.com/ashenclock_/)

Si ringrazia [Giovanni Luca Cusano](https://www.linkedin.com/in/giovanni-luca-cusano/) per aver provvisto alla creazione dei watermark.


## Licenza

Questo progetto è rilasciato sotto la licenza **GNU AGPL v3** - vedi il file [LICENSE](../../LICENSE) per i dettagli.

### Maggiori Limitazioni della Licenza AGPL v3

1. **Uso e Distribuzione**: Sei libero di usare, modificare e distribuire questo software, a condizione che tu rispetti i termini della licenza AGPL v3.

2. **Disponibilità del Codice Sorgente**: Se modifichi e distribuisci questo software (ad esempio come servizio web), devi rendere disponibile il codice sorgente della versione modificata agli utenti del tuo servizio.

3. **Nessun Uso Commerciale Senza Divulgazione del Codice Sorgente**: Se utilizzi questo software per scopi commerciali, devi rendere disponibile il codice sorgente modificato sotto la stessa licenza AGPL v3, garantendo che le stesse libertà si applichino a qualsiasi opera derivata.

4. **Redistribuzione**: Qualsiasi redistribuzione del codice, comprese le versioni modificate, deve essere rilasciata sotto la licenza AGPL v3.

5. **Attribuzione**: Quando redistribuisci il software (modificato o meno), devi fornire l'attribuzione corretta agli autori originali e indicare eventuali modifiche effettuate. Devi inoltre includere il testo della licenza insieme alla redistribuzione.

Per maggiori dettagli, consulta la [licenza completa AGPL v3](https://www.gnu.org/licenses/agpl-3.0.html).
