# gemini_bot
Simple Gemini DCA bot

The normal Gemini web or app platforms charge pretty high fees, comparable to Coinbase. But this bot takes advantage of their API fee structure which is completely different and is insanely cheap. It creates a "maker-or-cancel" limit buy or sell order and only incurs their super-low 0.1% "maker" API fee (as opposed to their still very low 0.35% "taker" API fee). That means the fee on a $100 order would be 10¢!

Run this bot as a repeating cron job to dollar cost average (DCA) your buys or sells for nearly zero fees.

Current Gemini minimum API orders are 0.00001 for bitcoin which allows for extremely small orders (0.00001 btc @ $60k = $0.60!). I strongly recommend making LOTS of small, frequent orders rather than a few large ones. Learn more about what I call [micro dollar cost averaging](https://github.com/kdmukai/gdax_bot/blob/master/README.md#basic-investing-strategy-dollar-cost-averaging).


### Usage
Run ```python gemini_bot.py -h``` for usage information:

```
usage: gemini_bot.py [-h] [-sandbox] [-warn_after WARN_AFTER] [-j] [-c CONFIG_FILE]
                     market_name {BUY,SELL} amount amount_currency

        Basic Gemini DCA buying/selling bot.

        ex:
            BTCUSD BUY 14 USD          (buy $14 worth of BTC)
            BTCUSD BUY 0.00125 BTC     (buy 0.00125 BTC)
            ETHBTC SELL 0.00125 BTC    (sell 0.00125 BTC worth of ETH)
            ETHBTC SELL 0.1 ETH        (sell 0.1 ETH)
    

positional arguments:
  market_name           (e.g. BTCUSD, ETHBTC, etc)
  {BUY,SELL}
  amount                The quantity to buy or sell in the amount_currency
  amount_currency       The currency the amount is denominated in

optional arguments:
  -h, --help            show this help message and exit
  -sandbox              Run against sandbox, skips user confirmation prompt
  -warn_after WARN_AFTER
                        secs to wait before sending an alert that an order isn't done
  -j, --job             Suppresses user confirmation prompt
  -c CONFIG_FILE, --config CONFIG_FILE
                        Override default config file location
```


## Setup:
Generate an API key for your account:
* Scope: "primary"
* Permissions: "Trading"

Copy `settings.conf.example` to `settings.conf` and enter the API client key and client secret.


### Optional: Create AWS SNS topic
The bot will post a status message to an SNS topic that can be forwarded to your email. Add the `SNS_TOPIC` and your AWS IAM access credentials to the `settings.conf` file to enable this option.


### Python virtualenv
Create a virtualenv for the project and then install the dependencies:
```
pip install -r requirements.txt
```


### Run manually or via cron job
You can run this manually for one-off buys or sells but it's really meant to be run as a repeating cron job.

For example:
```
05 */2 * * * cd /my/gemini_bot/dir && /my/.envs/gemini_bot-env/bin/python -u gemini_bot.py BTCUSD BUY 5.00 BTC
```

This will buy $5 worth of BTC every other hour at 5min past the hour.
