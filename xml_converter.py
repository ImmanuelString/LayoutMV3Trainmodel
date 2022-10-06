import pyconvert.pyconv
from datetime import datetime
from pytz import timezone
import pandas as pd

class IDRec:
    SendingSystemID = str
    InterfaceID = str
    BusinessProcessVariantCode = str
    TestIndicator = str

class EDIForwardRec:
    RecordType = b''
    VendorNumber = int
    Date = str # date
    Time = str # time
    IVCategory = str
    BusinessProcessVariant = b''
    BusinesProcessSubvariant = str
    BusinessArea = str # short
    LegacySystem = str
    Country = str
    OneTimeVendor = str
    Name = str
    Name2 = str
    Street = str
    PostalCode = str
    City = str
    BankAccountNumber = str
    BankNumber = str
    Region = str

class EDIHeader:
    RecordType = b''
    DocumentDate = str # date
    ReferenceDocNo = str # long
    Currency = str
    PaymentTerms = str
    GrossAmount = float
    TaxBaseAmount = str
    TaxAmount = float
    TaxCode = str
    TaxRate = str
    TaxJurisdiction = str
    CCName = str # short
    DeliveryCosts = float
    DeliveryCostsTaxCode = str
    DeliveryCostsTaxJurisdiction = str
    InvoiceIndicator = str
    ArchivingDocType = str
    LinkToImage = str
    HeaderText = str
    PaymentBlock = str
    PaymentMethod = str
    PaymentMethodSupplKey = str

class EDIItemAssign:
    RecordType = b''
    RefDocumentCategory = b''
    PONumberOrDelNote = int
    POItem = str

class EDIItem:
    ItemNumber = b''
    MaterialNumber = str
    MaterialText = str
    VehicleIdentificationNumber = str
    Quantity = str # short
    POUnit = str
    ItemAmount = float
    GLAcount = str
    CompanyCode = str
    CostCenter = str
    Order = str
    WBSElement = str
    ItemText = str
    LocalVehicleID = str
    ModelSeriesID = str
    TaxJurisdictionItem = str
    TaxRate = str
    TaxCode = str
    VendorPoNumber = str
    VendorPoNumberLine = b''

class EDIItems:
    ediitem = [EDIItem]

class ExtEDInvMessages:
    idrec = [IDRec]
    ediforwardrec = [EDIForwardRec]
    edihead = [EDIHeader]
    ediitassign = [EDIItemAssign]
    EDIItem = [EDIItems]

def pdftoxml_maker(invoice_number, invoice_date, po_number, invoice_amount, itemdetails):
    """pdf to xml maker"""
    try:
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        timestamparr = str(timestamp).split('.')
        invoicename = 'Invoice_'+timestamparr[0]
        currency = ''
        
        extEdi = ExtEDInvMessages()
        idr = IDRec()
        edifwr = EDIForwardRec()
        edihder = EDIHeader()
        ediitass = EDIItemAssign()

        idr.SendingSystemID = '' # doubt
        idr.InterfaceID = '4D002'
        idr.BusinessProcessVariantCode = ''
        idr.TestIndicator = ''
        extEdi.idrec = idr

        now = datetime.now()
        now = pd.to_datetime(now).strftime('%Y-%m-%d %H:%M:%S').split(' ')
        edifwr.RecordType = '00'
        edifwr.VendorNumber = ''
        edifwr.Date = now[0]
        edifwr.Time = now[1]
        edifwr.IVCategory = ''
        edifwr.BusinessProcessVariant = '00'
        edifwr.BusinesProcessSubvariant = ''
        edifwr.BusinessArea = ''
        edifwr.LegacySystem = '' # doubt
        edifwr.Country = ''
        edifwr.OneTimeVendor = ''
        edifwr.Name = ''
        edifwr.Name2 = ''
        edifwr.Street = ''
        edifwr.PostalCode = ''
        edifwr.City = ''
        edifwr.BankAccountNumber = ''
        edifwr.BankNumber = ''
        edifwr.Region = ''
        extEdi.ediforwardrec = edifwr

        try:
            invoicedate = pd.to_datetime(invoicedate).strftime('%Y-%m-%d')
        except:
            invoicedate = invoicedate

        edihder.RecordType = '00'
        edihder.DocumentDate = invoicedate
        edihder.ReferenceDocNo = invoice_number
        edihder.Currency = currency if len(currency) == 3 else 'USD'
        edihder.PaymentTerms = ''
        edihder.GrossAmount = invoice_amount
        edihder.TaxBaseAmount = ''
        edihder.TaxAmount = ''
        edihder.TaxCode = ''
        edihder.TaxRate = ''
        edihder.TaxJurisdiction = ''
        edihder.CCName = '' # found failed
        edihder.DeliveryCosts = ''
        edihder.DeliveryCostsTaxCode = ''
        edihder.DeliveryCostsTaxJurisdiction = ''
        edihder.InvoiceIndicator = '' # doubt
        edihder.ArchivingDocType = ''
        edihder.LinkToImage = ''
        edihder.HeaderText = ''
        edihder.PaymentBlock = ''
        edihder.PaymentMethod = ''
        edihder.PaymentMethodSupplKey = ''
        extEdi.edihead = edihder

        ediitass.RecordType = '00'
        ediitass.RefDocumentCategory = ''
        ediitass.PONumberOrDelNote = po_number
        ediitass.POItem = ''
        extEdi.ediitassign = ediitass
        
        extEdi.EDIItem = list()
        extEdi.EDIItem = []
        counter = 10
        if len(itemdetails) > 0:
            for itd in itemdetails:
                ediitm = EDIItem()
                ediitm.ItemNumber = counter
                ediitm.MaterialNumber = itd[0]
                ediitm.MaterialText = itd[1]
                ediitm.VehicleIdentificationNumber = ''
                ediitm.Quantity = itd[3]
                ediitm.POUnit = itd[2]
                ediitm.ItemAmount = itd[4]
                ediitm.GLAcount = ''
                ediitm.CompanyCode = ''
                ediitm.CostCenter = ''
                ediitm.Order = ''
                ediitm.WBSElement = ''
                ediitm.ItemText = ''
                ediitm.LocalVehicleID = ''
                ediitm.ModelSeriesID = ''
                ediitm.TaxJurisdictionItem = ''
                ediitm.TaxRate = ''
                ediitm.TaxCode = ''
                ediitm.VendorPoNumber = ''
                ediitm.VendorPoNumberLine = ''
                extEdi.EDIItem.append(ediitm)
                counter = counter + 10

        xml_doc = pyconvert.pyconv.convert2XML(extEdi)

        xml_file = "{}{}{}".format('/content/',invoicename,'.xml')
        f = open(xml_file, "wb")
        f.write(bytes(xml_doc.toprettyxml(), 'utf8'))
        f.close()
        
    except Exception as e:
        print(str(e))