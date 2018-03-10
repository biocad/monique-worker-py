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

## run worker example
Run all needed services from [monique repository](https://github.com/biocad/monique-queue) (but not workers).

Run worker with following command:
```bash
python3 examples/exampleA.py --config examples/configA.json
```

## run component example
Again, run all needed services from [monique repository](https://github.com/biocad/monique-queue).

Run userdata receiver with command:
```bash
python3 examples/userdata_receiver.py --config examples/userdata_receiver.json
```

Run userdata sender with command:
```bash
python3 examples/userdata_sender.py --config examples/userdata_sender.json
```