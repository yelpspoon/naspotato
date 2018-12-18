#!/usr/bin/env python

import schedule, time, transmissionrpc, thread, logging, logging.handlers


''' Process to query Transmission RPC to collect torrent life-span info.
    Runs a simple Py httpd (threaded) to allow for web-based status checks.
    Logging handles process output to console (docker logs) and file (httpd).
'''

''' VARS '''
schedule_chk_interval_seconds = 60
timer_sleep                   = 1
log_hour_minute_second        = 'm'
log_interval_count            = 5
log_file_name                 = 'index.html'
#log_byte_size                 = 500000  ## 512K
log_backup_cnt                = 12
HTTP_PORT                     = 8888

''' edit Transmission Server parameters here '''
trans_server_hostip           = 'nas.local'
trans_server_port             = 9091
''' How long before we delete finished torrents '''
torrent_hours_lived           = 2  

''' Setup logging module '''
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

''' Create handlers '''
c_handler = logging.StreamHandler()
#f_handler = logging.FileHandler(log_file_name)
#f_handler = logging.handlers.RotatingFileHandler(
f_handler = logging.handlers.TimedRotatingFileHandler(
        log_file_name, 
        when=log_hour_minute_second, 
        interval=log_interval_count, 
        backupCount=log_backup_cnt)
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)

''' Create formatters and add it to handlers '''
log_format = logging.Formatter('%(asctime)s - %(process)s - %(levelname)s - %(message)s')
c_handler.setFormatter(log_format)
f_handler.setFormatter(log_format)

''' Add handlers to the log '''
log.addHandler(c_handler)
log.addHandler(f_handler)


def runStatus(port):
    ''' Create a simple httpd for displaying status file
        in an http endpoint <NAS Server:8080>
    '''
    import SimpleHTTPServer
    import SocketServer

    PORT = port
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print "serving at port", PORT  # Startup Message
    return httpd.serve_forever()


def job():
    ''' Query Transmission RPC for torrent info
        Remove stale torrents that have finished or have 
        been seeing for > 2 hours.
    '''
    now = int( round( time.time()) )
    tc = transmissionrpc.Client( trans_server_hostip, port=trans_server_port )

    # get torrents
    log.info('Checking Transmission...<br>')
    for torrent in tc.get_torrents():
        
        #if torrent.downloadDir == '/downloads/completed/sonar': 
        if torrent.downloadDir == '/downloads/completed':
            log.info( 'Skipping {0}<br>'.format(torrent.name) )
            log.info('------------------------<br>')
            continue
        
        runTime = (now - torrent.startDate)/60
        runWord = 'minutes'
        if runTime > 90:
            runTime = runTime/60
            runWord = 'hours'

        log.info( '{0} {1} for {2} {3}<br>'.format(torrent.name, torrent.status, runTime, runWord) )

        # if FINISHED or SEEDING for more than TWO HOURS, DELETE
        if torrent.isFinished or (torrent.status == 'seeding' and (runWord == 'hours' and runTime > torrent_hours_lived )):
            log.info( 'Removing torrent: {0}<br>'.format(torrent.name) )
            tc.remove_torrent(torrent.hashString, delete_data=True)
            log.info('------------------------<br>')
    log.info('------------------------<br>')


''' Run httpd as a "daemon" thread to allow scheduler loop '''
thread.start_new_thread(runStatus, (HTTP_PORT,))
schedule.every(schedule_chk_interval_seconds).seconds.do(job)

''' MAIN '''
while True:
    schedule.run_pending()
    time.sleep(timer_sleep)

