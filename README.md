# Invoice_creation
Invoice data handling management screen and creating invoices(Refer Invoice-app.rar in my repository)

# Django REST with React: setting up a Python virtual environment, and the project

First things first make sure to have a Python virtual environment in place. Create a new folder and move into it:

```
mkdir django-react && cd $_
```

Once done create and activate the new Python environment:
```
python3 -m venv venv
source venv/bin/activate
```
NOTE: from now on make sure to be always in the django-react folder and to have the Python environment active.

Now let's pull in the dependencies:
```
pip install django djangorestframework
```
When the installation ends you're ready to create a new Django project:
```
django-admin startproject django_react
```
# Django REST with React: building a Django application


A Django project can have many applications. Each application ideally should do one thing. Django applications are modular and reusable, if another project needs the same app over and over we can put that app in the Python package manager and install it from there.

To create a new application in Django you would run:

```
django-admin startapp leads
```

This will create our new leads app in the django-react folder. Your project structure now should be:
```
(venv) your@prompt:~/Code/django-react$ tree -d -L 1
.
├── django_react
├── leads
└── venv
```
Now let’s tell Django how to use the new app. Open up django_react/settings.py and add the app in INSTALLED_APPS:
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'leads.apps.LeadsConfig', # activate the new app
]
```
# Django REST with React: creating a Django model

Open up leads/models.py and create the Lead model:

```
from django.db import models

class GeneratePDF(models.Model):
    invoice_num =models.CharField(max_length=30)
    client_name =models.CharField(max_length=30)
    client_email=models.CharField(max_length=30)
    project_name=models.CharField(max_length=30)
    Amount_charged=models.IntegerField()

    def __str__(self):
        return self.invoice_num
 ```
 
When planning a model try to choose the most appropriate fields for your use case. And with the model in place let's create a migration by running:

```
python manage.py makemigrations leads
```
and finally migrate the database with:
```
python manage.py migrate
```
# Django REST with React: Django REST serializers

What is serialization? What is a Django REST serializer? Serialization is the act of transforming an object into another data format. After transforming an object we can save it to a file or send it through the network.

Why serialization is necessary? Think of a Django model: it's a Python class. How do you render a Python class to JSON in a browser? With a Django REST serializer!

A serializer works the other way around too: it converts JSON to objects. This way you can:

display Django models in a browser by converting them to JSON
make CRUD request with a JSON payload to the API
To recap: a Django REST serializer is mandatory for operating on models through the API. Create a new file named leads/serializers.py. The LeadSerializer takes our Lead model and some fields:

```
from rest_framework import serializers
from .models import GeneratePDF

class GeneratePDFSerializers(serializers.ModelSerializer):

    class Meta:
        model= GeneratePDF
        fields=('invoice_num','client_name','client_email','project_name')
        
 ```
 As you can see we're subclassing ModelSerializer. A ModelSerializer in Django REST is like a ModelForm. It is suitable whenever you want to closely map a Model to a Serializer.

Save and close the file. In the next sections we'll take a look at views and urls.

# Django REST with React: setting up the controll... ehm the views

A controller encapsulates logic for processing requests and returning responses. In the traditional MVC architecture there is the Model, the View, and the Controller. Example of MVC frameworks are Rails, Phoenix, Laravel.

Open up leads/views.py and create the view:

```
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import GeneratePDF
from .Serializers import GeneratePDFSerializers

class GeneratePDFList(APIView):

     def get(self, request):
        GeneratePDF1= GeneratePDF.objects.all()
        serializer= GeneratePDFSerializers(GeneratePDF1, many= True)
        return Response(serializer.data)
     def post(self):
        pass

```

# Django REST with React: setting up the rout... ehm the urls

To configure the URL mapping include the app urls in django_react/urls.py:

```
from django.contrib import admin
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from invoiceapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^GeneratePDF/', views.GeneratePDFList.as_view()),

]

