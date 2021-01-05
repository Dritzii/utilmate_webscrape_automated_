from json.decoder import JSONDecodeError

import re
import requests
import csv
import os
import pandas as pd
import sys
from sqlalchemy import create_engine

class api_config:
    def __init__(self, is_test=False):
        if is_test:
            self.is_test = 'Zappy'
            self.token = ""
        else:
            self.is_test = 'Benergy'
            self.token = ""
        self.session = requests.session()
        if not self.self_login():
            raise Exception and print("Login not successful")
        else:
            self.cookie = self.self_login()
        self.url = "https://crm.utilmate.com/"
        self.path = os.path.dirname(os.path.abspath(__file__)) + '/Billed Consumption Report.csv'
        self.path_email = os.path.dirname(os.path.abspath(__file__)) + '/email_report.csv'
        self.path_invoices = os.path.dirname(os.path.abspath(__file__)) + '/invoices_report.csv'
        self.sms_report = os.path.dirname(os.path.abspath(__file__)) + '/sms_report.csv'
        self.receipts = os.path.dirname(os.path.abspath(__file__)) + '/receipts.csv'
        self.charges_report = os.path.dirname(os.path.abspath(__file__)) + '/charges_report.csv'
        
    # building the Cookie to authenticate everything without the crappy utilmate token bullcrap
    def self_login(self):
        form_data = "__RequestVerificationToken=VH6KicWfOda3gT_vRWW8C5qX9oS8JpvvIXNBZAnjt6yLZ4PONcq2MyKuO7ly9BEzyqwvi6odchfq1wFhhquwN5Hq7VZ650CANt980cO44601&returnUrl=&UserName=john.%40benergy.net.au&Password=&RememberMe=true&RememberMe=false&demoswitch=on&DemoMode=false&X-Requested-With=XMLHttpRequest"
        url = "https://crm.utilmate.com/Account/Login?Length=7"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "crm.utilmate.com",
            "Origin": "https://crm.utilmate.com",
            
            "Referer": "https://crm.utilmate.com/Account?timeout=False",
            "Request-Id": "|E87fL.hNCXV",
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": "_ga=GA1.2.1624341804.1607032985; __hstc=255621463.409ff1d9e8a392ccc8e48c00eb4f40bc.1607032985612.1607032985612.1607032985612.1; hubspotutk=409ff1d9e8a392ccc8e48c00eb4f40bc; __hssrc=1; __hs_opt_out=no; __hs_initial_opt_in=true; __RequestVerificationToken=PC92BeVhggZ87OR4DZzemmucirXw8J763J7LkCxxcwUro2gz6FMtb923dFyigqlOqmZru3XKrjbVCqkNIlYNzpYO2Z24CSVeWJVg2MvzUJA1; ai_user=OmFPn|2020-12-03T22:18:20.868Z; ASP.NET_SessionId=g2phuyxvcg3h3xa4rlus3wd2; ARRAffinity=f44b849bd929aa52188672c5d3b7b3acafea5cc9addb786b3d4f6ce66472a4bd; ARRAffinitySameSite=f44b849bd929aa52188672c5d3b7b3acafea5cc9addb786b3d4f6ce66472a4bd; ai_session=A9p1y|1607548917311|1607550438563.08;"
        }
        data = self.session.post(url,headers=headers, data=form_data)
        cookie = data.headers['Set-Cookie']
        m = re.findall('([^\s]+)', cookie)
        new_cookie = headers['Cookie']
        new_requests_ = new_cookie + ' ' + m[8] + '; ' + m[14]
        return new_requests_
        
    
    def Make_File_billing(self):
        with open(self.path, 'w', newline='') as write_file:
            print("making file")
            writer = csv.writer(write_file)
            writer.writerow(['Network', 'Site Code', 'Site Name', 'Site Identifier', 'Price Plan Code', 'Price Plan '
                                                                                                        'Description',
                             'Product Type', 'Site Type', 'Site Address', 'Meter Serial', 'Register', 'Account Number',
                             'Account Name', 'Billed To Date', 'Start Date', 'End Date', 'Units', 'Billed Description',
                             'Billed Consumption/ Days', 'Billed Rate', 'Billed Amount', 'GST', 'Billed Total',
                             'Billed Discount',
                             'Invoice Number', 'Invoice Date'])
    
    def make_charges_report(self):
        with open(self.charges_report, 'w', newline='') as write_file:
            print("making file")
            writer = csv.writer(write_file)
            writer.writerow(['Account Name', 'Approved', 'Approved Date', 'Approved User', 'Charge Amount', 'Charge Date',
                                                                                                        'Invoice Date',
                             'Invoice Description', 'Invoice Number', 'Invoice Run', 'Notes', 'Sales Cust Number', 'Site Code',
                             'Site Identifier', 'Site Name', 'account_number', 'cust_account_id'])

    def make_email_report(self):
        with open(self.path_email, 'w', newline='') as write_file:
            print("making file")
            writer = csv.writer(write_file)
            writer.writerow(['Account_Number', 'Account_Name', 'Site_Code', 'Site_Name', 'From_Address',
                             'Recipients', 'Subject', 'Status', 'Sent_Date', 'Email_Amount'])
            
            
    def make_sms_report(self):
        with open(self.sms_report, 'w', newline='') as write_file:
            print("making file")
            writer = csv.writer(write_file)
            writer.writerow(['Account Number', 'Account Name', 'Site Code', 'Site Name', 'Phone Number',
                             'Message Content', 'Status','Sent Date'])
        
            
    def make_invoices_report(self):
        with open(self.path_invoices, 'w', newline='') as write_file:
            print("making file")
            writer = csv.writer(write_file)
            writer.writerow(['Ref', 'account_number', 'Sales Cust Number', 'cust_account_id', 'Account Name',
                             'Customer Type', 'Product', 'Site Code', 'Site Name', 'Start Date', 'Previous Balance', 'Adjustment Total', 'Receipt Total', 'Opening Balance', 'Invoice Amount', 'Total Due',
                             'GST', 'Tax Rate', 'Invoice Date',
                             'Posted Date', 'Due Date', 'Paid', 'Amount Paid', 'Reversal', 'Prompt Payment Discount', 'Paid Promptly', 'Plan ID'])
            
    def make_receipts_report(self):
        with open(self.receipts, 'w', newline='') as write_file:
            print("making file")
            writer = csv.writer(write_file)
            writer.writerow(['ref', 'account_number', 'Sales Cust Number', 'cust_account_id', 'Account Name',
                             'Product', 'Site Code', 'Site Name', 'Amount', 'Posted Date', 'Receipt Date', 'Start Date', 'Customer Type', 'Batch No', 'Batch Type', 'Batch Name', 'Reference', 'Dishonour Type'
                             ])
            

    def get_billing_report_data(self, start_date, end_date):
        with open(self.path, 'a', newline='', encoding='utf-8') as append_file:
            writer = csv.writer(append_file)
            url = self.url + "/Report/GetReportData"
            headers = {
                'Content-Type': 'application/json',
                'Cookie': self.cookie
            }
            payload = {"data": {"reportId": 114, "reportParam": {"PARTY": "", "CUSTOMER": "", "ACCOUNT": "", "SITE": "",
                                                                 "START_DATE": start_date, "END_DATE": end_date,
                                                                 "NETWORK_NODE": ""}}}
            try:
                try:
                    data = self.session.post(url, headers=headers, json=payload).json()
                    print("grabbing get_billing_report_data ", start_date, end_date)
                    for each in data['Data']:
                        network = (each['Network'])
                        site_code = (each['Site Code'])
                        site_name = (each['Site Name'])
                        site_id = (each['Site Identifier'])
                        price_plan_code = (each['Price Plan Code'])
                        price_plan_desc = (each['Price Plan Description'])
                        product_type = (each['Product Type'])
                        site_type = (each['Site Type'])
                        site_address = (each['Site Address'])
                        meter_id = (each['Meter Serial'])
                        register = (each['Register'])
                        acc_num = (each['account_number'])
                        acc_name = (each['Account Name'])
                        billed_to_Date = (each['Billed to Date'])
                        sdate = (each['Start Date'])
                        edate = (each['End Date'])
                        units = (each['Units'])
                        billed_Description = (each['Billed Description'])
                        billed_consumption = (each['Billed Consumption/ Days'])
                        billed_rate = (each['Billed Rate'])
                        billed_amount = (each['Billed Amount'])
                        gst = (each['GST'])
                        billed_total = (each['Billed Total'])
                        billed_discount = (each['Billed Discount'])
                        invoice_number = (each['Invoice Number'])
                        invoice_date = (each['Invoice Date'])
                        writer.writerow(
                            [network, site_code, site_name, site_id, price_plan_code, price_plan_desc, product_type,
                            site_type,
                            site_address, meter_id, register, acc_num, acc_name, billed_to_Date, sdate, edate, units,
                            billed_Description, billed_consumption,
                            billed_rate, billed_amount, gst, billed_total, billed_discount, invoice_number, invoice_date])
                except KeyError as a:
                    print("Error ", a, start_date, end_date)
            except JSONDecodeError as e:
                print("Error ", e, start_date, end_date)

    def get_email_report_data(self, start_date, end_date):
        with open(self.path_email, 'a', newline='', encoding='utf-8') as append_file:
            writer = csv.writer(append_file)
            url = self.url + "/Report/GetReportData"
            headers = {
                'Content-Type': 'application/json',
                'Cookie': self.cookie
            }
            payload = {"data": {"reportId": 145,
                                "reportParam": {"PARTY": "19552", "CUSTOMER": "1990", "ACCOUNT": "1507", "SITE": "1999",
                                                "START_DATE": start_date, "END_DATE": end_date}}}
            try:
                try:
                    data = self.session.post(url, headers=headers, json=payload).json()
                    print("grabbing email_report_data ", start_date, end_date)
                    for each in data['Data']:
                        acc_no = each['Account Number']
                        acc_name = each['Account Name']
                        site_code = each['Site Code']
                        site_name = each['Site Name']
                        from_address = each['From Address']
                        recipient = each['Recipients']
                        subject = each['Subject']
                        status = each['Status']
                        send_date = each['Sent Date']
                        email_account = each['Email Amount']
                        writer.writerow(
                            [acc_no, acc_name, site_code, site_name, from_address, recipient,
                             subject, status, send_date, email_account])
                except KeyError as a:
                    print("Error ", a, start_date, end_date)
            except JSONDecodeError as e:
                print("Error ", e, start_date, end_date)
    
    def get_invoices(self, start_date, end_date):
        with open(self.path_invoices, 'a', newline='', encoding='utf-8') as append_file:
            writer = csv.writer(append_file)
            url = self.url + "/Report/GetReportData"
            headers = {
                'Content-Type': 'application/json',
                'Cookie': self.cookie
            }
            payload = {"data":{"reportId":115,"reportParam":{"PARTY":"","CUSTOMER":"","ACCOUNT":"","SITE":"","START_DATE":start_date,"END_DATE":end_date,"TRANS_DATE":"N","NETWORK_NODE":""}}}
            try:
                try:
                    data = self.session.post(url, headers=headers, json=payload).json()
                    print("grabbing invoice data ", start_date, end_date)
                    for each in data['Data']:
                        ref = each['Ref']
                        account_number = each['account_number']
                        sales_customer = each['Sales Cust Number']
                        cust_account_id = each['cust_account_id']
                        account_name = each['Account Name']
                        customer_type = each['Customer Type']
                        product = each['Product']
                        site_code = each['Site Code']
                        site_name = each['Site Name']
                        start = each['Start Date']
                        previous_balance = each['Previous Balance']
                        adjustment_total = each['Adjustment Total']
                        receipt_total = each['Receipt Total']
                        opening_balance = each['Opening Balance']
                        invoice_amount = each['Invoice Amount']
                        total_due = each['Total Due']
                        gst = each['GST']
                        tax_rate = each['Tax Rate']
                        invoice_date = each['Invoice Date']
                        posted_date = each['Posted Date']
                        due_date = each['Due Date']
                        paid = each['Paid']
                        amount_paid = each['Amount Paid']
                        reversal = each['Reversal']
                        prompt_payment_discount = each['Prompt Payment Discount']
                        paid_promptly = each['Paid Promptly']
                        plan_id = each['Plan ID']
                        writer.writerow(
                            [ref, account_number, sales_customer, cust_account_id, account_name, customer_type,
                             product, site_code, site_name, start, previous_balance, adjustment_total, receipt_total, opening_balance, invoice_amount,
                             total_due, gst, tax_rate, invoice_date, posted_date, due_date, paid, amount_paid, reversal, prompt_payment_discount, paid_promptly, plan_id])
                except KeyError as a:
                    print("Error ", a, start_date, end_date)
            except JSONDecodeError as e:
                print("Error ", e, start_date, end_date)
                
                
    def get_sms(self, start_date, end_date):
        with open(self.sms_report, 'a', newline='', encoding='utf-8') as append_file:
            writer = csv.writer(append_file)
            url = self.url + "/Report/GetReportData"
            headers = {
                'Content-Type': 'application/json',
                'Cookie': self.cookie
            }
            payload = {"data":{"reportId":142,"reportParam":{"PARTY":"","CUSTOMER":"","ACCOUNT":"","SITE":"","START_DATE":start_date,"END_DATE":end_date}}}
            try:
                try:
                    data = self.session.post(url, headers=headers, json=payload).json()
                    print("grabbing invoice data ", start_date, end_date)
                    for each in data['Data']:
                        ref = each['Account Number']
                        account_number = each['Account Name']
                        sales_customer = each['Site Code']
                        cust_account_id = each['Site Name']
                        account_name = each['Phone Number']
                        customer_type = each['Message Content']
                        product = each['Status']
                        site_code = each['Sent Date']
                        writer.writerow(
                            [ref, account_number, sales_customer, cust_account_id, account_name, customer_type,
                             product, site_code])
                except KeyError as a:
                    print("Error ", a, start_date, end_date)
            except JSONDecodeError as e:
                print("Error ", e, start_date, end_date)
                
    def get_normalized_consumption(self, start_date, end_date):
        with open(self.sms_report, 'a', newline='', encoding='utf-8') as append_file:
            writer = csv.writer(append_file)
            url = self.url + "/Report/GetReportData"
            headers = {
                'Content-Type': 'application/json',
                'Cookie': self.cookie
            }
            payload = {"data":{"reportId":142,"reportParam":{"PARTY":"","CUSTOMER":"","ACCOUNT":"","SITE":"","START_DATE":start_date,"END_DATE":end_date}}}
            try:
                try:
                    data = self.session.post(url, headers=headers, json=payload).json()
                    print("grabbing invoice data ", start_date, end_date)
                    for each in data['Data']:
                        ref = each['Account Number']
                        account_number = each['Account Name']
                        sales_customer = each['Site Code']
                        cust_account_id = each['Site Name']
                        account_name = each['Phone Number']
                        customer_type = each['Message Content']
                        product = each['Status']
                        site_code = each['Sent Date']
                        writer.writerow(
                            [ref, account_number, sales_customer, cust_account_id, account_name, customer_type,
                             product, site_code])
                except KeyError as a:
                    print("Error ", a, start_date, end_date)
            except JSONDecodeError as e:
                print("Error ", e, start_date, end_date)
                
    def account_information(self):
        user = "python"
        password = "python.B3n3rgy"
        ip = "118.88.24.10"
        conn_str = f'mysql+pymysql://{user}:{password}@{ip}/site'
        engine = create_engine(conn_str)
        sql_data = engine.execute("SELECT DISTINCT account_number FROM uml_ar.invoices")
        for each in sql_data:
            account_number = each[0]
            headers = {
                'Content-Type': 'application/json',
                'Authorization' : 'Bearer 76A0EF27-6283-498B-94F3-1D827FFAD9CF'
            }
            data = {"companycode": "Benergy", "methodcode": "GETPRICES", "parameters": [ {"account_number": account_number }]}
            
            url = "https://API.utilmate.com/api/Utilmate/post"
            data = requests.post(url, headers=headers, json=data).json()
            if data['data']:
                print(data['data'])
            else:
                print("Nothing here for ", account_number)
    
    def get_real_receipts(self, start_date, end_date):
        with open(self.receipts, 'a', newline='', encoding='utf-8') as append_file:
            writer = csv.writer(append_file)
            url = self.url + "/Report/GetReportData"
            headers = {
                    'Content-Type': 'application/json',
                    'Cookie': self.cookie
                }
            payload = {"data":{"reportId":116,"reportParam":{"PARTY":"","CUSTOMER":"","ACCOUNT":"","SITE":"","START_DATE": start_date,"END_DATE": end_date,"TRANS_DATE":"N","NETWORK_NODE":""}}}
            try:
                try:
                    data = self.session.post(url, headers=headers, json=payload).json()
                    print("grabbing Receipt data ", start_date, end_date)
                    for each in data['Data']:
                        """['Ref', 'account_number', 'Sales Cust Number', 'cust_account_id', 'Account Name',
                                'Product', 'Site Code', 'Site Name', 'Amount', 'Posted Date', 'Receipt Date', 'Start Date', 'Customer Type', 'Batch No', 'Batch Type', 'Batch Name', 'Reference', 'Dishonour Type'
                                ])"""
                        
                        ref = each['Ref']
                        account_number = each['account_number']
                        Sales_Cust_Number = each['Sales Cust Number']
                        cust_account_id = each['cust_account_id']
                        Account_Name = each['Account Name']
                        Product = each['Product']
                        Site_Code = each['Site Code']
                        Site_Name = each['Site Name']
                        Amount = each['Amount']
                        Posted_Date = each['Posted Date']
                        Receipt_Date = each['Receipt Date']
                        Start_Date = each['Start Date']
                        Customer_Type = each['Customer Type']
                        Batch_No = each['Batch No']
                        Batch_Type = each['Batch Type']
                        Batch_Name = each['Batch Name']
                        Reference = each['Reference']
                        Dishonour_Type = each['Dishonour Type']
                        writer.writerow(
                                [ref, account_number, Sales_Cust_Number, cust_account_id, Account_Name, Product,
                                Site_Code, Site_Name, Amount, Posted_Date, Receipt_Date, Start_Date, Customer_Type, Batch_No, Batch_Type, Batch_Name,
                                Reference, Dishonour_Type])
                except KeyError as a:
                    print("Error ", a, start_date, end_date)
            except JSONDecodeError as e:
                print("Error ", e, start_date, end_date)
                
    
    def get_charges_report(self, start_date, end_date):
        with open(self.charges_report, 'a', newline='', encoding='utf-8') as append_file:
            writer = csv.writer(append_file)
            url = self.url + "/Report/GetReportData"
            headers = {
                    'Content-Type': 'application/json',
                    'Cookie': self.cookie
                }
            payload = {"data":{"reportId":112,"reportParam":{"PARTY":"","CUSTOMER":"","ACCOUNT":"","SITE":"","START_DATE": start_date,"END_DATE": end_date,"TRANS_DATE":"N","NETWORK_NODE":""}}}
            try:
                try:
                    data = self.session.post(url, headers=headers, json=payload).json()
                    print("grabbing Charges data ", start_date, end_date)
                    for each in data['Data']:
                        """(['Account Name', 'Approved', 'Approved Date', 'Approved User', 'Charge Amount', 'Charge Date'
                                                                                                        'Invoice Date',
                             'Invoice Description', 'Invoice Number', 'Invoice Run', 'Notes', 'Sales Cust Number', 'Site Code',
                             'Site Identifier', 'Site Name', 'account_number', 'cust_account_id'])"""
                        
                        account_number = each['Account Name']
                        Sales_Cust_Number = each['Approved']
                        cust_account_id = each['Approved Date']
                        Account_Name = each['Approved User']
                        Product = each['Charge Amount']
                        Site_Code = each['Charge Date']
                        Site_Name = each['Invoice Date']
                        Amount = each['Invoice Description']
                        Posted_Date = each['Invoice Number']
                        Receipt_Date = each['Invoice Run']
                        Start_Date = each['Notes']
                        Customer_Type = each['Sales Cust Number']
                        Batch_No = each['Site Code']
                        Batch_Type = each['Site Identifier']
                        Batch_Name = each['Site Name']
                        Reference = each['account_number']
                        Dishonour_Type = each['cust_account_id']
                        writer.writerow(
                                [account_number, Sales_Cust_Number, cust_account_id, Account_Name, Product, Site_Code,
                                 Site_Name, Amount, Posted_Date, Receipt_Date, Start_Date, Customer_Type, Batch_No, Batch_Type, Batch_Name,
                                Reference, Dishonour_Type])
                except KeyError as a:
                    print("Error ", a, start_date, end_date)
            except JSONDecodeError as e:
                print("Error ", e, start_date, end_date)




