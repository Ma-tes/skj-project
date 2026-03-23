## Použité AI nástroje

- Claude Sonnet 4.6
- Claude Opus 4.6

## Použité dokumentace
- https://fastapi.tiangolo.com/learn/

## Příklady promptů

- „Create implementation of endpoints. With small model repository. Make it as clean as possible, without any other dependencies."
- „Use something different and also separate the endpoints to different file endpoints.py"
- „Add user id support for all endpoints."
- „Generate metadata logging into json - for individual endpoints."
- „Generate requirements for this project."

## Co AI vygenerovala správně

- Kompletní strukturu projektu (main.py, endpoints.py, repository.py, models.py, database.py)
- Ne příliš perfektní, ale repository pattern a ukládáním souborů na disk
- REST API endpointy (upload, download, delete, list) s FastAPI a APIRouter
- Oddělení souborů podle uživatelů (storage/<user_id>/<file_id>)
- Použití UUID jako názvu souboru na disku – bez kolizí názvů

## Co bylo nutné opravit

- Strukturu endpointů do separátních souborů

## Jaké chyby AI udělala

- Nekonzistence mezi požadavky, počas většího context window

## Requirements

1. pip install -r requirements.txt
2. run 0.0.0.0/8000/docs