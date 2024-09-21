# eye

The CLI for moving files and processing photogrammetry data. 

## Install

Use `pipx` to keep the cli dependencies isolated

Install from Pypi

```
pipx install eye
```

Here is installing it directly from a wheel:

```
➜ pipx install dist/eye-0.1.0-py3-none-any.whl
  installed package eye 0.1.0, installed using Python 3.12.2
  These apps are now globally available
    - eye
done! ✨ 🌟 ✨

➜ which eye
/Users/will.barley/.local/bin/eye
```

## Build

First bump the version number in `pyproject.toml`.
Then:

```
poetry publish --build
```