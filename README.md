# anihunter
Tired of searching manually to find upcoming anime? Want to find stuff that flies below the radar too, not just popular stuff? Give AniHunter a try!\
This simple python application takes a list of your favorite (AniList) tags and scours the AniList database for upcoming anime that contains one or more of those tags!\
It will automatically open the AniList pages for them in your browser too, so you can read more and add to your planning list if you're interested.\
AniHunter remembers things its shown you before and will only show them again if they got another relevant tag added and might be worth another look!

# FAQ
Q: Do I need an AniList account to use this?\
A: No you don't technically need one. The application will work just the same if you don't have one.\
\
Q: Do I need an internet connection to use this?\
A: Yes.\
\
Q: Why is it making me wait for a countdown before it continues loading?\
A: AniList rate-limits their API. If we make too many requests, we have to wait. Them's the rules.\
\
Q: Where are the cache files stored?\
A: They are stored in `/home/<USER>/Documents/anihunter/cache` on Linux and `C:\Users\<USER>\Documents\anihunter\cache` on Windows. You can delete this cache folder if you want to reset the application's memory\
\
Q: Where should my tag file be?\
A: By default, it should be in the same directory as the executable. Don't worry, though. AniHunter will make one for you if it doesn't exist and will try to open it in your default text editor for your convenience!\
\
Q: I encountered a problem with this program! How do I report it?\
A: Add a new issue to the project here: https://github.com/ApothecarySoft/anihunter/issues
