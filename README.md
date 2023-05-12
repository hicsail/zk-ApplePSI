# SIEVE-IR-Phase3

SIEVE-IR-Phase3 project provides an E2E pipeline, under picoZK, to implement Zero-Knowledge Proof.

----

## 📖 Setting up

Clone this repo:

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


<strong> 0) Clone picozk</strong> 

Clone the repository and then install with `pip install`:

```
git clone git@github.com:uvm-plaid/picozk.git
cd picozk
pip install .
```


<strong> 1) Enter Docker Shell</strong> 

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


<strong> 2) Install wiztoolkit</strong> 

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


## 🏋️‍♀️ Run your python script inside the container

You can run your python script in docker shell and compile by picozk in the following command. 

```
/bin/bash ./run_emp.sh -f apple_psi 
```

This runs <a href="https://github.com/hicsail/SIEVE-IR-Phase3/blob/main/apple_psi.py">    apple_psi.py</a><br>


## Usage of PICOZK

To generate a zero-knowledge (ZK) statement, write a Python program
that uses the PicoZK library, and then run the program to generate the
statement. For example, the following program corresponds to a ZK
statement that the prover knows a number `x` such that `x + x * x` is
30:

``` python
from picozk import *

with PicoZKCompiler('picozk_test'):
    x = SecretInt(5)
    z = x + x * x
    assert0(z + -30)
```

Running this program results in three files:
- `picozk_test.rel`: the *relation*, which is the statement itself
  (known to both prover and verifier)
- `picozk_test.type0.ins`: the *instance*, which holds public
  information (known to both prover and verifier, always empty in our
  setting)
- `picozk_test.type0.wit`: the *witness*, which holds secret
  information (known only to prover)

These files can be used to generate a ZK proof using any backend
compatible with the [SIEVE intermediate representation
(IR)](https://stealthsoftwareinc.github.io/wizkit-blog/2021/09/20/introducing-the-sieve-ir.html) -
for example, the [EMP Toolkit](https://github.com/emp-toolkit/emp-ir).
