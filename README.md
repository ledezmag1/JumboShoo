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

