import csv
import re
import sys

def main():

    if len(sys.argv)==3:
        if sys.argv[1]=="-c" or sys.argv[1]=="--csv":
            if re.search(r"^\w+\.csv$",sys.argv[2]):
                crm=sys.argv[2]
                clean_report=check_fields(crm)
                write_field(clean_report,crm)
            else:
                sys.exit("invalid usage")
        else:
            sys.exit("invalid usage")
    elif len(sys.argv)==1:
         clean_report=check_fields()
         write_field(clean_report)

    else:
        sys.exit("invalid usage")

   

def check_fields(crm="excel_crm.csv"):
    clean_report=[]
    with open(crm,"r") as file:
        read=csv.DictReader(file)
        report=list(read)
    for lines in report:
        if not re.search(r"^[A-Za-z]+(?: [A-Za-z]+)+$",lines["Name"]):
            continue
        if not re.search(r"^[1-9]\d{9}$",lines["Contact Info"]):
            continue
        if not re.search(r"^\d+$",lines["Number of Visits"]):
            continue
        else:
            if int(lines["Number of Visits"])>1000:
                   lines["Status"]="lead"    
            elif   300<int(lines["Number of Visits"])<500:
                        lines["Status"]="middle lead"
            elif 200<int(lines["Number of Visits"])<300:
                lines["Status"]="lead chance low"
            else:
                lines["Status"]="very low"
            clean_report.append(lines)
        
    return clean_report
            
               
                       
def write_field(clean_report,crm="excel_crm.csv"):
    clean_crm="clean_"+crm
    with open (clean_crm,"w",newline="") as write:
        writer = csv.DictWriter(write,fieldnames=["Name","Contact Info","Status","Number of Visits","Bough(yes,no)"])
        writer.writeheader()
        writer.writerows(clean_report)



if __name__=="__main__":
    main()