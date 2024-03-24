### USING BLOOMBERG API
# BLOOMBERG API IS DIFFERENT: It does not require API KEY.
# Bloomberg API access is typically granted through licensed software like the Bloomberg Terminal or Server API (SAPI)

import blpapi
from datetime import datetime

def main():
    # Initialize the session options with the Bloomberg service
    sessionOptions = blpapi.SessionOptions()
    sessionOptions.setServerHost('localhost')
    sessionOptions.setServerPort(8194)

    # Create and start a session
    session = blpapi.Session(sessionOptions)
    if not session.start():
        print("Failed to start session.")
        return

    # Open the news service (this is a placeholder; actual service endpoint may vary)
    if not session.openService("//blp/news_service"):
        print("Failed to open news service.")
        return

    # Obtain the service
    newsService = session.getService("//blp/news_service")
    
    # Create a request for news data (Note: The actual request type and parameters depend on Bloomberg's API)
    request = newsService.createRequest("NewsSearchRequest")  # This is hypothetical and for illustrative purposes
    request.set("query", "Trump")  # Assuming there's a way to set a query or keywords
    # Set additional request parameters if necessary, such as date range or news source filters

    # Send the request
    print("Sending request for news about 'Trump'...")
    session.sendRequest(request)

    # Process the incoming events/messages
    while True:
        event = session.nextEvent()
        for msg in event:
            # Here, you would parse the msg to extract and process news information
            print(msg)
        if event.eventType() in (blpapi.Event.RESPONSE, blpapi.Event.PARTIAL_RESPONSE):
            break
        elif event.eventType() == blpapi.Event.SESSION_STATUS:
            if msg.messageType() == blpapi.Name("SessionTerminated"):
                print("Session terminated")
                return

if __name__ == "__main__":
    main()





