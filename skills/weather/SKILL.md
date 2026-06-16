---
name: weather
version: 0.1.0
description: >-
  Current conditions and a multi-day forecast for any city via Open-Meteo's free
  public API (no API key required). Use for weather, forecast, temperature, or
  rain questions about a place.
triggers:
  - weather
  - forecast
  - temperature
  - rain
  - clima
  - pronóstico
requires:
  bins: []
  env: []
  config: []
---

# Weather — Open-Meteo (keyless)

Answer weather questions by calling Open-Meteo's free public API with `exec curl`.
**No API key, no auth header.**

## Step 1 — resolve the city to coordinates (geocoding)

```bash
exec curl -s "https://geocoding-api.open-meteo.com/v1/search?name=Berlin&count=1&language=en&format=json"
```

Read `results[0].latitude`, `results[0].longitude`, `results[0].name`,
`results[0].country`. If `results` is empty/missing, tell the user the city
wasn't found and ask them to clarify.

## Step 2 — fetch current + daily forecast

```bash
exec curl -s "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code&timezone=auto&forecast_days=3"
```

- `current` → now: temperature (`temperature_2m`, °C), humidity, wind, `weather_code`.
- `daily` arrays (index 0 = today, 1 = tomorrow, …): `temperature_2m_max/min`,
  `precipitation_probability_max` (%), `weather_code`.

## WMO weather codes → words

`0` clear · `1-3` mainly clear → partly cloudy · `45/48` fog · `51-57` drizzle ·
`61-67` rain · `71-77` snow · `80-82` rain showers · `95-99` thunderstorm.

## Rules

- **Always geocode first** (Step 1) to get lat/long — don't guess coordinates.
- One forecast call covers current + several days — don't loop one request per day.
- Answer in plain language with the numbers asked (temperature, rain chance) and
  translate `weather_code` into a human description. Use °C.
- If a call fails, say so briefly and show the error.
