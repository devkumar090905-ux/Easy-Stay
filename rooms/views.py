from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .forms import RoomForm
from .models import Room
# Create your views here.

def home(request):
    rooms = Room.objects.all()
    return render(request,"base.html", {"rooms": rooms})

# def rooms_list(request):
#     rooms = Room.objects.all()
#     return render(request,"rooms.html",{"rooms":rooms})

def room_detail(request, id):
    room = get_object_or_404(Room, id=id)
    return render(request, "room-details.html", {"room": room})


def add_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = RoomForm()

    return render(request, "add-room.html", {"form": form})

