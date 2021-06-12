# CTF-scripts
A collection of CTF related scripts, can be used to build a solid ground for CTFs

Some other needed commands:

```
sudo apt install tcpdump nmap tmux htop # install commonly used tools on machine
ssh ctf "sudo tcpdump -s 0 -U -n -w - -i ens3 not port 22" | wireshark -k -i - # remote wireshark connection, needs NOPASSWD rule for sudo for tcpdump
docker-compose up -d --no-deps --build <service_name> # rebuild and recreate docker container for service_name
```