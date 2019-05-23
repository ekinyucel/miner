# Twitter Miner

Streaming tweets by the given input parameter from twitter. Produces new messages to Kafka broker. 

# How to run

Add your own config.py file for twitter API credentials & kafka consumer&producer ip address is defined inside config.py file which is not added to remote repository. 
If you want to connect Kafka broker to produce/consume message you have to adde <your-ip-address>:29092 port for configuraton

## Run the producer
- python main.py governmentshutdown

## Spin up the kafka cluster&zookeeper

- docker-compose -f docker-compose.kafka.yml up

## Run the producer & consumer

- docker-compose up