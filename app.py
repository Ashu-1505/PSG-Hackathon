from flask import Flask, render_template, Blueprint, send_file, request, send_from_directory
import plotly.graph_objs as go
from pymongo import MongoClient
import io
from datetime import datetime
import os
#from scraper import scrape
from compare import scrape_it

#*****************************************
#           Scrappe the Reports
#scrape()
#*****************************************


# Create a Flask application
app = Flask(__name__,static_url_path='/static')
on_market = Blueprint('on_market', __name__, url_prefix='/on_market')
# Define a route for the root URL '/'


#************************************************************************************
#reading the results from the files and store it in a 2d list
def a(b):
    d_list = []
    for line in b:
        numbers = list(map(int, line.strip("[]").split(', ')))
        d_list.append(numbers)
    return d_list
b=open("stat/burp.txt",'r')
n=open("stat/ness.txt",'r')
bu= b.read().splitlines()
ne= n.read().splitlines()
burp=a(bu)
ness=a(ne)

b=open("stat/burp.txt",'r')
n=open("stat/ness.txt",'r')
bu= b.read().splitlines()
ne= n.read().splitlines()
burp_p=a(bu)
ness_p=a(ne)

#***********************************************************************************

#Read the vulnerabilities and store it in a 2d list.
def parse_line(line):
    elements = line.strip()[1:-1].split(', ')
    elements = [element.strip("'") for element in elements]
    return elements

def read_lists_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lists_2d = [parse_line(line) for line in lines]
    return lists_2d

file_path = r'stat\burp_vul.txt'
vul = read_lists_from_file(file_path)

file_path = r'stat\burp_vul_p.txt'
vul_p = read_lists_from_file(file_path)

#***********************************************************************************

def overview(a,b):
    on=[0,0,0,0]
    un=[0,0,0,0]
    for i in range(0,len(a)):
        if i%2==0:
            on[0]+=a[i][3]+b[i][3]
            on[1]+=a[i][0]+b[i][0]
            on[2]+=a[i][1]+b[i][1]
            on[3]+=a[i][2]+b[i][2]
        else:
            un[0]+=a[i][3]+b[i][3]
            un[1]+=a[i][0]+b[i][0]
            un[2]+=a[i][1]+b[i][1]
            un[3]+=a[i][2]+b[i][2]
    return on,un

def tot(a,b):
    c=burp[a][b]+ness[a][b]
    #return f"{c:02}"
    return c

def totp(a,b):
    c=burp_p[a][b]+ness_p[a][b]
    #return f"{c:02}"
    return c

#OnMarket_Overview - {{on_o}}
#UnderDev_Overview - {{un_o}}

#Creating a plot
def create_plot(array1,array2,t):
    categories = ['High', 'Medium', 'Low']
    values1 = array1
    values2 = array2
    colors = ['#DD4B50', '#F18C43', '#F8C851']
    # Create Plotly bar chart
    trace1 = go.Bar(
        x=categories,
        y=values1,
        name='Latest',
        marker=dict(color=colors, line=dict(color=colors, width=2))
    )
    trace2 = go.Bar(
        x=categories,
        y=values2,
        name='Previous',
        marker=dict(color='white', line=dict(color=colors, width=2)) 
    )
    data = [trace1, trace2]
    layout = go.Layout(
        title=t,
        xaxis=dict(title='Severeties'),
        yaxis=dict(title='Value')
    )
    fig = go.Figure(data=data, layout=layout)
    plot_div = fig.to_html(full_html=False)
    return plot_div

def extract_date_from_filename(filename):
    f=os.path.basename(filename)
    date_str = f.split('-')[3][1:7]
    date = datetime.strptime(date_str, '%m%d%y')
    formatted_date = date.strftime('%d %B, %Y').replace(" 0", " ")
    return formatted_date

def get_files(directory,keyword):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and keyword in f]
    files.sort(key=os.path.getctime, reverse=True)
    latest_file = files[0]
    second_latest_file=files[1]
    return os.path.basename(latest_file),latest_file, os.path.basename(second_latest_file),second_latest_file

def get_build(db_name, scanner, tar):
    if scanner == "Burp":
        directory = os.path.join(bd, db_name)
    else:
        directory = os.path.join(nd, db_name)
    latest_file=get_files(directory,tar)[1]
    b=os.path.basename(latest_file)
    c=b.split('-')[2]
    second_latest_file=get_files(directory,tar)[3]
    d=os.path.basename(second_latest_file)
    e=d.split('-')[2]
    return c,e

bd=r"C:\Users\ar00088284\OneDrive - ICU Medical Inc\Desktop\Reports\Burp" #change
nd=r"C:\Users\ar00088284\OneDrive - ICU Medical Inc\Desktop\Reports\Nessus" #change

#******************************************************************************************
#                                   WEB APP STARTS
#******************************************************************************************

