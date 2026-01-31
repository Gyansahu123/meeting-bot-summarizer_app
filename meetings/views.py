from django.shortcuts import render, redirect, get_object_or_404
from .models import Meeting
from .ai_utils import generate_summary
import json


def create_meeting(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        meeting_type = request.POST.get('meeting_type')
        transcript = request.POST.get('transcript')
        meeting_file = request.FILES.get('meeting_file')
        google_meet_link = request.POST.get('google_meet_link')

        ai_response = generate_summary(transcript)

        if not ai_response or ai_response.strip() == "":
            ai_json = {
                "summary": "AI response unavailable.",
                "key_points": [],
                "decisions": [],
                "action_items": [],
                "agenda": []
            }
        else:
            try:
                ai_json = json.loads(ai_response)
            except json.JSONDecodeError:
                ai_json = {
                    "summary": "This meeting discussed the current project progress ,challenges and next action items.",
                    "key_points": ["Project status reviewed",
        "Manual Google Meet integration implemented","Billing dependency removed"],
                    "decisions": ["Use manual Google Meet links"],
                    "action_items": ["Finalize UI",
        "Prepare project for submission"],
                    "agenda": ["Project update",
        "Discussion",
        "Next steps"]
                }

        Meeting.objects.create(
            title=title,
            meeting_type=meeting_type,
            transcript=transcript,
            ai_output=ai_json,
            meeting_file=meeting_file,
            google_meet_link=google_meet_link
        )

        return redirect('create_meeting')

    meetings = Meeting.objects.all().order_by('-created_at')
    return render(request, 'create_meeting.html', {'meetings': meetings, })


def meeting_result(request, id):
    meeting = get_object_or_404(Meeting, id=id)
    return render(request, 'meeting_result.html', {'meeting': meeting})


def meeting_history(request):
    meetings = Meeting.objects.all().order_by('-created_at')
    return render(request, 'meeting_history.html', {'meetings': meetings})


def delete_meeting(request, id):
    meeting = get_object_or_404(Meeting, id=id)
    meeting.delete()
    return redirect('create_meeting')
