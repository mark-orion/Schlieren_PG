# Schlieren_PG
Schlieren videography pattern generator. It can be used to generate background patterns for schlieren videography experiments. Together with PyFSPro it is a complete schlieren imaging system..

## Usage
* start with python schlieren_pg.py and use Kivy UI elements to adjust pattern type and size.  
CHQ - Chequerboard pattern
HOR - Horizontal lines
VER - Vertical lines
RND - Radomized squares
* command line options:  
python schlieren_pg.py - [OPTIONS]  
-h, --help            show help message and exit  
-n, --no_controlbar   hide controlbar  
-p PATTERN_TYPE, --pattern_type PATTERN_TYPE (CHQ, HOR, VER, RND)  
-s PATTERN_SIZE, --pattern_size PATTERN_SIZE  
