# Append-only price history and MarketEvents

Prices and status must not silently overwrite history. Latest values may live on Project/UnitType rows for query convenience, but every material change also appends a PriceSnapshot and/or MarketEvent. This preserves temporal intelligence, which is the core product bet over marketplace UX.
