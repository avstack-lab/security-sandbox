# AV Security Sandbox

A development environment for security analysis in autonomous vehicles.


## Runnables

To interact with simulators, it is often most convenient to run our attacker in its own process (and/or in a Docker container). To model communications over this interface, we set up sockets that send and receive data between the system and the attacker.


### Socket Demo

We've set up a simple socket demonstration to illustrate what this sending and receiving of data looks like. To run the demo, do the following:

In terminal 1, run:
```
poetry run python runnables/run_test_lidar_server.py
```

In terminal 2, run:
```
poetry run python runnables/run_test_lidar_client.py
```

You'll see that the server sends the data to the client, the client performs some "operation", and then sends back the data to the server. The server, in this case, waits until it has received the data back from the client until it continues.


### Running Attacks

Each attack is given a configuration YAML file where the parameters are defined. Each attack is set up to run via a simple Makefile command. Check the Makefile for the most up to date instances of the attack runnables