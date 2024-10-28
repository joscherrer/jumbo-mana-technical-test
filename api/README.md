# fairchess-api

## Requirements

- `python` >=3.12
- `pdm`
- `stockfish`

## Running

```bash
pdm install
pdm run fastapi dev src/api 
```

## Building the image

```bash
docker build -t fairchess-api .
```
