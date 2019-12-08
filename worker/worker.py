import os
from rq import get_current_job
import dropbox
from dropbox.files import WriteMode
import youtube_dl
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

YTDL_OPTS_OUTTMPL = os.getenv('YTDL_OPTS_OUTTMPL', '/tmp/%(title)s-%(id)s.%(ext)s')
YTDL_OPTS_FORMAT = os.getenv('YTDL_OPTS_FORMAT', 'bestvideo+bestaudio/best')
YTDL_OPTS_MERGE_FORMAT = os.getenv('YTDL_OPTS_MERGE_FORMAT', 'mkv')
DROPBOX_ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')
DROPBOX_BASE_PATH = os.getenv('DROPBOX_BASE_PATH', '/videos')


def ytdl_download_progress(progress):
    if progress['status'] == 'error':
        logger.debug('Error.')

    # if progress['status'] == 'downloading':
    #   logger.debug(f'Downloaded: {progress['_percent_str']}')

    if progress['status'] == 'finished':
        logger.debug('Done downloading.')


def ytdl_download(yt_url):
    logger.debug(f"Downloading video: {yt_url}")
    ydl_opts = {
        'format': YTDL_OPTS_FORMAT,
        'outtmpl': YTDL_OPTS_OUTTMPL,
        'merge_output_format': YTDL_OPTS_MERGE_FORMAT,
        'progress_hooks': [ytdl_download_progress]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        yt_info = ydl.extract_info(yt_url)
        file_path = ydl.prepare_filename(yt_info)
        yt_info['file_path'] = file_path
        return yt_info


def dbx_is_file_exist(folder, filename):
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        folder = dbx.files_list_folder(folder)
        for entry in folder.entries:
            status = filename.lower() == entry.name.lower()
            return status
    except Exception as err:
        logger.error(err)
        return False


def dbx_upload_progress(progress):
    if progress < 100:
        logger.debug(f'Uploaded: {progress}')
    else:
        logger.debug('Upload finished.')


def dbx_upload(file_path, destination_path):
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    f = open(file_path, 'rb')
    file_size = os.path.getsize(file_path)
    CHUNK_SIZE = 4 * 1024 * 1024
    if file_size <= CHUNK_SIZE:
        status = dbx.files_upload(f.read(), destination_path, mode=WriteMode.add)
        dbx_upload_progress(100)
    else:
        upload_session = dbx.files_upload_session_start(f.read(CHUNK_SIZE))
        cursor = dropbox.files.UploadSessionCursor(session_id=upload_session.session_id, offset=f.tell())
        commit = dropbox.files.CommitInfo(path=destination_path)
        while f.tell() < file_size:
            if ((file_size - f.tell()) <= CHUNK_SIZE):
                status = dbx.files_upload_session_finish(f.read(CHUNK_SIZE), cursor, commit)
                dbx_upload_progress(100)
            else:
                dbx.files_upload_session_append(f.read(CHUNK_SIZE), cursor.session_id, cursor.offset)
                dbx_upload_progress(cursor.offset / file_size * 100)
                cursor.offset = f.tell()
    f.close()
    return status


def download(yt_url):
    try:
        job = get_current_job()
        logger.info(f"Processing job: {job.id}")

        yt_info = ytdl_download(yt_url)
        # logger.debug(yt_info)

        file_path = yt_info['file_path']
        destination_path = os.path.join(DROPBOX_BASE_PATH, os.path.basename(file_path))
        file_exist = dbx_is_file_exist(DROPBOX_BASE_PATH, os.path.basename(file_path))
        if file_exist:
            raise Exception('File "%s" already exist.' % destination_path)

        logger.info('Trying to upload video %s to %s.' % (file_path, destination_path))
        dbx_upload(file_path, destination_path)

        try:
            os.remove(file_path)
        except Exception as err:
            logger.error('Could not remove temporary file %s.' % file_path)
            raise
    except Exception as e:
        logger.error(e)
