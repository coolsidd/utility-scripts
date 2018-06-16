import youtube_dl

# Creating/getting archive file containing list of already downloaded videos
file = open(input("Enter file name to check for previously downloaded videos: "
                  "\n (can be new or existing file) \n -> "), "a+")
check_WLplaylist = file.name

# Defining options for YoutubeDL object
options_parameters = {
    'username': input('Please enter google username/email id: '),
    'password': input('Please enter gmail password: '),
    'download_archive': check_WLplaylist,
}

# Downloading!!
with youtube_dl.YoutubeDL(options_parameters) as ydl:
    ydl.download(['https://www.youtube.com/playlist?list=WL'])
