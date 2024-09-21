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
➜ pipx install eye-cli
  installed package eye-cli 0.1.0, installed using Python 3.12.2
  These apps are now globally available
    - eye
done! ✨ 🌟 ✨

# start new shell...

➜ which eye
/Users/will.barley/.local/bin/eye
```

## Build

First bump the version number in `pyproject.toml`.
Then:

```
➜ poetry publish --build

There are 1 files ready for publishing. Build anyway? (yes/no) [no] yes
Building eye-cli (0.1.0)
  - Building sdist
  - Built eye_cli-0.1.0.tar.gz
  - Building wheel
  - Built eye_cli-0.1.0-py3-none-any.whl

Publishing eye-cli (0.1.0) to PyPI
 - Uploading eye_cli-0.1.0-py3-none-any.whl 100%
 - Uploading eye_cli-0.1.0.tar.gz 100%
```

