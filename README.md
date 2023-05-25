# checker_bot
To run the bot, you need to do three things:

1) Start Redis
2) Install the necessary libraries
3) Make changes to the configuration
4) Run it through the service

**Running Redis via Docker**
```
sudo docker pull redis
sudo docker run --name my-redis-container --restart=always -p 6379:6379 -d redis --requirepass <your_password>

```

**(You must have Python version 10 or higher).**

**Install the necessary libraries**
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Make changes to the configuration**
```

```

