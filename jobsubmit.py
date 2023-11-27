#!/bin/python3
#
import os
import sys
import argparse
import textwrap
import logging
import subprocess
import signal
import shutil
import argparse
import fnmatch
from datetime import datetime
import signal
# ...
prog="jobsubmit"
description="jobsubmit is a python script designed for reading the list of commands from a file and execute in a particular order."
epilog="For bug reporting please reach out <rajeshprasanth@rediffmail.com>."
usage="jobsubmit [options]"

major_version="2"
minor_version="0"
revision_version="0"



def version():
	print("jobsubmit"+"\t"+major_version+"."+minor_version+"."+revision_version)
	print("Copyright (C) 2015 Free Software Foundation, Inc. \nThis is free software; see the source for copying conditions.  There is NO\nwarranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.")


def cleanup():
	os.system("rm -rf stdout stderr done notdone")
	exit(0)

def fullcleanup():
	os.system("rm -rf stdout stderr done notdone *.log")
	exit(0)

def commandline_parser():
	parser = argparse.ArgumentParser(prog=prog,description=description,epilog=epilog,usage=usage,formatter_class=argparse.RawTextHelpFormatter)

	parser._optionals.title = 'options'

	group = parser.add_mutually_exclusive_group()

	group.add_argument("-v","--version",dest="version",action="store_true",
						help="show program's version number and exit.")
	group.add_argument("-c","--cleanup",dest="cleanup",action="store_true",
						help="cleanup stdout and stderr directories in the current directory(if any)")

	group.add_argument("-fc","--full-cleanup",dest="fullcleanup",action="store_true",
						help="cleanup stdout, stderr directories, and logfile in the current directory(if any)")

	group.add_argument("-d","--display",dest="display",action="store",nargs=2,metavar=("[file]","all"),
						help=textwrap.dedent("""\
						use 'all' to display all the lines of command in the file.
						use a dash to display ranges of lines of command in the file (1-100).
						use a comma to display multiple lines of command in the file (1,10,45,90,99).
						use a digit to display that specific line of command alone in the file (8).
						"""))

	group.add_argument("-r","--run",dest="run",action="store",nargs=2,metavar=("[file]","all"),
						help=textwrap.dedent("""\
						use 'all' to run all the lines of command in the file.
						use a dash to run ranges of lines of command in the file (1-100).
						use a comma to run multiple lines of command in the file (1,10,45,90,99).
						use a digit to run that specific line of command alone in the file (8).
						"""))

	group.add_argument("-as","--alert-screen",dest="alertscreen",action="store_true",
						help="""refresh alertscreen for monitoring job progress.""")

	args = parser.parse_args()

	if len(sys.argv)==1:
		parser.print_help(sys.stderr)
		sys.exit(1)

	return(args)


def error_msg(str):
	print(" ----------------------------------------------")
	print(" FATAL ERROR")
	print(" ----------------------------------------------")
	print(" Fatal Error : %s" %(str))
	print(" ----------------------------------------------")

def file_check(infile):
	#-----------------------------------------------#
	# Checks if file is in the Path and is readable #
	#-----------------------------------------------#
	try:
		filepath,filename=os.path.split(infile)
	except IOError as e:
			print(e)



