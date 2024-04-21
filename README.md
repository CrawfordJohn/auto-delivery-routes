<H1> COP3530 - Project 3 - Optimizing Autonomous Delivery Service Routes for Efficient Service </h1>

**Background:** We are a delivery company testing out a new form of automated delivery using a self-driving car. Due to a new law, this operation is only legal within the city of Miami. Unfortunately, our vehicle is really small, and can only handle one order at a time. Orders are randomly generated from a set of ~100,000 distinct points across the state of Florida, and our task is to find the shortest distance between our previous delivery location and the new, randomly generated one using the existing network of roads. Our self-driving car drives at a constant speed of 50mph, and can drive on all types of roads, including highways. This constant speed means that we are only concerned with minimizing the distance on these drives. The problem we are trying to solve is finding the shortest distance between deliveries using roads, so that we can deliver our orders as fast as possible.

<h2> Data Collection </h2>

Our data was queried from [OpenStreetMap](https://www.openstreetmap.org/#map=5/29.037/-75.410), a large map dataset similar to Google Maps that is open-source and free to use. You can specifically query all roads within a specific latitude and longitude so that you do not have to download all of the data just to get what you are looking for.

The latitude, longitude, and OpenStreetMap ID of each distinct delivery point we used can be found in the [nodes.csv](https://github.com/CrawfordJohn/auto-delivery-routes/blob/main/nodes.csv) file, and the roads that connect these delivery points can be found in [edges.csv](https://github.com/CrawfordJohn/auto-delivery-routes/blob/main/edges.csv)


<h2> Alogirthm Comparison </h2>

We placed each delivery point as a node in a graph and the streets as edges in the graph and used Dijkstra's Algorithm and the Bellman-Ford algorithm to find the shortest distance from one delivery point to another. 

<h2> Instructions for Running Code </h2>

To run this code on your own laptop, run these commands on your CLI

```
git clone https://github.com/CrawfordJohn/auto-delivery-routes.git
```

Once you have cloned the repository into your local IDE, you can configure your local python interpreter and create a virtual environment with the requirement.txt file

To create a virutal environment, run the following commands on your CLI (Windows):

```
cd auto-delivery-routes
```

```
py -m venv <env_name>
```

<env_name> can be any desired name for your environment.
Make sure to exclude the caret marks (<>).

```
.\<env_name>\Scripts\activate
```

```
pip install -r requirements.txt
```

Now, you can open and run app.py on your local IDE (such as PyCharm).
Your IDE will provide a link to a local host where you can view the web application.

![image](https://github.com/CrawfordJohn/auto-delivery-routes/assets/64513150/8391f100-e81b-445c-8495-ff1c32f2fde7)



<h2> User Interface </h2>

![image](https://github.com/CrawfordJohn/auto-delivery-routes/assets/64513150/d51f4dc7-08a3-457c-9d3f-56e903ecae4a)

Once you have opened the link to the local host, a map will pop up randomly generating your start location (symbolized by the car icon) and a delivery destination (symbolized by the blue marker). You can click on the _Dijkstra_ or _Bellman Ford_ buttons to calculate the shortest path from the start location to the destination using both algorithms. A pop-up in the lower right hand corner will tell you how much time it took for the algorithm computing the shortest path to run. To make your next delivery, press the _Make Next Delivery!_ button.

![image](https://github.com/CrawfordJohn/auto-delivery-routes/assets/64513150/5750574b-1a76-409d-a012-5dd9a258952a)

![image](https://github.com/CrawfordJohn/auto-delivery-routes/assets/64513150/16ad45d8-cb56-4554-8297-433097b2e893)



