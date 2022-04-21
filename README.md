# RUN && BUILD
to install dependency : 
```
pip install --no-cache-dir --upgrade -r requirements.txt
```
to run app : 
```
uvicorn app.main:app --reload --port 8888
```
or if you dont have uvicorn in environement variable
```
python -m uvicorn app.main:app --reload --port 8888
```

you can use the OpenAPI interface to try the API
```
http://localhost:8888/docs
```

# DOCKER
to build image please run 
```
docker build -t powerplant_img .
```

to run and expose the port 8888
```
docker run -d --name powerplant -p 8888:8888 powerplant_img
```

# WEBSOCKET
websocket is available at ws://localhost:8888/ws

# Algorithm EXPLANATION
For this project I use a Backtracking Algorithm

If I use all the power of a powerplant but I need 20KWH to complete my load and the others powerplants requires a minimum of 40KWH. Then the algorithm will try another way trying to take 80% of the first powerplant. (Then it will try with 60%, 40%, 20%, 0%. And this on each powerplant)
