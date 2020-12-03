XML Pipeline
===

Azure and Python
---

---
> **Author:** Matheus Willian Machado  
> **Date:** Dez 2, 2020
---

Overview
---

> I've a challenge for you [...]  
> this is the program that I need to build  
> read file from blob storage  
> use Azure Functions with Python library to read the xml  
> send data to Azure Event hubs  
>   
> ```xml
> <?xml version="1.0" encoding="UTF-8" ?>
> <root>
> <EventID>42-5221-120212</EventID>
> <EventKey>DELIVERY_SATISFACTION_EVENT</EventKey>
> <MarketID>US</MarketID>
> <RouteNumber>5221</RouteNumber>
> <BusinessUnit>94202</BusinessUnit>
> <DCNumber>42</DCNumber>
> <RestaurantNumber>7975</RestaurantNumber>
> <RestaurantPhoneNumber>3642493</RestaurantPhoneNumber>
> <PlannedArrival>2020-07-30 05:24:00</PlannedArrival>
> <RealArrival>2020-07-30 04:04:12</RealArrival>
> <DeliverySatisfaction>5</DeliverySatisfaction>
> <Driver>Kirk Black</Driver>
> <SigningManager>carl</SigningManager>
> </root>
> ```
>   
> that's it!  
> is this something would be interested to make?  
> [...]  
> this is the data :slightly_smiling_face:  
> you can read straight  
> give me how many hours you're gonna need to build this and document  
> pipeline will be  
> read xml file from blob storage -> using azure functions with python -> send to Azure event hubs -> capture on Azure Stream Analytics  
> (Luan Moreno)

---

Objectives
---

1. [x] Create a file with the xml example
1. [x] Create an Azure Event Hub (AEH)
1. [x] Create an Azure Stream Analytic (ASA)
1. [x] Create an Azure Function (AF)
1. [x] Implement a function to read data from ABS and send to AEH
1. [x] Integrate ASA to read data from AEH 

---

Arquitecture
---

![arquitetura](_img/00_Arquitecture_XMLPipeline.png)

---

Requirements
---

- Azure Subscription
- Visual Studio Code (VSCode)
- Azure Functions Extension
![Azure Functions Extension](_img/01_Requirements_azureFunctionsExtension.png)
- Python Extension
![Python Extension](_img/02_Requirements_pythonExtension.png)

---

Step-by-Step
---

### Creating Everything

First step was to create everything that we would need.

#### File example.xml

You can use any text editor to create the xml example, here was used VSCode.

![example.xml](_img/03_SBS_example-xml.png)

#### Resource Group

In [Azure](https://portal.azure.com), you can create a Resource Groups (RG), so we can organize all the project tools in one place.

![Creating Resource Group](_img/04_SBS_resourceGroup.png)

#### Event Hub

[Create as well an Event Hub](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-create), and we gonna need to [create a send and listen policy](https://docs.microsoft.com/en-us/azure/event-hubs/authorize-access-shared-access-signature) too.

![Creating Event Hub](_img/07_SBS_eventHub.png)

![Creating Event Hub](_img/08_SBS_eventHub.png)

![Creating Event Hub](_img/09_SBS_eventHub.png)

#### Stream Analytics

Next, [create azure stream analytics](https://docs.microsoft.com/en-us/azure/stream-analytics/stream-analytics-quick-create-portal).

![Creating Event Hub](_img/10_SBS_streamAnalytics.png)

#### Azure Functions

Using the VSCode Azure Functions Extension, create a new Project as follows:

![](_img/11_SBS_azureFunctions.png)

Right click this icon ![](_img/12_.png) to create an Azure Function from Template.

- Language: Python
- Interpreter: 3.6
- Template: Azure Blob Storage Trigger
- Settings: Create New (and create a new storage account)

After creation, you will be able to see your function as bellow:

![](_img/13_.png)

You can see the Azure Blob Storage created with the Azure Functions in [Azure Portal](https://portal.azure.com/) on "All Resources" section.

As soon as the function is created, right click on it and select the option "add binding".

- Direction: out
- Binding: Azure Event Hubs
- Name: $return
- Settings: Create new (and select all the settings related to the event hub you created).

Then, check the function.json file, it should look similar to this:

![](_img/17_.png)


---

Azure Functions
---

Create a container with the name of the path that you set on Azure Function creation, in case of doubt check the function.json file in "path" key. In this case we setted the path to "xml/{name}" so we need to create a "xml" container:

![](_img/16_.png)

![](_img/14_.png)

![](_img/15_.png)

In \_\_init__.py file, change it to look like this:

```python

import logging
from json import dumps
import azure.functions as func


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    xml = myblob.read()
    print(xml)
    return dumps({"xml": xml.decode('utf-8')})

```

To test a function inside VSCode one just need to press f5


![](_img/18_.png)

Now, let's upload the example.xml so we can test our function. We gonna do this within the portal for easiness.

![](_img/19_.png)

![](_img/20_.png)

The function should return something like this:

![](_img/21_.png)

Note that we asked the function to print the file content as you can see in the image above.  
We just need to check if Azure Function passed the json result to Azure Event Hub, we gonna look it in Azure Portal as well.

![](_img/22_.png)

As you can see above, there are some activity inside Event Hub.  
Next we'll check it with Stream Analytics.

----

Integrating Event Hubs with Stream Analytics
---

To integrate Event Hub with Stream Analytics, we need to set EH as input. Just follow the steps above.

![](_img/23_.png)

![](_img/24_.png)

![](_img/25_.png)

Once integrated, click on the icon ![](_img/27_.png) to request a sample of the data present in the hub and select a time period compatible with your execution. In this case, we'll select one day of data.

![](_img/26_.png)

![](_img/28_.png)

![](_img/29_.png)

When finished download the sample data

![](_img/30_.png)

And, look! Our example.xml went perfectly through the pipeline!

![](_img/31_.png)

---


References
---

1. <https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal>
1. <https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-create>
1. <https://docs.microsoft.com/en-us/azure/event-hubs/authorize-access-shared-access-signature>
1. <https://docs.microsoft.com/en-us/azure/stream-analytics/stream-analytics-quick-create-portal>
1. <https://docs.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=csharp>

---