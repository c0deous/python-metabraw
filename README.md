# python-MetaBRAW
A python-friendly Blackmagic RAW metadata parser
by Jesse Wallace (c0deous)

### Example Usage
```
>>> import metabraw
>>> braw = metabraw.metadata('testfile.braw')
>>> braw.clip['lens_type']
'.7x Sigma DC 18-35/1.7 HSM'
>>> braw.firstframe['iso']
400
```

### Dependencies
* Blackmagic RAW SDK 2.1 (earlier versions untested)
* Python 3.5+

All platforms should work but I've only tested it on Mac at the moment.

### Methods

* metadata(<BRAW File Path>, brawsdk_path=<optional>) - root class
  * **.clip**
    * returns a dictionary of general metadata (camera info, lens type)
  * **.firstframe**
    * returns a dictionary of clip specific metadata (ISO, focal length, white balance, etc)
  * **.list_clip_keys()**
    * lists all clip metadata dictionary keys
  * **.list_firstframe_keys()**
    * lists all firstframe metadata dictionary keys

### Other Info

This module works by scraping the output of an example script provided by Blackmagic. On Mac, located at ```/Applications/Blackmagic RAW/Blackmagic RAW SDK/Mac/Samples/ExtractMetadata/ExtractMetadata```

I created this out of sheer necessity and am too cowardly to deal with the C++ SDK. If you read my shitty python and wish to fix it or, even better, rewrite it to actually use the SDK please create a pull request. However, this is working for me now and anyone is free to use or modify it as needed.
