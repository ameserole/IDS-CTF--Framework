# IDS-CTF-Framework

This is a simple server for testing CTF challenges where users have to write IDS rules.

## Setup
Each challenge is meant to be ran in a separate Docker container. To start it simply run:
```
docker build -t <image-name> ./server/
docker run -it <image-name>
```

## Challenge Creation

At the moment only Suricata is supported as the backed IDS. To create a challenge only 3 files need to be modified. The current placeholder files are an example challenge where the rule has to alert on pings to `8.8.8.8` and `8.8.4.4`.

### Pcaps
The folder `./server/pcaps/` should contain the set of pcaps that the challenge author wants the user submitted rules to be ran against.

### Expected output
The `expected.json` file is the set of alerts that the user submitted rules should create. Each line should be the key value pairs that the challenge author expects to be seen. These values are checked against the key value pairs from the alert entries in the `eve.json` log file that Suricata generates. The user has to get the exact number of alerts. If they get more or less they will get the challenge wrong.

### flag
The `flag.txt` file contains the flag to present the user if they get the challenge correct.

## Example Challenge
The files currently in the `server` directory are an example ping challenge. The challenge is to just alert on Google's DNS server IP addresses `8.8.8.8` and `8.8.4.4`. The example solution can be found in `my.rules`. To submit the solution it can easily be sent over netcat with `cat my.rules | nc <ip-address> 9999`
