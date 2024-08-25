# Malstrom

Solving ARC with neural networks


## Dependencies

- [JSON parser](https://github.com/nlohmann/json)


## Build

Using [meson](https://pypi.org/project/meson/) build system

```bash
meson setup builddir
meson configure --prefix $(pwd) builddir
meson compile -C builddir
```


https://gist.github.com/p-i-/9ebed4917d5ea61674e536896fe0aa83