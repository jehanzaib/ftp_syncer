# Copyright (c) 2014, Muhammad Jehanzaib <mjb@iknowl.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import yaml
import time
import logging
from optparse import OptionParser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import LoggingEventHandler
from ftplib import FTP, error_reply, error_perm



argparse = OptionParser()
argparse.add_option("-c", "--config", dest="config",
                                        help = "Required. When set, it gets FTP credentials from given config file.",
                                        metavar="FILE")
argparse.add_option("-s", "--serverpath", dest="serverpath",
																				help = "Required. When set, the given remote directory is kept in sync with local directory.",
																				metavar="PATH")
argparse.add_option("-l", "--localpath", dest="localpath",
																				help = "Required. When set, the given local directory is kept in sync with remote directory.",
																				metavar="PATH")
args = argparse.parse_args()

if len(args) != 2 or args[0].config == None or args[0].serverpath == None or args[0].localpath == None:
	argparse.error("Incorrect number of arguments given. See --help or -h for help.")

global config
config = yaml.load(file(args[0].config, 'r'))

global server_path
server_path = args[0].serverpath

global local_path
local_path = args[0].localpath



def ftp_object():
  ftp = FTP(config['ftp_host'], config['ftp_user'], config['ftp_password'])
  ftp.cwd(server_path)

  return ftp


def ftp_syncer(src_object, destination_object, ftp_command, is_directory):
  ftp = ftp_object()

  if is_directory:
    if ftp_command == 'STOR ':
      ftp.mkd(destination_object)
    elif ftp_command == 'DELE ':
      ftp.rmd(destination_object)
  else:
    if ftp_command == 'STOR ':
      ftp.storbinary('STOR ' + destination_object, open(src_object, 'rb'))
    elif ftp_command == 'DELE ':
      ftp.delete(destination_object)

  ftp.close()


def sync_with_server(destination_object, ftp_command, is_directory):
  try:
    ftp_syncer(local_path + destination_object, destination_object, ftp_command, is_directory)
  except:
    print destination_object + ' unable to be synced with remote server.'
  else:
    print destination_object + ' synced with remote server.'


def initiate_sync(object_from_event, ftp_event, is_directory):
  src_object = object_from_event.split(local_path)

  if(len(src_object) > 1):
    sync_with_server(src_object[1], ftp_event, is_directory)
  else:
    return 'File index out of range.'


class CustomEventHandler(FileSystemEventHandler):
  def on_modified(self, event):
    initiate_sync(event.src_path, 'STOR ', event.is_directory)
    super(CustomEventHandler, self).on_modified(self)

  def on_created(self, event):
    initiate_sync(event.src_path, 'STOR ', event.is_directory)
    super(CustomEventHandler, self).on_modified(self)

  def on_deleted(self, event):
    initiate_sync(event.src_path, 'DELE ', event.is_directory)
    super(CustomEventHandler, self).on_deleted(self)


event_handler = CustomEventHandler()
observer = Observer()
observer.schedule(event_handler, local_path, recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
