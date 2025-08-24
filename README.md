# Solar Faults — Minimal Repo

Purpose-built, tiny repo for detecting solar faults using:
1) **Data fetcher** (Timestream) — simple query interface
2) **Metadata fetcher** — pulls plant/asset info you need
3) **Fault descriptions** — natural-language notes + logical rules (YAML)
4) **Runner** — executes deterministic rules or an LLM-based evaluator
5) **Outputs** — CSV of fault intervals: where and when each fault occurred

No fancy infra. No tests. Just the bits you asked for.

---

## Install
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Files (quick map)
- `modules/timestream_fetch.py` — stub to wrap *your existing Timestream pull code* (HelioLib or boto3).
- `modules/metadata_fetch.py` — stub wrapping *your existing metadata service*.
- `modules/patterns.py` — loads/validates YAML fault patterns.
- `modules/rule_engine.py` — evaluates deterministic fault rules on a DataFrame.
- `modules/llm_engine.py` — optional LLM flow (stubbed; wire OpenAI/Bedrock/etc.).
- `cli/fetch_data.py` — CLI to fetch & save telemetry to CSV.
- `cli/fetch_metadata.py` — CLI to fetch metadata to JSON.
- `cli/run.py` — CLI to run rules/LLM on your CSV and write `outputs/faults.csv`.
- `patterns/faults.yml` — example rules + natural-language descriptions.
- `examples/sample.csv` — tiny sample with `ts,ac_power_kw,irradiance_wm2`.

---

## How modules connect

**Flow (rules mode):**
```
metadata_fetch → timestream_fetch → (CSV) → rule_engine.run(data, patterns) → outputs/faults.csv
```

**Flow (LLM mode):**
```
metadata_fetch → timestream_fetch → (CSV) → llm_engine.analyze(data, pattern_descriptions) → outputs/faults.csv
```

- The **metadata** module gives you plant/asset/connection info you need to parameterize queries.
- The **timestream** module executes a simple query and returns a pandas DataFrame (or saves CSV).
- The **patterns** module loads YAML that contains both human descriptions and machine-readable conditions.
- The **runner** (CLI `cli/run.py`) plugs data + patterns into either the deterministic **rule_engine** or the **llm_engine**.

---

## CLI usage

### 1) Fetch metadata
```bash
python -m cli.fetch_metadata --plant-id p01 --out outputs/metadata.p01.json
```

### 2) Fetch data from Timestream
Provide either a raw query or let the CLI build a simple query from flags.
```bash
# Raw query
python -m cli.fetch_data --plant-id p01 --asset-id inv_7   --start "2025-08-24T10:00:00Z" --end "2025-08-24T11:00:00Z"   --query "SELECT time as ts, ac_power_kw, irradiance_wm2 FROM telemetry WHERE ..."   --out outputs/inv7.csv

# Or without --query (module can build a naive one; replace with your own)
python -m cli.fetch_data --plant-id p01 --asset-id inv_7   --start "2025-08-24T10:00:00Z" --end "2025-08-24T11:00:00Z"   --out outputs/inv7.csv
```

### 3) Run algorithms (rules)
```bash
python -m cli.run --data outputs/inv7.csv --patterns patterns/faults.yml --mode rules   --out outputs/faults.csv
```

### 4) Run algorithms (LLM) — optional
```bash
python -m cli.run --data outputs/inv7.csv --patterns patterns/faults.yml --mode llm   --out outputs/faults.csv
```
> `llm_engine.py` is stubbed. Wire your provider of choice (OpenAI/Bedrock) in one place.

---

## Output format
`outputs/faults.csv`:
```
plant_id,asset_id,fault_type,start_ts,end_ts,confidence,evidence
p01,inv_7,grid_curtailment,2025-08-24T10:01:00Z,2025-08-24T10:05:00Z,0.92,"irradiance>=600 & ac_power < 0.8*expected"
```

---

## Notes
- Replace the placeholder imports in `modules/timestream_fetch.py` and `modules/metadata_fetch.py` with your HelioLib calls (as per your READMEs).
- The rule syntax in `patterns/faults.yml` uses `pandas.eval` expressions over your DataFrame columns. Keep `ts` as a datetime column.
