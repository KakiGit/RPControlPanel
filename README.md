# RPControlPanel

1. Use Apache2

    ```bash
    sudo apt install apache2
    ```

2. Clone this repository and webui-aria2.

    ```bash
    git clone https://github.com/KakiGit/RPControlPanel.git
    cd RPControlPanel
    git clone https://github.com/ziahamza/webui-aria2.git
    ```

3. Link it to httpd directory which by default is `/var/www/html`.

    ```bash
    sudo rm -r /var/www/html
    sudo ln -s <YourPath>/RPControlPanel /var/www/html
    ```

4. Run linuxcmd.py to read parameters from Raspberry Pi and execute commands from the website.

    ```bash
    sudo nohup python linuxcmd.py &
    ```
5. Get aria2 and run it. The config file can be found on the Internet.

   ```bash
   sudo apt-get install aria2
   aria2c --conf-path=/etc/aria2/aria2.conf -D
   ```

