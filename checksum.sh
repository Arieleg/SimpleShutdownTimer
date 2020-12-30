#!/bin/bash
ls . -p | grep -v / | while read FILE
	do
		echo | sha256sum $FILE >> sha256sum.txt
	done

