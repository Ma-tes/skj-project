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

## 19.04 — Alembic migrace, Buckety, Billing, Soft Delete

1. Jaké nástroje AI byly použity
    - Claude Opus 4.6 (100%)
2. Příklady promptů
    - `"Follow all steps from task requirements."`
    - `"Create manual testing sequence with expected results... Write it down as steps."`
    - `"I cannot execute steps from 5?"` (debugging problému s curl)
    - `"It goes into dquote mode in CLI"` (problém s bash escapováním)
    - `"Step 5 still goes into dquote while echo"` (!! v double quotes spouští bash history expansion)
    - `"Create the curl for this file: 2b6bbff8-ae49-470f-a5ec-da668ca24665"`
    - `"Add there output to see if something happened"`
3. Co AI vygenerovala správně
    - Kompletní inicializaci Alembicu (alembic.ini, env.py s render_as_batch=True pro SQLite)
    - Všechny 4 migrační skripty (buckets + FK, billing sloupce, is_deleted, request counts)
    - Bucket model s relací na File
    - Advanced billing logiku (ingress/egress/internal rozlišení přes X-Internal-Source header)
    - Soft delete implementaci (is_deleted flag, filtrování v queries)
    - API request counting (count_write_requests, count_read_requests)
    - Pydantic schémata (BucketCreate, BucketResponse, BillingResponse)
    - BucketRepository a úpravy FileRepository
    - Kompletní manuální testovací sekvenci s očekávanými výsledky
4. Co bylo nutné opravit
    - Curl příkazy v testovací sekvenci používaly víceřádkový formát s `\` — v terminálu to způsobovalo přechod do dquote režimu. Opraveno na jednořádkové příkazy.
    - `echo "hello world!!!"` — `!!` v double quotes spouští bash history expansion. Opraveno na single quotes: `echo 'hello world!!!'`.
    - Testovací příkazy neměly výstup HTTP kódu — přidáno `-w "\nHTTP:%{http_code}\n"` pro viditelnost výsledků.
