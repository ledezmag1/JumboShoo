## Installation

I didn't have time to write a good intall guide. Running the install script will get you within spitting distance:
```shell
./install.sh
```

## Usage

> Make sure that the Systemd service is not running before running anything locally!
>
> ```shell
> sudo systemctl stop jumboshoo
> ```

```shell
# Close proximity test
python -m jumboshoo close-proximity

# Long proximity test
python -m jumboshoo long-proximity

# Thumper test
python -m jumboshoo thump

# Main state machine
python -m jumboshoo main
```

If you're using one of the SD cards that isn't the main one that went to Africa, run this command:
```shell
sudo systemctl enable jumboshoo
sudo systemctl start jumboshoo
```

