# Deterministic parsing before optional LLM extraction

Price, currency, district, and ProjectStatus are normalized with deterministic parsers and alias maps. LLM extraction is optional and only when traditional extraction fails. Invented values are forbidden; missing public data stays null.