@app.route('/')
def hello_world():
    a=overview(burp,ness)
    return render_template("home.html",on_oi=a[0][0],on_oh=a[0][1],on_om=a[0][2],on_ol=a[0][3],un_oi=a[1][0],un_oh=a[1][1],un_om=a[1][2],un_ol=a[1][3],
                           on_di=tot(0,3), on_dh=tot(0,0), on_dm=tot(0,1), on_dl=tot(0,2), on_pi=tot(2,3), on_ph=tot(2,0), on_pm=tot(2,1), on_pl=tot(2,2),
                            on_si=tot(4,3), on_sh=tot(4,0), on_sm=tot(4,1), on_sl=tot(4,2),
                           on_mi=tot(6,3), on_mh=tot(6,0), on_mm=tot(6,1), on_ml=tot(6,2), on_li=tot(8,3), on_lh=tot(8,0), on_lm=tot(8,1), on_ll=tot(8,2),
                           un_di=tot(1,3), un_dh=tot(1,0), un_dm=tot(1,1), un_dl=tot(1,2), un_pi=tot(3,3), un_ph=tot(3,0), un_pm=tot(3,1), un_pl=tot(3,2),
                           un_si=tot(5,3), un_sh=tot(5,0), un_sm=tot(5,1), un_sl=tot(5,2),
                           un_mi=tot(7,3), un_mh=tot(7,0), un_mm=tot(7,1), un_ml=tot(7,2), un_li=tot(9,3), un_lh=tot(9,0), un_lm=tot(9,1), un_ll=tot(9,2))

@app.route('/on_market')
def on_market():
    return render_template("onmarket.html")

@app.route('/under_dev')
def under_dev():
    return render_template("UnderDev.html")

@app.route('/on_market/PlumDuo_OnMarket')
def PlumDuo_OnMarket():
    return render_template('Result.html')

@app.route('/under_dev/PlumDuo_UnderDev')
def PlumDuo_UnderDev():
    return render_template('Result.html')


#REPORTS LISTING PAGE
@app.route('/<build>/<db>/view_reports')
def Report(build,db):
    db_name = db
    bsd=os.path.join(bd,db_name)
    nsd=os.path.join(nd,db_name)
    burp_files = [{"filename": f} for f in os.listdir(bsd) if os.path.isfile(os.path.join(bsd, f)) and build in f]
    nessus_files = [{"filename": f} for f in os.listdir(nsd) if os.path.isfile(os.path.join(nsd, f)) and build in f]
    return render_template('list.html', db_name=db_name, burp_files=burp_files, nessus_files=nessus_files, extract_date_from_filename=extract_date_from_filename)

#View Reports Page
@app.route('/download/<db_name>/<scanner>/<filename>')
def download_file(db_name, scanner, filename):
    if scanner == "Burp":
        directory = os.path.join(bd, db_name)
    elif scanner == "Nessus":
        directory = os.path.join(nd, db_name)
    else:
        return "Invalid scanner", 400
    
    return send_from_directory(directory, filename)

@app.route('/compare/<db_name>/<scanner>/<filename>')
def compare(db_name, scanner, filename):
    if scanner == "Burp":
        directory = os.path.join(bd, db_name)
    else:
        directory = os.path.join(nd, db_name)
    selected_file=os.path.join(directory,filename)
    t=os.path.splitext( filename)[0]
    tar=t.split('-')[1]
    latest_file=get_files(directory,tar)[1]
    scrape_it(latest_file,selected_file,scanner)
    f=open(r"stat\temp_comp.txt",'r')
    bu= f.read().splitlines()
    temp=a(bu)
    file_path = r'stat\temp_vcomp.txt'
    tvul = read_lists_from_file(file_path)
    new_vul=[]
    com_vul=[]
    for i in tvul[0]:
        if i in tvul[1]:
            com_vul.append(i)
        else:
            new_vul.append(i)
    b1=temp[0][0:3]
    b2=temp[1][0:3]
    n1=temp[2][0:3]
    n2=temp[3][0:3]
    plot_div1 = create_plot(n1,n2,"Nessus Statistics")
    plot_div2 = create_plot(b1,b2,"Burp Statistics")
    lb=get_build(db_name, scanner, tar)[0]
    b=os.path.basename(selected_file)
    pb=b.split('-')[2]
    ld=extract_date_from_filename(os.path.basename(latest_file))
    pd=extract_date_from_filename(b)
    return render_template('compare.html', product=db_name, icu_h=0, icu_m=0, icu_l=0, icu_i=0,
                           o_li=temp[0][3]+temp[2][3] , o_lh=temp[0][0]+temp[2][0], o_lm=temp[0][1]+temp[2][1], o_ll=temp[0][2]+temp[2][2],
                           o_pi=temp[1][3]+temp[3][3] , o_ph=temp[1][0]+temp[3][0], o_pm=temp[1][1]+temp[3][1], o_pl=temp[1][2]+temp[3][2], l_date=ld, p_date=pd,
                           plot_div1=plot_div1, plot_div2=plot_div2, elements=new_vul, elements1=com_vul,date=extract_date_from_filename(filename),build_no=lb, p_build=pb)

#On_Market or Under_Dev Page
@app.route('/View/<db_name>/<scanner>/<tar>')
def view_file(db_name, scanner, tar):
    if scanner == "Burp":
        directory = os.path.join(bd, db_name)
    else:
        directory = os.path.join(nd, db_name)
    
    filename=get_files(directory,tar)[0]
    return send_from_directory(directory, filename)




# Run the application
if __name__ == '__main__':
    app.run(debug=True)
