---
name: snowfall-smoke-test
description: Regenerates map.html for one or more saved address/date-range test cases and reports pass/fail, without retyping input()  prompts by hand. Use this whenever code in main.py, api/map.py, api/weather.py, or api/nearby.py has just been edited and you want a fast "did I break anything" check - this project has no automated test suite, so this is the closest thing to one. Trigger on requests like "test my changes", "does this still work", "smoke test", or "regenerate the map" for this project.
---

# Snowfall map smoke test

`main.py` only runs interactively (`input()` for address, start date, end date), so verifying a
change means retyping the same values every time. This skill runs the same pipeline
(geocode → nearby cities → fetch snowfall → render heatmap) programmatically against saved
test cases instead, and tells you plainly whether it worked.

## When to use this

After editing any file under `api/` or `main.py`, run this before telling the user the change
is done. It calls real, unauthenticated network APIs (Nominatim, Geonames, Open-Meteo), so it's
a true end-to-end check, not a mock - treat a pass here with real confidence, and treat a
failure as a real regression, not flakiness, unless the error message clearly says otherwise
(e.g. a network timeout).

## Running it

From the project root:

```bash
python .claude/skills/snowfall-smoke-test/scripts/smoke_test.py
```

This runs the single default case (Rexburg, Idaho, a 3-day date range - kept short so the
weather API call is fast) and prints one line per case:

```
[PASS] Case 1: Rexburg, Idaho (2024-01-01 to 2024-01-03) - OK - 4 data points, map.html 187321 bytes
```

or, if something is broken:

```
[FAIL] Case 1: Rexburg, Idaho (2024-01-01 to 2024-01-03) - Exception: 'NoneType' object has no attribute 'latitude'
```

The script exits non-zero if any case fails, so it's easy to tell success from failure without
parsing output closely.

## Using your own test cases

To check more than one location/date range at once (e.g. an address that previously returned
no nearby cities, or a longer date range), write a JSON file:

```json
[
  {"address": "Rexburg, Idaho", "start_date": "2024-01-01", "end_date": "2024-01-05"},
  {"address": "Denver, Colorado", "start_date": "2023-12-01", "end_date": "2023-12-07"}
]
```

and pass it in:

```bash
python .claude/skills/snowfall-smoke-test/scripts/smoke_test.py --cases my_cases.json
```

## What counts as a pass

For each case, the script checks - in order - that: geocoding the address succeeds, Geonames
returns at least one nearby city, weather data comes back non-empty for at least one of them,
the map object is built, and `map.html` in the project root gets freshly written (exists,
modified in the last 30 seconds, and isn't suspiciously small). Any exception along the way is
caught and reported as a failure with the exception message, rather than crashing the script -
that message is usually enough to point at which stage broke.

## Notes

- This overwrites `map.html` and appends to `.cache.sqlite` (the weather API's HTTP cache) in
  the project root, same as running `main.py` normally would.
- It does not need a code change to be useful - it's also a fine way to just check "is the
  project currently working" from a clean checkout.
