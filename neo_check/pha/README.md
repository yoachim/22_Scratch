Results for looking for PHAs in the presence of streaks

looks like we go from 1.627 million observations of PHAs to 1.625 million. So, as expected, no changes in the actual completeness values.


----

running in parallel on my fancy new laptop

seq 0 998 | xargs -I'{}' echo "python overlap_finder.py --lower {}" > cmnds.sh

