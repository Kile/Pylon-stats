## Archived because the bot is down and there is no reason to improve/continue this project

# Pylon-stats
<p align="center">
  <a href"https://discord.com/oauth2/authorize?client_id=816460731654209596&scope=bot&permissions=0">
     <img src="https://cdn.discordapp.com/avatars/816460731654209596/00beaa4c6b5d09fb498b8bb02bce9762.png?size=256">
  </a>
</p>
A discord bot using the Pylon API to get some stats


Feel free to contribute to get more endpoints implemented in the bot!


Invite the bot [here](https://discord.com/oauth2/authorize?client_id=816460731654209596&scope=bot&permissions=0)


See all the commands with `p.help`


Get an instruction on how to get your Pylon API key with `p.find_key`


Configure your Pylon API key with `p.key <key>`


Get Pylon statistics of your server with `p.stats <optional_server_id>`


See all endpoints available with `p.endpoints`


You need a mongodb account you can create [here](https://account.mongodb.com/account/login) with the following file structure:
```
Pylon
--keys
```
Where `Pylon` is the database and `keys` the collection


Furthermore you will also need to create a file named `config.json` with the following content:
```json
{
  "token": "your bot token",
  "mongodb": "your mongodb connection details"
}
```
To run this bot locally run `pip3 install -r requirements.txt`, then `python3 main.py`
