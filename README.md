# Motivation

This project gives an example of my thoughts on best practices on how to structure an ML project. 

A good ML practitioner should always be thinking of these things

- What problem am i trying to actually solve, what is the business value?
- How easy is it for someone to pick up my work?
- How can i get this into production as quickly as possible to add value?

There is no point having a load of notebooks which "work on my machine" but can't be turned into a product for adding business value.
Primarily the output of my own work is in integrating ML models into systems however i think this ethos is equally valid if your outputs are reports.
Could someone replicate this? Could they pick it up and build on it? If this report is valuable it probably needs to be run at intervals,
That should be done by an automated process and not some notebooks being rerun on your personal machine.

Whether you identify as a data scientist or any other type of ML practition you should be aiming to cultivate a skillset where you can get your model into a usable state for other people to work with.

I think as a data scientist even if you're not an amazing engineer (and i am not) you should be aiming to minimise the 

The 2 most common ways to get an ML model into production are

- Wrapping it in a microservice to provide an endpoint via HTTP or RPC
- Embedding the model directly in data processing code (This is often as a spark UDF)

The 2nd method couples you directly to the application code and makes thing such as A/B testing significantly harder.
It also requires you to have some data processing environment in your production system and that is often not the case.
This is why i would always favour the first approach as it allows flexibility for you to deploy new versions of your model more easily and provides a clean interface for the other parts of the system.

N.B There may be performance requirements which require you to embed your model directly but this is going to rarely be the case 
N.B you can always call the endpoint

# Technical thoughts
- Always push as much preprocessing into the model artifact to minimise  (this is true whether it's a spark pipeline, scikit-learn pipeline or tensorflow transforms)
    If you don't this will always come back to bite you in the arse. If all code is in the pipeline we know that the implementation in the production version will be the same as in training and the inputs your model receives will be the same as the ones it was trained on
    These sort of errors are insidious an can often be hard to identify but catestrophic
     (if you lower case  text in your training but then don't in the production system, your inputs will never match the training ones)
    TODO: (spark pipeline example or is that not specific enough to this)
- If you can't put it in the model artifact, write it in a way that you can import it directly into the production system (or at worst directly copy and paste it)
- If we're exposing an endpoint then we want the client to only have to send us raw inputs, then we can validate the structure and maintain control over the process from input to output(cleaning code is ML code therefore should live in the ML service)


# Project Components

This project contains all the steps to go from a dataset to a production system whilst emphasising reproducability and testability.

### train
The train folder contains the code for exploring a dataset and creating a model artifact. This is split into

- EDA
- Model Selection
- Final Model

Notebooks are great for exploring data but not so good for writing production code (and the code for training your model IS production code!)

### app
This shows a lightweight microservice for taking a model artifact and exposing it through an endpoint 
(i hesitate to say REST as it's just json over http).

It uses docker so whoever is deploying your model (you/devops) only needs to support Docker and we can. 

There are often conflicting desires from ML practitioners and OPs. You want to use the latest greatest technologies and 
OPs want to keep it stable with as few new technologeis to support. All OPs need to support is docker and you have the 
freedom to use whatever technologies you want. This is without getting into the advantages of kubernetes.


# Project Limitations
I will admit i specifically chose a toy dataset and in the real world data lives in many places structured or unstructured. 
However this workflow remains valid as this code for extracting the data would fit before the EDA step.

### Using other technologies

I have used scikit-learn in the project which means the serialization of the model and loading it into the microservice is easy enough.
Other technologies require a little bit more work (Tensorflow, Spark) but they can be saved to different serialisation standards (PMML, ONNX, PFA, MLeap) 
and loaded into memory of prebuilt containers (openscoring, tensorflow-serving).

### Model Storage and CI/CD
In this example i have directly saved the model in the output folder. In the real world this would not be the case. 

The model should be saved to an accessible location (FTP site, Google Storage, S3) then at runtime it can be downloaded to a volume on the container.

There are many advantages to this. 
- When you train the model and save it to the storage bucket you only need to update the model_location in the download script.
- You are not cluttering git storage
- Your CI process can run tests by building the Docker container and downloading the model before running the tests (this can include validation data sets and performance testing)
