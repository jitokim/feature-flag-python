# FastAPI Example Application

This example demonstrates how to use feature-flag-python in a FastAPI application.

## Features Demonstrated

- Basic feature flags with `ais_enabled()`
- A/B testing with `aget_experiment()` and `aget_variant()`
- Decorators: `@afeature_flag` and `@aexperiment_variant`
- Error handling and graceful degradation
- Health checks with feature flag status

## Running the Example

1. Install dependencies:
```bash
   pip install -r requirements.txt
```

2. Set up environment:
```bash
cp .env.example .env
# Edit .env with your feature flag server URL
```

3. Start the server:
```bash
python main.py
```
