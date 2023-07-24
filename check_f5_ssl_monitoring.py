#!/usr/bin/env python3
import sys
from datetime import datetime
import jsonargparse
from f5.bigip import ManagementRoot
from time import sleep

NOW = datetime.now()
CRITICAL = []
WARNING = []
TO_DELETE = []


def generateReport(args):
    all_critical=""
    all_warnings=""
    all_deleted=""

    if len(CRITICAL):
        for cert in CRITICAL:
            all_critical += "<tr><td>"+cert+"</td></tr>"
    else:
        all_critical += "<tr><td>No Certificates are at Critical Point</td></tr>"
    if len(WARNING):  
        for cert in WARNING:
            all_warnings += "<tr><td>"+cert+"</td></tr>"
    else:
        all_warnings += "<tr><td>No Certificates are at Warning Point</td></tr>"
    
    if len(TO_DELETE):
        for cert in TO_DELETE:
            all_deleted += "<tr><td>"+cert+"</td></tr>"
    else:
        all_deleted += "<tr><td>No Certificates are Expired</td></tr>"

    count_per_array = "<tr><td  style='text-align:center;'>"+ str(len(CRITICAL)) +"</th><td  style='text-align:center'>"+ str(len(WARNING))+" </th><td  style='text-align:center;'>"+ str(len(TO_DELETE)) +" </th></tr>"
    table ="""<!DOCTYPE html>
            <html>
            <head>
            <style>
            table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            border-color: darkgreen;
            width: 60%;
            }

            td, th {
            border: 1px solid #dddddd;
            border-color: darkgreen;
            text-align: left;
            padding: 8px;
            }

            tr:nth-child(even) {
            background-color: #dddddd;
            }
            </style>
            </head>
            <body style="margin-left:7%;margin-right:7%;background-color:#D3D3D3;">
            <p style="padding-top:10px"></p>
            <div style="display:block;border:2px solid maroon;width:50%;justify-content:center;margin:auto;">
                <h1 style="color: red;margin-down:40px;text-align:center;">"SSL Certificates Expiry Information"</h1>
            </div>
            <h2 style="color: maroon;width:50%;margin:auto;padding-top:1%;">Critical  Threshold : """+ str(args.critical) +""" Days </h2>
            <h2 style="color: maroon;margin-down:40px;width:50%;margin:auto;">Warning Threshold : """+ str(args.warning) +""" Days </h2>

            <table style="width:35%;justify-content:center;margin-left:auto;margin-right:auto;padding-top:px;margin-top:2%;">
                <tr>
                    <th  style="text-align:center;background-color:#FF0A0A;">Critical</th>
                    <th  style="text-align:center;background-color:#E8F000;">Warning</th>
                    <th  style="text-align:center;background-color:#CA594D;">Error</th>
                </tr>
                """+ count_per_array +"""
            </table>
            <p style="padding-top:35px"></p>
            
            <table style="margin-left:10%;width:auto;">
                <tr>
                    <th  style="text-align:center;background-color:#FF0A0A;">Critical </th>
                </tr>""" + all_critical + """
            </table>
            <p style="padding-top:15px"></p>
            <table style="margin-left:10%;width:auto;">
                <tr>
                    <th  style="text-align:center;background-color:#E8F000;">Warnings </th>
                </tr>""" + all_warnings + """
            </table>
            <p style="padding-top:15px"></p>
            <table style="margin-left:10%;width:auto;">
                <tr>
                    <th  style="text-align:center;background-color:#CA594D;">Error</th>
                </tr>""" + all_deleted + """
            </table>
            
            <p style="padding-top:40px"></p>
            <p style="font-size:20px;margin-left:5%;">---------------------------------------<br>
            Thanks<br>
            <large><b>Cloud Management Group</b></large><br>
            ITOPS, i2cinc<br>
            VOIP 4500<br>
            -------------------------------------------</p>
            </body>
            </html>
            """
    report_path = "report_" + args.f5.ip + ".html"
    report_html = open(report_path, "w")
    report_html.write(table)
    report_html.close()

def verify_cert(cert, warning, critical):
    expiration_time = datetime.fromtimestamp(cert.expirationDate)
    delta = expiration_time - NOW

    if delta.days >= 0 and delta.days <= critical:
        CRITICAL.append('" {} " is near to expire in <b>{} days</b>. Please initiate the renewal process.\n'.format(cert.name, delta.days))

    elif delta.days >= 0 and delta.days <= warning:
        WARNING.append('" {} " will expire in <b>{} days</b>. Please initiate the renewal process\n'.format(cert.name, delta.days))

    elif delta.days <= 0:
        TO_DELETE.append('" {} " is already expired <b>{} days</b> ago. Please review on priority and take necessary actions.\n'.format(cert.name, delta.days))


def check(args):
    mgmt = ManagementRoot(args.f5.ip, args.f5.user, args.f5.password)
    certs = mgmt.tm.sys.file.ssl_certs.get_collection()

    for cert in certs:
        verify_cert(cert, args.warning, args.critical)

    output = ""
    alert = False

    if len(CRITICAL):
        alert = True
        output += "CRITICAL: {} certificates are going to expire.\n".format(len(CRITICAL))

    if len(WARNING):
        alert = True
        output += "WARNING: {} certificates are going to expire.\n".format(len(WARNING))

    if len(TO_DELETE):
        alert = True
        output += "ERROR: {} certificates are already expired.\n".format(len(TO_DELETE))

    if alert:
        output += "Following certificates are raising the threshold:\n {}".format(
            "".join([ "{}".format(x) for x in CRITICAL + WARNING  + TO_DELETE ])
            )

    if not len(WARNING) and not len(CRITICAL) and not len(TO_DELETE):
        print("No Certificate is in Critical State, or at Warning state or is already expired")
        sys.exit(0)

    print("F5 IP is : ",args.f5.ip)
    print(output)

    generateReport(args)


def main():
    parser = jsonargparse.ArgumentParser(
        description="Monitor SSL certificates expiration registered in a F5 server.",
        default_env=True,
    )
    parser.add_argument(
        "-w",
        "--warning",
        help="number of days to raise a warning",
        type=int,
        required=True,
    )
    parser.add_argument(
        "-c",
        "--critical",
        help="number of days to raise a critical",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--f5.ip", help="F5 IP or hostname to connect to", required=True
    )
    parser.add_argument("--f5.user", help="F5 user to access Big IP API", required=True)
    parser.add_argument(
        "--f5.password", help="F5 password to access Big IP API", required=True
    )
    args = parser.parse_args()

    return check(args)


if __name__ == "__main__":
    main()
