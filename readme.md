##How to run
___
- -h --help: brings up a help message
- -s --sampling_method: 1 or 2 [default: 1]
    - downsample by deleting every row and column [sampling_method: 1]
    - upsample by inserting a row and column in every row and column [sampling_method: 1]
    - downsample by averaging pixels [sampling_method: 2]
    - upsample by nearest neighbor interpolation [sampling_method: 2]
    - provide image name (modify source to choose images from different directory)
___
##Known issues
___
Currently searching for exact image name in a certain directory if the image has multiple 
instances in the directory the image path will return the first result so it may not give
the exact image you were looking for but works perfect if you move the images to a new directory
and give them all unique names
___
##links
___
- [github](www.https://github.com/ch3rc/DIP3.git "github account") for code and logs
- contact me at my [UMSL email](ch3rc@umsystem.edu) if you have any questions