# docappbot
Takes and Schedules an appointment for a hosipital 
Ø INTRODUCTION:
This project aims at taking Doctor’s appointment from a patient who would like to visit the hospital. 
The patient can take several appointment for a day and can cancel any appointment he wants to. 
To take an appointment the patient has to request for an appointment from the telegram bot and he will be asked to enter the name, date , time and email. 
These data will be saved and stored in the database and the bot will confirm the appointment.
A confirmation mail will be sent to him after the appointment. 
The appointment can be canceled through a command,on doing so he will be requested to enter his appointment number and the appointment will be canceled. 
The cancelation notification mail will be sent.
 
Ø DATA:
The data will be the information that is entered from the patient who would like to take the appointment. 
The data will contain the name, date, time and email. 
This data will be stored in the database in the backend and will be used further to access and confirm the appointment.
 
Ø FRONT END:
o   Telegram
 
Ø BACK END:
o   Database using SQLite3
 
Ø COMPONENTS USED:
o   Telegram
o   Database
o   IBM Watson
 
Ø SOFTWARE USED:
o   Python
o   SQLite3
 
Ø FUNCTIONALITY OF IBM WATSON:
 
o   INTENTS :
An intent represents the purpose of a user's input. You can think of intents as the actions your users might want to perform with your application.

#Customer_care_appointments : This intent is used to take different appointments from patients.
#Customer_care_Cancel: This is used to cancel the appointment that is already being booked.
#Customer_care_hospital_location: The location of the hospital is specified in this intent.
 #doc_hours: The number of hours the hospital is open
 #list: the list of doctors working in the hospital.
#Welcome: the welcome message when the telegram bot starts.
#Cancel: This is used to cancel the appointment in the middle of the conversation.
 #End: This is used to end the session and start a new one.

o    ENTITIES :
Entities represent a class of object or a data type that is relevant to a user's purpose. By recognizing the entities that are mentioned in the user's input, the Watson Assistant service can choose the specific actions to take to fulfil an intent.

 @doctor: this has a list of doctors working in the hospital. This entity takes in the specified doctor’s name from the user.
@email: this entity takes in the email ID from the user through pattern matching.
@landmark: the address of the hospital
@sys-person: this entity takes in the name from the user.
@reply: it checks for a reply ‘yes’ from the user and replies accordingly.
@conversation_end: this entity ends the session.
@sys-time: it is used to take in the time from the user in the standard format.
@sys-date: it is used to take in the date from the user in the standard format.
@sys-number: this entity is used to extract the phone number from the user.
 
o   DIALOGUES:
A dialog defines the flow of your conversation in the form of a logic tree. It matches intents (what users say) to responses (what the bot says back). Each node of the tree has a condition that triggers it, based on user input.

Welcome(#welcome) : this dialog directs the start input from the user to the welcome intent.
Timing(#Doc_hours): this dialog directs the timing of the hospital.
Direction and locations(#Customer_care_store_location): directs the location of the hospital.
Listing doctors(#List): directs the user’s input to list intent and outputs the list of the doctors.
Make an Appointment(#Customer_care_appointments): this helps in making appointment from users
Cancel an Appointment(#Customer_care_cancel): this helps in cancelling the appointment that is already done.
Cancelling(#Cancel): this helps in cancelling the appointment between the session.
Final(#End): this helps in ending the session.
Anything else : if the user inputs any other data apart from the specified commands then it will interpret it and ask the user to repeat.
