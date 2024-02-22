FROM hicsail/sieveir:main
WORKDIR /usr/src/app

COPY . .

CMD [ "sleep", "infinity" ] 