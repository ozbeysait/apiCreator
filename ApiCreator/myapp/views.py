from django.shortcuts import render
import pyodbc
from dynamic_models.models import *
from .models import *
from django.contrib import admin
from importlib import import_module, reload
from django.urls import clear_url_caches
from django.conf import settings


def base(request):
    return render(request, 'index.html')


def getDB(request):
    if request.method == 'POST':
        modelName = request.POST['modelName']
        columns = []

        driver = request.POST['driver']
        server = request.POST['server']
        db = request.POST['db']
        user = request.POST['user']
        password = request.POST['password']

        conn_str = (
            f"Driver={{{driver}}};"
            f"Server={server};"
            f"Database={db};"
            f"UID={user};"
            f"PWD={password};"
        )

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{modelName}'")

        for i in cursor:
            print(i)
            columns.append(i)

        print("Len: ", len(columns))
        print("modelName:", modelName)
        modelExists = False
        modelCreated = False
        try:
            model_schema = ModelSchema.objects.create(name=modelName)
            modelCreated = True
        except Exception as e:
            print("error:", e)
            modelExists = True
            return render(request, 'index.html',
                          context={'modelExists': modelExists, 'modelCreated': modelCreated, 'modelName': modelName})

        len_req = len(columns)
        count = 0
        for x in range(len_req):
            count = count + 1
            dataType = "character"
            isNull = False
            isUnique = False
            if columns[x][7] == "varchar":
                dataType = "character"
            elif columns[x][7] == "int":
                dataType = "integer"
            elif columns[x][7] == "decimal":
                dataType = "float"

            if columns[x][5] == "(NULL)":
                isNull = True

            field_schema = FieldSchema.objects.create(
                name=columns[x][3],
                data_type=dataType,
                model_schema=model_schema,
                max_length=columns[x][8],
                null=isNull,
                unique=isUnique
            )

        model_create = Modelnames.objects.create(modelname=modelName)
        reg_model = model_schema.as_model()
        admin.site.register(reg_model)
        reload(import_module(settings.ROOT_URLCONF))
        clear_url_caches()


    return render(request, 'index.html', context={'modelExists': modelExists, 'modelCreated': modelCreated, 'modelName': modelName})
