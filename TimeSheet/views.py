from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from .models import Events, Comments
from django.utils import timezone
from django.contrib.auth.models import User, Group
# Create your views here.

#############################################################################################################
############################################# LogIn Page VIEWS ############################################
# user login page
def index(request):
    if request.method == 'GET':
        return render(request,'TimeSheet/logIn.html')
    else:
        if request.method =='POST':
            user = authenticate(username =request.POST['uname'], password = request.POST['upass'] )
            if user is not None:
                login(request,user)
                return redirect('ShowData/')
            else:
                return HttpResponse('NOT FOUND')
            
############################################################################################################
############################################ UserPage views ################################################


# normal user view page (can view his events, add new, delete and edit)
@login_required()
def showUserEvents(request):
    uID = request.user.id
    uname = request.user.username
    if request.user.has_perm('TimeSheet.EventsMiddleLayerAdmin'):
        state = 'admin'
    else:
        if  request.user.has_perm('TimeSheet.EventsSuperAdmin'):
            state = 'superAdmin'
        else:
            state = 'normalUser'
    eventsList = Events.objects.filter(RelatedUser=uID)
    requestedList = []
    for e in eventsList:
        currentcomment = Comments.objects.filter(RelatedEvent=e.id)
        NumberOfComments = len(currentcomment)
        requestedList.append((e.TimeStamp , e.EventText, e.TimeTaken , e.ApprovalStatus, e.id, NumberOfComments))
    return render(request,'TimeSheet/UserPage.html',{'events': requestedList, 'uname': uname, 'state': state})


#add new event
@login_required
def AddNewEvent(request):
    if request.method == 'POST':
        eventText = request.POST['uevent']
        eventDuration = request.POST['utime']
        if isinstance(eventText, str):
            eventHolder = Events(RelatedUser = request.user, TimeStamp = timezone.now(), EventText = eventText, TimeTaken = eventDuration) 
            eventHolder.save()
            return redirect('/TimeSheet/ShowData/')
        else:
            return HttpResponse("wrong input please go back")
    else:
        return redirect('/TimeSheet/ShowData/')


# delete event 
@login_required
def DeleteEvent(request,EventId):
    SelectedEvent = Events.objects.get(pk = EventId)
    SelectedEvent.delete()
    return redirect('/TimeSheet/ShowData/')


# direct user to the comments page
@login_required
def ShowComments(request, EventId):
    uname = request.user.username
    e = Events.objects.get(pk=EventId)
    eventDetails = [e.TimeStamp, e.EventText, e.TimeTaken, e.ApprovalStatus]
    comments = Comments.objects.filter(RelatedEvent=EventId)
    CommentsList = []
    for c in comments:
        CommentsList.append((c.TimeStamp,c.RelatedUser,c.CommentText))
    context = {'uname': uname, 'event': eventDetails,'Comments':CommentsList, 'eventId': EventId}
    return render(request, 'TimeSheet/Comments.html', context)
    
###################################################################################################################
######################### Comments page Views #####################################################################

@login_required
def AddNewComment(request, EventId):
    if request.method == 'POST':
        CommentTxt = request.POST['ucomment']
        CommentHolder = Comments(RelatedEvent= Events.objects.get(pk=EventId), RelatedUser = request.user, CommentText = CommentTxt, TimeStamp = timezone.now())
        CommentHolder.save()
    return redirect('/TimeSheet/ShowData/ViewComments/'+ str(EventId))

#####################################################################################################################
################################## Edit Event Details page views #################################################################

@login_required
def EditEvent(request, EventId):
    if request.method == 'GET':
        e = Events.objects.get(pk = EventId)
        eventTxt = e.EventText
        eventTime = e.TimeTaken
        Context = {'txt': eventTxt, 'time':eventTime, 'id': EventId}
        return render(request,'TimeSheet/EditEvent.html', Context)
    else:
        if request.method == 'POST':
            e = Events.objects.get(pk = EventId)
            newText = request.POST['uevent']
            newTime = request.POST['utime']
            e.EventText = newText
            e.TimeTaken= newTime
            e.TimeStamp = timezone.now()
            e.save()
            return redirect('/TimeSheet/ShowData/')


