import sys
sys.path.append('/usr/lib/python3/dist-packages/')
import gi, cairo
sys.path.pop()

gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')
