## Requisiti

* Python ≥ 3.8
* Rasa installato:

```bash
pip install rasa
```

---

## Struttura dei file del progetto

```
meteo_bot/
├── actions.py
├── config.yml
├── credentials.yml
├── domain.yml
├── endpoints.yml
├── data/
│   ├── nlu.yml
│   ├── rules.yml
```

---

## Inizializza il progetto

```bash
rasa init --no-prompt --name meteo_bot
cd meteo_bot
```

Elimina i file `stories.yml` e `tests/` per semplicità.

---

## `data/nlu.yml`: esempi di intenti e entità

```yaml
version: "3.1"

nlu:
- intent: saluto
  examples: |
    - Ciao
    - Ehi
    - Salve

- intent: chiedi_meteo
  examples: |
    - Che tempo fa a [Roma](città)?
    - Vorrei sapere il meteo a [Milano](città)
    - Meteo per [Napoli](città)
    - Com'è il tempo oggi a [Roma](città)?
    - Fa caldo a [Milano](città)?
```

---

## 'domain.yml`: definizioni fondamentali

```yaml
version: "3.1"

intents:
  - saluto
  - chiedi_meteo

entities:
  - città

slots:
  città:
    type: text
    mappings:
      - type: from_entity
        entity: città

responses:
  utter_saluto:
    - text: "Ciao! Dimmi una città e ti dirò il meteo."

actions:
  - action_meteo
```

---

## `data/rules.yml`: logica conversazionale

```yaml
version: "3.1"

rules:
- rule: Rispondere al saluto
  steps:
    - intent: saluto
    - action: utter_saluto

- rule: Fornire il meteo per una città
  steps:
    - intent: chiedi_meteo
    - slot_was_set:
        - città: true
    - action: action_meteo
```

---

## `actions.py`: logica personalizzata

```python
from typing import Any, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionMeteo(Action):
    def name(self) -> str:
        return "action_meteo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        
        città = tracker.get_slot("città")

        meteo_finto = {
            "Roma": "sole e 27°C",
            "Milano": "pioggia leggera e 22°C",
            "Napoli": "nuvoloso e 25°C"
        }

        if città in meteo_finto:
            risposta = f"A {città} oggi c'è {meteo_finto[città]}."
        else:
            risposta = f"Mi dispiace, non ho informazioni sul meteo per {città}."

        dispatcher.utter_message(text=risposta)
        return []
```

---

## `endpoints.yml`: attiva l’action server

```yaml
action_endpoint:
  url: "http://localhost:5055/webhook"
```

---

## `config.yml`: pipeline e politica base

```yaml
recipe: default.v1
language: it

pipeline:
  - name: WhitespaceTokenizer
  - name: RegexFeaturizer
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
  - name: DIETClassifier
  - name: EntitySynonymMapper
  - name: ResponseSelector
  - name: FallbackClassifier

policies:
  - name: RulePolicy
```

---

## Allena e avvia il bot

```bash
# Allena il modello
rasa train

# Avvia il server delle action personalizzate (nuova shell)
rasa run actions

# Avvia il bot in modalità terminale (altra shell)
rasa shell
```

---

## Esempio di dialogo

```
Utente: Ciao
Bot: Ciao! Dimmi una città e ti dirò il meteo.

Utente: Che tempo fa a Roma?
Bot: A Roma oggi c'è sole e 27°C.

Utente: E a Milano?
Bot: A Milano oggi c'è pioggia leggera e 22°C.
```

---
