# monique-worker-py
Wrapper for Monique worker (Python)

## build
Library `pyzmq` required. It can be installed with command
```bash
pip3 install pyzmq
```
Library with worker wrapper required. It can be installed from current directory with command
```bash
python3 setup.py install
```

## run examples
Run all needed services from [monique repository](https://github.com/biocad/monique-queue) (but not workers).

Run worker with following commands:
```bash
python3 examples/exampleA.py --config examples/configA.json
```
