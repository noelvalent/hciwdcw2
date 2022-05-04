from django.contrib import admin, messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.http import HttpResponse

from .models.backup import Backup

from utils.backup_utils import create_backup


# Register your models here.
@admin.register(Backup)
class BackupAdmin(admin.ModelAdmin):
    """
    Admin for Backup model.
    """
    actions = [
        'create_new_backup',
        'download_snapshot'
    ]

    # Any user cannot CRUD action directly.
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # Action for creating new backup
    def create_new_backup(self, request, queryset):
        if create_backup():
            self.message_user(
                request,
                'Backup Created!',
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                'Backup Failed',
                messages.ERROR
            )

    create_new_backup.short_description = 'Create New Backup'

    # Action for download snapshot file.
    def download_snapshot(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(
                request,
                'You cannot download multiple file...',
                messages.ERROR
            )
            return None

        backup = queryset[0]

        # response as a file.
        filename = backup.backup_file.name.split('/')[-1]
        response = HttpResponse(backup.backup_file, content_type='application/x-tar')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response

    download_snapshot.short_description = 'Download Snapshot'

    # changelist view override for customizing some actions.
    def changelist_view(self, request, extra_context=None):
        # ignore error: you must select at least one object.
        if 'action' in request.POST and request.POST['action'] == 'create_new_backup':
            if not request.POST.getlist(ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in Backup.objects.all():
                    post.update({ACTION_CHECKBOX_NAME: str(u.id)})

                # if user do not select object, automatically add to obj, but it is not used.
                request.POST = post

        # run super's changelist_view too.
        return super(BackupAdmin, self).changelist_view(request, extra_context)
