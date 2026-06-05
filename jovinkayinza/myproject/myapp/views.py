from django.shortcuts import render
from datetime import datetime
from .models import Video


# Render the home page.
def index(request):
    return render(request, 'index.html')


# Render the video listing page with all uploaded videos.
def video_listing(request):
    videos = Video.objects.all().order_by('-uploaded_at')
    return render(request, 'video_listing.html', {'videos': videos})


# Handle the add-video form and upload new videos.
def add_video(request):
    # Track any form validation errors.
    errors = {}
    # Keep the submitted values so the form can be re-filled.
    values = {
        'title': '',
        'description': '',
        'quality': '',
        'publish_date': '',
    }
    success = False
    preview = {}

    if request.method == 'POST':
        # Read the values the user sent in the form.
        values['title'] = request.POST.get('title', '').strip()
        values['description'] = request.POST.get('description', '').strip()
        values['quality'] = request.POST.get('quality', '').strip()
        values['publish_date'] = request.POST.get('publish_date', '').strip()
        video_file = request.FILES.get('video_file')
        thumbnail_file = request.FILES.get('thumbnail_file')

        # Make sure the required fields are not empty.
        if not values['title']:
            errors['title'] = 'Video title is required.'

        valid_qualities = {'720p', '1080p', '4k'}
        if not values['quality']:
            errors['quality'] = 'Please choose a video quality.'
        elif values['quality'] not in valid_qualities:
            errors['quality'] = 'Please select a valid quality option.'

        if not values['publish_date']:
            errors['publish_date'] = 'Publishing date is required.'
        else:
            try:
                values['publish_date'] = datetime.strptime(
                    values['publish_date'], '%Y-%m-%d'
                ).date()
            except ValueError:
                errors['publish_date'] = 'Enter a valid date in YYYY-MM-DD format.'

        # Validate the uploaded video file.
        if not video_file:
            errors['video_file'] = 'Please select a video file to upload.'
        else:
            allowed_extensions = {'.mp4', '.mov', '.mkv', '.webm'}
            filename = video_file.name.lower()
            if not any(filename.endswith(ext) for ext in allowed_extensions):
                errors['video_file'] = 'Allowed video formats: mp4, mov, mkv, webm.'

        # If everything is okay, save the video object.
        if not errors:
            video = Video.objects.create(
                title=values['title'],
                description=values['description'],
                quality=values['quality'],
                publish_date=values['publish_date'],
                video_file=video_file,
                thumbnail_file=thumbnail_file,
            )
            success = True
            preview = {
                'video_url': video.video_file.url,
                'thumbnail_url': video.thumbnail_file.url if video.thumbnail_file else None,
            }
            # Clear the form so the user sees a fresh form after upload.
            values = {
                'title': '',
                'description': '',
                'quality': '',
                'publish_date': '',
            }

    return render(request, 'add_video.html', {
        'errors': errors,
        'values': values,
        'success': success,
        'preview': preview,
    })
