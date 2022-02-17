# python_kafka

Python kafka beautiful sopu tutorial

Quick start with Kafka

#

kafka

#

beginners

#

macos

#

streaming
Just a quick introduction about Kafka. Apache Kafka is a framework implementation of a software bus using stream-processing. It is an open-source software platform developed by the Apache Software Foundation written in Scala and Java. The project aims to provide a unified, high-throughput, low-latency platform for handling real-time data feeds. Wikipedia

So you can use Kafka for streaming real time data, message or for a ETl application and many more types eg. Netflix heavily use Kafka.

Kafka general concept:
Producer -> kafka borker -> topic -> consumer

So producer can create stream of messages for a specific topic. And that topic can be send almost real time to consumer which subscribed to that topic.

How to install and start Kafka:
As kafka is depends on zookeeper [Apache ZooKeeper is an open-source server for highly reliable distributed coordination of cloud applications. It is a project of the Apache Software Foundation. Wikipedia]. So need to install zookeeper as well.
But first we need to install Java. I am installaing in mac, almost similar process for other operating system as well.

brew install java
brew install kafka
It will install kafka along with all dependencies including zookeeper.

Then we need to run zookeeper in one tab of terminal by running the following command zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties

Open another tab and run kafka by running the following command kafka-server-start /usr/local/etc/kafka/server.properties

Open another tab and create a topic on which we can test the both producer and consumer activity.
kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test
Then run producer to send message kafka-console-producer --broker-list localhost:9092 --topic test
It will open for you to send messages. Wait and open another tab.
Run consumer kafka-console-consumer --bootstrap-server localhost:9092 --topic test --from-beginning

And then go back to producer and send some message and see them immediately in consumer tab.