################ logout user and redirct it to the login page #########################################
@login_required
def log_out(request):
    logout(request)
    return redirect('/TimeSheet/ShowData/')




##############################################################################################################
######################################   Group Admin Views   ##################################################

# Show table of groups availble and their memebers
@login_required
@permission_required('TimeSheet.EventsMiddleLayerAdmin')
def ViewGroups(request):
    groups = request.user.groups.all()
    groupsDetails = []
    GroupUsers = []
    for group in groups:
        usersList = User.objects.filter(groups__name = group.name)
        for uSer in usersList:
            if request.user != uSer:
                GroupUsers.append((uSer.id, uSer.username))
        groupsDetails.append((group.id, group.name, GroupUsers))
    return render(request, 'TimeSheet/GroupAdmin.html', {'groups': groupsDetails})

# **************************************** Group view ******************************************************
# show table of all users of a group
@login_required
@permission_required('TimeSheet.EventsMiddleLayerAdmin')
def ShowGroupData(request, GroupId):
    requestedList = []
    GroupUsers = User.objects.filter(groups__id = GroupId)
    for eachUser in GroupUsers:
        eventsList = Events.objects.filter(RelatedUser=eachUser.id)
        for e in eventsList:
            currentcomment = Comments.objects.filter(RelatedEvent=e.id)
            NumberOfComments = len(currentcomment)
            requestedList.append((eachUser.username, e.TimeStamp , e.EventText, e.TimeTaken , e.ApprovalStatus, e.id, NumberOfComments))
    return render(request, 'TimeSheet/GroupDetails.html', {'events': requestedList, 'gpID': GroupId})


# Approve event groups view
@login_required
@permission_required('TimeSheet.EventsMiddleLayerAdmin')
def ApproveEventGroupV(request, EventId, GroupId):
    e = Events.objects.get(pk = EventId)
    e.ApprovalStatus = 'APP'
    e.save()
    return redirect('/TimeSheet/GroupAdmin/ShowGroupData/' + str(GroupId))

# Reject event groups view
login_required
@permission_required('TimeSheet.EventsMiddleLayerAdmin')
def RejectEventGroupV(request, EventId, GroupId):
    e = Events.objects.get(pk = EventId)
    e.ApprovalStatus = 'REJ'
    e.save()
    return redirect('/TimeSheet/GroupAdmin/ShowGroupData/' + str(GroupId))


# show comments for selected event OR Admin add comment
@login_required()
@permission_required('TimeSheet.EventsMiddleLayerAdmin')
def showGroupUserEventComments(request, EventId, GroupId):
    if request.method == 'POST':
        CommentTxt = request.POST['Acomment']
        CommentHolder = Comments(RelatedEvent= Events.objects.get(pk=EventId), RelatedUser = request.user, CommentText = CommentTxt, TimeStamp = timezone.now())
        CommentHolder.save()
        return redirect('/TimeSheet/GroupAdmin/ShowGroupData/'+ str(GroupId) +'/ViewComments/'+ str(EventId))
    else:
        if request.method == 'GET':
            e = Events.objects.get(pk=EventId)
            eventDetails = [e.TimeStamp, e.EventText, e.TimeTaken, e.ApprovalStatus]
            comments = Comments.objects.filter(RelatedEvent=EventId)
            CommentsList = []
            for c in comments:
                CommentsList.append((c.TimeStamp,c.RelatedUser,c.CommentText))
            context = {'event': eventDetails,'Comments':CommentsList, 'eventId': EventId, 'GPId': GroupId}
            return render(request, 'TimeSheet/AdminComment.html', context)

# ********************************************  user view  ******************************************************

# show table of a user
@login_required
@permission_required('TimeSheet.EventsMiddleLayerAdmin')
def ShowUserData(request, UserId):
    requestedList = []
    eventsList = Events.objects.filter(RelatedUser=UserId)
    for e in eventsList:
        currentcomment = Comments.objects.filter(RelatedEvent=e.id)
        NumberOfComments = len(currentcomment)
        requestedList.append((e.TimeStamp , e.EventText, e.TimeTaken , e.ApprovalStatus, e.id, NumberOfComments))
    return render(request, 'TimeSheet/UserDetails.html', {'events': requestedList, 'UserId': UserId})