def range_parser(ffilename,arg_full):
	#
	#----------------------------------------#
	# Find total number of lines in the file #
	#----------------------------------------#
	#
	counter = 1
	try:
		f = open (ffilename, 'r')
		# Reading from file
		for line in f:
			if line.strip() != "":
				counter = counter + 1
		numline=counter-1
	except IOError as e:
		print(e)
		exit(-1)


	#-----------------------------------------------
	# Type :: 0 (all)
	#-----------------------------------------------

	if isinstance(arg_full,str) and arg_full == "all":
		args=list(range(1,numline+1))
		return ffilename,args
	#-----------------------------------------------
	# Type :: 2 (comma separated)
	#-----------------------------------------------

	elif arg_full.find(',') > -1:
		args=arg_full.split(',')

		arg1=[int(i) for i in args]
		args=arg1
		if max(args) > numline:
			error_msg("num > max_line in file")
			exit(-1)
		if min(args) == 0:
			error_msg("num <= 0")
			exit(-1)
		return ffilename,args
	#-----------------------------------------------
	# Type :: 3 (hyphenated range)
	#-----------------------------------------------
	elif arg_full.find('-') > -1:
		start_line=int(arg_full.split('-')[0])
		end_line=int(arg_full.split('-')[1])

		if end_line > numline:
			error_msg("num <= 0")
			exit(-1)

		if start_line > numline:
			error_msg("start_line > max_line in file")
			exit(-1)

		if start_line > end_line :
			error_msg("start_line > end_line")
			exit(-1)

		if start_line ==0 :
			error_msg("start_line <= 0")
			exit(-1)
		args=list(range(start_line,end_line+1))
		return ffilename,args
	#-----------------------------------------------
	# Type :: 1 (single digit)
	#-----------------------------------------------
	else:
		args=[]
		arg1=int(arg_full)
		args.append(arg1)
		if max(args) > numline:
			error_msg("num > max_line in file")
			exit(-1)
		if min(args) <= 0:
			error_msg("num <= 0")
			exit(-1)
		return ffilename,args

def display(infile,argument):
	f = open (infile, 'r')

	job=f.readlines()
	for i in argument:
		j = i - 1
		cmd1=job[j]
		cmd=cmd1.strip()
		print("line # %5d | %s" %(i,cmd))
	f.close()


	exit(0)


def handle_exceptions(sig, frame):
	raise(SystemExit)

