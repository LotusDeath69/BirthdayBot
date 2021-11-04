from datetime import datetime
def a(b):
  for i in b:
    date = f"{datetime.now().month}/{datetime.now().day}"

c = {
  "a": "11/3", 
  "b": "12/3"
}
a(c)
