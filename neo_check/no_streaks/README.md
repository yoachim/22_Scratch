Toss all observations that have a streak of anykind


seq 1000 | xargs -I'{}' echo "python find_streaks.py --lower {}" > cmnds.sh

cat cmnds.sh | parallel -j 8
