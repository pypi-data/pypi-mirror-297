# pyshover

A simple Pushover client

Install:

Library and script: `pip install pyshover`
Script only: `pipx install pyshover`


Sample Usage:

```python
from pushover import Pushover

po = Pushover(app_token="fake", user_token="fake", message="message",title="title")
po.send()
```

Make the call more simple by exporting `PUSHOVER_USER_TOKEN`,
`PUSHOVER_APP_TOKEN`, and, optionally, `PUSHOVER_DEVICE_TOKEN`

```python
from pushover import Pushover

po = Pushover(message="message",title="title")
po.send()
```

### Lineage

- <https://github.com/pix0r/pushover>
- <https://github.com/wyattjoh/pushover>
- This repo. There is most definitely no compatibility with previous repos now

## Shell script

For CLI arguments, use `pushover -h`

### Installing with `pipx`

- `pipx install pyshover` will leave you with an isolated binary called `pushover`
- Confirm your install with `pipx list` or `which pushover`