# Approve event user view
@login_required
@permission_required('TimeSheet.EventsMiddleLayerAdmin')
def ApproveEventUserV(request, EventId, UserId):
    e = Events.objects.get(pk = EventId)
    e.ApprovalStatus = 'APP'
    e.save()
    return redirect('/TimeSheet/GroupAdmin/ShowUserData/' + str(UserId))

# Reject event user view
login_required
@permission_required('TimeSheet.EventsMiddleLayerAdmin')
def RejectEventUserV(request, EventId, UserId):
    e = Events.objects.get(pk = EventId)
    e.ApprovalStatus = 'REJ'
    e.save()
    return redirect('/TimeSheet/GroupAdmin/ShowUserData/' + str(UserId))


# show comments for selected event OR Admin add comment
@login_required()
@permission_required('TimeSheet.EventsMiddleLayerAdmin')
def showUserEventComments(request, EventId, UserId):
    if request.method == 'POST':
        CommentTxt = request.POST['Acomment']
        CommentHolder = Comments(RelatedEvent= Events.objects.get(pk=EventId), RelatedUser = request.user, CommentText = CommentTxt, TimeStamp = timezone.now())
        CommentHolder.save()
        return redirect('/TimeSheet/GroupAdmin/ShowUserData/'+ str(UserId) +'/ViewComments/'+ str(EventId))
    else:
        if request.method == 'GET':
            e = Events.objects.get(pk=EventId)
            eventDetails = [e.TimeStamp, e.EventText, e.TimeTaken, e.ApprovalStatus]
            comments = Comments.objects.filter(RelatedEvent=EventId)
            CommentsList = []
            for c in comments:
                CommentsList.append((c.TimeStamp,c.RelatedUser,c.CommentText))
            context = {'event': eventDetails,'Comments':CommentsList, 'eventId': EventId, 'UserId': UserId}
            return render(request, 'TimeSheet/AdminCommentUV.html', context)







##############################################################################################################
######################################  super Admin Views   ##################################################

# Show table of groups availble and their memebers
@login_required
@permission_required('TimeSheet.EventsSuperAdmin')
def SuperViewGroups(request):
    groups = Group.objects.all()
    groupsDetails = []
    
    for group in groups:
        usersList = User.objects.filter(groups__name = group.name)
        GroupUsers = []
        for uSer in usersList:
            if request.user != uSer:
                GroupUsers.append((uSer.id, uSer.username))
        groupsDetails.append((group.id, group.name, GroupUsers))
    print(groupsDetails)
    return render(request, 'TimeSheet/SuperGroupAdmin.html', {'groups': groupsDetails})


# **************************************** Group view ******************************************************
# show table of all users of a group
@login_required
@permission_required('TimeSheet.EventsSuperAdmin')
def SuperShowGroupData(request, GroupId):
    requestedList = []
    GroupUsers = User.objects.filter(groups__id = GroupId)
    for eachUser in GroupUsers:
        eventsList = Events.objects.filter(RelatedUser=eachUser.id)
        for e in eventsList:
            currentcomment = Comments.objects.filter(RelatedEvent=e.id)
            NumberOfComments = len(currentcomment)
            requestedList.append((eachUser.username, e.TimeStamp , e.EventText, e.TimeTaken , e.ApprovalStatus, e.id, NumberOfComments))
    return render(request, 'TimeSheet/SuperGroupDetails.html', {'events': requestedList, 'gpID': GroupId})


# Approve event groups view
@login_required
@permission_required('TimeSheet.EventsSuperAdmin')
def SuperApproveEventGroupV(request, EventId, GroupId):
    e = Events.objects.get(pk = EventId)
    e.ApprovalStatus = 'APP'
    e.save()
    return redirect('/TimeSheet/SuperAdmin/ShowGroupData/' + str(GroupId))

