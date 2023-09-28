# Tempest (0.1)

An application to get a weather consistency index for a given location during a given time period

## Running

```
docker compose up -d
```

To sync changes to the images after pulling changes:

```
docker compose up  -d --build
```

## Test Suite

The test suite is designed to debug more problems than the number of tests. This can be found in the error message in case the tests fail.

Make sure the application is running before running the test suite.

```
pip install pytest
cd test
pytest test.py
```
