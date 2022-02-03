# vt-backend
This repository contains whole backend for voting application. Beckend is managing service with printer and sending data to gateway.


docker build -t newbackendik .

docker run -p 8079:80 newbackendik




# PDF Creator

In src/PDF_creator folder is saved protype code for part of backend, which will generate PDF file from vote. For now, we have 3 types of tickets. Visual is taken from figma work by our amazing mates -> https://www.figma.com/file/nZQvOkmYpGrOGFcbSynenw/Vytla%C4%8Den%C3%BD-l%C3%ADstok?node-id=0%3A1

Code is devided in few parts. One main class BaseTicket has constructor for saving data and is extended by 3 classes each fot specific ticket type. Each class has his own create PDF method.

Downloaded font styles are stored in folder within codes. When I tried to put them in separate folder, code doesn't worked. I did not handeled it so I let it there next to codes. 

Have a nice day, goodbye :)