```
Next up create a new file named leads/urls.py. In this file we'll wire up LeadListCreate to api/lead/:

```
from django.urls import path
from . import views
urlpatterns = [
    path('GeneratePDF/', views.LeadListCreate.as_view() ),
]
```

Finally let's enable rest_framework in INSTALLED_APPS. Open up django_react/settings.py and add the app in INSTALLED_APPS:

```
# Application definition

INSTALLED_APPS = [
    # omitted for brevity
    'leads.apps.LeadsConfig',
    'rest_framework'
]
```
Now you should be able to run a sanity check with:

```
python manage.py runserver
```

Head over http://127.0.0.1:8000/GeneratePDF and you'll see the browsable API:

![Django1](https://raw.githubusercontent.com/Pythonbratty/Invoice_creation/master/django1.jpg)
![Django2](https://raw.githubusercontent.com/Pythonbratty/Invoice_creation/master/django2.jpg)
![Django3](https://raw.githubusercontent.com/Pythonbratty/Invoice_creation/master/django3.jpg)
![Django4](https://raw.githubusercontent.com/Pythonbratty/Invoice_creation/master/django4.jpg)
![Django5](https://raw.githubusercontent.com/Pythonbratty/Invoice_creation/master/django5.jpg)


# Django REST with React: Django and React together

## Setting up React and webpack

We already know how to create a Django app so let's do it again for the frontend app:
```
django-admin startapp frontend
```

You'll see a new directory called frontend inside your project folder:

```
(venv) your@prompt:~/Code/django-react$ tree -d -L 1
.
├── django_react
├── frontend
├── leads
└── venv
```

Let's also prepare a directory structure for holding React components:

```
mkdir -p ./frontend/src/components
```

and static files:

```
mkdir -p ./frontend/{static,templates}/frontend
```

Next up we'll set up React, webpack and babel. Move in the frontend folder and initialize the environment:
```
cd ./frontend && npm init -y
```
```
npm i webpack webpack-cli --save-dev
```
Now open up package.json and configure two scripts, one for production and one for development:
```
"scripts": {

  "dev": "webpack --mode development ./src/index.js --output ./static/frontend/main.js",
  "build": "webpack --mode production ./src/index.js --output ./static/frontend/main.js"
}
```
Close the file and save it. Now let's install babel for transpiling our code:

```
npm i @babel/core babel-loader @babel/preset-env @babel/preset-react --save-dev
```
Next up pull in React:
```
npm i react react-dom --save-dev
```

Now configure babel with a .babelrc (still inside ./frontend):

{
    "presets": [
        "@babel/preset-env", "@babel/preset-react"
    ]
}

NOTE: if you're getting regeneratorRuntime is not defined with async/await in your React components replace the above babel configuration with the version presented in this post.

And finally create a webpack.config.js for configuring babel-loader:

```
module.exports = {
  module: {
  
  
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ]
  }
};
```

# Django REST with React: preparing the frontend app

First things first create a view in ./frontend/views.py:

```
from django.shortcuts import render


def index(request):
    return render(request, 'frontend/index.html')
    ```
    
Then create a template in ./frontend/templates/frontend/index.html:

```
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Django REST with React</title>
</head>
<body>
<div id="app">
    <!-- React will load here -->
</div>
</body>
{% load static %}
<script src="{% static "frontend/main.js" %}"></script>
</html>
```

As you can see the template will call ./frontend/main.js which is our webpack bundle. Configure the new URL mapping to include the frontend in ./project/urls.py:
```
urlpatterns = [
    path('', include('Leads.urls')),
    path('', include('frontend.urls')),
]
```
Next up create a new file named ./frontend/urls.py:
```
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index ),
]
```

Finally enable the frontend app in ./project/settings.py:

```

