# imitation_server
#### This is Imitation server for testing link server with db -> main server. (sqlite3) 

## Usage
#### First
```commandline
git clone https://github.com/itqop/imitation_server.git
```
#### Next step -> create dir
```commandline
cd imitation_server
mkdir json_cache
```
#### Next step -> create and ACTIVATE virtual env [```read it on online```]

#### Next step -> install requirements
```commandline
pip install -r requirements.txt
```
### And finally -> launch project
```commandline
usage: python3 main.py <path to db file> /
<MULTIPLE_NUM generation time acceleration multiplier (maybe 30?)> /
<json data sending interval time !IN SECONDS!> (maybe 10?) /
<https host address for POST>
<https host address for GET>
```
#### For example
```commandline
python3 main.py /home/itqop/tcp_modbus_service.db 60 10 84.93.23.09/post 84.93.23.09/get
```