# BDL_8CH
**Engine API version**: `2.0.0`

An 8ch.net engine for BDL.


## Installation
```shell
$> git clone https://github.com/Wawachoo/BDL_8CH
$> cd BDL_8CH
$> python3.5 setup.py install
```


## Supported URLs
This engine supports URL of type `https://8ch.net/SECTION/res/THREAD_ID`.


## Repository name
The engine returns the thread name from from the thread page.


## Metadata
This engine export the following metadata:
* `{thread_section}`: thread section (ex: `g`);
* `{thread_name}`: thread name (ex: `the name of the thread`);
* `{thread_id}`: thread identifier (ex: `1234567`)
* `{post_id}`: Current item post's ID (all images within a same post share the same post ID)
