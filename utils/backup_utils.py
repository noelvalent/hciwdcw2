def create_backup():
    """
    This is utility function for creating backup file.
    It run shell script directly for using tar.
    Also, it added a model for admin page.

    Returns:
        (BOOL): result

    """
    import shutil, subprocess, datetime

    from os import path, listdir, remove

    from hciwdcw2.settings import BASE_DIR, MEDIA_ROOT
    from management.models.backup import Backup

    # run shell script
    p = subprocess.run(path.join(BASE_DIR, path.join('scripts', 'backup.sh')))
    if p.returncode != 0:
        return False

    # copy backup file
    backup_cached_path = path.join(MEDIA_ROOT, 'backup_cached')
    backup_path = path.join(MEDIA_ROOT, 'backup')
    backup_file_name = list(filter(lambda x: str(x).rfind('.tar'), listdir(backup_cached_path)))[0]

    shutil.copy2(
        path.join(backup_cached_path, backup_file_name),
        path.join(backup_path, backup_file_name)
    )

    # clean cache
    remove(path.join(backup_cached_path, backup_file_name))

    # create model
    backup_model = Backup()
    backup_model.backup_file.name = path.join(backup_path, backup_file_name)
    backup_model.created_by = datetime.datetime.now()
    backup_model.save()

    return True
