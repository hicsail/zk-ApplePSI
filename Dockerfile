FROM hicsail/zk-oracles:main
WORKDIR /usr/src/app

COPY . .

CMD [ "sleep", "infinity" ] 