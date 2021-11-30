# RASA Chatbot For Booking Flight Ticket

# Instructions:
1. Follow the official install instructions on RASA's website: https://rasa.com/docs/rasa/installation/
2. Download the codes
3. Activate virtual environment:
``` source ./venv/bin/activate ```
4. Open a Terminal and go to the root of the Chatbot Folder, run command below to start chatbot server:
``` rasa shell ```
5. Open another Terminal and go to the root of the Chatbot Folder, run command below to start action server:
``` rasa run actions ```

# Conversation Flows For Testing:

## New Customer Case:
1. Your input -> hi
2. Your input -> great or Your input -> terrible
3. Your input -> what can you do / how can you help me
4. Your input -> search flights / book flights
5. Your input -> San Jose (if you enter "san jos" the system will print error message)
6. Your input -> Kunming
7. Your input -> 12/24/2021 (if you enter "11/22/201" or "1/5/2022" the system will print error message)
8. Your input -> nonstop (if you enter "nonstopsss" the system will print error message)
9. Your input -> business 
10. Your input -> 1 ticket (if you enter "three tickets" the system will print error message)
11. Your input -> Tom Hanks 
12. Your input -> phone num is 4087773509 (if you enter "phone num is 408777" the system will print error message)
13. Your input -> finish / that's it \
14. Your input -> bye
To book another flight:
15. Your input -> new flight (Then you can file another form) \
To end or interrupt a booking process:
16. Your input -> done (Enter "done" anytime to interrupt the booking process)
17. Your input -> new flight (Enter "new flight" anytime to start a new form for booking process)

## Reject Service Case:
1. Your input -> hi
2. Your input -> great or Your input -> terrible
3. Your input -> what can you do / how can you help me
4. Your input -> no thank you / nope / don't need it

## Return Customer Case:
1. Your input -> hi
2. Your input -> book \
Then start filling the form
