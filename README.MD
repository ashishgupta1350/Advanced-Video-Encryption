Failed, because unlike images, videos use compression algorithms to compress each frame in the video. In opencv, it is not possible to use 
a lossless compression. The lossless compression results in 100's of mbs of file in 4-5 seconds video, which is really hard to read let alone write to!
The lossless compression is stegnographically unreadable for some reason, though my code is working to hande that! :( 

<br />

#

Lets discuss with some one who is expert in video compression. If you are one, please do talk. I am looking forward to comments in issues section of this repo. :'(
Image compression works. Video encryption works as well. The problem is writing that compression and then rereading it correctly. It is 
tough to implement everything together.

<br/>

#

### This repo's code is complete, the opencv cv2.VideoWriter is not equiped to handeling the video stenography( hidding data in videos).