# Reject event groups view
login_required
@permission_required('TimeSheet.EventsSuperAdmin')
def SuperRejectEventGroupV(request, EventId, GroupId):
    e = Events.objects.get(pk = EventId)
    e.ApprovalStatus = 'REJ'
    e.save()
    return redirect('/TimeSheet/SuperAdmin/ShowGroupData/' + str(GroupId))


# show comments for selected event OR Admin add comment
@login_required()
@permission_required('TimeSheet.EventsSuperAdmin')
def SupershowGroupUserEventComments(request, EventId, GroupId):
    if request.method == 'POST':
        CommentTxt = request.POST['Acomment']
        CommentHolder = Comments(RelatedEvent= Events.objects.get(pk=EventId), RelatedUser = request.user, CommentText = CommentTxt, TimeStamp = timezone.now())
        CommentHolder.save()
        return redirect('/TimeSheet/SuperAdmin/ShowGroupData/'+ str(GroupId) +'/ViewComments/'+ str(EventId))
    else:
        if request.method == 'GET':
            e = Events.objects.get(pk=EventId)
            eventDetails = [e.TimeStamp, e.EventText, e.TimeTaken, e.ApprovalStatus]
            comments = Comments.objects.filter(RelatedEvent=EventId)
            CommentsList = []
            for c in comments:
                CommentsList.append((c.TimeStamp,c.RelatedUser,c.CommentText))
            context = {'event': eventDetails,'Comments':CommentsList, 'eventId': EventId, 'GPId': GroupId}
            return render(request, 'TimeSheet/SuperAdminComment.html', context)

# ********************************************  user view  ******************************************************

# show table of a user
@login_required
@permission_required('TimeSheet.EventsSuperAdmin')
def SuperShowUserData(request, UserId):
    requestedList = []
    eventsList = Events.objects.filter(RelatedUser=UserId)
    for e in eventsList:
        currentcomment = Comments.objects.filter(RelatedEvent=e.id)
        NumberOfComments = len(currentcomment)
        requestedList.append((e.TimeStamp , e.EventText, e.TimeTaken , e.ApprovalStatus, e.id, NumberOfComments))
    return render(request, 'TimeSheet/SuperUserDetails.html', {'events': requestedList, 'UserId': UserId})


# Approve event user view
@login_required
@permission_required('TimeSheet.EventsSuperAdmin')
def SuperApproveEventUserV(request, EventId, UserId):
    e = Events.objects.get(pk = EventId)
    e.ApprovalStatus = 'APP'
    e.save()
    return redirect('/TimeSheet/SuperAdmin/ShowUserData/' + str(UserId))

# Reject event user view
login_required
@permission_required('TimeSheet.EventsSuperAdmin')
def SuperRejectEventUserV(request, EventId, UserId):
    e = Events.objects.get(pk = EventId)
    e.ApprovalStatus = 'REJ'
    e.save()
    return redirect('/TimeSheet/SuperAdmin/ShowUserData/' + str(UserId))


# show comments for selected event OR Admin add comment
@login_required()
@permission_required('TimeSheet.EventsSuperAdmin')
def SupershowUserEventComments(request, EventId, UserId):
    if request.method == 'POST':
        CommentTxt = request.POST['Acomment']
        CommentHolder = Comments(RelatedEvent= Events.objects.get(pk=EventId), RelatedUser = request.user, CommentText = CommentTxt, TimeStamp = timezone.now())
        CommentHolder.save()
        return redirect('/TimeSheet/SuperAdmin/ShowUserData/'+ str(UserId) +'/ViewComments/'+ str(EventId))
    else:
        if request.method == 'GET':
            e = Events.objects.get(pk=EventId)
            eventDetails = [e.TimeStamp, e.EventText, e.TimeTaken, e.ApprovalStatus]
            comments = Comments.objects.filter(RelatedEvent=EventId)
            CommentsList = []
            for c in comments:
                CommentsList.append((c.TimeStamp,c.RelatedUser,c.CommentText))
            context = {'event': eventDetails,'Comments':CommentsList, 'eventId': EventId, 'UserId': UserId}
            return render(request, 'TimeSheet/SuperAdminCommentUV.html', context)