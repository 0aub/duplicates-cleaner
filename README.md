# duplicates-cleaner
Simple script to delete duplicated files from specific directory. Detecting the duplicated files usually done by comparing the files hashes. I already implemented that in the code and tried in on many cases. I noticed that comparing hashes did not work for some duplicated videos I download from differents sources. So, I made the default algorithm is to detect the duplicated videos and audio files by comparing files sizes in KB and durations in seconds but any other type of files will be detected by the hash method. Of course, you have the ability to choose which algorithm you want to use. I hope this code helps you in a way or another.

# usage
Script arguments
<pre>
<li> -d    --dir
<li> -ho   --hash-only
<li> -s    --save
</pre>

To use the default algorithm
```
python duplicates.py  --dir [directory path] 
```
To use only hash algorithm
```
python duplicates.py  --dir [directory path] --hash-only
```
After detecting the duplicated files, it will ask you to press anything to confirm the deletion. You can save the detected files names in a file before confirming the deletion to be aware of what exactly will be deleted
```
python duplicates.py  --dir [directory path] --hash-only --save
```

# future enhancement
In the future, I will use threading to make the code too much faster


<br><br><br><br><br><br><br>
*Feel free to write any suggestions you think about.*