INSTALLED_APPS = [
    # omitted for brevity
    'GeneratePDF.apps.LeadsConfig',
    'rest_framework',
    'frontend', # enable the frontend app
]
```

# Django REST with React: the React frontend

Run the development server and head over http://127.0.0.1:8000/api/lead/ to insert some leads.

Now create a new file in ./frontend/src/components/App.js. It will be a React component for fetching and displaying data:

```
import React, { Component } from "react";
import { render } from "react-dom";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    fetch("api/lead")
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data,
            loaded: true
          };
        });
      });
  }

  render() {
    return (
      <ul>
        {this.state.data.map(contact => {
          return (
            <li key={contact.id}>
              {contact.invoice_num} - {contact.client_name} - {contact.client_email} - {contact.project_name} - {contact.Amount_charged}
            </li>
          );
        })}
      </ul>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);
```

Save and close the file. Now create the entry point for webpack in ./frontend/src/index.js and import your component:

```
import App from "./components/App";
```
Now we're ready to test things out. Run webpack with:

```
npm run dev
```
start the development server:
```
python manage.py runserver
```
and head over http://127.0.0.1:8000/. (If you see "Something went wrong" make sure to migrate and populate your database)

You should finally see your data in a React component!


# Creating Invoices 

Create invoices and payslips with Python.

```
# library to import the excel file
import openpyxl
from openpyxl import load_workbook

# libraries to create the pdf file and add text to it
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from openpyxl import load_workbook
# library to get logo related information
from PIL import Image

# convert the font so it is compatible
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

# import the sheet from the excel file
wb = openpyxl.load_workbook('C://Users//LENOVO//PycharmProjects//Creating_Invoices//Invoice_Record.xlsx')
sheet = wb['Invoices']

# import company's logo
im = Image.open('logo.jpg')
width, height = im.size
ratio = width / height
image_width = 800
image_height = int(image_width / ratio)

# Page information
page_width = 2156
page_height = 3050

# Invoice variables
company_name = 'The best company in the world'
payment_terms = 'x'
contact_info = 'x'
margin = 100
month_year = 'August 2020'


# def function
def create_invoice():
    for i in range(2, 12):
        # Reading values from excel file

        invoice_number = sheet.cell(row=i, column=1).value
        Client_name = sheet.cell(row=i, column=2).value
        Client_email = sheet.cell(row=i, column=3).value
        Project_name = sheet.cell(row=i, column=4).value.lower()
        

        # Creating a pdf file and setting a naming convention
        c = canvas.Canvas(str(invoice_number) + '_' + Project_name + '.pdf')

        c.setPageSize((page_width, page_height))




        # Drawing the image
        c.drawInlineImage("C:\\Users\\LENOVO\\PycharmProjects\\Creating_Invoices\\logo.jpg", page_width - image_width - margin,
                          page_height - image_height - margin,
                          image_width, image_height)

        # Invoice information
        c.setFont('Arial', 80)
        text = 'INVOICE'
        text_width = stringWidth(text, 'Arial', 80)
        c.drawString((page_width - text_width) / 2, page_height - image_height - margin, text)
        y = page_height - image_height - margin * 4
        x = 2 * margin
        x2 = x + 550

        c.setFont('Arial', 45)
        c.drawString(x, y, 'invoice number: ')
        c.drawString(x2, y, invoice_number)
        y -= margin

        c.drawString(x, y, 'Issued to: ')
        c.drawString(x2, y, Client_name)
        y -= margin

        c.drawString(x, y, 'Client email id: ')
        c.drawString(x2, y, str(Client_email))
        y -= margin

        c.drawString(x, y, 'Project name: ')
        c.drawString(x2, y, Project_name)
        y -= margin

       
        # Saving the pdf file
        c.save()

create_invoice()
```

The following screenshots depicts the invoices created into pdf file from excel file(Invoice_Record.xlxs).
![django6](https://raw.githubusercontent.com/Pythonbratty/Invoice_creation/master/django6.jpg)
![django7](https://raw.githubusercontent.com/Pythonbratty/Invoice_creation/master/django7.jpg)




        

