## 23.03

1. Jaké nástroje AI byly použity
   - Claude Opus 4.6(100%)
2. Příklady promptů
    - „Create implementation of endpoints. With small model repository. Make it as clean as possible, without any other dependencies."
    - „Use something different and also separate the endpoints to different file endpoints.py"
    - „Add user id support for all endpoints."
    - „Generate metadata logging into json - for individual endpoints."
    - „Generate requirements for this project."
3. Co AI vygenerovala správně
    - Kompletní strukturu projektu (main.py, endpoints.py, repository.py, models.py, database.py)
    - Ne příliš perfektní, ale repository pattern a ukládáním souborů na disk
    - REST API endpointy (upload, download, delete, list) s FastAPI a APIRouter
    - Oddělení souborů podle uživatelů (storage/<user_id>/<file_id>)
    - Použití UUID jako názvu souboru na disku – bez kolizí názvů
4. Co bylo nutné opravit
    - Strukturu endpointů do separátních souborů

## 30.03

1. Jaké nástroje AI byly použity
    - Claude Sonnet 4.6(80%), Claude Opus 4.6(20%)
2. Příklady promptů
    - `"Show examples, how to use the Pydantic for this case?"`
    - `"Perfect, implement it."`
    - `"Create: from pydantic import BaseModel, Field... And implement create_db_task and get_db_task on /db-tasks"`
    - `"Merge task_endpoint into #file:endpoints.py."`
    - `"Now, create request schemas for all #file:endpoints.py."`
    - `"Renaming it to TaskRequest."`
    - `"Now, do it for all other endpoints calls. files"`
    - `"Check if all requirements are implemented: ..."`
    - `"Fix it."`
    - `"Check it again."`
    - `"Now check it with the full requirements: ..."`
3. Co AI vygenerovala správně
    - Vzhledem k examplům zadání, claude vygeneroval takřka vše správně
4. Co bylo nutné opravit
    - Zbytečné rozdělení endpointů do více souborů -> Pro tento project je to prozatím zbytečné.
