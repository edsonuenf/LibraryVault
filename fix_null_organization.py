from apps.images.models import Audio, Video
from apps.images.models_organization import UserProfile

def fix_null_organization():
    # Corrige Audio
    for audio in Audio.objects.filter(organization__isnull=True):
        try:
            user_profile = UserProfile.objects.get(user=audio.user)
            audio.organization = user_profile.organization
            audio.save()
            print(f"Audio {audio.id} corrigido.")
        except UserProfile.DoesNotExist:
            print(f"Audio {audio.id} sem UserProfile, não corrigido.")
    # Corrige Video
    for video in Video.objects.filter(organization__isnull=True):
        try:
            user_profile = UserProfile.objects.get(user=video.user)
            video.organization = user_profile.organization
            video.save()
            print(f"Video {video.id} corrigido.")
        except UserProfile.DoesNotExist:
            print(f"Video {video.id} sem UserProfile, não corrigido.")

if __name__ == "__main__":
    fix_null_organization()
