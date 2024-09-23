import boto3
from boto3 import Session

class TablesManager:
    def __init__(self, prod) -> None:
        self.session: Session = boto3.session.Session(
            region_name = "us-east-1",
        )

        if prod:
            self.accounts = self.session.resource('dynamodb').Table("dfk-autoplayer-accounts")
            self.autoplayer = self.session.resource('dynamodb').Table("dfk-autoplayer")

            #trading tables
            self.trades = self.session.resource('dynamodb').Table("dfk-trading-trades")
            self.active_orders = self.session.resource('dynamodb').Table("dfk-trading-active-orders")
            self.trade_errors = self.session.resource('dynamodb').Table("dfk-trading-errors")
        else:
            self.accounts = self.session.resource('dynamodb').Table("dfk-autoplayer-accounts-dev")
            self.autoplayer = self.session.resource('dynamodb').Table("dfk-autoplayer-dev")

            #trading tables
            self.trades = self.session.resource('dynamodb').Table("dfk-trading-trades-dev")
            self.active_orders = self.session.resource('dynamodb').Table("dfk-trading-active-orders-dev")
            self.trade_errors = self.session.resource('dynamodb').Table("dfk-trading-errors-dev")

        self.gas = self.session.resource('dynamodb').Table("dfk-autoplayer-gas")
        self.mining_gas = self.session.resource('dynamodb').Table("dfk-autoplayer-mining-gas")
        self.gardening_gas = self.session.resource('dynamodb').Table("dfk-autoplayer-gardening-gas")
        self.history = self.session.resource('dynamodb').Table("dfk-autoplayer-history")
        self.payouts = self.session.resource('dynamodb').Table("dfk-autoplayer-payouts")
        self.fees = self.session.resource('dynamodb').Table("dfk-autoplayer-fee")
        self.managers = self.session.resource('dynamodb').Table("dfk-autoplayer-managers")

        self.buyer_tracking = self.session.resource('dynamodb').Table("dfk-buyer-tracking")
        self.autoplayer_tracking = self.session.resource('dynamodb').Table("dfk-autoplayer-tracking")
        self.profit_tracker = self.session.resource('dynamodb').Table("dfk-profit-tracker")



    