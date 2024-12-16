# Project IGDB: An Exploration of Learning ETL
**Author:** [Ehow Chen](https://github.com/ehowc)

**Last Updated:** December 15, 2024

## What is this project for?
This project is a demonstration of how to utilize cloud services to create a data engineering project from scratch. It is part of a guided course on Maven by [David Freitag](https://github.com/dkfreitag), which you can find [here](https://maven.com/david-freitag/first-serverless-de-project). The goals of creating this project include learning about various tools within Amazon Web Services (AWS), how they can be combined to create a compete workflow for extracting, transforming, and loading (ETL) data from online sources, and connect the transformed data to a tool for visualization. The process applied attempts to be as cost-effective and quick-to-query as possible so costs are contained with an increasing scale of data.

Perhaps more importantly, this project is about expanding my horizons and growing as a data professional. I enriched this project with my personal interests by learning how to use the [Internet Game Database (IGDB) API](https://www.igdb.com/api). This document doesn't dive deeply into the code but instead focuses on the broader picture of what is being used and why.

## Data Architecture 

The bulk of the this project uses AWS, with a bit of Python to process the data in a format that processes properly. Some of the tools are not necessary in principle given the "on-demand" nature of the data collection, but they can be applied in robust settings like a live data stream.
* Extract: Lambda, Firehose, S3, Python, Athena
* Transform: S3, Athena, Glue
* Load: S3, Athena, Glue, Grafana

![The architecture diagram for this project, featuring AWS and Grafana. Diagram generated using Draw.io.](images/project_igdb_architecture.png)

## API

This project uses data from the IGDB API, whose [site](https://www.igdb.com/api) clearly describes the steps to gaining access to the database. I found that using [Postman](https://www.postman.com/) helped me understand the nature of POST requests to use in the Python code.
* You are required to have a Twitch Developer account to generate credentials with IGDB using the POST request method.
* To narrow the scope of the query and analysis, the queries limited games to:
  * Nintendo platforms
  * Having at least 50 ratings from users and publications

The following fields were queried from the API:
* id (int): the unique ID of the game from IGDB
* first_release_date (timestamp): the date the game was initially released
* name (string): the name of the game
* total_rating (float): the average rating of the game across user and professional ratings
* total_rating_count (int): the total number of ratings
* last_updated (timestamp): code-generated timestamp when the code is run to call the API

## Extraction

Data extraction in a serverless environment is relatively straightforward. We need the following components:
* Storage: AWS S3 is our primary service to store data, as it is both cost effective and plays well with the rest of the AWS tools.
* Collection: Lambda utilizes Python code to call data from the IGDB API using Python. For the purposes of this project, we use Lambda to post requests in an "on-demand" basis.
* Regulation: Firehose enables us to collect data in situations where large amounts of data are constantly being called by Lambda and we wish to minimize computing costs to transfer the data. This particular tool is not necessary given the on-demand nature of the project, but it is included for the sake of learning how to use it.
* Inspection: Athena allows us to use SQL to examine the data being received and create a database structure to it.

At a very high level, the process goes as follows.
1. An S3 bucket is created, dedicated to the data that is received.
2. A firehose is created, which points to the S3 bucket.
3. A process is written in Lambda using Python code to call the API and point the data to the firehose. The Python code used to call the API can be found [here](lambda/get_igdb_data_lambda.py).
4. Athena is used to verify the data within the S3 bucket. (A database and an S3 bucket need to be created to query.)

Once the extracted data is verified to be as expected, we can move onto...

## Transformation

Data transformation in AWS can be approached many different ways, including third-party tools. This project uses Glue to minimize costs and simplify the flow, but tools like EC2 can be used for more complex processes.

Glue actually serves two purposes for Transformation:
1. Crawl the data to automate a data catalog for the extracted data from S3.
2. Write, update, and check a production table in a workflow using the crawled data.

Crawling data with Glue is relatively straightforward: you choose the S3 bucket with the extracted data and need to assign the Athena database. This enables Glue to automatically create a table to be referenced by the workflow.

Establishing the workflow is a bit more compelx



* id (int):
* first_release_date (timestamp):
* name (string): 
* total_rating (float):
* total_rating_count (int):
* last_updated (timestamp): 
* release_year (int):


## Loading & Visualizing the Data



[Link to Project IGBD's Grafana Snapshot](https://ehowconsults.grafana.net/dashboard/snapshot/2EuZOXr4pB4noHQbvUNC5LGuQNIpiUuf)

## Shortcomings & Improvements

