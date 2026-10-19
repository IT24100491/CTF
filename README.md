# Capture The Flag

Platform: https://ctf-box.vercel.app

## Running Stage 7

Stage 7 is a Docker-isolated Linux server, not hosted on Vercel.

```
cd stage7
docker build -t ctf-stage7 .
docker run -d --name ctf-stage7 -p 2222:22 ctf-stage7
```

Then connect:

```
ssh n.fernando@localhost -p 2222
```

Stop it when you're done:

```
docker rm -f ctf-stage7
```
