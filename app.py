
from flask import Flask, render_template, request
import http.client
import urllib.parse
import json

app = Flask(__name__)

# Function to fetch product data from Amazon
def fetch_amazon_data(query):
    conn = http.client.HTTPSConnection("real-time-amazon-data.p.rapidapi.com")
    # headers = {
    #     'x-rapidapi-key': "7baeb12c8emsh9e0d44e7386000ap143ac7jsn3a8ebde0d12e",
    #     'x-rapidapi-host': "real-time-amazon-data.p.rapidapi.com"
    # }
    
    
    headers = {
        'x-rapidapi-key': "ed181d4595msh6bb9094843920d3p1e6e2ajsna502f04a8e64",
        'x-rapidapi-host': "real-time-amazon-data.p.rapidapi.com"
    }


    encoded_query = urllib.parse.quote(query)
    conn.request("GET", f"/search?query={encoded_query}&country=US", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    
    
    decoded_data = data.decode("utf-8")
   
    try:
        response_data = json.loads(decoded_data)
        # Extract just the products list for easier template handling
        if "data" in response_data and "products" in response_data["data"]:
            return response_data["data"]["products"]
        return []
    except json.JSONDecodeError:
        print("Failed to parse Amazon API response as JSON")
        return []

# Function to fetch product data from Walmart
def fetch_walmart_data(query):
    conn = http.client.HTTPSConnection("walmart-data.p.rapidapi.com")


#     headers = {
#     'x-rapidapi-key': "de68d19fffmshbd7e5e20e58107ap114aeajsn8d5e9d28f44f",
#     'x-rapidapi-host': "walmart-data.p.rapidapi.com"
# }
    
    headers = {
    'x-rapidapi-key': "ed181d4595msh6bb9094843920d3p1e6e2ajsna502f04a8e64",
    'x-rapidapi-host': "walmart-data.p.rapidapi.com"
}



    encoded_query = urllib.parse.quote(query)
    search_endpoint = f"/walmart-serp.php?url=https%3A%2F%2Fwww.walmart.com%2Fsearch%3Fq%3D{encoded_query}"
    conn.request("GET", search_endpoint, headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    
    
    decoded_data = data.decode("utf-8")
   
    try:
        response_data = json.loads(decoded_data)
       
        
        # Extract products from the response
        if "body" in response_data and "products" in response_data["body"]:
            return response_data["body"]["products"]
        return []
    except json.JSONDecodeError:
        print("Failed to parse Walmart API response as JSON")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    amazon_results = []
    walmart_results = []
    query = ""
    
    if request.method == 'POST':
        query = request.form['query']
        amazon_results = fetch_amazon_data(query)
        walmart_results = fetch_walmart_data(query)
        
      
    
    return render_template('index.html', amazon=amazon_results, walmart=walmart_results, query=query)

if __name__ == '__main__':
    app.run(debug=True)