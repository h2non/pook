# Pook development

**All contributors are obliged to follow Pook's [Code of Conduct](./CODE_OF_CONDUCT.md)**.

## Getting started

First, clone the repository:

```bash
git clone git@github.com:h2non/pook.git
```

Pook uses [`hatch`](https://hatch.pypa.io/) for script and environment management. Run the `ci` script to set up a development virtual environment and verify your local setup:

```bash
hatch run ci
```

Running the `ci` script will:
- Cause Hatch to set up a development virtual environment
- Install pre-commit hooks
- Run the pre-commit hooks, including type checks
- Run the unit tests

Now you are ready to contribute to Pook! If there is a specific issue you'd like to work on, leave a comment expressing your interest and any questions you have for maintainers regarding implementation details.

When contributing code, please add unit tests for all changes and documentation for any non-internal changes.

## Testing

Pook supports all actively supported CPython versions, as well as the latest Pypy version. To run Pook's test suite for each supported interpreter, run the following:

```bash
hatch run test:test
```

Note that each interpreter requires a new virtual environment, and hatch will automatically handle creating these.

To run tests only for a specific version, affix the version designation to the environment name (the left side of the `:`):

```bash
hatch run test.pypy3.10:test
```

## Documentation

Generate the documentation site by running:

```bash
hatch run docs:build
```

## Building for distribution

Use Hatch's build tools to create the Pook distribution:

```bash
hatch build -c
```
