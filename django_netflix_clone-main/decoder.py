from django.contrib.sessions.models import Session

for s in Session.objects.all():
  try:
    decoded = s.get_decoded()
    print(decoded)
  except:
    # corrupted data
    pass