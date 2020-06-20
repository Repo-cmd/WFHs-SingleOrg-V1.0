from django.urls import path

from . import views

urlpatterns = [
    path('', views.index , name = 'index'),
    path('ShowData/', views.showUserEvents , name= 'showUserEvents'),
    path('ShowData/AddNewEvent/', views.AddNewEvent , name='addNewEvent'),
    path('ShowData/DeleteEvent/<int:EventId>', views.DeleteEvent, name='DeleteEvent'),
    path('ShowData/ViewComments/<int:EventId>', views.ShowComments, name= 'ViewComments'),
    path('ShowData/ViewComments/AddNewComment/<int:EventId>', views.AddNewComment, name='AddNewComment'),
    path('ShowData/EditEvent/<int:EventId>', views.EditEvent, name= 'EditEvent'),
    # admin routes
    path('GroupAdmin/', views.ViewGroups, name= 'viewGroupsForAdmin'),
    # admin group view routes
    path('GroupAdmin/ShowGroupData/<int:GroupId>', views.ShowGroupData, name= 'ShowGroupData'),
    path('GroupAdmin/ShowGroupData/<int:GroupId>/ApproveEvent/<int:EventId>', views.ApproveEventGroupV, name= 'ApproveEventGroupV'),
    path('GroupAdmin/ShowGroupData/<int:GroupId>/RejectEvent/<int:EventId>', views.RejectEventGroupV, name= 'RejectEventGroupV'),
    path('GroupAdmin/ShowGroupData/<int:GroupId>/ViewComments/<int:EventId>', views.showGroupUserEventComments, name= 'showGroupUserEventComments'),
    #admin user view routes
    path('GroupAdmin/ShowUserData/<int:UserId>', views.ShowUserData, name= 'ShowUserData'),
    path('GroupAdmin/ShowUserData/<int:UserId>/ApproveEvent/<int:EventId>', views.ApproveEventUserV, name= 'ApproveEventUserV'),
    path('GroupAdmin/ShowUserData/<int:UserId>/RejectEvent/<int:EventId>', views.RejectEventUserV, name= 'RejectEventUserV'),
    path('GroupAdmin/ShowUserData/<int:UserId>/ViewComments/<int:EventId>', views.showUserEventComments, name= 'showUserEventComments'),
    # super admin routes
    path('SuperAdmin/', views.SuperViewGroups, name= 'SuperViewGroups'),
    # super admin group view routes
    path('SuperAdmin/ShowGroupData/<int:GroupId>', views.SuperShowGroupData, name= 'ShowGroupData'),
    path('SuperAdmin/ShowGroupData/<int:GroupId>/ApproveEvent/<int:EventId>', views.SuperApproveEventGroupV, name= 'ApproveEventGroupV'),
    path('SuperAdmin/ShowGroupData/<int:GroupId>/RejectEvent/<int:EventId>', views.SuperRejectEventGroupV, name= 'RejectEventGroupV'),
    path('SuperAdmin/ShowGroupData/<int:GroupId>/ViewComments/<int:EventId>', views.SupershowGroupUserEventComments, name= 'showGroupUserEventComments'),
    # super admin user view routes
    path('SuperAdmin/ShowUserData/<int:UserId>', views.SuperShowUserData, name= 'ShowUserData'),
    path('SuperAdmin/ShowUserData/<int:UserId>/ApproveEvent/<int:EventId>', views.SuperApproveEventUserV, name= 'ApproveEventUserV'),
    path('SuperAdmin/ShowUserData/<int:UserId>/RejectEvent/<int:EventId>', views.SuperRejectEventUserV, name= 'RejectEventUserV'),
    path('SuperAdmin/ShowUserData/<int:UserId>/ViewComments/<int:EventId>', views.SupershowUserEventComments, name= 'showUserEventComments'),
]