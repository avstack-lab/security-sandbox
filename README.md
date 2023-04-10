# AV Security Sandbox

A development environment for security analysis in autonomous vehicles.


## Requirements/Installation

Ensure that when you clone the repository you also clone the submodules:

```
git clone --recurse-submodules https://github.com/avstack-lab/security-sandbox
```

### Download Data

Some attacks require you to download some attack trace data. See the `data` folder and run the shell scripts in that folder to download the data.

### Choice 1: Natively

Running this repository natively is only available on a Linux machine. It also currently only works with `python3.8`, so if you don't have `python3.8` installed, you'll need to run something like:

```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.8 python3.8-dev python3.8-distutils
```
(the above may not be exhaustive, but should get you started)

To run this repository natively on your machine, you must have [`poetry`][poetry] installed and available. Once you have downloaded and installed  [`poetry`][poetry], you can run the make command to install as follows:
```
make install
```

That's it!


### Choice 2: Docker

To use the provided docker container, you must have the [NVIDIA Container Toolkit][nvidia-container] installed. Additionally, the docker container is beefy - it bases on the nvidia container and then install [`avstack`][avstack-core] and [`avapi`][avstack-api] as development submodules. It is about 16 GB in size, so prepare for a lengthy pull process the first time. **NOTE:** The pull process happens inside `run_docker.sh`. 


## Runnables

To interact with simulators, it is often most convenient to run our attacker in its own process (and/or in a Docker container). To model communications over this interface, we set up sockets that send and receive data between the system and the attacker.


### Socket Demo

We've set up a simple socket demonstration to illustrate what this sending and receiving of data looks like. To run the demo, do the following:

In terminal 1, run: `make run_test_server`

In terminal 2, run: `make run_test_server`

You'll see that the server sends the data to the client, the client performs some "operation", and then sends back the data to the server. The server, in this case, waits until it has received the data back from the client until it continues.


### Running Attacks Through Terminal (natively)

Each attack is given a configuration YAML file where the parameters are defined. Each attack is set up to run via a simple Makefile command. Check the Makefile for the most up to date instances of the attack runnables.

#### Running Passthrough Attack

In terminal 1, run the test server (or your own server):
```
make run_test_server
```

In terminal 2, run the passthrough attacker:
```
make run_attacker_passthrough
```

#### Running False Positive Attack

In terminal 1, run the test server (or your own server):
```
make run_test_server
```

In terminal 2, run the passthrough attacker:
```
make run_attacker_passthrough
```

### Running Attacks Through Docker

Let's say you're on a brand new machine and you want to set this up as quickly as possible. We've created a docker container to help expedite running these attacks. To run the attacks through the docker container, you would do the following:


In terminal 1, run the test server (or your own server):
```
make run_test_server_without_poetry  # NOTE: this is the same as run_test_server, just without ensuring the exact same environment. Use at your own risk
```

In terminal 2, run the docker container: `bash run_docker.sh`. This will get you into an interactive docker container. Inside the docker container, you can run any of the attackers, such as `make run_attacker_passthrough` or `make run_attacker_fp`.


[avstack-core]: https://github.com/avstack-lab/lib-avstack-core
[avstack-api]: https://github.com/avstack-lab/lib-avstack-api
[nvidia-container]: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html
