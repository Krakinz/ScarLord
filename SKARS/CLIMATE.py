from sideloader import *
from SƈαɾLσɾԃ import WEATHER_API, dispatcher
from SKARSHOTS.clear_cmd_sql import get_clearcmd
from ꜰᴜɴᴄᴘᴏᴅ.misc import delete

__mod_name__ = "Climate"

def get_tz(con):
    for c_code in c_n:
        if con == c_n[c_code]:
            return tz(c_tz[c_code][0])
    try:
        if c_n[con]:
            return tz(c_tz[con][0])
    except KeyError:
        return


def weather(update: Update, context: CallbackContext):
    bot = context.bot
    chat = update.effective_chat
    message = update.effective_message
    city = message.text[len("/weather ") :]

    if city:
        APPID = WEATHER_API
        result = None
        timezone_countries = {
            timezone: country
            for country, timezones in c_tz.items()
            for timezone in timezones
        }

        if "," in city:
            newcity = city.split(",")
            if len(newcity[1]) == 2:
                city = newcity[0].strip() + "," + newcity[1].strip()
            else:
                country = get_tz((newcity[1].strip()).title())
                try:
                    countrycode = timezone_countries[f"{country}"]
                except KeyError:
                    weather.edit("`Invalid country.`")
                    return
                city = newcity[0].strip() + "," + countrycode.strip()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={APPID}"
        request = get(url)
        result = json.loads(request.text)

        if request.status_code != 200:
            msg = "No weather information for this location!"

        else:

            cityname = result["name"]
            longitude = result["coord"]["lon"]
            latitude = result["coord"]["lat"]
            curtemp = result["main"]["temp"]
            feels_like = result["main"]["feels_like"]
            humidity = result["main"]["humidity"]
            min_temp = result["main"]["temp_min"]
            max_temp = result["main"]["temp_max"]
            country = result["sys"]["country"]
            sunrise = result["sys"]["sunrise"]
            sunset = result["sys"]["sunset"]
            wind = result["wind"]["speed"]
            weath = result["weather"][0]
            desc = weath["main"]
            icon = weath["id"]
            condmain = weath["main"]
            conddet = weath["description"]

            if icon <= 232:  # Rain storm
                icon = "⛈"
            elif icon <= 321:  # Drizzle
                icon = "🌧"
            elif icon <= 504:  # Light rain
                icon = "🌦"
            elif icon <= 531:  # Cloudy rain
                icon = "⛈"
            elif icon <= 622:  # Snow
                icon = "❄️"
            elif icon <= 781:  # Atmosphere
                icon = "🌪"
            elif icon <= 800:  # Bright
                icon = "☀️"
            elif icon <= 801:  # A little cloudy
                icon = "⛅️"
            elif icon <= 804:  # Cloudy
                icon = "☁️"

            ctimezone = tz(c_tz[country][0])
            time = (
                datetime.now(ctimezone)
                .strftime("%A %d %b, %H:%M")
                .lstrip("0")
                .replace(" 0", " ")
            )
            fullc_n = c_n[f"{country}"]
            dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

            kmph = str(wind * 3.6).split(".")
            mph = str(wind * 2.237).split(".")

            def fahrenheit(f):
                temp = str(((f - 273.15) * 9 / 5 + 32)).split(".")
                return temp[0]

            def celsius(c):
                temp = str((c - 273.15)).split(".")
                return temp[0]

            def sun(unix):
                xx = (
                    datetime.fromtimestamp(unix, tz=ctimezone)
                    .strftime("%H:%M")
                    .lstrip("0")
                    .replace(" 0", " ")
                )
                return xx

            msg = f"*{cityname}, {fullc_n}*\n"
            msg += f"`Longitude: {longitude}`\n"
            msg += f"`Latitude: {latitude}`\n\n"
            msg += f"• **Time:** `{time}`\n"
            msg += f"• **Temperature:** `{celsius(curtemp)}°C\n`"
            msg += f"• **Feels like:** `{celsius(feels_like)}°C\n`"
            msg += f"• **Condition:** `{condmain}, {conddet}` " + f"{icon}\n"
            msg += f"• **Humidity:** `{humidity}%`\n"
            msg += f"• **Wind:** `{kmph[0]} km/h`\n"
            msg += f"• **Sunrise**: `{sun(sunrise)}`\n"
            msg += f"• **Sunset**: `{sun(sunset)}`"
        
    else:
        msg =  "Please specify a city or country"
            
            
    delmsg = message.reply_text(
        text=msg,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )

    cleartime = get_clearcmd(chat.id, "weather")

    if cleartime:
        context.dispatcher.run_async(delete, delmsg, cleartime.time)


__help__ = f"""{ALKL}Climate"""


WEATHER_WORK = CommandHandler(["weather"], weather, run_async=True)
dispatcher.add_handler(WEATHER_WORK)