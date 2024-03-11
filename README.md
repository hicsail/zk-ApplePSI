# zk-ApplePSI

zk-ApplePSI repository provides an E2E pipeline, supported by picozk, to test differential privacy under Zero-Knowledge Proof.

## Project Objective

This software aims to enhance the transparency of <a href="https://www.apple.com/child-safety/pdf/Apple_PSI_System_Security_Protocol_and_Analysis.pdf"> the Apple PSI Protocol </a> by using a zero-knowledge proof technique on the server-side setup. 
Apple claims that it utilizes the NCMEC’s CSAM database to identify illegal images stored on users’ devices and generates random images derived from these images to fill bots in a Cuckoo Table Apple builds on its server.
However, the current implementation does not provide a means for the public to verify whether Apple exclusively uses images from the specified database. 
Therefore, our implementation offers a step-by-step proof for each stage in the protocol, ensuring that no arbitrary images are added.


----

## Quick Navigation

- [Use Docker](#-use-docker)
- [Run Locally](#-run-locally)
- [Different Setup](#-different-setup)

## 🐳 [Use Docker](#-use-docker)


#### 🚧 Build Docker Image and Run Container

##### <ins><i> Option A Use published docker image </i> </ins>

Run this line of code in the command line:
```
docker run --platform linux/amd64 -it hicsail/zk-applepsi:main      
```

##### <ins><i> Option B Clone Repo </i> </ins>

Run the following in the command line to get the container up and running:
```
git clone https://github.com/hicsail/zk-ApplePSI.git     # Clone the repository
cd zk-ApplePSI                                           # Move into the root directory of the project
docker-compose up -d --build                             # Inside the root directory, run the build image:
```

#### 🖥️ Getting started

##### <ins><i> Step1: Enter Docker Shell</i> </ins>

Since you have a running container, you can subsequently run the following command in your terminal to start Docker Shell:

```
docker exec -it <containerID> bash
```

You can get a container-ID from the docker desktop app by clicking the small button highlighted in the red circle
<ul>
    <img width="1161" alt="image" src="https://user-images.githubusercontent.com/62607343/203409123-1a95786f-8b2a-4e71-a920-3a51cf50cf0f.png">
</ul>

If you see something like the following in your command line, you are successfully inside the docker shell
<ul>
<img width="300" alt="image" src="https://user-images.githubusercontent.com/62607343/203413803-19021cb9-07ba-4376-ade0-dbdc6c8506c5.png">
</ul>


##### <ins><i> Step2: Install wiztoolkit</i> </ins>

We are using Fire Alarm, one of wiztoolkit packages.
After entering the container, clone wiztoolkit repo and run the following commands to install wiztoolkit:

(* You might need to set up ssh key - Follow <a href="https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=linux"> the instruction </a>)

```
git clone git@github.mit.edu:sieve-all/wiztoolkit.git
cd wiztoolkit
make
make install
```


### 🏋️‍♀️ Run the shell script

Now all setups are done for you to run your Python script inside the docker shell.
Run the following command in the docker shell, and you will see the Python script,<a href="https://github.com/hicsail/SIEVE-IR-Phase3/blob/main/apple_psi.py">    apple_psi.py</a>, generating zk statements and fire-alarm checks the format of the statements:

```
/bin/bash ./run_IR0.sh -f apple_psi 
```

## 👨‍💻 [Run Locally](#-run-locally)

This option doesn't require Docker, while it focuses on running the Python scripts, skipping setting Fire Alarm.

Run this in the command line:
```
git clone git@github.com:hicsail/zk-ApplePSI.git 
```        

Move into the root directory of the project and install dependencies

```
cd zk-ApplePSI
git clone https://github.com/uvm-plaid/picozk.git
cp ./consts/poseidon_hash.py ./picozk/picozk/poseidon_hash/poseidon_hash.py
python3 -m venv venv           # or pypy3 -m venv myenv
source venv/bin/activate       # or source myenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install picozk/.
```

The following will run the main file:
```
python3 zk-ApplePSI.py  # or pypy3 zk-ApplePSI.py
```

## 🧪 [Different Setup](#-different-setup)

The current file contains <a href="https://github.com/hicsail/zk-ApplePSI/blob/a2586bde0d485e65a9a3a8eb37e394081b315d2a/apple_psi.py#L17-L28">    sample inputs of images in a vector </a>.
If you would like to experiment with a different set of images, you can modify the vector. Be sure to match both apple_secrets and ncmec_secrets; otherwise, the proof will fail.

<img width="699" alt="image" src="https://github.com/hicsail/zk-ApplePSI/assets/62607343/c8863686-45a6-4913-9361-57c98b5f57ea">


You may also choose a form of Lagrange interpolation. For simplicity, the default setting skips Lagrange interpolation to demonstrate that bots in a cuckoo table are generated from the same polynomial as the true data, because this proof is performed outside of zk. However, should you wish to see this part in the action, you could choose either the <a href="https://en.wikipedia.org/wiki/Lagrange_polynomial#:~:text=of%20large%20oscillation.-,Definition,-%5Bedit%5D"> "Standard" method </a> or <a href="https://en.wikipedia.org/wiki/Lagrange_polynomial#:~:text=.-,Barycentric%20form,-%5Bedit%5D"> "BaryCentric" method </a> by changing the Lagrange variable in <a href="https://github.com/hicsail/zk-ApplePSI/blob/a2586bde0d485e65a9a3a8eb37e394081b315d2a/apple_psi.py#L110"> this line </a>.



<img width="626" alt="image" src="https://github.com/hicsail/zk-ApplePSI/assets/62607343/36a8d6b3-5890-4fe0-bc2b-29594fc00d1c">

