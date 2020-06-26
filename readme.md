

В данном репозитории содержится:

    демо-версия онлайн детектора людей на изображениях и инструкция по его запуску;
    Файл с тренировкой детектора и блока сегментации "MaskRCNN_pretraining.ipynb";
    ссылка на готовый сайт.

требования: docker, git

    Для запуска проекта на локальном сервере:

$ sudo docker-compose build

$ sudo docker-compose up

ИЛИ

$ sudo docker-compose up --build

для глобального доступа к сайту (в побочном терминале):

$ ./ngrok http 5000

Подключиться к AWS:

$ ssh -i "MyKeys.pem" ubuntu@ec2-18-219-164-52.us-east-2.compute.amazonaws.com
