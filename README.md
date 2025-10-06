This is a script to be run as a Docker container.

It provides a html page showing what a Kodi device is playing and displays artwork, progress bar, media information, plot etc with background slideshow if more than one fanart is found. 

## Features

- **Real-time Playback Detection**: Automatically detects when Kodi starts/stops playing media
- **Playback State Monitoring**: Shows current play/pause state with visual indicators
- **Interactive Playback Controls**: Play/pause buttons with smooth fade transitions
- **Smart Timer Management**: Timer stops when paused and resyncs on resume
- **Comprehensive Media Support**: Episodes, movies, and music with appropriate artwork
- **Background Slideshow**: Multiple fanart images for enhanced visual experience
- **Responsive Design**: Clean, modern interface that works on various screen sizes

## Playback Controls

The interface includes:
- **Play/Pause Button**: Visual indicator that changes based on playback state
- **Smooth Transitions**: 500ms fade in/out effects when switching between play/pause states
- **Real-time Updates**: Button state updates automatically as you control playback in Kodi
- **Timer Integration**: Button positioned to the left of the playback timer
- **Interactive Discart Animation**: Discart (CD/DVD/Bluray artwork) spins during playback and pauses when media is paused

## Theater-Style Marquee Banner

The interface features a customizable marquee banner that displays the current media title in a theater sign style:
- **Auto-hide Toggle**: Click the half-circle tab to hide/show the marquee banner
- **Dynamic Color Shifting**: Smooth color transitions that cycle through different hues
- **Smooth Animations**: Fade in/out effects when toggling visibility
- **Responsive Design**: Banner adapts to different screen sizes
- **Clean Integration**: Seamlessly integrated with the overall design

### Text Shimmer Effect

The marquee banner includes an elegant text shimmer effect that adds visual interest:
- **Automatic Triggering**: Effect runs every 10 seconds when media is playing
- **Letter-by-Letter Animation**: Each letter of "NOW PLAYING" animates individually
- **Two-Stage Effect**: 
  1. **Dark Wave**: Letters fade to dark gray in sequence (80ms stagger between letters)
  2. **Shimmer Wave**: Bright orange glow sweeps across, leading the white fade
- **Perfect Timing**: Shimmer arrives first, then letters fade back to white with proper delay
- **Consistent Spacing**: Letter spacing remains identical whether effect is active or not
- **Smooth Transitions**: All animations use CSS transitions for fluid motion
- **Non-Intrusive**: Effect is subtle enough to not distract from content viewing

## Media Type Display Features

The application provides specialized displays and artwork for different media types, each optimized for the unique characteristics of TV shows, movies, and music:

### TV Shows
**Artwork Display:**
- **Show Poster**: Main TV show poster displayed prominently
- **Season Artwork**: Season-specific poster when available (shows season number and artwork)
- **ClearArt**: High-quality transparent show artwork (preferred for overlay)
- **Banner**: Wide banner artwork for show identification
- **Fanart Slideshow**: Multiple background images including show fanart and extrafanart

**Information Displayed:**
- Show title and episode title
- Season and episode numbers
- Episode plot/synopsis
- Show genre and rating
- Cast information (when available)
- Playback progress and time remaining

### Movies
**Artwork Display:**
- **Movie Poster**: Primary movie poster with cinematic styling
- **Discart**: Spinning disc/DVD/Blu-ray artwork that rotates during playback
- **ClearArt**: Transparent movie artwork for clean overlay
- **Banner**: Movie banner artwork for identification
- **Fanart Slideshow**: Cinematic background images from movie fanart and extrafanart

**Information Displayed:**
- Movie title and year
- Director and cast information
- Genre and rating
- Plot summary
- Video quality (resolution, codec, HDR type)
- Audio information (channels, codec)
- Playback progress and total runtime

### Music
**Artwork Display:**
- **Album Artwork**: Album cover displayed prominently (thumbnail or poster)
- **Artist ClearArt**: High-quality transparent artist artwork
- **Artist Banner**: Wide banner artwork for artist identification
- **Fanart Slideshow**: Artist fanart and concert/live performance images

**Information Displayed:**
- Artist name and song title
- Album name and release year
- Genre and music quality information
- Artist biography (when available from metadata)
- Album information and track details
- Playback progress and song duration

### Artwork Fallback System
Each media type follows a sophisticated fallback hierarchy to ensure optimal visual presentation:

**TV Shows:**
1. **ClearArt** → **Banner** → **Text Fallback**
2. **Season Poster** (when available) → **Show Poster** → **Default**
3. **Fanart Collection**: Main fanart + extrafanart folder images

**Movies:**
1. **ClearArt** → **Banner** → **Text Fallback**  
2. **Discart** (spinning disc artwork) for visual appeal
3. **Fanart Collection**: Movie fanart + extrafanart folder images

**Music:**
1. **ClearArt** → **Banner** → **Text Fallback**
2. **Album Artwork** (thumbnail/poster) as primary display
3. **Fanart Collection**: Artist fanart + concert/performance images

### Artwork Sources
- **Kodi's Artwork Database**: Primary source for all artwork types
- **Local Media Folders**: Scans movie/TV/music directories for additional artwork
- **Extrafanart Folders**: Automatically discovers fanart in `extrafanart/` subdirectories
- **Automatic Detection**: Script automatically detects available artwork types
- **Seamless Fallbacks**: Transitions between artwork types are smooth and automatic
- **Quality Priority**: Always displays the highest quality artwork available
- **Responsive Scaling**: All artwork types scale appropriately for different screen sizes

### Background Slideshow
When multiple fanart images are available:
- **Automatic Rotation**: Cycles through all available fanart images
- **20-Second Intervals**: Each image displays for 20 seconds
- **Smooth Transitions**: Fade effects between background changes
- **Dynamic Detection**: Automatically detects and uses all available fanart images
- **Extrafanart Support**: Scans `extrafanart/` subdirectories to find additional background images
- **Comprehensive Collection**: Includes fanart from both main directory and extrafanart folders for maximum variety

## Setup

Make sure Kodi has web control enabled

Unzip kodi-nowplaying.zip 

Edit the .env file and input the ip to your Kodi device, HTTP port and user/pass.

OPTIONAL: Create fallback and edit the kodi-nowplaying.py file and enter Kodi IP and user/pass there:
# Kodi connection details
```
KODI_HOST = os.getenv("KODI_HOST", "http://kodi_device_ip:kodi_port")

KODI_USER = os.getenv("KODI_USER", "kodi_HTTP_username")

KODI_PASS = os.getenv("KODI_PASS", "kodi_HTTP_password")
```
_________________________

Build and start container:
```docker compose build --no-cache kodi-nowplaying```
```docker compose up -d kodi-nowplaying```

Start playing media on your Kodi device

Test locally by visiting http://localhost:5001/nowplaying <- or replace localhost with the IP of the container host

Mount it as a custom Homarr iframe tile pointing to http://localhost:5001/nowplaying <- or replace localhost with the IP of the container host


