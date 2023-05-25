# checker_bot
To run the bot, you need to do three things:

1) Start Redis
2) Install the necessary libraries
3) Run it through the service

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

**Run it through the service**
```
nano /etc/systemd/system/humans_bot.service
```
```
[Unit]
Description=Humans bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/path/to/web3validator-Humans_Uptime_Checker_bot
ExecStart=/path/to/web3validator-Humans_Uptime_Checker_bot/venv/bin/python bot.py
Restart=on-failure
RestartSec=10
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

Start service
```
systemctl enable humans_bot
systemctl start humans_bot
```
