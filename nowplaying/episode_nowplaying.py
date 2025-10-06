"""
TV Episode-specific HTML generation for Kodi Now Playing application.
Handles TV episode display with show poster, season poster, and episode information.
"""

def generate_html(item, session_id, downloaded_art, progress_data, details):
    """
    Generate HTML for TV episode display.
    
    Args:
        item (dict): Media item from Kodi API
        session_id (str): Session ID for file naming
        downloaded_art (dict): Downloaded artwork files
        progress_data (dict): Playback progress information
        details (dict): Detailed media information
        
    Returns:
        str: HTML content for TV episode display
    """
    # Extract URLs for artwork
    # For TV episodes, 'poster' is typically the show poster, and we need to get season poster separately
    show_poster_url = f"/media/{downloaded_art.get('poster')}" if downloaded_art.get("poster") else ""
    season_poster_url = f"/media/{downloaded_art.get('season.poster')}" if downloaded_art.get("season.poster") else ""
    
    # Collect all fanart variants for slideshow
    fanart_variants = []
    
    # Check for all possible fanart variants in order of preference
    fanart_keys = ["fanart", "fanart1", "fanart2", "fanart3", "fanart4", "fanart5", "fanart6", "fanart7", "fanart8", "fanart9"]
    for fanart_key in fanart_keys:
        if downloaded_art.get(fanart_key):
            fanart_variants.append(f"/media/{downloaded_art.get(fanart_key)}")
    
    # Also check for extrafanart folder images (dynamic keys like extrafanart_main, extrafanart_fanart2, etc.)
    for key, value in downloaded_art.items():
        if key.startswith("extrafanart"):
            fanart_variants.append(f"/media/{value}")
    
    # Use first fanart as primary, or empty string if none
    fanart_url = fanart_variants[0] if fanart_variants else ""
    
    # Debug logging for fanart variants
    print(f"[DEBUG] Episode fanart variants found: {len(fanart_variants)}", flush=True)
    print(f"[DEBUG] Episode fanart variants: {fanart_variants}", flush=True)
    
    banner_url = f"/media/{downloaded_art.get('banner')}" if downloaded_art.get("banner") else ""
    clearlogo_url = f"/media/{downloaded_art.get('clearlogo')}" if downloaded_art.get("clearlogo") else ""
    clearart_url = f"/media/{downloaded_art.get('clearart')}" if downloaded_art.get("clearart") else ""
    
    # Extract TV episode information
    title = item.get("title", "Untitled Episode")
    show = item.get("showtitle", "")
    season = item.get("season", 0)
    episode = item.get("episode", 0)
    plot = item.get("plot", item.get("description", ""))
    
    # Create episode subtitle components for badges
    season_badge = f"Season {season}" if season > 0 else ""
    episode_badge = f"Episode {episode}" if episode > 0 else ""
    title_badge = title if title else ""
    
    # Extract IMDb ID and construct URL - ensure details is a dict
    if not isinstance(details, dict):
        details = {}
    imdb_id = details.get("uniqueid", {}).get("imdb", "")
    imdb_url = f"https://www.imdb.com/title/{imdb_id}" if imdb_id else ""
    
    # Get rating from details or fallback
    rating = round(details.get("rating", 0.0), 1)
    rating_html = f"<strong>⭐ {rating}</strong>" if rating > 0 else ""
    
    # Initialize defaults
    director_names = "N/A"
    cast_names = "N/A"
    hdr_type = "SDR"
    audio_languages = "N/A"
    subtitle_languages = "N/A"
    
    # Extract streamdetails - ensure details is a dict
    if not isinstance(details, dict):
        details = {}
    streamdetails = details.get("streamdetails", {})
    if not isinstance(streamdetails, dict):
        streamdetails = {}
    video_info = streamdetails.get("video", [{}])[0] if isinstance(streamdetails.get("video"), list) and len(streamdetails.get("video", [])) > 0 else {}
    audio_info = streamdetails.get("audio", []) if isinstance(streamdetails.get("audio"), list) else []
    subtitle_info = streamdetails.get("subtitle", []) if isinstance(streamdetails.get("subtitle"), list) else []
    
    # HDR type
    hdr_type = video_info.get("hdrtype", "").upper() or "SDR"
    
    # Audio languages
    audio_languages = ", ".join(sorted(set(
        a.get("language", "")[:3].upper() for a in audio_info if a.get("language")
    ))) or "N/A"
    
    # Subtitle languages
    subtitle_languages = ", ".join(sorted(set(
        s.get("language", "")[:3].upper() for s in subtitle_info if s.get("language")
    ))) or "N/A"
    
    # Director - ensure details is a dict
    if not isinstance(details, dict):
        details = {}
    if "director" in details:
        director_list = details.get("director", [])
        if isinstance(director_list, list):
            director_names = ", ".join(director_list) or "N/A"
    
    # Cast - limit to top 10 actors
    cast_list = details.get("cast", [])
    if isinstance(cast_list, list) and cast_list:
        cast_names = ", ".join([c.get("name") for c in cast_list[:10] if isinstance(c, dict) and c.get("name")]) or "N/A"
    
    # Genre and formatting
    genre_list = details.get("genre", [])
    if not isinstance(genre_list, list):
        genre_list = []
    genres = [g.capitalize() for g in genre_list]
    genre_badges = genres[:3]
    
    # Format media info
    resolution = "Unknown"
    height = video_info.get("height", 0)
    if height >= 2160:
        resolution = "4K"
    elif height >= 1080:
        resolution = "1080p"
    elif height >= 720:
        resolution = "720p"
    
    video_codec = video_info.get("codec", "Unknown").upper()
    audio_codec = audio_info[0].get("codec", "Unknown").upper() if audio_info else "Unknown"
    channels = audio_info[0].get("channels", 0) if audio_info else 0
    
    # Playback progress
    elapsed = progress_data.get("elapsed", 0)
    duration = progress_data.get("duration", 0)
    percent = int((elapsed / duration) * 100) if duration else 0
    paused = progress_data.get("paused", False)
    
    # Generate HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
      <style>
        body {{
          font-family: sans-serif;
          animation: fadeIn 1s;
          position: relative;
          margin: 0;
          padding: 0;
          opacity: 1;
          transition: opacity 1.5s ease;
        }}
        
        /* Fanart Slideshow Styles */
        .fanart-container {{
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: -1;
        }}
        
        .fanart-slide {{
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-size: cover;
          background-position: center;
          background-repeat: no-repeat;
          opacity: 0;
          transition: opacity 2s ease-in-out;
        }}
        
        .fanart-slide.active {{
          opacity: 1;
        }}
        
        .fanart-slide.fade-out {{
          opacity: 0;
        }}
        body.fade-out {{
          opacity: 0;
        }}
        .content {{
          position: relative;
          background: rgba(0,0,0,0.5);
          border-radius: 12px;
          padding: 40px;
          backdrop-filter: blur(5px);
          box-shadow: 0 8px 32px rgba(0,0,0,0.8);
          display: flex;
          gap: 40px;
          color: white;
        }}
        .left-section {{
          display: flex;
          gap: 40px;
        }}
        .right-section {{
          display: flex;
          align-items: center;
          justify-content: center;
        }}
        .poster-container {{
          display: flex;
          flex-direction: column;
          gap: 20px;
          align-items: flex-start;
        }}
        .show-poster {{
          height: 300px;
          border-radius: 8px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.6);
          position: relative;
          z-index: 2;
        }}
        .season-poster {{
          height: 300px;
          border-radius: 8px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.6);
          position: relative;
          z-index: 2;
        }}
        .progress {{
          background: #2a2a2a;
          border-radius: 15px;
          height: 20px;
          margin-top: 6px;
          overflow: hidden;
          border: 1px solid rgba(0,0,0,0.75);
          box-shadow: 
            inset 0 1px 0 rgba(255,255,255,0.1),
            inset 0 0 5px rgba(0,0,0,0.3),
            0 2px 2px rgba(255,255,255,0.1),
            inset 0 5px 10px rgba(0,0,0,0.4);
          position: relative;
        }}
        .bar {{
          background: linear-gradient(135deg, #4caf50 0%, #45a049 50%, #4caf50 100%);
          height: 20px;
          border-radius: 15px 3px 3px 15px;
          width: {percent}%;
          transition: width 0.5s;
          position: relative;
          box-shadow: 
            inset 0 8px 0 rgba(255,255,255,0.2),
            inset 0 1px 1px rgba(0,0,0,0.125);
          border-right: 1px solid rgba(0,0,0,0.3);
        }}
        .small {{
          font-size: 0.9em;
          color: #ccc;
        }}
        .badges {{
          display: flex;
          gap: 8px;
          margin-top: 10px;
          flex-wrap: wrap;
          align-items: center;
        }}
        .badge {{
          background: #333;
          color: white;
          padding: 4px 10px;
          border-radius: 20px;
          font-size: 0.8em;
          box-shadow: 0 2px 6px rgba(0,0,0,0.4);
        }}
        .episode-badges {{
          display: flex;
          gap: 10px;
          margin: 10px 0;
          flex-wrap: wrap;
        }}
        .episode-badge {{
          background: #4caf50;
          color: white;
          padding: 8px 15px;
          border-radius: 25px;
          font-size: 1.0em;
          font-weight: bold;
          box-shadow: 0 3px 8px rgba(0,0,0,0.4);
        }}
        .badge-imdb {{
          display: flex;
          align-items: center;
          gap: 4px;
          background: #f5c518;
          color: black;
          padding: 4px 10px;
          border-radius: 20px;
          font-size: 0.8em;
          box-shadow: 0 2px 6px rgba(0,0,0,0.4);
          text-decoration: none;
          font-weight: bold;
        }}
        .badge-imdb img {{
          height: 14px;
        }}
        
        #playback-button {{
          display: inline-block !important;
          vertical-align: middle;
          margin-right: 4px;
        }}
        .banner {{
          display: block;
          margin-bottom: 10px;
          max-width: 360px;
          width: 100%;
        }}
        .logo {{
          display: block;
          margin-bottom: 10px;
          max-height: 150px;
        }}
        .clearart {{
          display: block;
          max-height: 400px;
          max-width: 300px;
        }}
        .episode-info {{
          margin-bottom: 20px;
        }}
        .episode-title {{
          font-size: 1.2em;
          font-weight: bold;
          margin-bottom: 5px;
        }}
        .show-title {{
          font-size: 1.5em;
          font-weight: bold;
          margin-bottom: 10px;
          color: #4caf50;
        }}
        .marquee {{
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 80px;
          background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
          border: 3px solid #333;
          border-radius: 0 0 15px 15px;
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1000;
          box-shadow: 0 4px 20px rgba(0,0,0,0.8);
          margin-bottom: 20px;
        }}
        .marquee-toggle {{
          position: absolute;
          bottom: -15px;
          left: 50%;
          transform: translateX(-50%);
          width: 50px;
          height: 15px;
          background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
          border: none;
          border-radius: 0 0 25px 25px;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: all 0.3s ease;
          z-index: 1001;
        }}
        .marquee-toggle::before {{
          content: "";
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: linear-gradient(45deg, #ff6b35, #f7931e, #ff6b35, #f7931e);
          border-radius: 0 0 25px 25px;
          z-index: -1;
          animation: marqueeGlow 2s ease-in-out infinite alternate;
        }}
        .marquee-toggle:hover {{
          transform: translateX(-50%) scale(1.05);
        }}
        .marquee-toggle.hidden {{
          background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
        }}
        .marquee-toggle.hidden::before {{
          opacity: 0.5;
        }}
        .arrow {{
          width: 0;
          height: 0;
          border-left: 8px solid transparent;
          border-right: 8px solid transparent;
          border-bottom: 12px solid white;
          transition: transform 0.3s ease;
        }}
        .arrow.up {{
          border-bottom: none;
          border-top: 12px solid white;
        }}
        .marquee::before {{
          content: "";
          position: absolute;
          top: -8px;
          left: -8px;
          right: -8px;
          bottom: -8px;
          background: linear-gradient(45deg, #ff6b35, #f7931e, #ff6b35, #f7931e);
          border-radius: 0 0 20px 20px;
          z-index: -1;
          animation: marqueeGlow 2s ease-in-out infinite alternate;
        }}
        .marquee-text {{
          font-family: 'Arial Black', Arial, sans-serif;
          font-size: 2.2em;
          font-weight: 900;
          color: #fff;
          text-shadow: 
            0 0 10px #ff6b35,
            0 0 20px #ff6b35,
            0 0 30px #ff6b35,
            2px 2px 4px rgba(0,0,0,0.8);
          letter-spacing: 4px;
          text-transform: uppercase;
          animation: marqueePulse 1.5s ease-in-out infinite alternate;
        }}
        .marquee-text.shimmer {{
          animation: marqueePulse 1.5s ease-in-out infinite alternate;
        }}
        .marquee-text .letter {{
          margin-right: 4px;
        }}
        .marquee-text .letter:last-child {{
          margin-right: 0px;
        }}
        .marquee-text .letter:nth-child(4) {{
          margin-right: 0px;
        }}
        .marquee-text.shimmer .letter {{
          display: inline-block;
          color: #fff;
          text-shadow: 0 0 10px #ff6b35, 0 0 20px #ff6b35, 0 0 30px #ff6b35, 2px 2px 4px rgba(0,0,0,0.8);
          animation: letterDarkWave 0.2s ease-in-out forwards, letterShimmer 0.3s ease-in-out 1.0s forwards, letterFadeToWhite 0.3s ease-in-out 1.1s forwards;
          animation-fill-mode: forwards;
        }}
        .marquee-text.shimmer .letter:nth-child(1) {{ animation-delay: 0s, 1.0s, 1.1s; }}
        .marquee-text.shimmer .letter:nth-child(2) {{ animation-delay: 0.08s, 1.08s, 1.18s; }}
        .marquee-text.shimmer .letter:nth-child(3) {{ animation-delay: 0.16s, 1.16s, 1.26s; }}
        .marquee-text.shimmer .letter:nth-child(4) {{ animation-delay: 0.24s, 1.24s, 1.34s; }}
        .marquee-text.shimmer .letter:nth-child(5) {{ animation-delay: 0.32s, 1.32s, 1.42s; }}
        .marquee-text.shimmer .letter:nth-child(6) {{ animation-delay: 0.4s, 1.4s, 1.5s; }}
        .marquee-text.shimmer .letter:nth-child(7) {{ animation-delay: 0.48s, 1.48s, 1.58s; }}
        .marquee-text.shimmer .letter:nth-child(8) {{ animation-delay: 0.56s, 1.56s, 1.66s; }}
        .marquee-text.shimmer .letter:nth-child(9) {{ animation-delay: 0.64s, 1.64s, 1.74s; }}
        .marquee-text.shimmer .letter:nth-child(10) {{ animation-delay: 0.72s, 1.72s, 1.82s; }}
        .marquee-text.shimmer .letter:nth-child(11) {{ animation-delay: 0.8s, 1.8s, 1.9s; }}
        @keyframes letterDarkWave {{
          0% {{
            color: #fff;
            text-shadow: 0 0 10px #ff6b35, 0 0 20px #ff6b35, 0 0 30px #ff6b35, 2px 2px 4px rgba(0,0,0,0.8);
          }}
          100% {{
            color: #222;
            text-shadow: none;
          }}
        }}
        @keyframes letterShimmer {{
          0% {{
            color: #222;
            text-shadow: none;
          }}
          100% {{
            color: #222;
            text-shadow: none;
          }}
        }}
        @keyframes letterFadeToWhite {{
          0% {{
            color: #222;
            text-shadow: none;
          }}
          100% {{
            color: #fff;
            text-shadow: 0 0 10px #ff6b35, 0 0 20px #ff6b35, 0 0 30px #ff6b35, 2px 2px 4px rgba(0,0,0,0.8);
          }}
        }}
        @keyframes marqueeGlow {{
          0% {{ opacity: 0.7; }}
          100% {{ opacity: 1; }}
        }}
        @keyframes marqueePulse {{
          0% {{ 
            text-shadow: 
              0 0 10px #ff6b35,
              0 0 20px #ff6b35,
              0 0 30px #ff6b35,
              2px 2px 4px rgba(0,0,0,0.8);
          }}
          100% {{ 
            text-shadow: 
              0 0 15px #ff6b35,
              0 0 25px #ff6b35,
              0 0 35px #ff6b35,
              2px 2px 4px rgba(0,0,0,0.8);
          }}
        }}
        .content {{
          margin-top: 100px;
        }}
        .marquee {{
          transition: transform 0.5s ease-in-out;
        }}
        .marquee.hidden {{
          transform: translateY(-100%);
        }}
        .content.no-marquee {{
          margin-top: 20px;
        }}
      </style>
      <script>
        let elapsed = {elapsed};
        let duration = {duration};
        let paused = {str(paused).lower()};
        let lastPlaybackState = null;

        function updateTime() {{
          if (!paused && elapsed < duration) {{
            elapsed++;
            let percent = Math.floor((elapsed / duration) * 100);
            document.querySelector('.bar').style.width = percent + '%';
            
            // Format time based on duration
            let elapsedTime, totalTime;
            
            if (duration < 3600) {{
              // Less than 1 hour: show mm:ss
              let elapsedMinutes = Math.floor(elapsed / 60);
              let elapsedSeconds = elapsed % 60;
              elapsedTime = elapsedMinutes.toString().padStart(2, '0') + ':' + elapsedSeconds.toString().padStart(2, '0');
              
              let totalMinutes = Math.floor(duration / 60);
              let totalSeconds = duration % 60;
              totalTime = totalMinutes.toString().padStart(2, '0') + ':' + totalSeconds.toString().padStart(2, '0');
            }} else {{
              // 1 hour or more: show hh:mm:ss
              let hours = Math.floor(elapsed / 3600);
              let minutes = Math.floor((elapsed % 3600) / 60);
              let seconds = elapsed % 60;
              elapsedTime = hours.toString().padStart(2, '0') + ':' + minutes.toString().padStart(2, '0') + ':' + seconds.toString().padStart(2, '0');
              
              let totalHours = Math.floor(duration / 3600);
              let totalMinutes = Math.floor((duration % 3600) / 60);
              let totalSeconds = duration % 60;
              totalTime = totalHours.toString().padStart(2, '0') + ':' + totalMinutes.toString().padStart(2, '0') + ':' + totalSeconds.toString().padStart(2, '0');
            }}
            
            // Update timer text, preserving the button
            const timeDisplay = document.getElementById('time-display');
            const button = timeDisplay.querySelector('#playback-button');
            const timeText = elapsedTime + ' / ' + totalTime;
            
            // Skip timer update if button update is in progress
            if (buttonUpdateInProgress) {{
              console.log('[DEBUG] Skipping timer update - button update in progress');
              return;
            }}
            
            if (button) {{
              // If button exists, replace all text content while preserving the button
              const buttonHTML = button.outerHTML;
              timeDisplay.innerHTML = buttonHTML + timeText;
              // Re-cache the button reference since we recreated it
              cachedButton = timeDisplay.querySelector('#playback-button');
              console.log(`[DEBUG] Timer updated, button re-cached: ${{!!cachedButton}}`);
            }} else {{
              // If no button, just update text
              timeDisplay.textContent = timeText;
              console.log(`[DEBUG] Timer updated without button`);
            }}
          }}
        }}

        function resyncTime() {{
          fetch('/nowplaying?json=1')
            .then(res => res.json())
            .then(data => {{
              elapsed = data.elapsed;
              duration = data.duration;
              paused = data.paused;
            }});
        }}

        let lastItemId = null;
        let lastPausedState = null;
        let cachedButton = null;
        let buttonUpdateInProgress = false;
        
        function getOrCreateButton() {{
          // Get time-display element
          const timeDisplay = document.getElementById('time-display');
          if (!timeDisplay) {{
            console.log('[ERROR] time-display element not found, cannot recreate button');
            return null;
          }}
          
          // Try to get cached button first
          if (cachedButton && document.contains(cachedButton)) {{
            return cachedButton;
          }}
          
          // Try to find existing button
          let button = document.getElementById('playback-button');
          if (button) {{
            cachedButton = button;
            return button;
          }}
          
          // Button not found, try to recreate it
          console.log('[DEBUG] Button not found, attempting to recreate...');
          if (timeDisplay) {{
            // Create new button element
            button = document.createElement('img');
            button.id = 'playback-button';
            button.src = '/play-button.png';
            button.alt = 'Play';
            button.style.cssText = 'width: 20px; height: 20px; opacity: 1; transition: opacity 0.5s ease; display: inline-block; vertical-align: middle; margin-right: 4px;';
            
            // Add error handling for failed image loads
            button.onerror = function() {{
              console.log('[DEBUG] Button image failed to load, trying to reload...');
              this.style.opacity = '0.5';
              // Retry loading the image after a short delay
              setTimeout(() => {{
                this.src = this.src + '?retry=' + Date.now();
              }}, 1000);
            }};
            
            button.onload = function() {{
              console.log('[DEBUG] Button image loaded successfully');
              this.style.opacity = '1';
            }};
            
            // Insert at the beginning of time-display
            timeDisplay.insertBefore(button, timeDisplay.firstChild);
            cachedButton = button;
            console.log('[DEBUG] Button recreated successfully');
            return button;
          }} else {{
            console.log('[ERROR] time-display element not found, cannot recreate button');
            return null;
          }}
        }}
        
        function updatePlaybackButton(paused) {{
          // Prevent multiple simultaneous button updates
          if (buttonUpdateInProgress) {{
            console.log('[DEBUG] Button update already in progress, skipping...');
            return;
          }}
          
          // Get time-display element for setTimeout callbacks
          const timeDisplay = document.getElementById('time-display');
          
          const button = getOrCreateButton();
          console.log(`[DEBUG] updatePlaybackButton called: paused=${{paused}}, button found=${{!!button}}`);
          if (button) {{
            console.log(`[DEBUG] Button current src: ${{button.src}}`);
            
            // Determine new image source
            const newSrc = paused ? '/pause-button.png' : '/play-button.png';
            const newAlt = paused ? 'Pause' : 'Play';
            
            // If the image is already correct, no need to change
            if (button.src.endsWith(newSrc.split('/').pop())) {{
              console.log('[DEBUG] Button image already correct, no change needed');
              return;
            }}
            
            // Mark button update as in progress
            buttonUpdateInProgress = true;
            
            // Fade out → change image → fade in
            button.style.opacity = '0';
            
            setTimeout(() => {{
              // Double-check button still exists after timeout
              const currentButton = timeDisplay.querySelector('#playback-button');
              if (currentButton) {{
                currentButton.src = newSrc;
                currentButton.alt = newAlt;
                console.log(`[DEBUG] Button new src: ${{currentButton.src}}`);
                
                // Fade back in
                setTimeout(() => {{
                  currentButton.style.opacity = '1';
                  buttonUpdateInProgress = false; // Mark update as complete
                }}, 50); // Small delay to ensure image loads
              }} else {{
                console.log('[DEBUG] Button disappeared during update, recreating...');
                buttonUpdateInProgress = false; // Reset flag before retry
                // Button was removed during transition, recreate it
                setTimeout(() => updatePlaybackButton(paused), 100);
              }}
            }}, 250); // Half of transition duration for smooth effect
            
            // Ensure button is visible
            button.style.display = 'inline-block';
          }} else {{
            console.log('[ERROR] Could not get or create playback button!');
          }}
        }}
        
        function checkPlaybackChange() {{
          fetch('/poll_playback')
            .then(res => {{
              if (!res.ok) {{
                throw new Error(`HTTP ${{res.status}}`);
              }}
              return res.json();
            }})
            .then(data => {{
              const currentState = data.playing;
              const currentItemId = data.item_id;
              const currentPaused = data.paused;
              
              console.log(`[DEBUG] Poll result: playing=${{currentState}}, item_id=${{currentItemId}}, lastItemId=${{lastItemId}}, paused=${{currentPaused}}`);
              
              // Update playback button based on pause state
              if (currentPaused !== lastPausedState) {{
                updatePlaybackButton(currentPaused);
                lastPausedState = currentPaused;
              }}
              
              // Check for playback state change (start/stop)
              if (lastPlaybackState === null) {{
                lastPlaybackState = currentState;
                lastItemId = currentItemId;
                lastPausedState = currentPaused;
                updatePlaybackButton(currentPaused);
                console.log(`[DEBUG] Initial state set: lastPlaybackState=${{lastPlaybackState}}, lastItemId=${{lastItemId}}, lastPausedState=${{lastPausedState}}`);
              }} else if (currentState !== lastPlaybackState) {{
                console.log(`[DEBUG] Playback state changed from ${{lastPlaybackState}} to ${{currentState}}`);
                document.body.classList.add('fade-out');
                setTimeout(() => {{
                  window.location.href = '/'; // Redirect to root when playback stops
                }}, 1500);
              }}
              // Check for item change (new track/episode while playing)
              else if (currentState && currentItemId && lastItemId && currentItemId !== lastItemId) {{
                console.log(`[DEBUG] Item changed from ${{lastItemId}} to ${{currentItemId}}`);
                document.body.classList.add('fade-out');
                setTimeout(() => {{
                  location.reload(true); // Reload to show new track/episode
                }}, 800);
              }}
              
              lastPlaybackState = currentState;
              lastItemId = currentItemId;
            }})
            .catch(error => {{
              console.error('Polling error:', error);
              setTimeout(checkPlaybackChange, 2000);
            }});
        }}

        function toggleMarquee() {{
          const marquee = document.querySelector('.marquee');
          const toggle = document.querySelector('.marquee-toggle');
          const content = document.querySelector('.content');
          
          marquee.classList.toggle('hidden');
          toggle.classList.toggle('hidden');
          
          if (marquee.classList.contains('hidden')) {{
            content.classList.add('no-marquee');
            toggle.innerHTML = '<div class="arrow up"></div>';
            toggle.title = 'Show Marquee';
          }} else {{
            content.classList.remove('no-marquee');
            toggle.innerHTML = '<div class="arrow"></div>';
            toggle.title = 'Hide Marquee';
          }}
        }}

        // Initialize button immediately and on DOM ready
        function initializeButton() {{
          console.log('[DEBUG] Initializing playback button');
          updatePlaybackButton(false); // Initialize as playing
        }}
        
        // Shimmer effect timer - trigger every 60 seconds
        function startShimmerTimer() {{
          setInterval(() => {{
            const marqueeText = document.querySelector('.marquee-text');
            if (marqueeText && !marqueeText.classList.contains('hidden')) {{
              console.log('[DEBUG] Triggering shimmer effect');
              
              // Remove any existing shimmer class first
              marqueeText.classList.remove('shimmer');
              
              // Reset all letter animations by temporarily removing and re-adding the class
              const letters = marqueeText.querySelectorAll('.letter');
              letters.forEach(letter => {{
                letter.style.animation = 'none';
              }});
              
              // Force a reflow to ensure the reset takes effect
              marqueeText.offsetHeight;
              
              // Clear the inline styles to let CSS take over
              letters.forEach(letter => {{
                letter.style.animation = '';
              }});
              
              // Add shimmer class
              marqueeText.classList.add('shimmer');
              
              // Remove shimmer class after animation completes
              setTimeout(() => {{
                marqueeText.classList.remove('shimmer');
                // Reset all letters to normal state
                const letters = marqueeText.querySelectorAll('.letter');
                letters.forEach(letter => {{
                  letter.style.animation = 'none';
                  letter.style.color = '';
                  letter.style.textShadow = '';
                }});
              }}, 6000); // Match animation duration (5s total)
            }}
          }}, 10000); // 10 seconds for testing
        }}
        
        // Wait for DOM to be ready before initializing
        function waitForDOM() {{
          if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', initializeAll);
          }} else {{
            initializeAll();
          }}
        }}
        
        function initializeAll() {{
          // Wait a bit more for all elements to be rendered
          setTimeout(() => {{
            initializeButton();
            startShimmerTimer();
          }}, 200);
        }}
        
        waitForDOM();
        
        setInterval(updateTime, 1000);
        setInterval(resyncTime, 5000);
        setInterval(checkPlaybackChange, 2000);
        
        // Fanart slideshow functionality
        setTimeout(function() {{
          let currentFanartIndex = 0;
          const fanartSlides = document.querySelectorAll('.fanart-slide');
          const totalFanarts = fanartSlides.length;
          
          console.log(`[DEBUG] Found ${{totalFanarts}} fanart slides`);
          
          function cycleFanarts() {{
            if (totalFanarts <= 1) return;
            
            console.log(`[DEBUG] Cycling fanarts - current: ${{currentFanartIndex}}, next: ${{(currentFanartIndex + 1) % totalFanarts}}`);
            
            const currentSlide = fanartSlides[currentFanartIndex];
            currentSlide.classList.remove('active');
            currentSlide.classList.add('fade-out');
            
            currentFanartIndex = (currentFanartIndex + 1) % totalFanarts;
            
            const nextSlide = fanartSlides[currentFanartIndex];
            nextSlide.classList.remove('fade-out');
            nextSlide.classList.add('active');
            
            console.log(`[DEBUG] Now showing fanart ${{currentFanartIndex}}`);
          }}
          
          // Start slideshow if we have multiple fanarts
          if (totalFanarts > 1) {{
            console.log('[DEBUG] Starting fanart slideshow with 20 second intervals');
            setInterval(cycleFanarts, 20000); // Change every 20 seconds
          }} else {{
            console.log('[DEBUG] Not enough fanarts for slideshow');
          }}
        }}, 100); // Wait 100ms for DOM to be ready
      </script>
    </head>
    <body>
      <!-- Fanart Slideshow Container -->
      <div class="fanart-container">
        {''.join([f'<div class="fanart-slide{" active" if i == 0 else ""}" style="background-image: url(\'{fanart}\')"></div>' for i, fanart in enumerate(fanart_variants)]) if fanart_variants else ''}
      </div>
      
      <div class="marquee">
        <div class="marquee-text"><span class="letter">N</span><span class="letter">O</span><span class="letter">W</span><span class="letter">&nbsp;</span><span class="letter">P</span><span class="letter">L</span><span class="letter">A</span><span class="letter">Y</span><span class="letter">I</span><span class="letter">N</span><span class="letter">G</span></div>
        <div class="marquee-toggle" onclick="toggleMarquee()" title="Hide Marquee">
          <div style="color: white; font-size: 16px; font-weight: bold;">▲</div>
        </div>
      </div>
      <div class="content">
        <div class="left-section">
          <div class="poster-container">
            {f"<img class='show-poster' src='{show_poster_url}' />" if show_poster_url else ""}
            {f"<img class='season-poster' src='{season_poster_url}' />" if season_poster_url else ""}
          </div>
          <div>
            {f"<img class='logo' src='{clearlogo_url}' />" if clearlogo_url else (f"<img class='banner' src='{banner_url}' />" if banner_url else f"<h2 style='margin-bottom: 4px;'>📺 {show}</h2>")}
            
            <div class="episode-info">
              {f"<div class='show-title'>{show}</div>" if not clearlogo_url and not banner_url else ""}
              <div class="episode-badges">
                {f"<span class='badge episode-badge'>{season_badge}</span>" if season_badge else ""}
                {f"<span class='badge episode-badge'>{episode_badge}</span>" if episode_badge else ""}
                {f"<span class='badge episode-badge'>{title_badge}</span>" if title_badge else ""}
              </div>
            </div>
            
            {f"<p><strong>Director:</strong> {director_names}</p>" if director_names and director_names != "N/A" else ""}
            {f"<p><strong>Cast:</strong> {cast_names}</p>" if cast_names and cast_names != "N/A" else ""}
            {f"<h3 style='margin-top:20px;'>Plot</h3><p style='max-width:600px;'>{plot}</p>" if plot and plot.strip() else ""}
            <div class="badges">
              {rating_html}
              <a href="{imdb_url}" target="_blank" class="badge-imdb">
                <span>IMDb</span>
              </a>
              <span class="badge">{resolution}</span>
              <span class="badge">{video_codec}</span>
              <span class="badge">{audio_codec} {channels}ch</span>
              <span class="badge">HDR: {hdr_type}</span>
              <span class="badge">Audio: {audio_languages}</span>
              <span class="badge">Subs: {subtitle_languages}</span>
              {"".join(f"<span class='badge'>{g}</span>" for g in genre_badges)}
            </div>
            <div class="progress">
              <div class="bar"></div>
            </div>
            <div class="badges">
              <span class="badge" id="time-display" style="display: flex; align-items: center; gap: 8px;">
                <img id="playback-button" src="/play-button.png" alt="Play" style="width: 20px; height: 20px; opacity: 1; transition: opacity 0.5s ease;">
                {f"{elapsed//60:02d}:{elapsed%60:02d}" if duration < 3600 else f"{elapsed//3600:02d}:{(elapsed//60)%60:02d}:{elapsed%60:02d}"} / {f"{duration//60:02d}:{duration%60:02d}" if duration < 3600 else f"{duration//3600:02d}:{(duration//60)%60:02d}:{duration%60:02d}"}
              </span>
            </div>
          </div>
        </div>
        <!-- Clearart removed as requested -->
      </div>
    </body>
    </html>
    """
    return html
