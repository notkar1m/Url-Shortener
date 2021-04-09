from flask import *
import random,string,os,qrcode
domain = "127.0.0.1:8000"
with open("data.json") as f:
	data = json.load(f)
app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def index(): 
    global data
    if request.method == "POST":
        link = request.form['link']
        with open('data.json', 'r') as f:
            while True:
                code = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
                if f'"{code}": ' in f.read():
                    pass
                else:
                    break
        data[code] = link
        with open("data.json", "w+") as fp:
            json.dump(data, fp, sort_keys=True, indent=int(4))
        stat = f"Shortener Created Successfully, Link:"
        t = '.'
        qrcodeimg = qrcode.make(f"https://{domain}/{code}")
        random_qr = str(random.randint(0,3))
        qrcodeimg.save(f"static/qrcode/code_{random_qr}.png")
        qrcode_link = f"/static/qrcode/code_{random_qr}.png"
        return render_template("index.html", stat=stat, code=code, domain=domain, t=t, qrcode_link=qrcode_link)
    else:
        t = ','
        return render_template('index.html', t=t)
@app.route('/<code>')
def useLink(code): return redirect(data[code])
if __name__ == '__main__': app.run(port=8000, debug=True)
