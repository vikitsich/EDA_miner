<img src="https://raw.githubusercontent.com/KMouratidis/EDA_miner/master/y2d.png" width="250" align="left">

# EDA_miner

A visualization and analytics dashboard that is able to connect to APIs, receive your data,
and allow you to run Machine Learning models from a server. Started as a university project.

### Run with Docker:

To run with docker you can use our Dockerfile which only requires that you have a Redis server running on port 6379 on your host machine. Currently, the build only works with anaconda (contributions/suggestions are welcome; I'm a complete novice in Docker). Then run these two commands and you're all set.

```
>> sudo docker build -t kmouratidis/EDA_miner_docker .
>> sudo docker run --network host -p 8889:5000 kmouratidis/EDA_miner_docker
```

<br>

### Example of the Data View Tab:

![](https://i.imgur.com/FFogpHt.png)

### Example of the Explore & Visualize Tab:

![Interface options 2](https://i.imgur.com/zMMcDwp.png)

### Example of the Analyze & Predict Tab:

![Interface options 3](https://i.imgur.com/RNqpfo9.png)

