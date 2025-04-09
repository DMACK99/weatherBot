# A simple program to use an API call to get a weather JSON and print the forecast
# Made by Daniel Mack
#
# Import:
from pip._vendor import requests
import json

def get_wx():
        # Define the API endpoint URL
    url = 'https://api.weather.gov/gridpoints/ABQ/100,119/forecast'

    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            weather = json.dumps(response.json())
            return weather
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
  
        # Handle any network-related errors or exceptions
        print('Error:', e)
        return None


def main():
    wx = get_wx()
    #the number of 12hr periods I would like to check
    num_pers = 7

    #this was a sarcastic response, we don't need a daily sarcastic message, just one when wind is bad
    nowarning = ["It is lovely weather we are having"]
    warning = []

    #this is where I define the high wind speeds
    highwinds = ["45", "50", "55", "60", "65", "70", "75"]
    if wx:
        #trim off just the portion we care about
        periods = wx.find('periods')
        last_per = wx.find("\"number\": " + str(num_pers) + ",")
        wx = wx[-(len(wx)-periods+1):last_per]
        
        #remove useless characters && delimit with new lines
        wx = wx.replace(',', '\n')
        wx = wx.replace('\"', '')
        wx = wx.replace('[', '')
        wx = wx.replace(']', '')
        wx = wx.replace('{', '')
        wx = wx.replace('}', '')
        wx = wx.replace('periods:', '')

        #add in a new line before each number
        wx = wx.replace('number', '\nnumber')
        wx = wx.replace('\nnumber: 1', 'number: 1')

        #split
        spl_1 = wx.find('number: 2') - 3
        spl_2 = wx.find('number: 3') - 3
        spl_3 = wx.find('number: 4') - 3
        spl_4 = wx.find('number: 5') - 3
        spl_5 = wx.find('number: 6') - 3
        spl_6 = wx.find('number: 7') - 1

        #create an info array that contains our 6 wx reports (48 hrs worth of reports)
        info = [wx[:(spl_1)], wx[(spl_1 + 3):(spl_2)], wx[(spl_2 + 3):(spl_3)], wx[(spl_3 + 3):(spl_4)], wx[(spl_4 + 3):(spl_5)], 
                  wx[(spl_5 + 3):(spl_6)]]
        
        #this loop cleans up each report and makes it preeeeety
        size = len(info)
        for f in range(size):

            #splits report into individual lines, easier for formatting.
            temp = info[f].split('\n')
            tempsize = len(temp)
            #reset out to be blank
            out = [''] * tempsize

            #for loop ensures we always have the right sized array, some reports are different lengths
            for i in range(tempsize):
                out[i] = temp[i]
                #test line: print(out[i])
            
            report = ["", "", "", "", "", "", ""]
            #find smart indexes
            for i in out:
                if "name" in i:
                     nameLine = out.index(i)
                if "startTime" in i:
                     startTimeLine = out.index(i)
                if "endTime" in i:
                     endTimeLine = out.index(i)
                if "temperature" in i:
                     temperatureLine = out.index(i)
                if "windSpeed" in i:
                     windSpeedLine = out.index(i)
                if "windDirection" in i:
                     windDirLine = out.index(i)
                if "detailedForecast" in i:
                    forecastLine = out.index(i)

            #this is where the report array is created
            report[0] = ('WEATHER REPORT: ' + out[nameLine][7:]) 
            report[1] = ('Start Time: ' +  out[startTimeLine][23:31] + 'L')
            report[2] = ('End Time: ' + out[endTimeLine][21:29] + 'L')
            report[3] = ('Temperature: ' + out[temperatureLine][14:] + 'F')
            report[4] = ('Wind Speed: ' + out[windSpeedLine][12:])
            report[5] = ('Wind Direction: ' + out[windDirLine][16:])
            
            #some reports have detailed forcasts split into multiple lines
            extraLines = tempsize - forecastLine - 1
            #test line: print(extraLines)
            report[6] = ('Detailed Forecast: ' + out[forecastLine][19:])
            i = 1
            while i < extraLines:
                report[6] = (report[6] + '' + out[forecastLine+i])
                i += 1
            report[6] = (report[6] + " \n")

            for i in out[10].split(' '):
                for j in highwinds:
                    if i == j:
                        warning.append(report)
                        break
                        
        if len(nowarning) > len(warning):
            #a generic message could be sent daily when there is no upcoming weather event
            print(nowarning)
            return nowarning
        else:
            #this is my 'pretty print'
            for i in warning:
                for j in i:
                    print(j)
            return warning
        
    else:
        return("Weather not obtained")

if __name__ == '__main__':
    main()