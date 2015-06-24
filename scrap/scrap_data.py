from django.shortcuts import render_to_response
import requests
from bs4 import BeautifulSoup
import MySQLdb as msd
from datetime import date
import json
def f_data(request):
    d = msd.connect("localhost","root","sam123","fii_data" )
    cur = d.cursor()
    y=2012
    m=1
    insert_row_count=0
    print "This will take about 7-8 minutes...."
    while(y<date.today().year) or (m<=date.today().month):
            if(m<10):
                url= "http://www.moneycontrol.com/stocks/marketstats/fii_dii_activity/index.php?sel_month="+str(y)+"0"+str(m)
            else:
                url= "http://www.moneycontrol.com/stocks/marketstats/fii_dii_activity/index.php?sel_month="+str(y)+""+str(m)
                
            r = requests.get(url)
            td=[]
            dt_arr_temp=[]
            gr_pur_arr_temp=[]
            gr_sal_arr_temp=[]
            dt_arr=[]
            gr_pur_arr=[]
            gr_sal_arr=[]
            count=0
            
            for row in BeautifulSoup(r.content).findAll('td',{"width":"156"}):
                td=(row.text).split('-')
                if(td[0].isdigit()):
                    t=row.text
                    #print(t)
                    dt_arr_temp.append(t)
                    count+=1
            for i in reversed(dt_arr_temp):
                dt_arr.append(i)        
                        
            c=0        
            for row in BeautifulSoup(r.content).findAll('td',{"width":"102"}):
                if(c<count):
                    gr_pur_arr_temp.append(row.text)
                    c+=1
                else:
                    break
            for i in reversed(gr_pur_arr_temp):
                gr_pur_arr.append(i)    
            
            c=0        
            for row in BeautifulSoup(r.content).findAll('td',{"width":"83"}):
                if(c<count):
                    gr_sal_arr_temp.append(row.text)
                    c+=1
                else:
                    break
            for i in reversed(gr_sal_arr_temp):
                gr_sal_arr.append(i)    
    
            for x in xrange(0,count):
                dt=dt_arr[x].encode('ascii','ignore')
                purchase=gr_pur_arr[x].encode('ascii','ignore')
                sales=gr_sal_arr[x].encode('ascii','ignore')
                check=cur.execute("select * from records where date=%s",(dt))
                if not(check):
                    cur.execute("insert into records(date,gross_purchase,gross_sales)values(%s,%s,%s)",(dt,purchase,sales))
                    d.commit()
                    insert_row_count+=1
            if(m==12):
                m=1
                y+=1
            else:
                m+=1                        
    c=cur.execute("SELECT * FROM records")
    rowarray_list=[]
    for row in cur.fetchall():
        t=(row[1],float(row[2]),float(row[3]))
        rowarray_list.append(t)
    response_data=json.dumps(rowarray_list)    
    return render_to_response('high_chart.html', {'response_data': response_data})    