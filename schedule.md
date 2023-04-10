# 4/4/23 
#  I'm testing django channels tutorials on my test branch.  I'm using a new templates directory just to follow along and see if the chat functionality is working.  I don't know if I'll keep it like this or swap to a react front end and then adjust chat to work with that.  
# 4/5/23
# testing more ways to get authenticated users tied to chat rooms. slightly worried about transfering this to a front end that isn't django
# trying new views and urls to attempt auth users in chat rooms @branch centrifuge
# ok new views/urls work by requiring auth so I guess that's good.  Need to find way to get self.username to display in every message now and then i'll be okay with progress
# 4/6/23
# using the same tutorial video with more django docs to try and get a chat room functioning that saves messages now.  getting close(maybeHAHA)

# making a room and message model to establish some way of saving them.  going to try and link them with a one to many relationship.
# learning about static methods because I have dug a hole to hell.
# from django.db.models import Q.  this let me do weird queries and made progress with this.  not sure if progress was good.
#  <class 'ssage_api.admin.MessageInline'>: (admin.E202) 'ssage_api.Message' has more than one ForeignKey to 'auth.User'. You must specify a 'fk_name' attribute.
# solved with fk_name = 'sender' in messageInline "solved"
# ok so i set up an internal messaging system that works, this will be fine for now but I'd still like real time chat by due date. -->

# need to set up pallet stock and the internal conversion from order size to supply required.  ie. need 36801234 in an order and 10000 -->


# 4/7/23
#  For the weekend -   Set up params for gift query to open ai.  set up input form component.  redo models to store gift ideas to user.  websocket chat will be next week along with styling.  note to myself for weekend.  you can ping open ai through postman right now.  you can talk to django on the nextjs front end at the same time. i'm not sure why i can do that when googling told me i'd be out of luck with double auth headers but big shrugs letsgo.(for now)


# 4/10/23
# message view changed to show back and forth.   need to show real time updates on click to simulate realtime until websockets working