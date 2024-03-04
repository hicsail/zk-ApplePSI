# zk-ApplePSI

zk-ApplePSI project provides an E2E pipeline to implement Zero-Knowledge Proof.

----

## 📖 Setting up

<strong> Option A Use published docker image </strong>

Run this in the command line:
```
docker run --platform linux/amd64 -it hicsail/zk-apple-psi:main      
```

<strong> Option B Clone Repo </strong>

Run this in the command line:
```
git clone git@github.com:hicsail/SIEVE-IR-Phase3.git
```

Move into the root directory of the project

```
cd SIEVE-IR-PHASE3
```

Inside the root directory, run the build image:

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

If you see something like the following in your command line, you are successfully inside the docker shell
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


## 🏋️‍♀️ Run your Python script and firealarm test module inside the container

You can run your Python script and check the output format in the docker shell by the following command:

```
/bin/bash ./run_IR0.sh -f apple_psi 
```

This runs <a href="https://github.com/hicsail/SIEVE-IR-Phase3/blob/main/apple_psi.py">    apple_psi.py</a> and checks the format of the output statements.<br>

Alternatively, you can run just the Python statement inside the container:

```
python3 apple_psi.py
```


## 🧪 Experiment with Different Setup

The current file contains <a href="https://github.com/hicsail/zk-ApplePSI/blob/a2586bde0d485e65a9a3a8eb37e394081b315d2a/apple_psi.py#L17-L28">    sample inputs of images in a vector </a>.
If you would like to experiment with a different set of images, you can modify the vector. Be sure to match both apple_secrets and ncmec_secrets; otherwise, the proof will fail.

<img width="699" alt="image" src="https://github.com/hicsail/zk-ApplePSI/assets/62607343/c8863686-45a6-4913-9361-57c98b5f57ea">


You may also choose a form of Lagrange interpolation. For simplicity, the default setting skips Lagrange interpolation to demonstrate that bots in a cuckoo table are generated from the same polynomial as the true data, because this proof is performed outside of zk. However, should you wish to see this part in the action, you could choose either the <a href="https://en.wikipedia.org/wiki/Lagrange_polynomial#:~:text=of%20large%20oscillation.-,Definition,-%5Bedit%5D"> "Standard" method </a> or <a href="https://en.wikipedia.org/wiki/Lagrange_polynomial#:~:text=.-,Barycentric%20form,-%5Bedit%5D"> "BaryCentric" method </a> by changing the Lagrange variable in <a href="https://github.com/hicsail/zk-ApplePSI/blob/a2586bde0d485e65a9a3a8eb37e394081b315d2a/apple_psi.py#L110"> this line </a>.



<img width="626" alt="image" src="https://github.com/hicsail/zk-ApplePSI/assets/62607343/36a8d6b3-5890-4fe0-bc2b-29594fc00d1c">

