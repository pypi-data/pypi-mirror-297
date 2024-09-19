# expressive

A library for quickly applying symbolic expressions to NumPy arrays

Inspired in part by this Stack Overflow Question [Using numba.autojit on a lambdify'd sympy expression](https://stackoverflow.com/questions/22793601/using-numba-autojit-on-a-lambdifyd-sympy-expression)

## installation

via pip https://pypi.org/project/expressive/

```shell
pip install expressive
```

## usage

refer to tests for examples for now

generally follow a workflow like
* create instance `expr = Expressive("a + log(b)")`
* build instance `expr.build(sample_data)`
* instance is now callable `expr(real_data)`

The `data` should be provided as dict of NumPy arrays

```python
data = {
    "a": numpy.array(range(1_000_000), dtype="int64"),
    "b": numpy.array(range(1_000_000), dtype="int64"),
}
```

## testing

#### install dependencies

Only docker and compose (v2?) are required (used to generate the test environment)

```shell
sudo apt install docker.io docker-compose-v2
```

#### run tests

Just directly run the test script from the root of the repository, it will build the docker test environment and run itself inside it automatically

```shell
./test/runtests.sh
```

## contributing

Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) and [LICENSE.txt](LICENSE.txt)

## version history

##### v1.2.0
* enable autobuilding (skip explicit `.build()` call)
* basic display support for `Expressive` instances

##### v1.1.1
* add version history block

##### v1.1.0
* fixed bug: signature ordering could be unaligned with symbols, resulting in bad types
* added support for non-vector data arguments

##### v1.0.0

* completely new code tree under Apache 2 license
* basic support for indexed offsets

##### v0.2.0 (unreleased)

##### v0.1.0

* very early version with support for python 3.5
