import csv
from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.statement import Statement, BankAccount, recalculate_balance


class BelfiusCsv():
    delimiter = ';'
    quotechar = '"'
    escapechar = None
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_ALL


class BelfiusPlugin(Plugin):
    """Belfius plugin for ofxstatement (Belgium)
    """

    def get_parser(self, filename):
        f = open(filename, 'r', encoding=self.settings.get("charset", "ISO-8859-1"))
        # skip query header
        while True:
            line = f.readline()
            print(line)
            if not line:
                break
            if (line.startswith(";")):
                # blanco line after query header
                break

        # skip line with columns names
        f.readline()

        parser = BelfiusParser(f)
        return parser


class BelfiusParser(CsvStatementParser):
    date_format = "%d/%m/%Y"

#Rekening;Boekingsdatum;Afschriftnummer;Transactienummer;Rekening tegenpartij;Naam tegenpartij bevat;Straat en nummer;Postcode en plaats;Transactie;Valutadatum;Bedrag;Devies;BIC;Landcode;Mededelingen
#0        1             2               3                4                    5                      6                7                  8           9          10     11     12  13       14

    mappings = {
        'date': 1,
        'payee': 5,
        'memo': 14,
        'amount': 10
    }

    def __init__(self, filename):
        self.statement = Statement('GKCCBEBB', None,'EUR')
        self.fin = filename
        csv.register_dialect('belfiuscsv', BelfiusCsv())

    def parse(self):
        """Main entry point for parsers

        super() implementation will call to split_records and parse_record to
        process the file.
        """
        stmt = super(BelfiusParser, self).parse()
        recalculate_balance(stmt)
        return stmt

    def split_records(self):
        """Return iterable object consisting of a line per transaction
        """
        return csv.reader(self.fin, 'belfiuscsv')

    def parse_record(self, line):
        """Parse given transaction line and return StatementLine object
        """
        if (self.statement.account_id == None):
            self.statement.account_id =  line[0].replace(" ", "")
        stmtline = super(BelfiusParser, self).parse_record(line)
        stmtline.id = f'{line[1]}-{line[2]}-{line[3]}'
        stmtline.trntype = 'DEBIT' if stmtline.amount < 0 else 'CREDIT'
        stmtline.bank_account_to = BankAccount(line[12], line[4].replace(" ", ""))
        return stmtline

    def parse_float(self, value):
        """Return a float from a string with ',' as decimal mark.
         ex. 1.234,56 -> 1234.56
        """
        return float(value.replace('.','').replace(',', '.'))