def logger_banner(job):
	#--------------------------------------#
	# Create temporary directories         #
	#--------------------------------------#
	os.makedirs("stdout", exist_ok = True)
	os.makedirs("stderr", exist_ok = True)
	os.makedirs("notdone", exist_ok = True)
	os.makedirs("done", exist_ok = True)
	os.makedirs(os.path.expanduser('~')+"/.jobsubmit_config/", exist_ok = True)

	#--------------------------------------#
	# Initialize logger and logging setup  #
	#--------------------------------------#
	logdir = os.path.expanduser('~')+"/.jobsubmit_config/"+job.joblist_logname
	logging.basicConfig(filename=logdir, filemode='w', format='%(asctime)s - %(process)d - %(levelname)8s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

	#--------------------------------------#
	# Print Banner message in logger  #
	#--------------------------------------#
	logging.info('================================')
	logging.info('>>>Program Started')
	logging.info('================================')
	logging.info("jobsubmit"+"\t"+major_version+"."+minor_version+"."+revision_version)
	logging.info('--------------------------------')
	logging.info('Input file found in directory: %s', job.joblist_filepath)
	logging.info('Current directory: %s', job.current_directory)
	logging.info('Input file : %s', job.joblist_filename)
	logging.info('Reading input file %s', job.joblist_filename)
	logging.info('--------------------------------')
	logging.info('Queued Workflow')
	logging.info('--------------------------------')
	counter = 1
	for i in job.joblist_runrange:
		logging.info('Queued Workflow # %5d from line # %5d',counter,i)
		counter = counter + 1
	logging.info('--------------------------------')
	logging.info('Total Workflows queued : %5d',len(job.joblist_runrange))
	logging.info('--------------------------------')

def logger_summary(jobclass,**kwargs):
	logging.info('--------------------------------')
	logging.info('Summary')
	logging.info('--------------------------------')
	logging.info('Completed workflows     : %5d',kwargs["completed_counter"])
	logging.info('Failed workflows        : %5d',kwargs["failed_counter"])
	logging.info('Aborted workflows       : %5d',kwargs["aborted_counter"])
	logging.info('Interupted workflows    : %5d',kwargs["interupted_counter"])
	logging.info('Pending workflows       : %5d',len(jobclass.joblist_runrange) - kwargs["completed_counter"]-kwargs["failed_counter"]-kwargs["aborted_counter"]-kwargs["interupted_counter"])
	logging.info('--------------------------------')
	logging.info('================================')
	logging.info('>>>Program Completed')
	logging.info('================================')

def logger_event(jobclass,**kwargs):

	if kwargs["event_type"] == "started":
		logging.info(
		'Workflow # %5d of %5d %12s from %s at line # %5d with       pid: %8d',\
		kwargs["wf_counter"],\
		len(jobclass.joblist_runrange) ,\
		kwargs["event_type"],\
		jobclass.joblist_filename,\
		kwargs["job_line"],\
		kwargs["jobpid"] \
		)
	if kwargs["event_type"] == "completed" or kwargs["event_type"] == "failed" or kwargs["event_type"] == "interupted" or kwargs["event_type"] == "aborted":
		logging.info(
		'Workflow # %5d of %5d %12s from %s at line # %5d with exit code: %8d',\
		kwargs["wf_counter"],\
		len(jobclass.joblist_runrange) ,\
		kwargs["event_type"],\
		jobclass.joblist_filename,\
		kwargs["job_line"],\
		kwargs["exit_code"] \
		)

	# if kwargs["event_type"] == "failed":
	# 	logging.error(
	# 	'Workflow # %5d of %5d %12s from %s at line # %5d with exit code: %8d',\
	# 	kwargs["wf_counter"],\
	# 	len(jobclass.joblist_runrange) ,\
	# 	kwargs["event_type"],\
	# 	jobclass.joblist_filename,\
	# 	kwargs["job_line"],\
	# 	kwargs["exit_code"] \
	# 	)
	#
	# if kwargs["event_type"] == "aborted":
	# 	logging.error(
	# 	'Workflow # %5d of %5d %12s from %s at line # %5d with exit code: %8d',\
	# 	kwargs["wf_counter"],\
	# 	len(jobclass.joblist_runrange) ,\
	# 	kwargs["event_type"],\
	# 	jobclass.joblist_filename,\
	# 	kwargs["job_line"],\
	# 	kwargs["exit_code"] \
	# 	)
	#
	# if kwargs["event_type"] == "interupted":
	# 	logging.critical(
	# 	'Workflow # %5d of %5d %12s from %s at line # %5d with exit code: %8d',\
	# 	kwargs["wf_counter"],\
	# 	len(jobclass.joblist_runrange) ,\
	# 	kwargs["event_type"],\
	# 	jobclass.joblist_filename,\
	# 	kwargs["job_line"],\
	# 	kwargs["exit_code"] \
	# 	)
	#
	# if kwargs["log_level"] == "critical":
	# 	logging.critical(
	# 	kwargs["statement"]\
	# 	)

class job_init():
	def __init__(self, joblist_filepath=None, joblist_filename=None, current_directory=None,joblist_runrange=None,joblist_logname=None):
		self.joblist_filepath = joblist_filepath
		self.joblist_filename = joblist_filename
		self.current_directory = current_directory
		self.joblist_runrange = joblist_runrange
		self.joblist_logname = joblist_logname


	def total_lines(self):
		#
		#----------------------------------------#
		# Find total number of lines in the file #
		#----------------------------------------#
		#
		counter = 1
		try:
			file = str(self.joblist_filepath) +"/"+ str(self.joblist_filename)
			f = open (file, 'r')
			# Reading from file
			for line in f:
				if line.strip() != "":
					counter = counter + 1
			numline=counter-1
			return numline
		except IOError as e:
			print(e)
			exit(-1)

def runjobs(infile,argument):

	job = job_init()

	in_filepath,in_filename=os.path.split(infile)

	if in_filepath == "" or in_filepath == ".":
		in_filepath=os.getcwd()

	job.joblist_filepath = in_filepath
	job.joblist_filename = in_filename
	job.current_directory = os.getcwd()
	job.joblist_runrange = argument
	job.joblist_logname = 'jobsubmit.' + str(datetime.now().strftime("%y%m%d%H%M%S%f")) + '.log'
	print("\nMonitor workflow status at %s" %(os.path.expanduser('~')+"/.jobsubmit_config/"+job.joblist_logname))
	logger_banner(job)

	f = open (infile, 'r')
	job_line = f.readlines()

	wf_counter = 1
	failed_counter = 0
	completed_counter = 0
	aborted_counter = 0
	interupted_counter = 0

	for i in argument:

		cmd=job_line[i-1].strip()

		fout = open("stdout/"+job.joblist_filename+"_line_"+str(i)+".out",'w')
		ferr = open("stderr/"+job.joblist_filename+"_line_"+str(i)+".err",'w')

		proc = subprocess.Popen(cmd,shell=True,stdout=fout,stderr=ferr)
		#logging.info('Workflow # %d of %d started from %s at line # %d with pid: %d',wf_counter,len(argument) ,filename,i,proc.pid)
		logger_event(job,event_type="started",wf_counter=wf_counter,job_line = i,jobpid = proc.pid )
		os.system(str("touch "+os.path.expanduser('~')+"/.jobsubmit_config/"+job.joblist_logname+".lock"))
		try:
			#-----------------------------------#
			# Wait for the process to complete  #
			#-----------------------------------#
			proc.wait()
			signal.signal(signal.SIGTERM, handle_exceptions)
		except (KeyboardInterrupt,SystemExit):
			#-----------------------------------#
			# Kill the running processes  #
			#-----------------------------------#
			proc.kill()
			#logger_event(job,log_level="critical",event_type="aborted",wf_counter=wf_counter,job_line = i,exit_code = 130)
			logger_event(job,event_type="interupted",wf_counter=wf_counter,job_line = i,exit_code = 130)
			interupted_counter = interupted_counter + 1
			logger_summary(job,failed_counter=failed_counter,completed_counter=completed_counter,aborted_counter=aborted_counter,interupted_counter=interupted_counter)
			print("\nEncountered Manual interupt from user. Terminating all workflows.")
			print("\nTerminated at %s" %(str(datetime.now().strftime("%y/%m/%d %H:%M:%S:%f"))))
			print("--------------------------------------------------------------------------")
			os.system(str("rm -rf "+os.path.expanduser('~')+"/.jobsubmit_config/"+job.joblist_logname+".lock"))
			exit(-1)

		if proc.returncode < 0:
			logger_event(job,log_level="error",event_type="aborted",wf_counter=wf_counter,job_line = i,exit_code = proc.returncode)
			fnotdone = open("notdone/"+job.joblist_filename+"_line_"+str(i)+".lock",'w')
			aborted_counter = aborted_counter + 1

		elif proc.returncode > 0:
			logger_event(job,log_level="error",event_type="failed",wf_counter=wf_counter,job_line = i,exit_code = proc.returncode)
			fnotdone = open("notdone/"+job.joblist_filename+"_line_"+str(i)+".lock",'w')
			failed_counter = failed_counter + 1
		else:
			logger_event(job,event_type="completed",wf_counter=wf_counter,job_line = i,exit_code = proc.returncode)
			fdone = open("done/"+job.joblist_filename+"_line_"+str(i)+".lock",'w')
			completed_counter = completed_counter + 1
		wf_counter = wf_counter + 1
	logger_summary(job,failed_counter=failed_counter,completed_counter=completed_counter,aborted_counter=aborted_counter,interupted_counter=interupted_counter)
	os.system(str("rm -rf "+os.path.expanduser('~')+"/.jobsubmit_config/"+job.joblist_logname+".lock"))


def main():

	arg = commandline_parser()

	if arg.version:
		version()

	if arg.cleanup:
		cleanup()

	if arg.fullcleanup:
		fullcleanup()

	if arg.display:
		fname,run_range = range_parser(arg.display[0], arg.display[1])
		#file_check(fname)
		display(fname,run_range)

	if arg.run:
		fname,run_range = range_parser(arg.run[0], arg.run[1])
		print("--------------------------------------------------------------------------")
		print("Program : %s" %(prog))
		print("Version : %s.%s.%s" %(major_version,minor_version,revision_version))
		print("--------------------------------------------------------------------------")
		print("Copyright (C) 2015 Free Software Foundation, Inc.")
		print("This is free software; see the source for copying conditions.  There is NO")
		print("warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.")
		print("--------------------------------------------------------------------------")
		print("\nInvoked at %s" %(str(datetime.now().strftime("%y/%m/%d %H:%M:%S:%f"))))
		print("\nStarting workflows " )
		runjobs(fname,run_range)
		print("\nEnded Normally at %s" %(str(datetime.now().strftime("%y/%m/%d %H:%M:%S:%f"))))
		print("--------------------------------------------------------------------------")
		exit(0)
	if arg.alertscreen:
		print("WIP")

if __name__ == '__main__':
    main()
