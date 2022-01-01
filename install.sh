#!/bin/bash
#
#------------------------------#
# Install script for jobsubmit #
#------------------------------#
#
main () {
	mkdir -p /home/$USER/jobsubmit-config
	cp -R * /home/$USER/jobsubmit-config
	echo "#"
	echo "#------------------------------------------------------------------------------"
	echo "# Path variable for jobsubmit"
	echo "#------------------------------------------------------------------------------"
	echo "export PATH=/home/$USER/jobsubmit-config:\$PATH"

}

main >>  ~/.bashrc
echo "Installation completed."
