# import http.client

# conn = http.client.HTTPSConnection("nutrition-calculator.p.rapidapi.com")

# headers = {
#     'x-rapidapi-key': "175800c079mshc73c4de1d473049p1e7957jsn591174a77204",
#     'x-rapidapi-host': "nutrition-calculator.p.rapidapi.com"
# }

# conn.request("GET", "/api/bmi?measurement_units=std&feet=5&inches=2&lbs=120", headers=headers)

# res = conn.getresponse()
# data = res.read()

# print(data.decode("utf-8"))

# import http.client

# conn = http.client.HTTPSConnection("ind-nutrient-api1.p.rapidapi.com")

# headers = {
#     'x-rapidapi-key': "175800c079mshc73c4de1d473049p1e7957jsn591174a77204",
#     'x-rapidapi-host': "ind-nutrient-api1.p.rapidapi.com"
# }

# conn.request("GET", "/food/646e44df0e77ec175b88cf32", headers=headers)

# res = conn.getresponse()
# data = res.read()

# print(data.decode("utf-8"))