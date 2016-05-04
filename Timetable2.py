#抓取隔一天整天的value
import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime

systime = datetime.datetime.now()
date = systime + datetime.timedelta(days=1)
tomorrow = '%s' % date.date().strftime("%Y/%m/%d")
connection = sqlite3.connect("TwhispeedrailDb.sqlite")
cursor = connection.cursor()

def railtimetable():

    # railstr = ""
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='%s'" % tomorrow)
    check = cursor.fetchall()  # check if cursor can fet something from table
    if check[0][0] == 1:
        connection.close()
        pass
    else:
        cursor.execute("CREATE TABLE '%s'" % tomorrow + " (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,\
            '車次' TEXT NOT NULL, '出發時間' TEXT NOT NULL, '抵達時間' TEXT NOT NULL, '備註' TEXT)")
        connection.commit()

        count = 0
        hours = 0
        while (count < 9):
            strtime = "06:00"
            timedelay = date.strptime(strtime,"%H:%M") + datetime.timedelta(hours=hours)
            time = timedelay.time().strftime("%H:%M")
            searchdic = {"StartStation": "977abb69-413a-4ccf-a109-0272c24fd490",
                     "EndStation": "f2519629-5973-4d08-913b-479cce78a356",
                     "SearchDate": str(tomorrow),
                     "SearchTime": time,
                     "SearchWay": "DepartureInMandarin"}

            res = requests.post("https://www.thsrc.com.tw/tw/TimeTable/SearchResult", data=searchdic)  # data=字典,查詢的條件
            soup = BeautifulSoup(res.text, "html.parser")

            for i in soup.select("table"):
                timelist = []
                if i.select(".column1") != []:
                    timelist.append(i.select(".column1")[0].text)
                    # cursor.execute("INSERT INTO '%s'" % tomorrow+"(車次) VALUES (?)", (i.select(".column1")[0].text))
                    # connection.commit()
                    # railstr += i.select(".column1")[0].text
                else:
                    pass

                if i.select(".column3") != []:
                    timelist.append(i.select(".column3")[0].text)
                    # cursor.execute("INSERT INTO '%s'" % tomorrow+"(出發時間) VALUES (?)", (i.select(".column3")[0].text))
                    # connection.commit()
                else:
                    pass

                if i.select(".column4") != []:
                    timelist.append(i.select(".column4")[0].text)
                    # cursor.execute("INSERT INTO '%s'" % tomorrow+"(抵達時間) VALUES (?)", (i.select(".column4")[0].text))
                    # connection.commit()
                else:
                    pass

                if i.select(".column2") != []:
                    if timelist[0] != "車次":
                        timelist.append(i.select(".column2")[0].text)
                        cursor.execute("INSERT INTO '%s'" % tomorrow + "(車次,出發時間,抵達時間,備註) VALUES (?,?,?,?)", \
                                   (timelist[0], timelist[1], timelist[2], timelist[3]))
                        connection.commit()
                    else:
                        pass
                else:
                    pass
            count += 1
            hours += 2
    connection.close()




railtimetable()