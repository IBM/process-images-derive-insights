# Extract relevant text content from an image and derive insights

This code pattern demonstrates a methodology of deriving insights from scanned documents that has information organized into various sections or layouts.

Some of the scenarios encountered regularly in business are:
- A real estate company which scans newspaper classifieds to extract the individual classifieds. The classifieds appear in different layouts depending on the newspaper.
- In a bank, the supporting documents for a loan are scanned and uploaded. We have to extract some relevant information from the uploaded documents for further processing. Here the information is organized into sections, and the information we want is in one of the sections.
- Employers get scanned copies of certificates, government ids and other documents from employees joining the organization. They are verified for the details.
- In hospitals, a lot of times medical records are scanned and stored. They are later taken up for auditing and analysis. In such a scenario, we need to extract specific information from the records for analysis.

When we use an `OCR` tool directly on an image, we get text that is aggregated and mixed from the various sections. In the above described scenarios, we need to understand the layout and then retrieve only the information from individual sections.

Let us take the first scenario of the real estate company. The real estate classifieds are usually laid out in columns as shown below. Here, the individual classifieds must be identified and then the text content extracted.

![](images/preprocess.png)

Let us build a solution for this scenario to demonstrate our code pattern methodology. We will take a regional newspaper where the classifieds appear in `Hindi` language. This methodology can be extended to any other regional language.

![](images/hindi_preprocess.png)

We need to perform the following steps on the scanned image:
- Extract the individual classified information laid out in columns and rows
- Convert it to text format, translate if required, and extract the required information.

This solution is applicable to other use-case scenarios where we need to extract only relevant portions of text in images and get insights on them.

When the reader has completed this Code Pattern, they will understand how to:

* Containerize OpenCV, Tesseract and Cloud object storage client using an `Appsody` stack, and deploy them on an `OpenShift cluster on IBM Cloud`.
* Pre-process images to separate them into different sections using OpenCV
* Use Tesseract to extract text from an image
* Use Watson language translation to translate the text from `Hindi` to `English`.
* Use Watson Natural language Understanding to derive insights on the text.


<!--add an image in this path-->
![](images/architecture.png)

<!--Optionally, add flow steps based on the architecture diagram-->
## Flow

1. The classifieds image is stored in Object storage, and the jupyter notebook execution is triggered.
2. The Object storage operations microservice is invoked.
3. The classifieds image from Object storage is retrieved.
4. The Image pre-processor service is invoked. The different sections in the image are identified and extracted into separate images each containing only one single classified.
5. The individual classified image is sent to the Text extractor service where the address text is extracted.
6. The extracted address text is sent to Watson Language Translator where the content is translated to English.
7. The translated text in English is sent to Watson Natural Language Understanding where the entities of interest is extracted to generate the required insights.

