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
