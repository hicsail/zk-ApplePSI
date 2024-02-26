# zk-ApplePSI

zk-ApplePSI project provides an E2E pipeline to implement Zero-Knowledge Proof.

----

## 📖 Setting up

<strong> Option A Use published docker image </strong>

Run this in command line:
```
docker run --platform linux/amd64 -it hicsail/zk-apple-psi:main      
```

<strong> Option B Clone Repo </strong>

Run this in command line:
```
git clone git@github.com:hicsail/SIEVE-IR-Phase3.git
```

Move into the root directory of the project

```
cd SIEVE-IR-PHASE3
```

Inside the root directory, run build image:

```
docker-compose up -d --build
```

Now you have a brand new container running on your machine



## 🖥️ Getting started

<strong> Enter Docker Shell</strong> 

Since you have a running container, you can subsequently run the following command in your terminal to start Docker Shell:

```
docker exec -it <containerID> bash
```

You can get a containerID from the docker desktop app by clicking the small button highlighted in the red circle
<ul>
    <img width="1161" alt="image" src="https://user-images.githubusercontent.com/62607343/203409123-1a95786f-8b2a-4e71-a920-3a51cf50cf0f.png">
</ul>

If you see something like the following in your command line, you are successfully inside docker shell
<ul>
<img width="300" alt="image" src="https://user-images.githubusercontent.com/62607343/203413803-19021cb9-07ba-4376-ade0-dbdc6c8506c5.png">
</ul>


<strong> Install wiztoolkit</strong> 

Inside the container, clone wiztoolkit repo and move into wiztoolkit:

(*) You might need to set up ssh key - Follow <a href="https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=linux"> the instruction </a>

```
git clone git@github.mit.edu:sieve-all/wiztoolkit.git
cd wiztoolkit
```

And run the following commands to install wiztoolkit (Backend for IR0):

```
make
make install
```


## 🏋️‍♀️ Run your python script and firealarm test module inside the container

You can run your python script in docker shell and compile by picozk in the following command. 

```
/bin/bash ./run_IR0.sh -f apple_psi 
```

This runs <a href="https://github.com/hicsail/SIEVE-IR-Phase3/blob/main/apple_psi.py">    apple_psi.py</a><br> and checks the format of the output statements.

Alternatively, you can run just the Python statement as below inside the container:
```
python3 apple_psi.py
```