## Pre-requisites
* [IBM Cloud account](https://www.ibm.com/cloud/): Create an IBM Cloud account.
* [Python 3](https://www.python.org/downloads/): Install python 3.
* [Jupyter Software](https://jupyter.org/install): Install Jupyter Software.
* [Appsody CLI](https://appsody.dev/docs/installing/installing-appsody): Install Appsody CLI.

# Steps

Please follow the below to setup and run this code pattern.

1. [Clone the repo](#1-clone-the-repo)
2. [Create text extractor service](#2-create-text-extractor-service)
3. [Create image pre-processor service](#3-create-image-pre-processor-service)
4. [Create object storage operations service](#4-create-object-storage-operations-service)
5. [Setup Watson Language Translator](#5-setup-watson-language-translator)
6. [Setup Watson Natural Language Understanding](#6-setup-watson-natural-language-understanding)
7. [Run locally](#7-run-locally)
8. [Deploy and run on cloud](#8-deploy-and-run-on-cloud)
9. [Analyze the results](#8-analyze-the-results)

### 1. Clone the repo

Clone this [git repo](https://github.com/IBM/process-images-derive-insights).
Else, in a terminal, run:

```
$ git clone https://github.com/IBM/process-images-derive-insights
```
### 2. Create text extractor service

  #### 2.1 Create an appsody stack with Python Flask and Tesseract support

  Please refer to the below 3 steps in the tutorial [Create a custom Appsody stack with support for Python Flask and Tesseract](https://developer.ibm.com/tutorials/create-a-custom-appsody-stack-with-python-flask-and-tesseract-support/) to create the appsody stack.

a. [Create a copy of an Appsody Python Flask stack](https://developer.ibm.com/tutorials/create-a-custom-appsody-stack-with-python-flask-and-tesseract-support/#1-create-a-copy-of-an-appsody-python-flask-stack)

b. [Modify the Python Flask stack to add support for Tesseract](https://developer.ibm.com/tutorials/create-a-custom-appsody-stack-with-python-flask-and-tesseract-support/#2-modify-the-python-flask-stack-to-add-support-for-tesseract)

c. [Build the stack](https://developer.ibm.com/tutorials/create-a-custom-appsody-stack-with-python-flask-and-tesseract-support/#3-build-the-stack)

   #### 2.2 Create an appsody project using the new stack

  Create a new empty folder say `text_extractor`. Create an appsody project inside the newly created folder by running the below commands:

   ```
   $ cd text_extractor
   $ appsody init dev.local/python-flask-tesseract
   ```

  Copy the file `__init__.py` under the folder `sources/text_extraction/` in this repo that you have cloned.

  Replace file `__init__.py` under folder `text_extractor` with `__init__.py` under the folder `sources/text_extraction/` in this repo that you have cloned.

  #### 2.3 Build and test the project

  Goto the `text_extractor` folder and run the below commands:
  ```
  $ appsody build
  $ appsody run -p 3501:8080 -p 3502:5678
  ```

Open the url http://localhost:3501/home

If it says, `Your text extraction application test is successful` then your application is working fine.
Press Ctrl+C on the terminal to stop the running server.


### 3. Create image pre-processor service

  #### 3.1 Create an appsody stack with Python Flask and OpenCV support

  Please refer to the below 3 steps in the tutorial [Create a custom Appsody stack with support for Python Flask and OpenCV](https://developer.ibm.com/tutorials/create-a-custom-appsody-stack-with-python-flask-and-opencv-support/) to create the appsody stack.

a. [Create a copy of an Appsody Python Flask stack](https://developer.ibm.com/tutorials/create-a-custom-appsody-stack-with-python-flask-and-opencv-support/#1-create-copy-of-python-flask-stack)

b. [Modify the Python Flask stack to add support for Tesseract](https://developer.ibm.com/tutorials/create-a-custom-appsody-stack-with-python-flask-and-opencv-support/#2-modify-the-python-flask-stack-to-add-support-for-opencv)

c. [Build the stack](https://developer.ibm.com/tutorials/create-a-custom-appsody-stack-with-python-flask-and-opencv-support/#3-build-the-stack)

 #### 3.2 Create an appsody project using the new stack

  Create a new empty folder say `image_preprocessor`. Create an appsody project inside the newly created folder by running the below commands:

   ```
   $ cd image_preprocessor
   $ appsody init dev.local/python-flask-opencv
   $ mkdir images
   ```

  Copy the files `__init__.py` and `improcess.py` under the folder `sources/image_preprocessor/` in this repo that you have cloned.

  Replace file `__init__.py` under folder `image_preprocessor` with `__init__.py` under the folder `sources/image_preprocessor/` in this repo that you have cloned.

  Replace file `improcess.py` under folder `image_preprocessor` with `improcess.py` under the folder `sources/image_preprocessor/` in this repo that you have cloned.

#### 3.3 Build and test the project

  Goto the `image_preprocessor` folder and run the below commands:
  ```
  $ appsody build
  $ appsody run -p 4501:8080 -p 4502:5678
  ```

  Open the url http://localhost:4501/home

  If it says, `Your image preprocessor application test is successful` then your application is working fine. Press Ctrl+C on the terminal to stop the running server.

### 4. Create object storage operations service

 #### 4.1 [TODO - Link tutorial steps]

 #### 4.2 Create an instance of IBM Cloud Object Storage

Create an instance of [IBM Cloud Object Storage](https://cloud.ibm.com/catalog/services/cloud-object-storage).

![createos](images/create_os.png)

Create credentials for the newly created Cloud Object service

* Click on `Credentials`
* Click on `New Credential`. Make a note of the newly created credential in json format.

![createcred](images/create_credentials.png)

Create a bucket and upload an image to the bucket

* Click on `Buckets`
* Click on `Create bucket`

![createbucket](images/create_bucket.png)

* Select `Standard` under `Predefined buckets`

![standardbucket](images/standard_bucket.png)

* Give a name under `Unique bucket name` like `classifieds` and click on `Next`

![uniquename](images/uniquename.png)

* Click on `Browse and upload` and upload the image `newspaper_hindi.jpg` under `sources/object_storage_operations/` in this repo that you have cloned and click on `Next`.

![uploadimage](images/uploadimage.png)

* Click on `Next` in `Test bucket out` section.

* In `Summary` section click on `View Buckets` and search for your bucket `classifieds` in the search tab.

![viewbuckets](images/view_buckets.png)

* When you click on your bucket, it should show `newspaper_hindi.jpg` image in the bucket.

![newspaperimage](images/newspaper_image.png)

* You have now successfully created a bucket and uploaded an image.

#### 4.3 Create an appsody project using the new stack

Create a new empty folder say `object_storage_operations`. Create an appsody project inside the newly created folder by running the below commands:
 ```
 $ cd object_storage_operations
 $ appsody init dev.local/python-flask-os ostemplate
 ```
The files `Pipfile`,`osclient.py` and `config.ini` are created under the `object_storage_operations` folder.

Copy the files `__init__.py` under the folder `sources/object_storage_operations/` in this repo that you have cloned.

Place file `__init__.py` under folder `app3` with `__init__.py` under the folder `sources/object_storage_operations/` in this repo that you have cloned.

 * The file `__init__.py` has REST interfaces exposed to test the Cloud Object Storage operations.

Modify the contents of config.ini with the credentials that we created earlier.

Credentials we noted earlier on IBM Cloud:
![credentials](images/os_service_credentials.png)

The relevant portions indicated in the credentials are entered into the `config.ini` as shown below:

![config](images/config.png)

Modify the `COS_BUCKET_LOCATION` appropriately. The list of valid location constraints can be found [here](https://cloud.ibm.com/docs/services/cloud-object-storage?topic=cloud-object-storage-classes#classes-locationconstraint).

#### 4.4 Build and test the project

  Goto the `object_storage_operations` folder and run the below commands:
  ```
  $ appsody build
  $ appsody run -p 5501:8080 -p 5502:5678
  ```

  Open the url http://localhost:5501/home.

  If it says, `Your object storage operations application test is successful` then your application is working fine. Press Ctrl+C on the terminal to stop the running server.

### 5. Setup Watson Language Translator

Create an instance of [IBM Language Translator](https://cloud.ibm.com/catalog/services/language-translator).

![](images/create_lt.png)

Copy the `Credentials`, both `API Key` and `URL` as shown below and make a note of them. We will use them in step 7.

![](images/create_lt_credentials.png)

### 6. Setup Watson Natural Language Understanding

Create an instance of [IBM Natural Language Understanding](https://cloud.ibm.com/catalog/services/natural-language-understanding).

![](images/create_nlu.png)

Copy the `Credentials`, both `API Key` and `URL` as shown below and make a note of them. We will use them in step 7.

![](images/create_nlu_credentials.png)

### 7. Run locally

 #### Start the services

 Goto the `text_extractor` folder and run the below commands:
  ```
  $ appsody run -p 3501:8080 -p 3502:5678
  ```
 Goto the `image_preprocessor` folder and run the below commands:
  ```
  $ appsody run -p 4501:8080 -p 3502:5678
  ```
 Goto the `object_storage_operations` folder and run the below commands:
  ```
  $ appsody run -p 5501:8080 -p 3502:5678
  ```

 #### 7.2 Set up and run jupyter notebook

 * Launch jupyter notebook.
 * Upload `process_image_insights.ipynb` which is under `notebook` folder in this repo that you have cloned.
 * Goto `section 1.3` in the notebook.

 ![](images/notebook_news.png)

 * Specify the urls for the `text_extractor`(http://localhost:3501), `image_preprocessor`(http://localhost:4501) and `object_storage_operations`(http://localhost:5501). 
 * Fill the Language translator and Natural language understanding credentials that you have noted in step 5 and step 6 accordingly.

 * Click on `Run All` under `Cell` tab. Else you can run the notebook cell by cell by clicking on `Run` on each cell.

### 8. Deploy and run on cloud

#### 8.1 Login to IBM Cloud

    ```
    ibmcloud login
    ```
    
#### 8.2 Add a namespace to create your own image repository. Replace <my_namespace> with your preferred namespace.

    ```
    ibmcloud cr namespace-add <my_namespace>
    ```
    
#### 8.3 To ensure that your namespace is created, run the ibmcloud cr namespace-list command.

    ```
    ibmcloud cr namespace-list
    ```
    
#### 8.4 Tag the docker image. Replace the placeholder with the region of the container registry.

    ```
    docker tag dev.local/text-extractor:latest <region>.icr.io/<my_namespace>/text-extractor:latest
    docker tag dev.local/image-preprocessor:latest <region>.icr.io/<my_namespace>/image-preprocessor:latest
    docker tag dev.local/object-storage-operations:latest <region>.icr.io/<my_namespace>/object-storage-operations:latest
    ```
    
#### 8.5 Push the docker images into your namespace. Replace the placeholders for region, namespace with your container registry region and the namespace created earlier. 

    ```
    ibmcloud cr login
    docker push <region>.icr.io/<my_namespace>/text-extractor:latest
    docker push <region>.icr.io/<my_namespace>/image-preprocessor:latest
    docker push <region>.icr.io/<my_namespace>/object-storage-operations:latest
    ```
#### 8.6 Create an instance of OpenShift cluster on IBM Cloud

Create a OpenShift cluster [here](https://cloud.ibm.com/kubernetes/catalog/openshiftcluster).
![](images/openshift_create.png)

 #### 8.7 Open the OpenShift console

![](images/open_console.png)

 #### 8.8 Log in to OpenShift using the CLI and create a new project

![](images/copy_login_command.png)

Run the command.

#### 8.9. Create a deployment configurations files  for the three services with the below contents. 

Create three deployment configuration files - text_extractor_deploy.yaml,image_preprocessor_deploy.yaml and object_storage_operations_deploy.yaml.
Replace the region, namespace, service name with your container registry region, the namespace created earlier and service name(text-extractor / image-preprocessor / object-storage-operations)  
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <service name>-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: <service name>
  template:
    metadata:
      labels:
        app: <service name>
    spec:
      containers:
      - name: <service name>
        image: <region>.icr.io/<namespace>/<service name>:latest
    ports:
    - containerPort: 8080
      protocol: TCP
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: <service name>
  name: <service name>
spec:
  ports:
  - port: 8080
    protocol: TCP
    targetPort: 8080
    name: web
  selector:
    app: <service name>
  type: ClusterIP
```

#### 8.11 Create the deployments in your cluster.

    ```
    oc apply -f text_extractor_deploy.yaml
    oc apply -f image_preprocessor_deploy.yaml
    oc apply -f object_storage_operations_deploy.yaml
    ```
    
#### 8.12  Create a route for the services.

    ```
    oc expose service/text-extractor
    oc expose service/image-preprocessor
    oc expose service/object-storage-operations
    ```
    
#### 8.13 Get the route for the service   

    ```
    oc get routes
    ```
    
You will see the route to the service as seen below:
```
NAME    HOST/PORT           PATH                                                                      SERVICES                 PORT   TERMINATION   WILDCARD
text-extractor              text-extractor-default...us-south.containers.appdomain.cloud             text-extractor                  web           None
image-preprocessor          image-preprocessor-default...us-south.containers.appdomain.cloud         image-preprocessor              web           None
object-storage-operations   object-storage-operations-default...us-south.containers.appdomain.cloud  object-storage-operations       web           None
```
Note down the urls under `PATH` column for the services as shown.

 #### 8.14 Create an instance of Watson Studio

Create an instance of Watson Studio [here](https://cloud.ibm.com/catalog/services/watson-studio)
![](images/ws_create.png)

Click `Create`.

 #### 8.15 Import the notebook and configure

Create a new project `insights` by selecting `New Project`.

![](images/create_project.png)

Select `Add to project` and `Notebook`.

![](images/create_notebook.png)

Import the notebook `process_image_insights.ipynb` which is under `notebook` folder in this repo that you have cloned. Click `Create notebook`.

![](images/import_notebook.png)

Goto `section 1.3` in the notebook.

 ![](images/notebook_news.png)

 * Specify the urls for the `image_preprocessor`, `text_extractor` and `object_storage_operations`.
 * Fill the Language translator and Natural language understanding credentials that you have noted in step 5 and step 6 accordingly.
 * Click on `Run All` under `Cell` tab. Else you can run the notebook cell by cell by clicking on `Run` on each cell.

### 9. Analyze the results

In section 2.1 of the notebook, we have retrived the required image `newspaper_hindi.jpg` from the Cloud Object Storage.

![](images/result1.png)

In section 3.1 of the notebook, we have preprocessed the image using opencv to detect different addresses in the newspaper.

![](images/result2.jpg)

In section 4.1 of the notebook, we have extracted all the different addresses that were detected after the preprocessing using tesseract.

![](images/result3.png)

In section 5.1 of the notebook, we have translated all the extracted addresses using `Watson Language Translator` service. This will help us in data processing and analytics.

![](images/result4_1.jpg)
![](images/result4_2.jpg)
![](images/result4_3.png)
![](images/result4_4.jpg)

In section 6.1 of the notebook, we have used `Watson Natural Language Understanding` service to derive insights from the data.
In our case, the insights uncovers that `50% of the detected addresses are from Karnataka state`, `25% of the detected addresses are from West Bengal state` and the other `25% of the detected addresses are from Maharashtra state`. We can also choose to see comparision between two states, like between Karnataka and Maharashtra.

![](images/result5.png)

In section 7.1 of the notebook, we can search for addresses in the newspaper based on the location name. Type an address in the location text box and press enter. It will return you all the addresses in the newspaper from the specified locality .

![](images/result6_1.png)

Lets type `Karnataka` and press enter,

![](images/result6_2.png)

Similarly, lets now try with `West Bengal` and press enter,

![](images/result6_3.png)


# Related Content

1. [Create a custom Appsody stack with support for Python Flask and Tesseract](https://developer.ibm.com/tutorials/create-a-custom-appsody-stack-with-python-flask-and-tesseract-support/)

2. [Create a custom Appsody stack with support for Python Flask and OpenCV](https://developer.ibm.com/tutorials/create-a-custom-appsody-stack-with-python-flask-and-opencv-support/)

3. TODO - Add Object storage tutorial link

## License

This code pattern is licensed under the Apache License, Version 2. Separate third-party code objects invoked within this code pattern are licensed by their respective providers pursuant to their own separate licenses. Contributions are subject to the [Developer Certificate of Origin, Version 1.1](https://developercertificate.org/) and the [Apache License, Version 2](https://www.apache.org/licenses/LICENSE-2.0.txt).

[Apache License FAQ](https://www.apache.org/foundation/license-faq.html#WhatDoesItMEAN)
