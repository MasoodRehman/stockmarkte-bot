from scrapy.mail import MailSender
from scrapy.item import BaseItem
from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail

class ItemValueCheckContract(Contract):
    """ 
    My contract which checks the missing attributes in a return item e.g
    @itemAttributesCheck ticker_symbol business listing_bourse company_name company_url
    """
    name = 'itemAttributesCheck'

    def post_process(self, response):
        missing_field = list()
        mail_body = {}
        for x in response:
            for arg in self.args:
                if not arg in x:
                    missing_field.append(arg)

        missing_field_list = set(missing_field)
        if len(missing_field_list) > 0:
            """
            Generate email body and send report on specified email address 
            and raise an exeption `ContractFail`.
            """
            try:
                mail_body['args'] = "', '".join(missing_field_list)
                self.send_email("""Missing Item Field: ['%(args)s']""" % mail_body)
            except NameError, Argument:
                print Argument
            finally:
                raise ContractFail("'%s' field is missing" % mail_body['args'])

    def send_email(self, mail_body):
        mailer = MailSender(mailfrom="justjhondoe@gmail.com",smtphost="smtp.gmail.com",smtpport=587,smtpuser="justjhondoe@gmail.com",smtppass="jhondoe.123")
        return mailer.send(to=["masoodurrehman42@gmail.com"],subject="StockSpider: Stock Spiders Contract Error",body=mail_body)
        